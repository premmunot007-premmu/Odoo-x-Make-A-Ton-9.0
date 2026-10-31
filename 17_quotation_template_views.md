# Quotation Template Views

## Context
Sales reps use quotation templates to quickly generate proposals. This file creates the form, tree, and search views for `subscription.quotation.template`.

## Prompt for Antigravity

```markdown
In our Odoo 18 module `subscription_management`, create `views/quotation_template_views.xml`:

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_subscription_template_tree" model="ir.ui.view">
        <field name="name">subscription.quotation.template.tree</field>
        <field name="model">subscription.quotation.template</field>
        <field name="arch" type="xml">
            <tree string="Quotation Templates">
                <field name="name"/>
                <field name="plan_id"/>
                <field name="validity_days"/>
                <field name="is_active" widget="boolean_toggle"/>
            </tree>
        </field>
    </record>

    <record id="view_subscription_template_form" model="ir.ui.view">
        <field name="name">subscription.quotation.template.form</field>
        <field name="model">subscription.quotation.template</field>
        <field name="arch" type="xml">
            <form string="Quotation Template">
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" placeholder="e.g. Standard SaaS Offer"/></h1>
                    </div>
                    <group>
                        <group>
                            <field name="plan_id"/>
                            <field name="validity_days"/>
                        </group>
                        <group>
                            <field name="is_active"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Template Products">
                            <field name="template_line_ids">
                                <tree editable="bottom">
                                    <field name="product_id"/>
                                    <field name="quantity"/>
                                    <field name="unit_price"/>
                                </tree>
                            </field>
                        </page>
                        <page string="Terms &amp; Notes">
                            <field name="note" placeholder="Default quotation proposal terms..."/>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>
</odoo>
```
```

## Expected Output
- `views/quotation_template_views.xml`

## Verification
Under Subscriptions > Subscriptions > Quotation Templates, create a new template with default lines and assign it on a subscription draft.
