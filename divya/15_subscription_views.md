# Subscription Views — Form, Tree, Kanban, Search

## Context
The most important views. Subscription form has status bar with clickable states, action buttons (Confirm, Activate, Pause, Close, Renew), inline subscription lines, and chatter. Tree has color decorations by state. Kanban groups by state.

## Prompt for Claude Code

```
In the Odoo 18 module "subscription_management", create all Subscription views.

Create `views/subscription_views.xml`:

TREE VIEW:
- decoration-success: state == 'active'
- decoration-info: state in ('confirmed', 'quotation')
- decoration-muted: state == 'closed'
- decoration-warning: state == 'paused'
- Columns: name, partner_id, plan_id, start_date, expiry_date, next_billing_date, amount_total (widget="monetary"), state (widget="badge", decoration-success/info/etc)

FORM VIEW:
<form>
    <header>
        <button name="action_send_quotation" string="Send Quotation" type="object" class="btn-primary" invisible="state != 'draft'"/>
        <button name="action_confirm" string="Confirm" type="object" class="btn-primary" invisible="state != 'quotation'"/>
        <button name="action_activate" string="Activate" type="object" class="btn-primary" invisible="state != 'confirmed'"/>
        <button name="action_pause" string="Pause" type="object" invisible="state != 'active'"/>
        <button name="action_activate" string="Resume" type="object" class="btn-primary" invisible="state != 'paused'"/>
        <button name="action_renew" string="Renew" type="object" invisible="state not in ('active', 'paused')"/>
        <button name="action_close" string="Close" type="object" invisible="state in ('closed', 'draft')"/>
        <button name="action_create_invoice" string="Create Invoice" type="object" class="btn-secondary" invisible="state != 'active'"/>
        <field name="state" widget="statusbar" statusbar_visible="draft,quotation,confirmed,active,closed"/>
    </header>
    <sheet>
        <div class="oe_title">
            <h1><field name="name" readonly="1"/></h1>
        </div>
        <group>
            <group>
                <field name="partner_id"/>
                <field name="plan_id"/>
                <field name="template_id"/>
                <button name="action_load_template" string="Load Template" type="object" class="btn-link" invisible="not template_id"/>
                <field name="user_id"/>
            </group>
            <group>
                <field name="start_date"/>
                <field name="expiry_date"/>
                <field name="next_billing_date"/>
                <field name="payment_term"/>
            </group>
        </group>
        <notebook>
            <page string="Subscription Lines">
                <field name="subscription_line_ids" widget="one2many">
                    <tree editable="bottom">
                        <field name="product_id"/>
                        <field name="variant_id" optional="show"/>
                        <field name="quantity"/>
                        <field name="unit_price"/>
                        <field name="tax_ids" widget="many2many_tags"/>
                        <field name="discount"/>
                        <field name="subtotal" sum="Total"/>
                        <field name="tax_amount" sum="Tax"/>
                        <field name="total" sum="Grand Total"/>
                    </tree>
                </field>
                <group class="oe_subtotal_footer">
                    <field name="amount_untaxed" widget="monetary"/>
                    <field name="amount_tax" widget="monetary"/>
                    <field name="amount_total" widget="monetary" class="oe_subtotal_footer_separator"/>
                </group>
            </page>
            <page string="Invoices" invisible="invoice_count == 0">
                <field name="invoice_ids">
                    <tree>
                        <field name="name"/>
                        <field name="invoice_date"/>
                        <field name="amount_total" widget="monetary"/>
                        <field name="state" widget="badge"/>
                    </tree>
                </field>
            </page>
            <page string="Notes">
                <field name="note" placeholder="Internal notes..."/>
            </page>
        </notebook>
    </sheet>
    <chatter/>
</form>

KANBAN VIEW:
- Default group by state
- Card shows: name, partner_id, plan_id, amount_total, next_billing_date
- Color indicator based on state

SEARCH VIEW:
- Search: partner_id, name, plan_id
- Filters: My Subscriptions (user_id = uid), Active (state=active), Expiring Soon (expiry_date within 30 days), Expired (is_expired=True), Draft, Closed
- Group By: State, Plan, Customer, Salesperson, Month (start_date)

Update __manifest__.py to include 'views/subscription_views.xml'.
```

## Expected Output
- `views/subscription_views.xml`

## Verification
- Navigate to Subscriptions, test all view types, verify buttons work per state
