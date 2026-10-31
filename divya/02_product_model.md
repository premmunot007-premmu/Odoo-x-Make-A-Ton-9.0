# Product Model — Products & Variants

## Context
Brightloop sells software products on subscription. Products have variants (e.g., brand variants where choosing "Odoo" brand adds ₹560 to price). This is the first business model.

## Prompt for Claude Code

```
In the Odoo 18 module "subscription_management", create the Product and Product Variant models.

Create `models/product.py`:

class SubscriptionProduct(models.Model):
    _name = 'subscription.product'
    _description = 'Subscription Product'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    Fields:
    - name: Char, required, tracked=True, string="Product Name"
    - product_type: Selection [('software', 'Software'), ('addon', 'Add-on'), ('service', 'Service')], required, default='software'
    - sales_price: Float, string="Sales Price", required, default=0.0, digits=(10,2)
    - cost_price: Float, string="Cost Price", digits=(10,2)
    - notes: Html, string="Description"
    - image: Binary, string="Product Image", attachment=True
    - is_active: Boolean, default=True, string="Active"
    - variant_ids: One2many to 'subscription.product.variant', inverse='product_id'
    - variant_count: Integer, compute='_compute_variant_count'

    @api.depends('variant_ids')
    def _compute_variant_count(self):
        for rec in self:
            rec.variant_count = len(rec.variant_ids)

    def name_get(self):
        return [(rec.id, rec.name) for rec in self]

    _sql_constraints = [
        ('positive_sales_price', 'CHECK(sales_price >= 0)', 'Sales price must be positive!'),
        ('positive_cost_price', 'CHECK(cost_price >= 0)', 'Cost price must be positive!'),
    ]


class SubscriptionProductVariant(models.Model):
    _name = 'subscription.product.variant'
    _description = 'Product Variant'

    Fields:
    - product_id: Many2one to 'subscription.product', required, ondelete='cascade'
    - variant_name: Char, required, string="Variant Attribute" (e.g., "Brand")
    - variant_value: Char, required, string="Variant Value" (e.g., "Odoo")
    - price_extra: Float, string="Extra Price", default=0.0, digits=(10,2), help="Additional price for this variant (e.g., 560 for Odoo brand)"

    _sql_constraints = [
        ('unique_variant', 'UNIQUE(product_id, variant_name, variant_value)', 'Variant combination must be unique per product!'),
    ]

Update `models/__init__.py` to import product.

Follow Odoo 18 conventions: use proper decorators, api.model, api.depends. Include docstrings.
```

## Expected Output
- `models/product.py`
- Updated `models/__init__.py`

## Verification
```bash
python odoo-bin -c odoo.conf -u subscription_management
# Check: Settings > Technical > Database Structure > Models > search "subscription.product"
```
