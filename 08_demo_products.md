# Demo Products & Variants Data

## Context
Prem is responsible for realistic demo data and frontend enhancements. Brightloop sells software products and add-ons with variants (such as Brand: Odoo adding ₹560). This file generates the demo XML data for products and variants.

## Prompt for Antigravity

```markdown
In our Odoo 18 module `subscription_management`, create `data/demo_products.xml`:

1. Define records for `subscription.product`:
   - `prod_brightloop_crm`: "Brightloop CRM", type: software, sales_price: 1200.0, cost_price: 400.0, description: "Full customer relationship management system."
   - `prod_brightloop_erp`: "Brightloop Enterprise Suite", type: software, sales_price: 3500.0, cost_price: 1200.0, description: "Unified ERP backend with accounting, inventory, and payroll."
   - `prod_email_marketing`: "Email Marketing Automation Add-on", type: addon, sales_price: 450.0, cost_price: 100.0, description: "Send up to 50k monthly newsletter campaigns."
   - `prod_storage_boost`: "100GB Extra Cloud Storage", type: addon, sales_price: 250.0, cost_price: 50.0, description: "High-speed encrypted backup storage."
   - `prod_vip_support`: "24/7 Dedicated Priority Support", type: service, sales_price: 1500.0, cost_price: 600.0, description: "1-hour SLA phone & Slack channel support."

2. Define variants for `subscription.product.variant`:
   - Variant on `prod_brightloop_erp`:
     - variant_name: "Brand"
     - variant_value: "Odoo Integrated"
     - price_extra: 560.0
   - Variant on `prod_brightloop_crm`:
     - variant_name: "Brand"
     - variant_value: "Standard Edition"
     - price_extra: 0.0
   - Variant on `prod_brightloop_crm`:
     - variant_name: "Brand"
     - variant_value: "Odoo Enterprise Sync"
     - price_extra: 560.0

Wrap in `<odoo><data noupdate="1"> ... </data></odoo>`.
```

## Expected Output
- `data/demo_products.xml`

## Verification
Load demo data via:
```bash
python odoo-bin -c odoo.conf -u subscription_management
```
Verify under Subscriptions > Products & Plans > Products that the 5 products with variants are present.
