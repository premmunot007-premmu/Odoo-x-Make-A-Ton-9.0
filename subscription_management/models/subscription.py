# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)

class Subscription(models.Model):
    _name = 'subscription.subscription'
    _description = 'Subscription'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'create_date desc, id desc'
    _rec_name = 'name'

    name = fields.Char(string="Subscription Number", readonly=True, copy=False, default='New', tracking=True)
    partner_id = fields.Many2one('res.partner', string="Customer", required=True, tracking=True, domain="[('customer_rank', '>', 0)]")
    plan_id = fields.Many2one('subscription.plan', string="Subscription Plan", required=True, tracking=True)
    template_id = fields.Many2one('subscription.quotation.template', string="Quotation Template")
    start_date = fields.Date(string="Start Date", required=True, default=fields.Date.today, tracking=True)
    expiry_date = fields.Date(string="Expiry Date", tracking=True)
    next_billing_date = fields.Date(string="Next Billing Date", compute='_compute_next_billing_date', store=True, tracking=True)
    payment_term = fields.Selection([
        ('immediate', 'Immediate Payment'),
        ('15_days', '15 Days'),
        ('30_days', '30 Days'),
        ('60_days', '60 Days'),
    ], string="Payment Terms", default='30_days', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('quotation', 'Quotation'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('closed', 'Closed'),
    ], string="Status", default='draft', required=True, tracking=True, copy=False)
    subscription_line_ids = fields.One2many('subscription.subscription.line', 'subscription_id', string="Subscription Lines")
    invoice_ids = fields.One2many('subscription.invoice', 'subscription_id', string="Invoices")
    invoice_count = fields.Integer(string="Invoice Count", compute='_compute_invoice_count')
    is_expired = fields.Boolean(string="Is Expired", compute='_compute_is_expired', store=True)
    close_reason = fields.Text(string="Close Reason")
    note = fields.Html(string="Notes")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string="Currency", related='company_id.currency_id')

    amount_untaxed = fields.Float(string="Untaxed Amount", compute='_compute_amounts', store=True, digits=(12, 2))
    amount_tax = fields.Float(string="Taxes", compute='_compute_amounts', store=True, digits=(12, 2))
    amount_total = fields.Float(string="Total Amount", compute='_compute_amounts', store=True, digits=(12, 2))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('subscription.subscription') or 'New'
        return super().create(vals_list)

    @api.depends('subscription_line_ids.subtotal', 'subscription_line_ids.tax_amount')
    def _compute_amounts(self):
        for record in self:
            lines = record.subscription_line_ids
            record.amount_untaxed = sum(lines.mapped('subtotal'))
            record.amount_tax = sum(lines.mapped('tax_amount'))
            record.amount_total = record.amount_untaxed + record.amount_tax

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = len(record.invoice_ids)

    @api.depends('start_date', 'plan_id.billing_frequency')
    def _compute_next_billing_date(self):
        for record in self:
            if not record.start_date or not record.plan_id:
                record.next_billing_date = False
                continue
            freq = record.plan_id.billing_frequency
            today = fields.Date.today()
            billing_date = record.start_date
            while billing_date <= today:
                if freq == 'daily':
                    billing_date += relativedelta(days=1)
                elif freq == 'weekly':
                    billing_date += relativedelta(weeks=1)
                elif freq == 'monthly':
                    billing_date += relativedelta(months=1)
                elif freq == 'yearly':
                    billing_date += relativedelta(years=1)
                else:
                    billing_date += relativedelta(months=1)
            record.next_billing_date = billing_date

    @api.depends('expiry_date')
    def _compute_is_expired(self):
        today = fields.Date.today()
        for record in self:
            record.is_expired = bool(record.expiry_date and record.expiry_date < today)

    def _compute_access_url(self):
        super()._compute_access_url()
        for rec in self:
            rec.access_url = f'/my/subscriptions/{rec.id}'

    ### State Machine Transitions ###

    def action_send_quotation(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_("Only draft subscriptions can be sent as quotations."))
            if not rec.subscription_line_ids:
                raise UserError(_("Cannot send a quotation without subscription lines."))
            rec.write({'state': 'quotation'})
            rec.message_post(body=_("Quotation created and sent to customer."))

    def action_confirm(self):
        for rec in self:
            if rec.state not in ('draft', 'quotation'):
                raise UserError(_("Only draft or quotation subscriptions can be confirmed."))
            if not rec.subscription_line_ids:
                raise UserError(_("Cannot confirm a subscription without lines."))
            rec.write({'state': 'confirmed'})
            rec.message_post(body=_("Subscription confirmed by %s.") % self.env.user.name)
            # Send notification email if template exists
            template = self.env.ref('subscription_management.email_template_subscription_confirmed', raise_if_not_found=False)
            if template:
                template.send_mail(rec.id, force_send=False)

    def action_activate(self):
        for rec in self:
            if rec.state not in ('confirmed', 'paused'):
                raise UserError(_("Only confirmed or paused subscriptions can be activated."))
            rec.write({'state': 'active'})
            rec.message_post(body=_("Subscription is now Active."))

    def action_pause(self):
        for rec in self:
            if rec.state != 'active':
                raise UserError(_("Only active subscriptions can be paused."))
            if not rec.plan_id.allow_pause:
                raise UserError(_("Plan '%s' does not permit pausing.") % rec.plan_id.name)
            rec.write({'state': 'paused'})
            rec.message_post(body=_("Subscription has been paused."))

    def action_close(self):
        for rec in self:
            if rec.state in ('closed', 'draft'):
                raise UserError(_("Cannot close a draft or already closed subscription."))
            if rec.state == 'active' and not rec.plan_id.allow_early_close and not rec.is_expired:
                raise UserError(_("Plan '%s' does not allow early termination.") % rec.plan_id.name)
            rec.write({'state': 'closed'})
            rec.message_post(body=_("Subscription closed."))

    def action_renew(self):
        self.ensure_one()
        if not self.plan_id.allow_renew:
            raise UserError(_("Plan '%s' does not allow renewals.") % self.plan_id.name)
        freq = self.plan_id.billing_frequency
        freq_map = {
            'daily': relativedelta(days=1),
            'weekly': relativedelta(weeks=1),
            'monthly': relativedelta(months=1),
            'yearly': relativedelta(years=1)
        }
        delta = freq_map.get(freq, relativedelta(months=1))
        new_start = fields.Date.today()
        new_expiry = (self.expiry_date or new_start) + delta

        self.write({
            'state': 'active',
            'start_date': new_start,
            'expiry_date': new_expiry,
            'close_reason': False,
        })
        self.message_post(body=_("Subscription renewed until %s.") % new_expiry)

    def action_load_template(self):
        self.ensure_one()
        if not self.template_id:
            raise UserError(_("Please choose a quotation template first."))
        lines = []
        for tl in self.template_id.template_line_ids:
            lines.append((0, 0, {
                'product_id': tl.product_id.id,
                'quantity': tl.quantity,
                'unit_price': tl.unit_price,
            }))
        self.write({
            'plan_id': self.template_id.plan_id.id,
            'subscription_line_ids': [(5, 0, 0)] + lines,
        })
        return True

    ### Billing Engine ###

    def _get_discount_amount(self, line):
        """Calculate applicable discount rule on this subscription line"""
        today = fields.Date.today()
        discounts = self.env['subscription.discount.rule'].search([
            ('is_active', '=', True),
            '|', ('date_start', '=', False), ('date_start', '<=', today),
            '|', ('date_end', '=', False), ('date_end', '>=', today),
            '|',
                '&', ('apply_on', '=', 'product'), ('product_ids', 'in', [line.product_id.id]),
                ('apply_on', '=', 'subscription'),
        ])
        base_amount = line.quantity * (line.unit_price + (line.variant_id.price_extra if line.variant_id else 0.0))
        total_discount = 0.0

        for disc in discounts:
            if disc.max_usage > 0 and disc.current_usage >= disc.max_usage:
                continue
            if disc.min_quantity and line.quantity < disc.min_quantity:
                continue
            if disc.min_purchase and base_amount < disc.min_purchase:
                continue

            if disc.discount_type == 'percentage':
                val = base_amount * (disc.amount / 100.0)
            else:
                val = min(disc.amount, base_amount)

            total_discount += val
            disc.sudo().write({'current_usage': disc.current_usage + 1})

        return min(total_discount, base_amount)

    def action_create_invoice(self):
        """Create an invoice from this subscription with duplicate prevention."""
        self.ensure_one()
        if self.state != 'active':
            raise UserError(_("Invoices can only be created for Active subscriptions."))

        # Duplicate billing prevention check
        last_invoice = self.env['subscription.invoice'].search([
            ('subscription_id', '=', self.id),
            ('state', '!=', 'cancelled'),
        ], order='invoice_date desc', limit=1)

        freq_map = {
            'daily': relativedelta(days=1),
            'weekly': relativedelta(weeks=1),
            'monthly': relativedelta(months=1),
            'yearly': relativedelta(years=1)
        }
        step = freq_map.get(self.plan_id.billing_frequency, relativedelta(months=1))

        if last_invoice and last_invoice.invoice_date:
            next_allowed = last_invoice.invoice_date + step
            if fields.Date.today() < next_allowed:
                raise UserError(_("Already billed for the current period! Next invoice allowed on or after %s.") % next_allowed)

        term_days = {'immediate': 0, '15_days': 15, '30_days': 30, '60_days': 60}
        due_date = fields.Date.today() + relativedelta(days=term_days.get(self.payment_term, 30))

        invoice_lines = []
        for line in self.subscription_line_ids:
            discount_val = self._get_discount_amount(line)
            unit_price = line.unit_price + (line.variant_id.price_extra if line.variant_id else 0.0)
            invoice_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'description': line.product_id.name,
                'quantity': line.quantity,
                'unit_price': unit_price,
                'discount_amount': discount_val,
                'tax_ids': [(6, 0, line.tax_ids.ids)],
            }))

        invoice = self.env['subscription.invoice'].create({
            'subscription_id': self.id,
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.today(),
            'due_date': due_date,
            'invoice_line_ids': invoice_lines,
        })

        self.write({'next_billing_date': fields.Date.today() + step})
        self.message_post(body=_("Invoice %s generated automatically.") % invoice.name)

        return {
            'type': 'ir.actions.act_window',
            'name': _('Subscription Invoice'),
            'res_model': 'subscription.invoice',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }

    @api.model
    def action_mass_invoice(self):
        """Batch billing on billing day: processes all active subscriptions due."""
        today = fields.Date.today()
        due_subs = self.search([
            ('state', '=', 'active'),
            ('next_billing_date', '<=', today),
        ])
        invoices = self.env['subscription.invoice']
        for sub in due_subs:
            try:
                res = sub.action_create_invoice()
                if res and res.get('res_id'):
                    invoices |= self.env['subscription.invoice'].browse(res['res_id'])
            except Exception as e:
                _logger.warning("Billing error on subscription %s: %s", sub.name, e)

        return {
            'type': 'ir.actions.act_window',
            'name': _('Mass Generated Invoices (%d)') % len(invoices),
            'res_model': 'subscription.invoice',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', invoices.ids)],
        }

    ### Scheduled Actions ###

    @api.model
    def _cron_close_expired(self):
        today = fields.Date.today()
        expired_subs = self.search([
            ('state', '=', 'active'),
            ('expiry_date', '!=', False),
            ('expiry_date', '<', today),
            ('plan_id.auto_close', '=', True),
        ])
        for sub in expired_subs:
            sub.write({
                'state': 'closed',
                'close_reason': f"Auto-closed on expiry ({sub.expiry_date}) by daily cron.",
            })
            sub.message_post(body=_("Subscription automatically closed due to plan expiry."))
        _logger.info("Auto-close cron processed %d expired subscriptions.", len(expired_subs))

    @api.model
    def _cron_billing(self):
        _logger.info("Daily billing cron initiated.")
        self.action_mass_invoice()

    @api.constrains('start_date', 'expiry_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.expiry_date and rec.expiry_date < rec.start_date:
                raise ValidationError(_("Expiry date cannot be prior to start date."))
