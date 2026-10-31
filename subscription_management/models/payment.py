# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class SubscriptionPayment(models.Model):
    """A payment received against a confirmed invoice; the invoice becomes Paid once fully settled."""

    _name = 'subscription.payment'
    _description = 'Payment'
    _inherit = ['mail.thread']
    _order = 'payment_date desc, id desc'

    name = fields.Char(string="Payment Reference", compute='_compute_name', store=True)
    invoice_id = fields.Many2one(
        'subscription.invoice',
        string="Invoice",
        required=True,
        ondelete='restrict',
        index=True,
        tracking=True,
        domain=[('state', '=', 'confirmed')],
    )
    partner_id = fields.Many2one(
        'res.partner', related='invoice_id.partner_id', store=True, string="Customer",
    )
    payment_method = fields.Selection(
        [
            ('bank_transfer', 'Bank Transfer'),
            ('credit_card', 'Credit Card'),
            ('upi', 'UPI'),
            ('cash', 'Cash'),
            ('cheque', 'Cheque'),
        ],
        string="Payment Method",
        required=True,
        default='bank_transfer',
        tracking=True,
    )
    amount = fields.Monetary(string="Amount Paid", required=True, tracking=True)
    payment_date = fields.Date(
        string="Payment Date", required=True, default=fields.Date.context_today, tracking=True,
    )
    note = fields.Text(string="Payment Note")
    reference = fields.Char(string="Transaction Reference")
    company_id = fields.Many2one(
        'res.company', related='invoice_id.company_id', store=True, string="Company",
    )
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Currency")

    _sql_constraints = [
        ('positive_amount', 'CHECK(amount > 0)', 'Payment amount must be positive!'),
    ]

    @api.depends('invoice_id.name', 'payment_date')
    def _compute_name(self):
        for rec in self:
            rec.name = f"PAY/{rec.invoice_id.name or ''}/{rec.payment_date or ''}"

    @api.onchange('invoice_id')
    def _onchange_invoice_id(self):
        """Prefill the outstanding amount."""
        if self.invoice_id and not self.amount:
            self.amount = self.invoice_id.amount_due

    @api.constrains('invoice_id', 'amount')
    def _check_invoice(self):
        """Payments only go to confirmed/paid invoices and may not exceed the invoice total."""
        for rec in self:
            invoice = rec.invoice_id
            if invoice.state not in ('confirmed', 'paid'):
                raise ValidationError(_(
                    "Payments can only be registered on confirmed invoices; %s is not confirmed.",
                    invoice.name,
                ))
            rounding = invoice.currency_id.rounding or 0.01
            if float_compare(invoice.amount_paid, invoice.amount_total, precision_rounding=rounding) > 0:
                raise ValidationError(_(
                    "Payments on %(invoice)s would total %(paid).2f, more than the invoice total of %(total).2f.",
                    invoice=invoice.name,
                    paid=invoice.amount_paid,
                    total=invoice.amount_total,
                ))

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records.invoice_id._sync_state_with_payments()
        return records

    def write(self, vals):
        old_invoices = self.invoice_id
        res = super().write(vals)
        (old_invoices | self.invoice_id)._sync_state_with_payments()
        return res

    def unlink(self):
        invoices = self.invoice_id
        res = super().unlink()
        invoices._sync_state_with_payments()
        return res
