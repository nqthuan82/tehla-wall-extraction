import os

with open('SKILL.md', encoding='utf-8') as f:
    content = f.read()

assert content.startswith('---'), 'Missing frontmatter'
assert 'name:' in content, 'Missing name'
assert 'description:' in content, 'Missing description'

tokens = len(content) // 4
print(f'  SKILL.md: {len(content.splitlines())} lines, ~{tokens} tokens')
assert tokens < 3500, f'SKILL.md qua lon: {tokens} tokens (max 3500)'

for ref in ['stop-and-ask.md', 'wall-height-openings.md', 'hranice-poziarnych.md']:
    path = f'references/{ref}'
    assert os.path.exists(path), f'Missing: {path}'
    t = len(open(path, encoding='utf-8').read()) // 4
    print(f'  references/{ref}: ~{t} tokens')

print('Validation OK')
