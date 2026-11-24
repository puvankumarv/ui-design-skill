# UI Design Skill (B2B UI Designer)

**B2B websites and product UI, designed from real-site research and checked for accessibility, modern web practice and AI slop.** It's a Claude skill with an MCP server; the skill and plugin are named `b2b-ui-designer`.

Give it a brief, a URL, screenshots or HTML. It covers:

- **Marketing pages:** homepage, pricing, product and feature pages, solution pages by industry or role, security and trust, demo request, and industrial / logistics / B2B ecommerce sites
- **App screens:** dashboards, data tables, detail pages, settings, onboarding
- **Audits** of existing pages

For each page it produces:
- a design brief, and a page plan listing each section, its component and why,
- design tokens (CSS variables for light and dark mode, JSON or Tailwind) whose contrast is guaranteed,
- the page as one HTML file or React + Tailwind,
- a checker report and a list of every placeholder the client must replace.

## Where the rules come from

- **29 B2B homepages** plus pricing pages and components from a reference archive of real sites (hero layouts, visuals, CTAs, type, colour).
- **8 live B2B sites:** full section order, CTA labels and counts, and measured animation timings.
- **Standards and design systems:** WCAG 2.2, web.dev Core Web Vitals, IBM Carbon, Shopify Polaris, Atlassian, Salesforce Lightning, Material 3, GOV.UK, NN/g and Baymard.

Every rule carries a source tag (`b2b-ui-designer/references/sources.md`). The raw research is in `b2b-ui-research/`.

## What the checker verifies

| Family | Checks |
|---|---|
| Accessibility (`a11y-*`) | Text contrast (CSS rules and design tokens, every theme), form labels, button and link names, alt text, focus visibility, target size |
| Semantic HTML (`html-*`) | lang, title, viewport, charset, description, one `<main>`, one `<h1>`, heading order, clickable divs |
| Performance (`perf-*`) | Image width/height (CLS), lazy-loaded hero (LCP), lazy-loading below the fold, font families and `display=swap`, render-blocking scripts, video attributes |
| Modern CSS (`css-*`) | `100vh` → `dvh`, `color-scheme` with dark themes |
| Motion (`motion-*`) | `prefers-reduced-motion`, pause controls for loops and autoplay video, hover timing, animating layout properties |
| B2B (`b2b-*`) | Sections marked, one primary CTA label, CTA in the hero and repeated, ≤ 2 hero buttons, proof present and before the ask, one CTA band, pricing units and an enterprise path, reading width, form marking, autocomplete and button labels |
| AI slop (`slop-*`) | Purple/indigo gradients, gradient text, default framework colours, glassmorphism overuse, emoji icons, buzzwords, unsourced stats, fake testimonials, vague proof, lorem ipsum, generic section titles, stock and placeholder media |

## What's inside

| Path | What it is |
|---|---|
| `b2b-ui-designer/SKILL.md` | The skill: procedure, page modules, rules, deliverables |
| `b2b-ui-designer/references/pages/` | One module per page type: homepage, pricing, product-feature, solution, security-trust, demo-request, industrial, app-screens |
| `b2b-ui-designer/references/` | Components, cards, styles, motion, accessibility, modern web, AI slop, copy, inspiration, sources |
| `b2b-ui-designer/templates/` | Design brief and intake questions; blueprint data |
| `b2b-ui-designer/scripts/check_page.py` | The page checker |
| `b2b-ui-designer/scripts/tokens.py` | Design tokens for 5 style directions, contrast-safe for any brand accent |
| `b2b-ui-designer/scripts/blueprint.py` | Section order per page type and sales motion |
| `b2b-ui-designer/scripts/contrast.py` | WCAG contrast ratios |
| `b2b-ui-designer/scripts/mcp_server.py` | MCP server: the tools above, references as resources, `design_page` and `audit_page` prompts |
| `b2b-ui-designer/examples/` | A homepage built by the skill that passes the checker with no errors or warnings |
| `b2b-ui-research/` | Research notes: archive survey, live-site measurements, design-system rules |
| `tests/` | Unit tests run by CI |

## Install

**Claude Code: plugin**
```
/plugin marketplace add puvankumarv/ui-design-skill
/plugin install b2b-ui-designer@b2b-ui-designer
```

**Any agent that supports skills**
```bash
npx skills add puvankumarv/ui-design-skill
```

**MCP server only** (any MCP client; Python 3.10+, no dependencies)
```json
{ "mcpServers": { "b2b-ui-designer": { "command": "python3", "args": ["/path/to/b2b-ui-designer/scripts/mcp_server.py"] } } }
```

It works best with a reference-archive MCP (such as Inspo) connected too: the skill then studies 3–5 real sites before each design.

## Use the scripts directly

```bash
python3 b2b-ui-designer/scripts/blueprint.py homepage --motion sales-led --enterprise
python3 b2b-ui-designer/scripts/tokens.py fintech-trust --accent "#0f766e" --report
python3 b2b-ui-designer/scripts/check_page.py my-page.html
```

## License

MIT
