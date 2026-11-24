# Security and trust page

**Master decision:** which certifications and documents to put first. This page is read by IT, security and procurement reviewers late in the deal, and it often decides whether the deal closes.

## Section order

1. `hero`: plain statement ("How we protect your data") + certification badges
2. `compliance`: one card per certification or regulation (SOC 2 Type II, ISO 27001, GDPR, HIPAA, PCI DSS), each with status and date
3. `data-protection`: encryption at rest and in transit, data residency, retention, deletion
4. `infrastructure`: hosting provider, regions, availability, backups, disaster recovery
5. `access`: SSO / SAML, SCIM, role-based permissions, audit logs, 2FA
6. `privacy`: subprocessors list, DPA, privacy policy
7. `documents`: request the SOC 2 report, pen-test summary, security questionnaire (CAIQ / SIG)
8. `contact`: security team email, responsible disclosure / bug bounty
9. Status page link

## Rules

- Write in plain language with specifics: "AES-256 at rest, TLS 1.2+ in transit", not "bank-grade security".
- Every badge matches a certification the client actually holds, with its scope and date. **Never add a badge as decoration.**
- Calm visual style: the `enterprise` or `fintech-trust` direction, no playful motion.
- Documents behind a short request form are fine. The list of what exists stays public.
