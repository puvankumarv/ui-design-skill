# DRAFT — Page blueprints and placement rules

Status: draft for review. Built from `site_survey.md` (29 archive homepages), `live_site_notes.md` (8 live sites) and `design_system_rules.md`. The evidence column shows how many sampled sites support each choice.

## Step 0: classify the business (decides everything below)

| Sales motion | How you can tell | Primary CTA | Secondary CTA |
|---|---|---|---|
| **Sales-led** | Price depends on contract, buyers are enterprises | Get a demo / Contact sales | Watch demo / See how it works |
| **Self-serve** (product-led) | Card signup, public prices | Start for free / Get started | Book a demo (for larger teams) |
| **Hybrid** | Both | Get started | Get a demo (ghost button) |
| **Service / industrial** | Quotes, logistics, manufacturing, agencies | Request a quote / Talk to an expert | Download catalogue / Explore services |

## Blueprint A: B2B homepage

| # | Section | Required? | Default component | Evidence |
|---|---|---|---|---|
| 0 | Announcement bar or pill | Optional | Pill above headline ("New: …") | 13/29 archive |
| 1 | Sticky nav | Required | Inline nav; **mega menu** if 3+ products or segments | Most sites; mega on HubSpot, Salesforce, Flexport |
| 2 | Hero | Required | See hero decision table | 29/29 |
| 3 | Logo strip | Required if you have logos | Static strip; marquee if > 8 logos | ~20/29 archive, 4/8 live |
| 4 | Problem or positioning statement | Recommended | One large sentence, centred | Linear, Ramp, HubSpot, Salesforce |
| 5 | Product suite **or** feature deep-dives | Required | Suite grid if multiple products; alternating rows or workflow narrative if one product | 6/8 live |
| 6 | How it works | Optional | Numbered 3-step | Self-serve and service businesses |
| 7 | Proof | Required | Case-study cards with a metric headline; or stat row; or testimonial | 8/8 live have some proof |
| 8 | Integrations | Recommended for software | Logo grid + count ("2,000+") | HubSpot, Stripe, Ramp |
| 9 | Security / trust | Required for enterprise and fintech | Badge row (SOC 2, ISO 27001, GDPR) + link to trust page | Fintech and enterprise sites |
| 10 | Analyst / review badges | Optional | G2 / Gartner / Forrester row | HubSpot, Salesforce, Datadog |
| 11 | FAQ | Recommended | Accordion, 5–8 questions | Ramp, Salesforce |
| 12 | Final CTA band | Required | Repeat hero promise + primary CTA | 5/8 live |
| 13 | Footer | Required | Sitemap footer (4–6 columns) for multi-product; compact otherwise | 4/8 live mega footers |

### Hero decision table

| Situation | Hero layout | Visual |
|---|---|---|
| Software with a strong UI | Centred stack, product UI below, bleeding off the bottom edge | Real product screenshot (59% of the sample) |
| Fintech, compliance, or text-heavy value prop | Split: text left 40–45%, visual right 55–60% | Dashboard UI, card or live widget |
| Interactive calculator possible (pricing, ROI, conversion) | Split with a **working widget** as the visual | Wise converter pattern |
| Strong brand, abstract product (infrastructure, AI) | Centred, type only, or with an abstract graphic | Type carries it; logos directly below |
| Service / industrial | Split with real photography of operations, plus a proof stat | Photo + floating stat card |

**Hero rules:**
- Headline, subhead, CTA and the top of the visual all fit inside 1280×800.
- Headline 2–3 lines, sentence case, display-to-body size ratio about 3:1.
- At most 2 buttons. A third path becomes a text link.
- A single accent colour, used on the primary CTA and at most one highlighted headline phrase.

## Blueprint B: Pricing page

1. Headline + one line on what the price depends on
2. Billing toggle (monthly / annual, savings badge) **or** usage selector (seats, volume)
3. 3–4 plan cards; the recommended plan is visually raised; Enterprise = "Contact sales"
4. Per-plan "Everything in X, plus:" lists, 5–8 items
5. Full comparison table (sticky plan header, grouped rows, ✓ / – / limits)
6. Logos or a short quote near the plans
7. Pricing FAQ (billing, seats, cancellation, security)
8. Final CTA

## Blueprint C: Product / feature page

Hero (feature promise + UI) → problem → 3–4 capability blocks (alternating rows) → workflow or demo video → proof specific to the feature → related integrations → CTA.

## Blueprint D: Solution page (by industry or role)

Hero naming the audience ("for finance teams") → their pains (3) → how the product solves each → case study from that industry → relevant features grid → compliance for that industry → CTA.

## Blueprint E: Security / trust page

Headline → certification badges → sections: data protection, infrastructure, access control, compliance, privacy → downloadable documents (SOC 2 report on request) → contact security team.

## Blueprint F: Demo request page

Split layout: left = what you'll get on the call (3 bullets), logos, one quote; right = short form (4–5 fields). Success state: confirmation and calendar booking inline.

## Blueprint G: App screens (from design systems)

| Screen | Order |
|---|---|
| Dashboard | Page title + date range / filters (top-right) → 3–5 KPI cards → main chart (full width) → supporting charts (2 columns) → detail table |
| List / table | Title + primary action → search + filters → active filter chips → table with bulk actions → pagination |
| Detail | Breadcrumb → title + status + actions → tabs → content in cards → activity sidebar |
| Settings | Left nav of sections → one section per page → grouped form cards → save bar (sticky when dirty) |
| Onboarding | Progress (steps) → one task per screen → skip option → finish on the first useful screen, never an empty dashboard |

## Placement rules (checker candidates)

1. Primary CTA appears in the hero and again at least every 2–3 sections on long pages; it is the same label every time.
2. Proof (logos, metrics) appears before the first request for commitment below the hero.
3. No more than one full-bleed accent band on a page.
4. Text column ≤ 75 characters.
5. Section padding 80–160px on desktop; consistent within a page.
6. Cookie banner placed bottom-left or bottom bar, never covering the hero CTA.
7. Every metric shown names its source or is clearly the company's own.
