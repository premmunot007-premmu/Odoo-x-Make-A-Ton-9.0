# Subscription Model — Core State Machine

## Context
The subscription is the central model. It has a unique sequence number, links to customer and plan, manages lifecycle states (Draft→Quotation→Confirmed→Active→Closed), and computes billing dates.

## Prompt for Claude Code

```
In the Odoo 18 module "subscription_management", create the core Subscription model.

Create `models/subscription.py`:

class Subscription(models.Model):
    _name = 'subscription.subscription'
    _description = 'Subscription'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'name desc'

    Fields:
    - name: Char, string="Subscription Number", readonly=True, copy=False, default='New'
    - partner_id: Many2one('res.partner'), required, string="Customer", tracked=True, domain="[('customer_rank','>',0)]"
    - plan_id: Many2one('subscription.plan'), required, string="Plan", tracked=True
    - template_id: Many2one('subscription.quotation.template'), string="Quotation Template"
    - start_date: Date, required, default=fields.Date.today, tracked=True
    - expiry_date: Date, tracked=True
    - next_billing_date: Date, compute='_compute_next_billing_date', store=True
    - payment_term: Selection [('immediate','Immediate'), ('15_days','15 Days'), ('30_days','30 Days'), ('60_days','60 Days')], default='30_days'
    - state: Selection [('draft','Draft'), ('quotation','Quotation'), ('confirmed','Confirmed'), ('active','Active'), ('paused','Paused'), ('closed','Closed')], default='draft', tracked=True, string="Status"
    - subscription_line_ids: One2many('subscription.subscription.line', 'subscription_id')
    - invoice_ids: One2many('subscription.invoice', 'subscription_id')
    - invoice_count: Integer, compute='_compute_invoice_count'
    - amount_untaxed: Float, compute='_compute_amounts', store=True
    - amount_tax: Float, compute='_compute_amounts', store=True
    - amount_total: Float, compute='_compute_amounts', store=True
    - company_id: Many2one('res.company', default=lambda self: self.env.company)
    - currency_id: Many2one('res.currency', related='company_id.currency_id')
    - user_id: Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    - note: Html, string="Internal Notes"
    - is_expired: Boolean, compute='_compute_is_expired', store=True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('subscription.subscription') or 'New'
        return super().create(vals_list)

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
        # Compute next billing date based on frequency from start_date
        for rec in self:
            if rec.start_date and rec.plan_id:
                from dateutil.relativedelta import relativedelta
                freq_map = {'daily': relativedelta(days=1), 'weekly': relativedelta(weeks=1), 'monthly': relativedelta(months=1), 'yearly': relativedelta(years=1)}
                rec.next_billing_date = rec.start_date + freq_map.get(rec.plan_id.billing_frequency, relativedelta(months=1))
            else:
                rec.next_billing_date = False

    @api.depends('expiry_date')
    def _compute_is_expired(self):
        today = fields.Date.today()
        for rec in self:
            rec.is_expired = rec.expiry_date and rec.expiry_date < today

    def action_send_quotation(self):
        self.ensure_one()
        self.write({'state': 'quotation'})

    def action_confirm(self):
        self.ensure_one()
        self.write({'state': 'confirmed'})

    def action_activate(self):
        self.ensure_one()
        self.write({'state': 'active'})

    def action_pause(self):
        self.ensure_one()
        if not self.plan_id.allow_pause:
            raise UserError("This plan does not allow pausing.")
        self.write({'state': 'paused'})

    def action_close(self):
        self.ensure_one()
        self.write({'state': 'closed'})

    def action_renew(self):
        self.ensure_one()
        if not self.plan_id.allow_renew:
            raise UserError("This plan does not allow renewal.")
        from dateutil.relativedelta import relativedelta
        freq_map = {'daily': relativedelta(days=1), 'weekly': relativedelta(weeks=1), 'monthly': relativedelta(months=1), 'yearly': relativedelta(years=1)}
        new_expiry = fields.Date.today() + freq_map.get(self.plan_id.billing_frequency, relativedelta(months=1))
        self.write({'state': 'active', 'expiry_date': new_expiry})

    def action_load_template(self):
        """Load products from quotation template into subscription lines"""
        self.ensure_one()
        if self.template_id:
            lines = []
            for tpl_line in self.template_id.template_line_ids:
                lines.append((0, 0, {
                    'product_id': tpl_line.product_id.id,
                    'quantity': tpl_line.quantity,
                    'unit_price': tpl_line.unit_price,
                }))
            self.write({'subscription_line_ids': lines, 'plan_id': self.template_id.plan_id.id})

    @api.constrains('start_date', 'expiry_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.expiry_date and rec.start_date > rec.expiry_date:
                raise ValidationError("Expiry date must be after start date.")

    def _compute_access_url(self):
        super()._compute_access_url()
        for rec in self:
            rec.access_url = f'/my/subscriptions/{rec.id}'

Update models/__init__.py to import subscription.
Include all necessary Odoo imports (models, fields, api, exceptions).
```

## Expected Output
- `models/subscription.py`
- Updated `models/__init__.py`

## Verification
```bash
python odoo-bin -c odoo.conf -u subscription_management
# Create a subscription record in shell, test state transitions
```
