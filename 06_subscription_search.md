# 06 — Subscription Search View

## Context
This is PART 3 of the subscription views — the **search view**. This enables filtering, searching, and grouping subscriptions. Key filters include "My Subscriptions" (assigned to current user), "Active", "Expiring Soon" (within 30 days), and "Expired". Group-by options let managers analyze by state, plan, customer, or month.

**Depends on**: `subscription.subscription` model, views from `04` and `05`.

## Prompt for Antigravity

```
APPEND to the existing file `views/subscription_views.xml` in the Odoo 18 module `subscription_mgmt`. Add the SEARCH VIEW for `subscription.subscription`. Append this INSIDE the `<odoo>` tags (before `</odoo>`).

## Odoo 18 Conventions
- Use standard `<search>` view syntax
- `<filter>` elements with `name`, `string`, `domain`, and optionally `date` attributes
- Root element already exists (`<odoo>`) — just add the new record

## Search View to Create

### Subscription Search View (`view_subscription_search`)
Model: `subscription.subscription`

```xml
<record id="view_subscription_search" model="ir.ui.view">
    <field name="name">subscription.subscription.search</field>
    <field name="model">subscription.subscription</field>
    <field name="arch" type="xml">
        <search string="Search Subscriptions">
            <!-- Search Fields -->
            <field name="name" string="Reference"/>
            <field name="partner_id" string="Customer"
                   filter_domain="[('partner_id', 'ilike', self)]"/>
            <field name="plan_id" string="Plan"/>

            <!-- Separator -->
            <separator/>

            <!-- My Records Filter -->
            <filter name="my_subscriptions" string="My Subscriptions"
                    domain="[('create_uid', '=', uid)]"/>

            <separator/>

            <!-- State Filters -->
            <filter name="filter_draft" string="Draft"
                    domain="[('state', '=', 'draft')]"/>
            <filter name="filter_confirmed" string="Confirmed"
                    domain="[('state', '=', 'confirmed')]"/>
            <filter name="filter_active" string="Active"
                    domain="[('state', '=', 'active')]"/>
            <filter name="filter_paused" string="Paused"
                    domain="[('state', '=', 'paused')]"/>

            <separator/>

            <!-- Date-based Filters -->
            <filter name="filter_expiring_soon" string="Expiring Soon (30 days)"
                    domain="[('end_date', '&lt;=', (context_today() + datetime.timedelta(days=30)).strftime('%%Y-%%m-%%d')), ('end_date', '&gt;=', context_today().strftime('%%Y-%%m-%%d')), ('state', '=', 'active')]"/>
            <filter name="filter_expired" string="Expired"
                    domain="[('state', '=', 'expired')]"/>
            <filter name="filter_closed" string="Closed"
                    domain="[('state', '=', 'closed')]"/>

            <separator/>

            <!-- Date Filter -->
            <filter name="filter_start_date" string="Start Date" date="start_date"/>

            <separator/>

            <!-- Group By -->
            <group expand="0" string="Group By">
                <filter name="group_by_state" string="State"
                        context="{'group_by': 'state'}"/>
                <filter name="group_by_plan" string="Plan"
                        context="{'group_by': 'plan_id'}"/>
                <filter name="group_by_customer" string="Customer"
                        context="{'group_by': 'partner_id'}"/>
                <filter name="group_by_start_month" string="Start Month"
                        context="{'group_by': 'start_date:month'}"/>
                <filter name="group_by_end_month" string="End Month"
                        context="{'group_by': 'end_date:month'}"/>
            </group>
        </search>
    </field>
</record>
```

## Notes
- The "Expiring Soon" filter uses `context_today()` plus 30 days to find subscriptions ending within a month
- The date filter on `start_date` enables the date range picker in the search bar
- Group by options let users analyze subscriptions by various dimensions
- Make sure `<separator/>` elements separate logical filter groups

## File Path
APPEND to `views/subscription_views.xml`
```

## Expected Output
- **File**: `views/subscription_views.xml` (now has all 4 views: list, kanban, form, search)

## Verification
1. Upgrade module
2. Navigate to Subscriptions
3. Search bar should show autocomplete for Customer, Plan, Reference
4. Click "Filters" dropdown — should show: My Subscriptions, Draft, Confirmed, Active, Paused, Expiring Soon, Expired, Closed
5. Click "Group By" — should show: State, Plan, Customer, Start Month, End Month
6. Apply "Active" filter → only active subscriptions shown
7. Apply "Group By → State" → list groups into state sections
8. Test "Expiring Soon" filter — should show active subscriptions with end_date within 30 days
