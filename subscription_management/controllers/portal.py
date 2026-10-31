# -*- coding: utf-8 -*-
from odoo import http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

PAGE_SIZE = 10


class SubscriptionPortal(CustomerPortal):
    """Customer portal pages for subscriptions and subscription invoices.

    Invoices live under /my/subscription-invoices (not /my/invoices) so they never
    collide with the Accounting app's portal routes if it is installed.
    """

    def _subscription_portal_domain(self):
        """Records of the current user's customer company (matches the portal record rules)."""
        partner = request.env.user.partner_id
        return [('partner_id', 'child_of', [partner.commercial_partner_id.id])]

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        domain = self._subscription_portal_domain()
        if 'subscription_count' in counters:
            values['subscription_count'] = request.env['subscription.subscription'].search_count(domain)
        if 'subscription_invoice_count' in counters:
            values['subscription_invoice_count'] = request.env['subscription.invoice'].search_count(
                domain + [('state', '!=', 'draft')]
            )
        return values

    # ------------------------------------------------------------------
    # Subscriptions
    # ------------------------------------------------------------------

    @http.route(['/my/subscriptions', '/my/subscriptions/page/<int:page>'], type='http', auth='user', website=True)
    def portal_my_subscriptions(self, page=1, **kw):
        Subscription = request.env['subscription.subscription']
        domain = self._subscription_portal_domain()
        count = Subscription.search_count(domain)
        pager = portal_pager(url='/my/subscriptions', total=count, page=page, step=PAGE_SIZE)
        subscriptions = Subscription.search(domain, limit=PAGE_SIZE, offset=pager['offset'], order='create_date desc')
        request.session['my_subscriptions_history'] = subscriptions.ids[:100]
        values = self._prepare_portal_layout_values()
        values.update({
            'subscriptions': subscriptions,
            'pager': pager,
            'page_name': 'subscriptions',
            'default_url': '/my/subscriptions',
        })
        return request.render('subscription_management.portal_my_subscriptions', values)

    @http.route('/my/subscriptions/<int:subscription_id>', type='http', auth='public', website=True)
    def portal_subscription_detail(self, subscription_id, access_token=None, **kw):
        try:
            subscription = self._document_check_access('subscription.subscription', subscription_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        values = self._get_page_view_values(
            subscription, access_token, {'subscription': subscription, 'page_name': 'subscription'},
            'my_subscriptions_history', False,
        )
        return request.render('subscription_management.portal_subscription_detail', values)

    # ------------------------------------------------------------------
    # Invoices
    # ------------------------------------------------------------------

    @http.route(['/my/subscription-invoices', '/my/subscription-invoices/page/<int:page>'],
                type='http', auth='user', website=True)
    def portal_my_invoices(self, page=1, **kw):
        Invoice = request.env['subscription.invoice']
        # Drafts are internal work in progress; customers see invoices once confirmed.
        domain = self._subscription_portal_domain() + [('state', '!=', 'draft')]
        count = Invoice.search_count(domain)
        pager = portal_pager(url='/my/subscription-invoices', total=count, page=page, step=PAGE_SIZE)
        invoices = Invoice.search(domain, limit=PAGE_SIZE, offset=pager['offset'], order='invoice_date desc, id desc')
        request.session['my_subscription_invoices_history'] = invoices.ids[:100]
        values = self._prepare_portal_layout_values()
        values.update({
            'invoices': invoices,
            'pager': pager,
            'page_name': 'subscription_invoices',
            'default_url': '/my/subscription-invoices',
        })
        return request.render('subscription_management.portal_my_invoices', values)

    @http.route('/my/subscription-invoices/<int:invoice_id>', type='http', auth='public', website=True)
    def portal_invoice_detail(self, invoice_id, access_token=None, report_type=None, download=False, **kw):
        try:
            invoice = self._document_check_access('subscription.invoice', invoice_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        if invoice.state == 'draft':
            return request.redirect('/my')
        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(
                model=invoice, report_type=report_type,
                report_ref='subscription_management.action_report_invoice', download=download,
            )
        values = self._get_page_view_values(
            invoice, access_token, {'invoice': invoice, 'page_name': 'subscription_invoice'},
            'my_subscription_invoices_history', False,
        )
        return request.render('subscription_management.portal_invoice_detail', values)
