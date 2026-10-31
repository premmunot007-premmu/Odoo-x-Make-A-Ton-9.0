# 02 — Product Model & Variants

## Context
The product model is the foundational data entity. Brightloop Software sells software products, add-ons, and services on subscription. Each product can have **variants** (e.g., "Enterprise Brand Package" adds ₹560 to the base price). This file creates two models: `subscription.product` (the main product) and `subscription.product.variant` (variant options that modify the price).

This file depends on: `01_module_scaffold.md` (module must exist).

## Prompt for Antigravity

```
Create an Odoo 18 model file for product management in the subscription_management module.

Create file: E:\odoo18\custom_addons\subscription_management\models\product.py

### Model 1: subscription.product

This model represents a product that can be sold on subscription.

from odoo import models, fields, api

class SubscriptionProduct(models.Model):
    _name = 'subscription.product'
    _description = 'Subscription Product'
    _order = 'name asc'

    Fields:
    - name: Char, required=True, string="Product Name"
    - product_type: Selection with choices [('software', 'Software'), ('addon', 'Add-on'), ('service', 'Service')], required=True, default='software', string="Product Type"
    - sales_price: Float, required=True, digits=(12, 2), string="Sales Price", default=0.0
    - cost_price: Float, digits=(12, 2), string="Cost Price", default=0.0
    - notes: Text, string="Internal Notes"
    - image: Binary, string="Product Image", attachment=True
    - is_active: Boolean, string="Active", default=True
    - variant_ids: One2many to 'subscription.product.variant', inverse field 'product_id', string="Variants"
    - currency_symbol: Char, default='₹', string="Currency"

    Add a computed field:
    - variant_count: Integer, compute='_compute_variant_count', string="Variant Count"

    Method _compute_variant_count:
        for record in self:
            record.variant_count = len(record.variant_ids)

    Add _sql_constraints:
        ('name_unique', 'UNIQUE(name)', 'Product name must be unique!')
        ('sales_price_positive', 'CHECK(sales_price >= 0)', 'Sales price must be positive!')
        ('cost_price_positive', 'CHECK(cost_price >= 0)', 'Cost price must be positive!')

    Add a name_get method (Odoo 18 uses _compute_display_name):
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.name} ({record.get_selection_label('product_type', record.product_type)})"

    Wait — in Odoo 18, use the simpler approach. Just set _rec_name = 'name' and let Odoo handle display_name automatically. Skip the custom _compute_display_name for now.

### Model 2: subscription.product.variant

This model represents variant options for a product. For example, a "Brand Package" variant that adds ₹560 to the base product price.

class SubscriptionProductVariant(models.Model):
    _name = 'subscription.product.variant'
    _description = 'Product Variant'
    _order = 'product_id, variant_name'

    Fields:
    - product_id: Many2one to 'subscription.product', required=True, ondelete='cascade', string="Product"
    - variant_name: Char, required=True, string="Variant Name" (e.g., "Brand Package", "Premium Support")
    - variant_value: Char, string="Variant Value" (e.g., "Enterprise", "Gold")
    - price_extra: Float, digits=(12, 2), string="Extra Price", default=0.0, help="Additional price added to the base product price when this variant is selected"

    Add _sql_constraints:
        ('price_extra_positive', 'CHECK(price_extra >= 0)', 'Extra price must be positive or zero!')

    Add a computed field:
    - final_price: Float, compute='_compute_final_price', string="Final Price", store=True

    @api.depends('product_id.sales_price', 'price_extra')
    def _compute_final_price(self):
        for record in self:
            record.final_price = record.product_id.sales_price + record.price_extra

Also update models/__init__.py to import this file:
    from . import product

Use standard Odoo 18 conventions:
- Use proper field types and attributes
- Use _sql_constraints for database-level validation
- Use @api.depends for computed fields
- All monetary fields should use digits=(12, 2)
- Include proper docstrings
```

## Expected Output

```
subscription_management/
├── models/
│   ├── __init__.py  (updated to import product)
│   └── product.py
```

## Verification

1. Check Python syntax: `python -c "import ast; ast.parse(open('models/product.py').read()); print('OK')"`
2. Verify `models/__init__.py` contains `from . import product`
3. The model should have all required fields with correct types
4. SQL constraints should be present for uniqueness and positive prices
