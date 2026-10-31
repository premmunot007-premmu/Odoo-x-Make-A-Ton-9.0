# Payment Reconciliation — Paid/Outstanding Tracking

## Context
When a payment is recorded, the system must update invoice amounts and state. Track outstanding invoices for chasing overdue payments.

## Prompt for Antigravity

```
In the Odoo 18 module "subscription_management", enhance payment reconciliation.

In `models/payment.py`, update create method:

@api.model_create_multi
def create(self, vals_list):
    records = super().create(vals_list)
    for payment in records:
        invoice = payment.invoice_id
        # Recompute payment status
        total_paid = sum(invoice.payment_ids.mapped('amount'))
        if total_paid >= invoice.amount_total:
            invoice.write({'state': 'paid'})
            invoice.message_post(body=f"Invoice fully paid. Payment of ₹{payment.amount} received via {payment.payment_method}.")
        else:
            invoice.message_post(body=f"Partial payment of ₹{payment.amount} received via {payment.payment_method}. Outstanding: ₹{invoice.amount_due}")
    return records

@api.constrains('amount', 'invoice_id')
def _check_overpayment(self):
    for rec in self:
        if rec.amount > rec.invoice_id.amount_due + rec.amount:  # before this payment
            raise ValidationError("Payment amount exceeds the outstanding balance!")

Add to Invoice model a method to get outstanding invoices for a customer:

@api.model
def get_outstanding_invoices(self, partner_id=None):
    """Get all outstanding (unpaid/partial) invoices, optionally for a specific customer"""
    domain = [('state', '=', 'confirmed'), ('payment_status', 'in', ['not_paid', 'partial'])]
    if partner_id:
        domain.append(('partner_id', '=', partner_id))
    return self.search(domain, order='due_date asc')

@api.model
def get_overdue_invoices(self):
    """Get all overdue invoices"""
    today = fields.Date.today()
    return self.search([
        ('state', '=', 'confirmed'),
        ('payment_status', 'in', ['not_paid', 'partial']),
        ('due_date', '<', today),
    ], order='due_date asc')
```

## Expected Output
- Updated `models/payment.py`
- Updated `models/invoice.py`

## Verification
- Record payment → invoice state should change when fully paid
- Check outstanding invoices method returns correct results
