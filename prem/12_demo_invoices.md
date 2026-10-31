# Demo Invoices Data

## Context
Invoices generated from subscriptions can be in Draft, Confirmed, Paid, or Overdue states. This demo file populates invoices to test billing reconciliation and the finance dashboard.

## Prompt for Antigravity

```markdown
In our Odoo 18 module `subscription_management`, create `data/demo_invoices.xml`:

Create demo `subscription.invoice` records:
1. `inv_paid_last_month`:
   - partner_id: `customer_small_shop`
   - subscription_id: `sub_active_acuity`
   - invoice_date: First day of current month
   - due_date: 15 days ago
   - state: "paid"
   - lines: 1x CRM (1200), 1x Storage (250) + GST 18%

2. `inv_confirmed_outstanding`:
   - partner_id: `customer_enterprise_corp`
   - subscription_id: `sub_active_starlight`
   - invoice_date: 5 days ago
   - due_date: 25 days in future
   - state: "confirmed"
   - lines: 25x Enterprise Suite (unit: 4060) + 1x VIP Support (1500)

3. `inv_overdue_urgent`:
   - partner_id: `customer_retail_chain`
   - subscription_id: `sub_paused_urbancart`
   - invoice_date: 45 days ago
   - due_date: 15 days ago
   - state: "confirmed"
   - note: "Payment overdue by 15 days - 2nd reminder sent"

4. `inv_draft_upcoming`:
   - partner_id: `customer_tech_startup`
   - invoice_date: today
   - state: "draft"

Wrap in `<odoo><data noupdate="1"> ... </data></odoo>`.
```

## Expected Output
- `data/demo_invoices.xml`

## Verification
Open Invoices list view. The overdue filter should display `inv_overdue_urgent` with a red overdue badge.
