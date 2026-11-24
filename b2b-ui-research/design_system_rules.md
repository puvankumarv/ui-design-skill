# Rules from design systems, standards and UX research

This file fills the archive's biggest gap: **app UI** (dashboards, tables, forms, settings). It also adds hard accessibility thresholds. Each rule carries a source tag. Values marked **[verify]** come from memory of the published docs and must be checked against the live source before the skill ships.

Source tags: `WCAG` (W3C WCAG 2.2) · `CARBON` (IBM Carbon) · `POLARIS` (Shopify Polaris) · `ATLAS` (Atlassian Design System) · `SLDS` (Salesforce Lightning) · `M3` (Material Design 3) · `NNG` (Nielsen Norman Group) · `BAY` (Baymard Institute) · `GOVUK` (GOV.UK Design System)

## 1. Accessibility thresholds (checker rules)

| Rule | Threshold | Source |
|---|---|---|
| Body text contrast | ≥ 4.5:1 | WCAG 1.4.3 (AA) |
| Large text contrast (≥ 24px, or ≥ 18.66px bold) | ≥ 3:1 | WCAG 1.4.3 (AA) |
| UI component and graphic contrast (borders, icons, focus ring) | ≥ 3:1 | WCAG 1.4.11 (AA) |
| Target size, minimum | ≥ 24×24 CSS px, or enough spacing | WCAG 2.5.8 (AA) |
| Target size, recommended for primary actions | 44×44 CSS px | WCAG 2.5.5 (AAA) |
| Visible focus indicator | Required | WCAG 2.4.7 (AA) |
| Focus not hidden by sticky header or cookie banner | Required | WCAG 2.4.11 (AA) |
| Auto-moving content > 5s (carousels, marquees, auto-advance) | Pause / stop control | WCAG 2.2.2 (A) |
| Motion triggered by interaction can be turned off | Respect `prefers-reduced-motion` | WCAG 2.3.3 (AAA); treat as required |
| Reflow at 320px wide with no horizontal scroll | Required | WCAG 1.4.10 (AA) |
| Every input has a programmatic label | Required | WCAG 3.3.2 / 1.3.1 |
| Don't ask for the same info twice in a flow | Required | WCAG 3.3.7 (A) |
| No cognitive test to sign in (allow paste, password managers) | Required | WCAG 3.3.8 (AA) |

## 2. Spacing and grid

- Base unit **8px** with a 4px half-step for tight UI. `CARBON` `ATLAS` `POLARIS` (Polaris uses a 4px base).
- Carbon spacing scale: 2, 4, 8, 12, 16, 24, 32, 40, 48, 64, 80, 96, 160 px. `CARBON` **[verify]**
- Marketing sections: 80–160px vertical padding on desktop, 48–80px on mobile. (Archive measurement, `site_survey.md`.)
- Content max-width 1200–1280px; text column 60–75 characters. `BAY` `NNG`
- 12-column grid on desktop, 4 columns on mobile. `CARBON` `M3`

## 3. Typography

- B2B default: a neutral grotesk (Inter, Geist, IBM Plex Sans, system UI). 79% of surveyed sites use one.
- Serif display only for headlines, and only when the brand wants a trust or editorial voice (fintech, compliance, consulting).
- Product UI body: 14px; marketing body: 16–18px. `CARBON` `SLDS` **[verify exact defaults]**
- Use tabular numbers (`font-variant-numeric: tabular-nums`) in tables, prices and stats.
- Left-align body text; centre only short hero and section headings. `NNG`

## 4. Data tables (app UI)

| Rule | Detail | Source |
|---|---|---|
| Row density options | Carbon row heights: 24 (xs), 32 (sm), 40 (md), 48 (lg, default), 64 (xl) px | `CARBON` **[verify]** |
| Offer a density toggle | Compact for power users, comfortable for occasional ones | `CARBON` `ATLAS` |
| Align numbers right, text left | Headers align with their data | `CARBON` `NNG` |
| Sticky header row on long tables | | `CARBON` `POLARIS` |
| Bulk actions appear when rows are selected | Action bar replaces toolbar | `CARBON` `POLARIS` |
| Filters above the table; show active filters as removable chips | | `POLARIS` `NNG` |
| Pagination or "load more" with total count | | `CARBON` |
| Empty, loading (skeleton) and error states for every table | | `POLARIS` `ATLAS` |
| No zebra striping by default; use row hover | Stripes add noise in dense tables | `CARBON` (uses optional zebra) **[verify]** |

## 5. Forms (demo requests, signup, settings)

| Rule | Source |
|---|---|
| Single column | `BAY` `NNG` |
| Labels above fields, never placeholder-only | `BAY` `GOVUK` `NNG` |
| Mark both required and optional fields explicitly | `BAY` |
| Validate inline after the user leaves a field, not on every keystroke | `BAY` `NNG` |
| Error message says what went wrong and how to fix it, placed next to the field | `GOVUK` `NNG` |
| Demo forms: ask only what sales needs to route (name, work email, company, size). Enrich the rest later | Common B2B practice; `NNG` on form length |
| Field width matches expected input length | `GOVUK` `BAY` |
| Primary button left-aligned under the form, verb label ("Book demo", not "Submit") | `GOVUK` `NNG` |

## 6. Dashboards

- Top row: 3–5 KPI cards (label, value, change vs period, sparkline). `CARBON` `POLARIS`
- Then the one chart that answers the main question, full width. Then supporting charts in 2 columns, then a detail table.
- Date range picker and filters placed top-right, applying to the whole page.
- Every chart has a title that states the insight, units on axes, and an empty state.

## 7. Motion (design-system values)

| System | Durations | Easing |
|---|---|---|
| Carbon | fast-01 70ms, fast-02 110ms, moderate-01 150ms, moderate-02 240ms, slow-01 400ms, slow-02 700ms | Productive standard `cubic-bezier(0.2, 0, 0.38, 0.9)`; expressive standard `cubic-bezier(0.4, 0.14, 0.3, 1)` **[verify]** |
| Material 3 | Short 50–200ms, medium 250–400ms, long 450–600ms | Emphasized `cubic-bezier(0.2, 0, 0, 1)` **[verify]** |

Carbon's split maps directly to B2B: **productive** motion (fast, subtle) inside the app; **expressive** motion (slower, more noticeable) for marketing moments and key transitions.

## 8. B2B buying behaviour (shapes page content)

- Buyers look for pricing early. Hiding it entirely is a common frustration; give at least a starting price or what the price depends on. `NNG` (B2B website usability research)
- Several people are involved in buying (users, managers, IT/security, finance, legal). Pages need a path for each: product detail, ROI, security/compliance, procurement docs. `NNG`
- Proof must be specific: named customers, real metrics, analyst reports. Vague claims ("trusted by thousands") carry little weight. `NNG`
- Security, compliance and integration questions block deals late. A security/trust page and an integrations page are expected on enterprise sites.
