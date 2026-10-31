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
    notes = fields.Html(string="Internal Notes")
    image = fields.Binary(string="Product Image", attachment=True)
    is_active = fields.Boolean(string="Active", default=True)
    variant_ids = fields.One2many(
        'subscription.product.variant', 'product_id', string="Variants",
    )
    variant_count = fields.Integer(string="Variant Count", compute='_compute_variant_count')

    product_code = fields.Char(string="Product Code")
    base_price = fields.Float(
        string="Base Price", compute='_compute_base_price', inverse='_inverse_base_price', store=True, digits=(10, 2),
    )
    active = fields.Boolean(string="Active Flag", compute='_compute_active', inverse='_inverse_active', store=True)
    description = fields.Text(string="Description", compute='_compute_description', inverse='_inverse_description', store=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string="Currency", related='company_id.currency_id')

    @api.depends('sales_price')
    def _compute_base_price(self):
        for rec in self:
            rec.base_price = rec.sales_price

    def _inverse_base_price(self):
        for rec in self:
            rec.sales_price = rec.base_price

    @api.depends('is_active')
    def _compute_active(self):
        for rec in self:
            rec.active = rec.is_active

    def _inverse_active(self):
        for rec in self:
            rec.is_active = rec.active

    @api.depends('notes')
    def _compute_description(self):
        for rec in self:
            rec.description = rec.notes

    def _inverse_description(self):
        for rec in self:
            rec.notes = rec.description

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
    variant_name = fields.Char(string="Variant Attribute", required=True, default="Brand")
    variant_value = fields.Char(string="Variant Value", required=True)
    price_extra = fields.Float(
        string="Extra Price",
        default=0.0,
        digits=(10, 2),
        help="Additional price for this variant (e.g., 560 for Odoo brand)",
    )
    name = fields.Char(string="Variant Name", compute='_compute_name', store=True, readonly=False)
    variant_code = fields.Char(string="Variant Code")
    description = fields.Text(string="Description")
    active = fields.Boolean(string="Active", default=True)
    is_active = fields.Boolean(string="Is Active", default=True)

    @api.depends('variant_name', 'variant_value')
    def _compute_name(self):
        for rec in self:
            if rec.variant_name and rec.variant_value:
                rec.name = f"{rec.variant_name}: {rec.variant_value}"
            elif rec.variant_value:
                rec.name = rec.variant_value
            elif not rec.name:
                rec.name = "Variant"

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
