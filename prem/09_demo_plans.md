# Demo Plans Data

## Context
Brightloop sells subscriptions billed daily, weekly, monthly, or yearly. Some auto-close when expired, while others allow early close, pause, or renewal.

## Prompt for Antigravity

```markdown
In our Odoo 18 module `subscription_management`, create `data/demo_plans.xml`:

Create 4 realistic `subscription.plan` records:
1. `plan_starter_monthly`:
   - Name: "Starter Monthly"
   - billing_frequency: "monthly"
   - min_quantity: 1
   - auto_close: False
   - allow_early_close: True
   - allow_pause: True
   - allow_renew: True
   - description: "Affordable plan for small shops with flexible monthly billing."

2. `plan_growth_yearly`:
   - Name: "Growth Annual Plan"
   - billing_frequency: "yearly"
   - min_quantity: 5
   - auto_close: False
   - allow_early_close: False
   - allow_pause: True
   - allow_renew: True
   - description: "Discounted annual contract for growing teams (minimum 5 seats)."

3. `plan_trial_daily`:
   - Name: "Fast Pilot (Daily Billing)"
   - billing_frequency: "daily"
   - min_quantity: 1
   - auto_close: True
   - allow_early_close: True
   - allow_pause: False
   - allow_renew: False
   - description: "Short-term evaluation plan that automatically shuts off on expiry date."

4. `plan_enterprise_quarterly`:
   - Name: "Enterprise Flexible"
   - billing_frequency: "weekly"
   - min_quantity: 10
   - auto_close: False
   - allow_early_close: True
   - allow_pause: True
   - allow_renew: True
   - description: "Weekly high-velocity billing plan for agile enterprise deployments."

Also add `subscription.plan.line` records connecting default products to these plans.
Wrap in `<odoo><data noupdate="1"> ... </data></odoo>`.
```

## Expected Output
- `data/demo_plans.xml`

## Verification
Inspect Plans view under Subscriptions > Products & Plans > Plans.
