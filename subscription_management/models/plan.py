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
    sequence = fields.Integer(string="Sequence", default=10)
    plan_code = fields.Char(string="Plan Code")
    billing_frequency = fields.Selection(
        [
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('semi_annually', 'Semi-Annual'),
            ('yearly', 'Yearly'),
            ('annually', 'Annually'),
        ],
        string="Billing Frequency",
        required=True,
        default='monthly',
        tracking=True,
    )
    base_price = fields.Float(string="Base Price", default=0.0, digits=(10, 2))
    active = fields.Boolean(string="Active", compute='_compute_active', inverse='_inverse_active', store=True)
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id)
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
    is_active = fields.Boolean(string="Active Flag", default=True)
    plan_line_ids = fields.One2many('subscription.plan.line', 'plan_id', string="Plan Lines")

    @api.depends('is_active')
    def _compute_active(self):
        for rec in self:
            rec.active = rec.is_active

    def _inverse_active(self):
        for rec in self:
            rec.is_active = rec.active

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
    variant_id = fields.Many2one('subscription.product.variant', string="Variant", domain="[('product_id', '=', product_id)]")
    default_qty = fields.Integer(string="Default Quantity", default=1)
    default_price = fields.Float(string="Default Unit Price", digits=(10, 2))
    quantity = fields.Float(string="Quantity", compute='_compute_quantity', inverse='_inverse_quantity', store=True)
    unit_price = fields.Float(string="Unit Price", compute='_compute_unit_price', inverse='_inverse_unit_price', store=True, digits=(10, 2))
    subtotal = fields.Float(string="Subtotal", compute='_compute_subtotal', store=True, digits=(10, 2))

    @api.depends('default_qty')
    def _compute_quantity(self):
        for rec in self:
            rec.quantity = float(rec.default_qty or 1.0)

    def _inverse_quantity(self):
        for rec in self:
            rec.default_qty = int(rec.quantity or 1)

    @api.depends('default_price')
    def _compute_unit_price(self):
        for rec in self:
            rec.unit_price = rec.default_price or 0.0

    def _inverse_unit_price(self):
        for rec in self:
            rec.default_price = rec.unit_price or 0.0

    @api.depends('quantity', 'unit_price', 'default_qty', 'default_price')
    def _compute_subtotal(self):
        for rec in self:
            qty = rec.quantity if rec.quantity else float(rec.default_qty or 1.0)
            price = rec.unit_price if rec.unit_price else (rec.default_price or 0.0)
            rec.subtotal = qty * price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Prefill the unit price from the product's sales price."""
        if self.product_id:
            self.default_price = self.product_id.sales_price
            self.unit_price = self.product_id.sales_price
