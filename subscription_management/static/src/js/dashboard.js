/** @odoo-module */
import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { formatMonetary } from "@web/views/fields/formatters";

class SubscriptionDashboard extends Component {
    static template = "subscription_management.Dashboard";
    static props = ["*"];

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            loaded: false,
            activeSubscriptions: 0,
            collectedThisMonth: 0,
            outstandingAmount: 0,
            overdueInvoices: 0,
            monthlyRevenue: [],
            statusDistribution: [],
            currencyId: false,
        });
        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        // All KPIs come from one server call, computed in the user's timezone.
        const data = await this.orm.call("subscription.subscription", "get_dashboard_data", []);
        Object.assign(this.state, {
            loaded: true,
            activeSubscriptions: data.active_subscriptions,
            collectedThisMonth: data.collected_this_month,
            outstandingAmount: data.outstanding_amount,
            overdueInvoices: data.overdue_invoices,
            monthlyRevenue: data.monthly_revenue,
            statusDistribution: data.status_distribution,
            currencyId: data.currency_id,
        });
    }

    formatAmount(value) {
        return formatMonetary(value, { currencyId: this.state.currencyId });
    }

    get maxMonthlyRevenue() {
        return Math.max(...this.state.monthlyRevenue.map((m) => m.amount), 0);
    }

    barHeight(amount) {
        const max = this.maxMonthlyRevenue;
        return max ? Math.max((amount / max) * 100, 2) : 2;
    }

    get totalSubscriptions() {
        return this.state.statusDistribution.reduce((sum, s) => sum + s.count, 0);
    }

    statusShare(count) {
        const total = this.totalSubscriptions;
        return total ? Math.round((count / total) * 100) : 0;
    }

    openWindow(name, resModel, domain) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name,
            res_model: resModel,
            views: [[false, "list"], [false, "form"]],
            domain,
        });
    }

    openActiveSubscriptions() {
        this.openWindow("Active Subscriptions", "subscription.subscription", [["state", "=", "active"]]);
    }

    openSubscriptionsByState(state, label) {
        this.openWindow(`${label} Subscriptions`, "subscription.subscription", [["state", "=", state]]);
    }

    openPayments() {
        this.action.doAction("subscription_management.action_payment");
    }

    openOutstandingInvoices() {
        this.openWindow("Outstanding Invoices", "subscription.invoice", [["state", "=", "confirmed"]]);
    }

    openOverdueInvoices() {
        this.openWindow("Overdue Invoices", "subscription.invoice", [["is_overdue", "=", true]]);
    }
}

registry.category("actions").add("subscription_dashboard", SubscriptionDashboard);
