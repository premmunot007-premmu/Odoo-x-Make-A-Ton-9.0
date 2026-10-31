# Password Validation on res.users

## Context

We are building a **Subscription Management System** as an Odoo 18 custom module (`subscription_management`). This file creates a model that inherits `res.users` to enforce password validation rules at the model level.

The password policy requires:
- Minimum 8 characters
- At least 1 uppercase letter (A-Z)
- At least 1 lowercase letter (a-z)
- At least 1 special character (!@#$%^&*() etc.)

This validation runs whenever a user is created or their password is changed, ensuring the policy is enforced regardless of whether the user signs up via the custom form, the admin creates them, or they change their password.

### Related files:
- `controllers/auth.py` — Also validates on the controller side (double validation)
- `models/__init__.py` — Must import this file

---

## Prompt for Antigravity

```
Create the file `models/res_users.py` for an Odoo 18 custom module named `subscription_management`.

This file inherits `res.users` to add server-side password validation rules.

### Requirements:

1. **File location:** `models/res_users.py`

2. **Also create/update** `models/__init__.py` to import `res_users`.

3. **Class definition:**
   ```python
   from odoo import models, fields, api
   from odoo.exceptions import ValidationError
   import re

   class ResUsers(models.Model):
       _inherit = 'res.users'
   ```

4. **Override `create()` method:**
   ```python
   @api.model_create_multi
   def create(self, vals_list):
       for vals in vals_list:
           if vals.get('password'):
               self._validate_password_strength(vals['password'])
       return super().create(vals_list)
   ```

5. **Override `write()` method:**
   ```python
   def write(self, vals):
       if vals.get('password'):
           self._validate_password_strength(vals['password'])
       return super().write(vals)
   ```

6. **Password validation method:**
   ```python
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
   ```

   The method should:
   - Check each rule independently
   - Collect ALL failures into a list
   - Raise a SINGLE `ValidationError` listing all failures
   - Example error message:
     ```
     Password does not meet security requirements:
     - Must be at least 8 characters long (currently 5)
     - Must contain at least one uppercase letter (A-Z)
     - Must contain at least one special character (!@#$%^&*()_+-=[]{}|;':",.<>?/)
     ```

7. **Special character regex pattern:**
   ```python
   SPECIAL_CHARS_PATTERN = r'[!@#$%^&*()_+\-=\[\]{}|;\':",.<>?/\\]'
   ```

8. **Add a helper method for external use:**
   ```python
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
       """
   ```
   This is useful for the controller to check before attempting create.

9. **Docstrings and comments:**
   - Module-level docstring explaining purpose
   - Method-level docstrings
   - Inline comments for regex patterns

10. **Edge cases to handle:**
    - `password` is `None` → skip validation
    - `password` is empty string → fail all checks
    - Very long passwords → no upper limit needed
    - Unicode characters in password → allowed, but don't count as uppercase/lowercase for ASCII rules

### Also generate `models/__init__.py`:
```python
from . import res_users
```

Generate the complete, production-ready Python file.
```

---

## Expected Output

Two files:

1. **`models/__init__.py`** — Import file
2. **`models/res_users.py`** — Contains:
   - `ResUsers` class inheriting `res.users`
   - Overridden `create()` with password validation
   - Overridden `write()` with password validation
   - `_validate_password_strength()` method that raises `ValidationError`
   - `check_password_strength()` helper that returns a dict

---

## Verification

1. **Test valid password** — `"MyP@ssw0rd"` should pass all checks
2. **Test too short** — `"Ab@1"` should fail (too short)
3. **Test no uppercase** — `"mypassword@1"` should fail
4. **Test no lowercase** — `"MYPASSWORD@1"` should fail
5. **Test no special char** — `"MyPassword1"` should fail
6. **Test multiple failures** — `"abc"` should list all failures
7. **Test create flow** — Creating a user with weak password should raise `ValidationError`
8. **Test write flow** — Changing password to weak one should raise `ValidationError`
9. **Check `check_password_strength()`** — Returns correct dict structure
