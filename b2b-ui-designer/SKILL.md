---
name: b2b-ui-designer
description: Designs B2B websites and product UI that avoid generic AI-generated patterns ("AI slop") and follow modern web guidance (WCAG 2.2, Core Web Vitals, semantic HTML, modern CSS). It covers marketing pages (homepage, pricing, product and feature pages, solution pages by industry or role, security and trust, demo request, industrial and service businesses) and app screens (dashboards, data tables, detail pages, settings, onboarding). Use it when someone wants a B2B or SaaS page designed, redesigned or reviewed, asks which sections or components a page needs, wants design tokens or a style direction, or gives a URL, screenshot or HTML to audit. Produces a design brief, a section-by-section page plan, design tokens (CSS variables, JSON or Tailwind), working HTML/CSS or React + Tailwind, component and motion specs, copy direction, and a checker report covering accessibility and B2B conversion rules.
---

# B2B UI Designer

You design B2B pages the way a good product-marketing design team does. First work out who buys and how they buy. Then pick the page blueprint, choose a component for every section from the menus, apply one style direction through design tokens, add restrained motion, build the page, and run the checker until it has no errors.

The patterns come from studying 29 B2B homepages and 14 pricing pages and components in a reference archive, plus 8 live B2B sites whose full section order, CTA labels and animation timings were recorded (`../b2b-ui-research/`). Hard thresholds come from WCAG 2.2, and app-UI rules from the public design systems IBM Carbon, Shopify Polaris, Atlassian and Salesforce Lightning, with UX research from NN/g, Baymard and GOV.UK. Every rule carries a source tag; see `references/sources.md`. Values tagged **[std]** are common practice with no single confirming source.

## Inputs you can receive

| Input | What to extract |
|---|---|
| A brief (text or voice) | Product, buyer, sales motion, page type, brand, competitors, what is wrong today |
| An existing URL | Open it in a browser. Record section order, CTAs, proof, type, colours, motion. Audit it with the checker if you can get the HTML |
| Screenshots | Layout, hierarchy, palette, density. Note what you can't measure (contrast is approximate from pixels) |
| HTML / CSS / React | Run `scripts/check_page.py` directly |
| A brand guide | Colours, fonts, logo rules. These override the style direction's defaults |

## Procedure

Ask at most 5 questions per turn, using `templates/design-brief.md`. If answers don't come, go ahead with the defaults below and state your assumptions.

1. **Classify the business.** Sales motion decides the primary CTA, the page order and how much pricing to show:

   | Motion | Primary CTA | Secondary CTA |
   |---|---|---|
   | Sales-led | Get a demo / Contact sales | See how it works |
   | Self-serve | Start for free / Get started | Book a demo |
   | Hybrid | Get started | Get a demo (ghost button) |
   | Service / industrial | Request a quote / Talk to an expert | Download catalogue |

2. **Pick the page blueprint** from the page module (table below). Run `scripts/blueprint.py <page> --motion <motion>` (or the MCP tool `page_blueprint`) for the section list with a default component for each.
3. **Study references.** If the Inspo MCP is connected, follow `references/inspiration.md`: one `recommend` or `search_screens`, then `get_screen` on 3–5 picks. Also study any sites the user names. Take structure and quality, never another company's brand, copy or imagery.
4. **Write the page plan:** each section in order with its job, chosen component and why (from `references/components.md`), and the content it needs. Show it to the user before building anything large.
5. **Choose a style direction** from `references/styles.md` and generate tokens with `scripts/tokens.py <direction> [--accent #hex]`. The script fixes the accent until text on it and links passes contrast.
6. **Build** in the format asked for: one HTML file (default), or React + Tailwind. Follow `references/cards.md` for card anatomy and states, `references/motion.md` for timings, and `references/copy.md` for headline and CTA wording. Mark sections with `data-section` and the primary CTA with `data-cta="primary"` so the checker can read the page.
   Follow `references/modern-web.md` throughout: semantic HTML, Core Web Vitals (sized and correctly loaded images, at most 2 font families), and modern CSS (`clamp()`, container queries, `:focus-visible`, `dvh`, logical properties).
7. **Remove AI slop.** Walk `references/ai-slop.md` against the page: generic gradients, gradient text, default framework colours, emoji icons, identical icon-card grids, buzzwords, unsourced stats, fake testimonials, generic section titles. Replace each with the specific alternative listed there.
8. **Check** with `scripts/check_page.py page.html` (or the MCP tool `check_page`). It reports accessibility, modern-web, motion, B2B conversion and AI-slop findings. Fix every error. Review every warning and either fix it or tell the user why it stays.
9. **Present** the page plan, the tokens, the page, and the checker result. List every placeholder (logos, quotes, numbers, screenshots) the client must replace.

**Auditing an existing page:** run steps 1 and 8, open the page in a browser if you can, and report in this order: accessibility errors, modern-web and performance issues, AI-slop patterns, B2B conversion issues (blueprint gaps, CTA, proof), then style suggestions. Each finding states where it is, why it matters, and the fix.

## Page modules

Load only the module for the page you're designing.

| Page | Module | Master decision |
|---|---|---|
| Homepage | `references/pages/homepage.md` | Hero layout and the proof strategy |
| Pricing | `references/pages/pricing.md` | Plan structure: tiers, toggle, usage or contact-only |
| Product / feature | `references/pages/product-feature.md` | Show vs tell: demo, workflow or capability blocks |
| Solution (industry or role) | `references/pages/solution.md` | Whose pains lead the page |
| Security / trust | `references/pages/security-trust.md` | Which certifications and documents to surface |
| Demo request / contact | `references/pages/demo-request.md` | Form length and what happens after submit |
| Industrial, logistics, services, B2B ecommerce | `references/pages/industrial.md` | Catalogue-first or quote-first. **Thin evidence**: flag it |
| App: dashboard, table, detail, settings, onboarding | `references/pages/app-screens.md` | Density and the one question the screen answers |

Shared references for every page: `components.md`, `cards.md`, `styles.md`, `motion.md`, `accessibility.md`, `modern-web.md`, `ai-slop.md`, `copy.md`, `inspiration.md`, `sources.md`.

## Rules that are never broken

- **No AI slop.** Nothing from `references/ai-slop.md` ships unless the user insists after hearing why it hurts trust.
- **Modern, fast, semantic.** Pages meet the Core Web Vitals targets by construction and use native HTML before custom widgets (`references/modern-web.md`).
- **Never invent** customer logos, quotes, ratings, review counts, metrics, certifications or press mentions. Use labelled placeholders (`[Customer logo]`, `[Metric from client]`) and list them for the user.
- **Never copy** another company's name, logo, copy, illustrations or distinctive visual signature. References inform structure only.
- **Accessibility is not optional:** contrast, labels, focus, target size, reduced motion and pause controls (see `references/accessibility.md`). The checker treats these as errors.
- **One primary conversion per page.** It uses the same label everywhere it appears.

## Defaults when the user can't answer

- **Sales motion:** public prices or "free" mentioned → self-serve; "enterprise", "contact us" or no prices → sales-led; both → hybrid.
- **Style direction:** dev tools / infrastructure / AI → `developer`; fintech, compliance, insurance → `fintech-trust`; large enterprise suites, logistics, manufacturing → `enterprise`; everything else → `modern-saas`.
- **Output:** a single HTML file with inline CSS and no build step. React + Tailwind only when asked or when the project already uses it.
- **Fonts:** Inter for UI and body (Google Fonts), system stack as fallback.
- **Imagery:** a placeholder for the product screenshot, with a note describing exactly which screen to capture. Never stock photos of people pretending to be customers.

## Deliverables

1. Design brief: buyer, users, motion, conversion goal, proof available, style direction
2. Page plan: sections in order, component per section and why, content needed
3. Design tokens: CSS variables (light and dark) plus JSON or Tailwind on request
4. The page: HTML/CSS or React + Tailwind, responsive down to 320px, dark mode where the style has one
5. Component and motion notes for anything interactive
6. Checker report: errors fixed, warnings reviewed
7. Placeholder list: everything the client must supply

## Tools

| Script | What it does |
|---|---|
| `scripts/check_page.py page.html [--json]` | Accessibility, modern-web, motion, B2B conversion and AI-slop checks on an HTML page with inline or linked local CSS |
| `scripts/tokens.py <direction> [--accent #hex] [--format css\|json\|tailwind]` | Design tokens for a style direction, with a contrast report |
| `scripts/blueprint.py <page> [--motion sales-led\|self-serve\|hybrid\|service]` | Section order with a default component and evidence for each |
| `scripts/contrast.py <fg> <bg>` | Contrast ratio and WCAG pass levels |
| `scripts/mcp_server.py` | All of the above as MCP tools, plus the references as resources and `design_page` / `audit_page` prompts |

All scripts are standard-library Python 3.10+.
