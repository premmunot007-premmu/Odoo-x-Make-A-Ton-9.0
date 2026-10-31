# Customer Portal — Controller & Templates

## Context
Customers access their subscriptions and invoices through a portal. Portal inherits from Odoo's portal.portal with "My Subscriptions" and "My Invoices" links showing counts.

## Prompt for Claude Code

```
In the Odoo 18 module "subscription_management", create the full customer portal.

Create `controllers/portal.py`:

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

class SubscriptionPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id
        if 'subscription_count' in counters:
            values['subscription_count'] = request.env['subscription.subscription'].search_count([
                ('partner_id', '=', partner.id)
            ])
        if 'invoice_count' in counters:
            values['invoice_count'] = request.env['subscription.invoice'].search_count([
                ('partner_id', '=', partner.id)
            ])
        return values

    @http.route(['/my/subscriptions', '/my/subscriptions/page/<int:page>'], type='http', auth='user', website=True)
    def portal_my_subscriptions(self, page=1, **kw):
        partner = request.env.user.partner_id
        domain = [('partner_id', '=', partner.id)]
        Subscription = request.env['subscription.subscription']
        count = Subscription.search_count(domain)
        pager = portal_pager(url='/my/subscriptions', total=count, page=page, step=10)
        subscriptions = Subscription.search(domain, limit=10, offset=pager['offset'], order='create_date desc')
        return request.render('subscription_management.portal_my_subscriptions', {
            'subscriptions': subscriptions,
            'pager': pager,
            'page_name': 'subscriptions',
        })

    @http.route('/my/subscriptions/<int:subscription_id>', type='http', auth='user', website=True)
    def portal_subscription_detail(self, subscription_id, **kw):
        subscription = request.env['subscription.subscription'].browse(subscription_id)
        if subscription.partner_id != request.env.user.partner_id:
            return request.redirect('/my')
        return request.render('subscription_management.portal_subscription_detail', {
            'subscription': subscription,
            'page_name': 'subscription',
        })

    @http.route(['/my/invoices', '/my/invoices/page/<int:page>'], type='http', auth='user', website=True)
    def portal_my_invoices(self, page=1, **kw):
        partner = request.env.user.partner_id
        domain = [('partner_id', '=', partner.id)]
        Invoice = request.env['subscription.invoice']
        count = Invoice.search_count(domain)
        pager = portal_pager(url='/my/invoices', total=count, page=page, step=10)
        invoices = Invoice.search(domain, limit=10, offset=pager['offset'], order='invoice_date desc')
        return request.render('subscription_management.portal_my_invoices', {
            'invoices': invoices,
            'pager': pager,
            'page_name': 'invoices',
        })

    @http.route('/my/invoices/<int:invoice_id>', type='http', auth='user', website=True)
    def portal_invoice_detail(self, invoice_id, **kw):
        invoice = request.env['subscription.invoice'].browse(invoice_id)
        if invoice.partner_id != request.env.user.partner_id:
            return request.redirect('/my')
        return request.render('subscription_management.portal_invoice_detail', {
            'invoice': invoice,
            'page_name': 'invoice',
        })

Update `controllers/__init__.py` to import portal.

Create `views/portal_templates.xml` with QWeb templates:

1. Inherit portal.portal to add "My Subscriptions" and "My Invoices" links with count badges
2. portal_my_subscriptions template: table listing subscriptions (name, plan, status badge, dates, amount)
3. portal_subscription_detail template: full subscription info, lines table, linked invoices
4. portal_my_invoices template: table listing invoices (number, date, amount, status)
5. portal_invoice_detail template: full invoice with lines, payment status, amounts

Use Odoo portal layout templates (portal.portal_layout, portal.portal_breadcrumbs).
Style with Bootstrap classes for responsive design.

Update __manifest__.py to include 'views/portal_templates.xml'.
```

## Expected Output
- `controllers/portal.py`
- `controllers/__init__.py` (updated)
- `views/portal_templates.xml`

## Verification
- Login as portal user, visit /my, verify "My Subscriptions" and "My Invoices" appear
