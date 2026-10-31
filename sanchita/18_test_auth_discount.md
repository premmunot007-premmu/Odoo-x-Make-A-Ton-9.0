# Automated Unit Tests: Strong Passwords & Discount Rules

## Context
Unit tests verifying password strength regex rules (8+ chars, upper, lower, special character) and discount rule application (limits, percentage, min purchase).

## Prompt for Antigravity

```markdown
In our Odoo 18 module `subscription_management`, create `tests/test_auth_discount.py`:

```python
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo import fields

class TestAuthAndDiscount(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Users = self.env['res.users']
        self.Discount = self.env['subscription.discount.rule']
        self.Product = self.env['subscription.product']
        self.Subscription = self.env['subscription.subscription']
        self.Partner = self.env['res.partner']
        self.Plan = self.env['subscription.plan']

        self.test_prod = self.Product.create({'name': 'SaaS Suite', 'sales_price': 2000.0})

    def test_01_strong_password_policy(self):
        """Test password validation rules"""
        # Weak password (too short)
        with self.assertRaises(ValidationError):
            self.Users.create({
                'name': 'Shorty',
                'login': 'short@example.com',
                'password': 'Ab1!',
            })

        # Weak password (missing special character)
        with self.assertRaises(ValidationError):
            self.Users.create({
                'name': 'NoSpecial',
                'login': 'nospecial@example.com',
                'password': 'Password123',
            })

        # Strong valid password
        user = self.Users.create({
            'name': 'Valid User',
            'login': 'valid@example.com',
            'password': 'SecurePass@2026',
        })
        self.assertTrue(user.id)

    def test_02_discount_rule_calculation(self):
        """Test discount usage limit and percentage calculation"""
        disc = self.Discount.create({
            'name': 'Promo 10% Off',
            'discount_type': 'percentage',
            'amount': 10.0,
            'apply_on': 'subscription',
            'max_usage': 1,
            'current_usage': 0,
        })
        self.assertTrue(disc.is_active)

        # Check discount preview computation
        partner = self.Partner.create({'name': 'Promo Client', 'customer_rank': 1})
        plan = self.Plan.create({'name': 'Basic Plan', 'billing_frequency': 'monthly'})
        sub = self.Subscription.create({
            'partner_id': partner.id,
            'plan_id': plan.id,
            'state': 'active',
            'subscription_line_ids': [(0, 0, {
                'product_id': self.test_prod.id,
                'quantity': 1,
                'unit_price': 2000.0,
            })]
        })

        discount_val = sub._get_discount_amount(sub.subscription_line_ids[0])
        self.assertEqual(discount_val, 200.0) # 10% of 2000
        self.assertEqual(disc.current_usage, 1)
        self.assertFalse(disc.is_active) # Max usage reached
```
```

## Expected Output
- `tests/test_auth_discount.py`

## Verification
Run tests:
```bash
python odoo-bin -c odoo.conf -u subscription_management --test-enable --test-tags=.test_auth_discount --stop-after-init
```
