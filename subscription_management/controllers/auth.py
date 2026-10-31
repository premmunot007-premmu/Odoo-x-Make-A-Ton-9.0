# -*- coding: utf-8 -*-
import json
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

    def _extract_payload(self, **post):
        """Extract payload from JSON body, request params, or keyword arguments."""
        data = {}
        try:
            if hasattr(request, 'get_json_data'):
                json_data = request.get_json_data()
                if isinstance(json_data, dict):
                    data.update(json_data)
        except Exception:
            pass
        if not data:
            try:
                raw_data = getattr(request, 'httprequest', None) and request.httprequest.data
                if raw_data:
                    parsed = json.loads(raw_data.decode('utf-8'))
                    if isinstance(parsed, dict):
                        if 'params' in parsed and isinstance(parsed['params'], dict):
                            data.update(parsed['params'])
                        else:
                            data.update(parsed)
            except Exception:
                pass
        if not data and hasattr(request, 'params') and isinstance(request.params, dict):
            data.update(request.params)
        if post:
            data.update(post)
        return data

    def _json_response(self, data, status=200):
        """Return a JSON HTTP response."""
        try:
            if hasattr(request, 'make_json_response'):
                return request.make_json_response(data, status=status)
            if hasattr(request, 'make_response'):
                return request.make_response(
                    json.dumps(data),
                    headers=[('Content-Type', 'application/json')],
                    status=status,
                )
        except Exception:
            pass
        return data

    @http.route('/subscription/reset-password', type='http', auth='public', website=True, methods=['GET', 'POST'], csrf=False)
    def reset_password_request(self, **post):
        if request.httprequest.method == 'POST':
            data = self._extract_payload(**post)
            email = (data.get('email') or '').strip().lower()

            if email:
                user = request.env['res.users'].sudo().search([
                    '|', ('login', '=', email), ('email', '=', email)
                ], limit=1)
                if user:
                    raw_token = user._generate_reset_token()
                    try:
                        template = request.env.ref('subscription_management.email_template_password_reset')
                        if template:
                            template.sudo().with_context(
                                reset_token=raw_token,
                                reset_login=user.login,
                            ).send_mail(user.id, force_send=True)
                    except Exception:
                        pass

            return self._json_response({
                'success': True,
                'message': 'If an account with that email exists, a reset link has been sent.'
            })

        return request.render('subscription_management.reset_password_request_page', {})

    @http.route('/subscription/reset-password/confirm', type='http', auth='public', website=True, methods=['GET', 'POST'], csrf=False)
    def reset_password_confirm(self, token=None, login=None, **post):
        if request.httprequest.method == 'POST':
            data = self._extract_payload(**post)
            token = data.get('token') or token
            login = (data.get('login') or login or '').strip().lower()
            password = data.get('password')
            confirm_password = data.get('confirm_password')

            if not token or not login or not password or not confirm_password:
                return self._json_response({
                    'success': False,
                    'error': _("All fields (token, login, password, confirm_password) are required."),
                    'message': _("All fields (token, login, password, confirm_password) are required.")
                }, status=400)

            user = request.env['res.users'].sudo().search([
                '|', ('login', '=', login), ('email', '=', login)
            ], limit=1)
            if not user:
                return self._json_response({
                    'success': False,
                    'error': _("User not found."),
                    'message': _("User not found.")
                }, status=400)

            if not user._verify_reset_token(token):
                return self._json_response({
                    'success': False,
                    'error': _("Invalid or expired reset token."),
                    'message': _("Invalid or expired reset token.")
                }, status=400)

            if password != confirm_password:
                return self._json_response({
                    'success': False,
                    'error': _("Passwords do not match."),
                    'message': _("Passwords do not match.")
                }, status=400)

            try:
                user._validate_password_strength(password)
                user.sudo().write({'password': password})
                user._clear_reset_token()
                return self._json_response({
                    'success': True,
                    'message': 'Password updated successfully.',
                    'redirect': '/subscription/login'
                })
            except Exception as e:
                return self._json_response({
                    'success': False,
                    'error': str(e),
                    'message': str(e)
                }, status=400)

        # GET request handling
        token = token or post.get('token') or (hasattr(request, 'params') and request.params.get('token'))
        login = (login or post.get('login') or (hasattr(request, 'params') and request.params.get('login')) or '').strip().lower()

        user = False
        if login:
            user = request.env['res.users'].sudo().search([
                '|', ('login', '=', login), ('email', '=', login)
            ], limit=1)

        is_valid = False
        if user and token:
            try:
                is_valid = user._verify_reset_token(token)
            except Exception:
                is_valid = False

        if is_valid:
            return request.render('subscription_management.reset_password_confirm_page', {
                'token': token,
                'login': login,
            })

        return request.render('subscription_management.reset_password_request_page', {
            'error': _("Invalid or expired reset token. Please request a new one.")
        })
