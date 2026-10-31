# Product & Plan Views

## Context
Tree, form, kanban, and search views for Products (with variant management) and Plans (with inline plan lines).

## Prompt for Claude Code

```
In the Odoo 18 module "subscription_management", create all views for Product and Plan models.

Create `views/product_views.xml`:
- Tree view: columns — name, product_type, sales_price, cost_price, variant_count, is_active
- Form view:
  - Header area (no buttons needed)
  - Sheet with:
    - div for image (widget="image") on right
    - group with name, product_type, sales_price, cost_price, is_active
    - notebook:
      - tab "Variants": one2many tree for variant_ids (editable="bottom") — variant_name, variant_value, price_extra
      - tab "Description": notes field (Html widget)
  - Chatter: message_follower_ids, message_ids, activity_ids
- Kanban view: card showing image, name, product_type badge, sales_price
- Search view: search by name, filter by product_type, filter active/archived, group by product_type

Create `views/plan_views.xml`:
- Tree view: name, billing_frequency, min_quantity, date_start, date_end, auto_close, is_active
- Form view:
  - group: name, billing_frequency, min_quantity
  - group: date_start, date_end
  - group: auto_close, allow_early_close, allow_pause, allow_renew
  - notebook:
    - tab "Default Products": one2many inline tree for plan_line_ids (editable="bottom") — product_id, default_qty, default_price
    - tab "Description": description field
- Search view: search by name, filter by billing_frequency, group by billing_frequency

Use Odoo 18 XML conventions. Use proper field widgets: widget="badge" for selections, widget="many2many_tags" where appropriate.
Update __manifest__.py to include 'views/product_views.xml' and 'views/plan_views.xml'.
```

## Expected Output
- `views/product_views.xml`
- `views/plan_views.xml`

## Verification
- Navigate to Products menu, verify tree/form/kanban/search all work
- Navigate to Plans menu, verify inline plan lines work
