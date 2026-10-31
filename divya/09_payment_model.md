# Payment Model

## Context
Payments are recorded against invoices with method, amount, date, and note. Track paid vs outstanding. When fully paid, invoice moves to "paid" state.

## Prompt for Claude Code

```
In the Odoo 18 module "subscription_management", create the Payment model.

Create `models/payment.py`:

class SubscriptionPayment(models.Model):
    _name = 'subscription.payment'
    _description = 'Payment'
    _inherit = ['mail.thread']
    _order = 'payment_date desc'

    Fields:
    - name: Char, compute='_compute_name', store=True
    - invoice_id: Many2one('subscription.invoice', required, string="Invoice", tracked=True)
    - partner_id: Many2one('res.partner', related='invoice_id.partner_id', store=True, string="Customer")
    - payment_method: Selection [('bank_transfer','Bank Transfer'), ('credit_card','Credit Card'), ('upi','UPI'), ('cash','Cash'), ('cheque','Cheque')], required, default='bank_transfer', string="Payment Method"
    - amount: Float, required, digits=(10,2), string="Amount Paid"
    - payment_date: Date, required, default=fields.Date.today
    - note: Text, string="Payment Note"
    - reference: Char, string="Transaction Reference"
    - company_id: Many2one('res.company', default=lambda self: self.env.company)
    - currency_id: Many2one('res.currency', related='company_id.currency_id')

    @api.depends('invoice_id', 'payment_date')
    def _compute_name(self):
        for rec in self:
            rec.name = f"PAY/{rec.invoice_id.name or ''}/{rec.payment_date or ''}"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            # Check if invoice is fully paid
            if rec.invoice_id.amount_due <= 0:
                rec.invoice_id.write({'state': 'paid'})
        return records

    @api.constrains('amount')
    def _check_amount(self):
        for rec in self:
            if rec.amount <= 0:
                raise ValidationError("Payment amount must be positive.")

    _sql_constraints = [
        ('positive_amount', 'CHECK(amount > 0)', 'Payment amount must be positive!'),
    ]

Update models/__init__.py to import payment.
```

## Expected Output
- `models/payment.py`

## Verification
- Create payment against invoice, verify amount_due reduces and state changes
