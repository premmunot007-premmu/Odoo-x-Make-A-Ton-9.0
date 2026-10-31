# Demo Customers Data

## Context
Brightloop serves small shops and large companies. This file generates realistic `res.partner` demo customers with portal accounts.

## Prompt for Antigravity

```markdown
In our Odoo 18 module `subscription_management`, create `data/demo_customers.xml`:

Create 4 demo customer partners:
1. `customer_small_shop`:
   - Name: "Acuity Bakery & Cafe"
   - is_company: True
   - customer_rank: 1
   - email: "contact@acuitybakery.com"
   - phone: "+91 98765 43210"
   - street: "42 Market Street"
   - city: "Bangalore"
   - zip: "560001"

2. `customer_enterprise_corp`:
   - Name: "Starlight Logistics Pvt Ltd"
   - is_company: True
   - customer_rank: 1
   - email: "billing@starlightlogistics.com"
   - phone: "+91 98220 11223"
   - street: "Tower 4, Cyber City"
   - city: "Gurgaon"
   - zip: "122002"

3. `customer_tech_startup`:
   - Name: "NovaEdge Tech Labs"
   - is_company: True
   - customer_rank: 1
   - email: "ops@novaedge.io"
   - street: "10 Innovation Hub"
   - city: "Hyderabad"
   - zip: "500081"

4. `customer_retail_chain`:
   - Name: "Urban Cart Supermarkets"
   - is_company: True
   - customer_rank: 1
   - email: "accounts@urbancart.in"
   - street: "88 Ring Road"
   - city: "Mumbai"
   - zip: "400050"

Ensure each record has `<field name="customer_rank">1</field>` so they appear in customer selectors.
Wrap in `<odoo><data noupdate="1"> ... </data></odoo>`.
```

## Expected Output
- `data/demo_customers.xml`

## Verification
Under Contacts, verify these 4 companies are listed and selectable in subscription records.
