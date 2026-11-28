# Changelog

## 0.2.0 (2026-11-28)

- New example pages: a SaaS pricing page (billing toggle, plan cards, comparison table) and an API dashboard in the developer style (dark by default, light theme, KPI cards, charts, data table with density toggle). Examples now cover the homepage, pricing and app-dashboard blueprints in two style directions.
- Checker: transparent backgrounds are no longer measured for contrast (they showed false failures on dark themes).
- Checker: on pricing pages the primary CTA is expected in the plan cards rather than the hero, as the pricing blueprint specifies.
- Checker: app screens are exempt from the unsourced-stat rule, since their figures are the user's own data.

## 0.1.0 (2026-11-24)

First version.

- Skill with 8 page modules (homepage, pricing, product-feature, solution, security-trust, demo-request, industrial, app-screens) and shared references for components, cards, styles, motion, accessibility, modern web, AI slop, copy and inspiration.
- Page checker with accessibility, semantic HTML, performance, modern CSS, motion, B2B conversion and AI-slop rules.
- Design tokens for 5 style directions, with contrast-safe handling of any brand accent.
- Page blueprints per page type and sales motion.
- MCP server (dual-era protocol) with tools, resources, prompts and completions.
- Example SaaS homepage that passes the checker.
- Research notes from 29 archive homepages, 8 live B2B sites and public design systems.
