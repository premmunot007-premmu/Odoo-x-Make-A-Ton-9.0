# 01 — Menu Structure

## Context
This is the **first view file** to create. It defines the entire navigation hierarchy for the Subscription Management module. All other view files will reference these menu items as parents. The menus use `groups` to control visibility — admin sees everything, staff sees operational menus, customers use the portal (separate).

**Depends on**: The module `__manifest__.py` and security groups defined by the backend lead.

## Prompt for Antigravity

```
Create the file `views/menu.xml` for an Odoo 18 custom module called `subscription_mgmt`. This file defines the complete menu structure for the Subscription Management System.

## Module Technical Name
`subscription_mgmt`

## Security Groups (already defined elsewhere)
- `subscription_mgmt.group_subscription_user` — Staff users
- `subscription_mgmt.group_subscription_manager` — Admin/Manager users

## Menu Hierarchy

### Top-Level Menu
- XML ID: `menu_subscription_root`
- Name: "Subscription Management"
- Icon: use web_icon if needed
- Sequence: 10
- Groups: `group_subscription_user` (so both user and manager see it)

### Sub-Menus (direct children of root):

1. **Subscriptions** (`menu_subscription_main`)
   - Sequence: 10
   - Action: `action_subscription_list` (ir.actions.act_window for `subscription.subscription`, view_mode: list,form,kanban)

2. **Products & Plans** (`menu_products_plans`)
   - Sequence: 20
   - This is a PARENT menu (no action), with children:
     - **Products** (`menu_products`) → Action: `action_product_list` (for `subscription.product`, view_mode: list,form,kanban)  — Sequence 10
     - **Product Variants** (`menu_product_variants`) → Action: `action_product_variant_list` (for `subscription.product.variant`, view_mode: list,form) — Sequence 20
     - **Plans** (`menu_plans`) → Action: `action_plan_list` (for `subscription.plan`, view_mode: list,form) — Sequence 30

3. **Billing** (`menu_billing`)
   - Sequence: 30
   - Parent menu with children:
     - **Invoices** (`menu_invoices`) → Action: `action_invoice_list` (for `subscription.invoice`, view_mode: list,form) — Sequence 10
     - **Payments** (`menu_payments`) → Action: `action_payment_list` (for `subscription.payment`, view_mode: list,form) — Sequence 20

4. **Discounts & Taxes** (`menu_discounts_taxes`)
   - Sequence: 40
   - Parent menu with children:
     - **Discount Rules** (`menu_discounts`) → Action: `action_discount_list` (for `subscription.discount`, view_mode: list,form) — Sequence 10
     - **Tax Rules** (`menu_taxes`) → Action: `action_tax_list` (for `subscription.tax`, view_mode: list,form) — Sequence 20

5. **Configuration** (`menu_configuration`)
   - Sequence: 50
   - Groups: `subscription_mgmt.group_subscription_manager` (manager only)
   - Parent menu with children:
     - **Quotation Templates** (`menu_quotation_templates`) → Action: `action_quotation_template_list` (for `subscription.quotation.template`, view_mode: list,form) — Sequence 10

6. **Dashboard** (`menu_dashboard`)
   - Sequence: 1 (appears first!)
   - Action: `action_subscription_dashboard` (ir.actions.client, tag: `subscription_dashboard`)
   - Groups: `subscription_mgmt.group_subscription_manager`

## Requirements
- Use `<odoo>` as root element (Odoo 18 standard)
- Define ALL `ir.actions.act_window` records BEFORE the menu items that reference them
- Define the `ir.actions.client` action for the dashboard
- Use proper `groups` attributes
- Each action should have a sensible `name`, `res_model`, `view_mode`
- Add `help` attribute to actions with a friendly empty-state message wrapped in `<p class="o_view_nocontent_smiling_face">`
- All XML IDs must be prefixed appropriately (no module prefix needed inside the same module)
- Use `noupdate="0"` or no noupdate (data that should update on upgrade)
- The file should be valid, standalone XML

## File Path
`views/menu.xml`
```

## Expected Output
- **File**: `views/menu.xml`
- Contains: ~7 `ir.actions.act_window` records, 1 `ir.actions.client` record, ~12 `menuitem` elements

## Verification
1. Add `'views/menu.xml'` to `__manifest__.py` `'data'` list (should be LAST in the list, after all view files)
2. Upgrade module: `python odoo-bin -u subscription_mgmt -d your_db`
3. Refresh browser — you should see "Subscription Management" in the top menu bar
4. Click it — sub-menus should appear (views will be auto-generated defaults until we create custom views)
5. Check Odoo logs for any XML errors
