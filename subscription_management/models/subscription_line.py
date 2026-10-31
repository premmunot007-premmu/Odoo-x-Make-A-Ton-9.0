# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SubscriptionLine(models.Model):
    """A product line on a subscription; the variant's extra price is added to the unit price."""

    _name = 'subscription.subscription.line'
    _description = 'Subscription Line'

    subscription_id = fields.Many2one(
        'subscription.subscription', string="Subscription", required=True, ondelete='cascade', index=True,
    )
    currency_id = fields.Many2one(related='subscription_id.currency_id')
    product_id = fields.Many2one('subscription.product', string="Product", required=True)
    variant_id = fields.Many2one(
        'subscription.product.variant', string="Variant", domain="[('product_id', '=', product_id)]",
    )
    quantity = fields.Float(string="Quantity", required=True, default=1.0)
    unit_price = fields.Float(string="Unit Price", required=True, digits=(10, 2))
    tax_ids = fields.Many2many('subscription.tax', string="Taxes", domain=[('is_active', '=', True)])
    discount = fields.Float(string="Discount (%)", default=0.0)
    subtotal = fields.Monetary(string="Subtotal", compute='_compute_amounts', store=True)
    tax_amount = fields.Monetary(string="Tax Amount", compute='_compute_amounts', store=True)
    total = fields.Monetary(string="Total", compute='_compute_amounts', store=True)

    @api.depends(
        'quantity', 'unit_price', 'discount', 'variant_id.price_extra',
        'tax_ids.amount', 'tax_ids.tax_type',
    )
    def _compute_amounts(self):
        """Subtotal = qty × (unit price + variant extra) less discount; taxes apply to the subtotal."""
        for line in self:
            price = line.unit_price + line.variant_id.price_extra
            subtotal = line.quantity * price * (1 - line.discount / 100.0)
            tax_amount = sum(tax.compute_tax(subtotal) for tax in line.tax_ids)
            line.subtotal = subtotal
            line.tax_amount = tax_amount
            line.total = subtotal + tax_amount

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Prefill the price and drop a variant that belongs to another product."""
        if self.product_id:
            self.unit_price = self.product_id.sales_price
        if self.variant_id.product_id != self.product_id:
            self.variant_id = False

    @api.constrains('product_id', 'variant_id')
    def _check_variant_product(self):
        for line in self:
            if line.variant_id and line.variant_id.product_id != line.product_id:
                raise ValidationError(_("The variant must belong to the selected product."))

    @api.constrains('discount')
    def _check_discount(self):
        for line in self:
            if not 0.0 <= line.discount <= 100.0:
                raise ValidationError(_("Discount must be between 0 and 100%."))

    @api.constrains('quantity')
    def _check_quantity(self):
        for line in self:
            if line.quantity <= 0:
                raise ValidationError(_("Quantity must be greater than zero."))
