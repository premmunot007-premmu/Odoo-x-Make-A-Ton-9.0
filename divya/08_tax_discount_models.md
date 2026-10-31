# Tax & Discount Models

## Context
Admin creates tax rules (percentage/fixed) and discount rules (fixed/%, with min purchase/quantity, date range, usage limits, applies to products or whole subscriptions).

## Prompt for Claude Code

```
In the Odoo 18 module "subscription_management", create Tax and Discount Rule models.

Create `models/tax.py`:

class SubscriptionTax(models.Model):
    _name = 'subscription.tax'
    _description = 'Tax Rule'

    Fields:
    - name: Char, required (e.g., "GST 18%", "Service Tax 5%")
    - tax_type: Selection [('percentage','Percentage'), ('fixed','Fixed Amount')], required, default='percentage'
    - amount: Float, required, digits=(10,2), help="Percentage value or fixed amount"
    - is_active: Boolean, default=True
    - description: Text

    def compute_tax(self, base_amount):
        """Compute tax on given base amount"""
        self.ensure_one()
        if self.tax_type == 'percentage':
            return base_amount * (self.amount / 100.0)
        return self.amount

    def name_get(self):
        result = []
        for tax in self:
            if tax.tax_type == 'percentage':
                result.append((tax.id, f"{tax.name} ({tax.amount}%)"))
            else:
                result.append((tax.id, f"{tax.name} (₹{tax.amount})"))
        return result


Create `models/discount.py`:

class SubscriptionDiscountRule(models.Model):
    _name = 'subscription.discount.rule'
    _description = 'Discount Rule'

    Fields:
    - name: Char, required
    - discount_type: Selection [('fixed','Fixed Amount'), ('percentage','Percentage')], required, default='percentage'
    - amount: Float, required, help="Discount amount or percentage"
    - min_purchase: Float, string="Minimum Purchase Amount", help="Minimum order value to qualify"
    - min_quantity: Integer, string="Minimum Quantity", help="Minimum quantity to qualify"
    - date_start: Date, string="Valid From"
    - date_end: Date, string="Valid Until"
    - max_usage: Integer, string="Maximum Uses", default=0, help="0 = unlimited"
    - current_usage: Integer, string="Times Used", default=0, readonly=True
    - product_ids: Many2many('subscription.product', string="Applicable Products")
    - apply_on: Selection [('product','Specific Products'), ('subscription','Entire Subscription')], required, default='product'
    - is_active: Boolean, compute='_compute_is_active', store=True, string="Active"
    - description: Text

    @api.depends('date_start', 'date_end', 'max_usage', 'current_usage')
    def _compute_is_active(self):
        today = fields.Date.today()
        for rec in self:
            date_ok = True
            if rec.date_start and rec.date_start > today:
                date_ok = False
            if rec.date_end and rec.date_end < today:
                date_ok = False
            usage_ok = rec.max_usage == 0 or rec.current_usage < rec.max_usage
            rec.is_active = date_ok and usage_ok

Update models/__init__.py to import tax and discount.
```

## Expected Output
- `models/tax.py`
- `models/discount.py`

## Verification
- Create tax rule "GST 18%", test compute_tax(1000) returns 180
- Create discount rule, verify is_active computation
