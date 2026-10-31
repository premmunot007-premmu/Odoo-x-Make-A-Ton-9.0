# Demo Payments Across Multiple Methods

## Context
Brightloop receives customer payments through Bank Transfer, Credit Card, UPI, and Cash. This file generates demo payment entries tied to invoices.

## Prompt for Antigravity

```markdown
In our Odoo 18 module `subscription_management`, create `data/demo_payments.xml`:

Create demo `subscription.payment` records:
1. `pay_bank_transfer_full`:
   - invoice_id: `inv_paid_last_month`
   - payment_method: "bank_transfer"
   - amount: 1711.0 (Full total with GST)
   - payment_date: 10 days ago
   - reference: "HDFC-NEFT-991823901"
   - note: "Full settlement received via NEFT"

2. `pay_upi_partial`:
   - invoice_id: `inv_confirmed_outstanding`
   - payment_method: "upi"
   - amount: 25000.0 (Partial payment)
   - payment_date: 2 days ago
   - reference: "UPI/390192830192/GPay"
   - note: "Advance milestone installment"

3. `pay_credit_card_small`:
   - invoice_id: `inv_paid_last_month`
   - payment_method: "credit_card"
   - amount: 500.0
   - payment_date: 12 days ago
   - reference: "STRIPE_CH_99A102Z"
   - note: "Card auto-charge"

Wrap in `<odoo><data noupdate="1"> ... </data></odoo>`.
```

## Expected Output
- `data/demo_payments.xml`

## Verification
Under Billing > Payments, verify payments appear with amounts, dates, and payment methods.
