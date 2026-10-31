# Prem's Setup Guide — Frontend, Views & UX Lead

## Your Role
You are the **Frontend, Views & UX Lead** for the Subscription Management System. You own ALL XML views, menus, actions, the customer portal, the finance dashboard, wizards, reports, and frontend styling. Your work is what makes the system usable.

---

## 1. Prerequisites & Environment

### Tools
- **Odoo 18** Community/Enterprise (Python 3.10+, PostgreSQL 15+)
- **Git** for version control
- **VS Code** (or your editor) + Odoo extension
- **Antigravity** AI coding assistant — you will paste prompts from the `.md` files into it

### Git Workflow
```bash
cd "E:\odoo hack 2"
git checkout -b prem/frontend-views
# After completing each .md file's prompt:
git add .
git commit -m "feat(views): <short description of what you added>"
```

Commit after every file. This keeps changes atomic and merge-friendly.

---

## 2. Understanding Odoo 18 XML Views

### View Types
| View Type | Purpose | Key Element |
|-----------|---------|------------|
| **Tree/List** | Tabular list of records | `<list>` (Odoo 18) or `<tree>` |
| **Form** | Detailed single-record editing | `<form>` |
| **Kanban** | Card-based grouped view | `<kanban>` |
| **Search** | Filters, search fields, group-by | `<search>` |
| **Graph** | Charts and graphs | `<graph>` |
| **Pivot** | Pivot table | `<pivot>` |
| **Dashboard** | KPI dashboard | OWL component + `ir.actions.client` |

### XML Record Structure
Every view is an `ir.ui.view` record:
```xml
<record id="unique_xml_id" model="ir.ui.view">
    <field name="name">human.readable.name</field>
    <field name="model">module.model_name</field>
    <field name="arch" type="xml">
        <!-- View definition here -->
    </field>
</record>
```

### Window Actions
```xml
<record id="action_xml_id" model="ir.actions.act_window">
    <field name="name">Display Name</field>
    <field name="res_model">module.model_name</field>
    <field name="view_mode">list,form,kanban</field>
</record>
```

### Menu Items
```xml
<menuitem id="menu_xml_id"
          name="Menu Label"
          parent="parent_menu_id"
          action="action_xml_id"
          sequence="10"/>
```

---

## 3. Odoo 18 Key Conventions

### Form View Layout
```xml
<form>
    <header>
        <!-- Status bar and action buttons -->
        <button name="action_confirm" type="object" string="Confirm"
                class="btn-primary" invisible="state != 'draft'"/>
        <field name="state" widget="statusbar"
               statusbar_visible="draft,confirmed,active"/>
    </header>
    <sheet>
        <group>
            <group><!-- Left column fields --></group>
            <group><!-- Right column fields --></group>
        </group>
        <notebook>
            <page string="Tab Name">
                <!-- Content -->
            </page>
        </notebook>
    </sheet>
    <div class="oe_chatter">
        <field name="message_follower_ids"/>
        <field name="message_ids"/>
    </div>
</form>
```

### Decorations (Conditional Styling in Tree/List)
```xml
<list decoration-danger="state == 'closed'"
      decoration-success="state == 'active'"
      decoration-info="state == 'confirmed'">
```

### Invisible/Readonly Conditions (Odoo 18 — no attrs!)
In Odoo 18, use direct attributes:
```xml
<field name="field" invisible="state != 'draft'"/>
<button name="action" invisible="state != 'draft'"/>
```
**Do NOT use `attrs={}` — that is deprecated in Odoo 18.**

---

## 4. View Inheritance

### Extending Existing Views
```xml
<record id="inherited_view_id" model="ir.ui.view">
    <field name="name">extension.name</field>
    <field name="model">original.model</field>
    <field name="inherit_id" ref="original_module.original_view_id"/>
    <field name="arch" type="xml">
        <xpath expr="//field[@name='existing_field']" position="after">
            <field name="new_field"/>
        </xpath>
    </field>
</record>
```

### Portal Inheritance
Portal pages inherit `portal.portal`:
```xml
<template id="portal_my_home_subscription" name="Subscriptions"
          inherit_id="portal.portal_my_home" priority="30">
    <xpath expr="//div[hasclass('o_portal_docs')]" position="inside">
        <!-- Add link here -->
    </xpath>
</template>
```

---

## 5. OWL (Odoo Web Library) Basics

OWL is Odoo 18's frontend framework (similar to React/Vue).

### Component Structure
```javascript
/** @odoo-module **/
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class MyDashboard extends Component {
    static template = "subscription_mgmt.Dashboard";
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
    }
}
registry.category("actions").add("subscription_dashboard", MyDashboard);
```

### OWL Template (XML)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <t t-name="subscription_mgmt.Dashboard">
        <div class="o_dashboard">
            <h1>Dashboard</h1>
        </div>
    </t>
</templates>
```

---

## 6. Portal Development

### Controller Pattern
```python
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

class SubscriptionPortal(CustomerPortal):
    @route(['/my/subscriptions'], type='http', auth='user', website=True)
    def portal_my_subscriptions(self, **kw):
        subscriptions = request.env['subscription.subscription'].search([
            ('partner_id', '=', request.env.user.partner_id.id)
        ])
        return request.render('subscription_mgmt.portal_subscriptions', {
            'subscriptions': subscriptions,
        })
```

### QWeb Template for Portal
```xml
<template id="portal_subscriptions" name="My Subscriptions">
    <t t-call="portal.portal_layout">
        <h3>My Subscriptions</h3>
        <t t-foreach="subscriptions" t-as="sub">
            <!-- Render each subscription -->
        </t>
    </t>
</template>
```

---

## 7. QWeb Reports

### Report Action
```xml
<record id="action_report_invoice" model="ir.actions.report">
    <field name="name">Invoice</field>
    <field name="model">subscription.invoice</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">subscription_mgmt.report_invoice_document</field>
    <field name="report_file">subscription_mgmt.report_invoice_document</field>
    <field name="binding_model_id" ref="model_subscription_invoice"/>
    <field name="binding_type">report</field>
</record>
```

### Report Template
```xml
<template id="report_invoice_document">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="doc">
            <t t-call="web.external_layout">
                <!-- Invoice content here -->
            </t>
        </t>
    </t>
</template>
```

---

## 8. File Structure You Will Create

```
subscription_mgmt/
├── views/
│   ├── menu.xml                        # 01
│   ├── product_views.xml               # 02
│   ├── plan_views.xml                  # 03
│   ├── subscription_views.xml          # 04, 05, 06
│   ├── invoice_views.xml               # 07
│   ├── payment_views.xml               # 08
│   ├── discount_views.xml              # 09
│   ├── tax_views.xml                   # 10
│   ├── quotation_template_views.xml    # 11
│   ├── portal_templates.xml            # 13, 14
│   ├── dashboard.xml                   # 15
├── controllers/
│   ├── __init__.py
│   ├── portal.py                       # 12
├── wizard/
│   ├── __init__.py
│   ├── payment_wizard.py               # 19
│   ├── payment_wizard_views.xml        # 19
├── reports/
│   ├── invoice_report.xml              # 17
│   ├── subscription_report.xml         # 18
├── static/
│   ├── src/
│   │   ├── js/
│   │   │   └── dashboard.js            # 15, 16
│   │   ├── xml/
│   │   │   └── dashboard.xml           # 15, 16
│   │   └── scss/
│   │       └── subscription.scss       # 20
```

---

## 9. Execution Order

Work through the files **in order** (01 → 20). Each file builds on the previous:

1. **01** — Menus first (skeleton)
2. **02–06** — Core model views (products, plans, subscriptions)
3. **07–11** — Supporting model views (invoices, payments, discounts, taxes, quotations)
4. **12–14** — Portal (controller + templates)
5. **15–16** — Dashboard (OWL + charts)
6. **17–18** — Reports (printable PDFs)
7. **19** — Wizard (payment registration)
8. **20** — Styling & assets

---

## 10. How to Use Each .md File

1. Open the `.md` file
2. Find the **"## Prompt for Antigravity"** section
3. Copy the entire prompt text
4. Paste it into Antigravity
5. Review the generated code
6. Place the files in the correct module path
7. Run: `git add . && git commit -m "feat(views): <description>"`
8. Move to the next file

---

## 11. Testing Your Views

After adding each XML file:
1. Add it to `__manifest__.py` under `'data'` (or `'assets'` for static files)
2. Restart Odoo: `python odoo-bin -u subscription_mgmt -d your_db`
3. Check the browser — navigate to the menu/view
4. Look at the Odoo server logs for XML parsing errors

### Common Errors
| Error | Fix |
|-------|-----|
| `ParseError: ... not well-formed` | Check XML syntax — missing closing tags |
| `View not found` | Ensure XML ID matches, file is in `__manifest__.py` |
| `Access Denied` | Check `groups` attribute on menus/actions |
| `KeyError: 'field_name'` | The model field doesn't exist yet — coordinate with backend dev |

---

> **Remember**: You depend on the **backend models** created by Adithya. If a model or field doesn't exist yet, coordinate. Your views reference model fields — they must match exactly.

Good luck, Prem! 🚀
