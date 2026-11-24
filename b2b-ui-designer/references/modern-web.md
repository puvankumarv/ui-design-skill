# Modern web guidance

Build pages the way the current web platform expects: semantic, fast, resilient, and using modern CSS instead of workarounds. Source tags: `[WEBDEV]` web.dev (Google), `[MDN]` MDN Web Docs, `[WCAG]`, `[HTML]` the HTML Living Standard.

## Performance: Core Web Vitals

Targets at the 75th percentile of page loads. `[WEBDEV]`

| Metric | Good | What usually breaks it in B2B pages | Do |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | ≤ 2.5s | Huge hero screenshot, lazy-loaded hero image, web fonts blocking text | Hero image: correct size, AVIF/WebP, `fetchpriority="high"`, **never** `loading="lazy"`; preload the main font |
| **INP** (Interaction to Next Paint) | ≤ 200ms | Heavy JS for menus, carousels, chat widgets | Native HTML (`<details>`, `<dialog>`, popover), little JS, defer third-party scripts |
| **CLS** (Cumulative Layout Shift) | ≤ 0.1 | Images without dimensions, late cookie banners pushing content, font swaps | `width`/`height` (or `aspect-ratio`) on every image and video; banners overlay, never push; `size-adjust` fallback fonts |

Checker: `perf-img-dimensions`, `perf-lazy-hero`, `perf-lazy-below`, `perf-fonts`.

## Images and media

- Every `<img>` has `width` and `height` attributes (or a CSS `aspect-ratio`). `[WEBDEV]`
- Below-the-fold images use `loading="lazy"` and `decoding="async"`; the hero image does not. `[WEBDEV]`
- Serve `srcset`/`sizes` or `<picture>` with AVIF/WebP. Product screenshots: export at 2× and compress.
- Video: `muted playsinline` for autoplay loops, a `poster`, `preload="none"` or `metadata` below the fold, and controls or a pause button. `[WCAG 2.2.2]`
- Decorative images: `alt=""`. Meaningful ones: alt text that says what the image shows.

## Fonts

- At most 2 families (display + body), plus a mono only for code. Each family costs load time. `[WEBDEV]`
- Google Fonts URLs include `&display=swap`; self-hosted fonts use `font-display: swap`. `[WEBDEV]`
- Preconnect to the font origin; prefer variable fonts over several static weights.
- Fallback stack: `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`.

## Semantic HTML

- Landmarks: one `<header>`, `<nav>`, **one `<main>`**, `<footer>`; `<section>` with a heading for each page section. `[HTML]` `[WCAG 1.3.1]`
- One `<h1>`; heading levels in order without skips.
- Buttons are `<button>`, links are `<a href>`. Never a clickable `<div>`. `[WCAG 4.1.2]`
- Native elements before custom widgets: `<details>/<summary>` for FAQs, `<dialog>` for modals, the `popover` attribute for menus, `<input type="range">`, `<select>`. `[MDN]`
- `<html lang>`, `<meta charset>`, `<meta name="viewport" content="width=device-width, initial-scale=1">`, a `<title>` and `<meta name="description">`.
- Social sharing: Open Graph title, description and image.

Checker: `html-*` rules.

## Modern CSS to reach for

| Need | Use | Instead of |
|---|---|---|
| Fluid type and spacing | `clamp(1rem, 0.9rem + 0.5vw, 1.25rem)` | Breakpoint-by-breakpoint font sizes |
| Components that adapt to their container | Container queries (`container-type: inline-size` + `@container`) | Viewport media queries inside components |
| Full-height sections on mobile | `100dvh` / `100svh` | `100vh` (jumps with mobile browser bars) |
| Colour tokens and tints | Custom properties, `color-mix()`, `oklch()` | Hard-coded hex everywhere |
| Dark mode | `prefers-color-scheme` + `color-scheme: light dark` + a `data-theme` override | Separate stylesheets |
| Parent-aware styling | `:has()` (e.g. form row with an invalid input) | Extra JS-toggled classes |
| Layout | Grid (with `subgrid` for card alignment) and Flexbox with `gap` | Floats, margin hacks |
| Internationalisation | Logical properties (`margin-inline`, `padding-block`, `inset-inline-start`) | `left`/`right` |
| Focus styles | `:focus-visible` with a 2px outline at ≥ 3:1 contrast | `outline: none` |
| Text balance | `text-wrap: balance` on headings, `text-wrap: pretty` on paragraphs | Manual `<br>` |
| Page and state transitions | View Transitions API, `@starting-style`, with reduced-motion fallback | Heavy animation libraries for simple fades |
| Scroll-linked effects | `animation-timeline: view()` (progressive enhancement) | Scroll event listeners |
| Reading width | `max-width: 65ch` on text | Fixed pixel widths |

Use the newest features as progressive enhancement: the page must still work and look right without them.

Checker: `css-100vh`, `css-no-focus-visible`, `css-no-dark-scheme`.

## Responsive

- Mobile first; test at 320, 375, 768, 1024, 1280 and 1440px wide. `[WCAG 1.4.10]` reflow at 320px.
- No horizontal page scroll at any width. Wide tables scroll inside their own container.
- Touch targets ≥ 44×44px on touch layouts (`[WCAG 2.5.5]`), never under 24px (`[WCAG 2.5.8]`).
- Navigation collapses to a disclosure menu built on `<button aria-expanded>`, not a hover-only menu.

## Resilience and privacy

- Content and links work without JavaScript; JS enhances.
- Respect `prefers-reduced-motion`, `prefers-color-scheme`, and `prefers-contrast` where cheap.
- Cookie banners: equal-weight "Accept" and "Reject", no pre-ticked boxes, never covering the main CTA or focus.
- Third-party scripts (chat, analytics, tag managers) load after interaction or idle, never in `<head>` blocking render.
