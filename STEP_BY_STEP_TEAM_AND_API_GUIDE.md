# 🌟 Team Step-by-Step Execution, Setup & External Resources / API Guide

This master guide provides the exact step-by-step instructions for **Neeraj, Prem, Divya, and Sanchita** to execute their tasks, configure **Claude Code Pro** and **Antigravity**, generate API keys (Gemini / Anthropic), and ensure **every member's contributions are visible in the GitHub repository**.

---

## 🔑 External Resources & API Setup

### 1. Google Gemini API Key (For Antigravity)
If you or your team use Google Gemini models inside Antigravity:
1. **Visit Google AI Studio**: Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).
2. **Log in** with your Google account.
3. Click **"Create API Key"** (choose or create a Google Cloud project).
4. Copy your generated key (`AIzaSy...`).
5. **Add to Antigravity**:
   - In Antigravity Settings > **API Keys / Providers** > Select **Google Gemini**.
   - Paste the copied key into the API key input field and click **Save**.
   - Alternatively, in your system terminal or `.bashrc` / Windows Environment Variables:
     ```powershell
     [System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'your_key_here', 'User')
     ```

### 2. Claude Code Pro Setup (For Divya)
Divya holds the Claude Code Pro subscription:
1. **Install Claude Code CLI**:
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```
2. **Login / Authenticate**:
   ```bash
   claude
   ```
   Follow the terminal authentication prompt to link your Claude Pro account.
3. **Run Claude Code in your module folder**:
   ```bash
   cd ~/odoo18/custom_addons/subscription_management
   claude
   ```

### 3. Local Odoo 18 & PostgreSQL (Zero-Cost Open Source)
No paid cloud APIs are mandatory for running the core subscription engine; Odoo 18 Community Edition runs locally on PostgreSQL 16.
- **Python 3.10+** (Official Python installer)
- **PostgreSQL 16** (Default user `odoo`, password `odoo`)
- **Odoo 18.0 Community** (Cloned from `https://github.com/odoo/odoo.git --branch 18.0 --depth 1`)

---

## 👥 Step-by-Step Process for Each Member

---

### 🔴 DIVYA (Core Engine — Claude Code Pro) — [HEAVIEST TASK]

Divya builds the core backend models, business logic, security matrices, views, customer portal, OWL dashboard, and PDF reports.

#### Step-by-Step Workflow:
1. **Initialize Git Branch**:
   ```bash
   git checkout -b divya/core-engine
   ```
2. **Open Claude Code**:
   ```bash
   cd ~/odoo18/custom_addons/subscription_management
   claude
   ```
3. **Execute Files 01 to 20 in Order**:
   - Open file `divya/01_module_scaffold.md`.
   - Copy the text under `## Prompt for Claude Code`.
   - Paste it into Claude Code and press Enter.
   - Claude Code will generate the module structure.
   - Verify and commit:
     ```bash
     git add .
     git commit -m "feat(core): scaffold subscription_management module"
     ```
   - Proceed sequentially through files `02_product_model.md` to `20_final_assembly.md`.
4. **Push Branch & Open Pull Request**:
   ```bash
   git push origin divya/core-engine
   ```
   Open a Pull Request on GitHub: `divya/core-engine` ➔ `main`.

---

### 🟡 NEERAJ (Auth, User Management & Business Rules — Antigravity)

Neeraj builds the strong password validator, public signup/login controllers, password reset mechanism, cron automations, and transactional email templates.

#### Step-by-Step Workflow:
1. **Sync with Main & Create Branch**:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b neeraj/auth-business-logic
   ```
2. **Open Antigravity**:
   - Open your project workspace in Antigravity.
   - Ensure your Gemini API key or preferred model is selected.
3. **Execute Files 01 to 20 in Order**:
   - Open `neeraj/08_password_validation.md`.
   - Copy the prompt under `## Prompt for Antigravity`.
   - Paste into Antigravity conversation.
   - Review code modifications in `models/res_users.py`.
   - Commit:
     ```bash
     git add .
     git commit -m "feat(auth): strong password regex and email uniqueness"
     ```
   - Proceed through `09_signup_controller.md` to `20_init_manifest_final.md`.
4. **Push Branch & Open Pull Request**:
   ```bash
   git push origin neeraj/auth-business-logic
   ```
   Open a Pull Request on GitHub: `neeraj/auth-business-logic` ➔ `main`.

---

### 🟡 PREM (Demo Data, Wizards & UX Enhancements — Antigravity)

Prem creates realistic demo datasets (products, plans, customers, subscriptions across all states, invoices, multi-method payments), the payment registration popup wizard, and SCSS styling.

#### Step-by-Step Workflow:
1. **Sync with Main & Create Branch**:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b prem/ux-demo-data
   ```
2. **Open Antigravity**:
   - Open your project in Antigravity.
3. **Execute Files 08 to 20 in Order**:
   - Open `prem/08_demo_products.md`.
   - Copy the prompt under `## Prompt for Antigravity`.
   - Paste into Antigravity to generate `data/demo_products.xml`.
   - Commit:
     ```bash
     git add data/demo_products.xml
     git commit -m "data(demo): add products and variants with Odoo brand fee"
     ```
   - Proceed through `09_demo_plans.md` to `20_asset_registration.md`.
4. **Push Branch & Open Pull Request**:
   ```bash
   git push origin prem/ux-demo-data
   ```
   Open a Pull Request on GitHub: `prem/ux-demo-data` ➔ `main`.

---

### 🟢 SANCHITA (Testing, Docs & Production Deployment — Antigravity)

Sanchita creates the automated unit test suite, comprehensive README, Docker Compose file, user & admin manuals, demo pitch script, and deployment architecture.

#### Step-by-Step Workflow:
1. **Sync with Main & Create Branch**:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b sanchita/tests-docs-devops
   ```
2. **Open Antigravity**:
   - Open your project in Antigravity.
3. **Execute Files 09 to 20 in Order**:
   - Open `sanchita/09_readme.md`.
   - Copy the prompt into Antigravity to generate `README.md`.
   - Commit:
     ```bash
     git add README.md
     git commit -m "docs: comprehensive project overview, features and credentials"
     ```
   - Proceed through `10_docker_compose.md` to `20_deployment_guide.md`.
   - Execute the test suite:
     ```bash
     python odoo-bin -c odoo.conf -u subscription_management --test-enable --test-tags=subscription_management --stop-after-init
     ```
4. **Push Branch & Open Pull Request**:
   ```bash
   git push origin sanchita/tests-docs-devops
   ```
   Open a Pull Request on GitHub: `sanchita/tests-docs-devops` ➔ `main`.

---

## 🏆 Ensuring Every Member's Contribution Shows on GitHub

To guarantee that GitHub's contribution graph and repository analytics display all 4 contributors:

1. **Configure Git Identity on Each Machine**:
   Each teammate must run:
   ```bash
   git config --global user.name "Your Full Name"
   git config --global user.email "your-github-registered-email@example.com"
   ```
   *(Important: The email must match the email verified on their GitHub profile).*

2. **Branch & PR Strategy**:
   - Do **NOT** commit everything from one account.
   - Neeraj commits to `neeraj/*` branches.
   - Prem commits to `prem/*` branches.
   - Divya commits to `divya/*` branches.
   - Sanchita commits to `sanchita/*` branches.

3. **Merging Order**:
   ```
   1. Merge Divya's PR (Core Engine Models & Views)
   2. Merge Neeraj's PR (Auth, Email, Cron Logic)
   3. Merge Prem's PR (Demo Data, Wizards, SCSS)
   4. Merge Sanchita's PR (Tests, Docs, Docker)
   ```
   Use **"Create a merge commit"** or **"Rebase and merge"** on GitHub so each member's individual commits are preserved in the `main` history.
