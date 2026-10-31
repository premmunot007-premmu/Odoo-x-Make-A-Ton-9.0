# 06 — Quotation Template Model

## Context
Quotation templates are pre-built configurations that bundle a plan with specific product lines, quantities, and prices. When a user creates a subscription, they can select a template to auto-fill the plan and subscription lines — saving time for repetitive subscription setups. For example, a "Starter Package" template might include the base software product + a support add-on at preset prices.

This file depends on: `01_module_scaffold.md`, `02_product_model.md`, `03_plan_model.md`.

## Prompt for Antigravity

```
Create an Odoo 18 model file for quotation templates in the subscription_management module.

Create file: E:\odoo18\custom_addons\subscription_management\models\quotation_template.py

### Model 1: subscription.quotation.template

This model represents pre-built subscription templates for quick setup.

from odoo import models, fields, api

class SubscriptionQuotationTemplate(models.Model):
    _name = 'subscription.quotation.template'
    _description = 'Subscription Quotation Template'
    _order = 'name asc'

    Fields:
    - name: Char, required=True, string="Template Name"
    - plan_id: Many2one to 'subscription.plan', required=True, ondelete='restrict', string="Subscription Plan"
    - validity_days: Integer, string="Quotation Validity (Days)", default=30, help="Number of days the quotation is valid"
    - description: Html, string="Description"
    - is_active: Boolean, string="Active", default=True
    - template_line_ids: One2many to 'subscription.quotation.template.line', inverse field 'template_id', string="Template Lines"

    Computed fields:
    - line_count: Integer, compute='_compute_line_count', string="Line Count"
    - total_amount: Float, compute='_compute_total_amount', digits=(12, 2), string="Total Amount"

    @api.depends('template_line_ids')
    def _compute_line_count(self):
        for record in self:
            record.line_count = len(record.template_line_ids)

    @api.depends('template_line_ids.quantity', 'template_line_ids.unit_price')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(
                line.quantity * line.unit_price for line in record.template_line_ids
            )

    SQL constraints:
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Template name must be unique!'),
        ('validity_positive', 'CHECK(validity_days > 0)', 'Validity days must be positive!'),
    ]

### Model 2: subscription.quotation.template.line

class SubscriptionQuotationTemplateLine(models.Model):
    _name = 'subscription.quotation.template.line'
    _description = 'Quotation Template Line'
    _order = 'sequence, id'

    Fields:
    - template_id: Many2one to 'subscription.quotation.template', required=True, ondelete='cascade', string="Template"
    - product_id: Many2one to 'subscription.product', required=True, ondelete='restrict', string="Product"
    - sequence: Integer, string="Sequence", default=10
    - quantity: Float, required=True, default=1.0, digits=(12, 2), string="Quantity"
    - unit_price: Float, required=True, digits=(12, 2), string="Unit Price"

    Computed fields:
    - subtotal: Float, compute='_compute_subtotal', store=True, digits=(12, 2), string="Subtotal"

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.unit_price = self.product_id.sales_price

    SQL constraints:
    _sql_constraints = [
        ('quantity_positive', 'CHECK(quantity > 0)', 'Quantity must be greater than zero!'),
        ('unit_price_positive', 'CHECK(unit_price >= 0)', 'Unit price must be positive!'),
    ]

Also update models/__init__.py to add:
    from . import quotation_template

Use Odoo 18 conventions throughout.
```

## Expected Output

```
subscription_management/
├── models/
│   ├── __init__.py  (updated: from . import quotation_template)
│   └── quotation_template.py
```

## Verification

1. Check Python syntax: `python -c "import ast; ast.parse(open('models/quotation_template.py').read()); print('OK')"`
2. Verify both models exist: `subscription.quotation.template` and `subscription.quotation.template.line`
3. Verify `_onchange_product_id` sets unit_price from product
4. Verify `_compute_total_amount` sums all lines
5. Verify `models/__init__.py` includes `quotation_template`
