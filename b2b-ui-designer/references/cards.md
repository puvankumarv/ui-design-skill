# Card anatomy

One spec, rendered three ways depending on the style direction.

## Content order

1. Media or icon (optional): a UI crop, logo or icon
2. Eyebrow (optional): category or label, small caps or small text
3. Title: 1 line, max 2. States the benefit or the name
4. Body: 2–3 lines, max ~140 characters
5. Action: a link ("Learn more →") or a button

If the card has a single destination, make the **whole card** the link: put the `<a>` on the title and stretch its click area with a `::after` overlay. Never nest interactive elements inside a clickable card.

## Values per style direction

| Property | `enterprise` | `modern-saas` / `fintech-trust` | `developer` (dark) | `editorial` |
|---|---|---|---|---|
| Surface | `--surface` on a `--bg-subtle` section | `--surface` on `--bg` | `--surface` slightly lighter than `--bg` | `--bg` (no card fill) |
| Edge | 1px `--border` | Soft shadow `--shadow-sm` | 1px `--border` at low alpha + inner top highlight | Top rule only |
| Radius | `--radius-sm` (4–6px) | `--radius-lg` (12–16px) | `--radius-md` (8–10px) | 0 |
| Padding | 24px | 24–32px | 24px | 0 + 24px top |
| Hover | Border to `--border-strong` | Lift 2px + `--shadow-md`, 200ms | Border brightens, 150ms | Title underline |
| Icon | Line icon in a 40px tinted square | Duotone icon or UI crop | Mono glyph or code | None |
| Title | 18px / 600 | 20px / 600 | 18px / 500 | 22px serif |

## States (all required for interactive cards)

| State | Rule |
|---|---|
| Default | As above |
| Hover | One change only (border **or** lift **or** underline) |
| Focus-visible | 2px outline in `--focus`, 2px offset, ≥ 3:1 against the background `[WCAG 2.4.7, 1.4.11]` |
| Active / pressed | Remove lift, slightly darker border |
| Disabled | 50% opacity is not enough on its own; add "Unavailable" text and `aria-disabled` |
| Loading (app UI) | Skeleton blocks in the same layout, shimmer ≤ 1.6s loop, static under reduced motion |
| Selected (app UI) | Accent border + checkmark + `aria-selected` / `aria-pressed`, never colour alone |

## Card grids

- Use CSS Grid with `subgrid` (or fixed internal rows) so titles, bodies and actions line up across cards.
- 3 columns desktop, 2 tablet, 1 mobile, via `repeat(auto-fit, minmax(18rem, 1fr))` or container queries.
- Equal-height cards, but never pad short copy with filler to match long copy.
- A grid of more than 6 identical cards is a list. Use a list or table.
