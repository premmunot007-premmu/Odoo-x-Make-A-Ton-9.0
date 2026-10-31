# Project Architecture & Directory Structure Guide

## Context
Provide complete developer documentation in `docs/PROJECT_STRUCTURE.md` explaining the responsibility of each folder and file within the `subscription_management` module.

## Prompt for Antigravity

```markdown
Create `docs/PROJECT_STRUCTURE.md` documenting the repository layout:

```markdown
# 📂 Subscription Management Module Architecture

The module `subscription_management` follows modern Odoo 18 MVC architecture:

```
subscription_management/
├── __init__.py                # Root python module initialization
├── __manifest__.py            # Module descriptor, metadata, dependencies & asset registry
├── models/                    # ORM Models (Business Logic & Schema)
│   ├── __init__.py
│   ├── product.py             # Products & Product Variants (+₹560 brand logic)
│   ├── plan.py                # Billing frequencies, min seats, auto-close policies
│   ├── subscription.py        # Core state machine, sequences, mass billing cron
│   ├── subscription_line.py   # Subscription items, tax & discount auto-calculation
│   ├── quotation_template.py  # Standardized sales quotation templates
│   ├── invoice.py             # Invoices generated from subscriptions
│   ├── invoice_line.py        # Itemized invoice lines with taxes
│   ├── payment.py             # Multi-method payments and balance reconciliation
│   ├── tax.py                 # Tax rules (fixed/percentage)
│   ├── discount.py            # Tiered & promotional discount rules
│   └── res_users.py           # Strong password enforcement & reset tokens
├── controllers/               # HTTP & Web Controllers
│   ├── __init__.py
│   ├── auth.py                # Public registration, password validation & login
│   └── portal.py              # Customer self-service portal (/my/subscriptions)
├── wizard/                    # Pop-up dialogs
│   ├── __init__.py
│   ├── payment_wizard.py      # Transient model to record invoice payments
│   └── payment_wizard_views.xml
├── views/                     # XML Views & Actions
│   ├── menu.xml               # Top bar menu hierarchy
│   ├── product_views.xml      # Tree, form, kanban & search for products
│   ├── plan_views.xml         # Tree, form for subscription plans
│   ├── subscription_views.xml # Color-coded tree, kanban by state, form with chatter
│   ├── invoice_views.xml      # Invoice views with payment status badges
│   ├── payment_views.xml      # Payment list and details
│   ├── discount_views.xml     # Rules configuration views
│   ├── tax_views.xml          # Tax configuration views
│   ├── quotation_template_views.xml
│   ├── auth_templates.xml     # QWeb templates for signup & login
│   └── portal_templates.xml   # QWeb templates for customer portal
├── security/                  # Access Control & Security
│   ├── subscription_security.xml # RBAC Groups (Admin, Staff, Customer Portal)
│   ├── ir.model.access.csv       # Model CRUD permissions matrix
│   └── subscription_record_rules.xml # Multi-tenant domain isolation
├── data/                      # Initial & Scheduled System Data
│   ├── sequences.xml          # SUB/2026/... and INV/2026/... sequences
│   ├── cron.xml               # Daily mass billing & auto-close cron jobs
│   ├── email_templates.xml    # QWeb transactional email templates
│   ├── demo_products.xml      # Sample products and variants
│   ├── demo_plans.xml         # Sample billing plans
│   ├── demo_customers.xml     # Sample partner records
│   ├── demo_subscriptions.xml # Multi-state subscriptions
│   ├── demo_invoices.xml      # Sample invoices (paid, confirmed, overdue)
│   └── demo_payments.xml      # Sample payments
├── reports/                   # Printable PDF Reports (QWeb)
│   ├── invoice_report.xml     # Printable invoice PDF with taxes & totals
│   └── subscription_report.xml# Subscription contract summary PDF
├── static/                    # Frontend Assets (OWL & SCSS)
│   ├── description/
│   │   └── icon.png           # App icon
│   └── src/
│       ├── js/
│       │   └── dashboard.js   # OWL Component for Executive KPI Dashboard
│       ├── xml/
│       │   └── dashboard.xml  # OWL Template for Dashboard
│       └── scss/
│           ├── dashboard.scss # Dashboard KPI card hover effects & styling
│           └── portal.scss    # Custom responsive portal styling
└── tests/                     # Automated Test Suites
    ├── __init__.py
    ├── test_product.py
    ├── test_subscription.py
    ├── test_invoice.py
    └── test_auth_discount.py
```
```
```

## Expected Output
- `docs/PROJECT_STRUCTURE.md`
