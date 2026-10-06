---
name: practice-ux
description: How to reason about and decide user experience in SDD — building understanding from evidence, framing the user's goal and context, generating and evaluating alternatives against usability principles and cognitive load, making explicit UX decisions with trade-offs, then specifying flows, information architecture, every screen state, interaction, UX writing, accessibility (WCAG 2.2 AA, owned here), design systems, low-fidelity prototypes, and reviewing built UIs. Use when designing or reviewing any user-facing experience.
---

# Practice: UX design

Good UX comes from **decisions**, not decoration: what the user is trying to do, what gets in their way, which design best removes that friction, and why. This skill is first a way of reasoning, then a way of specifying.

## 1. Understand: evidence before opinions

Build the picture from:
- personas (`.sdd/product/personas.md`);
- the brief's jobs and pains;
- whatever evidence the human provides (interviews, analytics, support tickets, recordings).

For each primary job, write down:
- **Goal**: what the user is trying to get done, in their words.
- **Context**: device, environment, frequency, time pressure, expertise, interruptions, emotional state (anxious? in a hurry?).
- **Current behavior and pain**: what they do today and where it breaks.
- **Success**: what tells them they're done.

Mark every unsupported belief as `ASM-nn`. If real research would change the design materially, write a **research plan** (question, participants, method, the decision it informs) for the human to run. Never invent research results.

## 2. Frame the design problem

Before drawing anything, state:
- **the design question** ("How might a locked-out customer regain access in under a minute without contacting support?");
- **constraints**: requirements, platform conventions, accessibility, technical limits, brand;
- **what must be true for this to work** (the riskiest assumption);
- **what is out of scope.**

## 3. Generate alternatives

Sketch at least two genuinely different approaches for anything non-trivial. They should differ in structure (one page vs a wizard, inline vs modal, automatic vs explicit), not just in styling. Look at established patterns users already know: the platform's conventions, and how comparable products solve the problem. Novelty in interaction is a cost users pay.

## 4. Evaluate with principles

Judge each alternative against:

| Lens | Questions |
|---|---|
| Goal fit | Does it get the user to success with the fewest decisions and steps? |
| Cognitive load | How much must they remember, read or decide at once? Recognition beats recall; progressive disclosure beats everything at once. |
| Feedback and status | Does the user always know what happened, what is happening, and what to do next? |
| Error prevention and recovery | Are mistakes hard to make, easy to notice, and cheap to undo? |
| Consistency | Does it match the platform and the design system, so knowledge transfers? |
| Control and freedom | Can the user back out, cancel, undo? Is anything irreversible clearly flagged? |
| Accessibility | Can it be used by keyboard, screen reader, low vision, motor impairment, or under cognitive strain? (§9) |
| Edge reality | Does it survive empty data, huge data, slow networks, interruptions, mistakes? |
| Cost | What does it cost to build and to maintain, relative to the user value? |

Where the evidence is thin, choose the option that is **cheapest to reverse** and make it measurable.

## 5. Decide and record

Record each significant UX decision in `ux.md`:
- the decision;
- the alternatives considered;
- why this one won (which principles and evidence);
- what it costs or gives up;
- how we'll know if it's wrong (a metric, a test, a support signal).

Decisions that imply expensive architecture go to the architect. Decisions that add capability go to product-lead.

## 6. Specify flows and structure

- **Flows**: one `UX-nn` per flow, mapped to REQs (`refs:`). Include entry points, steps, decisions, and exits for success and every failure the ACs define, drawn as a diagram in the markdown. Flows never add capabilities the requirements lack (file a finding to product-lead instead).
- **Information architecture**: the navigation model, grouping, labels taken from the glossary, and where each primary action lives.

## 7. Every state is a design

For each screen, specify its purpose, primary action, content hierarchy, and **every state**:

| State | Must define |
|---|---|
| Empty | First use; what to do next |
| Loading | What is shown, when, and what happens on timeout |
| Partial | Some data failed or is still loading |
| Error | The message, the cause in user terms, the recovery action |
| Success | Confirmation and next step |
| Permission denied | Why, and what the user can do about it |
| Offline / slow | Behavior, retries, what is preserved |

Specify responsive behavior per breakpoint; design mobile-first when the context is mobile.

## 8. Words are interface

- Use plain language, the user's vocabulary (the glossary) and the active voice.
- Error messages say **what happened and what to do next**, never blame, and never expose internals.
- Keep the tone consistent with the design system.
- List every user-facing string in `ux.md` with a key, for translation.

## 9. Accessibility (owned here)

Accessibility is a design requirement, specified in `ux.md`, turned into ACs with product-lead, verified by test-engineer and checked in code review. Target: **WCAG 2.2 AA**.

| Area | Specify |
|---|---|
| Structure | Headings, landmarks, lists, reading order |
| Operability | Every action reachable and usable by keyboard; no traps; visible, logical focus; focus management on navigation and dialogs |
| Perception | Contrast ≥ 4.5:1 (3:1 for large text and UI parts); no information by color alone; text alternatives; captions |
| Input | A label for every control; errors identified in text and linked to their fields; status messages announced |
| Motion and time | Respect reduced-motion preferences; no time limits without extension |
| Targets | At least 24×24 px |

When accessibility would block a journey for assistive-technology users, that is **critical**.

## 10. Design system

`.sdd/product/design-system.md`:
- **principles**;
- **tokens**: color with contrast pairs, typography, spacing, radii, elevation, motion;
- **components**: purpose, variants, states, accessibility notes;
- **patterns**: forms, tables, empty states, notifications, dialogs, navigation;
- **voice and tone**.

Prefer adopting an accessible component library that fits the chosen frontend technology over inventing one. Every new screen uses the system, and any deviation is a recorded decision.

## 11. Prototypes

When a flow is complex or contested, build a **low-fidelity static prototype** in `specs/<f>/prototypes/`: no build step, no real data. It exists to make the decision concrete for the human and the engineers. It never ships.

## 12. Reviewing built UI

Against the running app or the evidence pack:
- each flow end to end;
- every state reachable and specified;
- copy as specified;
- the decisions from §5 honored;
- accessibility per §9 (keyboard-only run, automated check results, contrast);
- responsive behavior.

Findings go to the task's engineer, or to product-lead if the spec itself is wrong.
