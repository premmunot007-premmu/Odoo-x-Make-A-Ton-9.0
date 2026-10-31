# Password Validation — res.users Override

## Context
The problem statement requires: password must be 8+ characters, with uppercase, lowercase, and a special character. Each email can belong to only one account.

## Prompt for Antigravity

```
In the Odoo 18 module "subscription_management", create a file `models/res_users.py` that inherits res.users.

Override the `create()` and `write()` methods to validate passwords:
- Minimum 8 characters
- At least 1 uppercase letter (A-Z)
- At least 1 lowercase letter (a-z)
- At least 1 special character (!@#$%^&*()_+-=[]{}|;:,.<>?)

Use regex for validation. Raise ValidationError with a clear message listing all requirements if any fail.

Also add a constraint on login (email) field to ensure uniqueness:
_sql_constraints = [
    ('unique_login', 'UNIQUE(login)', 'This email is already registered!'),
]

Add a helper method `_validate_password(password)` that can be reused.

Import: from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

Class should be:
class ResUsers(models.Model):
    _inherit = 'res.users'

Update models/__init__.py to import res_users.
```

## Expected Output
- `models/res_users.py`

## Verification
- Try creating a user with password "abc" — should fail
- Try "Abcdefg1!" — should succeed
- Try duplicate email — should fail
