/** @odoo-module **/
import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class SubscriptionDashboard extends Component {
    static template = "subscription_management.Dashboard";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            activeSubscriptions: 0,
            totalRevenue: 0,
            outstandingAmount: 0,
            overdueInvoices: 0,
            statusDistribution: [],
            recentSubscriptions: [],
        });

        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        try {
            // 1. Active subscriptions count
            this.state.activeSubscriptions = await this.orm.searchCount(
                "subscription.subscription",
                [["state", "=", "active"]]
            );

            // 2. Total revenue (paid invoices)
            const paidInvoices = await this.orm.searchRead(
                "subscription.invoice",
                [["state", "=", "paid"]],
                ["amount_total", "total_amount"]
            );
            this.state.totalRevenue = paidInvoices.reduce(
                (sum, inv) => sum + (inv.total_amount || inv.amount_total || 0),
                0
            );

            // 3. Outstanding amount (confirmed & overdue)
            const outstandingInvoices = await this.orm.searchRead(
                "subscription.invoice",
                [["state", "in", ["confirmed", "overdue"]]],
                ["amount_due"]
            );
            this.state.outstandingAmount = outstandingInvoices.reduce(
                (sum, inv) => sum + (inv.amount_due || 0),
                0
            );

            // 4. Overdue invoices count
            this.state.overdueInvoices = await this.orm.searchCount(
                "subscription.invoice",
                [["state", "=", "overdue"]]
            );

            // 5. Status distribution
            const allSubs = await this.orm.readGroup(
                "subscription.subscription",
                [],
                ["state"],
                ["state"]
            );
            this.state.statusDistribution = allSubs.map((g) => ({
                label: g.state ? g.state.toUpperCase() : "DRAFT",
                count: g.state_count || 0,
            }));

            // 6. Recent subscriptions
            this.state.recentSubscriptions = await this.orm.searchRead(
                "subscription.subscription",
                [],
                ["name", "partner_id", "plan_id", "state", "total_amount"],
                { limit: 5, order: "create_date desc" }
            );
        } catch (e) {
            console.error("Dashboard data load error:", e);
        }
    }

    openSubscriptions() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Active Subscriptions",
            res_model: "subscription.subscription",
            view_mode: "list,form,kanban",
            domain: [["state", "=", "active"]],
        });
    }

    openInvoices() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Paid Invoices",
            res_model: "subscription.invoice",
            view_mode: "list,form",
            domain: [["state", "=", "paid"]],
        });
    }

    openOutstanding() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Outstanding Invoices",
            res_model: "subscription.invoice",
            view_mode: "list,form",
            domain: [["state", "in", ["confirmed", "overdue"]]],
        });
    }

    openOverdueInvoices() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Overdue Invoices",
            res_model: "subscription.invoice",
            view_mode: "list,form",
            domain: [["state", "=", "overdue"]],
        });
    }

    openSubscriptionDetail(id) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Subscription",
            res_model: "subscription.subscription",
            res_id: id,
            view_mode: "form",
            views: [[false, "form"]],
        });
    }
}

registry.category("actions").add("subscription_dashboard", SubscriptionDashboard);
