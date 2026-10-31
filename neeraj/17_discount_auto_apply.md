# Discount Auto-Application on Invoicing

## Context
When creating an invoice, applicable discount rules should auto-apply: check product/subscription scope, date validity, usage limits, min purchase/quantity conditions.

## Prompt for Antigravity

```
In the Odoo 18 module "subscription_management", enhance the discount application logic.

In `models/subscription.py`, ensure `_get_discount_amount(line)` method handles all cases:

def _get_discount_amount(self, line):
    """Calculate total discount for a subscription line based on active discount rules"""
    today = fields.Date.today()
    
    # Find all potentially applicable discount rules
    domain = [
        '|', ('date_start', '=', False), ('date_start', '<=', today),
        '|', ('date_end', '=', False), ('date_end', '>=', today),
    ]
    all_discounts = self.env['subscription.discount.rule'].search(domain)
    
    base_amount = line.quantity * line.unit_price
    total_discount = 0.0
    
    for disc in all_discounts:
        # Check usage limit
        if disc.max_usage > 0 and disc.current_usage >= disc.max_usage:
            continue
        
        # Check scope
        if disc.apply_on == 'product' and line.product_id not in disc.product_ids:
            continue
        
        # Check minimum conditions
        if disc.min_quantity and line.quantity < disc.min_quantity:
            continue
        if disc.min_purchase and base_amount < disc.min_purchase:
            continue
        
        # Apply discount
        if disc.discount_type == 'percentage':
            discount_val = base_amount * (disc.amount / 100.0)
        else:
            discount_val = min(disc.amount, base_amount)  # Don't exceed base
        
        total_discount += discount_val
        
        # Increment usage counter
        disc.sudo().write({'current_usage': disc.current_usage + 1})
    
    return min(total_discount, base_amount)  # Cap at 100%

Also add a method to preview discounts without applying:
def _preview_discounts(self):
    """Show what discounts would apply to current subscription lines"""
    self.ensure_one()
    result = []
    for line in self.subscription_line_ids:
        discount = self._get_discount_amount(line)
        if discount > 0:
            result.append({
                'product': line.product_id.name,
                'original': line.quantity * line.unit_price,
                'discount': discount,
                'final': (line.quantity * line.unit_price) - discount,
            })
    return result
```

## Expected Output
- Updated `models/subscription.py` with enhanced discount logic

## Verification
- Create discount rule for a product, create invoice → discount should appear on invoice line
