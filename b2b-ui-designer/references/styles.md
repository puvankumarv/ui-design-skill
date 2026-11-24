# Style directions

Five directions observed in the survey. Pick one; generate its tokens with `scripts/tokens.py <direction>`. A client brand guide overrides colours and fonts but keeps the direction's structure (radius, elevation, density, motion).

| Direction | When | Seen on (structure only) |
|---|---|---|
| `enterprise` | Large suites, logistics, manufacturing, HR, public sector, security pages | Salesforce, Datadog, Flexport |
| `modern-saas` | Most SaaS: collaboration, marketing, sales and support tools | Arrows, Ramp, Brevo, Campaign Monitor |
| `fintech-trust` | Payments, banking, spend, compliance, insurance | Brex, Sardine, Public, Wise |
| `developer` | APIs, infrastructure, dev tools, data platforms, AI tooling | Unkey, Novu, Linear, Vercel |
| `editorial` | Consulting, analytics, research, agencies, premium services | Hex, Forest Admin, Mailchimp |

## What each direction sets

| Token group | `enterprise` | `modern-saas` | `fintech-trust` | `developer` | `editorial` |
|---|---|---|---|---|---|
| Default mode | Light | Light | Light (warm off-white) | **Dark** | Light |
| Accent (default) | Blue `#0b5cad` | Blue `#2563eb` | Orange `#e8590c` | Lime `#a3e635` | Deep green `#1f6f50` |
| Display font | Inter | Inter | Inter (heavy) | Geist | Newsreader (serif) |
| Body font | Inter | Inter | Inter | Geist | Inter |
| Mono | IBM Plex Mono | JetBrains Mono | JetBrains Mono | Geist Mono | IBM Plex Mono |
| Radius | 4 / 6 / 8px | 8 / 12 / 16px | 6 / 10 / 14px | 6 / 8 / 12px | 0 / 2 / 4px |
| Elevation | Borders, almost no shadow | Soft layered shadows | Light shadows | Borders + glow | None (rules) |
| Density | High | Medium | Medium | Medium-high | Low (airy) |
| Section padding | 80px | 112px | 112px | 96px | 128px |
| Imagery | Real operations photos, product UI | Product UI everywhere | Product UI, product photography, live widgets | Code, diagrams, product UI | Editorial photography, charts |
| Motion | Minimal | Moderate | Minimal-moderate | Moderate, glows | Minimal |

Default accents were chosen to pass contrast in their mode. When the user gives a brand accent, `tokens.py --accent` keeps the hue and adjusts lightness until white or black text on it reaches 4.5:1, and makes a separate `--accent-text` for links on the page background.

## Choosing when it's unclear

- Who signs the contract? Enterprise procurement → `enterprise`; a developer with a credit card → `developer`; a finance lead → `fintech-trust`.
- What do competitors look like? Differentiate within the direction (accent, type, imagery), not by abandoning it. A logistics site that looks like a crypto launch loses trust.
- Dark mode by default only for `developer`. 8 of the 11 dark sites in the survey were dev or AI tools; fintech and enterprise stayed light.

## Colour rules for every direction

- One accent. A second colour only for data visualisation and status.
- Status colours (success, warning, danger, info) are separate from the accent and always come with an icon or text.
- Neutrals carry 90% of the page: background, surface, border, text, muted text.
- Accent placement: primary buttons, links, one highlighted headline phrase, focus ring, small UI marks. Never body text or large backgrounds (except a single `cta-band`).
