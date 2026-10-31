# 01 — Module Scaffold & Manifest

## Context
This is the very first file to create. It sets up the Odoo 18 custom module skeleton — the `__manifest__.py` (module metadata, dependencies, data files) and root `__init__.py`. Every subsequent file depends on this scaffold existing. The module is called `subscription_management` and will live in the custom addons directory.

## Prompt for Antigravity

```
Create an Odoo 18 custom module scaffold for a module called "subscription_management". This module is a Subscription Management System for a software company called "Brightloop Software".

Create these files in E:\odoo18\custom_addons\subscription_management\:

### File 1: __manifest__.py

Create the module manifest with these exact settings:

{
    'name': 'Subscription Management',
    'version': '18.0.1.0.0',
    'category': 'Sales/Subscriptions',
    'summary': 'Manage software subscriptions, billing, invoicing, and payments',
    'description': """
        Subscription Management System for Brightloop Software
        ======================================================
        - Product & variant management
        - Subscription plans (daily/weekly/monthly/yearly)
        - Subscription lifecycle (Draft → Quotation → Confirmed → Active → Closed)
        - Automated invoicing and billing
        - Tax and discount rule engine
        - Payment tracking
        - Portal access for customers
    """,
    'author': 'Brightloop Software',
    'website': 'https://www.brightloop.com',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'portal'],
    'data': [
        # Security
        'security/subscription_security.xml',
        'security/ir.model.access.csv',
        'security/subscription_record_rules.xml',
        # Data
        'data/sequences.xml',
        'data/cron.xml',
        'data/mail_templates.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

### File 2: __init__.py (root level)

from . import models

### File 3: models/__init__.py (placeholder — will be updated as models are added)

# Models will be imported here as they are created
# from . import product
# from . import plan
# from . import subscription
# from . import subscription_line
# from . import quotation_template
# from . import invoice
# from . import invoice_line
# from . import tax
# from . import discount
# from . import payment

### File 4: Create empty directories with placeholder files

Create these empty directories (with empty __init__.py or .gitkeep files where needed):
- security/ (create an empty placeholder)
- data/ (create an empty placeholder)
- views/ (create an empty placeholder)

Use standard Odoo 18 conventions:
- Use 'license': 'LGPL-3'
- Use proper version format: '18.0.1.0.0'
- The module should be marked as 'application': True since it's a standalone app
- Include 'mail' in depends for chatter support
- Include 'portal' in depends for customer portal access
```

## Expected Output

```
subscription_management/
├── __init__.py
├── __manifest__.py
├── models/
│   └── __init__.py
├── security/
├── data/
└── views/
```

## Verification

1. Check that `__manifest__.py` is valid Python (no syntax errors):
   ```bash
   python -c "exec(open('__manifest__.py').read())"
   ```
2. Check `__init__.py` imports models package.
3. **Do NOT try to install the module yet** — the data files referenced in manifest don't exist yet. That's expected. We'll install after security files are created (files 12-14).
