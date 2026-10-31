# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SubscriptionDiscountRule(models.Model):
    """A discount applied automatically at invoicing, to specific products or a whole subscription."""

    _name = 'subscription.discount.rule'
    _description = 'Discount Rule'
    _order = 'name'

    name = fields.Char(string="Rule Name", required=True)
    discount_type = fields.Selection(
        [
            ('fixed', 'Fixed Amount'),
            ('percentage', 'Percentage'),
        ],
        string="Discount Type",
        required=True,
        default='percentage',
    )
    amount = fields.Float(
        string="Amount", required=True, digits=(10, 2), help="Discount amount or percentage",
    )
    min_purchase = fields.Float(
        string="Minimum Purchase Amount", digits=(10, 2), help="Minimum order value to qualify",
    )
    min_quantity = fields.Integer(string="Minimum Quantity", help="Minimum quantity to qualify")
    date_start = fields.Date(string="Valid From")
    date_end = fields.Date(string="Valid Until")
    max_usage = fields.Integer(string="Maximum Uses", default=0, help="0 = unlimited")
    current_usage = fields.Integer(string="Times Used", default=0, readonly=True, copy=False)
    product_ids = fields.Many2many('subscription.product', string="Applicable Products")
    apply_on = fields.Selection(
        [
            ('product', 'Specific Products'),
            ('subscription', 'Entire Subscription'),
        ],
        string="Apply On",
        required=True,
        default='product',
    )
    is_active = fields.Boolean(
        string="Active",
        compute='_compute_is_active',
        search='_search_is_active',
        help="Within its validity dates and usage limit today.",
    )
    description = fields.Text(string="Description")

    _sql_constraints = [
        ('positive_amount', 'CHECK(amount >= 0)', 'Discount amount cannot be negative!'),
        ('positive_max_usage', 'CHECK(max_usage >= 0)', 'Maximum uses cannot be negative!'),
    ]

    def _is_valid_on(self, date):
        """True if the rule is within its date range on ``date`` and has uses left."""
        self.ensure_one()
        if self.date_start and self.date_start > date:
            return False
        if self.date_end and self.date_end < date:
            return False
        return self.max_usage == 0 or self.current_usage < self.max_usage

    @api.depends('date_start', 'date_end', 'max_usage', 'current_usage')
    def _compute_is_active(self):
        """Not stored: validity depends on today's date, so it is evaluated on every read."""
        today = fields.Date.context_today(self)
        for rec in self:
            rec.is_active = rec._is_valid_on(today)

    def _search_is_active(self, operator, value):
        # The usage check compares two columns, which a domain can't express;
        # rules are few, so evaluate in Python.
        if operator not in ('=', '!='):
            raise UserError(_("Unsupported search operator for 'Active'."))
        today = fields.Date.context_today(self)
        want_active = (operator == '=') == bool(value)
        rules = self.search([]).filtered(lambda r: r._is_valid_on(today) == want_active)
        return [('id', 'in', rules.ids)]

    @api.constrains('discount_type', 'amount')
    def _check_percentage(self):
        for rec in self:
            if rec.discount_type == 'percentage' and rec.amount > 100:
                raise ValidationError(_("A percentage discount cannot exceed 100%."))

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for rec in self:
            if rec.date_start and rec.date_end and rec.date_start > rec.date_end:
                raise ValidationError(_("End date must be after start date."))

    @api.constrains('apply_on', 'product_ids')
    def _check_products(self):
        for rec in self:
            if rec.apply_on == 'product' and not rec.product_ids:
                raise ValidationError(_("Select at least one product for a product-specific discount."))
