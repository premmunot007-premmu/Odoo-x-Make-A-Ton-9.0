# Plan Model — Subscription Plans

## Context
Plans define billing frequency (daily/weekly/monthly/yearly), minimum quantities, availability dates, and lifecycle options (auto-close, pause, renew). Plans have plan lines linking to default products.

## Prompt for Claude Code

```
In the Odoo 18 module "subscription_management", create the Subscription Plan model.

Create `models/plan.py`:

class SubscriptionPlan(models.Model):
    _name = 'subscription.plan'
    _description = 'Subscription Plan'
    _inherit = ['mail.thread']

    Fields:
    - name: Char, required, tracked=True
    - billing_frequency: Selection [('daily','Daily'), ('weekly','Weekly'), ('monthly','Monthly'), ('yearly','Yearly')], required, default='monthly', tracked=True
    - min_quantity: Integer, default=1, string="Minimum Quantity"
    - date_start: Date, string="Available From"
    - date_end: Date, string="Available Until"
    - auto_close: Boolean, default=False, string="Auto-Close on Expiry", help="Automatically close subscriptions when plan end date is reached"
    - allow_early_close: Boolean, default=True, string="Allow Early Termination"
    - allow_pause: Boolean, default=False, string="Allow Pause"
    - allow_renew: Boolean, default=True, string="Allow Renewal"
    - description: Text, string="Plan Description"
    - is_active: Boolean, default=True
    - plan_line_ids: One2many to 'subscription.plan.line', inverse='plan_id'

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for rec in self:
            if rec.date_start and rec.date_end and rec.date_start > rec.date_end:
                raise ValidationError("End date must be after start date.")


class SubscriptionPlanLine(models.Model):
    _name = 'subscription.plan.line'
    _description = 'Plan Line'

    Fields:
    - plan_id: Many2one to 'subscription.plan', required, ondelete='cascade'
    - product_id: Many2one to 'subscription.product', required, string="Product"
    - default_qty: Integer, default=1, string="Default Quantity"
    - default_price: Float, digits=(10,2), string="Default Unit Price"

Update models/__init__.py to import plan.
```

## Expected Output
- `models/plan.py`
- Updated `models/__init__.py`

## Verification
```bash
python odoo-bin -c odoo.conf -u subscription_management
# Check model exists in Technical > Models
```
