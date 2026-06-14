# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This is a **Claude Agent Skill package**, not an application. The "code" is a set of
instructions (`SKILL.md` + `references/*.md`) that get loaded into a future Claude
session whenever a user uploads an architectural PDF/CAD drawing and asks about brick
walls (tehlové murivo / tehla). The instructions are written in Vietnamese; all
generated *output* (Excel/PDF reports) must be in Slovak.

The Makefile/`scripts/` here are tooling to validate and package *this skill itself* —
they are unrelated to the wall-extraction logic the skill performs at runtime.

## Commands

```bash
make validate      # check SKILL.md frontmatter + enforce token budgets
make count-tokens   # print token estimate for SKILL.md and each references/*.md
make build          # package the repo into dist/tehla-wall-extraction.skill
make clean          # remove dist/
```

Notes:
- `make` is not installed by default on Windows; install via `winget install GnuWin32.Make`
  and ensure `C:\Program Files (x86)\GnuWin32\bin` is on PATH.
- The Makefile auto-selects `python3` or `python` (`PYTHON` variable) — on this machine
  `python3` is a non-functional Windows Store stub, so it falls back to `python`.
- `make build` deliberately does **not** shell out to `zip` — on Windows `zip` may
  resolve to 7-Zip's incompatible CLI, so `scripts/build_skill.py` uses Python's
  `zipfile` module instead. It excludes `.git`, `dist`, `.claude`, `__pycache__`,
  `.DS_Store`.

## Architecture

### `SKILL.md` — entry point
- YAML frontmatter (`name`, `description`) is what Claude uses to **auto-activate**
  this skill; the `description` must keep mentioning the trigger conditions (PDF/CAD
  upload + tehla/murivo/POROTHERM/priečky keywords) and the tehla-vs-ŽB ambiguity.
- Hard token budget: `scripts/validate_skill.py` asserts `len(SKILL.md) // 4 < 3500`
  tokens. Keep additions terse; move detail into `references/`.
- Body is a numbered workflow (BƯỚC 0–8) that a future Claude instance follows when
  processing a drawing:
  - BƯỚC 0: render PDF to images (`pdftoppm`), set output directory = input filename
    (without extension) — all outputs for a run go under `<input_basename>/`.
  - BƯỚC 1: read the materials legend — **must not skip**, governs the tehla-vs-ŽB
    color rules table.
  - BƯỚC 2: `is_tehla_wall()` pixel-color heuristic (red hatch = tehla, grey/black =
    ŽB/concrete).
  - BƯỚC 3: derive px↔mm scale from dimension lines, locate walls via dark-pixel rows.
  - BƯỚC 4 / 4b: classify walls by location; read real S.H. (ceiling height) per room
    and real opening (door/window) sizes — never default to 3.000 m.
  - BƯỚC 5: shared-wall accounting (Method 2 — count in both rooms, mark `[1]`/`[2]`,
    only `[1]` rows feed subtotals).
  - BƯỚC 6: `Čistá plocha = (Dĺžka × Výška) − Σ otvor` (Excel formula must be `=E-F`,
    never self-referencing `=F-G`).
  - BƯỚC 7/8: Excel column layout + row color coding, and PDF overlay color map.

### `references/*.md` — loaded on demand, referenced by name from SKILL.md
- `stop-and-ask.md` — the 7 situations where Claude **must stop and ask the user**
  rather than guess (unclear material symbol, missing S.H., unreadable opening
  dimensions, unclear wall thickness, ambiguous drawing, wall on a material boundary,
  symbol not in legend). Includes the required question format and how to record
  user-confirmed values in the `Poznámka` column.
- `wall-height-openings.md` — how to read `S.H.`/`H.H.`/`T.I.` ceiling-height markers
  and compute wall height; the 4 prioritized sources for opening (door/window)
  dimensions and which openings count as deductions.
- `hranice-poziarnych.md` — disambiguates fire-compartment boundary lines (orange
  dash-dot, thin) from tehla brick hatch (solid dark red, thick) — both can appear
  reddish in a render but only the latter counts as wall area.

### Core domain invariant
Only **solid red/dark-red hatch** = tehla (counts toward billable area). Black/grey
lines and fills = ŽB (reinforced concrete) or betón — never counted. This distinction
drives BƯỚC 1, BƯỚC 2, and `hranice-poziarnych.md`, and getting it wrong is the
highest-impact error category listed in SKILL.md's "CÁC LỖI PHỔ BIẾN" table.

## Editing this skill

After changing `SKILL.md` or any `references/*.md`, run `make validate` to confirm
the token budget and required reference files are still satisfied before committing.

### Token optimization

Every token in `SKILL.md` is loaded into context on **every** activation, so it is
the most expensive file in this repo per byte. When developing/extending this skill:
- Keep `SKILL.md` as a terse checklist/workflow; push detailed explanations, examples,
  and edge cases into `references/*.md`, which are only read when explicitly needed.
- Run `make count-tokens` before and after edits to see the impact, and `make validate`
  to enforce the <3500-token ceiling on `SKILL.md`.
- Prefer tables and short code snippets over prose; avoid repeating rules that already
  live in a `references/` file — link to it instead.
- When trimming, prioritize cutting redundancy over cutting the stop-and-ask rules,
  color-distinction tables, or formula warnings — those prevent the costly errors
  listed in "CÁC LỖI PHỔ BIẾN".
