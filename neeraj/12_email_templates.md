# Email Templates

## Context
Transactional emails for: subscription confirmation, invoice sent, payment received, password reset.

## Prompt for Antigravity

```
In the Odoo 18 module "subscription_management", create `data/email_templates.xml`.

Create mail.template records for:

1. Subscription Confirmed:
- model_id: subscription.subscription
- subject: "Your Subscription ${object.name} is Confirmed"
- body_html: Professional HTML email with subscription details (name, plan, start date, amount), company logo placeholder, "View Subscription" button linking to portal

2. Invoice Sent:
- model_id: subscription.invoice
- subject: "Invoice ${object.name} from Brightloop Software"
- body_html: Invoice summary (number, date, amount, due date), line items table, "View Invoice" button

3. Payment Received:
- model_id: subscription.payment
- subject: "Payment Confirmation - ${object.invoice_id.name}"
- body_html: Payment details (amount, method, date), remaining balance, "View Invoice" button

4. Password Reset:
- model_id: res.users
- subject: "Reset Your Password - Brightloop Software"
- body_html: Reset link with token URL, 24h expiry notice, security warning about not sharing

Use Odoo's mail template syntax: ${object.field_name}, ${object.partner_id.name}
Use responsive HTML with inline CSS for email compatibility.

Update __manifest__.py data list to include 'data/email_templates.xml'.
```

## Expected Output
- `data/email_templates.xml`

## Verification
- Check Settings > Technical > Email Templates, verify 4 templates exist
