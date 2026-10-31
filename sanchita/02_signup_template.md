# Signup Template

## Context

We are building a **Subscription Management System** as an Odoo 18 custom module (`subscription_management`). This file creates the QWeb signup page template that is rendered by the GET `/subscription/signup` route defined in `controllers/auth.py`.

The signup page must:
- Have a clean, professional form with fields for name, email, password, confirm password, and company name
- Include client-side password strength indicator
- Display error and success messages
- Submit via AJAX (JSON POST)
- Link to the login page
- Be branded for "Brightloop Software"

### Related files:
- `controllers/auth.py` — The controller that renders this template and handles POST
- `static/src/css/auth.css` — Styling (can be included inline or as separate file)

---

## Prompt for Antigravity

```
Create the file `views/auth_templates.xml` for an Odoo 18 custom module named `subscription_management`.

This file contains the QWeb template for the customer signup page of a Subscription Management System for "Brightloop Software".

### Requirements:

1. **File location:** `views/auth_templates.xml`

2. **Template ID:** `subscription_management.signup_page`

3. **Structure:** Use `<odoo>` root tag, then `<template>` tag. The template should extend `web.login_layout` OR be a standalone page inheriting from `website.layout` if website module is available. For maximum compatibility, create a standalone HTML page.

4. **Use this structure:**
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <odoo>
       <template id="signup_page" name="Subscription Signup">
           <t t-call="web.login_layout">
               <!-- Content here -->
           </t>
       </template>
   </odoo>
   ```

5. **Form fields (inside a card/container):**
   - **Full Name** — `<input type="text" name="name" required="required" class="form-control" placeholder="Enter your full name"/>`
   - **Email Address** — `<input type="email" name="email" required="required" class="form-control" placeholder="Enter your email"/>`
   - **Company Name** — `<input type="text" name="company_name" class="form-control" placeholder="Company name (optional)"/>`
   - **Password** — `<input type="password" name="password" required="required" class="form-control" placeholder="Create a password" id="signup_password"/>`
   - **Confirm Password** — `<input type="password" name="confirm_password" required="required" class="form-control" placeholder="Confirm your password"/>`

6. **Password Strength Indicator:**
   - Below the password field, add a `<div id="password-strength">` container
   - It should have a progress bar that changes color:
     - Red (weak): less than 8 chars
     - Orange (fair): 8+ chars but missing some criteria
     - Yellow (good): meets 3 of 4 criteria
     - Green (strong): meets all 4 criteria (8+ chars, uppercase, lowercase, special char)
   - Show text indicators: "Weak", "Fair", "Good", "Strong"
   - Add checklist below:
     - ✓/✗ At least 8 characters
     - ✓/✗ Contains uppercase letter
     - ✓/✗ Contains lowercase letter
     - ✓/✗ Contains special character

7. **Password strength JavaScript (inline `<script>` at bottom):**
   ```javascript
   document.getElementById('signup_password').addEventListener('input', function() {
       var password = this.value;
       var strength = 0;
       var checks = {
           length: password.length >= 8,
           uppercase: /[A-Z]/.test(password),
           lowercase: /[a-z]/.test(password),
           special: /[!@#$%^&*()_+\-=\[\]{}|;':",.<>?\/]/.test(password)
       };
       // Update individual check indicators
       // Update progress bar width and color
       // Update strength text
   });
   ```

8. **Error/Success message display:**
   - `<div id="signup-message" class="alert" style="display:none;"></div>` at top of form
   - Use `t-if="error"` to show server-side errors: `<div class="alert alert-danger"><t t-esc="error"/></div>`

9. **Form submission via JavaScript (AJAX):**
   ```javascript
   document.getElementById('signup-form').addEventListener('submit', function(e) {
       e.preventDefault();
       // Collect form data
       // POST to /subscription/signup as JSON using fetch()
       // On success: show success message, redirect after 2 seconds
       // On error: show error message
   });
   ```
   
   The fetch call should use:
   ```javascript
   fetch('/subscription/signup', {
       method: 'POST',
       headers: {
           'Content-Type': 'application/json',
       },
       body: JSON.stringify({
           jsonrpc: '2.0',
           method: 'call',
           params: {
               name: formData.name,
               email: formData.email,
               password: formData.password,
               confirm_password: formData.confirm_password,
               company_name: formData.company_name,
           }
       })
   });
   ```

10. **Footer links:**
    - "Already have an account? <a href='/subscription/login'>Log in</a>"

11. **Styling:**
    - Use Bootstrap 5 classes (Odoo 18 includes Bootstrap 5)
    - Center the form on page with max-width 480px
    - Card with shadow, rounded corners
    - "Brightloop Software" heading at top of card
    - "Create Your Account" subheading
    - Primary color buttons matching Odoo's theme

12. **Accessibility:**
    - All inputs have `<label>` tags with `for` attribute
    - Form has `aria-label`
    - Error messages have `role="alert"`

Generate the complete XML file with all templates, inline CSS, and inline JavaScript.
```

---

## Expected Output

A single file `views/auth_templates.xml` containing:
- QWeb template `signup_page` with a professional signup form
- Inline JavaScript for password strength checking
- Inline JavaScript for AJAX form submission
- Bootstrap 5 styled layout
- Password requirements checklist

---

## Verification

1. **Check XML validity** — Ensure proper `<?xml?>` declaration, `<odoo>` root, `<template>` structure
2. **Check template ID** — Must be `subscription_management.signup_page` (matches controller)
3. **Check all form fields** — name, email, company_name, password, confirm_password
4. **Check password strength JS** — All 4 criteria checked (length, upper, lower, special)
5. **Check AJAX submission** — Uses JSON-RPC format with `jsonrpc: '2.0'`
6. **Check error display** — Both client-side and server-side error handling
7. **Check login link** — Points to `/subscription/login`
8. **Visual test** — Install module, navigate to `/subscription/signup`, verify form renders
