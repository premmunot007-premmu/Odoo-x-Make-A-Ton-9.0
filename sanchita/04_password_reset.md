# Password Reset Flow

## Context

We are building a **Subscription Management System** as an Odoo 18 custom module (`subscription_management`). This file creates the password reset flow allowing users to request a password reset link via email and set a new password.

The flow:
1. User clicks "Forgot password?" on login page
2. User enters their email on the reset request page
3. System generates a secure token, stores it with expiry (24 hours)
4. System sends email with reset link containing the token
5. User clicks link, enters new password
6. System validates password, updates user record, invalidates token

### Related files:
- `controllers/auth.py` — Add reset routes here (or create separate file)
- `models/res_users.py` — Store reset token fields
- `data/email_templates.xml` — Reset email template (built in next prompt)

---

## Prompt for Antigravity

```
Extend the Odoo 18 custom module `subscription_management` to add a password reset flow.

### Files to create/modify:

#### 1. Add fields to `models/res_users.py` (EXTEND existing file)

Add these fields to the `ResUsers` class that already inherits `res.users`:

```python
import secrets
import hashlib
from datetime import datetime, timedelta

class ResUsers(models.Model):
    _inherit = 'res.users'

    # Existing password validation code stays...

    # ADD these new fields:
    password_reset_token = fields.Char(
        string='Password Reset Token',
        copy=False,
        groups='base.group_system',
    )
    password_reset_token_expiry = fields.Datetime(
        string='Token Expiry',
        copy=False,
        groups='base.group_system',
    )
```

Add these methods:

```python
def _generate_reset_token(self):
    """Generate a secure password reset token and store it with 24h expiry."""
    self.ensure_one()
    raw_token = secrets.token_urlsafe(32)
    # Store hashed token for security
    hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()
    self.sudo().write({
        'password_reset_token': hashed_token,
        'password_reset_token_expiry': fields.Datetime.now() + timedelta(hours=24),
    })
    return raw_token  # Return unhashed token for the email link

def _verify_reset_token(self, token):
    """Verify a password reset token is valid and not expired."""
    self.ensure_one()
    hashed_token = hashlib.sha256(token.encode()).hexdigest()
    if self.password_reset_token != hashed_token:
        return False
    if not self.password_reset_token_expiry or self.password_reset_token_expiry < fields.Datetime.now():
        return False
    return True

def _clear_reset_token(self):
    """Clear the reset token after successful password change."""
    self.sudo().write({
        'password_reset_token': False,
        'password_reset_token_expiry': False,
    })
```

#### 2. Add routes to `controllers/auth.py` (EXTEND existing file)

Add these routes to the `AuthController` class:

**Route: GET `/subscription/reset-password`**
- Renders reset request form (enter email)
- Template: `subscription_management.reset_password_request_page`
- `auth='public'`

**Route: POST `/subscription/reset-password`**
- Accepts JSON with `email` field
- Searches `res.users` for user with that login/email
- If found: generates token, sends email template
- ALWAYS returns success message (security: don't reveal if email exists)
  ```python
  return {'success': True, 'message': 'If an account with that email exists, a reset link has been sent.'}
  ```
- The email sending:
  ```python
  template = request.env.ref('subscription_management.email_template_password_reset')
  # Pass the raw (unhashed) token via context
  template.sudo().with_context(reset_token=raw_token).send_mail(user.id, force_send=True)
  ```

**Route: GET `/subscription/reset-password/confirm`**
- Accepts query params: `token` and `login` (email)
- Validates token against user
- If valid: renders new password form
- If invalid: renders error page
- Template: `subscription_management.reset_password_confirm_page`
- `auth='public'`

**Route: POST `/subscription/reset-password/confirm`**
- Accepts JSON: `token`, `login`, `password`, `confirm_password`
- Validates token
- Validates new password strength (reuse existing validation)
- Checks password == confirm_password
- If all valid:
  ```python
  user.sudo().write({'password': new_password})
  user._clear_reset_token()
  return {'success': True, 'message': 'Password updated successfully.', 'redirect': '/subscription/login'}
  ```
- If invalid: return error JSON

#### 3. Add QWeb templates to `views/auth_templates.xml` (EXTEND existing file)

Add TWO new templates:

**Template: `reset_password_request_page`**
- Simple form with email input
- "Send Reset Link" button
- AJAX submission
- Success message: "Check your email for a reset link"
- Link back to login page

**Template: `reset_password_confirm_page`**
- Hidden fields for `token` and `login` (pre-filled from URL params)
- New password field with strength indicator
- Confirm password field
- "Set New Password" button
- AJAX submission
- On success, redirect to login page

Both templates should use the same styling as the signup page (Bootstrap 5, card layout, Brightloop branding).

Generate all the code additions needed. Show what to add to each file, clearly marking where the new code goes relative to existing code.
```

---

## Expected Output

Modifications to three files:

1. **`models/res_users.py`** — New fields (`password_reset_token`, `password_reset_token_expiry`) and methods (`_generate_reset_token`, `_verify_reset_token`, `_clear_reset_token`)
2. **`controllers/auth.py`** — Four new routes for password reset request and confirmation (GET and POST each)
3. **`views/auth_templates.xml`** — Two new QWeb templates for reset request and reset confirmation pages

---

## Verification

1. **Token generation** — Check that `secrets.token_urlsafe(32)` produces a secure random token
2. **Token hashing** — Stored token should be SHA-256 hashed (raw token only in email link)
3. **Token expiry** — Verify 24-hour expiry is correctly calculated
4. **Security** — Reset request always returns same message (doesn't reveal email existence)
5. **Password validation** — New password goes through same strength validation
6. **Token cleanup** — Token is cleared after successful password change
7. **Template rendering** — GET routes render correct templates with required context
8. **AJAX flow** — POST routes return proper JSON responses
9. **Edge case: expired token** — Should return clear error message
10. **Edge case: already-used token** — After clear, token verification should fail
