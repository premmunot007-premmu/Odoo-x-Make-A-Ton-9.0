# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class SubscriptionTax(models.Model):
    _name = 'subscription.tax'
    _description = 'Subscription Tax Rule'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(string="Tax Name (e.g. GST 18%)", required=True)
    tax_type = fields.Selection([
        ('percentage', 'Percentage (%)'),
        ('fixed', 'Fixed Levy (₹)'),
    ], string="Tax Type", required=True, default='percentage')
    amount = fields.Float(string="Rate / Amount", required=True, digits=(12, 2), default=0.0)
    is_active = fields.Boolean(string="Active", default=True)
    description = fields.Text(string="Description / Tax Note")

    def compute_tax(self, base_amount, quantity=1.0):
        self.ensure_one()
        if self.tax_type == 'percentage':
            return base_amount * (self.amount / 100.0)
        elif self.tax_type == 'fixed':
            return self.amount * quantity
        return 0.0

    def name_get(self):
        res = []
        for rec in self:
            label = f"{rec.name} ({rec.amount}%)" if rec.tax_type == 'percentage' else f"{rec.name} (₹{rec.amount})"
            res.append((rec.id, label))
        return res
