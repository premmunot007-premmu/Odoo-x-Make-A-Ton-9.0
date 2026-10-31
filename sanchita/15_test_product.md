# Automated Unit Tests: Product & Variant Calculations

## Context
Automated unit tests to guarantee pricing integrity, positive value constraints, and brand extra fees.

## Prompt for Antigravity

```markdown
In our Odoo 18 module `subscription_management`, create `tests/test_product.py`:

```python
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestSubscriptionProduct(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Product = self.env['subscription.product']
        self.Variant = self.env['subscription.product.variant']

        self.prod_crm = self.Product.create({
            'name': 'Brightloop CRM Test',
            'product_type': 'software',
            'sales_price': 1000.0,
            'cost_price': 300.0,
        })

    def test_01_product_creation(self):
        """Test product fields and name_get"""
        self.assertEqual(self.prod_crm.name, 'Brightloop CRM Test')
        self.assertEqual(self.prod_crm.sales_price, 1000.0)
        self.assertEqual(self.prod_crm.variant_count, 0)

    def test_02_product_variant_price_extra(self):
        """Test adding Odoo brand variant with 560 extra fee"""
        var_odoo = self.Variant.create({
            'product_id': self.prod_crm.id,
            'variant_name': 'Brand',
            'variant_value': 'Odoo',
            'price_extra': 560.0,
        })
        self.assertEqual(self.prod_crm.variant_count, 1)
        self.assertEqual(var_odoo.price_extra, 560.0)

    def test_03_negative_price_constraint(self):
        """Test positive price constraint"""
        with self.assertRaises(Exception):
            self.Product.create({
                'name': 'Invalid Negative Price',
                'sales_price': -100.0,
            })
```

Also create `tests/__init__.py`:
```python
from . import test_product
from . import test_subscription
from . import test_invoice
from . import test_auth_discount
```
```

## Expected Output
- `tests/test_product.py`
- `tests/__init__.py`

## Verification
Run tests:
```bash
python odoo-bin -c odoo.conf -u subscription_management --test-enable --test-tags=subscription_management --stop-after-init
```
