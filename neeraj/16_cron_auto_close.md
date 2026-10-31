# Cron — Auto-Close Expired Subscriptions

## Context
Daily cron job that finds active subscriptions past their expiry date (where plan has auto_close=True) and closes them automatically.

## Prompt for Antigravity

```
In the Odoo 18 module "subscription_management", verify the cron job for auto-closing works.

In `models/subscription.py`, ensure method exists:

@api.model
def _cron_close_expired(self):
    """Auto-close expired subscriptions where plan allows auto-close"""
    import logging
    _logger = logging.getLogger(__name__)
    
    today = fields.Date.today()
    expired_subs = self.search([
        ('state', '=', 'active'),
        ('expiry_date', '!=', False),
        ('expiry_date', '<', today),
        ('plan_id.auto_close', '=', True),
    ])
    
    for sub in expired_subs:
        sub.write({'state': 'closed'})
        sub.message_post(
            body=f"Subscription auto-closed. Expiry date: {sub.expiry_date}",
            message_type='notification',
        )
    
    _logger.info("Auto-close cron: closed %d expired subscriptions", len(expired_subs))
    return True

In `data/cron.xml`, ensure the cron record:
<record id="cron_close_expired" model="ir.cron">
    <field name="name">Subscription: Auto-Close Expired</field>
    <field name="model_id" ref="model_subscription_subscription"/>
    <field name="state">code</field>
    <field name="code">model._cron_close_expired()</field>
    <field name="interval_number">1</field>
    <field name="interval_type">days</field>
    <field name="numbercall">-1</field>
    <field name="active" eval="True"/>
</record>
```

## Expected Output
- Verified `_cron_close_expired` method
- Verified `data/cron.xml`

## Verification
- Create subscription with past expiry + auto_close plan, run cron manually, verify it closes
