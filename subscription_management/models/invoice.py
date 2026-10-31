# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SubscriptionInvoice(models.Model):
    _name = 'subscription.invoice'
    _description = 'Subscription Invoice'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'invoice_date desc, id desc'
    _rec_name = 'name'

    name = fields.Char(string="Invoice Number", readonly=True, copy=False, default='New', tracking=True)
    subscription_id = fields.Many2one('subscription.subscription', string="Subscription", ondelete='restrict', tracking=True)
    partner_id = fields.Many2one('res.partner', string="Customer", required=True, tracking=True)
    invoice_date = fields.Date(string="Invoice Date", required=True, default=fields.Date.today, tracking=True)
    due_date = fields.Date(string="Due Date", tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft', required=True, tracking=True, copy=False)
    invoice_line_ids = fields.One2many('subscription.invoice.line', 'invoice_id', string="Invoice Lines")
    payment_ids = fields.One2many('subscription.payment', 'invoice_id', string="Payments")
    note = fields.Text(string="Notes / Payment Instructions")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string="Currency", related='company_id.currency_id')

    amount_untaxed = fields.Float(string="Untaxed Amount", compute='_compute_amounts', store=True, digits=(12, 2))
    amount_tax = fields.Float(string="Taxes", compute='_compute_amounts', store=True, digits=(12, 2))
    amount_total = fields.Float(string="Total Amount", compute='_compute_amounts', store=True, digits=(12, 2))

    amount_paid = fields.Float(string="Amount Paid", compute='_compute_payment_amounts', store=True, digits=(12, 2))
    amount_due = fields.Float(string="Amount Due", compute='_compute_payment_amounts', store=True, digits=(12, 2))
    payment_status = fields.Selection([
        ('not_paid', 'Not Paid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Fully Paid')
    ], string="Payment Status", compute='_compute_payment_amounts', store=True)
    is_overdue = fields.Boolean(string="Is Overdue", compute='_compute_is_overdue', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('subscription.invoice') or 'New'
        return super().create(vals_list)

    @api.depends('invoice_line_ids.subtotal', 'invoice_line_ids.tax_amount', 'invoice_line_ids.total')
    def _compute_amounts(self):
        for invoice in self:
            lines = invoice.invoice_line_ids
            invoice.amount_untaxed = sum(lines.mapped('subtotal'))
            invoice.amount_tax = sum(lines.mapped('tax_amount'))
            invoice.amount_total = sum(lines.mapped('total'))

    @api.depends('payment_ids.amount', 'amount_total')
    def _compute_payment_amounts(self):
        for invoice in self:
            paid = sum(invoice.payment_ids.mapped('amount'))
            invoice.amount_paid = paid
            invoice.amount_due = max(invoice.amount_total - paid, 0.0)
            if paid <= 0:
                invoice.payment_status = 'not_paid'
            elif paid < invoice.amount_total:
                invoice.payment_status = 'partial'
            else:
                invoice.payment_status = 'paid'

    @api.depends('due_date', 'state', 'payment_status')
    def _compute_is_overdue(self):
        today = fields.Date.today()
        for invoice in self:
            invoice.is_overdue = bool(
                invoice.due_date and invoice.due_date < today and
                invoice.state == 'confirmed' and invoice.payment_status != 'paid'
            )

    def _compute_access_url(self):
        super()._compute_access_url()
        for rec in self:
            rec.access_url = f'/my/invoices/{rec.id}'

    def action_confirm(self):
        for invoice in self:
            if invoice.state != 'draft':
                raise UserError(_("Only draft invoices can be confirmed."))
            if not invoice.invoice_line_ids:
                raise UserError(_("Cannot confirm an invoice without lines."))
            invoice.state = 'confirmed'
            invoice.message_post(body=_("Invoice confirmed."))
            # Send invoice email template
            template = self.env.ref('subscription_management.email_template_invoice_sent', raise_if_not_found=False)
            if template:
                template.send_mail(invoice.id, force_send=False)

    def action_cancel(self):
        for invoice in self:
            if invoice.state not in ('draft', 'confirmed'):
                raise UserError(_("Only draft or confirmed invoices can be cancelled."))
            if invoice.payment_ids:
                raise UserError(_("Cannot cancel an invoice with payments registered. Please refund/delete payments first."))
            invoice.state = 'cancelled'
            invoice.message_post(body=_("Invoice cancelled."))

    def action_set_to_draft(self):
        for invoice in self:
            if invoice.state != 'cancelled':
                raise UserError(_("Only cancelled invoices can be reset to draft."))
            invoice.state = 'draft'

    def action_register_payment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Register Payment'),
            'res_model': 'subscription.payment',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_invoice_id': self.id,
                'default_amount': self.amount_due,
                'default_payment_date': fields.Date.today(),
            },
        }

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Invoice number must be unique!'),
    ]
