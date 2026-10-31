# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class SubscriptionLine(models.Model):
    _name = 'subscription.subscription.line'
    _description = 'Subscription Line'
    _order = 'sequence, id'

    subscription_id = fields.Many2one('subscription.subscription', string="Subscription", required=True, ondelete='cascade')
    product_id = fields.Many2one('subscription.product', string="Product", required=True, ondelete='restrict')
    variant_id = fields.Many2one(
        'subscription.product.variant',
        string="Variant",
        domain="[('product_id', '=', product_id)]",
        help="Optional variant adding an extra fee"
    )
    sequence = fields.Integer(string="Sequence", default=10)
    quantity = fields.Float(string="Quantity", required=True, default=1.0, digits=(12, 2))
    unit_price = fields.Float(string="Unit Price", required=True, digits=(12, 2))
    tax_ids = fields.Many2many(
        'subscription.tax',
        'sub_line_tax_rel',
        'line_id',
        'tax_id',
        string="Taxes"
    )
    discount = fields.Float(string="Discount (%)", digits=(5, 2), default=0.0)

    subtotal = fields.Float(string="Subtotal", compute='_compute_amounts', store=True, digits=(12, 2))
    tax_amount = fields.Float(string="Tax Amount", compute='_compute_amounts', store=True, digits=(12, 2))
    total = fields.Float(string="Total", compute='_compute_amounts', store=True, digits=(12, 2))
    price_with_variant = fields.Float(string="Effective Unit Price", compute='_compute_price_with_variant', digits=(12, 2))

    @api.depends('unit_price', 'variant_id.price_extra')
    def _compute_price_with_variant(self):
        for line in self:
            extra = line.variant_id.price_extra if line.variant_id else 0.0
            line.price_with_variant = line.unit_price + extra

    @api.depends('quantity', 'unit_price', 'discount', 'tax_ids', 'variant_id.price_extra')
    def _compute_amounts(self):
        for line in self:
            base_unit = line.unit_price + (line.variant_id.price_extra if line.variant_id else 0.0)
            if line.discount:
                base_unit = base_unit * (1.0 - (line.discount / 100.0))
            subtotal = line.quantity * base_unit
            line.subtotal = subtotal

            tax_val = 0.0
            for tax in line.tax_ids:
                if tax.tax_type == 'percentage':
                    tax_val += subtotal * (tax.amount / 100.0)
                elif tax.tax_type == 'fixed':
                    tax_val += tax.amount * line.quantity
            line.tax_amount = tax_val
            line.total = line.subtotal + line.tax_amount

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.unit_price = self.product_id.sales_price
            self.variant_id = False

    _sql_constraints = [
        ('quantity_positive', 'CHECK(quantity > 0)', 'Quantity must be strictly greater than 0!'),
        ('unit_price_positive', 'CHECK(unit_price >= 0)', 'Unit price must be positive or zero!'),
        ('discount_range', 'CHECK(discount >= 0 AND discount <= 100)', 'Discount must be between 0% and 100%!'),
    ]
