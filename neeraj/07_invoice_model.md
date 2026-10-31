# 07 — Invoice Model

## Context
Invoices are generated from active subscriptions on billing day. Each invoice captures a snapshot of the subscription at billing time — the customer, products, quantities, prices, taxes, and totals. Invoices move through states: Draft → Confirmed → Paid (or Cancelled). The invoice model must prevent duplicate billing for the same period and support payment tracking. This replaces the manual invoice creation that Brightloop was doing with spreadsheets.

This file depends on: `01_module_scaffold.md`, `04_subscription_model.md`.

## Prompt for Antigravity

```
Create an Odoo 18 model file for invoicing in the subscription_management module.

Create file: E:\odoo18\custom_addons\subscription_management\models\invoice.py

### Model: subscription.invoice

This model represents invoices generated from subscriptions.

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class SubscriptionInvoice(models.Model):
    _name = 'subscription.invoice'
    _description = 'Subscription Invoice'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'invoice_date desc, id desc'
    _rec_name = 'name'

    Fields:
    - name: Char, string="Invoice Number", readonly=True, copy=False, default='New', tracking=True
    - subscription_id: Many2one to 'subscription.subscription', string="Subscription", ondelete='restrict', tracking=True
    - partner_id: Many2one to 'res.partner', required=True, string="Customer", tracking=True
    - invoice_date: Date, required=True, string="Invoice Date", default=fields.Date.today, tracking=True
    - due_date: Date, string="Due Date", tracking=True
    - state: Selection with choices [
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled')
      ], default='draft', required=True, string="Status", tracking=True, copy=False
    - invoice_line_ids: One2many to 'subscription.invoice.line', inverse field 'invoice_id', string="Invoice Lines"
    - payment_ids: One2many to 'subscription.payment', inverse field 'invoice_id', string="Payments"
    - note: Text, string="Notes"
    - company_id: Many2one to 'res.company', string="Company", default=lambda self: self.env.company
    - billing_period_start: Date, string="Billing Period Start"
    - billing_period_end: Date, string="Billing Period End"

    Computed fields:
    - amount_untaxed: Float, compute='_compute_amounts', store=True, digits=(12, 2), string="Untaxed Amount", tracking=True
    - amount_tax: Float, compute='_compute_amounts', store=True, digits=(12, 2), string="Tax Amount"
    - amount_total: Float, compute='_compute_amounts', store=True, digits=(12, 2), string="Total Amount", tracking=True
    - amount_paid: Float, compute='_compute_payment_amounts', store=True, digits=(12, 2), string="Amount Paid"
    - amount_due: Float, compute='_compute_payment_amounts', store=True, digits=(12, 2), string="Amount Due"
    - payment_count: Integer, compute='_compute_payment_amounts', store=True, string="Payment Count"

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
            payments = invoice.payment_ids
            invoice.amount_paid = sum(payments.mapped('amount'))
            invoice.amount_due = invoice.amount_total - invoice.amount_paid
            invoice.payment_count = len(payments)

    ### State Machine Actions ###

    def action_confirm(self):
        """Confirm a draft invoice."""
        for invoice in self:
            if invoice.state != 'draft':
                raise UserError(_("Only draft invoices can be confirmed."))
            if not invoice.invoice_line_ids:
                raise UserError(_("Cannot confirm an invoice without lines."))
            invoice.state = 'confirmed'
            invoice.message_post(body=_("Invoice confirmed."))

    def action_cancel(self):
        """Cancel an invoice. Only draft or confirmed invoices can be cancelled."""
        for invoice in self:
            if invoice.state not in ('draft', 'confirmed'):
                raise UserError(_("Only draft or confirmed invoices can be cancelled."))
            if invoice.payment_ids:
                raise UserError(_("Cannot cancel an invoice with existing payments. Remove payments first."))
            invoice.state = 'cancelled'
            invoice.message_post(body=_("Invoice cancelled."))

    def action_set_to_draft(self):
        """Reset a cancelled invoice to draft."""
        for invoice in self:
            if invoice.state != 'cancelled':
                raise UserError(_("Only cancelled invoices can be reset to draft."))
            invoice.state = 'draft'

    def action_register_payment(self):
        """Placeholder: open payment wizard or create a payment record.
        Actual payment creation is done via the payment model."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'subscription.payment',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_invoice_id': self.id,
                'default_amount': self.amount_due,
                'default_payment_date': fields.Date.today(),
            },
        }

    def _check_mark_paid(self):
        """Check if the invoice is fully paid and update state accordingly."""
        for invoice in self:
            if invoice.state == 'confirmed' and invoice.amount_due <= 0:
                invoice.state = 'paid'
                invoice.message_post(body=_("Invoice fully paid."))

    ### CRUD Overrides ###

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('subscription.invoice') or 'New'
        return super().create(vals_list)

    @api.constrains('due_date', 'invoice_date')
    def _check_due_date(self):
        for invoice in self:
            if invoice.due_date and invoice.invoice_date and invoice.due_date < invoice.invoice_date:
                raise ValidationError(_("Due date cannot be before the invoice date."))

    SQL constraints:
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Invoice number must be unique!'),
    ]

Also update models/__init__.py to add:
    from . import invoice

Use Odoo 18 conventions. Include mail.thread and mail.activity.mixin for chatter support. Use tracking=True on key fields. Use _() for all user-facing strings.
```

## Expected Output

```
subscription_management/
├── models/
│   ├── __init__.py  (updated: from . import invoice)
│   └── invoice.py
```

## Verification

1. Check Python syntax: `python -c "import ast; ast.parse(open('models/invoice.py').read()); print('OK')"`
2. Verify all 4 states: draft, confirmed, paid, cancelled
3. Verify `action_register_payment` returns an action dict
4. Verify `_check_mark_paid` checks amount_due <= 0
5. Verify sequence generation in `create` method
6. Verify `_compute_payment_amounts` computes paid/due correctly
7. Verify `models/__init__.py` includes `invoice`
