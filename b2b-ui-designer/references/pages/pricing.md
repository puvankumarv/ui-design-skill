# Pricing page

**Master decision:** the plan structure — tiers, a billing toggle, a usage selector, or contact-only.

Evidence: 4 archive pricing pages (Netlify, Amie, Anytype, Beehiiv), 10 archive pricing components, Linear's live pricing page, and NN/g B2B research on pricing transparency.

## Section order

| # | Section | Default |
|---|---|---|
| 1 | `hero` | Headline + one line on what the price depends on ("Per user, billed monthly or annually") |
| 2 | `plan-controls` | Monthly/annual toggle with a savings badge, **or** a usage selector (seats, volume, subscribers) |
| 3 | `plans` | 3–4 plan cards |
| 4 | `logos` or a short quote | Proof close to the decision |
| 5 | `compare` | Full comparison table |
| 6 | `faq` | Billing, seats, trials, cancellation, security, invoices |
| 7 | `cta-band` | Primary CTA + "Talk to sales" |

## Choosing the structure

| Business | Structure | Inspo archetype |
|---|---|---|
| 3 tiers (most common) | Three cards, the recommended one raised | `pricing/three-card` |
| Two plans, cadence matters | Toggle + two cards | `pricing/toggle` |
| Usage-based (API calls, GB, messages) | Line items or a calculator | `pricing/per-use` |
| One offering | Single plan card | `pricing/single-plan` |
| Enterprise-only, custom contracts | What's covered + contact form, no prices | `pricing/enterprise` |
| Any of the above | Comparison table **below** the cards | `pricing/table` |

## Plan card rules

- Plan name, one-line "who it's for", price with an **explicit unit** ("$20 per user / month", "billed annually"). `[4/4 archive]`
- The recommended plan is raised by one thing only: a coloured top border, a filled CTA, or a "Most popular" label. Not all three.
- Higher tiers list "Everything in Basic, plus:" and then only the additions (5–8 items). `[Netlify, Amie]`
- Enterprise: "Custom" or "Contact sales"; list what's included (SSO, SLA, audit logs, dedicated support, invoicing).
- A CTA in every card. Labels match the motion: "Start free", "Start trial", "Contact sales".
- Annual savings shown as a number ("Save 20%"), never only as a strikethrough.

## Comparison table rules

- Sticky header row with plan names and CTAs. `[CARBON]`
- Rows grouped by category (Core, Collaboration, Security, Support) with group headings.
- ✓ / – / specific limits ("10 projects"). Use text alternatives for icons (`aria-label="Included"`).
- Feature names link to or explain the feature in a tooltip.
- On mobile: one plan column at a time with a plan switcher, not a horizontally scrolling 5-column table.

## Transparency

Buyers look for pricing early, and hiding it entirely frustrates them. `[NNG]` Sales-led companies should still show at least one of: a starting price, what the price depends on, or example packages.

## Checker hooks

Set `data-page="pricing"` on `<body>`. The checker then warns when no price unit ("per user", "/month", "billed") appears, or when there is no enterprise / contact path.
