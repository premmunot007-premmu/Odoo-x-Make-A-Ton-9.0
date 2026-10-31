# 00 — Neeraj Setup Guide: Backend Architect & Core Engine

> **Role:** Backend Architect & Core Engine Lead  
> **Module:** `subscription_management`  
> **Branch:** `neeraj/backend-core`  
> **Odoo Version:** 18.0  

---

## 1. Prerequisites

### 1.1 Install Python 3.10+
- Download from https://www.python.org/downloads/
- During install, **check "Add Python to PATH"**
- Verify: `python --version`

### 1.2 Install PostgreSQL 15+
1. Download from https://www.postgresql.org/download/windows/
2. Install with default settings. Remember the superuser password.
3. Create an Odoo database user:
```sql
-- Open pgAdmin or psql
CREATE USER odoo WITH PASSWORD 'odoo' CREATEDB;
```

### 1.3 Install Git
- Download from https://git-scm.com/download/win
- Verify: `git --version`

---

## 2. Odoo 18 Setup

### 2.1 Clone Odoo 18
```bash
cd E:\
git clone https://github.com/odoo/odoo.git --depth 1 --branch 18.0 odoo18
```

### 2.2 Create a Python Virtual Environment
```bash
cd E:\odoo18
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2.3 Create the Odoo Configuration File
Create `E:\odoo18\odoo.conf`:
```ini
[options]
admin_passwd = admin
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
db_name = subscription_db
addons_path = E:\odoo18\addons,E:\odoo18\custom_addons
default_productivity_apps = True
```

### 2.4 Create Custom Addons Folder
```bash
mkdir E:\odoo18\custom_addons
```

### 2.5 Start Odoo (first run — creates database)
```bash
cd E:\odoo18
venv\Scripts\activate
python odoo-bin -c odoo.conf -d subscription_db -i base
```
- Open http://localhost:8069 and log in with `admin` / `admin`.

---

## 3. Module Development Workspace

### 3.1 Module Location
All your generated code goes into:
```
E:\odoo18\custom_addons\subscription_management\
```

### 3.2 Folder Structure (created progressively by the prompts)
```
subscription_management/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── product.py
│   ├── plan.py
│   ├── subscription.py
│   ├── subscription_line.py
│   ├── quotation_template.py
│   ├── invoice.py
│   ├── invoice_line.py
│   ├── tax.py
│   ├── discount.py
│   └── payment.py
├── security/
│   ├── subscription_security.xml
│   ├── ir.model.access.csv
│   └── subscription_record_rules.xml
├── data/
│   ├── sequences.xml
│   ├── cron.xml
│   └── mail_templates.xml
└── views/
    └── (handled by frontend team)
```

---

## 4. Git Workflow

### 4.1 Initial Setup
```bash
cd E:\odoo18\custom_addons\subscription_management
git init
git checkout -b neeraj/backend-core
```

### 4.2 After Each File/Prompt
```bash
git add .
git commit -m "feat: <description of what was added>"
```

Example commit messages:
```
feat: module scaffold and manifest
feat: product model and variants
feat: subscription plan model
feat: subscription model with state machine
feat: invoice model and lines
feat: tax and discount rules
feat: payment model
feat: security groups, access rules, record rules
feat: sequences and cron jobs
feat: billing automation
feat: computed fields and constraints
feat: mail integration and templates
feat: final init imports and cleanup
```

### 4.3 Push to Remote (if using GitHub/GitLab)
```bash
git remote add origin <your-repo-url>
git push -u origin neeraj/backend-core
```

---

## 5. How to Use Antigravity with These Prompts

### Step-by-Step Process:

1. **Open Antigravity** (your AI coding assistant).
2. **Open the first prompt file** (`01_module_scaffold.md`).
3. **Copy the content inside the "Prompt for Antigravity" section**.
4. **Paste it into Antigravity** and let it generate the code.
5. **Save the generated files** to the correct location under `E:\odoo18\custom_addons\subscription_management\`.
6. **Run verification** as described in the "Verification" section.
7. **Commit your changes** with git.
8. **Move to the next prompt file** and repeat.

### Important Tips:
- **Go in order** — files 01 through 20 build on each other.
- **After file 01**, restart Odoo with `-u subscription_management` to install the module.
- **After each model file**, restart Odoo with:
  ```bash
  python odoo-bin -c odoo.conf -d subscription_db -u subscription_management
  ```
- **Check the Odoo log** for errors. Fix any before moving on.
- If Antigravity misses something, ask it to fix the specific error.

---

## 6. Testing & Verification

### 6.1 Module Installation Test
```bash
python odoo-bin -c odoo.conf -d subscription_db -i subscription_management
```
No errors = success.

### 6.2 Quick Smoke Test (after all files)
1. Log into Odoo → Settings → Activate Developer Mode.
2. Go to Settings → Technical → Database Structure → Models.
3. Search for `subscription.` — you should see all your models.
4. Create test records: Product → Plan → Subscription → Invoice → Payment.

### 6.3 Security Test
1. Create a Staff user — assign `Subscription Staff` group.
2. Create a Portal user — assign `Subscription Customer` group.
3. Log in as each and verify access restrictions.

---

## 7. Prompt Execution Order

| # | File | What It Creates |
|---|------|----------------|
| 01 | `01_module_scaffold.md` | `__manifest__.py`, `__init__.py` |
| 02 | `02_product_model.md` | `models/product.py` (product + variants) |
| 03 | `03_plan_model.md` | `models/plan.py` (plan + plan lines) |
| 04 | `04_subscription_model.md` | `models/subscription.py` |
| 05 | `05_subscription_line_model.md` | `models/subscription_line.py` |
| 06 | `06_quotation_template_model.md` | `models/quotation_template.py` |
| 07 | `07_invoice_model.md` | `models/invoice.py` |
| 08 | `08_invoice_line_model.md` | `models/invoice_line.py` |
| 09 | `09_tax_model.md` | `models/tax.py` |
| 10 | `10_discount_model.md` | `models/discount.py` |
| 11 | `11_payment_model.md` | `models/payment.py` |
| 12 | `12_security_groups.md` | `security/subscription_security.xml` |
| 13 | `13_access_rules.md` | `security/ir.model.access.csv` |
| 14 | `14_record_rules.md` | `security/subscription_record_rules.xml` |
| 15 | `15_sequences.md` | `data/sequences.xml` |
| 16 | `16_cron_jobs.md` | `data/cron.xml` |
| 17 | `17_billing_automation.md` | Billing method in subscription model |
| 18 | `18_computed_fields_constraints.md` | SQL/Python constraints, computed fields |
| 19 | `19_mail_integration.md` | mail.thread, email templates |
| 20 | `20_init_imports.md` | All `__init__.py` files finalized |

---

## 8. Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Check `__init__.py` imports match file names |
| `KeyError: 'subscription.product'` | Model file not imported. Check `models/__init__.py` |
| `Access Denied` | Check `ir.model.access.csv` has the model entry |
| `Column not found` | Run with `-u subscription_management` to update DB |
| `Duplicate key` | Drop the DB and recreate: `dropdb subscription_db && createdb subscription_db` |
| Port 8069 in use | Kill existing Odoo process or use `--http-port 8070` |

---

**You're all set! Start with `01_module_scaffold.md` and work through each file in order. Good luck at the hackathon! 🚀**
