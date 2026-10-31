# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
import werkzeug.utils

class SubscriptionAuth(http.Controller):

    @http.route('/subscription/signup', type='http', auth='public', website=True, methods=['GET', 'POST'], csrf=True)
    def signup(self, **post):
        values = {'error': None, 'success': None}
        if request.httprequest.method == 'POST':
            name = post.get('name', '').strip()
            email = post.get('email', '').strip().lower()
            password = post.get('password', '')
            confirm_password = post.get('confirm_password', '')
            company_name = post.get('company_name', '').strip()

            if not name or not email or not password:
                values['error'] = _("Please fill in all required fields.")
                return request.render('subscription_management.signup_page', values)

            if password != confirm_password:
                values['error'] = _("Passwords do not match.")
                return request.render('subscription_management.signup_page', values)

            # Check email uniqueness
            existing = request.env['res.users'].sudo().search([('login', '=', email)], limit=1)
            if existing:
                values['error'] = _("An account with this email address already exists.")
                return request.render('subscription_management.signup_page', values)

            try:
                # Password validation
                request.env['res.users'].sudo()._validate_password_strength(password)

                # Create customer partner and portal user
                partner = request.env['res.partner'].sudo().create({
                    'name': company_name or name,
                    'email': email,
                    'customer_rank': 1,
                    'is_company': bool(company_name),
                })

                portal_group = request.env.ref('base.group_portal')
                customer_sub_group = request.env.ref('subscription_management.group_subscription_customer', raise_if_not_found=False)

                groups = [(4, portal_group.id)]
                if customer_sub_group:
                    groups.append((4, customer_sub_group.id))

                user = request.env['res.users'].sudo().create({
                    'name': name,
                    'login': email,
                    'email': email,
                    'password': password,
                    'partner_id': partner.id,
                    'groups_id': groups,
                })

                values['success'] = _("Account created successfully! You can now log in.")
                return request.render('subscription_management.login_page', values)

            except Exception as e:
                values['error'] = str(e)
                return request.render('subscription_management.signup_page', values)

        return request.render('subscription_management.signup_page', values)

    @http.route('/subscription/login', type='http', auth='public', website=True, methods=['GET', 'POST'], csrf=True)
    def login(self, **post):
        values = {'error': None}
        if request.httprequest.method == 'POST':
            login = post.get('login', '').strip().lower()
            password = post.get('password', '')
            try:
                uid = request.session.authenticate(request.db, login, password)
                if uid:
                    user = request.env['res.users'].browse(uid)
                    if user.has_group('subscription_management.group_subscription_admin') or user.has_group('subscription_management.group_subscription_staff'):
                        return werkzeug.utils.redirect('/web')
                    else:
                        return werkzeug.utils.redirect('/my/subscriptions')
            except Exception:
                values['error'] = _("Invalid email or password.")
                return request.render('subscription_management.login_page', values)

        return request.render('subscription_management.login_page', values)

    @http.route('/subscription/reset-password', type='http', auth='public', website=True, methods=['GET', 'POST'], csrf=True)
    def reset_password_request(self, **post):
        values = {'error': None, 'success': None}
        if request.httprequest.method == 'POST':
            email = post.get('email', '').strip().lower()
            user = request.env['res.users'].sudo().search([('login', '=', email)], limit=1)
            if user:
                token = user.generate_reset_token()
                template = request.env.ref('subscription_management.email_template_password_reset', raise_if_not_found=False)
                if template:
                    template.sudo().with_context(reset_url=f"/subscription/reset-password/confirm?token={token}").send_mail(user.id, force_send=False)
            # Generic message to avoid email enumeration
            values['success'] = _("If the account exists, a password reset link has been dispatched to your email.")
            return request.render('subscription_management.reset_password_page', values)

        return request.render('subscription_management.reset_password_page', values)

    @http.route('/subscription/reset-password/confirm', type='http', auth='public', website=True, methods=['GET', 'POST'], csrf=True)
    def reset_password_confirm(self, token=None, **post):
        values = {'error': None, 'success': None, 'token': token or post.get('token')}
        user = request.env['res.users'].sudo().verify_reset_token(values['token'])
        if not user:
            values['error'] = _("Invalid or expired reset token. Please request a new one.")
            return request.render('subscription_management.reset_password_page', values)

        if request.httprequest.method == 'POST':
            password = post.get('password', '')
            confirm_password = post.get('confirm_password', '')
            if password != confirm_password:
                values['error'] = _("Passwords do not match.")
                return request.render('subscription_management.reset_password_confirm_page', values)

            try:
                user._validate_password_strength(password)
                user.sudo().write({'password': password})
                user.clear_reset_token()
                values['success'] = _("Your password has been successfully updated! Please log in.")
                return request.render('subscription_management.login_page', values)
            except Exception as e:
                values['error'] = str(e)
                return request.render('subscription_management.reset_password_confirm_page', values)

        return request.render('subscription_management.reset_password_confirm_page', values)
