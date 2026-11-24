# Motion

B2B motion is fast and restrained: it confirms actions, explains changes of state, and adds a little life to marketing pages. Timings below were measured on 8 live B2B sites (`live_site_notes.md`) and match the IBM Carbon and Material 3 motion systems.

## Timing table

| Interaction | Duration | Easing token | Evidence |
|---|---|---|---|
| Button / link hover and press | 100–150ms | `--ease-out` | Linear 0.1s (276 elements), Flexport 0.15s (535), Carbon fast-02 110ms |
| Card hover lift, tab switch, accordion | 200–250ms | `--ease-standard` | Ramp 0.2s, Stripe 0.25s, Carbon moderate-02 240ms |
| Dropdown / mega menu | 150–250ms open, faster close | `--ease-out` | Live sites 0.15–0.3s |
| Modal / drawer | 200–300ms in, 150–200ms out | `--ease-out` in, `--ease-in` out | Carbon, M3 |
| Scroll reveal (fade + 8–16px rise) | 400–600ms, stagger 60–80ms | `--ease-expressive` | Stripe 0.6–1s, Linear 0.4–0.7s |
| Hero entrance (once) | 600–800ms | `--ease-expressive` | Stripe |
| Number counter (once, when in view) | 800–1200ms | `--ease-out` | Optional |
| Logo marquee | 30–90s per loop | linear | Linear 30s, Salesforce 85s (Ramp 180s) |
| Skeleton shimmer | 1.2–1.6s loop | linear | Rippling 1.6s |

Tokens from `tokens.py`:

```css
--dur-instant: 100ms; --dur-fast: 150ms; --dur-base: 220ms; --dur-slow: 400ms; --dur-reveal: 600ms;
--ease-out: cubic-bezier(0, 0, 0.38, 0.9);
--ease-in: cubic-bezier(0.2, 0, 1, 0.9);
--ease-standard: cubic-bezier(0.2, 0, 0.38, 0.9);
--ease-expressive: cubic-bezier(0.16, 1, 0.3, 1);
```

The first three curves follow Carbon's productive set **[verify]**. `--ease-expressive` is the strong ease-out Stripe uses for reveals.

## Productive vs expressive

- **App UI (productive):** the fast end of every range. No scroll reveals, no entrances. Motion only for feedback and state.
- **Marketing (expressive):** reveals, a hero entrance and ambient loops are allowed, each used sparingly.

## Rules

1. **Reduced motion is required.** Wrap movement in `@media (prefers-reduced-motion: no-preference)`, or remove it under `reduce`. Under reduce, use instant changes or opacity-only fades ≤ 150ms. `[WCAG 2.3.3]` Checker: `motion-reduced`.
2. **Anything moving on its own for more than 5 seconds needs a pause control** (marquee, carousel, auto-advancing tabs, background video). Pausing on hover alone isn't enough for keyboard and touch users. Add a pause button, or pause on `:focus-within` too. `[WCAG 2.2.2]` Checker: `motion-pause`.
3. **Animate only `transform` and `opacity`** (plus `filter` sparingly). Never `width`, `height`, `top` or `margin`: they cause layout work and jank. `[WEBDEV]`
4. **Direct feedback stays under 300ms.** Checker: `motion-long-hover` warns on transitions over 300ms on buttons and links.
5. **No decorative motion on text:** no parallax headlines, no letter-by-letter typing effects, no infinite bounces.
6. **Reveal once.** Scroll reveals trigger once (IntersectionObserver with `unobserve`), never re-animate on scroll back up.
7. **Content is visible without JS.** Start reveal states with a `.js` class on `<html>` so content isn't hidden if scripts fail.

## Patterns

**Scroll reveal (CSS + tiny JS):**
```css
@media (prefers-reduced-motion: no-preference) {
  .js [data-reveal] { opacity: 0; transform: translateY(12px);
    transition: opacity var(--dur-reveal) var(--ease-expressive), transform var(--dur-reveal) var(--ease-expressive); }
  .js [data-reveal].is-in { opacity: 1; transform: none; }
}
```
```js
document.documentElement.classList.add('js');
const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -10% 0px' });
document.querySelectorAll('[data-reveal]').forEach(el => io.observe(el));
```

**Marquee with pause:** duplicate the track, animate `translateX(-50%)` linearly, set `animation-play-state: paused` on `:hover` and `:focus-within`, add a visible pause button, and show a static wrapped row under reduced motion.

**Progressive enhancement:** `animation-timeline: view()` for scroll-linked effects and the View Transitions API for page and state changes, both inside `@supports` and the reduced-motion query.
