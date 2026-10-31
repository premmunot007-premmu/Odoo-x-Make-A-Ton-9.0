# Computed Fields & Depends Decorators

## Context
Ensure all computed fields across all models have proper @api.depends decorators and work correctly.

## Prompt for Antigravity

```
In the Odoo 18 module "subscription_management", review and fix all computed fields.

Go through each model and ensure these computed fields exist with correct @api.depends:

1. subscription.product:
   - variant_count: depends('variant_ids')

2. subscription.subscription:
   - amount_untaxed: depends('subscription_line_ids.subtotal')
   - amount_tax: depends('subscription_line_ids.tax_amount')
   - amount_total: depends('subscription_line_ids.subtotal', 'subscription_line_ids.tax_amount')
   - invoice_count: depends('invoice_ids')
   - next_billing_date: depends('start_date', 'plan_id.billing_frequency')
   - is_expired: depends('expiry_date')

3. subscription.subscription.line:
   - subtotal: depends('quantity', 'unit_price', 'discount', 'variant_id.price_extra')
   - tax_amount: depends('subtotal', 'tax_ids', 'tax_ids.amount')
   - total: depends('subtotal', 'tax_amount')

4. subscription.invoice:
   - amount_untaxed: depends('invoice_line_ids.subtotal')
   - amount_tax: depends('invoice_line_ids.tax_amount')
   - amount_total: depends('invoice_line_ids.subtotal', 'invoice_line_ids.tax_amount')
   - amount_paid: depends('payment_ids.amount')
   - amount_due: depends('amount_total', 'payment_ids.amount')
   - payment_status: depends('amount_total', 'payment_ids.amount')
   - is_overdue: depends('due_date', 'state')

5. subscription.invoice.line:
   - subtotal: depends('quantity', 'unit_price', 'discount_amount')
   - tax_amount: depends('subtotal', 'tax_ids')
   - total: depends('subtotal', 'tax_amount')

6. subscription.discount.rule:
   - is_active: depends('date_start', 'date_end', 'max_usage', 'current_usage')

7. subscription.payment:
   - name: depends('invoice_id', 'payment_date')

Verify all store=True on computed fields that need to be searchable.
Add any missing @api.onchange decorators for UX (e.g., product_id → unit_price).
```

## Expected Output
- Updates across all model files

## Verification
- Change a subscription line qty → subtotal should auto-update
- Add payment to invoice → amount_due should decrease
