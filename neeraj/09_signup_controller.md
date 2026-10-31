# Signup Controller

## Context
New customers sign up with email+password. The controller validates input, creates a portal user, and returns to login page.

## Prompt for Antigravity

```
In the Odoo 18 module "subscription_management", create `controllers/auth.py`.

Create a controller class SubscriptionAuth inheriting from http.Controller:

Route GET `/subscription/signup`:
- Renders a signup page template

Route POST `/subscription/signup`:
- Receives: name, email, password, confirm_password
- Validates: email not already in res.users, passwords match, password meets strength requirements (8+ chars, upper, lower, special)
- Creates res.users with portal group (base.group_portal)
- Creates res.partner linked to the user
- On success: redirect to /web/login with success message
- On error: re-render signup with error message

Route GET `/subscription/reset-password`:
- Renders password reset request page

Route POST `/subscription/reset-password`:
- Receives email, generates secure token (uuid4), stores in a new field on res.users (reset_token, reset_token_expiry)
- Sends email with reset link using mail.template
- Shows confirmation message

Route GET `/subscription/reset-password/confirm/<token>`:
- Validates token exists and not expired (24h)
- Renders new password form

Route POST `/subscription/reset-password/confirm`:
- Validates token, sets new password, clears token
- Redirects to login

Update controllers/__init__.py to import auth.
```

## Expected Output
- `controllers/auth.py`
- Updated `controllers/__init__.py`

## Verification
- Visit /subscription/signup in browser, test the form
