# Finding and using references

References keep a design current and specific to its brief. They inform **structure, hierarchy, density and quality**. They never supply brand, copy, imagery or a distinctive visual signature.

## 1. Inspo MCP (when connected)

An archive of real production sites with screenshots, palettes, fonts, a fold-by-fold breakdown, page flows and 68 reference component archetypes. Budget per page: one `recommend`, one or two `search_screens`, then `get_screen` on the 3–5 you keep.

| Need | Call |
|---|---|
| Start from a brief | `recommend(brief, pageType, vibe, mode)` |
| Browse a segment | `search_screens(query, industry="saas"\|"fintech"\|"developer-tools"\|"ai", pageType="landing"\|"pricing"\|"features")` |
| A specific component on real sites | `find_components(type="pricing"\|"hero"\|"logo-cloud"\|"testimonial"\|..., industry)` |
| Starter code for an archetype | `find_reference_components(type)` → `get_reference_jsx(type, id)` |
| How a company sequences pages | `get_site_pages(siteSlug)` |
| A site's real tokens | `get_design_system(slug)` |

Useful filters for B2B: `vibe: "serious" | "technical" | "calm"`, `paperBand: "light"` (enterprise, fintech) or `"dark"` (developer).

**Known gaps:** few traditional enterprise or industrial sites, and no app UI. Use the live-site method and `pages/app-screens.md` for those.

## 2. Live sites (browser)

For the client's competitors and anything the archive lacks, open the site and record:
1. Section order (headings top to bottom)
2. CTA labels and how many times each appears
3. Proof types (logos, metrics, quotes, badges)
4. Motion: what moves, roughly how fast
5. Nav model (inline, mega) and footer

The `../b2b-ui-research/live_site_notes.md` file shows the method and the script used.

## 3. User-supplied references

Sites they like, competitors, screenshots, a brand guide. Ask what they like about each one: layout, tone, colour, density, a specific component. Copy the quality, not the look.

## 4. Turning references into decisions

For each kept reference, write one line: "From [site]: [structural idea] → used in [section]". Show this to the user with the page plan.

## Never

- Copy a company's name, logo, wordmark, copy, illustrations, photography, or a signature visual (e.g. a specific gradient mesh, mascot or hero effect).
- Recreate a competitor's page and rename it.
- Use a reference's demo content (names, numbers, quotes) as placeholder content.
