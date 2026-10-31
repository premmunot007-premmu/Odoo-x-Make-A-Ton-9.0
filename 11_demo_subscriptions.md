# Demo Subscriptions Across All States

## Context
Brightloop's subscriptions transition through states: Draft → Quotation → Confirmed → Active → Paused → Closed. This demo dataset showcases subscriptions across every state with realistic dates and lines.

## Prompt for Antigravity

```markdown
In our Odoo 18 module `subscription_management`, create `data/demo_subscriptions.xml`:

Create demo subscriptions linking customers, plans, and lines:
1. `sub_active_acuity`:
   - partner_id: `customer_small_shop`
   - plan_id: `plan_starter_monthly`
   - state: "active"
   - start_date: 30 days ago
   - next_billing_date: today or tomorrow
   - payment_term: "30_days"
   - lines: 1x Brightloop CRM (unit_price: 1200) + 1x 100GB Extra Storage (unit_price: 250)

2. `sub_active_starlight`:
   - partner_id: `customer_enterprise_corp`
   - plan_id: `plan_growth_yearly`
   - state: "active"
   - start_date: 6 months ago
   - expiry_date: 6 months in future
   - payment_term: "60_days"
   - lines: 25x Brightloop Enterprise Suite with Odoo variant (price_extra: 560) + 1x VIP Priority Support

3. `sub_quotation_nova`:
   - partner_id: `customer_tech_startup`
   - plan_id: `plan_starter_monthly`
   - state: "quotation"
   - start_date: today
   - lines: 5x Brightloop CRM

4. `sub_paused_urbancart`:
   - partner_id: `customer_retail_chain`
   - plan_id: `plan_starter_monthly`
   - state: "paused"
   - start_date: 90 days ago

5. `sub_closed_old`:
   - partner_id: `customer_small_shop`
   - plan_id: `plan_trial_daily`
   - state: "closed"
   - start_date: 60 days ago
   - expiry_date: 45 days ago

Wrap in `<odoo><data noupdate="1"> ... </data></odoo>`.
```

## Expected Output
- `data/demo_subscriptions.xml`

## Verification
Open Subscriptions kanban view: you should see cards in Draft/Quotation, Active, Paused, and Closed columns.
