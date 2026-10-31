# Hackathon Live Demo & Presentation Script (10-Minute Winning Pitch)

## Context
A battle-tested 10-minute presentation and live demo script for the hackathon judges, demonstrating every single requirement from the Brightloop Software problem statement.

## Prompt for Antigravity

```markdown
Create `docs/DEMO_SCRIPT.md`:

```markdown
# 🏆 Brightloop Subscription Platform - Hackathon Demo Script

**Total Demo Duration:** 10 Minutes  
**Roles Demonstrated:** System Admin, Internal Staff, External Customer

---

## ⏱️ Minute 0:00 - 1:30 | The Hook & Pain Points
- **Narrative:** "Today, Brightloop Software manages subscriptions on spreadsheets. Renewals get forgotten, invoices are hand-typed with errors, and bank reconciliation takes hours. Here is our unified Odoo 18 subscription engine."
- Show the **Dashboard**: Highlight active subscriptions, monthly recurring revenue (MRR), outstanding balance, and overdue alerts loading in under 2 seconds.

---

## ⏱️ Minute 1:30 - 3:30 | Scene 1: Product Variants & Subscription Plans
- Log in as **Admin**.
- Navigate to **Subscriptions > Products**:
  - Show "Brightloop Enterprise Suite".
  - Open variants: Show the **Brand: Odoo** variant adding **₹560** extra automatically.
- Navigate to **Plans**:
  - Show the 4 frequencies: Daily, Weekly, Monthly, Yearly.
  - Highlight policy toggles: Auto-close on expiry, allow pause, allow renew.

---

## ⏱️ Minute 3:30 - 5:30 | Scene 2: Sales Rep & Quotation Templates
- Log in as **Staff**.
- Open **Subscriptions > All Subscriptions** > Click **New**.
- Select customer "Acuity Bakery".
- Select Quotation Template: Click **Load Template** — observe product lines, quantities, and prices auto-populating instantly.
- Demonstrate state transitions:
  - Draft → Click **Send Quotation**
  - Click **Confirm**
  - Click **Activate** (Observe next billing date calculated dynamically based on frequency).

---

## ⏱️ Minute 5:30 - 7:00 | Scene 3: Automated Billing Day & Discount Rules
- "It is billing day: hundreds of accounts are due."
- Click **Create Invoice** on an active subscription.
- Point out:
  - Lines, taxes (GST 18%), and totals are prefilled.
  - Active discount rules auto-applied without staff intervention.
  - Attempt to click Create Invoice again immediately: **System raises duplicate billing prevention error!**

---

## ⏱️ Minute 7:00 - 8:30 | Scene 4: Payments & Reconciliation
- On the confirmed invoice, click **Register Payment**.
- Show the wizard prefilled with the outstanding amount.
- Select method `UPI` and enter partial payment of ₹10,000.
- State updates to **Partially Paid** with real-time balance due.
- Record the remaining balance via `Bank Transfer`: Invoice transitions to **Paid**.

---

## ⏱️ Minute 8:30 - 9:30 | Scene 5: Customer Self-Service Portal
- Log out of backend.
- Visit `/subscription/signup`: Show real-time password strength validation (8+ chars, upper, lower, special character).
- Log in as Customer (`portal@acuitybakery.com`).
- Navigate to `/my/subscriptions`: Customer views active subscriptions, next renewal dates, and downloads official invoice PDFs.

---

## ⏱️ Minute 9:30 - 10:00 | Conclusion & Q&A
- Show full test suite passing in CLI (`tests/`).
- Summary of architecture: Odoo 18 custom module, OWL dashboard, zero external dependencies required.
```
```

## Expected Output
- `docs/DEMO_SCRIPT.md`
