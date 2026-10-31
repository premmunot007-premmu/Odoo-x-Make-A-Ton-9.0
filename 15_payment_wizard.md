# Register Payment Wizard (Transient Model & Popup Dialog)

## Context
When staff or admin clicks "Register Payment" on an invoice, an Odoo wizard popup modal opens with default amount set to the remaining balance, payment method selector, date, and transaction reference.

## Prompt for Antigravity

```markdown
In our Odoo 18 module `subscription_management`:

1. Create `wizard/payment_wizard.py`:
```python
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SubscriptionPaymentWizard(models.TransientModel):
    _name = 'subscription.payment.wizard'
    _description = 'Register Invoice Payment Wizard'

    invoice_id = fields.Many2one('subscription.invoice', string="Invoice", required=True)
    partner_id = fields.Many2one('res.partner', related='invoice_id.partner_id', readonly=True)
    amount = fields.Float(string="Payment Amount", required=True, digits=(10, 2))
    amount_due = fields.Float(related='invoice_id.amount_due', readonly=True)
    payment_method = fields.Selection([
        ('bank_transfer', 'Bank Transfer'),
        ('credit_card', 'Credit Card'),
        ('upi', 'UPI'),
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
    ], default='bank_transfer', required=True)
    payment_date = fields.Date(default=fields.Date.today, required=True)
    reference = fields.Char(string="Payment Reference / Transaction ID")
    note = fields.Text(string="Note")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')
        if active_id:
            invoice = self.env['subscription.invoice'].browse(active_id)
            res.update({
                'invoice_id': invoice.id,
                'amount': invoice.amount_due,
            })
        return res

    def action_confirm_payment(self):
        self.ensure_one()
        if self.amount <= 0:
            raise ValidationError("Payment amount must be greater than zero.")
        if self.amount > self.invoice_id.amount_due:
            raise ValidationError("Payment amount exceeds outstanding balance.")

        self.env['subscription.payment'].create({
            'invoice_id': self.invoice_id.id,
            'amount': self.amount,
            'payment_method': self.payment_method,
            'payment_date': self.payment_date,
            'reference': self.reference,
            'note': self.note,
        })
        return {'type': 'ir.actions.act_window_close'}
```

2. Create `wizard/payment_wizard_views.xml`:
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_subscription_payment_wizard_form" model="ir.ui.view">
        <field name="name">subscription.payment.wizard.form</field>
        <field name="model">subscription.payment.wizard</field>
        <field name="arch" type="xml">
            <form string="Register Payment">
                <group>
                    <group>
                        <field name="invoice_id" readonly="1"/>
                        <field name="partner_id"/>
                        <field name="amount_due"/>
                    </group>
                    <group>
                        <field name="amount"/>
                        <field name="payment_method"/>
                        <field name="payment_date"/>
                        <field name="reference"/>
                    </group>
                </group>
                <field name="note" placeholder="Optional internal notes..."/>
                <footer>
                    <button name="action_confirm_payment" string="Create Payment" type="object" class="btn-primary"/>
                    <button string="Cancel" class="btn-secondary" special="cancel"/>
                </footer>
            </form>
        </field>
    </record>

    <record id="action_payment_wizard" model="ir.actions.act_window">
        <field name="name">Register Payment</field>
        <field name="res_model">subscription.payment.wizard</field>
        <field name="view_mode">form</field>
        <field name="target">new</field>
    </record>
</odoo>
```

3. Update `wizard/__init__.py`:
```python
from . import payment_wizard
```
```

## Expected Output
- `wizard/payment_wizard.py`
- `wizard/payment_wizard_views.xml`
- `wizard/__init__.py`

## Verification
Open a Confirmed invoice in Odoo, click "Register Payment" button in the header. The wizard modal should pop up prefilled with the outstanding balance.
