---
name: digest-sources
description: >-
  Digest and synthesize MULTIPLE sources about ONE topic into a single
  semantic note in the knowledge vault (`semantic/<domain>/<topic>.md`),
  creating it or merging into it without ever blind-appending. Handles web
  URLs, local files (PDF/markdown/txt), pasted text, and video/YouTube
  transcripts. Use when the user says things like "digest these sources",
  "update my notes on X", "research X and save it to my brain", "synthesize
  these articles", "consolidate what I've read about X", or hands over a pile
  of links/files on a shared subject and wants durable, deduped, cited
  knowledge. This is the synthesizer agent's primary procedure; it can also be
  invoked directly in a normal session.
---
Read all the raw files in the "$1" directory from my second brain's semantic memory and build me a structured wiki organized by concept — not by source or by person.

For each major concept, write a standalone article that:

- Explains what the concept is in plain language
- Summarizes what the evidence says
- Notes where these experts agree
- Specifically flags where they disagree and why
- Links to related articles

Also update the INDEX file that lists every article in the wiki with a one-line description.

Write everything so any user can understand it.

## Guardrails

- **No source, no claim.** Every assertion in the note traces to `## Sources`.
  Can't source it → it goes to Open questions or doesn't go in.
- **One topic per note.** Resist scope creep; spin a sibling note and
  cross-link instead.
- **Merge, never blind-append.** Re-running on the same topic must converge,
  not bloat.
- **Provenance is non-negotiable.** `author: agent:synthesizer`, dated, sourced,
  confidence-rated — always.
- **Abstract, topic-neutral voice.** The note body is standalone reference
  knowledge *about the subject* — written in neutral third person, the way an
  encyclopedia entry reads. Do not name the owner, do not write in first
  person ("I", "my", the user's name), and do not editorialize about the note's
  memory type or its place in any memory system (no "this semantic note…", "as
  declarative memory…", "in the brain…"). The `title:` and headings name the
  *topic*, never a relationship to it ("Retrieval-Augmented Generation", not
  "Notes on RAG"). All the "what kind of memory / whose it is" information
  lives silently in frontmatter and the `## Sources` ledger — never in prose.