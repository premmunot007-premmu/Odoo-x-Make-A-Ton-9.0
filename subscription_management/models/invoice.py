# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero


class SubscriptionInvoice(models.Model):
    """An invoice billed from a subscription, moving through Draft → Confirmed → Paid (or Cancelled)."""

    _name = 'subscription.invoice'
    _description = 'Subscription Invoice'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'invoice_date desc, name desc'

    name = fields.Char(
        string="Invoice Number", readonly=True, copy=False, default='New', index='trigram',
    )
    subscription_id = fields.Many2one(
        'subscription.subscription', string="Subscription", tracking=True, index=True,
    )
    partner_id = fields.Many2one('res.partner', string="Customer", required=True, tracking=True)
    invoice_date = fields.Date(
        string="Invoice Date", required=True, default=fields.Date.context_today, tracking=True,
    )
    due_date = fields.Date(string="Due Date", tracking=True)
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('paid', 'Paid'),
            ('cancelled', 'Cancelled'),
        ],
        string="Status",
        default='draft',
        required=True,
        copy=False,
        tracking=True,
    )
    invoice_line_ids = fields.One2many(
        'subscription.invoice.line', 'invoice_id', string="Invoice Lines", copy=True,
    )
    payment_ids = fields.One2many('subscription.payment', 'invoice_id', string="Payments")
    amount_untaxed = fields.Monetary(string="Untaxed Amount", compute='_compute_amounts', store=True)
    amount_tax = fields.Monetary(string="Taxes", compute='_compute_amounts', store=True)
    amount_total = fields.Monetary(string="Total", compute='_compute_amounts', store=True, tracking=True)
    amount_paid = fields.Monetary(string="Amount Paid", compute='_compute_payment_status', store=True)
    amount_due = fields.Monetary(string="Amount Due", compute='_compute_payment_status', store=True)
    payment_status = fields.Selection(
        [
            ('not_paid', 'Not Paid'),
            ('partial', 'Partially Paid'),
            ('paid', 'Fully Paid'),
        ],
        string="Payment Status",
        compute='_compute_payment_status',
        store=True,
    )
    is_overdue = fields.Boolean(
        string="Overdue", compute='_compute_is_overdue', search='_search_is_overdue',
    )
    company_id = fields.Many2one(
        'res.company', string="Company", required=True, default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Currency")
    total_amount = fields.Monetary(string="Total Amount", compute='_compute_total_amount', store=True)
    subtotal = fields.Monetary(string="Untaxed Subtotal", compute='_compute_subtotal', store=True)
    tax_amount = fields.Monetary(string="Tax Amount", compute='_compute_tax_amount', store=True)
    notes = fields.Text(string="Notes Text", compute='_compute_notes', inverse='_inverse_notes', store=True)

    @api.depends('amount_total')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = rec.amount_total

    @api.depends('amount_untaxed')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.amount_untaxed

    @api.depends('amount_tax')
    def _compute_tax_amount(self):
        for rec in self:
            rec.tax_amount = rec.amount_tax

    @api.depends('note')
    def _compute_notes(self):
        for rec in self:
            rec.notes = rec.note

    def _inverse_notes(self):
        for rec in self:
            rec.note = rec.notes

    note = fields.Text(string="Notes")

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name, company_id)', 'Invoice number must be unique per company!'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        """Assign the next invoice number from the sequence."""
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('subscription.invoice') or 'New'
        return super().create(vals_list)

    @api.ondelete(at_uninstall=False)
    def _unlink_except_posted(self):
        """Only draft or cancelled invoices may be deleted, to keep billing history intact."""
        if self.filtered(lambda r: r.state in ('confirmed', 'paid')):
            raise UserError(_("You cannot delete a confirmed or paid invoice. Cancel it first."))

    # ------------------------------------------------------------------
    # Computes
    # ------------------------------------------------------------------

    @api.depends('invoice_line_ids.subtotal', 'invoice_line_ids.tax_amount')
    def _compute_amounts(self):
        for rec in self:
            rec.amount_untaxed = sum(rec.invoice_line_ids.mapped('subtotal'))
            rec.amount_tax = sum(rec.invoice_line_ids.mapped('tax_amount'))
            rec.amount_total = rec.amount_untaxed + rec.amount_tax

    @api.depends('payment_ids.amount', 'amount_total')
    def _compute_payment_status(self):
        for rec in self:
            rounding = rec.currency_id.rounding or 0.01
            rec.amount_paid = sum(rec.payment_ids.mapped('amount'))
            rec.amount_due = rec.amount_total - rec.amount_paid
            if float_is_zero(rec.amount_paid, precision_rounding=rounding):
                rec.payment_status = 'not_paid'
            elif float_compare(rec.amount_paid, rec.amount_total, precision_rounding=rounding) < 0:
                rec.payment_status = 'partial'
            else:
                rec.payment_status = 'paid'

    @api.depends('due_date', 'state')
    def _compute_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            rec.is_overdue = bool(
                rec.due_date and rec.due_date < today and rec.state not in ('paid', 'cancelled')
            )

    def _search_is_overdue(self, operator, value):
        """Evaluated against today's date at search time, so it never goes stale."""
        if operator not in ('=', '!='):
            raise UserError(_("Unsupported search operator for 'Overdue'."))
        today = fields.Date.context_today(self)
        overdue_domain = [
            ('due_date', '!=', False),
            ('due_date', '<', today),
            ('state', 'not in', ('paid', 'cancelled')),
        ]
        if (operator == '=') == bool(value):
            return overdue_domain
        return ['!', '&', '&'] + overdue_domain

    def _compute_access_url(self):
        super()._compute_access_url()
        for rec in self:
            rec.access_url = f'/my/subscription-invoices/{rec.id}'

    # ------------------------------------------------------------------
    # State transitions
    # ------------------------------------------------------------------

    def _check_state(self, allowed_states, action_label):
        """Raise if any record is not in one of ``allowed_states``."""
        invalid = self.filtered(lambda r: r.state not in allowed_states)
        if invalid:
            raise UserError(_(
                "Cannot %(action)s invoice(s) %(names)s in their current status.",
                action=action_label,
                names=", ".join(invalid.mapped('name')),
            ))

    def action_confirm(self):
        self._check_state(['draft'], _("confirm"))
        if self.filtered(lambda r: not r.invoice_line_ids):
            raise UserError(_("You cannot confirm an invoice without lines."))
        self.write({'state': 'confirmed'})

    def action_cancel(self):
        self._check_state(['draft', 'confirmed'], _("cancel"))
        if self.filtered('payment_ids'):
            raise UserError(_("You cannot cancel an invoice that has payments. Delete the payments first."))
        self.write({'state': 'cancelled'})

    def action_mark_paid(self):
        self._check_state(['confirmed'], _("mark as paid"))
        self.write({'state': 'paid'})

    def action_draft(self):
        return self.action_reset_to_draft()

    def action_reset_to_draft(self):
        self._check_state(['cancelled'], _("reset to draft"))
        self.write({'state': 'draft'})

    def action_register_payment(self):
        """Open a payment form in a dialog, prefilled with this invoice and its amount due."""
        self.ensure_one()
        self._check_state(['confirmed'], _("register a payment for"))
        return {
            'type': 'ir.actions.act_window',
            'name': _("Register Payment"),
            'res_model': 'subscription.payment',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_invoice_id': self.id,
                'default_amount': self.amount_due,
            },
        }

    def _sync_state_with_payments(self):
        """Move confirmed invoices to Paid once fully paid, and back if a payment is edited or removed."""
        self.filtered(lambda r: r.state == 'confirmed' and r.payment_status == 'paid').write({'state': 'paid'})
        self.filtered(lambda r: r.state == 'paid' and r.payment_status != 'paid').write({'state': 'confirmed'})


class SubscriptionInvoiceLine(models.Model):
    """A billed product line; ``discount_amount`` is an absolute amount deducted from the line."""

    _name = 'subscription.invoice.line'
    _description = 'Invoice Line'

    invoice_id = fields.Many2one(
        'subscription.invoice', string="Invoice", required=True, ondelete='cascade', index=True,
    )
    currency_id = fields.Many2one(related='invoice_id.currency_id')
    product_id = fields.Many2one('subscription.product', string="Product", required=True)
    description = fields.Char(string="Description")
    quantity = fields.Float(string="Quantity", required=True, default=1.0)
    unit_price = fields.Float(string="Unit Price", required=True, digits=(10, 2))
    tax_ids = fields.Many2many('subscription.tax', string="Taxes", domain=[('is_active', '=', True)])
    tax_id = fields.Many2one('subscription.tax', string="Tax", compute='_compute_single_tax', inverse='_inverse_single_tax')
    discount_amount = fields.Float(string="Discount Amount", default=0.0, digits=(10, 2))
    discount = fields.Float(string="Discount (%)", default=0.0)
    subtotal = fields.Monetary(string="Subtotal", compute='_compute_amounts', store=True)
    tax_amount = fields.Monetary(string="Tax Amount", compute='_compute_amounts', store=True)
    total = fields.Monetary(string="Total", compute='_compute_amounts', store=True)

    @api.depends('tax_ids')
    def _compute_single_tax(self):
        for rec in self:
            rec.tax_id = rec.tax_ids[0] if rec.tax_ids else False

    def _inverse_single_tax(self):
        for rec in self:
            if rec.tax_id:
                rec.tax_ids = [(6, 0, [rec.tax_id.id])]
            else:
                rec.tax_ids = [(5, 0, 0)]

    @api.depends('quantity', 'unit_price', 'discount_amount', 'tax_ids.amount', 'tax_ids.tax_type')
    def _compute_amounts(self):
        """Subtotal = qty × unit price − discount; taxes apply to the subtotal."""
        for line in self:
            subtotal = (line.quantity * line.unit_price) - line.discount_amount
            tax_amount = sum(tax.compute_tax(subtotal) for tax in line.tax_ids)
            line.subtotal = subtotal
            line.tax_amount = tax_amount
            line.total = subtotal + tax_amount

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Prefill the description and price from the product."""
        if self.product_id:
            self.description = self.product_id.name
            self.unit_price = self.product_id.sales_price
