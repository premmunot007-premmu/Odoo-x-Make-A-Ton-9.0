# 05 — Subscription Line Model

## Context
Subscription lines are the individual product entries within a subscription. Each line links a product (and optionally a variant) to the subscription with quantity, unit price, taxes, and discounts. The subtotal and total (with tax) are computed automatically. These lines are used to generate invoice lines when billing occurs.

This file depends on: `01_module_scaffold.md`, `02_product_model.md`, `04_subscription_model.md`.

## Prompt for Antigravity

```
Create an Odoo 18 model file for subscription lines in the subscription_management module.

Create file: E:\odoo18\custom_addons\subscription_management\models\subscription_line.py

### Model: subscription.subscription.line

This model represents individual product lines within a subscription.

from odoo import models, fields, api

class SubscriptionLine(models.Model):
    _name = 'subscription.subscription.line'
    _description = 'Subscription Line'
    _order = 'sequence, id'

    Fields:
    - subscription_id: Many2one to 'subscription.subscription', required=True, ondelete='cascade', string="Subscription"
    - product_id: Many2one to 'subscription.product', required=True, ondelete='restrict', string="Product"
    - variant_id: Many2one to 'subscription.product.variant', string="Variant", domain="[('product_id', '=', product_id)]", help="Optional product variant that adds extra price"
    - sequence: Integer, string="Sequence", default=10
    - quantity: Float, required=True, default=1.0, digits=(12, 2), string="Quantity"
    - unit_price: Float, required=True, digits=(12, 2), string="Unit Price"
    - tax_ids: Many2many to 'subscription.tax', relation='subscription_line_tax_rel', column1='line_id', column2='tax_id', string="Taxes"
    - discount: Float, string="Discount (%)", digits=(5, 2), default=0.0

    Computed fields:
    - subtotal: Float, compute='_compute_amounts', store=True, digits=(12, 2), string="Subtotal"
    - tax_amount: Float, compute='_compute_amounts', store=True, digits=(12, 2), string="Tax Amount"
    - total: Float, compute='_compute_amounts', store=True, digits=(12, 2), string="Total"
    - price_with_variant: Float, compute='_compute_price_with_variant', digits=(12, 2), string="Price (with variant)"

    @api.depends('unit_price', 'variant_id.price_extra')
    def _compute_price_with_variant(self):
        for line in self:
            extra = line.variant_id.price_extra if line.variant_id else 0.0
            line.price_with_variant = line.unit_price + extra

    @api.depends('quantity', 'unit_price', 'discount', 'tax_ids', 'variant_id.price_extra')
    def _compute_amounts(self):
        for line in self:
            # Base price includes variant extra
            base_price = line.unit_price + (line.variant_id.price_extra if line.variant_id else 0.0)
            
            # Apply discount
            if line.discount:
                base_price = base_price * (1 - (line.discount / 100.0))
            
            # Subtotal = quantity * discounted price
            line.subtotal = line.quantity * base_price
            
            # Calculate taxes
            tax_amount = 0.0
            for tax in line.tax_ids:
                if tax.tax_type == 'percentage':
                    tax_amount += line.subtotal * (tax.amount / 100.0)
                elif tax.tax_type == 'fixed':
                    tax_amount += tax.amount * line.quantity
            
            line.tax_amount = tax_amount
            line.total = line.subtotal + line.tax_amount

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """When product changes, set unit_price from product's sales_price and clear variant."""
        if self.product_id:
            self.unit_price = self.product_id.sales_price
            self.variant_id = False

    @api.onchange('variant_id')
    def _onchange_variant_id(self):
        """Informational: no field change needed, but recomputation triggers automatically."""
        pass

    SQL constraints:
    _sql_constraints = [
        ('quantity_positive', 'CHECK(quantity > 0)', 'Quantity must be greater than zero!'),
        ('unit_price_positive', 'CHECK(unit_price >= 0)', 'Unit price must be positive!'),
        ('discount_range', 'CHECK(discount >= 0 AND discount <= 100)', 'Discount must be between 0 and 100!'),
    ]

Also update models/__init__.py to add:
    from . import subscription_line

Use Odoo 18 conventions. Ensure computed fields have proper @api.depends decorators and store=True for fields used in parent computations.
```

## Expected Output

```
subscription_management/
├── models/
│   ├── __init__.py  (updated: from . import subscription_line)
│   └── subscription_line.py
```

## Verification

1. Check Python syntax: `python -c "import ast; ast.parse(open('models/subscription_line.py').read()); print('OK')"`
2. Verify `_compute_amounts` handles both percentage and fixed taxes
3. Verify variant price_extra is added to unit_price in computation
4. Verify discount is applied correctly (as percentage)
5. Verify SQL constraints for quantity, price, and discount range
6. Verify `models/__init__.py` includes `subscription_line`
