# User Role Setup

## Context

We are building a **Subscription Management System** as an Odoo 18 custom module (`subscription_management`). This file creates the user role definitions, default admin configuration, portal user template, and group assignment logic.

The system has 3 roles:
1. **Admin** (`base.group_system`) — Full access to everything. Can create staff. Manages all subscriptions, products, billing.
2. **Staff** (`base.group_user`) — Internal user. Can manage subscriptions, view reports, but cannot change settings or create other staff.
3. **Customer** (`base.group_portal`) — Portal user. Can only view their own subscriptions, invoices, and payments.

### Related files:
- `security/ir.model.access.csv` — Model-level access per group
- `security/security_rules.xml` — Record rules per group
- `models/res_users.py` — User model extensions
- `__manifest__.py` — Must reference this data file

---

## Prompt for Antigravity

```
Create the file `data/user_roles.xml` for an Odoo 18 custom module named `subscription_management`.

This file defines the user role configuration, custom groups, and default user setup for a Subscription Management System.

### Requirements:

1. **File location:** `data/user_roles.xml`

2. **XML structure:**
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <odoo>
       <data noupdate="0">
           <!-- Group categories and groups -->
       </data>
       <data noupdate="1">
           <!-- Default users (noupdate so they aren't reset on upgrade) -->
       </data>
   </odoo>
   ```

3. **Create a module-specific group category:**
   ```xml
   <record id="module_category_subscription_management" model="ir.module.category">
       <field name="name">Subscription Management</field>
       <field name="description">Groups for Brightloop Subscription Management System</field>
       <field name="sequence">10</field>
   </record>
   ```

4. **Create custom groups** (these add module-specific permissions on top of Odoo's base groups):

   a. **Subscription Customer group:**
   ```xml
   <record id="group_subscription_customer" model="res.groups">
       <field name="name">Customer</field>
       <field name="category_id" ref="module_category_subscription_management"/>
       <field name="implied_ids" eval="[(4, ref('base.group_portal'))]"/>
       <field name="comment">Portal customers who can view their own subscriptions and invoices.</field>
   </record>
   ```

   b. **Subscription Staff group:**
   ```xml
   <record id="group_subscription_staff" model="res.groups">
       <field name="name">Staff</field>
       <field name="category_id" ref="module_category_subscription_management"/>
       <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
       <field name="comment">Staff members who manage subscriptions, view reports, handle customer issues.</field>
   </record>
   ```

   c. **Subscription Admin group:**
   ```xml
   <record id="group_subscription_admin" model="res.groups">
       <field name="name">Administrator</field>
       <field name="category_id" ref="module_category_subscription_management"/>
       <field name="implied_ids" eval="[(4, ref('subscription_management.group_subscription_staff'))]"/>
       <field name="comment">Full access administrators. Can manage users, settings, all data.</field>
   </record>
   ```
   
   Note: Admin implies Staff, so admins automatically get staff permissions.

5. **Create default admin user configuration:**
   ```xml
   <!-- Assign the subscription admin group to the default admin user -->
   <record id="base.user_admin" model="res.users">
       <field name="groups_id" eval="[(4, ref('subscription_management.group_subscription_admin'))]"/>
   </record>
   ```

6. **Create a method in `models/res_users.py` to assign roles on signup:**
   
   Add this method to the existing `ResUsers` class:
   ```python
   @api.model
   def _assign_subscription_role(self, user, role='customer'):
       """
       Assign subscription management role to a user.
       
       Args:
           user: res.users record
           role: 'customer', 'staff', or 'admin'
       """
       role_map = {
           'customer': self.env.ref('subscription_management.group_subscription_customer'),
           'staff': self.env.ref('subscription_management.group_subscription_staff'),
           'admin': self.env.ref('subscription_management.group_subscription_admin'),
       }
       group = role_map.get(role)
       if group:
           user.sudo().write({
               'groups_id': [(4, group.id)]
           })
   
   def get_subscription_role(self):
       """Return the user's subscription management role as a string."""
       self.ensure_one()
       if self.has_group('subscription_management.group_subscription_admin'):
           return 'admin'
       elif self.has_group('subscription_management.group_subscription_staff'):
           return 'staff'
       elif self.has_group('subscription_management.group_subscription_customer'):
           return 'customer'
       return 'none'
   ```

7. **Also create `security/ir.model.access.csv`** with access rights for each group:

   ```csv
   id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
   access_product_customer,subscription.product.customer,model_subscription_product,subscription_management.group_subscription_customer,1,0,0,0
   access_product_staff,subscription.product.staff,model_subscription_product,subscription_management.group_subscription_staff,1,1,1,0
   access_product_admin,subscription.product.admin,model_subscription_product,subscription_management.group_subscription_admin,1,1,1,1
   access_plan_customer,subscription.plan.customer,model_subscription_plan,subscription_management.group_subscription_customer,1,0,0,0
   access_plan_staff,subscription.plan.staff,model_subscription_plan,subscription_management.group_subscription_staff,1,1,1,0
   access_plan_admin,subscription.plan.admin,model_subscription_plan,subscription_management.group_subscription_admin,1,1,1,1
   access_subscription_customer,subscription.subscription.customer,model_subscription_subscription,subscription_management.group_subscription_customer,1,0,0,0
   access_subscription_staff,subscription.subscription.staff,model_subscription_subscription,subscription_management.group_subscription_staff,1,1,1,0
   access_subscription_admin,subscription.subscription.admin,model_subscription_subscription,subscription_management.group_subscription_admin,1,1,1,1
   access_invoice_customer,subscription.invoice.customer,model_subscription_invoice,subscription_management.group_subscription_customer,1,0,0,0
   access_invoice_staff,subscription.invoice.staff,model_subscription_invoice,subscription_management.group_subscription_staff,1,1,1,0
   access_invoice_admin,subscription.invoice.admin,model_subscription_invoice,subscription_management.group_subscription_admin,1,1,1,1
   access_payment_customer,subscription.payment.customer,model_subscription_payment,subscription_management.group_subscription_customer,1,0,0,0
   access_payment_staff,subscription.payment.staff,model_subscription_payment,subscription_management.group_subscription_staff,1,1,1,0
   access_payment_admin,subscription.payment.admin,model_subscription_payment,subscription_management.group_subscription_admin,1,1,1,1
   access_discount_customer,subscription.discount.customer,model_subscription_discount,subscription_management.group_subscription_customer,1,0,0,0
   access_discount_staff,subscription.discount.staff,model_subscription_discount,subscription_management.group_subscription_staff,1,1,0,0
   access_discount_admin,subscription.discount.admin,model_subscription_discount,subscription_management.group_subscription_admin,1,1,1,1
   ```

   Note: Adjust `model_id:id` references to match actual model names from your team (e.g., Ajay's product model, Kaushal's invoice model). The model external IDs follow the pattern `model_<model_name_with_underscores>`.

Generate the complete `data/user_roles.xml` file, the role-assignment methods for `models/res_users.py`, and the `security/ir.model.access.csv` file.
```

---

## Expected Output

Three files/additions:

1. **`data/user_roles.xml`** — Group category, 3 custom groups (Customer, Staff, Admin), admin user group assignment
2. **`models/res_users.py`** additions — `_assign_subscription_role()` and `get_subscription_role()` methods
3. **`security/ir.model.access.csv`** — CRUD permissions per model per group

---

## Verification

1. **Group hierarchy** — Admin implies Staff, Customer implies Portal
2. **Category** — Custom category "Subscription Management" created
3. **Admin assignment** — `base.user_admin` gets the subscription admin group
4. **Access CSV** — Customers: read-only, Staff: read/write/create, Admin: full CRUD
5. **Role methods** — `_assign_subscription_role()` correctly maps roles to groups
6. **`get_subscription_role()`** — Returns correct string for each group
7. **XML IDs** — All groups have proper XML IDs for cross-referencing
8. **Install test** — After module install, check Settings → Groups for new groups
