# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SubscriptionPlan(models.Model):
    """A billing plan: how often subscribers are billed and what they may do with their subscription."""

    _name = 'subscription.plan'
    _description = 'Subscription Plan'
    _inherit = ['mail.thread']
    _order = 'name'

    name = fields.Char(string="Plan Name", required=True, tracking=True)
    billing_frequency = fields.Selection(
        [
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
        ],
        string="Billing Frequency",
        required=True,
        default='monthly',
        tracking=True,
    )
    min_quantity = fields.Integer(string="Minimum Quantity", default=1)
    date_start = fields.Date(string="Available From")
    date_end = fields.Date(string="Available Until")
    auto_close = fields.Boolean(
        string="Auto-Close on Expiry",
        default=False,
        help="Automatically close subscriptions when plan end date is reached",
    )
    allow_early_close = fields.Boolean(string="Allow Early Termination", default=True)
    allow_pause = fields.Boolean(string="Allow Pause", default=False)
    allow_renew = fields.Boolean(string="Allow Renewal", default=True)
    description = fields.Text(string="Plan Description")
    is_active = fields.Boolean(string="Active", default=True)
    plan_line_ids = fields.One2many('subscription.plan.line', 'plan_id', string="Plan Lines")

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        """Ensure the availability window is not inverted."""
        for rec in self:
            if rec.date_start and rec.date_end and rec.date_start > rec.date_end:
                raise ValidationError(_("End date must be after start date."))


class SubscriptionPlanLine(models.Model):
    """A default product included in a plan, with its default quantity and unit price."""

    _name = 'subscription.plan.line'
    _description = 'Plan Line'

    plan_id = fields.Many2one(
        'subscription.plan', string="Plan", required=True, ondelete='cascade', index=True,
    )
    product_id = fields.Many2one('subscription.product', string="Product", required=True)
    default_qty = fields.Integer(string="Default Quantity", default=1)
    default_price = fields.Float(string="Default Unit Price", digits=(10, 2))

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Prefill the unit price from the product's sales price."""
        if self.product_id:
            self.default_price = self.product_id.sales_price
