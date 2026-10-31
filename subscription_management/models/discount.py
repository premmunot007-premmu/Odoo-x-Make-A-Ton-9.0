# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SubscriptionDiscountRule(models.Model):
    _name = 'subscription.discount.rule'
    _description = 'Subscription Discount Rule'
    _order = 'name asc'
    _rec_name = 'name'

    name = fields.Char(string="Discount Rule Name", required=True)
    discount_type = fields.Selection([
        ('percentage', 'Percentage (%)'),
        ('fixed', 'Fixed Amount (₹)'),
    ], string="Discount Type", required=True, default='percentage')
    amount = fields.Float(string="Discount Value", required=True, digits=(12, 2), default=0.0)
    apply_on = fields.Selection([
        ('subscription', 'Entire Subscription'),
        ('product', 'Specific Products'),
    ], string="Apply On", required=True, default='subscription')
    product_ids = fields.Many2many('subscription.product', 'sub_disc_prod_rel', 'disc_id', 'prod_id', string="Applicable Products")
    min_purchase = fields.Float(string="Minimum Purchase Amount (₹)", digits=(12, 2), default=0.0)
    min_quantity = fields.Integer(string="Minimum Seats / Quantity", default=0)
    date_start = fields.Date(string="Valid From")
    date_end = fields.Date(string="Valid Until")
    max_usage = fields.Integer(string="Usage Limit (0 = Unlimited)", default=0)
    current_usage = fields.Integer(string="Times Used", default=0, readonly=True)
    is_active = fields.Boolean(string="Active", compute='_compute_is_active', store=True)
    description = fields.Text(string="Terms & Conditions")

    @api.depends('date_start', 'date_end', 'max_usage', 'current_usage')
    def _compute_is_active(self):
        today = fields.Date.today()
        for rec in self:
            active = True
            if rec.date_start and today < rec.date_start:
                active = False
            if rec.date_end and today > rec.date_end:
                active = False
            if rec.max_usage > 0 and rec.current_usage >= rec.max_usage:
                active = False
            rec.is_active = active

    @api.constrains('amount', 'discount_type')
    def _check_amount(self):
        for rec in self:
            if rec.amount <= 0:
                raise ValidationError(_("Discount amount must be strictly greater than 0."))
            if rec.discount_type == 'percentage' and rec.amount > 100:
                raise ValidationError(_("Percentage discount cannot exceed 100%."))
