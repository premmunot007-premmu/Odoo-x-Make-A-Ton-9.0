# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SubscriptionPayment(models.Model):
    _name = 'subscription.payment'
    _description = 'Subscription Payment'
    _inherit = ['mail.thread']
    _order = 'payment_date desc, id desc'
    _rec_name = 'name'

    name = fields.Char(string="Payment Reference", compute='_compute_name', store=True)
    invoice_id = fields.Many2one('subscription.invoice', string="Invoice", required=True, tracking=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string="Customer", related='invoice_id.partner_id', store=True, readonly=True)
    payment_method = fields.Selection([
        ('bank_transfer', 'Bank Transfer (NEFT/RTGS/IMPS)'),
        ('credit_card', 'Credit / Debit Card'),
        ('upi', 'UPI / QR Code'),
        ('cash', 'Cash'),
        ('cheque', 'Cheque / Draft'),
    ], string="Payment Method", required=True, default='bank_transfer', tracking=True)
    amount = fields.Float(string="Amount Paid (₹)", required=True, digits=(12, 2), tracking=True)
    payment_date = fields.Date(string="Payment Date", required=True, default=fields.Date.today, tracking=True)
    reference = fields.Char(string="Transaction ID / UTR", tracking=True)
    note = fields.Text(string="Internal Note")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string="Currency", related='company_id.currency_id')

    @api.depends('invoice_id.name', 'payment_date')
    def _compute_name(self):
        for rec in self:
            inv_name = rec.invoice_id.name or 'INV'
            date_str = rec.payment_date or fields.Date.today()
            rec.name = f"PAY/{inv_name}/{date_str}"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for payment in records:
            inv = payment.invoice_id
            if inv.state == 'confirmed' and inv.amount_due <= 0:
                inv.write({'state': 'paid'})
                inv.message_post(body=_("Invoice fully settled via %s (₹%s).") % (payment.payment_method, payment.amount))
            else:
                inv.message_post(body=_("Payment of ₹%s received via %s. Remaining: ₹%s.") % (payment.amount, payment.payment_method, inv.amount_due))

            # Send receipt email if available
            template = self.env.ref('subscription_management.email_template_payment_received', raise_if_not_found=False)
            if template:
                template.send_mail(payment.id, force_send=False)
        return records

    @api.constrains('amount')
    def _check_amount(self):
        for rec in self:
            if rec.amount <= 0:
                raise ValidationError(_("Payment amount must be greater than zero!"))

    _sql_constraints = [
        ('positive_amount', 'CHECK(amount > 0)', 'Payment amount must be strictly positive!'),
    ]
