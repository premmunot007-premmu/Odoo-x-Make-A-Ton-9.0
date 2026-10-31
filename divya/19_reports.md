# QWeb Reports — Invoice PDF & Subscription Summary

## Context
Printable invoice PDF report with company header, customer address, line items, tax summary, totals. Subscription summary report with plan details and billing history.

## Prompt for Claude Code

```
In the Odoo 18 module "subscription_management", create QWeb PDF reports.

Create `reports/invoice_report.xml`:

<!-- Report Action -->
<record id="action_report_invoice" model="ir.actions.report">
    <field name="name">Invoice</field>
    <field name="model">subscription.invoice</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">subscription_management.report_invoice_document</field>
    <field name="report_file">subscription_management.report_invoice_document</field>
    <field name="binding_model_id" ref="model_subscription_invoice"/>
    <field name="binding_type">report</field>
</record>

<!-- QWeb Template -->
<template id="report_invoice_document">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="doc">
            <t t-call="web.external_layout">
                <div class="page">
                    <h2>Invoice <span t-field="doc.name"/></h2>
                    <div class="row mt-4 mb-4">
                        <div class="col-6">
                            <strong>Customer:</strong><br/>
                            <span t-field="doc.partner_id.name"/><br/>
                            <span t-field="doc.partner_id.street"/><br/>
                            <span t-field="doc.partner_id.city"/>
                            <span t-field="doc.partner_id.zip"/>
                        </div>
                        <div class="col-6 text-end">
                            <strong>Invoice Date:</strong> <span t-field="doc.invoice_date"/><br/>
                            <strong>Due Date:</strong> <span t-field="doc.due_date"/><br/>
                            <strong>Subscription:</strong> <span t-field="doc.subscription_id.name"/>
                        </div>
                    </div>
                    <table class="table table-bordered">
                        <thead>
                            <tr>
                                <th>Product</th><th>Description</th><th class="text-end">Qty</th>
                                <th class="text-end">Unit Price</th><th class="text-end">Discount</th>
                                <th class="text-end">Tax</th><th class="text-end">Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            <t t-foreach="doc.invoice_line_ids" t-as="line">
                                <tr>
                                    <td><span t-field="line.product_id.name"/></td>
                                    <td><span t-field="line.description"/></td>
                                    <td class="text-end"><span t-field="line.quantity"/></td>
                                    <td class="text-end"><span t-field="line.unit_price" t-options='{"widget": "monetary"}'/></td>
                                    <td class="text-end"><span t-field="line.discount_amount" t-options='{"widget": "monetary"}'/></td>
                                    <td class="text-end"><span t-field="line.tax_amount" t-options='{"widget": "monetary"}'/></td>
                                    <td class="text-end"><span t-field="line.total" t-options='{"widget": "monetary"}'/></td>
                                </tr>
                            </t>
                        </tbody>
                    </table>
                    <div class="row">
                        <div class="col-6"/>
                        <div class="col-6">
                            <table class="table">
                                <tr><td>Subtotal</td><td class="text-end"><span t-field="doc.amount_untaxed" t-options='{"widget": "monetary"}'/></td></tr>
                                <tr><td>Tax</td><td class="text-end"><span t-field="doc.amount_tax" t-options='{"widget": "monetary"}'/></td></tr>
                                <tr class="fw-bold"><td>Total</td><td class="text-end"><span t-field="doc.amount_total" t-options='{"widget": "monetary"}'/></td></tr>
                                <tr><td>Amount Paid</td><td class="text-end"><span t-field="doc.amount_paid" t-options='{"widget": "monetary"}'/></td></tr>
                                <tr class="fw-bold"><td>Amount Due</td><td class="text-end"><span t-field="doc.amount_due" t-options='{"widget": "monetary"}'/></td></tr>
                            </table>
                        </div>
                    </div>
                </div>
            </t>
        </t>
    </t>
</template>

Create `reports/subscription_report.xml` similarly for subscription summary:
- Report action bound to subscription.subscription
- Template showing: subscription details, plan info, line items, invoice history

Update __manifest__.py to include report files.
```

## Expected Output
- `reports/invoice_report.xml`
- `reports/subscription_report.xml`

## Verification
- Open an invoice, click Print > Invoice, verify PDF generates correctly
