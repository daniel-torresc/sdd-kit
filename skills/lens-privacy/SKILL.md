---
name: lens-privacy
description: Privacy and data-protection lens for SDD consultants, independent of technology — for features that collect, store, process or share personal data: data inventory and flows, purpose and lawful basis (flagged for the human), data minimization, retention and deletion, data-subject rights (access, correction, erasure, portability, objection), consent and transparency, processors and transfers, privacy by design and default, privacy impact assessment triggers, and privacy-safe logging, analytics and testing. Use whenever personal data is involved. Legal interpretation is always the human's decision.
---

# Lens: Privacy and data protection

Security protects data from people who shouldn't have it. Privacy limits **what we collect, why, for how long, and what people can control**. This lens applies privacy by design. It does not give legal advice: interpretations of law (lawful basis, regulated categories, cross-border transfers) are flagged for the human as D3.

## 1. Data inventory and flows

For the feature, list every personal data element: what it is, where it comes from, where it is stored, who and what accesses it, where it is sent (processors, third parties, model providers, analytics), and how long it is kept. Draw the flow in the design. **Special categories** (health, biometrics, beliefs, orientation, etc.), children's data and precise location are flagged immediately.

## 2. Purpose and lawful basis

Each element has a stated **purpose** tied to a requirement. The **lawful basis** (consent, contract, legal obligation, legitimate interest, …) is proposed with reasoning and confirmed by the human (D3). Data collected "in case it's useful" has no purpose and must not be collected.

## 3. Minimization and defaults

- Collect only what the purpose needs. Prefer derived or aggregated values over raw data, and pseudonymous identifiers over direct ones.
- The most privacy-protective settings are the **default**. Optional sharing is opt-in.
- Restrict access internally to those who need it, and log administrative access.

## 4. Retention and deletion

Every element has a retention period and a deletion mechanism that reaches all copies: primary stores, replicas, backups (on their rotation), caches, logs, analytics and processors. Anonymization must be real, not just removing names. Deletion is tested.

## 5. Data-subject rights

Design how the system supports access, correction, erasure, portability and objection or withdrawal of consent: who can request, how identity is verified, which data is in scope across stores, and the response time. Requirements and acceptance criteria cover the flows the product must offer.

## 6. Transparency and consent

What users are told (notices at the point of collection), and when consent is needed: granular, informed, as easy to withdraw as to give, and recorded with what was agreed and when. Copy is specified in `ux.md`.

## 7. Processors and transfers

Every third party receiving personal data is listed with its purpose, the data it gets, its location and the agreement in place. Transfers outside the required region or jurisdiction are flagged (D3). This includes model providers, analytics, error tracking and email services.

## 8. Privacy-safe engineering

- No personal data in logs, metrics labels, traces, error messages or URLs. Use opaque identifiers.
- Analytics are aggregated or pseudonymous, and respect consent.
- Test, staging and development use synthetic or properly anonymized data, never production copies of personal data.
- Exports and backups are encrypted and access-controlled.

## 9. Impact assessment

Trigger a privacy impact assessment (decision package for the human) when the feature involves special categories, large-scale processing, systematic monitoring, profiling with significant effects, new technologies applied to personal data, or transfers to new jurisdictions.

## Review checklist

- [ ] Data inventory and flow documented; special categories flagged
- [ ] Purpose per element; lawful basis proposed and sent to the human
- [ ] Minimization and protective defaults applied
- [ ] Retention and deletion defined and reaching all copies, tested
- [ ] Data-subject rights supported where required
- [ ] Notices and consent specified (with ux-designer)
- [ ] Processors and transfers listed; cross-border transfers flagged
- [ ] No personal data in logs, telemetry, URLs or non-production environments
- [ ] Impact assessment triggered where required

Severity: personal data exposed, retained without purpose, or sent to an undisclosed third party → **critical**; missing deletion path, data-subject right unsupported, or personal data in logs → **major**.
