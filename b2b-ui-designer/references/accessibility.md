# Accessibility

Target: **WCAG 2.2 level AA**, plus a few AAA items that cost little. Enterprise buyers increasingly require an accessibility conformance report (VPAT) before purchase, so this is a sales requirement as well as a legal one.

## Thresholds the checker enforces

| Rule | Threshold | WCAG | Checker id |
|---|---|---|---|
| Body text contrast | ≥ 4.5:1 | 1.4.3 AA | `a11y-contrast` |
| Large text (≥ 24px, or ≥ 18.66px bold) | ≥ 3:1 | 1.4.3 AA | `a11y-contrast` |
| Borders of inputs, icons, focus ring | ≥ 3:1 | 1.4.11 AA | (tokens report) |
| Target size | ≥ 24×24px; 44×44px for primary actions on touch | 2.5.8 AA / 2.5.5 AAA | `a11y-target` |
| Visible focus | `:focus-visible` style present if outlines are removed | 2.4.7 AA | `a11y-focus` |
| Images | `alt` on every `<img>` (`alt=""` if decorative) | 1.1.1 A | `a11y-img-alt` |
| Form labels | Every input has a `<label>`, `aria-label` or `aria-labelledby`. Placeholder doesn't count | 3.3.2 A, 1.3.1 A | `a11y-label` |
| Names for buttons and links | Visible text or `aria-label` | 4.1.2 A, 2.4.4 A | `a11y-name` |
| Page language | `<html lang>` | 3.1.1 A | `html-lang` |
| Headings | One `<h1>`, no skipped levels | 1.3.1 A | `html-h1`, `html-heading-order` |
| Auto-moving content > 5s | Pause control | 2.2.2 A | `motion-pause` |
| Interaction-triggered motion | Disabled under `prefers-reduced-motion` | 2.3.3 AAA (treated as required) | `motion-reduced` |

## Rules the checker can't fully see (check by hand)

- **Colour is never the only signal** (status, errors, chart series, required fields). `[1.4.1]`
- **Reflow at 320px** without horizontal scrolling, and text resizable to 200%. `[1.4.10, 1.4.4]`
- **Keyboard:** every control reachable with Tab, in visual order; menus, tabs and dialogs follow the WAI-ARIA Authoring Practices patterns; Esc closes overlays; focus returns to the trigger. `[2.1.1, 2.4.3]`
- **Focus not obscured** by the sticky header or cookie banner (`scroll-padding-top` equal to the header height). `[2.4.11]`
- **Skip link** to `<main>` as the first focusable element. `[2.4.1]`
- **Error messages** say what went wrong and how to fix it, next to the field, linked with `aria-describedby`, and announced. `[3.3.1, 3.3.3]`
- **Don't ask twice** for the same information in one flow. `[3.3.7]`
- **Accessible sign-in:** allow paste and password managers; no puzzles. `[3.3.8]`
- **Dragging** (sortable lists, sliders) has a click or keyboard alternative. `[2.5.7]`
- **Consistent help:** contact and help links in the same place on every page. `[3.2.6]`
- Charts have a text summary or data table alternative.

## Patterns

- Focus ring: `outline: 2px solid var(--focus); outline-offset: 2px;` on `:focus-visible`.
- Visually hidden text for icon-only buttons: a `.sr-only` span, or `aria-label`.
- Accordions: `<details>/<summary>`. Tabs: `role="tablist"` with arrow-key navigation. Dialogs: `<dialog>` with `showModal()`.
- Tables: `<th scope>`, `<caption>`, `aria-sort` on sorted headers.
