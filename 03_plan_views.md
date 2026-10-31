# 03 — Plan Views

## Context
Plans define the subscription packages customers can buy (e.g., "Monthly Pro Plan", "Annual Enterprise"). Each plan has plan lines that specify which products/variants are included, at what quantity and price. The form view needs an inline editable one2many for plan lines.

**Depends on**: `subscription.plan` and `subscription.plan.line` models from backend.

**Model fields expected for `subscription.plan`**:
- `name` (Char) — Plan name
- `plan_code` (Char) — Unique code
- `description` (Text)
- `billing_frequency` (Selection: monthly/quarterly/semi_annually/annually)
- `base_price` (Float/Monetary)
- `currency_id` (Many2one: res.currency)
- `plan_line_ids` (One2many: subscription.plan.line)
- `active` (Boolean)

**Model fields expected for `subscription.plan.line`**:
- `plan_id` (Many2one: subscription.plan)
- `product_id` (Many2one: subscription.product)
- `variant_id` (Many2one: subscription.product.variant)
- `quantity` (Integer/Float)
- `unit_price` (Float/Monetary)
- `subtotal` (Float/Monetary, computed)

## Prompt for Antigravity

```
Create the file `views/plan_views.xml` for the Odoo 18 module `subscription_mgmt`. This file defines all views for the `subscription.plan` model.

## Odoo 18 Rules
- Use `invisible="expression"` NOT `attrs` (attrs is deprecated)
- Use `<list>` or `<tree>` for list views
- Root element: `<odoo>`

## Views to Create

### 1. Plan List View (`view_subscription_plan_list`)
Model: `subscription.plan`
- Columns: `plan_code`, `name`, `billing_frequency` (badge widget), `base_price` (monetary), `currency_id`, `active`
- Decoration: `decoration-muted="not active"`
- Default order: `sequence, name`

### 2. Plan Form View (`view_subscription_plan_form`)
Model: `subscription.plan`
Layout:
```xml
<form string="Subscription Plan">
    <sheet>
        <div class="oe_title">
            <label for="name"/>
            <h1><field name="name" placeholder="Plan Name"/></h1>
            <field name="plan_code" placeholder="e.g., PLAN-001"/>
        </div>
        <group>
            <group string="Billing">
                <field name="billing_frequency"/>
                <field name="base_price" widget="monetary"/>
                <field name="currency_id" groups="base.group_multi_currency"/>
            </group>
            <group string="Settings">
                <field name="active"/>
            </group>
        </group>
        <notebook>
            <page string="Plan Lines" name="plan_lines">
                <field name="plan_line_ids">
                    <list editable="bottom">
                        <field name="product_id"/>
                        <field name="variant_id" domain="[('product_id', '=', product_id)]" optional="show"/>
                        <field name="quantity"/>
                        <field name="unit_price" widget="monetary"/>
                        <field name="subtotal" widget="monetary" readonly="1" sum="Total"/>
                    </list>
                </field>
                <!-- Show total at the bottom -->
                <group class="oe_subtotal_footer">
                    <field name="base_price" widget="monetary" string="Total Plan Price" class="oe_subtotal_footer_separator"/>
                </group>
            </page>
            <page string="Description" name="description">
                <field name="description" placeholder="Describe what this plan includes..."/>
            </page>
        </notebook>
    </sheet>
</form>
```

### 3. Plan Search View (`view_subscription_plan_search`)
Model: `subscription.plan`
- Search fields: `name`, `plan_code`
- Filters:
  - "Monthly" → `billing_frequency = 'monthly'`
  - "Quarterly" → `billing_frequency = 'quarterly'`
  - "Semi-Annual" → `billing_frequency = 'semi_annually'`
  - "Annual" → `billing_frequency = 'annually'`
  - separator
  - "Archived" → `active = False`
- Group by: `billing_frequency`

## File Path
`views/plan_views.xml`

Do NOT include menu items or actions — those are already in `views/menu.xml`.
```

## Expected Output
- **File**: `views/plan_views.xml`
- Contains: 3 `ir.ui.view` records (list, form, search)

## Verification
1. Add `'views/plan_views.xml'` to `__manifest__.py` `'data'` list (before `menu.xml`)
2. Upgrade module
3. Navigate to Products & Plans → Plans
4. List view should show plan details with billing frequency badges
5. Open a plan — form should show inline editable plan lines
6. Add a plan line: select product, variant should filter by product, enter qty/price
7. Test search filters for billing frequency
