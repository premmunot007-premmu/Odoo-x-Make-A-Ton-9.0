# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class SubscriptionQuotationTemplate(models.Model):
    _name = 'subscription.quotation.template'
    _description = 'Subscription Quotation Template'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(string="Template Name", required=True)
    plan_id = fields.Many2one('subscription.plan', string="Subscription Plan", required=True, ondelete='restrict')
    validity_days = fields.Integer(string="Quotation Validity (Days)", default=30)
    description = fields.Html(string="Description / Offer Terms")
    is_active = fields.Boolean(string="Active", default=True)
    template_line_ids = fields.One2many('subscription.quotation.template.line', 'template_id', string="Template Lines")

    line_count = fields.Integer(string="Line Count", compute='_compute_line_count')
    total_amount = fields.Float(string="Total Amount", compute='_compute_total_amount', digits=(12, 2))

    @api.depends('template_line_ids')
    def _compute_line_count(self):
        for record in self:
            record.line_count = len(record.template_line_ids)

    @api.depends('template_line_ids.quantity', 'template_line_ids.unit_price')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(line.quantity * line.unit_price for line in record.template_line_ids)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Template name must be unique!'),
        ('validity_positive', 'CHECK(validity_days > 0)', 'Validity days must be positive!'),
    ]


class SubscriptionQuotationTemplateLine(models.Model):
    _name = 'subscription.quotation.template.line'
    _description = 'Quotation Template Line'
    _order = 'sequence, id'

    template_id = fields.Many2one('subscription.quotation.template', string="Template", required=True, ondelete='cascade')
    product_id = fields.Many2one('subscription.product', string="Product", required=True, ondelete='restrict')
    sequence = fields.Integer(string="Sequence", default=10)
    quantity = fields.Float(string="Quantity", required=True, default=1.0, digits=(12, 2))
    unit_price = fields.Float(string="Unit Price", required=True, digits=(12, 2))
    subtotal = fields.Float(string="Subtotal", compute='_compute_subtotal', store=True, digits=(12, 2))

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.unit_price = self.product_id.sales_price

    _sql_constraints = [
        ('quantity_positive', 'CHECK(quantity > 0)', 'Quantity must be positive!'),
        ('unit_price_positive', 'CHECK(unit_price >= 0)', 'Unit price must be positive or zero!'),
    ]
