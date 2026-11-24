# Homepage

**Master decision:** the hero layout, and how the page proves its claims.

Evidence: 29 archive homepages (`site_survey.md`) and 8 live sites with full section order (`live_site_notes.md`). Counts in brackets are "sites showing this / sites sampled".

## Section order

| # | Section (`data-section`) | Required? | Default component | Evidence |
|---|---|---|---|---|
| 0 | `announcement` | Optional | Pill above the headline linking to the newest launch, report or event | [13/29] |
| 1 | `nav` | Required | Sticky inline nav, 56–72px tall. **Mega menu** if there are 3+ products, segments or a resource library | Mega on HubSpot, Salesforce, Flexport |
| 2 | `hero` | Required | See the hero decision table | [29/29] |
| 3 | `logos` | Required if logos exist | Static strip ≤ 8 logos, marquee above that | [~20/29] archive, [4/8] live |
| 4 | `positioning` | Recommended | One large sentence naming the problem or the category | Linear, Ramp, HubSpot, Salesforce |
| 5 | `features` or `products` | Required | Product suite grid when there are several products; feature deep-dives or a workflow narrative for one product | [6/8] live have a suite grid |
| 6 | `how-it-works` | Optional | Numbered 3 steps. Strong for self-serve and services | — |
| 7 | `proof` | Required | Case-study cards with the metric in the headline; or a stat row; or a pull quote | [8/8] live |
| 8 | `integrations` | Recommended for software | Logo grid + count ("Connects to 200+ tools") | HubSpot, Stripe, Ramp |
| 9 | `security` | Required for enterprise, fintech, health | Badge row (SOC 2, ISO 27001, GDPR, HIPAA) + link to the trust page | Fintech and enterprise sites |
| 10 | `awards` | Optional | Analyst or review-site badges (G2, Gartner, Forrester) | HubSpot, Salesforce, Datadog |
| 11 | `faq` | Recommended | Accordion, 5–8 questions about price, setup, security, switching | Ramp, Salesforce |
| 12 | `cta-band` | Required | Restate the hero promise + primary CTA (+ secondary) | [5/8] live; Ramp and Salesforce repeat the hero headline word for word |
| 13 | `footer` | Required | Sitemap footer (4–6 columns) for multi-product companies; compact otherwise | [4/8] live mega footers |

Merge or drop optional sections to keep the page around 6–10 screens tall. The live sample ran from 6,900px (HubSpot) to 16,400px (Salesforce).

## Hero decision table

| Situation | Layout | Visual | Seen on |
|---|---|---|---|
| Software with a strong UI | Centred stack; product UI below, bleeding off the bottom edge | Real product screenshot | Featurebase, Arrows, Morgen, Hex, Novu |
| Fintech, compliance, text-heavy value prop | Split: text left 40–45%, visual right 55–60% | Dashboard UI, product photo, or a live widget | Brex, Sardine, Lemon Squeezy, Alloy (8/10 fintech) |
| An interactive calculator is possible (price, ROI, conversion, quote) | Split, with a **working widget** as the visual | The widget itself | Wise converter |
| Strong brand, abstract product (infrastructure, AI) | Centred, type only, or with an abstract graphic | Type carries it; logos directly below | Polar, Mux, Vercel, Forest Admin |
| Service / industrial | Split with real photography of operations | Photo + floating stat card | Razorpay, Flexport |

Overall, **real product UI is the visual on 59% of B2B homepages**. Prefer it over illustration.

## Hero rules

- Headline, subhead, primary CTA and the top of the visual fit inside 1280×800. `[archive]`
- Headline: 2–3 lines on desktop, sentence case, display:body size ratio about 3:1. `[archive]`
- Subhead: 1–2 sentences that say what the product is and for whom.
- At most 2 buttons. Further paths are text links ("See it in action →"). `[13/29 use two]`
- Self-serve may use an email field as the CTA ("Enter your work email" + button). `[5/29]`
- One accent colour: on the primary CTA and at most one highlighted headline phrase. `[archive]`
- Optional trust line under the CTA: "No credit card required", rating badge or a short logo row.

## Proof strategy

Choose by what the client can actually supply. **Never invent proof.**

| Client has | Use |
|---|---|
| Named customers with measurable results | Case-study cards, headline = metric ("Cut close time by 40%") |
| Many recognisable logos | Logo strip after the hero, logo grid in the proof section |
| Review-site presence | Rating badge in the hero, reviews row in proof |
| Analyst recognition | Awards row near the end |
| Usage numbers | Stat row (3–4 figures, tabular numbers, each with its source or "as of" date) |
| Very little yet (early stage) | Founder note, design-partner quotes, a detailed "how it works", a transparent pricing preview |

Proof must come **before** the first CTA below the hero. `[checker: proof-before-ask]`

## Common mistakes

- Feature grid with nine identical icon cards and no product visual.
- Three different primary CTAs ("Start trial", "Get demo", "Contact us") competing.
- "Trusted by thousands of companies" with no names.
- Hero carousel that auto-rotates (fails WCAG 2.2.2 without a pause control, and hides most messages).
