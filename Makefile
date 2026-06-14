SKILL_DIR = .
DIST_DIR  = dist
PYTHON   := $(shell python3 -c "import sys" >/dev/null 2>&1 && echo python3 || echo python)

build:
	@$(PYTHON) scripts/build_skill.py

validate:
	@echo "Checking SKILL.md frontmatter..."
	@$(PYTHON) scripts/validate_skill.py

count-tokens:
	@$(PYTHON) scripts/count_tokens.py

clean:
	rm -rf $(DIST_DIR)
