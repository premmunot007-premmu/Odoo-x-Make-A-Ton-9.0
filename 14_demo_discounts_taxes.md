# Demo Taxes & Discount Rules

## Context
Admin configures tax rates (e.g. GST 18%) and discount rules (percentage or fixed, min purchase / seat counts, start/end dates, max uses).

## Prompt for Antigravity

```markdown
In our Odoo 18 module `subscription_management`, create `data/demo_discounts_taxes.xml`:

1. Create Tax Rules (`subscription.tax`):
   - `tax_gst_18`:
     - name: "GST 18%"
     - tax_type: "percentage"
     - amount: 18.0
     - is_active: True
   - `tax_service_5`:
     - name: "Service Cess 5%"
     - tax_type: "percentage"
     - amount: 5.0
     - is_active: True
   - `tax_fixed_handling`:
     - name: "Fixed Platform Levy"
     - tax_type: "fixed"
     - amount: 100.0
     - is_active: True

2. Create Discount Rules (`subscription.discount.rule`):
   - `disc_bulk_seats_15`:
     - name: "Enterprise Bulk 15% Off"
     - discount_type: "percentage"
     - amount: 15.0
     - min_quantity: 10
     - apply_on: "subscription"
     - max_usage: 100
     - current_usage: 2
     - description: "Applies to any subscription with 10 or more licenses"

   - `disc_startup_voucher`:
     - name: "Startup Welcome Voucher ₹1000"
     - discount_type: "fixed"
     - amount: 1000.0
     - min_purchase: 2000.0
     - apply_on: "subscription"
     - max_usage: 50
     - current_usage: 8

   - `disc_crm_promo`:
     - name: "CRM Early Bird 10%"
     - discount_type: "percentage"
     - amount: 10.0
     - apply_on: "product"
     - product_ids: `[prod_brightloop_crm]`
     - max_usage: 20

Wrap in `<odoo><data noupdate="1"> ... </data></odoo>`.
```

## Expected Output
- `data/demo_discounts_taxes.xml`

## Verification
Under Configuration > Taxes and Configuration > Discount Rules, verify all records load.
