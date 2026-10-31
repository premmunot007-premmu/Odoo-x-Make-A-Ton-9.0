# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SubscriptionPlan(models.Model):
    _name = 'subscription.plan'
    _description = 'Subscription Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(string="Plan Name", required=True, tracking=True)
    billing_frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ], string="Billing Frequency", required=True, default='monthly', tracking=True)
    min_quantity = fields.Integer(string="Minimum Quantity", default=1, help="Minimum quantity/seats required for this plan")
    date_start = fields.Date(string="Available From")
    date_end = fields.Date(string="Available Until")
    auto_close = fields.Boolean(
        string="Auto Close on Expiry",
        default=False,
        help="Automatically close subscriptions on their expiry date via scheduled action"
    )
    allow_early_close = fields.Boolean(string="Allow Early Closure", default=True, help="Allow customers or staff to terminate early")
    allow_pause = fields.Boolean(string="Allow Pause", default=False, help="Allow pausing subscriptions temporarily")
    allow_renew = fields.Boolean(string="Allow Renewal", default=True, help="Allow subscription renewals")
    description = fields.Html(string="Plan Description")
    is_active = fields.Boolean(string="Active", default=True, tracking=True)
    plan_line_ids = fields.One2many('subscription.plan.line', 'plan_id', string="Default Plan Lines")

    product_count = fields.Integer(string="Products Count", compute='_compute_product_count')
    is_available = fields.Boolean(string="Currently Available", compute='_compute_is_available', store=True)

    @api.depends('plan_line_ids')
    def _compute_product_count(self):
        for record in self:
            record.product_count = len(record.plan_line_ids)

    @api.depends('date_start', 'date_end', 'is_active')
    def _compute_is_available(self):
        today = fields.Date.today()
        for record in self:
            available = record.is_active
            if record.date_start and today < record.date_start:
                available = False
            if record.date_end and today > record.date_end:
                available = False
            record.is_available = available

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_end and record.date_end < record.date_start:
                raise ValidationError(_("Plan end date must be after start date."))

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Plan name must be unique!'),
        ('min_quantity_positive', 'CHECK(min_quantity >= 1)', 'Minimum quantity must be at least 1!'),
    ]


class SubscriptionPlanLine(models.Model):
    _name = 'subscription.plan.line'
    _description = 'Subscription Plan Line'
    _order = 'sequence, id'

    plan_id = fields.Many2one('subscription.plan', string="Plan", required=True, ondelete='cascade')
    product_id = fields.Many2one('subscription.product', string="Product", required=True, ondelete='restrict')
    sequence = fields.Integer(string="Sequence", default=10)
    default_qty = fields.Float(string="Default Quantity", default=1.0, digits=(12, 2))
    default_price = fields.Float(string="Default Unit Price", digits=(12, 2), help="Overrides product sales price if set > 0")
    display_price = fields.Float(string="Effective Price", compute='_compute_display_price', digits=(12, 2))

    @api.depends('default_price', 'product_id.sales_price')
    def _compute_display_price(self):
        for record in self:
            record.display_price = record.default_price if record.default_price > 0 else (record.product_id.sales_price if record.product_id else 0.0)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.default_price = self.product_id.sales_price
