# Security — Groups, Access Rules, Record Rules

## Context
Three roles: Admin (full access), Staff (limited day-to-day), Customer (portal — own data only). Admin can create staff and manage everything. Record rules ensure customers see only their own records.

## Prompt for Claude Code

```
In the Odoo 18 module "subscription_management", create the complete security layer.

Create `security/subscription_security.xml`:
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Category -->
    <record id="module_category_subscription" model="ir.module.category">
        <field name="name">Subscription Management</field>
        <field name="sequence">20</field>
    </record>

    <!-- Groups -->
    <record id="group_subscription_customer" model="res.groups">
        <field name="name">Customer (Portal)</field>
        <field name="category_id" ref="module_category_subscription"/>
        <field name="implied_ids" eval="[(4, ref('base.group_portal'))]"/>
    </record>

    <record id="group_subscription_staff" model="res.groups">
        <field name="name">Staff</field>
        <field name="category_id" ref="module_category_subscription"/>
        <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
    </record>

    <record id="group_subscription_admin" model="res.groups">
        <field name="name">Administrator</field>
        <field name="category_id" ref="module_category_subscription"/>
        <field name="implied_ids" eval="[(4, ref('group_subscription_staff'))]"/>
    </record>
</odoo>

Create `security/ir.model.access.csv` with these columns:
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink

Rules for ADMIN (group_subscription_admin) — full CRUD on ALL models:
- subscription.product, subscription.product.variant, subscription.plan, subscription.plan.line
- subscription.subscription, subscription.subscription.line
- subscription.quotation.template, subscription.quotation.template.line
- subscription.invoice, subscription.invoice.line
- subscription.payment, subscription.tax, subscription.discount.rule

Rules for STAFF (group_subscription_staff):
- Read+Write+Create on: subscription, subscription.line, invoice, invoice.line, payment
- Read only on: product, product.variant, plan, plan.line, tax, discount.rule, quotation.template

Rules for PORTAL (group_subscription_customer / base.group_portal):
- Read only on: subscription, subscription.line, invoice, invoice.line, payment

Create `security/subscription_record_rules.xml`:
Record rules with domains:
1. Portal users: subscription records where partner_id = user.partner_id
2. Portal users: invoice records where partner_id = user.partner_id
3. Portal users: payment records where invoice_id.partner_id = user.partner_id
4. Staff/Admin: see all records (no domain restriction)

Example:
    <record id="subscription_portal_rule" model="ir.rule">
        <field name="name">Portal: Own Subscriptions Only</field>
        <field name="model_id" ref="model_subscription_subscription"/>
        <field name="groups" eval="[(4, ref('base.group_portal'))]"/>
        <field name="domain_force">[('partner_id', '=', user.partner_id.id)]</field>
    </record>

Update __manifest__.py data list to include:
    'security/subscription_security.xml',
    'security/ir.model.access.csv',
    'security/subscription_record_rules.xml',
```

## Expected Output
- `security/subscription_security.xml`
- `security/ir.model.access.csv`
- `security/subscription_record_rules.xml`
- Updated `__manifest__.py`

## Verification
- Install module, check Settings > Users > Groups for the 3 subscription groups
- Login as portal user, verify only own records visible
