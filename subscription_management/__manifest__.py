# -*- coding: utf-8 -*-
{
    'name': 'Subscription Management System',
    'version': '18.0.1.0.0',
    'category': 'Sales/Subscriptions',
    'summary': 'Unified Subscription Lifecycle, Invoicing, Recurring Billing, and Customer Portal for Brightloop Software',
    'description': """
Subscription Management System for Brightloop Software
======================================================
- Product & Brand Variant Management (Dynamic price add-on such as Brand Odoo +₹560)
- Subscription Plans (Daily, Weekly, Monthly, Yearly)
- Subscription Lifecycle (Draft -> Quotation -> Confirmed -> Active -> Paused -> Closed)
- Standardized Quotation Templates
- Automated Invoicing & Duplicate Billing Prevention
- Configurable Tax & Promotional / Volume Discount Rules
- Multi-Method Payment Reconciliation (Bank Transfer, UPI, Credit Card, Cash, Cheque)
- Secure Multi-Role Authentication (Admin, Staff, Customer Portal) with Password Enforcement
- Customer Self-Service Portal (/my/subscriptions, /my/invoices)
- Scheduled Automated Cron Jobs (Billing & Auto-Close on Expiry)
    """,
    'author': 'Neeraj & Brightloop Team',
    'website': 'https://www.brightloop.com',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'portal'],
    'data': [
        'security/subscription_security.xml',
        'security/ir.model.access.csv',
        'security/subscription_record_rules.xml',
        'data/sequences.xml',
        'data/cron.xml',
        'data/email_templates.xml',
        'views/auth_templates.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
