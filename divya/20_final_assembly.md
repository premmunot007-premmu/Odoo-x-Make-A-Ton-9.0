# Final Assembly — Sequences, Config Data & Manifest

## Context
Final file: ensure all data files, sequences, default config are in place. Update __manifest__.py with the complete list of all data files, views, reports, and assets.

## Prompt for Claude Code

```
In the Odoo 18 module "subscription_management", do the final assembly.

1. Create `data/default_config.xml`:
- Default tax: GST 18% (subscription.tax record)
- Default payment term note

2. Verify/create `data/sequences.xml` has:
- Subscription sequence: SUB/%(year)s/%(month)s/ padding 4
- Invoice sequence: INV/%(year)s/%(month)s/ padding 4

3. Create/update `data/cron.xml` with both cron jobs (auto-close + billing)

4. Create `views/discount_views.xml`:
- Tree: name, discount_type, amount, date_start, date_end, current_usage, max_usage, is_active
- Form: all fields with date pickers, many2many_tags for product_ids
- Search: filter active/expired

5. Create `views/tax_views.xml`:
- Simple tree and form views

6. Create `views/quotation_template_views.xml`:
- Form with inline template lines, tree view

7. Update `__manifest__.py` with COMPLETE data list:
'data': [
    'security/subscription_security.xml',
    'security/ir.model.access.csv',
    'security/subscription_record_rules.xml',
    'data/sequences.xml',
    'data/cron.xml',
    'data/default_config.xml',
    'views/menu.xml',
    'views/product_views.xml',
    'views/plan_views.xml',
    'views/subscription_views.xml',
    'views/invoice_views.xml',
    'views/payment_views.xml',
    'views/discount_views.xml',
    'views/tax_views.xml',
    'views/quotation_template_views.xml',
    'views/portal_templates.xml',
    'reports/invoice_report.xml',
    'reports/subscription_report.xml',
],
'assets': {
    'web.assets_backend': [
        'subscription_management/static/src/js/dashboard.js',
        'subscription_management/static/src/xml/dashboard.xml',
        'subscription_management/static/src/scss/dashboard.scss',
    ],
},

8. Update ALL `__init__.py` files:
models/__init__.py should import: product, plan, subscription, subscription_line, invoice, tax, discount, payment, quotation_template
controllers/__init__.py should import: portal

9. Final check: ensure every model has its _name, _description, and all imports (models, fields, api, exceptions).

Run a full install test:
python odoo-bin -c odoo.conf -i subscription_management --test-enable --stop-after-init
```

## Expected Output
- `data/default_config.xml`
- `views/discount_views.xml`
- `views/tax_views.xml`
- `views/quotation_template_views.xml`
- Updated `__manifest__.py` (complete)
- Updated all `__init__.py` files

## Verification
```bash
python odoo-bin -c odoo.conf -i subscription_management --stop-after-init
# Should install cleanly with 0 errors
# All menus, views, and features should work
```
