# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SubscriptionProduct(models.Model):
    """A software product, add-on or service sold on a subscription basis."""

    _name = 'subscription.product'
    _description = 'Subscription Product'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string="Product Name", required=True, tracking=True)
    product_type = fields.Selection(
        [
            ('software', 'Software'),
            ('addon', 'Add-on'),
            ('service', 'Service'),
        ],
        string="Product Type",
        required=True,
        default='software',
        tracking=True,
    )
    sales_price = fields.Float(
        string="Sales Price", required=True, default=0.0, digits=(10, 2), tracking=True,
    )
    cost_price = fields.Float(string="Cost Price", digits=(10, 2))
    notes = fields.Html(string="Description")
    image = fields.Binary(string="Product Image", attachment=True)
    is_active = fields.Boolean(string="Active", default=True)
    variant_ids = fields.One2many(
        'subscription.product.variant', 'product_id', string="Variants",
    )
    variant_count = fields.Integer(string="Variant Count", compute='_compute_variant_count')

    _sql_constraints = [
        ('positive_sales_price', 'CHECK(sales_price >= 0)', 'Sales price must be positive!'),
        ('positive_cost_price', 'CHECK(cost_price >= 0)', 'Cost price must be positive!'),
    ]

    @api.depends('variant_ids')
    def _compute_variant_count(self):
        """Count the variants defined on each product."""
        for rec in self:
            rec.variant_count = len(rec.variant_ids)


class SubscriptionProductVariant(models.Model):
    """An attribute/value pair of a product (e.g. Brand: Odoo) with an extra price."""

    _name = 'subscription.product.variant'
    _description = 'Product Variant'
    _order = 'product_id, variant_name, variant_value'

    product_id = fields.Many2one(
        'subscription.product', string="Product", required=True, ondelete='cascade', index=True,
    )
    variant_name = fields.Char(string="Variant Attribute", required=True)
    variant_value = fields.Char(string="Variant Value", required=True)
    price_extra = fields.Float(
        string="Extra Price",
        default=0.0,
        digits=(10, 2),
        help="Additional price for this variant (e.g., 560 for Odoo brand)",
    )

    _sql_constraints = [
        (
            'unique_variant',
            'UNIQUE(product_id, variant_name, variant_value)',
            'Variant combination must be unique per product!',
        ),
    ]

    @api.depends('product_id.name', 'variant_name', 'variant_value')
    def _compute_display_name(self):
        """Show variants as "Product (Attribute: Value)" in dropdowns and breadcrumbs."""
        for rec in self:
            rec.display_name = f"{rec.product_id.name} ({rec.variant_name}: {rec.variant_value})"
