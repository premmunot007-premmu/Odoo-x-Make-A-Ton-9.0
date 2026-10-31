# Dashboard — OWL Component with KPIs & Charts

## Context
Finance lead needs a dashboard showing: active subscription count, monthly revenue, outstanding amount, overdue invoices, with charts for trends.

## Prompt for Claude Code

```
In the Odoo 18 module "subscription_management", create an OWL dashboard.

Create `static/src/js/dashboard.js`:

/** @odoo-module */
import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class SubscriptionDashboard extends Component {
    static template = "subscription_management.Dashboard";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            activeSubscriptions: 0,
            totalRevenue: 0,
            outstandingAmount: 0,
            overdueInvoices: 0,
            monthlyRevenue: [],
            statusDistribution: [],
        });
        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        // Active subscriptions count
        this.state.activeSubscriptions = await this.orm.searchCount(
            "subscription.subscription", [["state", "=", "active"]]
        );

        // Total revenue this month (paid invoices)
        const now = new Date();
        const firstDay = new Date(now.getFullYear(), now.getMonth(), 1).toISOString().split('T')[0];
        const paidInvoices = await this.orm.searchRead(
            "subscription.invoice",
            [["state", "=", "paid"], ["invoice_date", ">=", firstDay]],
            ["amount_total"]
        );
        this.state.totalRevenue = paidInvoices.reduce((sum, inv) => sum + inv.amount_total, 0);

        // Outstanding amount
        const confirmedInvoices = await this.orm.searchRead(
            "subscription.invoice",
            [["state", "=", "confirmed"]],
            ["amount_due"]
        );
        this.state.outstandingAmount = confirmedInvoices.reduce((sum, inv) => sum + inv.amount_due, 0);

        // Overdue invoices count
        this.state.overdueInvoices = await this.orm.searchCount(
            "subscription.invoice", [["is_overdue", "=", true], ["state", "!=", "paid"]]
        );

        // Status distribution for pie chart
        const allSubs = await this.orm.readGroup(
            "subscription.subscription", [], ["state"], ["state"]
        );
        this.state.statusDistribution = allSubs.map(g => ({
            label: g.state, count: g.state_count
        }));
    }

    openSubscriptions() {
        this.action.doAction("subscription_management.action_subscription");
    }

    openInvoices() {
        this.action.doAction("subscription_management.action_invoice");
    }

    openOverdueInvoices() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Overdue Invoices",
            res_model: "subscription.invoice",
            view_mode: "tree,form",
            domain: [["is_overdue", "=", true]],
        });
    }

    openPayments() {
        this.action.doAction("subscription_management.action_payment");
    }
}

registry.category("actions").add("subscription_dashboard", SubscriptionDashboard);


Create `static/src/xml/dashboard.xml`:
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <t t-name="subscription_management.Dashboard">
        <div class="o_subscription_dashboard container-fluid py-4">
            <h2 class="mb-4">Subscription Dashboard</h2>
            <!-- KPI Cards Row -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="card bg-primary text-white shadow cursor-pointer" t-on-click="openSubscriptions">
                        <div class="card-body text-center">
                            <h5>Active Subscriptions</h5>
                            <h2 class="display-4"><t t-esc="state.activeSubscriptions"/></h2>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-success text-white shadow cursor-pointer" t-on-click="openInvoices">
                        <div class="card-body text-center">
                            <h5>Revenue This Month</h5>
                            <h2 class="display-4">₹<t t-esc="state.totalRevenue.toLocaleString()"/></h2>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-warning text-dark shadow cursor-pointer" t-on-click="openInvoices">
                        <div class="card-body text-center">
                            <h5>Outstanding</h5>
                            <h2 class="display-4">₹<t t-esc="state.outstandingAmount.toLocaleString()"/></h2>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card bg-danger text-white shadow cursor-pointer" t-on-click="openOverdueInvoices">
                        <div class="card-body text-center">
                            <h5>Overdue Invoices</h5>
                            <h2 class="display-4"><t t-esc="state.overdueInvoices"/></h2>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Status Distribution -->
            <div class="row">
                <div class="col-md-6">
                    <div class="card shadow">
                        <div class="card-header"><h5>Subscription Status</h5></div>
                        <div class="card-body">
                            <table class="table">
                                <thead><tr><th>Status</th><th>Count</th></tr></thead>
                                <tbody>
                                    <t t-foreach="state.statusDistribution" t-as="item" t-key="item.label">
                                        <tr><td><t t-esc="item.label"/></td><td><t t-esc="item.count"/></td></tr>
                                    </t>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </t>
</templates>

Create `static/src/scss/dashboard.scss`:
.o_subscription_dashboard {
    .card { transition: transform 0.2s; border-radius: 12px; }
    .card:hover { transform: translateY(-4px); }
    .cursor-pointer { cursor: pointer; }
    .display-4 { font-weight: 700; }
}

Update __manifest__.py assets section:
'assets': {
    'web.assets_backend': [
        'subscription_management/static/src/js/dashboard.js',
        'subscription_management/static/src/xml/dashboard.xml',
        'subscription_management/static/src/scss/dashboard.scss',
    ],
},
```

## Expected Output
- `static/src/js/dashboard.js`
- `static/src/xml/dashboard.xml`
- `static/src/scss/dashboard.scss`

## Verification
- Click Dashboard in menu, verify KPI cards show with correct data
