# Automated Unit Tests: Subscription Lifecycle & State Machine

## Context
Unit tests validating subscription transitions (Draft → Quotation → Confirmed → Active → Paused → Closed), sequence numbering, and date constraints.

## Prompt for Antigravity

```markdown
In our Odoo 18 module `subscription_management`, create `tests/test_subscription.py`:

```python
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError
from odoo import fields
from dateutil.relativedelta import relativedelta

class TestSubscriptionLifecycle(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Partner = self.env['res.partner']
        self.Plan = self.env['subscription.plan']
        self.Product = self.env['subscription.product']
        self.Subscription = self.env['subscription.subscription']

        self.customer = self.Partner.create({'name': 'Test Client Corp', 'customer_rank': 1})
        self.plan = self.Plan.create({
            'name': 'Monthly Pro Plan',
            'billing_frequency': 'monthly',
            'allow_pause': True,
            'allow_renew': True,
            'allow_early_close': True,
        })
        self.product = self.Product.create({
            'name': 'Cloud Platform',
            'sales_price': 500.0,
        })

    def test_01_lifecycle_flow(self):
        """Test complete state machine flow"""
        sub = self.Subscription.create({
            'partner_id': self.customer.id,
            'plan_id': self.plan.id,
            'start_date': fields.Date.today(),
            'subscription_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 2,
                'unit_price': 500.0,
            })]
        })
        self.assertEqual(sub.state, 'draft')
        self.assertEqual(sub.amount_total, 1000.0)

        # Quotation
        sub.action_send_quotation()
        self.assertEqual(sub.state, 'quotation')

        # Confirm
        sub.action_confirm()
        self.assertEqual(sub.state, 'confirmed')

        # Activate
        sub.action_activate()
        self.assertEqual(sub.state, 'active')

        # Pause
        sub.action_pause()
        self.assertEqual(sub.state, 'paused')

        # Resume
        sub.action_activate()
        self.assertEqual(sub.state, 'active')

        # Close
        sub.action_close()
        self.assertEqual(sub.state, 'closed')

    def test_02_pause_disallowed(self):
        """Test pause restriction if plan denies it"""
        strict_plan = self.Plan.create({
            'name': 'Strict Annual',
            'billing_frequency': 'yearly',
            'allow_pause': False,
        })
        sub = self.Subscription.create({
            'partner_id': self.customer.id,
            'plan_id': strict_plan.id,
        })
        sub.action_send_quotation()
        sub.action_confirm()
        sub.action_activate()
        with self.assertRaises(UserError):
            sub.action_pause()
```
```

## Expected Output
- `tests/test_subscription.py`

## Verification
Run:
```bash
python odoo-bin -c odoo.conf -u subscription_management --test-enable --test-tags=.test_subscription --stop-after-init
```
