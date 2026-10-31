# Subscription Lifecycle — Pause, Renew, Early Close

## Context
Plans can allow/disallow pausing, renewal, and early closing. These need proper business logic with validation.

## Prompt for Antigravity

```
In the Odoo 18 module "subscription_management", enhance subscription lifecycle methods.

In `models/subscription.py`, ensure these methods exist and are complete:

def action_pause(self):
    """Pause an active subscription (if plan allows)"""
    for rec in self:
        if rec.state != 'active':
            raise UserError("Only active subscriptions can be paused.")
        if not rec.plan_id.allow_pause:
            raise UserError(f"Plan '{rec.plan_id.name}' does not allow pausing.")
        rec.write({'state': 'paused'})
        rec.message_post(body="Subscription paused by %s" % self.env.user.name)

def action_resume(self):
    """Resume a paused subscription"""
    for rec in self:
        if rec.state != 'paused':
            raise UserError("Only paused subscriptions can be resumed.")
        rec.write({'state': 'active'})
        rec.message_post(body="Subscription resumed by %s" % self.env.user.name)

def action_close(self):
    """Close a subscription (early close if plan allows, or normal close)"""
    for rec in self:
        if rec.state in ('closed', 'draft'):
            raise UserError("Cannot close a draft or already closed subscription.")
        if rec.state == 'active' and not rec.plan_id.allow_early_close:
            raise UserError(f"Plan '{rec.plan_id.name}' does not allow early termination.")
        rec.write({'state': 'closed'})
        rec.message_post(body="Subscription closed by %s" % self.env.user.name)

def action_renew(self):
    """Renew a subscription for another billing period"""
    for rec in self:
        if not rec.plan_id.allow_renew:
            raise UserError(f"Plan '{rec.plan_id.name}' does not allow renewal.")
        from dateutil.relativedelta import relativedelta
        freq_map = {
            'daily': relativedelta(days=1),
            'weekly': relativedelta(weeks=1),
            'monthly': relativedelta(months=1),
            'yearly': relativedelta(years=1),
        }
        delta = freq_map.get(rec.plan_id.billing_frequency, relativedelta(months=1))
        new_start = rec.expiry_date or fields.Date.today()
        new_expiry = new_start + delta
        rec.write({
            'state': 'active',
            'start_date': new_start,
            'expiry_date': new_expiry,
        })
        rec.message_post(body=f"Subscription renewed until {new_expiry}")

Also add a button method for loading quotation template:
def action_load_template(self):
    self.ensure_one()
    if not self.template_id:
        raise UserError("Please select a quotation template first.")
    # Clear existing lines
    self.subscription_line_ids.unlink()
    # Load from template
    lines = []
    for tpl_line in self.template_id.template_line_ids:
        lines.append((0, 0, {
            'product_id': tpl_line.product_id.id,
            'quantity': tpl_line.quantity,
            'unit_price': tpl_line.unit_price or tpl_line.product_id.sales_price,
        }))
    self.write({
        'subscription_line_ids': lines,
        'plan_id': self.template_id.plan_id.id,
    })
    return True
```

## Expected Output
- Updated `models/subscription.py` with complete lifecycle methods

## Verification
- Test full lifecycle: Draft → Quotation → Confirmed → Active → Paused → Active → Closed
- Test renew creates new period
- Test plan restrictions are enforced
