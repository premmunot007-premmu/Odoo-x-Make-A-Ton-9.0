# Mail Integration — Chatter & Activities

## Context
Subscription and Invoice models should have chatter (message log) for tracking changes, and activity scheduling for follow-ups.

## Prompt for Antigravity

```
In the Odoo 18 module "subscription_management", ensure mail.thread and mail.activity.mixin are properly integrated.

1. Verify these models inherit mail.thread and mail.activity.mixin:
   - subscription.product (mail.thread + mail.activity.mixin)
   - subscription.subscription (mail.thread + mail.activity.mixin + portal.mixin)
   - subscription.invoice (mail.thread + mail.activity.mixin + portal.mixin)
   - subscription.payment (mail.thread only)

2. Add tracked=True to important fields:
   - subscription: state, partner_id, plan_id, start_date, expiry_date
   - invoice: state, partner_id, amount_total
   - payment: amount

3. Add message posting in state change methods:
   In subscription.py action_confirm():
       self.message_post(body="Subscription confirmed.")
   In action_activate():
       self.message_post(body="Subscription activated.")
   In action_close():
       self.message_post(body="Subscription closed.")
   In action_pause():
       self.message_post(body="Subscription paused.")

   In invoice.py action_confirm():
       self.message_post(body="Invoice confirmed.")

4. Send email on subscription confirmation:
   In action_confirm(), after state change:
       template = self.env.ref('subscription_management.email_template_subscription_confirmed', raise_if_not_found=False)
       if template:
           template.send_mail(self.id, force_send=True)

5. Ensure form views have chatter section at bottom:
   <div class="oe_chatter">
       <field name="message_follower_ids"/>
       <field name="activity_ids"/>
       <field name="message_ids"/>
   </div>
```

## Expected Output
- Updated model files with mail integration
- Message posting in state change methods

## Verification
- Change subscription state, check chatter shows the change
