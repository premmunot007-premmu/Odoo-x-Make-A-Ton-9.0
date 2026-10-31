# Billing Automation — Mass Invoice & Cron

## Context
On billing day, hundreds of subscriptions are due. A cron job finds all active subscriptions due for billing and mass-generates invoices. Another cron auto-closes expired subscriptions.

## Prompt for Claude Code

```
In the Odoo 18 module "subscription_management", create billing automation.

Add to `models/subscription.py`:

    @api.model
    def action_mass_invoice(self):
        """Mass generate invoices for all active subscriptions due for billing.
        Called manually or via cron job."""
        today = fields.Date.today()
        due_subscriptions = self.search([
            ('state', '=', 'active'),
            ('next_billing_date', '<=', today),
        ])
        invoices = self.env['subscription.invoice']
        errors = []
        for sub in due_subscriptions:
            try:
                result = sub.action_create_invoice()
                if result and result.get('res_id'):
                    invoices |= self.env['subscription.invoice'].browse(result['res_id'])
            except Exception as e:
                errors.append(f"{sub.name}: {str(e)}")
        
        if errors:
            # Log errors but don't fail the whole batch
            import logging
            _logger = logging.getLogger(__name__)
            for err in errors:
                _logger.warning("Billing error: %s", err)
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'Generated Invoices ({len(invoices)})',
            'res_model': 'subscription.invoice',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', invoices.ids)],
        }

    @api.model
    def _cron_close_expired(self):
        """Cron: Auto-close subscriptions past expiry date with auto_close plan"""
        today = fields.Date.today()
        expired = self.search([
            ('state', '=', 'active'),
            ('expiry_date', '<', today),
            ('plan_id.auto_close', '=', True),
        ])
        expired.write({'state': 'closed'})
        import logging
        _logger = logging.getLogger(__name__)
        _logger.info("Auto-closed %d expired subscriptions", len(expired))

    @api.model
    def _cron_billing(self):
        """Cron: Mass billing for due subscriptions"""
        self.action_mass_invoice()

Create `data/cron.xml`:
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <!-- Daily: Auto-close expired subscriptions -->
        <record id="cron_close_expired_subscriptions" model="ir.cron">
            <field name="name">Subscription: Auto-Close Expired</field>
            <field name="model_id" ref="model_subscription_subscription"/>
            <field name="state">code</field>
            <field name="code">model._cron_close_expired()</field>
            <field name="interval_number">1</field>
            <field name="interval_type">days</field>
            <field name="numbercall">-1</field>
            <field name="active">True</field>
        </record>

        <!-- Daily: Mass billing -->
        <record id="cron_mass_billing" model="ir.cron">
            <field name="name">Subscription: Daily Billing</field>
            <field name="model_id" ref="model_subscription_subscription"/>
            <field name="state">code</field>
            <field name="code">model._cron_billing()</field>
            <field name="interval_number">1</field>
            <field name="interval_type">days</field>
            <field name="numbercall">-1</field>
            <field name="active">True</field>
        </record>
    </data>
</odoo>

Create `data/sequences.xml`:
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <record id="seq_subscription" model="ir.sequence">
            <field name="name">Subscription Sequence</field>
            <field name="code">subscription.subscription</field>
            <field name="prefix">SUB/%(year)s/%(month)s/</field>
            <field name="padding">4</field>
        </record>
        <record id="seq_invoice" model="ir.sequence">
            <field name="name">Invoice Sequence</field>
            <field name="code">subscription.invoice</field>
            <field name="prefix">INV/%(year)s/%(month)s/</field>
            <field name="padding">4</field>
        </record>
    </data>
</odoo>

Update __manifest__.py data list to include 'data/cron.xml' and 'data/sequences.xml'.
```

## Expected Output
- Updated `models/subscription.py`
- `data/cron.xml`
- `data/sequences.xml`
- Updated `__manifest__.py`

## Verification
- Run _cron_billing manually in shell, verify invoices are created
- Verify subscription numbers start with SUB/2026/10/0001
