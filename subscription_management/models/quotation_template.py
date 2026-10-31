# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SubscriptionQuotationTemplate(models.Model):
    """A pre-built quotation: a plan plus default product lines that sales reps load into a subscription."""

    _name = 'subscription.quotation.template'
    _description = 'Quotation Template'
    _order = 'name'

    name = fields.Char(string="Template Name", required=True)
    plan_id = fields.Many2one('subscription.plan', string="Plan", required=True)
    validity_days = fields.Integer(
        string="Validity (Days)", default=30, help="Number of days the quotation remains valid",
    )
    template_line_ids = fields.One2many(
        'subscription.quotation.template.line', 'template_id', string="Template Lines", copy=True,
    )
    is_active = fields.Boolean(string="Active", default=True)
    note = fields.Text(string="Notes")

    _sql_constraints = [
        ('positive_validity', 'CHECK(validity_days >= 0)', 'Validity cannot be negative!'),
    ]


class SubscriptionQuotationTemplateLine(models.Model):
    """A default product line on a quotation template."""

    _name = 'subscription.quotation.template.line'
    _description = 'Quotation Template Line'

    template_id = fields.Many2one(
        'subscription.quotation.template', string="Template", required=True, ondelete='cascade', index=True,
    )
    product_id = fields.Many2one('subscription.product', string="Product", required=True)
    quantity = fields.Float(string="Quantity", default=1.0)
    unit_price = fields.Float(string="Unit Price", digits=(10, 2))

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Prefill the unit price from the product's sales price."""
        if self.product_id:
            self.unit_price = self.product_id.sales_price

    @api.constrains('quantity')
    def _check_quantity(self):
        for line in self:
            if line.quantity <= 0:
                raise ValidationError(_("Quantity must be greater than zero."))
