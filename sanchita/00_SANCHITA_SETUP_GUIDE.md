# Sanchita's Setup Guide — Auth, User Management & Testing Lead

## Your Role

You are the **Authentication, User Management, Demo Data & Testing** lead for the **Subscription Management System** Odoo 18 module. Your module technical name is `subscription_management`.

You are responsible for:
- User signup, login, password reset flows
- Password validation rules
- Role-based access (Admin / Staff / Portal Customer)
- Demo/sample data for products, plans, subscriptions, invoices, customers
- Unit tests for ALL models and flows

---

## Understanding Odoo's Auth System

### Key Concepts

1. **`res.users`** — The core user model in Odoo. Every login account is a `res.users` record. Each user has a linked `res.partner` (contact) record.

2. **`res.partner`** — The contact model. Holds name, email, address, company info. A `res.users` record always has a `partner_id` pointing to a `res.partner`.

3. **Groups** — Odoo uses `res.groups` for role-based access:
   - `base.group_system` → Administrator (full access)
   - `base.group_user` → Internal User (staff/employee)
   - `base.group_portal` → Portal User (external customer)
   - `base.group_public` → Public (unauthenticated)

4. **Record Rules** (`ir.rule`) — Define row-level access. Example: "Portal users can only see their own subscriptions."

5. **Access Control Lists** (`ir.model.access`) — Define model-level CRUD permissions per group.

### How Signup Works in Odoo

Odoo has a built-in `/web/signup` but we create a **custom signup** at `/subscription/signup` to:
- Enforce our password policy
- Auto-assign portal group
- Collect extra fields (company name)
- Return JSON for AJAX-friendly usage

### How Portal Users Work

Portal users:
- Log in at `/web/login` or our custom login
- See the portal frontend (not the backend)
- Have record rules limiting them to their own data
- Are created with `groups_id = [(6, 0, [ref('base.group_portal')])]`

---

## Your Git Workflow

```bash
# 1. Clone the repo (if not already)
cd "E:\odoo hack 2"
git clone <repo-url> .

# 2. Create your branch
git checkout -b sanchita/auth-testing

# 3. After creating each file, commit
git add .
git commit -m "feat(auth): add signup controller"

# 4. Push regularly
git push origin sanchita/auth-testing
```

---

## How to Use These Prompt Files

Each `.md` file (01 through 20) contains a **prompt** designed to be pasted directly into **Antigravity** (AI coding assistant).

### Steps:
1. Open the `.md` file (e.g., `01_signup_controller.md`)
2. Find the **"## Prompt for Antigravity"** section
3. Copy the entire prompt text
4. Paste it into Antigravity's chat
5. Review the generated code
6. Place the file in the correct location within your module
7. Test and commit

### Order of Execution:
Follow this recommended order to avoid dependency issues:

**Phase 1: Models & Security (do these first)**
1. `03_password_validation.md` — res.users password validation
2. `08_user_role_setup.md` — User roles & groups
3. `09_portal_user_restrictions.md` — Record rules

**Phase 2: Controllers & Views**
4. `01_signup_controller.md` — Signup controller
5. `02_signup_template.md` — Signup template
6. `04_password_reset.md` — Password reset flow
7. `05_password_reset_template.md` — Reset email template
8. `06_login_controller.md` — Login controller
9. `07_login_template.md` — Login template

**Phase 3: Admin Features**
10. `10_admin_staff_management.md` — Staff management

**Phase 4: Demo Data**
11. `11_demo_products.md`
12. `12_demo_plans.md`
13. `13_demo_customers.md`
14. `14_demo_subscriptions.md`
15. `15_demo_invoices_payments.md`

**Phase 5: Tests**
16. `16_test_product_model.md`
17. `17_test_subscription_lifecycle.md`
18. `18_test_invoice_payment.md`
19. `19_test_discount.md`
20. `20_test_auth.md`

---

## Module File Structure

After completing all prompts, your module should look like this:

```
subscription_management/
├── __init__.py
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── auth.py                      # Signup, login, password reset
├── models/
│   ├── __init__.py
│   └── res_users.py                 # Password validation, user extensions
├── views/
│   └── auth_templates.xml           # Signup, login, reset QWeb templates
├── data/
│   ├── email_templates.xml          # Password reset email
│   ├── user_roles.xml               # Groups, default users
│   └── demo/
│       ├── demo_products.xml
│       ├── demo_plans.xml
│       ├── demo_customers.xml
│       ├── demo_subscriptions.xml
│       ├── demo_invoices.xml
│       └── demo_payments.xml
├── security/
│   ├── ir.model.access.csv
│   └── security_rules.xml           # Record rules for portal users
├── tests/
│   ├── __init__.py
│   ├── test_product.py
│   ├── test_subscription.py
│   ├── test_invoice.py
│   ├── test_discount.py
│   └── test_auth.py
└── static/
    └── src/
        └── css/
            └── auth.css             # Styling for auth pages
```

---

## How to Write Odoo Tests

### Test Class Structure

```python
# tests/test_example.py
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError

@tagged('post_install', '-at_install')
class TestExample(TransactionCase):

    @classmethod
    def setUpClass(cls):
        """Runs once before all test methods."""
        super().setUpClass()
        # Create shared test data
        cls.product = cls.env['subscription.product'].create({
            'name': 'Test Product',
            'list_price': 100.0,
        })

    def test_product_creation(self):
        """Test that product is created correctly."""
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.list_price, 100.0)

    def test_required_field(self):
        """Test that missing required fields raise errors."""
        with self.assertRaises(ValidationError):
            self.env['subscription.product'].create({})
```

### Running Tests

```bash
# Run all tests for the module
python odoo-bin -c odoo.conf -d test_db --test-tags subscription_management -i subscription_management --stop-after-init

# Run a specific test class
python odoo-bin -c odoo.conf -d test_db --test-tags /subscription_management:TestProduct -i subscription_management --stop-after-init

# Run with demo data loaded
python odoo-bin -c odoo.conf -d test_db --test-tags subscription_management -i subscription_management --stop-after-init --without-demo=False
```

### Test Tags

- `@tagged('post_install', '-at_install')` — Runs after module is installed (most common)
- `@tagged('at_install')` — Runs during installation
- `@tagged('-standard', 'custom_tag')` — Custom tag, excluded from standard runs

### Common Test Patterns

```python
# Test constraint violations
with self.assertRaises(ValidationError):
    record.write({'field': 'invalid_value'})

# Test record creation
record = self.env['model.name'].create({...})
self.assertTrue(record.id)

# Test computed fields
self.assertEqual(record.computed_field, expected_value)

# Test state transitions
record.action_confirm()
self.assertEqual(record.state, 'confirmed')

# Test access rights (as different user)
record_as_portal = record.with_user(self.portal_user)
with self.assertRaises(AccessError):
    record_as_portal.unlink()
```

---

## Coordination with Team

- **Rupesh** (Team Lead) defines the `__manifest__.py`, `__init__.py`, and overall module structure
- **Ajay** builds the core subscription, product, plan models — your tests must align with his field names
- **Kaushal** builds invoice, payment, discount, tax models — your tests for those must align with his fields
- **You** build auth flows, demo data, and tests for everything

### Before Writing Tests:
1. Ask teammates for their **model names** and **field names**
2. Check the models they've created in `models/` folder
3. Align your demo data XML IDs so others can reference them

---

## Quick Reference: Odoo 18 Key APIs

```python
# Create record
record = self.env['model.name'].create({'field': 'value'})

# Search
records = self.env['model.name'].search([('field', '=', 'value')])

# Browse by ID
record = self.env['model.name'].browse(record_id)

# Write/update
record.write({'field': 'new_value'})

# Delete
record.unlink()

# Sudo (bypass access rules)
record.sudo().write({...})

# Change user context
record.with_user(user_id).read()

# Reference XML ID
product = self.env.ref('subscription_management.demo_product_crm')
```

---

## Checklist

- [ ] Password validation model (res.users inherit)
- [ ] Signup controller + template
- [ ] Login controller + template
- [ ] Password reset controller + email template
- [ ] User role definitions (groups, record rules)
- [ ] Portal user restrictions (record rules)
- [ ] Admin staff management views
- [ ] Demo products (5-6 records)
- [ ] Demo plans (4-5 records)
- [ ] Demo customers (5-6 records)
- [ ] Demo subscriptions (8-10 records)
- [ ] Demo invoices & payments
- [ ] Test: product model
- [ ] Test: subscription lifecycle
- [ ] Test: invoice & payment
- [ ] Test: discount
- [ ] Test: auth flows
- [ ] All tests passing
- [ ] Code committed and pushed

---

> **Tip:** Run tests frequently as you build. Don't wait until the end!
