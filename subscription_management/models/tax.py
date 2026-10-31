# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SubscriptionTax(models.Model):
    """A tax applied to subscription and invoice lines, as a percentage or a fixed amount."""

    _name = 'subscription.tax'
    _description = 'Tax Rule'
    _order = 'name'

    name = fields.Char(string="Tax Name", required=True, help="e.g. GST 18%, Service Tax 5%")
    tax_type = fields.Selection(
        [
            ('percentage', 'Percentage'),
            ('fixed', 'Fixed Amount'),
        ],
        string="Tax Type",
        required=True,
        default='percentage',
    )
    amount = fields.Float(
        string="Amount", required=True, digits=(10, 2), help="Percentage value or fixed amount",
    )
    is_active = fields.Boolean(string="Active", default=True)
    description = fields.Text(string="Description")

    _sql_constraints = [
        ('positive_amount', 'CHECK(amount >= 0)', 'Tax amount cannot be negative!'),
    ]

    @api.depends('name', 'tax_type', 'amount')
    def _compute_display_name(self):
        """Show the rate next to the name, e.g. "GST (18.0%)" or "Cess (₹50.0)"."""
        symbol = self.env.company.currency_id.symbol or ''
        for tax in self:
            if tax.tax_type == 'percentage':
                tax.display_name = f"{tax.name} ({tax.amount}%)"
            else:
                tax.display_name = f"{tax.name} ({symbol}{tax.amount})"

    @api.constrains('tax_type', 'amount')
    def _check_percentage(self):
        for tax in self:
            if tax.tax_type == 'percentage' and tax.amount > 100:
                raise ValidationError(_("A percentage tax cannot exceed 100%."))

    def compute_tax(self, base_amount):
        """Compute tax on given base amount"""
        self.ensure_one()
        if self.tax_type == 'percentage':
            return base_amount * (self.amount / 100.0)
        return self.amount
