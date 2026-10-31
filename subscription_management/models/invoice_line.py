# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class SubscriptionInvoiceLine(models.Model):
    _name = 'subscription.invoice.line'
    _description = 'Subscription Invoice Line'
    _order = 'sequence, id'

    invoice_id = fields.Many2one('subscription.invoice', string="Invoice", required=True, ondelete='cascade')
    product_id = fields.Many2one('subscription.product', string="Product", required=True)
    description = fields.Char(string="Description", required=True)
    sequence = fields.Integer(string="Sequence", default=10)
    quantity = fields.Float(string="Quantity", required=True, default=1.0, digits=(12, 2))
    unit_price = fields.Float(string="Unit Price", required=True, digits=(12, 2))
    tax_ids = fields.Many2many('subscription.tax', 'inv_line_tax_rel', 'line_id', 'tax_id', string="Taxes")
    discount_amount = fields.Float(string="Discount (₹)", default=0.0, digits=(12, 2))

    subtotal = fields.Float(string="Subtotal", compute='_compute_amounts', store=True, digits=(12, 2))
    tax_amount = fields.Float(string="Tax Amount", compute='_compute_amounts', store=True, digits=(12, 2))
    total = fields.Float(string="Total", compute='_compute_amounts', store=True, digits=(12, 2))

    @api.depends('quantity', 'unit_price', 'discount_amount', 'tax_ids')
    def _compute_amounts(self):
        for line in self:
            base = max((line.quantity * line.unit_price) - (line.discount_amount or 0.0), 0.0)
            line.subtotal = base

            tax_val = 0.0
            for tax in line.tax_ids:
                if tax.tax_type == 'percentage':
                    tax_val += base * (tax.amount / 100.0)
                elif tax.tax_type == 'fixed':
                    tax_val += tax.amount * line.quantity
            line.tax_amount = tax_val
            line.total = line.subtotal + line.tax_amount

    _sql_constraints = [
        ('quantity_positive', 'CHECK(quantity > 0)', 'Invoice quantity must be positive!'),
        ('unit_price_positive', 'CHECK(unit_price >= 0)', 'Invoice unit price must be positive or zero!'),
    ]
