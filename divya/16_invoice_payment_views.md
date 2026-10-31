# Invoice & Payment Views

## Context
Invoice views with status bar, confirm/cancel/payment buttons, invoice line details. Payment views with method, amount, reference.

## Prompt for Claude Code

```
In the Odoo 18 module "subscription_management", create Invoice and Payment views.

Create `views/invoice_views.xml`:

TREE VIEW:
- decoration-danger: is_overdue == True
- decoration-success: state == 'paid'
- decoration-muted: state == 'cancelled'
- Columns: name, partner_id, subscription_id, invoice_date, due_date, amount_total (monetary), amount_due (monetary), payment_status (widget="badge"), state (widget="badge")

FORM VIEW:
<form>
    <header>
        <button name="action_confirm" string="Confirm" type="object" class="btn-primary" invisible="state != 'draft'"/>
        <button name="%(action_payment_wizard)d" string="Register Payment" type="action" class="btn-primary" invisible="state != 'confirmed'"/>
        <button name="action_cancel" string="Cancel" type="object" invisible="state in ('paid', 'cancelled')"/>
        <field name="state" widget="statusbar" statusbar_visible="draft,confirmed,paid"/>
    </header>
    <sheet>
        <div class="oe_title"><h1><field name="name" readonly="1"/></h1></div>
        <group>
            <group>
                <field name="partner_id"/>
                <field name="subscription_id"/>
                <field name="invoice_date"/>
                <field name="due_date"/>
            </group>
            <group>
                <field name="payment_status" widget="badge"/>
                <field name="amount_paid" widget="monetary"/>
                <field name="amount_due" widget="monetary"/>
                <field name="is_overdue" invisible="1"/>
            </group>
        </group>
        <notebook>
            <page string="Invoice Lines">
                <field name="invoice_line_ids">
                    <tree editable="bottom">
                        <field name="product_id"/>
                        <field name="description"/>
                        <field name="quantity"/>
                        <field name="unit_price"/>
                        <field name="tax_ids" widget="many2many_tags"/>
                        <field name="discount_amount"/>
                        <field name="subtotal" sum="Subtotal"/>
                        <field name="tax_amount" sum="Tax"/>
                        <field name="total" sum="Total"/>
                    </tree>
                </field>
                <group class="oe_subtotal_footer">
                    <field name="amount_untaxed" widget="monetary"/>
                    <field name="amount_tax" widget="monetary"/>
                    <field name="amount_total" widget="monetary" class="oe_subtotal_footer_separator"/>
                </group>
            </page>
            <page string="Payments">
                <field name="payment_ids">
                    <tree>
                        <field name="payment_date"/>
                        <field name="payment_method"/>
                        <field name="amount" widget="monetary"/>
                        <field name="reference"/>
                    </tree>
                </field>
            </page>
        </notebook>
        <field name="note" placeholder="Additional notes..."/>
    </sheet>
    <chatter/>
</form>

SEARCH VIEW:
- Filters: Draft, Confirmed, Paid, Overdue (is_overdue=True), Cancelled
- Group By: State, Customer, Month

Create `views/payment_views.xml`:

TREE VIEW: payment_date, invoice_id, partner_id, payment_method, amount (monetary), reference

FORM VIEW:
- group: invoice_id, partner_id, payment_method
- group: amount, payment_date, reference
- note field

SEARCH VIEW:
- Filter by payment_method, Group by method, month

Update __manifest__.py to include both view files.
```

## Expected Output
- `views/invoice_views.xml`
- `views/payment_views.xml`

## Verification
- Open invoice, verify status bar and buttons, test Register Payment flow
