# Component menus: which component, in which section, when

Archetype ids (`features/bento` etc.) match the Inspo reference index. When the Inspo MCP is connected, `get_reference_jsx(type, id)` returns React + Tailwind starter source for that archetype. Rewrite it with this skill's tokens; never ship it with its demo content.

## Hero
See the decision table in `pages/homepage.md`. Archetypes: `hero/split-screen`, `hero/stat-led` (only with a real number), `hero/marquee` (type-led), `hero/question`.

## Logos
| Situation | Component | Archetype |
|---|---|---|
| ≤ 8 logos | Static strip, logos muted to one tone | `logo-cloud/strip` |
| > 8 logos | Marquee, 30–90s loop, pause on hover/focus, static under reduced motion | `logo-cloud/marquee` |
| A large roster in the proof section | 4×3 grid | `logo-cloud/grid` |
| Different relationships (customers, partners, investors) | Grouped with honest labels | `logo-cloud/sectioned` |

## Features
| Situation | Component | Archetype |
|---|---|---|
| 4–6 features, each with a visual | Bento grid; the largest tile is the lead feature | `features/bento` |
| 2–4 deep features | Alternating image/text rows with real UI crops | `features/alternating` |
| A process | Numbered steps or a workflow narrative (Linear) | `features/numbered-triplet` |
| A feature best shown live | Copy left, working demo or code right | `features/workbench` |
| Different value per role | Tabs, one per role (roving `tabindex`, arrow keys) | — |
| Many small capabilities (secondary list) | Compact 3–4 column list with small icons | `features/icon-trio` |
| Replacing a manual way of working | Before / with (no competitor names) | `features/compare` |
| Several products | Product-suite grid: one card per product, linked | Stripe, Ramp, HubSpot |

Don't use a 3×2 grid of identical icon cards as the main feature section (`ai-slop.md`).

## Proof
| Client has | Component | Archetype |
|---|---|---|
| Measurable outcomes | Case-study cards, metric as headline, logo, link | — |
| Company-scale numbers | Stat row, 3–4 figures, tabular numbers, source line | `stat/row`, `stat/annotated` |
| One strong voice | Pull quote with photo, name, role, company | `testimonial/pull-quote` |
| Many short reviews | Mosaic or reviews row with the review-site name | `testimonial/mosaic`, `testimonial/reviews-row` |
| Analyst recognition | Badge row with report name and year | — |

## Pricing
See `pages/pricing.md`. Archetypes: `pricing/three-card`, `pricing/toggle`, `pricing/per-use`, `pricing/single-plan`, `pricing/enterprise`, `pricing/table`.

## FAQ
| Situation | Archetype |
|---|---|
| Default, 5–8 questions | `faq/accordion` (native `<details>`) |
| Questions split by audience | `faq/category-tabs` |
| More than 12 questions | `faq/search-led` |
| End of page, still unsure | `faq/with-cta` |

## CTA
| Situation | Archetype |
|---|---|
| Default end of page | `cta/two-button` (primary + ghost, never a third) |
| The single loud ask | `cta/banded` (max one per page) |
| Newsletter, waitlist | `cta/form-led` |
| Calm enterprise brand | `cta/inverted` |

## Navigation
| Situation | Archetype |
|---|---|
| One product, ≤ 6 links | `nav/inline` |
| 3+ products, segments, a resource library | `nav/mega` (opens on click and focus, closes on Esc, not hover-only) |
| Docs, deep hierarchies | `nav/breadcrumb` |
| ⌘K-led product | `nav/search-first` |

Nav CTA cluster: "Sign in" as a text link, then the primary CTA as a small button. Sales-led sites may add "Contact sales" as a text link.

## Footer
| Situation | Archetype |
|---|---|
| Multi-product company | `footer/sitemap` (4–6 columns, only real pages) |
| Single product | Compact footer: logo, 3–6 links, legal, status |
| Content-led | `footer/newsletter` |

Footer always includes: legal links, a security/trust link (enterprise), the status page (software), and contact.
