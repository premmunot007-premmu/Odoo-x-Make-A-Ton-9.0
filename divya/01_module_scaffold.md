# Module Scaffold — __manifest__.py & __init__.py

## Context
This is the foundation file for the entire Odoo 18 custom module. Every other file depends on this existing first.

## Prompt for Claude Code

```
Create an Odoo 18 custom module called "subscription_management" in the current directory. Create these files:

1. `__manifest__.py` with:
   - name: "Subscription Management System"
   - version: "18.0.1.0.0"
   - category: "Sales/Subscriptions"
   - summary: "Unified subscription management with billing, invoicing, payments, and customer portal"
   - description: Long description about Brightloop Software's subscription management needs
   - author: "Team Brightloop"
   - website: "https://github.com/your-repo"
   - depends: ['base', 'mail', 'portal', 'web']
   - data: [] (empty for now, we'll add files as we create them)
   - demo: []
   - assets: {}
   - installable: True
   - application: True
   - auto_install: False
   - license: "LGPL-3"

2. `__init__.py` that imports:
   - from . import models
   - from . import controllers
   - from . import wizard

3. `models/__init__.py` (empty, will be populated later)
4. `controllers/__init__.py` (empty)
5. `wizard/__init__.py` (empty)
6. `security/` directory (empty)
7. `data/` directory (empty)
8. `views/` directory (empty)
9. `reports/` directory (empty)
10. `static/src/js/` directory (empty)
11. `static/src/xml/` directory (empty)
12. `static/src/scss/` directory (empty)
13. `static/description/icon.png` — create a placeholder or note that an icon is needed

Use Odoo 18 conventions. The module should install without errors even if data files are empty.
```

## Expected Output
- `__manifest__.py`
- `__init__.py`
- `models/__init__.py`
- `controllers/__init__.py`
- `wizard/__init__.py`
- Empty directories: `security/`, `data/`, `views/`, `reports/`, `static/src/`

## Verification
```bash
python odoo-bin -c odoo.conf -i subscription_management
# Module should install without errors
```
