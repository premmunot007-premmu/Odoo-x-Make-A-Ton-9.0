# -*- coding: utf-8 -*-
{
    'name': 'Subscription Management System',
    'version': '18.0.1.0.0',
    'category': 'Sales/Subscriptions',
    'summary': 'Unified subscription management with billing, invoicing, payments, and customer portal',
    'description': """
Subscription Management System
==============================

Brightloop Software sells its products on a recurring basis and needs a single
place to manage the full subscription lifecycle instead of juggling
spreadsheets, manual invoices and disconnected payment tracking.

This module provides:

* Subscription plans with configurable billing periods (monthly, yearly, etc.)
* Customer subscriptions with a clear lifecycle: draft, quotation, confirmed,
  in progress, closed
* Recurring billing and automatic invoice generation
* Payment tracking against subscription invoices
* Discounts, taxes and product variants on subscription lines
* A customer portal where subscribers can view their subscriptions, invoices
  and payment history
* Reports on recurring revenue, active subscriptions and overdue payments
    """,
    'author': 'Team Brightloop',
    'website': 'https://github.com/your-repo',
    'depends': ['base', 'mail', 'portal', 'web'],
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
    'demo': [],
    'assets': {
        'web.assets_backend': [
            'subscription_management/static/src/js/dashboard.js',
            'subscription_management/static/src/xml/dashboard.xml',
            'subscription_management/static/src/scss/dashboard.scss',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
