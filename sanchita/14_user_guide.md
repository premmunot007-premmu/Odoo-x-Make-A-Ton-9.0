# End-User Operation & Feature Guide

## Context
Create `docs/USER_GUIDE.md` detailing how to use the system for administrators, sales representatives, billing clerks, and end customers.

## Prompt for Antigravity

```markdown
Create `docs/USER_GUIDE.md` with step-by-step operating instructions:

```markdown
# 📖 Brightloop Subscription Platform - User Guide

## 1. Setting up Products & Variants
1. Navigate to **Subscriptions > Products & Plans > Products**.
2. Click **New**.
3. Enter Product Name (e.g. *Brightloop CRM*), Product Type (*Software*), and Sales Price.
4. Under the **Variants** tab, click **Add a line**.
5. Set Attribute as `Brand`, Value as `Odoo`, and Extra Price as `560.00`.
6. Save.

## 2. Setting up Billing Plans
1. Navigate to **Subscriptions > Products & Plans > Plans**.
2. Click **New**.
3. Choose Billing Frequency (*Daily*, *Weekly*, *Monthly*, or *Yearly*).
4. Configure lifecycle policies:
   - Check **Auto-Close on Expiry** if the subscription should stop automatically.
   - Configure **Allow Pause** or **Allow Renewal**.
5. In **Default Products**, add standard software packages and click Save.

## 3. Creating & Managing Subscriptions
1. Navigate to **Subscriptions > Subscriptions > All Subscriptions**.
2. Click **New**. Select a Customer and Plan.
3. To load a pre-configured quote, choose a **Quotation Template** and click **Load Template**.
4. Add line items, adjusting quantities and selecting applicable variants.
5. Lifecycle Transitions:
   - Click **Send Quotation** (State moves to Quotation).
   - Click **Confirm** (State moves to Confirmed).
   - Click **Activate** (State moves to Active).
   - Click **Pause** or **Renew** as needed.

## 4. Invoicing & Billing Day
- Individual: Click **Create Invoice** directly on an active subscription form.
- Automated Mass Billing: Run via scheduled action or call `action_mass_invoice()` to bill all due accounts simultaneously. Duplicate billing within the same period is strictly blocked.

## 5. Registering Payments
1. Open any confirmed invoice.
2. Click **Register Payment**.
3. Select Payment Method (*Bank Transfer*, *UPI*, *Credit Card*, etc.).
4. Confirm payment. The invoice will auto-transition to **Paid** once the balance reaches 0.

## 6. Accessing the Customer Portal
1. Customers log in at `/subscription/login`.
2. Browse to `/my/subscriptions` to view active contracts, renewal dates, and associated invoices.
3. Download official invoice PDFs on demand.
```
```

## Expected Output
- `docs/USER_GUIDE.md`
