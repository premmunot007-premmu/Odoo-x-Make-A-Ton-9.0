# Automated Unit Tests: Invoicing, Duplicate Prevention & Payment Reconciliation

## Context
Unit tests verifying that invoices are generated accurately from active subscriptions, duplicate billing is prevented, and payments reconcile invoices to Paid state.

## Prompt for Antigravity

```markdown
In our Odoo 18 module `subscription_management`, create `tests/test_invoice.py`:

```python
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo import fields

class TestInvoiceAndPayment(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Partner = self.env['res.partner']
        self.Plan = self.env['subscription.plan']
        self.Product = self.env['subscription.product']
        self.Tax = self.env['subscription.tax']
        self.Subscription = self.env['subscription.subscription']
        self.Payment = self.env['subscription.payment']

        self.customer = self.Partner.create({'name': 'Billing Corp', 'customer_rank': 1})
        self.plan = self.Plan.create({'name': 'Monthly Plan', 'billing_frequency': 'monthly'})
        self.product = self.Product.create({'name': 'Base App', 'sales_price': 1000.0})
        self.tax_18 = self.Tax.create({'name': 'GST 18%', 'tax_type': 'percentage', 'amount': 18.0})

        self.sub = self.Subscription.create({
            'partner_id': self.customer.id,
            'plan_id': self.plan.id,
            'state': 'active',
            'subscription_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1,
                'unit_price': 1000.0,
                'tax_ids': [(6, 0, [self.tax_18.id])],
            })]
        })

    def test_01_invoice_generation_and_tax(self):
        """Test invoice creation with 18% tax calculation"""
        res = self.sub.action_create_invoice()
        inv_id = res['res_id']
        invoice = self.env['subscription.invoice'].browse(inv_id)

        self.assertEqual(invoice.state, 'draft')
        self.assertEqual(invoice.amount_untaxed, 1000.0)
        self.assertEqual(invoice.amount_tax, 180.0)
        self.assertEqual(invoice.amount_total, 1180.0)
        self.assertEqual(invoice.amount_due, 1180.0)

    def test_02_duplicate_billing_prevention(self):
        """Test that calling action_create_invoice twice in same period fails"""
        self.sub.action_create_invoice()
        with self.assertRaises(UserError):
            self.sub.action_create_invoice()

    def test_03_payment_reconciliation(self):
        """Test registering payment transitions invoice to paid"""
        res = self.sub.action_create_invoice()
        invoice = self.env['subscription.invoice'].browse(res['res_id'])
        invoice.action_confirm()

        # Partial payment
        pay1 = self.Payment.create({
            'invoice_id': invoice.id,
            'amount': 500.0,
            'payment_method': 'upi',
        })
        self.assertEqual(invoice.payment_status, 'partial')
        self.assertEqual(invoice.amount_due, 680.0)

        # Full payment settlement
        pay2 = self.Payment.create({
            'invoice_id': invoice.id,
            'amount': 680.0,
            'payment_method': 'bank_transfer',
        })
        self.assertEqual(invoice.payment_status, 'paid')
        self.assertEqual(invoice.state, 'paid')
        self.assertEqual(invoice.amount_due, 0.0)
```
```

## Expected Output
- `tests/test_invoice.py`

## Verification
Run test runner:
```bash
python odoo-bin -c odoo.conf -u subscription_management --test-enable --test-tags=.test_invoice --stop-after-init
```
