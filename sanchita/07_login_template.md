# Login Template

## Context

We are building a **Subscription Management System** as an Odoo 18 custom module (`subscription_management`). This file creates the QWeb login page template rendered at `/subscription/login`.

The login page must:
- Have a clean, professional design matching the signup page
- Display email and password fields
- Show error messages from failed login attempts
- Link to "Forgot password?" and "Sign up" pages
- Submit as a standard HTML form POST (not AJAX)
- Be branded for "Brightloop Software"

### Related files:
- `controllers/auth.py` — Renders this template and handles POST
- `views/auth_templates.xml` — Add this template alongside signup template

---

## Prompt for Antigravity

```
Add a login page template to `views/auth_templates.xml` in the Odoo 18 custom module `subscription_management`.

This template should be added AFTER the existing signup template in the same file.

### Requirements:

1. **Template ID:** `subscription_management.login_page`

2. **Structure:**
   ```xml
   <template id="login_page" name="Subscription Login">
       <t t-call="web.login_layout">
           <!-- Login form content -->
       </t>
   </template>
   ```

3. **Page layout:**
   - Centered card (max-width 420px) with shadow
   - "Brightloop Software" branding/logo at top
   - "Welcome Back" heading
   - "Sign in to your account" subheading

4. **Error message display:**
   ```xml
   <t t-if="error">
       <div class="alert alert-danger alert-dismissible fade show" role="alert">
           <t t-esc="error"/>
           <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"/>
       </div>
   </t>
   ```

5. **Login form:**
   ```xml
   <form action="/subscription/login" method="POST" id="login-form">
       <input type="hidden" name="csrf_token" t-att-value="request.csrf_token()"/>
       <input type="hidden" name="redirect" t-att-value="redirect"/>
       
       <div class="mb-3">
           <label for="login" class="form-label">Email Address</label>
           <input type="email" name="login" id="login" 
                  class="form-control form-control-lg" 
                  placeholder="Enter your email" 
                  t-att-value="login or ''"
                  required="required" autofocus="autofocus"/>
       </div>
       
       <div class="mb-3">
           <label for="password" class="form-label">Password</label>
           <input type="password" name="password" id="password" 
                  class="form-control form-control-lg" 
                  placeholder="Enter your password" 
                  required="required"/>
       </div>
       
       <div class="d-flex justify-content-between align-items-center mb-3">
           <div class="form-check">
               <input class="form-check-input" type="checkbox" id="remember_me"/>
               <label class="form-check-label" for="remember_me">Remember me</label>
           </div>
           <a href="/subscription/reset-password" class="text-decoration-none">Forgot password?</a>
       </div>
       
       <button type="submit" class="btn btn-primary btn-lg w-100">Sign In</button>
   </form>
   ```

6. **Footer links:**
   ```xml
   <div class="text-center mt-4">
       <span class="text-muted">Don't have an account? </span>
       <a href="/subscription/signup" class="text-decoration-none fw-bold">Sign up</a>
   </div>
   ```

7. **Styling (inline or within template):**
   - Same visual style as the signup page (consistency)
   - Bootstrap 5 classes
   - Card with border-radius, shadow
   - Primary button in teal/blue color
   - Responsive design
   - Background: light gray (#f8f9fa) or subtle gradient

8. **Password visibility toggle (optional enhancement):**
   - Small eye icon button inside the password field
   - Toggles between `type="password"` and `type="text"`
   - JavaScript:
     ```javascript
     document.getElementById('toggle-password').addEventListener('click', function() {
         var pwd = document.getElementById('password');
         pwd.type = pwd.type === 'password' ? 'text' : 'password';
         this.classList.toggle('fa-eye');
         this.classList.toggle('fa-eye-slash');
     });
     ```

9. **CSRF token** — Must include hidden input with CSRF token for form security

10. **Pre-fill email** — If `login` value is passed from controller (after failed attempt), pre-fill the email field

Generate the complete template XML to be added to the existing `auth_templates.xml` file.
```

---

## Expected Output

A QWeb template block to add to `views/auth_templates.xml`:
- Template `login_page` with professional login form
- Error message display
- CSRF token inclusion
- Forgot password and signup links
- Optional password visibility toggle
- Consistent styling with signup page

---

## Verification

1. **Template ID** — Must be `subscription_management.login_page` (matches controller)
2. **Form action** — Points to `/subscription/login` with `method="POST"`
3. **CSRF token** — Hidden input with `t-att-value="request.csrf_token()"`
4. **Error display** — Uses `t-if="error"` conditional
5. **Email pre-fill** — Uses `t-att-value="login or ''"` on email input
6. **Forgot password link** — Points to `/subscription/reset-password`
7. **Signup link** — Points to `/subscription/signup`
8. **Visual consistency** — Same card style, colors, branding as signup page
9. **Navigate to `/subscription/login`** — Page should render without errors
