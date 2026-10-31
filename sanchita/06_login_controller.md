# Login Controller

## Context

We are building a **Subscription Management System** as an Odoo 18 custom module (`subscription_management`). This file creates custom login and logout routes that match the app's branding and redirect users based on their role.

Login behavior:
- Custom login page at `/subscription/login` with Brightloop Software branding
- On successful login: redirect Admin → `/web` (backend), Portal Customer → `/my` (portal)
- On failed login: show error message
- Logout: clear session and redirect to login page

### Related files:
- `controllers/auth.py` — Add login/logout routes here
- `views/auth_templates.xml` — Add login template here
- `models/res_users.py` — User model with roles

---

## Prompt for Antigravity

```
Extend `controllers/auth.py` in the Odoo 18 custom module `subscription_management` to add login and logout routes.

### Requirements:

#### 1. Route: GET `/subscription/login`
- Renders the QWeb template `subscription_management.login_page`
- `auth='public'`
- `website=True` (if website module is installed, otherwise omit)
- Passes context: `{'error': error_message}` if redirected with error

```python
@http.route('/subscription/login', type='http', auth='public', website=False, csrf=True)
def login_page(self, redirect=None, **kw):
    """Render the custom login page."""
    values = {
        'error': kw.get('error', ''),
        'login': kw.get('login', ''),
        'redirect': redirect,
    }
    return request.render('subscription_management.login_page', values)
```

#### 2. Route: POST `/subscription/login`
- Accepts form data: `login` (email), `password`
- `type='http'` (standard form post, not JSON)
- `auth='none'` (user is not authenticated yet)
- Uses `request.session.authenticate()` to verify credentials

```python
@http.route('/subscription/login', type='http', auth='none', methods=['POST'], csrf=True)
def login(self, login=None, password=None, redirect=None, **kw):
    """Handle login form submission."""
    if not login or not password:
        return request.redirect('/subscription/login?error=Please+enter+email+and+password')
    
    try:
        db = request.session.db or request.env.cr.dbname
        uid = request.session.authenticate(db, login, password)
        if uid:
            # Determine redirect based on user role
            user = request.env['res.users'].sudo().browse(uid)
            if user.has_group('base.group_system') or user.has_group('base.group_user'):
                # Admin or internal user → backend
                return request.redirect(redirect or '/web')
            else:
                # Portal user → portal home
                return request.redirect(redirect or '/my')
        else:
            return request.redirect('/subscription/login?error=Invalid+email+or+password')
    except Exception as e:
        _logger.error('Login error: %s', str(e))
        return request.redirect('/subscription/login?error=Invalid+email+or+password')
```

#### 3. Route: GET `/subscription/logout`
- Clears the user session
- Redirects to login page
- `auth='user'` (must be logged in to log out)

```python
@http.route('/subscription/logout', type='http', auth='user')
def logout(self, **kw):
    """Log out and redirect to login page."""
    request.session.logout()
    return request.redirect('/subscription/login')
```

#### 4. Additional helper method:

```python
def _get_user_redirect_url(self, user):
    """Determine the appropriate redirect URL based on user's role."""
    if user.has_group('base.group_system'):
        return '/web'  # Admin
    elif user.has_group('base.group_user'):
        return '/web'  # Staff/Internal user
    elif user.has_group('base.group_portal'):
        return '/my'   # Portal customer
    else:
        return '/subscription/login'
```

### Important considerations:
- `request.session.authenticate()` takes `(db, login, password)` args
- Use `request.session.db` to get the current database name
- Handle `odoo.exceptions.AccessDenied` for invalid credentials
- The login POST should be `type='http'` not `type='json'` for standard form submission
- Add proper CSRF protection with `csrf=True`
- Import `from odoo.exceptions import AccessDenied` at the top

Generate the complete additions to `controllers/auth.py`, clearly showing where these routes fit with the existing signup routes.
```

---

## Expected Output

Additions to `controllers/auth.py`:
- `login_page()` — GET route rendering login template
- `login()` — POST route handling authentication
- `logout()` — GET route clearing session
- `_get_user_redirect_url()` — Helper for role-based redirect

---

## Verification

1. **Route paths** — `/subscription/login` (GET & POST), `/subscription/logout` (GET)
2. **Auth types** — GET login: `auth='public'`, POST login: `auth='none'`, logout: `auth='user'`
3. **Session authenticate** — Uses `request.session.authenticate(db, login, password)`
4. **Role-based redirect** — Admin → `/web`, Portal → `/my`
5. **Error handling** — Invalid credentials show error message, don't crash
6. **CSRF** — All routes have CSRF protection
7. **Logout** — Properly calls `request.session.logout()`
8. **Edge case** — Empty email/password handled gracefully
