# AI slop: patterns to recognise and refuse

"AI slop" is the generic look of pages generated without design judgement: interchangeable, decorated rather than designed, and full of claims nobody can check. B2B buyers have learned to read these patterns as "template, unproven, not serious". Every page this skill produces must avoid them, and every audit must call them out.

The checker flags the ones it can detect in code (`slop-*` warnings). The rest are on you: walk this list before presenting any page.

## Visual tells

| Pattern | Why it reads as slop | Do instead | Checker |
|---|---|---|---|
| Purple-to-blue or indigo-to-pink gradient backgrounds | The default "AI startup" look; says nothing about the brand | One brand accent on a neutral ground; gradients only when the brand owns them | `slop-gradient` |
| Gradient-filled headline text | Decoration standing in for a message | Solid text; emphasise one phrase with the accent colour at most | `slop-gradient-text` |
| Default framework colours (Tailwind indigo-500 `#6366f1`, violet-500 `#8b5cf6`, purple-600 `#9333ea`) | Shows nobody chose a colour | Tokens from `tokens.py` with a deliberate accent | `slop-default-color` |
| Glassmorphism everywhere (blurred translucent cards, glowing blobs) | Hurts contrast and performance; generic | Solid surfaces; at most one translucent element (e.g. a sticky nav) | `slop-glass` |
| A 3×2 grid of identical icon cards (icon in rounded square, title, two lines) as the main feature section | The most recognised AI layout; nothing is prioritised | Bento with a lead tile, alternating rows with real UI, or a workflow narrative (`components.md`) | — (review) |
| Emoji used as icons in headings, buttons or feature cards (🚀 ✨ ⚡ 🔒) | Toy-like for a B2B buyer | A consistent icon set, or no icon | `slop-emoji` |
| Sparkle ✨ icons and "AI-powered" badges on everything | Noise; every product says it | Say what the AI does, once, where it matters | `slop-emoji`, copy review |
| Every section centred, same width, same rhythm | No hierarchy, no pacing | Mix centred statements with left-aligned split sections; vary density | — (review) |
| Large radius + heavy shadow on every element | Soft, undifferentiated surfaces | Radius and elevation from the style direction; flat by default | — (review) |
| Hover scale or bounce on everything | Distracting; slows scanning | Motion only where it explains state (`motion.md`) | `motion-long-hover` |
| Fake browser chrome or invented UI drawn around a placeholder | Looks like a mock, not a product | Real screenshots, or a clearly labelled placeholder | — (review) |
| Stock photos of smiling teams at laptops; AI-generated people | Read as fake instantly | Real product UI, real customers, real facilities | `slop-placeholder-media` (stock hosts) |
| Social icon rows for accounts that don't exist; icons in footers as decoration | Filler | Only real channels, as text links if few | — (review) |

## Content tells

| Pattern | Do instead | Checker |
|---|---|---|
| Buzzwords: revolutionize, supercharge, unlock, unleash, seamless, effortless, elevate, empower, leverage, cutting-edge, game-changer, next-generation, world-class, robust, synergy, "in today's fast-paced world", "take X to the next level" | Say what the product does, for whom, with a specific result | `slop-buzzwords` (3+ hits) |
| Unsourced round-number stats: "10x faster", "99.9% uptime", "10,000+ teams", "50% more revenue" | Real numbers from the client, with source or date; otherwise a labelled placeholder | `slop-unsourced-stat` |
| Fake testimonials: "John D., CEO", "Jane Doe", "Sarah K." with stock avatars | Real named quotes with role and company, or a placeholder | `slop-fake-person` |
| "Trusted by thousands of companies" with no names | Named logos or nothing | `slop-vague-proof` |
| Generic section titles: "Features", "Why choose us", "Our solutions", "What we offer" | A title that states the benefit ("Close the books in three days") | `slop-generic-heading` |
| Triplets of adjectives: "fast, secure, and scalable" | One concrete claim with evidence | — (review) |
| Lorem ipsum or "Your headline here" left in | Real copy or a clearly marked `[placeholder]` | `slop-lorem` |
| Every headline a question or every subhead starting "Whether you're…" | Vary; lead with the outcome | — (review) |

## Structural tells

- The same section order as every template: hero → 3 features → testimonials → pricing → CTA, regardless of the business. Use the blueprint for the sales motion instead.
- A pricing section on the homepage of a sales-led enterprise product, with invented prices.
- FAQ answers that repeat the question.
- Footer with 5 columns of links to pages that don't exist.

## How to use this in an audit

Report slop findings under their own heading, after accessibility errors and before style suggestions. For each: what it is, where, why it hurts trust, and the specific replacement.
