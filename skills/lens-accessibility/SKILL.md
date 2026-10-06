---
name: lens-accessibility
description: Accessibility lens for SDD consultants — WCAG 2.2 AA requirements for features with a user interface, reviewing requirements and ux.md for accessible flows, reviewing implementations (semantics, keyboard, focus, contrast, labels, errors, motion, target size), and verifying with automated (axe) and manual (keyboard-only, screen reader) checks. Use when the a11y lens is active.
---

# Lens: Accessibility (WCAG 2.2 AA)

## Specify / UX
- Every UI REQ has accessibility ACs where behavior matters: keyboard operability, focus after actions, error identification in text, status messages announced.
- `ux.md` specifies: heading structure, landmarks, labels, focus order, contrast pairs, target sizes (≥ 24×24 px), reduced motion, no color-only meaning.

## Design / Plan
- Component library chosen supports accessibility (ARIA patterns, keyboard support); tasks include axe checks and a keyboard-only e2e path per journey.

## Review (implementation)
| Check | How |
|---|---|
| Semantics | Native elements first; ARIA only to fill gaps; correct roles/names/states |
| Keyboard | Every action reachable and operable; no traps; visible focus; logical order |
| Forms | Labels associated; errors in text, linked to fields, announced |
| Contrast | Text 4.5:1 (large 3:1); UI components and focus indicators 3:1 |
| Media/motion | Alternatives for images; captions; `prefers-reduced-motion` respected |
| Dynamic content | Live regions for async status; focus management for dialogs and route changes |

## Verify
axe (Playwright) on every screen and state; keyboard-only run of each journey; a screen-reader spot check of critical flows (VoiceOver/NVDA) noted in the evidence pack.

Severity: blocking a journey for keyboard or screen-reader users → **critical**; failing a AA criterion on a primary screen → **major**.
