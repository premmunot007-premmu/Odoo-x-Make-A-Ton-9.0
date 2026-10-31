# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class SubscriptionProduct(models.Model):
    _name = 'subscription.product'
    _description = 'Subscription Product'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(string="Product Name", required=True, tracking=True)
    product_type = fields.Selection([
        ('software', 'Software'),
        ('addon', 'Add-on'),
        ('service', 'Service')
    ], string="Product Type", required=True, default='software', tracking=True)
    sales_price = fields.Float(string="Sales Price", required=True, digits=(12, 2), default=0.0, tracking=True)
    cost_price = fields.Float(string="Cost Price", digits=(12, 2), default=0.0, tracking=True)
    notes = fields.Html(string="Description / Internal Notes")
    image = fields.Binary(string="Product Image", attachment=True)
    is_active = fields.Boolean(string="Active", default=True, tracking=True)
    currency_symbol = fields.Char(string="Currency", default='₹')
    variant_ids = fields.One2many('subscription.product.variant', 'product_id', string="Variants")
    variant_count = fields.Integer(string="Variant Count", compute='_compute_variant_count')

    @api.depends('variant_ids')
    def _compute_variant_count(self):
        for record in self:
            record.variant_count = len(record.variant_ids)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Product name must be unique!'),
        ('sales_price_positive', 'CHECK(sales_price >= 0)', 'Sales price must be positive or zero!'),
        ('cost_price_positive', 'CHECK(cost_price >= 0)', 'Cost price must be positive or zero!'),
    ]


class SubscriptionProductVariant(models.Model):
    _name = 'subscription.product.variant'
    _description = 'Product Variant'
    _order = 'product_id, variant_name, id'

    product_id = fields.Many2one('subscription.product', string="Product", required=True, ondelete='cascade')
    variant_name = fields.Char(string="Variant Attribute (e.g. Brand)", required=True)
    variant_value = fields.Char(string="Variant Value (e.g. Odoo)", required=True)
    price_extra = fields.Float(
        string="Extra Price",
        digits=(12, 2),
        default=0.0,
        help="Additional fee added to the base product price (e.g., 560 for Odoo brand)"
    )
    final_price = fields.Float(string="Final Price", compute='_compute_final_price', store=True, digits=(12, 2))

    @api.depends('product_id.sales_price', 'price_extra')
    def _compute_final_price(self):
        for record in self:
            base = record.product_id.sales_price if record.product_id else 0.0
            record.final_price = base + (record.price_extra or 0.0)

    _sql_constraints = [
        ('unique_variant', 'UNIQUE(product_id, variant_name, variant_value)', 'Variant combination must be unique per product!'),
        ('price_extra_positive', 'CHECK(price_extra >= 0)', 'Extra price must be positive or zero!'),
    ]

    def name_get(self):
        res = []
        for rec in self:
            extra_str = f" (+₹{rec.price_extra})" if rec.price_extra else ""
            res.append((rec.id, f"{rec.variant_name}: {rec.variant_value}{extra_str}"))
        return res
