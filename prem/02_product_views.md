# 02 — Product Views

## Context
This file creates all views for the `subscription.product` model — the catalog of software products that Brightloop sells as subscriptions. Products have variants (e.g., Basic, Pro, Enterprise tiers). The views need to look polished with images, proper grouping, and a kanban for visual browsing.

**Depends on**: `subscription.product` model (backend), `subscription.product.variant` model for inline variants. Menu items from `01_menu_structure.md`.

**Model fields expected**:
- `name` (Char) — Product name
- `product_code` (Char) — Unique code
- `product_type` (Selection: software/service/bundle) — Type
- `description` (Text) — Description
- `image` (Binary) — Product image
- `base_price` (Float) — Base price
- `cost_price` (Float) — Cost
- `currency_id` (Many2one: res.currency)
- `variant_ids` (One2many: subscription.product.variant)
- `active` (Boolean)
- `tag_ids` (Many2many) if exists

## Prompt for Antigravity

```
Create the file `views/product_views.xml` for an Odoo 18 module called `subscription_mgmt`. This file defines all views for the `subscription.product` model AND the `subscription.product.variant` model.

## IMPORTANT: Odoo 18 Conventions
- Use `invisible="condition"` directly on elements, NOT `attrs="{'invisible': [...]}"` (attrs is deprecated in Odoo 18)
- Use `<list>` tag instead of `<tree>` for list views (Odoo 18 preference, though `<tree>` still works)
- Root element: `<odoo>`

## Views to Create

### 1. Product List View (`view_product_list`)
```xml
Model: subscription.product
Type: list
```
- Columns: `product_code`, `name`, `product_type` (with badge widget), `base_price` (monetary widget), `cost_price` (monetary widget), `currency_id`, `active`
- Decorations: `decoration-muted="not active"`
- Editable: no (click to open form)
- Default order: `name asc`

### 2. Product Form View (`view_product_form`)
```xml
Model: subscription.product
Type: form
```
Layout:
```
<form>
    <sheet>
        <div class="oe_button_box" name="button_box">
            <!-- Stat button for variant count if possible -->
        </div>
        <field name="image" widget="image" class="oe_avatar" options="{'preview_image': 'image'}"/>
        <div class="oe_title">
            <label for="name"/>
            <h1><field name="name" placeholder="Product Name"/></h1>
            <field name="product_code" placeholder="e.g., PROD-001"/>
        </div>
        <group>
            <group string="General">
                <field name="product_type"/>
                <field name="active"/>
            </group>
            <group string="Pricing">
                <field name="base_price" widget="monetary"/>
                <field name="cost_price" widget="monetary"/>
                <field name="currency_id" groups="base.group_multi_currency"/>
            </group>
        </group>
        <notebook>
            <page string="Description" name="description">
                <field name="description" placeholder="Describe this product..."/>
            </page>
            <page string="Variants" name="variants">
                <field name="variant_ids">
                    <list editable="bottom">
                        <field name="name"/>
                        <field name="variant_code"/>
                        <field name="price_extra" widget="monetary"/>
                        <field name="active"/>
                    </list>
                </field>
            </page>
        </notebook>
    </sheet>
</form>
```

### 3. Product Kanban View (`view_product_kanban`)
```xml
Model: subscription.product
Type: kanban
```
- Card shows: image (if any), product name, product_type badge, base_price
- Use `oe_kanban_global_click` for clicking
- Template structure with `kanban-box` class
- Show placeholder if no image

### 4. Product Search View (`view_product_search`)
```xml
Model: subscription.product
Type: search
```
- Search fields: `name`, `product_code`, `product_type`
- Filters: "Software" (product_type=software), "Services" (product_type=service), "Bundles" (product_type=bundle), "Archived" (active=False)
- Group by: `product_type`
- Use `<separator/>` between filter groups

### 5. Product Variant List View (`view_product_variant_list`)
```xml
Model: subscription.product.variant
Type: list
```
- Columns: `name`, `variant_code`, `product_id`, `price_extra`, `active`

### 6. Product Variant Form View (`view_product_variant_form`)
```xml
Model: subscription.product.variant
Type: form
```
- Simple form with all fields in a group layout
- Fields: `name`, `variant_code`, `product_id`, `price_extra`, `description`, `active`

## File Path
`views/product_views.xml`

NOTE: Do NOT include menu items or actions in this file — those are in `views/menu.xml`.
Wrap everything in `<odoo>` root element.
All view xml_ids should be descriptive: e.g., `view_subscription_product_list`, `view_subscription_product_form`, etc.
```

## Expected Output
- **File**: `views/product_views.xml`
- Contains: 6 `ir.ui.view` records (4 for product, 2 for variant)

## Verification
1. Add `'views/product_views.xml'` to `__manifest__.py` `'data'` list (BEFORE `menu.xml`)
2. Upgrade module
3. Navigate to Subscription Management → Products & Plans → Products
4. Check list view shows correct columns with badges and monetary formatting
5. Click a record — form should show image placeholder, grouped fields, notebook tabs
6. Switch to kanban — cards should render with product info
7. Test search filters and group by
