# Discount Rules & Tax Configuration Views

## Context
Admin controls taxes and discount rules. Prem creates clean XML tree, form, and search views for both `subscription.tax` and `subscription.discount.rule`.

## Prompt for Antigravity

```markdown
In our Odoo 18 module `subscription_management`:

1. Create `views/discount_views.xml`:
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_subscription_discount_tree" model="ir.ui.view">
        <field name="name">subscription.discount.rule.tree</field>
        <field name="model">subscription.discount.rule</field>
        <field name="arch" type="xml">
            <tree string="Discount Rules" decoration-muted="not is_active">
                <field name="name"/>
                <field name="discount_type" widget="badge"/>
                <field name="amount"/>
                <field name="apply_on" widget="badge"/>
                <field name="date_start"/>
                <field name="date_end"/>
                <field name="current_usage"/>
                <field name="max_usage"/>
                <field name="is_active" widget="boolean_toggle"/>
            </tree>
        </field>
    </record>

    <record id="view_subscription_discount_form" model="ir.ui.view">
        <field name="name">subscription.discount.rule.form</field>
        <field name="model">subscription.discount.rule</field>
        <field name="arch" type="xml">
            <form string="Discount Rule">
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" placeholder="e.g. Summer Promo 20%"/></h1>
                    </div>
                    <group>
                        <group string="Discount Configuration">
                            <field name="discount_type"/>
                            <field name="amount"/>
                            <field name="apply_on"/>
                            <field name="product_ids" widget="many2many_tags" invisible="apply_on != 'product'"/>
                        </group>
                        <group string="Conditions &amp; Limits">
                            <field name="min_purchase"/>
                            <field name="min_quantity"/>
                            <field name="max_usage"/>
                            <field name="current_usage" readonly="1"/>
                            <field name="date_start"/>
                            <field name="date_end"/>
                            <field name="is_active" widget="boolean_toggle"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Terms &amp; Description">
                            <field name="description" placeholder="Internal rule notes..."/>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_subscription_discount_search" model="ir.ui.view">
        <field name="name">subscription.discount.rule.search</field>
        <field name="model">subscription.discount.rule</field>
        <field name="arch" type="xml">
            <search string="Search Discounts">
                <field name="name"/>
                <filter string="Active" name="active" domain="[('is_active', '=', True)]"/>
                <filter string="Expired / Inactive" name="inactive" domain="[('is_active', '=', False)]"/>
                <group expand="0" string="Group By">
                    <filter string="Type" name="group_by_type" context="{'group_by': 'discount_type'}"/>
                    <filter string="Apply On" name="group_by_apply" context="{'group_by': 'apply_on'}"/>
                </group>
            </search>
        </field>
    </record>
</odoo>
```

2. Create `views/tax_views.xml`:
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_subscription_tax_tree" model="ir.ui.view">
        <field name="name">subscription.tax.tree</field>
        <field name="model">subscription.tax</field>
        <field name="arch" type="xml">
            <tree string="Taxes">
                <field name="name"/>
                <field name="tax_type" widget="badge"/>
                <field name="amount"/>
                <field name="is_active" widget="boolean_toggle"/>
            </tree>
        </field>
    </record>

    <record id="view_subscription_tax_form" model="ir.ui.view">
        <field name="name">subscription.tax.form</field>
        <field name="model">subscription.tax</field>
        <field name="arch" type="xml">
            <form string="Tax Rule">
                <sheet>
                    <group>
                        <group>
                            <field name="name"/>
                            <field name="tax_type"/>
                            <field name="amount"/>
                        </group>
                        <group>
                            <field name="is_active"/>
                            <field name="description"/>
                        </group>
                    </group>
                </sheet>
            </form>
        </field>
    </record>
</odoo>
```
```

## Expected Output
- `views/discount_views.xml`
- `views/tax_views.xml`

## Verification
Open Configuration > Taxes and Configuration > Discount Rules. Create and edit rules with validation.
