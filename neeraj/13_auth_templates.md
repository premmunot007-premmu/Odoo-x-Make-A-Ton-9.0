# Auth Page Templates — Signup, Login, Reset

## Context
QWeb templates for the custom auth pages: signup form, login form, password reset request, and reset confirmation.

## Prompt for Antigravity

```
In the Odoo 18 module "subscription_management", create `views/auth_templates.xml`.

Create QWeb templates:

1. template id="signup_page":
- Clean centered card layout (Bootstrap)
- Title: "Create Your Account"
- Form fields: Name, Email, Password (with strength indicator), Confirm Password
- Client-side validation hints:
  - "✓ 8+ characters" / "✗ 8+ characters" (toggle class based on length)
  - "✓ Uppercase letter" / "✗ Uppercase letter"
  - "✓ Lowercase letter" / "✗ Lowercase letter"
  - "✓ Special character" / "✗ Special character"
- Submit button "Create Account"
- Link: "Already have an account? Login"
- Error message display area (if error passed from controller)
- Use t-call="web.login_layout" or standalone layout

2. template id="login_page":
- Centered card, "Welcome Back" title
- Email and Password fields
- "Login" button
- Links: "Forgot Password?" and "Create Account"
- Error message display

3. template id="reset_password_page":
- "Reset Password" title
- Email field
- "Send Reset Link" button
- Success message area

4. template id="reset_password_confirm_page":
- "Set New Password" title
- New Password field (with strength indicator)
- Confirm Password field
- Hidden token field
- "Reset Password" button

All templates should:
- Use Bootstrap 5 classes
- Be mobile-responsive
- Have a clean, modern look
- Include CSRF token in forms: <input type="hidden" name="csrf_token" t-att-value="request.csrf_token()"/>

Update __manifest__.py to include 'views/auth_templates.xml'.
```

## Expected Output
- `views/auth_templates.xml`

## Verification
- Visit /subscription/signup, /subscription/login in browser
