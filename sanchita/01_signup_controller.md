# Signup Controller

## Context

We are building a **Subscription Management System** as an Odoo 18 custom module (`subscription_management`). This file creates the signup controller that allows new customers to register via a custom signup page at `/subscription/signup`.

The signup flow must:
- Accept email, password, confirm_password, name, and optional company name
- Validate email uniqueness against `res.partner` and `res.users`
- Validate password strength (min 8 chars, 1 uppercase, 1 lowercase, 1 special char)
- Create a `res.users` record with portal group on success
- Return JSON responses for AJAX compatibility
- Serve a QWeb signup template on GET requests

### Module Structure (relevant files):
```
subscription_management/
├── controllers/
│   ├── __init__.py
│   └── auth.py          ← THIS FILE
├── models/
│   └── res_users.py     (password validation — built separately)
├── views/
│   └── auth_templates.xml (signup template — built separately)
```

### Dependencies:
- `res.users` model (Odoo core)
- `res.partner` model (Odoo core)
- `base.group_portal` group (Odoo core)

---

## Prompt for Antigravity

```
Create the file `controllers/auth.py` for an Odoo 18 custom module named `subscription_management`.

This controller handles user signup for a Subscription Management System built for "Brightloop Software".

### Requirements:

1. **File location:** `controllers/auth.py`

2. **Also create/update** `controllers/__init__.py` to import `auth`.

3. **Class:** `AuthController` inheriting from `odoo.http.Controller`

4. **Route: GET `/subscription/signup`**
   - Renders the QWeb template `subscription_management.signup_page`
   - Passes any error/success messages to the template context
   - Publicly accessible (no auth required): `auth='public'`

5. **Route: POST `/subscription/signup`**
   - Accepts form data: `name`, `email`, `password`, `confirm_password`, `company_name` (optional)
   - `type='json'` so it returns JSON responses
   - `auth='public'`, `csrf=True`

6. **Validation logic (in order):**
   a. All required fields present (name, email, password, confirm_password)
   b. Email format validation (basic regex)
   c. Password matches confirm_password
   d. Password strength check:
      - Minimum 8 characters
      - At least 1 uppercase letter (A-Z)
      - At least 1 lowercase letter (a-z)
      - At least 1 special character (!@#$%^&*()_+-=[]{}|;':",.<>?/)
   e. Email uniqueness: check `res.users` for existing `login` field match
      Also check `res.partner` for existing email

7. **On validation success:**
   - Use `sudo()` to create a new `res.users` record:
     ```python
     user_vals = {
         'name': name,
         'login': email,
         'email': email,
         'password': password,
         'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])],
     }
     ```
   - If `company_name` is provided, set it on the partner:
     ```python
     user.partner_id.write({
         'company_name': company_name,
     })
     ```
   - Return JSON: `{'success': True, 'message': 'Account created successfully. You can now log in.', 'redirect': '/subscription/login'}`

8. **On validation failure:**
   - Return JSON: `{'success': False, 'error': '<specific error message>'}`
   - Error messages should be user-friendly:
     - "All fields are required."
     - "Please enter a valid email address."
     - "Passwords do not match."
     - "Password must be at least 8 characters long."
     - "Password must contain at least one uppercase letter."
     - "Password must contain at least one lowercase letter."
     - "Password must contain at least one special character."
     - "An account with this email already exists."

9. **Error handling:**
   - Wrap user creation in try/except
   - Log errors using `_logger`
   - Return generic error on unexpected exceptions: `{'success': False, 'error': 'An unexpected error occurred. Please try again.'}`

10. **Imports needed:**
    ```python
    import re
    import logging
    from odoo import http
    from odoo.http import request
    ```

### Full code for `controllers/auth.py`:

Generate the complete, production-ready file with proper docstrings and comments.

### Also generate `controllers/__init__.py`:
```python
from . import auth
```
```

---

## Expected Output

Two files:

1. **`controllers/__init__.py`** — Simple import file
2. **`controllers/auth.py`** — Contains `AuthController` class with:
   - `signup_page()` GET route
   - `signup()` POST route
   - Password validation helper method `_validate_password(password)`
   - Email validation helper method `_validate_email(email)`
   - All error handling and logging

---

## Verification

After generating the code:

1. **Check imports** — Ensure `re`, `logging`, `odoo.http`, `request` are imported
2. **Check routes** — Both GET and POST routes should be defined with correct paths
3. **Check auth** — Both routes should have `auth='public'`
4. **Check password validation** — All 4 rules (length, uppercase, lowercase, special char) must be present
5. **Check email uniqueness** — Must search both `res.users` and `res.partner`
6. **Check user creation** — Must use `sudo()` and assign `base.group_portal`
7. **Check JSON responses** — Both success and error responses should be well-structured
8. **Test mentally** — Walk through: what happens if email exists? If password is "abc"? If everything is valid?
