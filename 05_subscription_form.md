# 05 — Subscription Form View

## Context
This is PART 2 of the subscription views — the detailed **form view**. This is the most complex view in the system. It needs a status bar with clickable states, action buttons that show/hide based on state, a sheet with customer/plan info, a notebook with subscription lines (editable inline), a tab for related invoices, and the chatter for communication history.

**Depends on**: `subscription.subscription` model, `subscription.subscription.line` model, views from `04_subscription_tree_kanban.md`.

**Model fields expected for `subscription.subscription`**:
- `name`, `partner_id`, `plan_id`, `state`, `start_date`, `end_date`, `next_billing_date`
- `total_amount`, `currency_id`, `subscription_line_ids`, `invoice_ids`
- `company_id` (Many2one: res.company)
- `notes` (Text)
- `message_follower_ids`, `message_ids` (from mail.thread mixin)

**Model fields expected for `subscription.subscription.line`**:
- `subscription_id` (Many2one)
- `product_id` (Many2one: subscription.product)
- `variant_id` (Many2one: subscription.product.variant)
- `quantity` (Float)
- `unit_price` (Monetary)
- `discount` (Float, percentage)
- `tax_id` (Many2one: subscription.tax) or `tax_ids` (Many2many)
- `subtotal` (Monetary, computed)

**State transition methods** (defined in backend model):
- `action_confirm` — draft → confirmed
- `action_activate` — confirmed → active
- `action_pause` — active → paused
- `action_resume` — paused → active
- `action_close` — any → closed
- `action_renew` — closed/expired → draft (creates renewal)

## Prompt for Antigravity

```
APPEND to the existing file `views/subscription_views.xml` in the Odoo 18 module `subscription_mgmt`. Add the FORM VIEW for `subscription.subscription`. This view should be appended INSIDE the existing `<odoo>` tags (before the closing `</odoo>`).

## Odoo 18 Rules
- Use `invisible="expression"` directly, NOT `attrs` (attrs is DEPRECATED in Odoo 18)
- Boolean expressions like `invisible="state != 'draft'"` are valid
- For combining conditions: `invisible="state != 'active' and state != 'paused'"`

## Form View to Create

### Subscription Form View (`view_subscription_form`)
Model: `subscription.subscription`

```xml
<record id="view_subscription_form" model="ir.ui.view">
    <field name="name">subscription.subscription.form</field>
    <field name="model">subscription.subscription</field>
    <field name="arch" type="xml">
        <form string="Subscription">
            <header>
                <!-- Action buttons - visible based on state -->
                <button name="action_confirm" type="object" string="Confirm"
                        class="btn-primary" invisible="state != 'draft'"
                        confirm="Are you sure you want to confirm this subscription?"/>
                <button name="action_activate" type="object" string="Activate"
                        class="btn-primary" invisible="state != 'confirmed'"/>
                <button name="action_pause" type="object" string="Pause"
                        class="btn-warning" invisible="state != 'active'"/>
                <button name="action_resume" type="object" string="Resume"
                        class="btn-primary" invisible="state != 'paused'"/>
                <button name="action_close" type="object" string="Close"
                        class="btn-danger"
                        invisible="state in ('closed', 'expired', 'draft')"
                        confirm="Are you sure you want to close this subscription?"/>
                <button name="action_renew" type="object" string="Renew"
                        class="btn-success"
                        invisible="state != 'closed' and state != 'expired'"/>
                <!-- Status bar -->
                <field name="state" widget="statusbar"
                       statusbar_visible="draft,confirmed,active"/>
            </header>
            <sheet>
                <div class="oe_button_box" name="button_box">
                    <!-- Smart button for invoice count -->
                    <button name="action_view_invoices" type="object"
                            class="oe_stat_button" icon="fa-money"
                            invisible="state == 'draft'">
                        <div class="o_stat_info">
                            <field name="invoice_count" class="o_stat_value"/>
                            <span class="o_stat_text">Invoices</span>
                        </div>
                    </button>
                </div>
                <widget name="web_ribbon" title="Expired"
                        bg_color="text-bg-danger"
                        invisible="state != 'expired'"/>
                <widget name="web_ribbon" title="Closed"
                        bg_color="text-bg-secondary"
                        invisible="state != 'closed'"/>
                <div class="oe_title">
                    <label for="name"/>
                    <h1>
                        <field name="name" readonly="1" placeholder="New"/>
                    </h1>
                </div>
                <group>
                    <group string="Customer Information">
                        <field name="partner_id"
                               options="{'no_create': False, 'no_open': True}"
                               readonly="state != 'draft'"/>
                        <field name="company_id" groups="base.group_multi_company"
                               readonly="state != 'draft'"/>
                        <field name="currency_id" invisible="1"/>
                    </group>
                    <group string="Subscription Details">
                        <field name="plan_id" readonly="state != 'draft'"/>
                        <field name="start_date" readonly="state != 'draft'"/>
                        <field name="end_date"/>
                        <field name="next_billing_date"
                               readonly="state in ('closed', 'expired')"/>
                    </group>
                </group>
                <notebook>
                    <page string="Subscription Lines" name="lines">
                        <field name="subscription_line_ids"
                               readonly="state in ('closed', 'expired')">
                            <list editable="bottom">
                                <field name="product_id"/>
                                <field name="variant_id"
                                       domain="[('product_id', '=', product_id)]"
                                       optional="show"/>
                                <field name="quantity"/>
                                <field name="unit_price" widget="monetary"/>
                                <field name="discount" optional="show"/>
                                <field name="tax_id" optional="show"/>
                                <field name="subtotal" widget="monetary"
                                       readonly="1" sum="Total"/>
                            </list>
                        </field>
                        <group class="oe_subtotal_footer oe_right" colspan="2">
                            <field name="total_amount" widget="monetary"
                                   class="oe_subtotal_footer_separator"
                                   string="Total Amount"/>
                        </group>
                    </page>
                    <page string="Invoices" name="invoices">
                        <field name="invoice_ids" readonly="1">
                            <list>
                                <field name="name"/>
                                <field name="invoice_date"/>
                                <field name="total_amount" widget="monetary" sum="Total"/>
                                <field name="state" widget="badge"
                                       decoration-success="state == 'paid'"
                                       decoration-danger="state == 'overdue'"
                                       decoration-info="state == 'confirmed'"
                                       decoration-muted="state == 'draft'"/>
                            </list>
                        </field>
                    </page>
                    <page string="Notes" name="notes">
                        <field name="notes" placeholder="Internal notes about this subscription..."/>
                    </page>
                </notebook>
            </sheet>
            <div class="oe_chatter">
                <field name="message_follower_ids"/>
                <field name="activity_ids"/>
                <field name="message_ids"/>
            </div>
        </form>
    </field>
</record>
```

## Key Points
- Buttons use `invisible` with state conditions (NOT attrs)
- Status bar shows draft → confirmed → active as clickable
- Smart button for invoices with count
- Ribbons for expired/closed states
- Subscription lines are editable inline with monetary widgets
- Chatter section at the bottom with followers, activities, messages
- Form fields become readonly in terminal states
- The `confirm` attribute on dangerous buttons asks user to confirm

## File Path
APPEND to `views/subscription_views.xml` (add before closing `</odoo>` tag)
```

## Expected Output
- **File**: `views/subscription_views.xml` (updated — now has list, kanban, AND form views)
- The form view record is appended

## Verification
1. Upgrade module
2. Navigate to Subscriptions, click on a subscription (or create new)
3. Form should show:
   - Header with state-dependent buttons (only relevant buttons visible)
   - Clickable status bar
   - Customer and plan info in two-column layout
   - Notebook with subscription lines, invoices, notes tabs
   - Chatter at bottom
4. Create a draft subscription → click "Confirm" → check button visibility changes
5. Check that expired subscriptions show the red ribbon
