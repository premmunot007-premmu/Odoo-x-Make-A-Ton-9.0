# -*- coding: utf-8 -*-
import logging

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

BILLING_PERIODS = {
    'daily': relativedelta(days=1),
    'weekly': relativedelta(weeks=1),
    'monthly': relativedelta(months=1),
    'yearly': relativedelta(years=1),
}


class Subscription(models.Model):
    """A customer's subscription to a plan, moving through Draft → Quotation → Confirmed → Active → Closed."""

    _name = 'subscription.subscription'
    _description = 'Subscription'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'name desc'

    name = fields.Char(
        string="Subscription Number", readonly=True, copy=False, default='New', index='trigram',
    )
    partner_id = fields.Many2one('res.partner', string="Customer", required=True, tracking=True)
    plan_id = fields.Many2one('subscription.plan', string="Plan", required=True, tracking=True)
    template_id = fields.Many2one(
        'subscription.quotation.template', string="Quotation Template", domain=[('is_active', '=', True)],
    )
    start_date = fields.Date(
        string="Start Date", required=True, default=fields.Date.context_today, tracking=True,
    )
    expiry_date = fields.Date(string="Expiry Date", tracking=True)
    next_billing_date = fields.Date(
        string="Next Billing Date",
        compute='_compute_next_billing_date',
        store=True,
        readonly=False,
        tracking=True,
    )
    payment_term = fields.Selection(
        [
            ('immediate', 'Immediate'),
            ('15_days', '15 Days'),
            ('30_days', '30 Days'),
            ('60_days', '60 Days'),
        ],
        string="Payment Term",
        default='30_days',
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('quotation', 'Quotation'),
            ('confirmed', 'Confirmed'),
            ('active', 'Active'),
            ('paused', 'Paused'),
            ('closed', 'Closed'),
        ],
        string="Status",
        default='draft',
        required=True,
        copy=False,
        tracking=True,
    )
    subscription_line_ids = fields.One2many(
        'subscription.subscription.line', 'subscription_id', string="Order Lines", copy=True,
    )
    invoice_ids = fields.One2many('subscription.invoice', 'subscription_id', string="Invoices")
    invoice_count = fields.Integer(string="Invoice Count", compute='_compute_invoice_count')
    amount_untaxed = fields.Monetary(string="Untaxed Amount", compute='_compute_amounts', store=True)
    amount_tax = fields.Monetary(string="Taxes", compute='_compute_amounts', store=True)
    amount_total = fields.Monetary(string="Total", compute='_compute_amounts', store=True, tracking=True)
    company_id = fields.Many2one(
        'res.company', string="Company", required=True, default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string="Currency")
    user_id = fields.Many2one(
        'res.users', string="Salesperson", default=lambda self: self.env.user, tracking=True,
    )
    end_date = fields.Date(string="End Date", compute='_compute_end_date', inverse='_inverse_end_date', store=True)
    total_amount = fields.Monetary(string="Total Amount", compute='_compute_total_amount', store=True)
    notes = fields.Text(string="Notes Text", compute='_compute_notes', inverse='_inverse_notes', store=True)

    @api.depends('expiry_date')
    def _compute_end_date(self):
        for rec in self:
            rec.end_date = rec.expiry_date

    def _inverse_end_date(self):
        for rec in self:
            rec.expiry_date = rec.end_date

    @api.depends('amount_total')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = rec.amount_total

    @api.depends('note')
    def _compute_notes(self):
        for rec in self:
            rec.notes = str(rec.note or '')

    def _inverse_notes(self):
        for rec in self:
            rec.note = rec.notes

    note = fields.Html(string="Internal Notes")
    is_expired = fields.Boolean(
        string="Expired", compute='_compute_is_expired', search='_search_is_expired',
    )

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name, company_id)', 'Subscription number must be unique per company!'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        """Assign the next subscription number from the sequence."""
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('subscription.subscription') or 'New'
        return super().create(vals_list)

    # ------------------------------------------------------------------
    # Computes
    # ------------------------------------------------------------------

    @api.depends('subscription_line_ids.subtotal', 'subscription_line_ids.tax_amount')
    def _compute_amounts(self):
        for rec in self:
            rec.amount_untaxed = sum(rec.subscription_line_ids.mapped('subtotal'))
            rec.amount_tax = sum(rec.subscription_line_ids.mapped('tax_amount'))
            rec.amount_total = rec.amount_untaxed + rec.amount_tax

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for rec in self:
            rec.invoice_count = len(rec.invoice_ids)

    @api.depends('start_date', 'plan_id.billing_frequency')
    def _compute_next_billing_date(self):
        """Initial billing date is one period after the start date; invoicing advances it afterwards."""
        for rec in self:
            if rec.start_date and rec.plan_id:
                rec.next_billing_date = rec.start_date + rec._get_billing_period()
            else:
                rec.next_billing_date = False

    @api.depends('expiry_date')
    def _compute_is_expired(self):
        today = fields.Date.context_today(self)
        for rec in self:
            rec.is_expired = bool(rec.expiry_date and rec.expiry_date < today)

    def _search_is_expired(self, operator, value):
        """Evaluated against today's date at search time, so it never goes stale."""
        if operator not in ('=', '!='):
            raise UserError(_("Unsupported search operator for 'Expired'."))
        today = fields.Date.context_today(self)
        expired = (operator == '=') == bool(value)
        if expired:
            return [('expiry_date', '!=', False), ('expiry_date', '<', today)]
        return ['|', ('expiry_date', '=', False), ('expiry_date', '>=', today)]

    def _compute_access_url(self):
        super()._compute_access_url()
        for rec in self:
            rec.access_url = f'/my/subscriptions/{rec.id}'

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_billing_period(self):
        """Return the relativedelta matching this subscription's plan frequency."""
        self.ensure_one()
        return BILLING_PERIODS.get(self.plan_id.billing_frequency, relativedelta(months=1))

    def _check_state(self, allowed_states, action_label):
        """Raise if any record is not in one of ``allowed_states``."""
        invalid = self.filtered(lambda r: r.state not in allowed_states)
        if invalid:
            raise UserError(_(
                "Cannot %(action)s subscription(s) %(names)s in their current status.",
                action=action_label,
                names=", ".join(invalid.mapped('name')),
            ))

    # ------------------------------------------------------------------
    # State transitions
    # ------------------------------------------------------------------

    def action_send_quotation(self):
        self._check_state(['draft'], _("send a quotation for"))
        self.write({'state': 'quotation'})

    def action_confirm(self):
        self._check_state(['draft', 'quotation'], _("confirm"))
        self.write({'state': 'confirmed'})

    def action_activate(self):
        self._check_state(['confirmed', 'paused'], _("activate"))
        self.write({'state': 'active'})

    def action_pause(self):
        self._check_state(['active'], _("pause"))
        if self.filtered(lambda r: not r.plan_id.allow_pause):
            raise UserError(_("This plan does not allow pausing."))
        self.write({'state': 'paused'})

    def action_close(self):
        self._check_state(['draft', 'quotation', 'confirmed', 'active', 'paused'], _("close"))
        early = self.filtered(
            lambda r: r.state in ('active', 'paused') and not r.plan_id.allow_early_close
            and (not r.expiry_date or r.expiry_date > fields.Date.context_today(r))
        )
        if early:
            raise UserError(_("This plan does not allow early termination."))
        self.write({'state': 'closed'})

    def action_renew(self):
        """Extend the subscription by one billing period from its current expiry (or today if already lapsed)."""
        self._check_state(['active', 'paused', 'closed'], _("renew"))
        today = fields.Date.context_today(self)
        for rec in self:
            if not rec.plan_id.allow_renew:
                raise UserError(_("This plan does not allow renewal."))
            base = max(rec.expiry_date, today) if rec.expiry_date else today
            rec.write({'state': 'active', 'expiry_date': base + rec._get_billing_period()})

    def action_load_template(self):
        """Replace subscription lines with the products from the selected quotation template."""
        self.ensure_one()
        if not self.template_id:
            raise UserError(_("Select a quotation template first."))
        lines = [fields.Command.clear()] + [
            fields.Command.create({
                'product_id': tpl_line.product_id.id,
                'quantity': tpl_line.quantity,
                'unit_price': tpl_line.unit_price,
            })
            for tpl_line in self.template_id.template_line_ids
        ]
        vals = {'subscription_line_ids': lines}
        if self.template_id.plan_id:
            vals['plan_id'] = self.template_id.plan_id.id
        self.write(vals)

    # ------------------------------------------------------------------
    # Invoicing
    # ------------------------------------------------------------------

    def action_create_invoice(self):
        """Button: create the invoice for this subscription and open it."""
        invoice = self._create_invoice()
        return {
            'type': 'ir.actions.act_window',
            'name': _("Invoice"),
            'res_model': 'subscription.invoice',
            'res_id': invoice.id,
            'view_mode': 'form',
        }

    def action_view_invoices(self):
        """Smart button: open this subscription's invoices."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _("Invoices"),
            'res_model': 'subscription.invoice',
            'view_mode': 'list,form',
            'domain': [('subscription_id', '=', self.id)],
            'context': {'default_subscription_id': self.id, 'default_partner_id': self.partner_id.id},
        }

    def _create_invoice(self):
        """Create an invoice from this subscription's lines, at most once per billing period.

        :return: the created ``subscription.invoice`` record
        """
        self.ensure_one()
        if self.state != 'active':
            raise UserError(_("Can only invoice active subscriptions."))
        if not self.subscription_line_ids:
            raise UserError(_("Subscription %s has no lines to invoice.", self.name))

        today = fields.Date.context_today(self)
        period = self._get_billing_period()

        # Prevent duplicate billing: one non-cancelled invoice per billing period.
        last_invoice = self.env['subscription.invoice'].search([
            ('subscription_id', '=', self.id),
            ('state', '!=', 'cancelled'),
        ], order='invoice_date desc', limit=1)
        if last_invoice:
            next_allowed = last_invoice.invoice_date + period
            if today < next_allowed:
                raise UserError(_(
                    "Already invoiced for this period. Next invoice allowed on %s.",
                    fields.Date.to_string(next_allowed),
                ))

        term_days = {'immediate': 0, '15_days': 15, '30_days': 30, '60_days': 60}
        due_date = today + relativedelta(days=term_days.get(self.payment_term, 30))

        line_vals, applied_rules = self._prepare_invoice_line_vals()
        invoice = self.env['subscription.invoice'].create({
            'subscription_id': self.id,
            'partner_id': self.partner_id.id,
            'company_id': self.company_id.id,
            'invoice_date': today,
            'due_date': due_date,
            'invoice_line_ids': [fields.Command.create(vals) for vals in line_vals],
        })

        # Each discount rule counts one use per invoice, however many lines it touched.
        for rule in applied_rules.sudo():
            rule.current_usage += 1

        # Advance from the scheduled date so a late run doesn't shift future billing days;
        # if several periods were missed, resume from today instead of billing them all at once.
        next_date = (self.next_billing_date or today) + period
        if next_date <= today:
            next_date = today + period
        self.next_billing_date = next_date
        return invoice

    @api.model
    def action_mass_invoice(self):
        """Mass generate invoices for all active subscriptions due for billing.

        Called manually or via cron job. Each subscription is billed in its own savepoint,
        so one failure is logged and rolled back without aborting the rest of the batch.
        """
        today = fields.Date.context_today(self)
        due_subscriptions = self.search([
            ('state', '=', 'active'),
            ('next_billing_date', '<=', today),
        ])
        invoices = self.env['subscription.invoice']
        errors = []
        for sub in due_subscriptions:
            try:
                with self.env.cr.savepoint():
                    invoices |= sub._create_invoice()
            except Exception as e:  # noqa: BLE001 - keep billing the remaining subscriptions
                errors.append(f"{sub.name}: {e}")
                _logger.warning("Billing error for %s: %s", sub.name, e)

        _logger.info(
            "Mass billing: %d invoice(s) created, %d subscription(s) failed",
            len(invoices), len(errors),
        )
        return {
            'type': 'ir.actions.act_window',
            'name': _("Generated Invoices (%s)", len(invoices)),
            'res_model': 'subscription.invoice',
            'view_mode': 'list,form',
            'domain': [('id', 'in', invoices.ids)],
        }

    @api.model
    def _cron_close_expired(self):
        """Cron: Auto-close subscriptions past expiry date with auto_close plan"""
        today = fields.Date.context_today(self)
        expired = self.search([
            ('state', '=', 'active'),
            ('expiry_date', '<', today),
            ('plan_id.auto_close', '=', True),
        ])
        # Direct write: expiry-based closing must bypass the early-termination check in action_close.
        expired.write({'state': 'closed'})
        _logger.info("Auto-closed %d expired subscriptions", len(expired))

    @api.model
    def _cron_billing(self):
        """Cron: Mass billing for due subscriptions"""
        self.action_mass_invoice()

    # ------------------------------------------------------------------
    # Dashboard
    # ------------------------------------------------------------------

    @api.model
    def get_dashboard_data(self):
        """KPIs and chart data for the OWL dashboard, in one call.

        Dates use the user's timezone, so "this month" starts on the user's 1st, not UTC's.
        """
        Invoice = self.env['subscription.invoice']
        Payment = self.env['subscription.payment']
        today = fields.Date.context_today(self)
        month_start = today.replace(day=1)

        collected = Payment._read_group(
            [('payment_date', '>=', month_start)], aggregates=['amount:sum'],
        )[0][0]
        outstanding = Invoice._read_group(
            [('state', '=', 'confirmed')], aggregates=['amount_due:sum'],
        )[0][0]

        # Payments collected per month, last 6 months (including empty months).
        first_month = month_start - relativedelta(months=5)
        by_month = dict(Payment._read_group(
            [('payment_date', '>=', first_month)],
            groupby=['payment_date:month'],
            aggregates=['amount:sum'],
        ))
        monthly = []
        for i in range(6):
            month = first_month + relativedelta(months=i)
            monthly.append({
                'label': month.strftime('%b %Y'),
                'amount': by_month.get(month, 0.0),
            })

        state_labels = dict(self._fields['state']._description_selection(self.env))
        counts = dict(self._read_group([], groupby=['state'], aggregates=['__count']))
        status_distribution = [
            {'state': state, 'label': label, 'count': counts.get(state, 0)}
            for state, label in state_labels.items()
        ]

        return {
            'active_subscriptions': counts.get('active', 0),
            'collected_this_month': collected or 0.0,
            'outstanding_amount': outstanding or 0.0,
            'overdue_invoices': Invoice.search_count([('is_overdue', '=', True)]),
            'monthly_revenue': monthly,
            'status_distribution': status_distribution,
            'currency_id': self.env.company.currency_id.id,
        }

    def _prepare_invoice_line_vals(self):
        """Build invoice line values from the subscription lines.

        Each invoice line's ``discount_amount`` combines the subscription line's own
        percentage discount with any active discount rules. Product rules are evaluated
        per line; subscription-wide rules are evaluated once against the whole
        subscription and spread across lines in proportion to their value.

        :return: (list of invoice line value dicts, recordset of discount rules applied)
        """
        self.ensure_one()
        rules = self._get_discount_rules()
        product_rules = rules.filtered(lambda r: r.apply_on == 'product')
        subscription_rules = rules - product_rules
        applied_rules = self.env['subscription.discount.rule']

        prepared = []
        for line in self.subscription_line_ids:
            unit_price = line.unit_price + line.variant_id.price_extra
            gross = line.quantity * unit_price
            base = gross * (1 - line.discount / 100.0)
            prepared.append((line, unit_price, gross, base))

        total_base = sum(base for _line, _price, _gross, base in prepared)
        total_qty = sum(self.subscription_line_ids.mapped('quantity'))
        subscription_discount = 0.0
        for rule in subscription_rules:
            if self._discount_rule_applies(rule, total_qty, total_base):
                subscription_discount += self._discount_rule_amount(rule, total_base)
                applied_rules |= rule

        line_vals = []
        for line, unit_price, gross, base in prepared:
            discount = gross - base
            for rule in product_rules.filtered(lambda r: line.product_id in r.product_ids):
                if self._discount_rule_applies(rule, line.quantity, base):
                    discount += self._discount_rule_amount(rule, base)
                    applied_rules |= rule
            if total_base:
                discount += subscription_discount * base / total_base
            line_vals.append({
                'product_id': line.product_id.id,
                'description': line.variant_id.display_name if line.variant_id else line.product_id.name,
                'quantity': line.quantity,
                'unit_price': unit_price,
                'tax_ids': [fields.Command.set(line.tax_ids.ids)],
                'discount_amount': min(discount, gross),
            })
        return line_vals, applied_rules

    def _get_discount_rules(self):
        """Return discount rules valid today that could apply to this subscription."""
        self.ensure_one()
        today = fields.Date.context_today(self)
        return self.env['subscription.discount.rule'].search([
            ('is_active', '=', True),
            '|', ('date_start', '=', False), ('date_start', '<=', today),
            '|', ('date_end', '=', False), ('date_end', '>=', today),
            '|',
                '&', ('apply_on', '=', 'product'),
                     ('product_ids', 'in', self.subscription_line_ids.product_id.ids),
                ('apply_on', '=', 'subscription'),
        ])

    @staticmethod
    def _discount_rule_applies(rule, quantity, base):
        """Check a rule's usage limit and minimum quantity / purchase thresholds."""
        if rule.max_usage > 0 and rule.current_usage >= rule.max_usage:
            return False
        if rule.min_quantity and quantity < rule.min_quantity:
            return False
        if rule.min_purchase and base < rule.min_purchase:
            return False
        return True

    @staticmethod
    def _discount_rule_amount(rule, base):
        """Discount a rule gives on ``base``: a percentage of it or a fixed amount."""
        if rule.discount_type == 'percentage':
            return base * (rule.amount / 100.0)
        return rule.amount

    # ------------------------------------------------------------------
    # Constraints
    # ------------------------------------------------------------------

    @api.constrains('start_date', 'expiry_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.expiry_date and rec.start_date > rec.expiry_date:
                raise ValidationError(_("Expiry date must be after start date."))
