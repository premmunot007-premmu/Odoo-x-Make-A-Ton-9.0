# Invoice Lines — Tax Auto-Calculation

## Context
This file was merged into 06_invoice_model.md. Invoice lines are already defined there with tax computation. This file adds the auto-generation method that creates invoice lines FROM subscription lines.

## Prompt for Claude Code

```
In the Odoo 18 module "subscription_management", add a method to the Subscription model (models/subscription.py) that generates an invoice from the subscription.

Add this method to class Subscription:

    def action_create_invoice(self):
        """Create an invoice from this subscription's lines"""
        self.ensure_one()
        if self.state != 'active':
            raise UserError("Can only invoice active subscriptions.")

        # Check for duplicate billing - prevent invoicing if already invoiced this period
        last_invoice = self.env['subscription.invoice'].search([
            ('subscription_id', '=', self.id),
            ('state', '!=', 'cancelled'),
        ], order='invoice_date desc', limit=1)

        if last_invoice:
            from dateutil.relativedelta import relativedelta
            freq_map = {'daily': relativedelta(days=1), 'weekly': relativedelta(weeks=1), 'monthly': relativedelta(months=1), 'yearly': relativedelta(years=1)}
            next_allowed = last_invoice.invoice_date + freq_map.get(self.plan_id.billing_frequency, relativedelta(months=1))
            if fields.Date.today() < next_allowed:
                raise UserError(f"Already invoiced for this period. Next invoice allowed after {next_allowed}")

        # Calculate due date based on payment terms
        term_days = {'immediate': 0, '15_days': 15, '30_days': 30, '60_days': 60}
        due_date = fields.Date.today() + relativedelta(days=term_days.get(self.payment_term, 30))

        # Create invoice
        invoice_lines = []
        for line in self.subscription_line_ids:
            # Check for applicable discounts
            discount_amount = self._get_discount_amount(line)
            invoice_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'description': line.product_id.name,
                'quantity': line.quantity,
                'unit_price': line.unit_price + (line.variant_id.price_extra if line.variant_id else 0),
                'tax_ids': [(6, 0, line.tax_ids.ids)],
                'discount_amount': discount_amount,
            }))

        invoice = self.env['subscription.invoice'].create({
            'subscription_id': self.id,
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.today(),
            'due_date': due_date,
            'invoice_line_ids': invoice_lines,
        })

        # Update next billing date
        from dateutil.relativedelta import relativedelta
        freq_map = {'daily': relativedelta(days=1), 'weekly': relativedelta(weeks=1), 'monthly': relativedelta(months=1), 'yearly': relativedelta(years=1)}
        self.write({'next_billing_date': fields.Date.today() + freq_map.get(self.plan_id.billing_frequency, relativedelta(months=1))})

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'subscription.invoice',
            'res_id': invoice.id,
            'view_mode': 'form',
        }

    def _get_discount_amount(self, line):
        """Find and apply applicable discount rules"""
        today = fields.Date.today()
        discounts = self.env['subscription.discount.rule'].search([
            ('is_active', '=', True),
            '|', ('date_start', '=', False), ('date_start', '<=', today),
            '|', ('date_end', '=', False), ('date_end', '>=', today),
            '|',
                '&', ('apply_on', '=', 'product'), ('product_ids', 'in', [line.product_id.id]),
                ('apply_on', '=', 'subscription'),
        ])
        total_discount = 0.0
        base = line.quantity * line.unit_price
        for disc in discounts:
            if disc.max_usage > 0 and disc.current_usage >= disc.max_usage:
                continue
            if disc.min_quantity and line.quantity < disc.min_quantity:
                continue
            if disc.min_purchase and base < disc.min_purchase:
                continue
            if disc.discount_type == 'percentage':
                total_discount += base * (disc.amount / 100.0)
            else:
                total_discount += disc.amount
            disc.sudo().write({'current_usage': disc.current_usage + 1})
        return total_discount

This creates invoices from subscriptions with duplicate prevention and discount auto-application.
```

## Expected Output
- Updated `models/subscription.py` with `action_create_invoice()` and `_get_discount_amount()`

## Verification
- Create an active subscription with lines, call action_create_invoice, verify invoice is created with correct amounts
