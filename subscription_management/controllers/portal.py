# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager

class SubscriptionCustomerPortal(CustomerPortal):

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
        SubModel = request.env['subscription.subscription']
        count = SubModel.search_count(domain)
        pager = portal_pager(url='/my/subscriptions', total=count, page=page, step=10)
        subscriptions = SubModel.search(domain, limit=10, offset=pager['offset'], order='create_date desc')
        return request.render('subscription_management.portal_my_subscriptions', {
            'subscriptions': subscriptions,
            'pager': pager,
            'page_name': 'subscriptions',
        })

    @http.route('/my/subscriptions/<int:subscription_id>', type='http', auth='user', website=True)
    def portal_my_subscription_detail(self, subscription_id, **kw):
        partner = request.env.user.partner_id
        sub = request.env['subscription.subscription'].browse(subscription_id)
        if not sub.exists() or sub.partner_id.id != partner.id:
            return request.redirect('/my/subscriptions')
        return request.render('subscription_management.portal_subscription_detail', {
            'subscription': sub,
            'page_name': 'subscription',
        })

    @http.route(['/my/invoices', '/my/invoices/page/<int:page>'], type='http', auth='user', website=True)
    def portal_my_invoices(self, page=1, **kw):
        partner = request.env.user.partner_id
        domain = [('partner_id', '=', partner.id)]
        InvModel = request.env['subscription.invoice']
        count = InvModel.search_count(domain)
        pager = portal_pager(url='/my/invoices', total=count, page=page, step=10)
        invoices = InvModel.search(domain, limit=10, offset=pager['offset'], order='invoice_date desc')
        return request.render('subscription_management.portal_my_invoices', {
            'invoices': invoices,
            'pager': pager,
            'page_name': 'invoices',
        })

    @http.route('/my/invoices/<int:invoice_id>', type='http', auth='user', website=True)
    def portal_my_invoice_detail(self, invoice_id, **kw):
        partner = request.env.user.partner_id
        inv = request.env['subscription.invoice'].browse(invoice_id)
        if not inv.exists() or inv.partner_id.id != partner.id:
            return request.redirect('/my/invoices')
        return request.render('subscription_management.portal_invoice_detail', {
            'invoice': inv,
            'page_name': 'invoice',
        })
