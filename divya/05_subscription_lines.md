# Subscription Line Model

## Context
Each subscription has line items: product, variant, quantity, unit price, taxes, discount, computed subtotal/total.

## Prompt for Claude Code

```
In the Odoo 18 module "subscription_management", create the Subscription Line model.

Create `models/subscription_line.py`:

class SubscriptionLine(models.Model):
    _name = 'subscription.subscription.line'
    _description = 'Subscription Line'

    Fields:
    - subscription_id: Many2one('subscription.subscription', required, ondelete='cascade')
    - product_id: Many2one('subscription.product', required, string="Product")
    - variant_id: Many2one('subscription.product.variant', string="Variant", domain="[('product_id','=',product_id)]")
    - quantity: Float, required, default=1.0
    - unit_price: Float, required, digits=(10,2)
    - tax_ids: Many2many('subscription.tax', string="Taxes")
    - discount: Float, string="Discount (%)", default=0.0
    - subtotal: Float, compute='_compute_amounts', store=True, string="Subtotal"
    - tax_amount: Float, compute='_compute_amounts', store=True
    - total: Float, compute='_compute_amounts', store=True

    @api.depends('quantity', 'unit_price', 'discount', 'tax_ids', 'variant_id')
    def _compute_amounts(self):
        for line in self:
            price = line.unit_price + (line.variant_id.price_extra if line.variant_id else 0.0)
            discount_amount = price * (line.discount / 100.0)
            subtotal = line.quantity * (price - discount_amount)
            tax_amount = sum(tax.compute_tax(subtotal) for tax in line.tax_ids)
            line.subtotal = subtotal
            line.tax_amount = tax_amount
            line.total = subtotal + tax_amount

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.unit_price = self.product_id.sales_price

    @api.onchange('variant_id')
    def _onchange_variant_id(self):
        # Trigger recomputation when variant changes
        pass

Update models/__init__.py.
```

## Expected Output
- `models/subscription_line.py`

## Verification
- Add a subscription line with a variant and verify price_extra is added
