# Customer Portal Custom Styling & UX

## Context
Customers manage their subscriptions and invoices online through the Odoo customer portal. Prem enhances the UX with custom SCSS styling for status chips, action buttons, cards, and invoice lists.

## Prompt for Antigravity

```markdown
In our Odoo 18 module `subscription_management`, create `static/src/scss/portal.scss`:

```scss
// Portal Subscription & Billing Styling
.o_portal_subscription {
    .sub_header_card {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: #ffffff;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 15px rgba(30, 58, 138, 0.15);
        margin-bottom: 24px;

        h2 {
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 8px;
        }

        .sub_status_badge {
            font-size: 0.85rem;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            text-transform: uppercase;
        }
    }

    .badge_state_active { background-color: #10b981; color: white; }
    .badge_state_draft { background-color: #6b7280; color: white; }
    .badge_state_confirmed { background-color: #3b82f6; color: white; }
    .badge_state_paused { background-color: #f59e0b; color: white; }
    .badge_state_closed { background-color: #ef4444; color: white; }

    .line_table {
        background: white;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #e5e7eb;

        th {
            background-color: #f9fafb;
            font-weight: 600;
            color: #374151;
            padding: 12px 16px;
        }

        td {
            padding: 12px 16px;
            vertical-align: middle;
        }
    }

    .totals_box {
        background: #f8fafc;
        border-radius: 8px;
        padding: 16px;
        border: 1px solid #e2e8f0;

        .total_row {
            display: flex;
            justify-content: space-between;
            padding: 6px 0;
            font-size: 0.95rem;

            &.grand_total {
                font-size: 1.25rem;
                font-weight: 700;
                color: #1e293b;
                border-top: 2px solid #cbd5e1;
                margin-top: 8px;
                padding-top: 8px;
            }
        }
    }
}
```

Update `__manifest__.py` under `assets` to include `web.assets_frontend`:
```python
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
```
```

## Expected Output
- `static/src/scss/portal.scss`
- Manifest updated with `web.assets_frontend`

## Verification
Login as a portal user and visit `/my/subscriptions/1`. The page should render with styled cards and badge indicators.
