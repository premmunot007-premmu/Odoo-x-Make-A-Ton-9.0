# Asset Bundles, Demo Data Registration & UX Manifest Assembly

## Context
Prem ensures all demo files, wizard views, SCSS styling, and JavaScript assets are properly wired in the module manifest so that demo data loads when `--dev=all` or demo mode is active.

## Prompt for Antigravity

```markdown
In our Odoo 18 module `subscription_management`:

1. Update `__manifest__.py` to declare both production `data` and `demo` datasets:
```python
{
    'name': 'Subscription Management System',
    'version': '18.0.1.0.0',
    'category': 'Sales/Subscriptions',
    'summary': 'Unified subscription, recurring billing, invoices, payments, portal and executive dashboard for Brightloop Software',
    'author': 'Brightloop Team',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'portal', 'web'],
    'data': [
        'security/subscription_security.xml',
        'security/ir.model.access.csv',
        'security/subscription_record_rules.xml',
        'data/sequences.xml',
        'data/cron.xml',
        'data/email_templates.xml',
        'wizard/payment_wizard_views.xml',
        'views/auth_templates.xml',
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
    'demo': [
        'data/demo_products.xml',
        'data/demo_plans.xml',
        'data/demo_customers.xml',
        'data/demo_discounts_taxes.xml',
        'data/demo_subscriptions.xml',
        'data/demo_invoices.xml',
        'data/demo_payments.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'subscription_management/static/src/js/dashboard.js',
            'subscription_management/static/src/xml/dashboard.xml',
            'subscription_management/static/src/scss/dashboard.scss',
        ],
        'web.assets_frontend': [
            'subscription_management/static/src/scss/portal.scss',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
```

2. Verify file paths and ensure no missing files or XML syntax errors.
```

## Expected Output
- Complete, error-free `__manifest__.py`

## Verification
Update module with demo data:
```bash
python odoo-bin -c odoo.conf -u subscription_management --stop-after-init
```
Verify all views, demo records, wizards, and assets load into PostgreSQL without errors.
