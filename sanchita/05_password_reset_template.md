# Password Reset Email Template

## Context

We are building a **Subscription Management System** as an Odoo 18 custom module (`subscription_management`). This file creates the email template that is sent when a user requests a password reset.

The email must:
- Look professional with "Brightloop Software" branding
- Contain a clickable reset link with the token
- Show expiry notice (24 hours)
- Be HTML formatted with inline styles (for email client compatibility)
- Use Odoo's email template system (`mail.template`)

### Related files:
- `controllers/auth.py` — Sends this template via `send_mail()`
- `models/res_users.py` — Generates the token passed via context

---

## Prompt for Antigravity

```
Create the file `data/email_templates.xml` for an Odoo 18 custom module named `subscription_management`.

This file defines the email template for password reset emails.

### Requirements:

1. **File location:** `data/email_templates.xml`

2. **XML structure:**
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <odoo>
       <data noupdate="1">
           <!-- Email template record here -->
       </data>
   </odoo>
   ```

3. **Template record:**
   ```xml
   <record id="email_template_password_reset" model="mail.template">
       <field name="name">Subscription Management: Password Reset</field>
       <field name="model_id" ref="base.model_res_users"/>
       <field name="subject">Reset Your Password - Brightloop Software</field>
       <field name="email_from">{{ (object.company_id.email or 'noreply@brightloop.com') }}</field>
       <field name="email_to">{{ object.email }}</field>
       <field name="auto_delete" eval="True"/>
       <field name="body_html" type="html">
           <!-- HTML email body here -->
       </field>
   </record>
   ```

4. **Email HTML body design:**
   
   Create a professional, responsive HTML email with inline styles. The email should include:

   a. **Header section:**
      - Background color: #875A7B (Odoo purple) or #2c3e50 (dark blue)
      - "Brightloop Software" logo text in white
      - Full width, padded

   b. **Body section:**
      - White background
      - Greeting: "Hello {{ object.name }},"
      - Explanation text: "We received a request to reset the password for your account associated with {{ object.email }}."
      - Security notice: "If you did not make this request, you can safely ignore this email."

   c. **Reset button:**
      - Large, centered CTA button
      - Background color: #00A09D (teal/Odoo primary) or #3498db (blue)
      - White text: "Reset My Password"
      - Link URL: `{{ (object.company_id.website or 'http://localhost:8069') }}/subscription/reset-password/confirm?token={{ ctx.get('reset_token', '') }}&amp;login={{ object.login }}`
      - Rounded corners, padding

   d. **Fallback link:**
      - "If the button doesn't work, copy and paste this link into your browser:"
      - Plain text URL (same as button link)

   e. **Expiry notice:**
      - "This link will expire in 24 hours."
      - Styled in lighter/italic text

   f. **Footer section:**
      - "© 2024 Brightloop Software. All rights reserved."
      - Company address (if available): `{{ object.company_id.street or '' }}`
      - "This is an automated message. Please do not reply to this email."
      - Lighter text color, smaller font

5. **Email CSS (all inline styles):**
   - Email clients don't support `<style>` blocks reliably
   - Use inline `style=""` on every element
   - Max width 600px, centered
   - Font family: Arial, Helvetica, sans-serif
   - Table-based layout for email client compatibility

6. **QWeb expressions to use:**
   - `{{ object.name }}` — User's name
   - `{{ object.email }}` — User's email
   - `{{ object.login }}` — User's login (same as email usually)
   - `{{ object.company_id.name }}` — Company name
   - `{{ object.company_id.website }}` — Company website URL
   - `{{ ctx.get('reset_token', '') }}` — The reset token passed via context

7. **Important notes:**
   - Use `&amp;` for `&` in URLs within XML
   - Wrap Jinja expressions carefully within XML CDATA or escape properly
   - The `noupdate="1"` ensures the template isn't overwritten on module upgrade
   - Use `auto_delete=True` to clean up sent emails

Generate the complete XML file with a professional HTML email template.
```

---

## Expected Output

A single file `data/email_templates.xml` containing:
- One `mail.template` record with ID `email_template_password_reset`
- Professional HTML email with Brightloop branding
- Reset button linking to `/subscription/reset-password/confirm?token=...&login=...`
- Expiry notice
- Footer with company info

---

## Verification

1. **XML validity** — Parse the file with an XML validator; ensure no unclosed tags
2. **Template ID** — Must match `subscription_management.email_template_password_reset` (referenced in controller)
3. **Model reference** — `model_id` must reference `base.model_res_users`
4. **Email recipient** — Uses `object.email` (the user's email)
5. **Reset URL** — Contains both `token` and `login` parameters
6. **Context variable** — Uses `ctx.get('reset_token', '')` for the token
7. **HTML rendering** — All inline styles, table-based layout, max-width 600px
8. **Escaping** — `&amp;` used for `&` in URLs within XML attributes
9. **noupdate** — Set to `1` so template survives module upgrades
10. **Visual check** — Install module, trigger a password reset, check the email in Odoo's mail system
