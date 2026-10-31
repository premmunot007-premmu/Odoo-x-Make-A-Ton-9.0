# -*- coding: utf-8 -*-
{
    'name': 'Subscription Management System',
    'version': '18.0.1.0.0',
    'category': 'Sales/Subscriptions',
    'summary': 'Unified subscription, recurring billing, invoices, payments, portal and executive dashboard for Brightloop Software',
    'description': """
Subscription Management System for Brightloop Software
======================================================
Comprehensive enterprise subscription lifecycle management for Odoo 18:
- Product and variant catalog with tiered brand attributes
- Flexible recurring plans (daily, weekly, monthly, quarterly, annual)
- Subscriptions state machine: Draft -> Quotation -> Confirmed -> Active -> Paused -> Closed -> Expired
- Automated mass billing engine and sequence generators
- Invoicing with tax calculation, discounts, and payment tracking
- Pop-up Register Payment wizard
- Customer portal with responsive UX and status badging
- High-performance OWL executive KPI dashboard with real-time operational feeds
- Formal QWeb printable PDF reports for Invoices and Subscription contracts
    """,
    'author': 'Brightloop Team',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'portal', 'web'],
    'data': [
        'security/subscription_security.xml',
        'security/ir.model.access.csv',
        'security/subscription_record_rules.xml',
        'data/sequences.xml',
        'data/default_config.xml',
        'data/cron.xml',
        'data/email_templates.xml',
        'wizard/payment_wizard_views.xml',
        'views/auth_templates.xml',
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
        'views/menu.xml',
        'data/demo_customers.xml',
        'data/demo_products.xml',
        'data/demo_plans.xml',
        'data/demo_discounts_taxes.xml',
        'data/demo_subscriptions.xml',
        'data/demo_invoices.xml',
        'data/demo_payments.xml',
    ],
    'demo': [],
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
