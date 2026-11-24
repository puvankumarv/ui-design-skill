# Demo request and contact pages

**Master decision:** how short the form is, and what happens right after submit.

## Layout

Split, form on the right (desktop) and first on mobile:
- **Left:** headline ("See [Product] in 30 minutes"), 3 bullets on what the call covers, a short logo row, one quote.
- **Right:** the form in a card.

Rippling offers both a live and an on-demand demo; Salesforce offers recorded demos. Offer a recorded option when you have one.

## Form rules

| Rule | Source |
|---|---|
| 4–5 fields: name, work email, company, company size (select), optional message. Enrich the rest later | `[NNG]` form length; common B2B practice `[std]` |
| Single column, labels above fields | `[BAY]` `[GOVUK]` |
| Never placeholder-only labels | `[BAY]` `[WCAG 3.3.2]` |
| Mark optional fields "(optional)", required ones visibly | `[BAY]` |
| Validate when the user leaves a field; error text below the field says how to fix it | `[BAY]` `[GOVUK]` |
| `autocomplete` attributes (name, email, organization) | `[WCAG 1.3.5]` |
| Button label is a verb phrase: "Book my demo", never "Submit" | `[GOVUK]` `[NNG]` |
| Under the button: what happens next and the response time | `[std]` |
| Privacy line with a link, no pre-ticked marketing checkbox | GDPR |

## After submit

Best: an inline calendar to book the slot immediately. Otherwise, a confirmation screen with the response time, what to prepare, and links to a recorded demo and case studies. Never a bare "Thank you".
