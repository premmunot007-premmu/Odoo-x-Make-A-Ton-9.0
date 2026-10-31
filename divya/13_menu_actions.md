# Menu Structure & Window Actions

## Context
The full navigation menu for the module: Subscriptions, Products & Plans, Billing, Configuration, Dashboard.

## Prompt for Claude Code

```
In the Odoo 18 module "subscription_management", create the complete menu structure.

Create `views/menu.xml`:
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Top-level menu -->
    <menuitem id="menu_subscription_root" name="Subscriptions" web_icon="subscription_management,static/description/icon.png" sequence="5"/>

    <!-- Sub-menus Level 1 -->
    <menuitem id="menu_subscriptions" name="Subscriptions" parent="menu_subscription_root" sequence="10"/>
    <menuitem id="menu_products" name="Products &amp; Plans" parent="menu_subscription_root" sequence="20"/>
    <menuitem id="menu_billing" name="Billing" parent="menu_subscription_root" sequence="30"/>
    <menuitem id="menu_config" name="Configuration" parent="menu_subscription_root" sequence="90"/>

    <!-- Subscriptions sub-items -->
    <menuitem id="menu_all_subscriptions" name="All Subscriptions" parent="menu_subscriptions" action="action_subscription" sequence="10"/>
    <menuitem id="menu_quotation_templates" name="Quotation Templates" parent="menu_subscriptions" action="action_quotation_template" sequence="20"/>

    <!-- Products & Plans sub-items -->
    <menuitem id="menu_all_products" name="Products" parent="menu_products" action="action_product" sequence="10"/>
    <menuitem id="menu_all_plans" name="Plans" parent="menu_products" action="action_plan" sequence="20"/>

    <!-- Billing sub-items -->
    <menuitem id="menu_invoices" name="Invoices" parent="menu_billing" action="action_invoice" sequence="10"/>
    <menuitem id="menu_payments" name="Payments" parent="menu_billing" action="action_payment" sequence="20"/>

    <!-- Configuration sub-items -->
    <menuitem id="menu_taxes" name="Taxes" parent="menu_config" action="action_tax" sequence="10"/>
    <menuitem id="menu_discounts" name="Discount Rules" parent="menu_config" action="action_discount" sequence="20"/>

    <!-- Dashboard (client action) -->
    <menuitem id="menu_dashboard" name="Dashboard" parent="menu_subscription_root" action="action_subscription_dashboard" sequence="1"/>

    <!-- Window Actions -->
    <record id="action_subscription" model="ir.actions.act_window">
        <field name="name">Subscriptions</field>
        <field name="res_model">subscription.subscription</field>
        <field name="view_mode">tree,form,kanban</field>
    </record>

    <record id="action_product" model="ir.actions.act_window">
        <field name="name">Products</field>
        <field name="res_model">subscription.product</field>
        <field name="view_mode">tree,form,kanban</field>
    </record>

    <record id="action_plan" model="ir.actions.act_window">
        <field name="name">Plans</field>
        <field name="res_model">subscription.plan</field>
        <field name="view_mode">tree,form</field>
    </record>

    <record id="action_invoice" model="ir.actions.act_window">
        <field name="name">Invoices</field>
        <field name="res_model">subscription.invoice</field>
        <field name="view_mode">tree,form</field>
    </record>

    <record id="action_payment" model="ir.actions.act_window">
        <field name="name">Payments</field>
        <field name="res_model">subscription.payment</field>
        <field name="view_mode">tree,form</field>
    </record>

    <record id="action_tax" model="ir.actions.act_window">
        <field name="name">Tax Rules</field>
        <field name="res_model">subscription.tax</field>
        <field name="view_mode">tree,form</field>
    </record>

    <record id="action_discount" model="ir.actions.act_window">
        <field name="name">Discount Rules</field>
        <field name="res_model">subscription.discount.rule</field>
        <field name="view_mode">tree,form</field>
    </record>

    <record id="action_quotation_template" model="ir.actions.act_window">
        <field name="name">Quotation Templates</field>
        <field name="res_model">subscription.quotation.template</field>
        <field name="view_mode">tree,form</field>
    </record>

    <!-- Dashboard client action placeholder -->
    <record id="action_subscription_dashboard" model="ir.actions.client">
        <field name="name">Dashboard</field>
        <field name="tag">subscription_dashboard</field>
    </record>
</odoo>

Update __manifest__.py data to include 'views/menu.xml'.
Make sure the menu is visible to subscription_admin and subscription_staff groups.
```

## Expected Output
- `views/menu.xml`
- Updated `__manifest__.py`

## Verification
- Install module, check that "Subscriptions" appears in the main menu bar
