# App screens: dashboards, tables, detail pages, settings, onboarding

**Master decision:** density, and the one question the screen answers.

App UI isn't in the reference archive, so these rules come from public design systems: `[CARBON]` IBM Carbon, `[POLARIS]` Shopify Polaris, `[ATLAS]` Atlassian, `[SLDS]` Salesforce Lightning, plus `[NNG]`. Values tagged **[verify]** should be checked against the current docs.

## Shell

- Left sidebar nav (collapsible to icons) for 5+ areas; top bar for search (⌘K), notifications, account, workspace switcher.
- Page header: breadcrumb (if nested) → title → primary action on the right.
- Content max width only for reading pages (settings, docs). Tables and dashboards use full width.
- App body type 14px, line-height 20px. `[CARBON]` `[SLDS]` **[verify]**
- Motion: the fast ("productive") end of every range in `motion.md`.

## Dashboard

Order: title + date range and filters (top right, applied to the whole page) → **3–5 KPI cards** → the one main chart (full width) → supporting charts in 2 columns → detail table. `[CARBON]` `[POLARIS]`

| KPI card part | Rule |
|---|---|
| Label | Plain name with the period ("Revenue, last 30 days") |
| Value | Large, tabular numbers, unit included |
| Change | Versus the previous period, as an arrow + % + colour **and** text (colour is never the only signal, `[WCAG 1.4.1]`) |
| Sparkline | Optional, no axes |

Chart titles state the insight ("Signups up 18% since pricing change"), axes carry units, and every chart has an empty and an error state.

## Data table

| Rule | Source |
|---|---|
| Density toggle: compact / default / comfortable. Carbon row heights 32 / 48 / 64px (also 24 and 40) | `[CARBON]` **[verify]** |
| Numbers right-aligned, text left-aligned, headers aligned with their data | `[CARBON]` `[NNG]` |
| Sticky header row; sticky first column when the table scrolls sideways | `[CARBON]` `[POLARIS]` |
| Toolbar: search, filters, column settings, export | `[CARBON]` |
| Active filters shown as removable chips with "Clear all" | `[POLARIS]` |
| Row selection → a bulk action bar replaces the toolbar and shows "N selected" | `[CARBON]` `[POLARIS]` |
| Sortable columns show the sort direction and use `aria-sort` | `[WCAG]` |
| Pagination with the total count and page-size choice, or "load more" | `[CARBON]` |
| Row hover highlight instead of zebra stripes by default | `[std]` |
| Loading = skeleton rows; empty = explanation + primary action; error = what failed + retry | `[POLARIS]` `[ATLAS]` |

## Detail page

Breadcrumb → title, status badge, key actions → tabs (Overview, Activity, Settings) → content in cards on the left (2/3), metadata and activity sidebar on the right (1/3).

## Settings

Left nav of sections → one section per page → grouped form cards with a heading and short description → a save bar that appears and sticks when anything changes, or autosave with a "Saved" status. Destructive actions sit in a separate "Danger zone" card and need confirmation by typing the name. `[ATLAS]` `[POLARIS]`

## Onboarding

- Show progress ("Step 2 of 4"), one task per screen, and let users skip.
- Ask only for what makes the first session useful (workspace name, invite teammates, connect one integration).
- Finish on a screen with real or sample data. Never drop users on an empty dashboard.
- Empty states everywhere: a short explanation, an illustration or icon, the primary action, and a link to docs or sample data. `[POLARIS]`
