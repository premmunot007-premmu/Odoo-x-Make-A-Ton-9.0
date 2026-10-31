# Professional .gitignore for Odoo 18 & Python Development

## Context
Ensure team members do not commit compiled python files, local database dumps, temporary IDE settings, or OS-specific files.

## Prompt for Antigravity

```markdown
Create `.gitignore` in the repository root:

```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environments
venv/
.venv/
env/
ENV/

# IDE & Editors
.idea/
.vscode/
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# Odoo Runtime & Filestore
*.log
odoo.log
odoo-server.log
sessions/
filestore/
*.dump
*.sql

# Antigravity & Scratch Artifacts
.gemini/
scratch/
temp/
*.pdf.txt
```
```

## Expected Output
- `.gitignore` in root

## Verification
Run `git status` to ensure `.pyc` and editor files are ignored.
