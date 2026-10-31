# Divya — Setup Guide (Claude Code Pro)

## Your Role
You are the **Core Engine Architect**. You build ALL backend models, security, views, dashboard, portal, and reports using **Claude Code Pro**.

## Step-by-Step Setup

### 1. Install Odoo 18 Development Environment
```bash
# Install Python 3.10+
# Install PostgreSQL 16
# Create database user
sudo -u postgres createuser -s odoo
sudo -u postgres createdb odoo18

# Clone Odoo 18
git clone https://github.com/odoo/odoo.git --depth 1 --branch 18.0 ~/odoo18
cd ~/odoo18
pip install -r requirements.txt

# Create custom addons folder
mkdir -p ~/odoo18/custom_addons/subscription_management
```

### 2. Git Workflow
```bash
git checkout -b divya/core-engine
# After each .md file is done:
git add .
git commit -m "feat(core): <description>"
git push origin divya/core-engine
```

### 3. How to Use These Files with Claude Code
1. Open Claude Code terminal
2. Open file 01 → copy the **"Prompt for Claude Code"** section
3. Paste into Claude Code
4. Review the generated code
5. Save files to `~/odoo18/custom_addons/subscription_management/`
6. Test: `python odoo-bin -c odoo.conf -u subscription_management --test-enable`
7. Commit → move to next file

### 4. Execution Order
Follow files 01→20 **strictly in order**. Each builds on the previous.

### 5. External Resources Needed
- **No external APIs needed** — everything is Odoo built-in
- PostgreSQL must be running locally
- Odoo 18 source code cloned
