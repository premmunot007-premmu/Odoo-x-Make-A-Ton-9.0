# Password Reset Flow

## Context
Users who forget their password get a reset link via email. Token-based reset with 24h expiry.

## Prompt for Antigravity

```
In the Odoo 18 module "subscription_management", add password reset fields to res.users.

In `models/res_users.py`, add fields:
- reset_token: Char, string="Reset Token"
- reset_token_expiry: Datetime, string="Token Expiry"

Add method:
def _generate_reset_token(self):
    import uuid
    from datetime import timedelta
    token = str(uuid.uuid4())
    self.sudo().write({
        'reset_token': token,
        'reset_token_expiry': fields.Datetime.now() + timedelta(hours=24),
    })
    return token

def _verify_reset_token(self, token):
    user = self.sudo().search([('reset_token', '=', token)], limit=1)
    if not user or not user.reset_token_expiry:
        return False
    if fields.Datetime.now() > user.reset_token_expiry:
        return False
    return user

def _clear_reset_token(self):
    self.sudo().write({'reset_token': False, 'reset_token_expiry': False})
```

## Expected Output
- Updated `models/res_users.py`

## Verification
- Generate token, verify it's stored
- Wait or mock expiry, verify token rejected
