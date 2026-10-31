# 04 — Subscription Tree & Kanban Views

## Context
This is PART 1 of the subscription views. Subscriptions are the core entity — they link a customer to a plan with start/end dates and go through states (draft → confirmed → active → paused → closed/expired). The list view needs color-coded rows by state, and the kanban needs to group by state for a visual pipeline.

**Depends on**: `subscription.subscription` model from backend.

**Model fields expected**:
- `name` (Char) — Subscription reference (e.g., SUB-00001)
- `partner_id` (Many2one: res.partner) — Customer
- `plan_id` (Many2one: subscription.plan)
- `state` (Selection: draft/confirmed/active/paused/closed/expired)
- `start_date` (Date)
- `end_date` (Date)
- `next_billing_date` (Date)
- `total_amount` (Monetary, computed)
- `currency_id` (Many2one: res.currency)
- `subscription_line_ids` (One2many: subscription.subscription.line)

## Prompt for Antigravity

```
Create the file `views/subscription_views.xml` for the Odoo 18 module `subscription_mgmt`. This is PART 1 — it contains the LIST and KANBAN views for `subscription.subscription`. The FORM view and SEARCH view will be added to this same file later.

## Odoo 18 Rules
- Use `invisible="expression"` NOT `attrs` (attrs is DEPRECATED)
- Root element: `<odoo>`
- For kanban views, use OWL-compatible template syntax

## Views to Create

### 1. Subscription List View (`view_subscription_list`)
Model: `subscription.subscription`

```xml
<record id="view_subscription_list" model="ir.ui.view">
    <field name="name">subscription.subscription.list</field>
    <field name="model">subscription.subscription</field>
    <field name="arch" type="xml">
        <list default_order="name desc"
              decoration-danger="state == 'closed' or state == 'expired'"
              decoration-success="state == 'active'"
              decoration-info="state == 'confirmed'"
              decoration-warning="state == 'paused'"
              decoration-muted="state == 'draft'">
            <field name="name"/>
            <field name="partner_id"/>
            <field name="plan_id"/>
            <field name="state" widget="badge"
                   decoration-danger="state == 'closed' or state == 'expired'"
                   decoration-success="state == 'active'"
                   decoration-info="state == 'confirmed'"
                   decoration-warning="state == 'paused'"/>
            <field name="start_date"/>
            <field name="end_date"/>
            <field name="next_billing_date"/>
            <field name="total_amount" widget="monetary" sum="Total"/>
            <field name="currency_id" column_invisible="1"/>
        </list>
    </field>
</record>
```

### 2. Subscription Kanban View (`view_subscription_kanban`)
Model: `subscription.subscription`

Create a kanban view with:
- `default_group_by="state"` so cards are grouped in columns by state
- Each card (kanban-box) should show:
  - Subscription name (bold, as title)
  - Customer name (`partner_id`)
  - Plan name (`plan_id`)
  - Next billing date
  - Total amount (monetary)
  - State badge with colors
- Use `oe_kanban_global_click` class on the card
- Use the kanban template structure:
```xml
<kanban default_group_by="state" class="o_subscription_kanban">
    <field name="name"/>
    <field name="partner_id"/>
    <field name="plan_id"/>
    <field name="state"/>
    <field name="next_billing_date"/>
    <field name="total_amount"/>
    <field name="currency_id"/>
    <templates>
        <t t-name="kanban-box">
            <div t-attf-class="oe_kanban_global_click oe_kanban_card">
                <div class="oe_kanban_content">
                    <div class="o_kanban_record_top">
                        <div class="o_kanban_record_headings">
                            <strong class="o_kanban_record_title">
                                <field name="name"/>
                            </strong>
                        </div>
                        <field name="state" widget="label_selection" options="{'classes': {'draft': 'secondary', 'confirmed': 'info', 'active': 'success', 'paused': 'warning', 'closed': 'danger', 'expired': 'dark'}}"/>
                    </div>
                    <div class="o_kanban_record_body">
                        <div><strong>Customer:</strong> <field name="partner_id"/></div>
                        <div><strong>Plan:</strong> <field name="plan_id"/></div>
                        <div><strong>Next Billing:</strong> <field name="next_billing_date"/></div>
                    </div>
                    <div class="o_kanban_record_bottom">
                        <div class="oe_kanban_bottom_left">
                            <field name="total_amount" widget="monetary"/>
                        </div>
                    </div>
                </div>
            </div>
        </t>
    </templates>
</kanban>
```

Adjust the template as needed for Odoo 18 kanban compatibility. Make sure:
- Fields used inside templates are declared at the top of `<kanban>` element
- Widget usage is correct for kanban context
- The state badge renders with appropriate colors

## File Path
`views/subscription_views.xml`

This file will be EXTENDED in later steps (05, 06) with form and search views. Only create LIST and KANBAN views now.
```

## Expected Output
- **File**: `views/subscription_views.xml`
- Contains: 2 `ir.ui.view` records (list and kanban)

## Verification
1. Add `'views/subscription_views.xml'` to `__manifest__.py` `'data'` list
2. Upgrade module
3. Navigate to Subscriptions menu
4. List view: rows should be color-coded by state
5. Switch to kanban: cards should group into state columns
6. Verify drag-and-drop between states works (if state field allows direct write)
