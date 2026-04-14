---
trigger: always_on
glob:
description:
---

# UX Rules

## Who is using this

The primary user is a 1–5 person Croatian SMB owner — a winemaker, a villa owner,
a rental operator. They manage the business from their phone. They are not technical.
They have no patience for software that requires configuration before it does anything
useful. They are already on Booking.com or Instagram; this product must feel simpler,
not more complex.

The end-user (widget customer) is a tourist or local buyer on the tenant's own website.
They may not speak Croatian.

## Admin dashboard UX rules

### Mobile-first
- Every layout must work on a 390px wide screen before it's designed for desktop.
- Touch targets are minimum 44×44px. No hover-only interactions.
- Sidebars collapse on mobile; use a bottom nav or hamburger pattern.

### Empty states are checklists, not blank screens
- When a tenant has no products, no resources, no loyalty program — show them
  exactly what to do next. One clear call to action. Never a blank white box.
- Example: "Nemate još nijedan proizvod. Dodajte prvi proizvod i počnite primati
  narudžbe." + a primary button.

### Every action is a guided wizard
- Multi-step forms are broken into one question per screen on mobile.
- Never show all fields at once for creation flows (new product, new resource,
  new reservation).
- Show progress (step 1 of 3) for flows with more than 2 steps.
- Sensible defaults everywhere. Tenant should be able to complete setup by only
  filling in the fields that are blank — not by choosing from options they don't
  understand.

### Defaults conform to Croatian standards
- VAT defaults to 25%. Never make the tenant choose.
- Currency defaults to EUR. Never show HRK, never show a currency picker.
- Date format: DD.MM.YYYY. Time: 24h. Locale: hr-HR.
- Language: Croatian throughout the admin UI. English is only for the widget
  when `data-locale="en"` is set by the tenant.

### Error messages are plain Croatian
- No technical language. No HTTP status codes visible to users.
- Not: "Error 422: Unprocessable Entity"
- Yes: "Unesite ispravnu e-mail adresu."
- Not: "Foreign key constraint failed"
- Yes: "Ovaj proizvod se ne može obrisati jer je dio narudžbe."
- Errors appear inline next to the field that caused them, not only in a toast.

### Confirmations for destructive actions only
- Don't ask "are you sure?" for reversible actions (edits, status changes).
- Do ask for hard deletes or cancellations that affect a customer
  (e.g. "Otkazati rezervaciju? Ova radnja se ne može poništiti.").

### Module gating is silent and informative
- If a module is not licensed, the nav item is visible but disabled, with a
  short explanation ("Webshop modul nije aktivan. Kontaktirajte podršku za
  aktivaciju.") — not a 403 page.
- Never show features the tenant hasn't licensed as broken — show them as
  locked with a clear upgrade path.

## Widget UX rules

### Zero friction for end-users
- The widget must be usable without an account.
- No redirect away from the tenant's domain. No full-page takeovers unless
  going to CorvusPay for payment (external, unavoidable).
- Inline loading states. If data takes >300ms, show a skeleton, not a spinner.

### Locale follows `data-locale`
- `hr` (default): all labels, buttons, placeholders in Croatian.
- `en`: all labels in English.
- Never mix languages within a single widget instance.

### Inline styles only
- The widget renders on arbitrary third-party pages. External CSS will break.
- All styling is inline. Font is inherited from the host page (`font-family: inherit`).
- Primary color is driven by the tenant's `widget_primary_color` setting — pass it
  as a CSS variable or inline style on the root element.

### Booking widget date picker
- Default check-in: tomorrow. Default check-out: the day after.
- Disable past dates. Disable dates that are already fully booked.
- Show price per night in the date picker tooltip.

### Loyalty widget
- Card lookup is by email only — no account required.
- Show stamp count visually (filled/empty circles up to `stamps_required`).
- If the card is full, show the reward and a "Redeem" button prominently.

## What the UI is not

- Not a website builder. Do not add page editors, themes, or layout options.
- Not a CRM. Customer contact data is captured at point of sale only.
- Not a reporting dashboard. Basic counts (orders today, reservations this week)
  are fine; charts, funnels, and cohort analysis are out of scope.
- Not a chat or support tool. No live chat, no ticketing.
