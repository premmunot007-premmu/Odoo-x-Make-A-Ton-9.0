# Invoice Model — Auto-Generated Invoices

## Context
Invoices are auto-created from subscriptions on billing day. Each invoice has a unique sequence, customer details, line items with taxes, and states: Draft→Confirmed→Paid→Cancelled. No duplicate billing.

## Prompt for Claude Code

```
In the Odoo 18 module "subscription_management", create the Invoice and Invoice Line models.

Create `models/invoice.py`:

class SubscriptionInvoice(models.Model):
    _name = 'subscription.invoice'
    _description = 'Subscription Invoice'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'invoice_date desc, name desc'

    Fields:
    - name: Char, readonly=True, copy=False, default='New', string="Invoice Number"
    - subscription_id: Many2one('subscription.subscription', string="Subscription", tracked=True)
    - partner_id: Many2one('res.partner', required, string="Customer", tracked=True)
    - invoice_date: Date, required, default=fields.Date.today, string="Invoice Date"
    - due_date: Date, string="Due Date"
    - state: Selection [('draft','Draft'), ('confirmed','Confirmed'), ('paid','Paid'), ('cancelled','Cancelled')], default='draft', tracked=True
    - invoice_line_ids: One2many('subscription.invoice.line', 'invoice_id')
    - payment_ids: One2many('subscription.payment', 'invoice_id')
    - amount_untaxed: Float, compute='_compute_amounts', store=True
    - amount_tax: Float, compute='_compute_amounts', store=True
    - amount_total: Float, compute='_compute_amounts', store=True
    - amount_paid: Float, compute='_compute_payment_status', store=True
    - amount_due: Float, compute='_compute_payment_status', store=True
    - payment_status: Selection [('not_paid','Not Paid'), ('partial','Partially Paid'), ('paid','Fully Paid')], compute='_compute_payment_status', store=True
    - is_overdue: Boolean, compute='_compute_is_overdue', store=True
    - company_id: Many2one('res.company', default=lambda self: self.env.company)
    - currency_id: Many2one('res.currency', related='company_id.currency_id')
    - note: Text

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('subscription.invoice') or 'New'
        return super().create(vals_list)

    @api.depends('invoice_line_ids.subtotal', 'invoice_line_ids.tax_amount')
    def _compute_amounts(self):
        for rec in self:
            rec.amount_untaxed = sum(rec.invoice_line_ids.mapped('subtotal'))
            rec.amount_tax = sum(rec.invoice_line_ids.mapped('tax_amount'))
            rec.amount_total = rec.amount_untaxed + rec.amount_tax

    @api.depends('payment_ids.amount', 'amount_total')
    def _compute_payment_status(self):
        for rec in self:
            rec.amount_paid = sum(rec.payment_ids.mapped('amount'))
            rec.amount_due = rec.amount_total - rec.amount_paid
            if rec.amount_paid <= 0:
                rec.payment_status = 'not_paid'
            elif rec.amount_paid < rec.amount_total:
                rec.payment_status = 'partial'
            else:
                rec.payment_status = 'paid'

    @api.depends('due_date', 'state')
    def _compute_is_overdue(self):
        today = fields.Date.today()
        for rec in self:
            rec.is_overdue = rec.due_date and rec.due_date < today and rec.state not in ('paid', 'cancelled')

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_mark_paid(self):
        self.write({'state': 'paid'})

    def _compute_access_url(self):
        super()._compute_access_url()
        for rec in self:
            rec.access_url = f'/my/invoices/{rec.id}'


class SubscriptionInvoiceLine(models.Model):
    _name = 'subscription.invoice.line'
    _description = 'Invoice Line'

    Fields:
    - invoice_id: Many2one('subscription.invoice', required, ondelete='cascade')
    - product_id: Many2one('subscription.product', required)
    - description: Char
    - quantity: Float, required, default=1.0
    - unit_price: Float, required, digits=(10,2)
    - tax_ids: Many2many('subscription.tax')
    - discount_amount: Float, default=0.0, string="Discount"
    - subtotal: Float, compute='_compute_amounts', store=True
    - tax_amount: Float, compute='_compute_amounts', store=True
    - total: Float, compute='_compute_amounts', store=True

    @api.depends('quantity', 'unit_price', 'discount_amount', 'tax_ids')
    def _compute_amounts(self):
        for line in self:
            subtotal = (line.quantity * line.unit_price) - line.discount_amount
            tax_amount = sum(tax.compute_tax(subtotal) for tax in line.tax_ids)
            line.subtotal = subtotal
            line.tax_amount = tax_amount
            line.total = subtotal + tax_amount

Update models/__init__.py.
```

## Expected Output
- `models/invoice.py` (both Invoice and InvoiceLine classes)

## Verification
- Create invoice manually, verify computed fields work
