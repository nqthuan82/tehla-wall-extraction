import glob

total = 0
for f in ['SKILL.md'] + glob.glob('references/*.md'):
    t = len(open(f, encoding='utf-8').read()) // 4
    total += t
    print(f'{f}: ~{t} tokens')
print(f'TONG: ~{total} tokens')
