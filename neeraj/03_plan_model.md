# 03 — Subscription Plan Model

## Context
The Plan model defines how a subscription is billed and what rules apply. Plans have a billing frequency (daily, weekly, monthly, yearly), availability date ranges, and behavioral flags (auto-close, allow pause, allow early close, allow renew). Each plan has **plan lines** that define which products are included by default with default quantities and prices. When a subscription is created from a plan, these plan lines populate the subscription lines.

This file depends on: `01_module_scaffold.md`, `02_product_model.md`.

## Prompt for Antigravity

```
Create an Odoo 18 model file for subscription plans in the subscription_management module.

Create file: E:\odoo18\custom_addons\subscription_management\models\plan.py

### Model 1: subscription.plan

This model defines a subscription plan with billing rules and product defaults.

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SubscriptionPlan(models.Model):
    _name = 'subscription.plan'
    _description = 'Subscription Plan'
    _order = 'name asc'

    Fields:
    - name: Char, required=True, string="Plan Name"
    - billing_frequency: Selection with choices [('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')], required=True, default='monthly', string="Billing Frequency"
    - min_quantity: Integer, string="Minimum Quantity", default=1, help="Minimum number of units for this plan"
    - date_start: Date, string="Available From", help="Date from which this plan is available for subscription"
    - date_end: Date, string="Available Until", help="Date until which this plan is available for subscription"
    - auto_close: Boolean, string="Auto Close on Expiry", default=False, help="Automatically close the subscription when it expires"
    - allow_early_close: Boolean, string="Allow Early Closure", default=True, help="Allow customers to close the subscription before expiry"
    - allow_pause: Boolean, string="Allow Pause", default=False, help="Allow customers to pause the subscription temporarily"
    - allow_renew: Boolean, string="Allow Renewal", default=True, help="Allow customers to renew the subscription after expiry"
    - description: Html, string="Description", help="Detailed description of the plan"
    - is_active: Boolean, string="Active", default=True
    - plan_line_ids: One2many to 'subscription.plan.line', inverse field 'plan_id', string="Plan Lines"

    Computed fields:
    - product_count: Integer, compute='_compute_product_count', string="Products"
    - is_available: Boolean, compute='_compute_is_available', string="Currently Available", store=True

    @api.depends('date_start', 'date_end', 'is_active')
    def _compute_is_available(self):
        today = fields.Date.today()
        for record in self:
            available = record.is_active
            if record.date_start and today < record.date_start:
                available = False
            if record.date_end and today > record.date_end:
                available = False
            record.is_available = available

    @api.depends('plan_line_ids')
    def _compute_product_count(self):
        for record in self:
            record.product_count = len(record.plan_line_ids)

    Python constraint:
    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_end and record.date_end < record.date_start:
                raise ValidationError("The end date must be after the start date.")

    SQL constraints:
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Plan name must be unique!'),
        ('min_quantity_positive', 'CHECK(min_quantity >= 0)', 'Minimum quantity must be positive!'),
    ]

### Model 2: subscription.plan.line

This model defines default products included in a plan.

class SubscriptionPlanLine(models.Model):
    _name = 'subscription.plan.line'
    _description = 'Plan Line'
    _order = 'sequence, id'

    Fields:
    - plan_id: Many2one to 'subscription.plan', required=True, ondelete='cascade', string="Plan"
    - product_id: Many2one to 'subscription.product', required=True, ondelete='restrict', string="Product"
    - sequence: Integer, string="Sequence", default=10
    - default_qty: Float, string="Default Quantity", default=1.0, digits=(12, 2)
    - default_price: Float, string="Default Unit Price", digits=(12, 2), help="If set, overrides the product's sales price. If 0, uses product's sales price."

    Computed fields:
    - display_price: Float, compute='_compute_display_price', string="Display Price", digits=(12, 2)

    @api.depends('default_price', 'product_id.sales_price')
    def _compute_display_price(self):
        for record in self:
            record.display_price = record.default_price if record.default_price > 0 else record.product_id.sales_price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.default_price = self.product_id.sales_price

Also update models/__init__.py to add:
    from . import plan

Use Odoo 18 conventions. Use proper field attributes, depends decorators, and constraint patterns.
```

## Expected Output

```
subscription_management/
├── models/
│   ├── __init__.py  (updated: from . import plan)
│   └── plan.py
```

## Verification

1. Check Python syntax: `python -c "import ast; ast.parse(open('models/plan.py').read()); print('OK')"`
2. Verify the model has all 12 fields on `subscription.plan`
3. Verify `subscription.plan.line` has the `_onchange_product_id` method
4. Confirm date constraint validation exists
5. Verify `models/__init__.py` now imports both `product` and `plan`
