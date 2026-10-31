# Login Controller & Role-Based Redirect

## Context
Custom login that redirects: admin → backend (/web), customers → portal (/my). Logout route.

## Prompt for Antigravity

```
In the Odoo 18 module "subscription_management", add to `controllers/auth.py`:

Route GET `/subscription/login`:
- Renders custom login page template if user not logged in
- If already logged in, redirects based on role

Route POST `/subscription/login`:
- Authenticates using request.session.authenticate(db, login, password)
- On success: check user groups
  - If user has group_subscription_admin → redirect to /web
  - If user has group_subscription_staff → redirect to /web
  - If portal user → redirect to /my
- On failure: re-render with error

Route `/subscription/logout`:
- Calls request.session.logout()
- Redirects to /subscription/login

Helper method to check user role:
def _get_user_redirect(self, user):
    if user.has_group('subscription_management.group_subscription_admin'):
        return '/web'
    elif user.has_group('subscription_management.group_subscription_staff'):
        return '/web'
    else:
        return '/my'
```

## Expected Output
- Updated `controllers/auth.py`

## Verification
- Login as admin → should go to /web
- Login as portal user → should go to /my
