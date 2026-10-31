# 07 — Invoice Views

## Context
Invoices are generated from subscriptions (either manually or via scheduled billing). Each invoice has invoice lines, a state workflow (draft → confirmed → paid, or overdue), and needs a "Register Payment" button that opens the payment wizard. The form view is complex with a status bar, invoice lines, and totals.

**Depends on**: `subscription.invoice` and `subscription.invoice.line` models from backend.

**Model fields expected for `subscription.invoice`**:
- `name` (Char) — Invoice number (e.g., INV-00001)
- `subscription_id` (Many2one: subscription.subscription)
- `partner_id` (Many2one: res.partner) — Customer
- `invoice_date` (Date)
- `due_date` (Date)
- `state` (Selection: draft/confirmed/paid/cancelled/overdue)
- `invoice_line_ids` (One2many: subscription.invoice.line)
- `subtotal` (Monetary, computed)
- `tax_amount` (Monetary, computed)
- `total_amount` (Monetary, computed)
- `amount_paid` (Monetary, computed)
- `amount_due` (Monetary, computed)
- `currency_id` (Many2one: res.currency)
- `payment_ids` (One2many: subscription.payment)
- `notes` (Text)
- `company_id` (Many2one: res.company)

**Model fields for `subscription.invoice.line`**:
- `invoice_id` (Many2one: subscription.invoice)
- `product_id` (Many2one: subscription.product)
- `description` (Char)
- `quantity` (Float)
- `unit_price` (Monetary)
- `discount` (Float)
- `tax_id` (Many2one: subscription.tax)
- `subtotal` (Monetary, computed)

## Prompt for Antigravity

```
Create the file `views/invoice_views.xml` for the Odoo 18 module `subscription_mgmt`. This file defines all views for `subscription.invoice`.

## Odoo 18 Rules
- Use `invisible="expression"` NOT `attrs` (deprecated)
- Root element: `<odoo>`
- Use `widget="badge"` with `decoration-*` for state display

## Views to Create

### 1. Invoice List View (`view_subscription_invoice_list`)
Model: `subscription.invoice`

```xml
<record id="view_subscription_invoice_list" model="ir.ui.view">
    <field name="name">subscription.invoice.list</field>
    <field name="model">subscription.invoice</field>
    <field name="arch" type="xml">
        <list default_order="invoice_date desc"
              decoration-danger="state == 'overdue'"
              decoration-success="state == 'paid'"
              decoration-info="state == 'confirmed'"
              decoration-muted="state == 'cancelled'">
            <field name="name"/>
            <field name="partner_id"/>
            <field name="subscription_id" optional="show"/>
            <field name="invoice_date"/>
            <field name="due_date"/>
            <field name="total_amount" widget="monetary" sum="Total"/>
            <field name="amount_paid" widget="monetary" sum="Paid" optional="show"/>
            <field name="amount_due" widget="monetary" sum="Due"/>
            <field name="currency_id" column_invisible="1"/>
            <field name="state" widget="badge"
                   decoration-danger="state == 'overdue'"
                   decoration-success="state == 'paid'"
                   decoration-info="state == 'confirmed'"
                   decoration-muted="state == 'cancelled'"
                   decoration-warning="state == 'draft'"/>
        </list>
    </field>
</record>
```

### 2. Invoice Form View (`view_subscription_invoice_form`)
Model: `subscription.invoice`

Create a detailed form with:

**Header:**
- Button "Confirm" (btn-primary) — visible only in draft state, calls `action_confirm`
- Button "Register Payment" (btn-primary) — visible in confirmed/overdue state, calls `action_register_payment` (opens wizard)
- Button "Cancel" (btn-danger) — visible in draft/confirmed state, calls `action_cancel`
- Button "Set to Draft" — visible in cancelled state, calls `action_draft`
- Status bar widget showing: draft, confirmed, paid

**Sheet:**
- Ribbon "OVERDUE" (red) when state is overdue
- Ribbon "CANCELLED" when state is cancelled
- Title section with invoice name (readonly)
- Two-column group:
  - Left: `partner_id`, `subscription_id`, `company_id`
  - Right: `invoice_date`, `due_date`, `currency_id`
- Notebook:
  - Page "Invoice Lines":
    - `invoice_line_ids` in editable list: `product_id`, `description`, `quantity`, `unit_price` (monetary), `discount`, `tax_id`, `subtotal` (monetary, readonly, sum)
    - Below the lines: subtotal footer showing `subtotal`, `tax_amount`, `total_amount` (separator), `amount_paid`, `amount_due` (bold)
  - Page "Payments":
    - `payment_ids` readonly list: `name` or date, `amount`, `payment_method`, `payment_date`
  - Page "Notes":
    - `notes` text field

**Chatter:**
- `message_follower_ids`, `activity_ids`, `message_ids`

### 3. Invoice Search View (`view_subscription_invoice_search`)
Model: `subscription.invoice`

- Search fields: `name`, `partner_id`, `subscription_id`
- Filters:
  - "Draft" → state = draft
  - "Confirmed" → state = confirmed
  - "Paid" → state = paid
  - "Overdue" → state = overdue
  - separator
  - "This Month" → invoice_date in current month
  - "This Quarter" → invoice_date in current quarter
  - separator
  - "Cancelled" → state = cancelled
- Group by: State, Customer, Subscription, Invoice Month (`invoice_date:month`)

## File Path
`views/invoice_views.xml`

Do NOT include menu items or actions — those are in `views/menu.xml`.
```

## Expected Output
- **File**: `views/invoice_views.xml`
- Contains: 3 `ir.ui.view` records (list, form, search)

## Verification
1. Add `'views/invoice_views.xml'` to `__manifest__.py` `'data'` list
2. Upgrade module
3. Navigate to Billing → Invoices
4. List view: rows color-coded by state, badges on state column
5. Open an invoice:
   - Draft: shows Confirm and Cancel buttons
   - Confirmed: shows Register Payment button
   - Paid: no action buttons, green status
   - Overdue: red OVERDUE ribbon
6. Check invoice lines are editable with subtotal footer
7. Test search filters and group by options
