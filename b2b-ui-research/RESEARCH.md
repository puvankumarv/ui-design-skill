# B2B UI Designer — research

Research for a Claude skill + MCP server that designs B2B websites and product UI. Started 2026-11-22. Nothing here is final; the drafts need review before the skill is built on them.

## Method

1. **Reference archive (Inspo MCP):** 29 B2B homepages (SaaS, fintech, developer tools), 4 pricing pages and 10 pricing components. Each comes with a breakdown of its first screen: layout, type, colour and signature detail. Also indexed 68 reference component archetypes that have React + Tailwind source.
2. **Live sites (built-in browser):** 8 B2B homepages (Stripe, Linear, Ramp, HubSpot, Datadog, Salesforce, Rippling, Flexport) and Linear's pricing page. A script recorded the full section order, CTA labels, transition durations and animations.
3. **Design systems and research:** WCAG 2.2, IBM Carbon, Shopify Polaris, Atlassian, Salesforce Lightning, Material 3, NN/g, Baymard, GOV.UK. Some numbers are marked [verify] to check against the live docs.

## Files

| File | What it holds |
|---|---|
| `site_survey.md` | Per-site table of archive homepages + pattern counts |
| `live_site_notes.md` | Full section order, CTA frequency and motion timings from live sites |
| `design_system_rules.md` | Accessibility thresholds, spacing, type, tables, forms, dashboards, motion values, buying behaviour |
| `draft_blueprints.md` | **Draft** page blueprints, hero decision table, placement rules |
| `draft_components_motion.md` | **Draft** component menus, card anatomy, style directions, motion spec, open questions |

## Main findings

1. **Real product UI is the hero visual on 59% of B2B homepages.** Illustrations and stock photos are rare.
2. **Hero layout follows the segment:** fintech uses a split layout (text left, visual right); SaaS and dev tools use a centred stack with the UI below.
3. **A logo strip right after the hero is close to universal** (~70% of the archive).
4. **One primary CTA, repeated.** Rippling repeats "Get a demo" 6 times; Stripe repeats "Contact sales" 3 times. The label depends on the sales motion.
5. **Proof is specific:** case-study headlines lead with a metric, plus analyst/G2 badges and integration counts.
6. **Pages end the same way:** FAQ → final CTA band (often repeating the hero headline) → large footer.
7. **Motion is fast and restrained:** hover 100–200ms, panels 200–300ms, scroll reveals 400–800ms with a strong ease-out. Logo marquees are the most common ambient animation.
8. **Dark mode is a dev-tool and AI signal** (8 of 11 dark sites); fintech and enterprise stay light.
9. **Gaps:** traditional industrial / B2B ecommerce and app UI are thin in the archive. App UI rules come from design systems; industrial needs another pass.
