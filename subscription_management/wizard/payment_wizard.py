# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SubscriptionPaymentWizard(models.TransientModel):
    _name = 'subscription.payment.wizard'
    _description = 'Register Invoice Payment Wizard'

    invoice_id = fields.Many2one('subscription.invoice', string="Invoice", required=True)
    partner_id = fields.Many2one('res.partner', related='invoice_id.partner_id', readonly=True, string="Customer")
    currency_id = fields.Many2one('res.currency', related='invoice_id.currency_id', readonly=True)
    amount = fields.Monetary(string="Payment Amount", required=True, currency_field='currency_id')
    amount_due = fields.Monetary(related='invoice_id.amount_due', readonly=True, string="Outstanding Balance", currency_field='currency_id')
    payment_method = fields.Selection([
        ('bank_transfer', 'Bank Transfer'),
        ('credit_card', 'Credit Card'),
        ('upi', 'UPI'),
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
    ], default='bank_transfer', required=True, string="Payment Method")
    payment_date = fields.Date(default=fields.Date.today, required=True, string="Payment Date")
    reference = fields.Char(string="Payment Reference / Transaction ID")
    note = fields.Text(string="Note")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')
        if active_id:
            invoice = self.env['subscription.invoice'].browse(active_id)
            if invoice.exists():
                res.update({
                    'invoice_id': invoice.id,
                    'amount': invoice.amount_due,
                })
        return res

    def action_confirm_payment(self):
        self.ensure_one()
        if self.amount <= 0:
            raise ValidationError("Payment amount must be greater than zero.")
        if self.amount > self.invoice_id.amount_due:
            raise ValidationError("Payment amount exceeds outstanding balance.")

        self.env['subscription.payment'].create({
            'invoice_id': self.invoice_id.id,
            'amount': self.amount,
            'payment_method': self.payment_method,
            'payment_date': self.payment_date,
            'reference': self.reference,
            'note': self.note,
        })
        return {'type': 'ir.actions.act_window_close'}
