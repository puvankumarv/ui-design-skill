# Sources

Every rule in this skill carries one of these tags. Values tagged **[verify]** were recorded from memory of the published documentation and must be confirmed against the live source before a release that depends on them. **[std]** marks common practice with no single confirming source: flag it to the user.

## Standards and platform guidance

| Tag | Source | Used for |
|---|---|---|
| `WCAG` | W3C, Web Content Accessibility Guidelines 2.2 (Recommendation, Oct 2023), https://www.w3.org/TR/WCAG22/ | Contrast, target size, focus, labels, motion, reflow |
| `WEBDEV` | Google, web.dev: Core Web Vitals, image and font performance, https://web.dev/articles/vitals | LCP / INP / CLS targets, image and font loading |
| `MDN` | Mozilla, MDN Web Docs, https://developer.mozilla.org/ | Modern CSS and HTML features |
| `HTML` | WHATWG HTML Living Standard, https://html.spec.whatwg.org/ | Semantic elements |
| `APG` | W3C WAI-ARIA Authoring Practices Guide, https://www.w3.org/WAI/ARIA/apg/ | Menus, tabs, dialogs, accordions |

## Design systems

| Tag | Source | Used for |
|---|---|---|
| `CARBON` | IBM Carbon Design System, https://carbondesignsystem.com/ | Spacing scale, data tables, motion durations and easing, dashboards |
| `POLARIS` | Shopify Polaris, https://polaris.shopify.com/ | Admin layouts, filters, empty states, settings |
| `ATLAS` | Atlassian Design System, https://atlassian.design/ | Forms, empty states, danger zones |
| `SLDS` | Salesforce Lightning Design System, https://www.lightningdesignsystem.com/ | Enterprise density, app body type |
| `M3` | Google Material Design 3, https://m3.material.io/ | Motion durations and easing |
| `GOVUK` | GOV.UK Design System, https://design-system.service.gov.uk/ | Form patterns, error messages, button labels |

## UX research

| Tag | Source | Used for |
|---|---|---|
| `NNG` | Nielsen Norman Group: B2B website usability research, form and table articles, https://www.nngroup.com/ | Pricing transparency, buying committees, proof, forms |
| `BAY` | Baymard Institute: form and checkout usability research, https://baymard.com/ | Labels, required / optional marking, inline validation, line length |

## This project's own research

| Tag | Source | Used for |
|---|---|---|
| `[archive]`, `[n/29]` | 29 B2B homepages, 4 pricing pages and 10 pricing components from the Inspo archive, captured 2026-11-22 (`../b2b-ui-research/site_survey.md`) | Hero layouts, visuals, CTAs, fold rules, style directions |
| `[live]`, `[n/8]` | 8 live B2B homepages + Linear pricing, recorded 2026-11-22 (`../b2b-ui-research/live_site_notes.md`) | Section order, CTA frequency, motion timings |

Site names appear in this skill only to cite where a structural pattern was observed. They are not endorsements, and their brands and content are never reused.
