# Quotation Template Model

## Context
Sales reps use pre-built quotation templates with plan and product lines. Templates have a validity period in days.

## Prompt for Claude Code

```
In the Odoo 18 module "subscription_management", create the Quotation Template model.

Create `models/quotation_template.py`:

class SubscriptionQuotationTemplate(models.Model):
    _name = 'subscription.quotation.template'
    _description = 'Quotation Template'

    Fields:
    - name: Char, required, string="Template Name"
    - plan_id: Many2one('subscription.plan', required, string="Plan")
    - validity_days: Integer, default=30, string="Validity (Days)", help="Number of days the quotation remains valid"
    - template_line_ids: One2many('subscription.quotation.template.line', 'template_id')
    - is_active: Boolean, default=True
    - note: Text

class SubscriptionQuotationTemplateLine(models.Model):
    _name = 'subscription.quotation.template.line'
    _description = 'Quotation Template Line'

    Fields:
    - template_id: Many2one('subscription.quotation.template', required, ondelete='cascade')
    - product_id: Many2one('subscription.product', required)
    - quantity: Float, default=1.0
    - unit_price: Float, digits=(10,2)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.unit_price = self.product_id.sales_price

Update models/__init__.py to import quotation_template.
```

## Expected Output
- `models/quotation_template.py`

## Verification
- Create template with lines, then create subscription using template and call action_load_template
