# -*- coding: utf-8 -*-
"""
Password validation module for res.users.

This module inherits res.users to enforce server-side password security rules
for the Subscription Management System according to Brightloop Software security
requirements.
"""

import re
from odoo import api, fields, models
from odoo.exceptions import ValidationError

# Special characters allowed and checked for password complexity
SPECIAL_CHARS_PATTERN = r'[!@#$%^&*()_+\-=\[\]{}|;\':",.<>?/\\]'


class ResUsers(models.Model):
    """
    Inherit res.users to add server-side password validation rules.
    """
    _inherit = 'res.users'

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create to validate password strength on user creation.
        """
        for vals in vals_list:
            if vals.get('password') is not None:
                self._validate_password_strength(vals['password'])
        return super().create(vals_list)

    def write(self, vals):
        """
        Override write to validate password strength on user updates.
        """
        if vals.get('password') is not None:
            self._validate_password_strength(vals['password'])
        return super().write(vals)

    @api.model
    def check_password_strength(self, password):
        """
        Check password strength without raising an error.

        Returns dict with results:
        {
            'is_valid': True/False,
            'score': 0-4,
            'errors': ['list of failure messages'],
            'checks': {
                'length': True/False,
                'uppercase': True/False,
                'lowercase': True/False,
                'special_char': True/False,
            }
        }

        :param str or None password: The password to validate.
        :return dict: Validation outcome, score, and error details.
        """
        pwd = password if password is not None else ''

        # Inline checks for each complexity rule:
        # 1. Length check: Minimum 8 characters
        has_length = len(pwd) >= 8

        # 2. Uppercase letter check: At least 1 ASCII uppercase letter (A-Z)
        # Note: Unicode characters are allowed in the password, but do not satisfy this ASCII rule
        has_upper = bool(re.search(r'[A-Z]', pwd))

        # 3. Lowercase letter check: At least 1 ASCII lowercase letter (a-z)
        # Note: Unicode characters are allowed in the password, but do not satisfy this ASCII rule
        has_lower = bool(re.search(r'[a-z]', pwd))

        # 4. Special character check: At least 1 character from SPECIAL_CHARS_PATTERN
        has_special = bool(re.search(SPECIAL_CHARS_PATTERN, pwd))

        checks = {
            'length': has_length,
            'uppercase': has_upper,
            'lowercase': has_lower,
            'special_char': has_special,
        }

        errors = []
        if not has_length:
            errors.append(f"Must be at least 8 characters long (currently {len(pwd)})")
        if not has_upper:
            errors.append("Must contain at least one uppercase letter (A-Z)")
        if not has_lower:
            errors.append("Must contain at least one lowercase letter (a-z)")
        if not has_special:
            errors.append("Must contain at least one special character (!@#$%^&*()_+-=[]{}|;':\",.<>?/)")

        score = sum(1 for passed in checks.values() if passed)
        is_valid = score == 4

        return {
            'is_valid': is_valid,
            'score': score,
            'errors': errors,
            'checks': checks,
        }

    @api.model
    def _validate_password_strength(self, password):
        """
        Validate password meets Brightloop Software security requirements.

        Rules:
        - Minimum 8 characters
        - At least 1 uppercase letter (A-Z)
        - At least 1 lowercase letter (a-z)
        - At least 1 special character

        Raises ValidationError with specific message indicating which rule(s) failed.
        """
        # Edge case: None skips validation
        if password is None:
            return

        result = self.check_password_strength(password)
        if not result['is_valid']:
            failure_list = "\n".join(f"- {error}" for error in result['errors'])
            raise ValidationError(
                f"Password does not meet security requirements:\n{failure_list}"
            )
