# 04 — Subscription Model

## Context
The Subscription model is the **central entity** of the entire system. It links a customer to a plan, tracks the subscription lifecycle through states (Draft → Quotation → Confirmed → Active → Closed), manages billing dates, and holds subscription lines (products being subscribed to). This is the most complex model with state machine logic, date computations, and multiple action methods.

This file depends on: `01_module_scaffold.md`, `02_product_model.md`, `03_plan_model.md`.

## Prompt for Antigravity

```
Create an Odoo 18 model file for the core subscription entity in the subscription_management module.

Create file: E:\odoo18\custom_addons\subscription_management\models\subscription.py

### Model: subscription.subscription

This is the main subscription model — the heart of the system. It tracks a customer's subscription to a plan.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta

class Subscription(models.Model):
    _name = 'subscription.subscription'
    _description = 'Subscription'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    _rec_name = 'name'

    Fields:
    - name: Char, string="Subscription Number", readonly=True, copy=False, default='New', tracking=True
      (This will be auto-generated via ir.sequence on create)
    - partner_id: Many2one to 'res.partner', required=True, string="Customer", tracking=True, domain="[('customer_rank', '>', 0)]"
    - plan_id: Many2one to 'subscription.plan', required=True, string="Subscription Plan", tracking=True
    - template_id: Many2one to 'subscription.quotation.template', string="Quotation Template"
    - start_date: Date, required=True, string="Start Date", default=fields.Date.today, tracking=True
    - expiry_date: Date, string="Expiry Date", tracking=True
    - next_billing_date: Date, string="Next Billing Date", compute='_compute_next_billing_date', store=True, tracking=True
    - payment_term: Integer, string="Payment Terms (Days)", default=30, help="Number of days for payment after invoice"
    - state: Selection with choices [
        ('draft', 'Draft'),
        ('quotation', 'Quotation'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('closed', 'Closed')
      ], default='draft', required=True, string="Status", tracking=True, copy=False
    - subscription_line_ids: One2many to 'subscription.subscription.line', inverse field 'subscription_id', string="Subscription Lines"
    - is_expired: Boolean, compute='_compute_is_expired', string="Is Expired", store=True
    - close_reason: Text, string="Close Reason"
    - company_id: Many2one to 'res.company', string="Company", default=lambda self: self.env.company

    Computed fields:
    - amount_untaxed: Float(digits=(12,2)), compute='_compute_amounts', store=True, string="Untaxed Amount"
    - amount_tax: Float(digits=(12,2)), compute='_compute_amounts', store=True, string="Taxes"
    - amount_total: Float(digits=(12,2)), compute='_compute_amounts', store=True, string="Total"
    - invoice_count: Integer, compute='_compute_invoice_count', string="Invoice Count"

    @api.depends('subscription_line_ids.subtotal', 'subscription_line_ids.tax_amount')
    def _compute_amounts(self):
        for record in self:
            lines = record.subscription_line_ids
            record.amount_untaxed = sum(lines.mapped('subtotal'))
            record.amount_tax = sum(lines.mapped('tax_amount'))
            record.amount_total = record.amount_untaxed + record.amount_tax

    @api.depends('start_date', 'plan_id.billing_frequency')
    def _compute_next_billing_date(self):
        for record in self:
            if not record.start_date or not record.plan_id:
                record.next_billing_date = False
                continue
            freq = record.plan_id.billing_frequency
            today = fields.Date.today()
            billing_date = record.start_date
            # Calculate next billing date from start_date based on frequency
            while billing_date <= today:
                if freq == 'daily':
                    billing_date += relativedelta(days=1)
                elif freq == 'weekly':
                    billing_date += relativedelta(weeks=1)
                elif freq == 'monthly':
                    billing_date += relativedelta(months=1)
                elif freq == 'yearly':
                    billing_date += relativedelta(years=1)
            record.next_billing_date = billing_date

    @api.depends('expiry_date')
    def _compute_is_expired(self):
        today = fields.Date.today()
        for record in self:
            record.is_expired = record.expiry_date and record.expiry_date < today

    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = self.env['subscription.invoice'].search_count([
                ('subscription_id', '=', record.id)
            ])

    ### State Machine Action Methods ###

    def action_send_quotation(self):
        """Move from Draft to Quotation state."""
        for record in self:
            if record.state != 'draft':
                raise UserError(_("Only draft subscriptions can be sent as quotations."))
            if not record.subscription_line_ids:
                raise UserError(_("Cannot send quotation without subscription lines."))
            record.state = 'quotation'

    def action_confirm(self):
        """Move from Quotation to Confirmed state."""
        for record in self:
            if record.state not in ('draft', 'quotation'):
                raise UserError(_("Only draft or quotation subscriptions can be confirmed."))
            if not record.subscription_line_ids:
                raise UserError(_("Cannot confirm a subscription without lines."))
            record.state = 'confirmed'

    def action_activate(self):
        """Move from Confirmed to Active state."""
        for record in self:
            if record.state != 'confirmed':
                raise UserError(_("Only confirmed subscriptions can be activated."))
            record.state = 'active'

    def action_pause(self):
        """Pause an active subscription (if allowed by plan)."""
        for record in self:
            if record.state != 'active':
                raise UserError(_("Only active subscriptions can be paused."))
            if not record.plan_id.allow_pause:
                raise UserError(_("This plan does not allow pausing."))
            record.state = 'paused'

    def action_resume(self):
        """Resume a paused subscription."""
        for record in self:
            if record.state != 'paused':
                raise UserError(_("Only paused subscriptions can be resumed."))
            record.state = 'active'

    def action_close(self):
        """Close the subscription."""
        for record in self:
            if record.state not in ('active', 'paused', 'confirmed'):
                raise UserError(_("Cannot close a subscription in this state."))
            if record.state == 'active' and not record.plan_id.allow_early_close:
                if not record.is_expired:
                    raise UserError(_("This plan does not allow early closure."))
            record.state = 'closed'

    def action_renew(self):
        """Renew a closed subscription by creating a new one."""
        self.ensure_one()
        if not self.plan_id.allow_renew:
            raise UserError(_("This plan does not allow renewal."))
        freq = self.plan_id.billing_frequency
        new_start = fields.Date.today()
        if freq == 'daily':
            new_expiry = new_start + relativedelta(days=1)
        elif freq == 'weekly':
            new_expiry = new_start + relativedelta(weeks=1)
        elif freq == 'monthly':
            new_expiry = new_start + relativedelta(months=1)
        elif freq == 'yearly':
            new_expiry = new_start + relativedelta(years=1)
        else:
            new_expiry = new_start + relativedelta(months=1)

        new_sub = self.copy({
            'start_date': new_start,
            'expiry_date': new_expiry,
            'state': 'draft',
            'close_reason': False,
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'subscription.subscription',
            'res_id': new_sub.id,
            'view_mode': 'form',
            'target': 'current',
        }

    ### Model CRUD Overrides ###

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('subscription.subscription') or 'New'
        return super().create(vals_list)

    @api.onchange('plan_id')
    def _onchange_plan_id(self):
        """When a plan is selected, populate subscription lines from plan lines."""
        if self.plan_id and self.plan_id.plan_line_ids:
            lines = []
            for pl in self.plan_id.plan_line_ids:
                lines.append((0, 0, {
                    'product_id': pl.product_id.id,
                    'quantity': pl.default_qty,
                    'unit_price': pl.default_price if pl.default_price > 0 else pl.product_id.sales_price,
                }))
            self.subscription_line_ids = lines

    @api.onchange('template_id')
    def _onchange_template_id(self):
        """When a template is selected, load plan and lines from the template."""
        if self.template_id:
            self.plan_id = self.template_id.plan_id
            lines = []
            for tl in self.template_id.template_line_ids:
                lines.append((0, 0, {
                    'product_id': tl.product_id.id,
                    'quantity': tl.quantity,
                    'unit_price': tl.unit_price,
                }))
            self.subscription_line_ids = lines

    @api.constrains('start_date', 'expiry_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.expiry_date and record.expiry_date <= record.start_date:
                raise ValidationError(_("Expiry date must be after the start date."))

    ### Cron Method (will be triggered by scheduled action) ###

    @api.model
    def _cron_close_expired(self):
        """Find all active subscriptions past their expiry date and close them if auto_close is enabled."""
        today = fields.Date.today()
        expired_subs = self.search([
            ('state', '=', 'active'),
            ('expiry_date', '<', today),
            ('plan_id.auto_close', '=', True),
        ])
        for sub in expired_subs:
            sub.state = 'closed'
            sub.close_reason = 'Auto-closed: subscription expired on %s' % sub.expiry_date
            sub.message_post(body=_("Subscription auto-closed due to expiry."))

Also update models/__init__.py to add:
    from . import subscription

Use Odoo 18 conventions throughout. Include proper use of tracking=True for chatter, _() for translatable strings, and UserError for user-facing errors.
```

## Expected Output

```
subscription_management/
├── models/
│   ├── __init__.py  (updated: from . import subscription)
│   └── subscription.py
```

## Verification

1. Check Python syntax: `python -c "import ast; ast.parse(open('models/subscription.py').read()); print('OK')"`
2. Verify all 6 states are defined in the selection
3. Verify all action methods exist: `action_send_quotation`, `action_confirm`, `action_activate`, `action_pause`, `action_resume`, `action_close`, `action_renew`
4. Verify the `create` method generates sequence numbers
5. Verify `_cron_close_expired` method exists
6. Verify `_compute_next_billing_date` uses `relativedelta` correctly
7. Verify `models/__init__.py` now imports `subscription`
