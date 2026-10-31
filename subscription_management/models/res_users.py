# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
import uuid
from datetime import timedelta

class ResUsers(models.Model):
    _inherit = 'res.users'

    reset_token = fields.Char(string="Password Reset Token", copy=False)
    reset_token_expiry = fields.Datetime(string="Reset Token Expiry", copy=False)

    @api.model
    def _validate_password_strength(self, password):
        """Enforce Brightloop security requirements:
        - Minimum 8 characters
        - At least 1 uppercase letter
        - At least 1 lowercase letter
        - At least 1 special character
        """
        if not password:
            return
        if len(password) < 8:
            raise ValidationError(_("Password must be at least 8 characters long."))
        if not re.search(r'[A-Z]', password):
            raise ValidationError(_("Password must contain at least one uppercase letter (A-Z)."))
        if not re.search(r'[a-z]', password):
            raise ValidationError(_("Password must contain at least one lowercase letter (a-z)."))
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            raise ValidationError(_("Password must contain at least one special character (!@#$%^&* etc.)."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('password'):
                self._validate_password_strength(vals['password'])
        return super().create(vals_list)

    def write(self, vals):
        if vals.get('password'):
            self._validate_password_strength(vals['password'])
        return super().write(vals)

    def generate_reset_token(self):
        """Generate a secure 24-hour token for password reset"""
        self.ensure_one()
        token = str(uuid.uuid4())
        self.sudo().write({
            'reset_token': token,
            'reset_token_expiry': fields.Datetime.now() + timedelta(hours=24),
        })
        return token

    @api.model
    def verify_reset_token(self, token):
        """Verify if the token is valid and not expired"""
        if not token:
            return False
        user = self.sudo().search([('reset_token', '=', token)], limit=1)
        if not user or not user.reset_token_expiry:
            return False
        if fields.Datetime.now() > user.reset_token_expiry:
            return False
        return user

    def clear_reset_token(self):
        self.sudo().write({
            'reset_token': False,
            'reset_token_expiry': False,
        })
