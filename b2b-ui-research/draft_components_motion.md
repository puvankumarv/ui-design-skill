# DRAFT — Component menus, card specs, style directions and motion

Status: draft for review. Component archetype names follow the Inspo reference index (68 archetypes with React + Tailwind source, fetched with `get_reference_jsx`), so the skill can pull starter code for any choice below.

## 1. Section → component menus

### Features
| Situation | Component | Inspo archetype |
|---|---|---|
| 4–6 features, each with a visual | Bento grid; the biggest tile is the lead feature | `features/bento` |
| 2–4 deep features | Alternating image/text rows | `features/alternating` |
| A workflow in steps | Numbered triplet or workflow narrative (Linear) | `features/numbered-triplet` |
| A feature best shown live | Copy left, working demo right | `features/workbench` |
| Different features per role | Tabs, one per role | — |
| Many small capabilities | 3-column icon grid | `features/icon-trio` |
| Replacing an old way of working | Before / with comparison (no competitor names) | `features/compare` |

### Proof
| Situation | Component | Inspo archetype |
|---|---|---|
| Many customer logos | Strip (≤ 8) or marquee (> 8) | `logo-cloud/strip`, `logo-cloud/marquee` |
| Large partner roster | 4×3 logo grid | `logo-cloud/grid` |
| Measurable outcomes | Case-study cards with metric headline | — (Salesforce, Stripe pattern) |
| Company-scale numbers | Stat row, 3–4 figures, tabular numbers | `stat/row` |
| One strong customer voice | Pull quote with name, role, company, photo | `testimonial/pull-quote` |
| Many reviews | Mosaic of quotes or star-review row | `testimonial/mosaic`, `testimonial/reviews-row` |

**Rule:** never invent logos, quotes or numbers. Use labelled placeholders until the client supplies real ones.

### Pricing
| Situation | Inspo archetype |
|---|---|
| 3 tiers (default) | `pricing/three-card` |
| Monthly / annual choice | `pricing/toggle` |
| Usage-based (API, volume) | `pricing/per-use` |
| One offering | `pricing/single-plan` |
| Enterprise only | `pricing/enterprise` |
| Full detail | `pricing/table` (always below the cards) |

### CTA
| Situation | Inspo archetype |
|---|---|
| Default end of page | `cta/two-button` (primary + ghost) |
| One loud ask per page | `cta/banded` (max one per page) |
| Newsletter / waitlist | `cta/form-led` |
| Calm enterprise brand | `cta/inverted` |

### Navigation
| Situation | Inspo archetype |
|---|---|
| 1 product, ≤ 6 links | `nav/inline` |
| 3+ products, segments or resources | `nav/mega` |
| Docs, deep hierarchy | `nav/breadcrumb` |
| ⌘K-driven product | `nav/search-first` |

### FAQ
`faq/accordion` by default (native `<details>`); `faq/category-tabs` when questions split by audience; `faq/search-led` when there are more than 12.

## 2. Card anatomy (one spec, three looks)

**Content order:** icon or media → eyebrow (optional) → title (1 line, max 2) → body (2–3 lines) → link or action. The whole card is clickable when it has a single destination.

| Property | Enterprise (calm) | Modern SaaS | Developer tool (dark) |
|---|---|---|---|
| Surface | White on light grey section | White on white | #0f0f12 on #0a0a0b |
| Edge | 1px border, neutral 200 | Soft shadow `0 1px 2px` + `0 8px 24px` at low opacity | 1px border at 8% white; inner top highlight |
| Radius | 4–8px | 12–16px | 8–12px |
| Padding | 24px | 24–32px | 24px |
| Hover | Border darkens; no movement | Lift 2–4px + shadow grows, 200ms | Border brightens / soft glow, 150ms |
| Icon | Line icon in a 40px tinted square | Duotone or illustrated | Mono glyph or code snippet |
| Title type | 18px semibold | 20px semibold | 18px medium, sometimes mono |

States every card needs: default, hover, focus-visible (2px ring at ≥ 3:1), pressed, disabled (if interactive), loading skeleton (in app UI).

## 3. Style directions (from the survey)

| Direction | Seen on | Tokens in short |
|---|---|---|
| **Enterprise** | Salesforce, Datadog, Flexport | Light, blue or navy accent, grotesk, 4–8px radius, borders over shadows, photography of real people and operations |
| **Modern SaaS** | Arrows, Ramp, Brevo, Campaign Monitor | Light, one saturated accent, Inter/Geist, 12–16px radius, product UI everywhere, soft shadows |
| **Fintech trust** | Brex, Sardine, Public, Wise | Light warm off-white, serif or heavy-sans headline, single strong accent (orange, lime, blue), real numbers up front |
| **Developer tool** | Unkey, Novu, Linear, Vercel | Dark, mono accents, code in the hero or features, thin borders, glow effects, GitHub / docs CTA |
| **Editorial / consulting** | Hex, Forest Admin, Mailchimp | Serif display, generous whitespace, case-study-led, restrained colour |

## 4. Motion spec (measured + design systems)

| Interaction | Duration | Easing | Evidence |
|---|---|---|---|
| Button / link hover, press | 100–150ms | ease-out | Linear 0.1s, Flexport 0.15s, Carbon fast-02 110ms |
| Card hover lift, tab switch, accordion | 200–250ms | `cubic-bezier(0.2, 0, 0.38, 0.9)` | Ramp 0.2s, Stripe 0.25s, Carbon moderate-02 240ms |
| Dropdown / mega menu open | 150–250ms | ease-out; close faster than open | Live sites 0.15–0.3s |
| Scroll reveal (fade + 8–16px rise) | 400–600ms, stagger 60–80ms | `cubic-bezier(0.16, 1, 0.3, 1)` | Stripe 0.6–1s; Linear 0.4–0.7s |
| Hero entrance | 600–800ms, once | same strong ease-out | Stripe |
| Number counter (stats) | 800–1200ms, once when in view | ease-out | Common; optional |
| Logo marquee | 30–90s per loop, pause on hover | linear | Linear 30s, Salesforce 85s, Ramp 180s |
| Product demo | Muted looping video ≤ 15s, or step-through screenshots | — | HubSpot, Datadog, Ramp |

**Always:**
- Respect `prefers-reduced-motion`: replace movement with instant or opacity-only changes.
- Anything that moves on its own for more than 5s gets a pause control (WCAG 2.2.2).
- Animate only `transform` and `opacity`.
- Motion explains something (state change, where content came from). No decorative parallax on text, no auto-playing carousels for key content, no long intro animations.
- App UI uses the fast end of every range ("productive"); marketing pages may use the slower end ("expressive").

## 5. Open questions for review

1. Should traditional industrial / B2B ecommerce (catalogues, quote requests, distributor portals) be a first-class module? It needs a second research pass; the archive barely covers it.
2. Output stack: plain HTML/CSS, React + Tailwind, or both? Inspo's reference code is React + Tailwind.
3. Should the skill include a regional layer like the interior skill (e.g. India-specific B2B patterns: GST invoicing, UPI, WhatsApp contact; seen on Razorpay)?
