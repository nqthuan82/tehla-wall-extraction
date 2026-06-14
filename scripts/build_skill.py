import os
import zipfile

SKILL_NAME = 'tehla-wall-extraction'
DIST_DIR = 'dist'
EXCLUDE_DIRS = {'.git', 'dist', '__pycache__', '.claude'}
EXCLUDE_FILES = {'.DS_Store'}

os.makedirs(DIST_DIR, exist_ok=True)
out_path = os.path.join(DIST_DIR, f'{SKILL_NAME}.skill')

with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for name in files:
            if name in EXCLUDE_FILES or name.endswith('.pyc'):
                continue
            path = os.path.join(root, name)
            arcname = os.path.join(SKILL_NAME, os.path.relpath(path, '.'))
            zf.write(path, arcname)

print(f'Built: {out_path}')
