# Live B2B site pass — full section order and motion

Captured 2026-11-22 in the built-in browser. For each homepage a script scrolled the full page, then recorded the visible h1–h3 headings in order, the CTA labels and how often each appears, CSS transition durations, running CSS animations, header positioning and video count. Section order below is read from the headings. Regional redirects were followed (Stripe → /in, Ramp → /en-gb, Salesforce → /in, Rippling → /en-GB).

**Limits:** headings miss sections with no heading tag (Datadog uses very few). JavaScript-driven motion (GSAP, Framer Motion) is often bundled and isn't detected through `window` globals, so "no library found" doesn't mean "no JS motion".

## Section order per site

| Site | Model | Section order (top → bottom) | Page height |
|---|---|---|---|
| **Stripe** | Hybrid | Hero → product suite (6 solution cards) → scale stats ("backbone of global commerce") → segments: enterprise / startups / platforms, each with case-study cards → developer & integrations (3 points) → news / reports | 14,057px |
| **Linear** | Self-serve + sales | Hero → logo marquee → positioning statement → 4 workflow sections (intake → planning → AI → build & ship) → changelog → final CTA → footer | 10,185px |
| **Ramp** | Hybrid | Hero → platform statement → "busywork" features (4) → testimonials ("Trusted by finance, loved by employees") → product suite (6) → FAQ (8 questions) → final CTA **repeating the hero headline** | 7,742px |
| **HubSpot** | Hybrid | Hero → 3 value props → "What is HubSpot?" → customer count (311,000+) → product hubs (10) → AI agents (3) → integrations (2,000+) → results + G2 badge → final CTA → mega footer | 6,922px |
| **Datadog** | Free trial + sales | Hero → analyst badge (Forrester Wave Leader) → product catalogue | 7,562px |
| **Salesforce** | Sales-led | Hero → value statement → customer logos → 8 platform sections → values → 5 case studies, **each headline a metric** ("cuts loan processing time by 90%") → G2 leader → resources → final CTA repeating H1 → FAQ | 16,429px |
| **Rippling** | Sales-led | Hero → app modules → "operating system" story → benefits → what's new → demo options (live / on demand) → demo request form | 8,144px |
| **Flexport** | Sales-led, logistics | Hero → services (5: ocean, air, customs, fulfilment, control tower) → insights / news (5) → newsletter → mega footer | 12,010px |
| **Linear pricing** | — | 4 tiers (Free, Basic, Business, Enterprise) → comparison table → final CTA | — |

## Patterns across the live sites

| Pattern | Seen on |
|---|---|
| Product-suite grid (one card per product or service) | Stripe, Ramp, HubSpot, Flexport, Rippling, Salesforce (6/8) |
| Case studies with a **number in the headline** | Stripe, Salesforce |
| Analyst or review-site badge (Gartner, Forrester, G2) | HubSpot, Salesforce, Datadog |
| Integrations section with a count ("2,000+") | HubSpot, Stripe, Ramp |
| FAQ near the end | Ramp, Salesforce |
| Final CTA band before the footer | Linear, Ramp, HubSpot, Salesforce, Rippling (5/8) |
| Final CTA reuses the hero headline | Ramp, Salesforce |
| News / changelog / insights section near the end | Stripe, Linear, Rippling, Flexport |
| Mega footer (5–7 link columns) | Linear, HubSpot, Flexport, Salesforce |

## CTA labels and frequency

| Site | Labels (count on page) | Reading |
|---|---|---|
| Stripe | Contact sales ×3, Get started ×1 | Sales CTA repeated; self-serve once |
| Linear | Get started, Sign up, Contact sales (×1 each) | Restrained |
| Ramp | Get started ×2, Get started for free, Get started now, See a demo | Self-serve dominant, demo secondary |
| HubSpot | Get a demo, Contact us | |
| Rippling | **Get a demo ×6**, Request live demo | Pure sales-led: one CTA, repeated |
| Flexport | Request a demo, Get started, Product demos, Contact us | |
| Salesforce | Start for free, Start a free trial, Watch demo, Watch all demos | Free trial + recorded demos |

**Rule drawn:** one primary conversion per page, repeated 3–6 times on a long page. Sales-led: "Get a demo" / "Contact sales". Self-serve: "Get started" / "Start for free". Hybrid: self-serve primary, demo as the ghost button.

## Motion measured

| Site | Most common transition | Other durations | CSS animations |
|---|---|---|---|
| Stripe | 0.25s | 0.15–0.4s UI; **0.6–1s** with `cubic-bezier(0.16, 1, 0.3, 1)` (strong ease-out) for reveals | Bento grid path loops 4–7s, fade-in 0.5s |
| Linear | **0.1s** (276 elements) | 0.16s, 0.4s, 0.7s | Logo marquee 30s, dot-grid loop 2.8s |
| Ramp | **0.2s** (154) | 0.15–0.3s | Logo marquee 180s, auto-advancing accordion 10s |
| HubSpot | **0.3s** (89) | 0.15–0.5s | Logo scroll 19s |
| Datadog | 0.15–0.3s | — | Logo animation 0.2s |
| Salesforce | 0.3s / 0.15s | 0.1–0.22s | Logo marquee 85s, floating spark 6s |
| Rippling | 0.15s | 0.3s, 0.5s | Skeleton shimmer 1.6s |
| Flexport | **0.15s** (535) | 0.06–0.6s | Drop-in 0.24s, grow 0.55s |

**Rules drawn:**
- Hover and press feedback: **100–200ms**. Nobody goes above 300ms for direct feedback.
- Panel, tab and accordion changes: **200–300ms**.
- Scroll reveals and hero entrances: **400–800ms** with a strong ease-out curve.
- Ambient loops (logo marquees, background graphics): 20–180s, slow enough to read as texture.
- Auto-advancing content (Ramp's accordion, every 10s) needs a pause control under WCAG 2.2.2.
- Video is common: HubSpot 15, Datadog 12, Ramp 5. Product demos are shown as short muted loops.

## Header behaviour

Fixed header: Linear, Ramp, Flexport. Static/relative `<header>` (may still use an inner sticky bar): Stripe, HubSpot, Datadog, Salesforce, Rippling. Treat sticky nav as the default for long pages, with a compact height (56–72px).
