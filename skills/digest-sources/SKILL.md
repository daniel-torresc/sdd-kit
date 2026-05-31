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

# digest-sources

Turn N sources on one topic into **one** living semantic note. The output is
not a summary dump — it is a *merged, deduped, contradiction-resolved,
provenance-stamped* topic note that gets a little more complete and a little
more trustworthy each time you run it.

This skill writes to the **brain** (`second-brain/`), a separate git repo
from this kit. It is bound by the brain's write contract in
[[CLAUDE.md]] and [[meta/SCHEMA]] — read both before your first write of a
session if you have not already.

## Mental model

A semantic note is a **claim ledger**, not an essay. Each run:

1. extracts atomic claims from each source, tagged with which source said it,
2. reconciles them against what the note already holds,
3. raises confidence where independent sources corroborate, lowers it where a
   claim stands alone or sources disagree,
4. rewrites the prose so a human reads synthesis, while the `## Sources`
   section preserves the audit trail.

Append-and-pray is the failure mode. Merge-with-context is the job.

## Resolve the brain path first

The brain may not be the working directory. Resolve it once, in this order,
and use an absolute path for every read/write/git call:

1. `$BRAIN_PATH` if set.
2. `/Users/danieltorres/Library/CloudStorage/OneDrive-Personal/Personal/Second Brain/second-brain`
   (canonical vault location).

Sanity-check the chosen path contains `CLAUDE.md` and `meta/SCHEMA.md` before
trusting it. Call this resolved path `$BRAIN` below.

## Procedure

### 1. Scope the topic → compute the path

- **Topic** = the single subject these sources share. If the sources actually
  span two topics, say so and digest the dominant one (or ask which).
- **Domain** = the top-level `semantic/` folder: `ai`, `engineering`,
  `finance`, `health`, `productivity`, … Reuse an existing domain folder if
  one fits; only coin a new domain when nothing fits.
- **Path** = `$BRAIN/semantic/<domain>/<topic-slug>.md`. Slug is lower-kebab,
  ASCII-only, stopwords stripped (per [[meta/SCHEMA]]).

State the resolved path before writing so a wrong placement is catchable.

### 2. Pull, then read the canonical target

```bash
git -C "$BRAIN" pull --ff-only
```

Read the target note if it exists. If it does, you are **updating** — hold its
existing claims, confidence, and `## Sources` in mind for step 4. If it does
not, you are **creating** from the semantic template
(`meta/templates/semantic.md`) plus the `## Sources` extension below.

### 3. Ingest each source → atomic claims

Classify and pull each source, then extract its claims (short, checkable
statements), each tagged with its origin:

| Source type   | How to ingest |
|---------------|---------------|
| **Web URL**   | `WebFetch` the URL. If a link is vague or dead, `WebSearch` to locate the canonical source. Record the access date. |
| **Local file**| `Read` it. PDFs: read by page range (`pages:`), large files in slices. md/txt: read directly. |
| **Pasted text** | Use the text already in the conversation; record it as `paste:<short-label>`. |
| **Video / YouTube** | Get the transcript, in order of preference: (a) if `yt-dlp` is installed, `yt-dlp --skip-download --write-auto-sub --sub-lang en --sub-format vtt -o "$TMPDIR/yt.%(ext)s" "<url>"` then read the `.vtt` and strip timestamps/cue numbers; (b) else `WebFetch` a transcript page if one exists; (c) else tell the user `yt-dlp` is missing (`brew install yt-dlp`) and ask them to paste the transcript. Never invent transcript content. |

For each source capture: a stable identifier (`url:…` / `file:…` /
`paste:…` / `video:…`), the access/publish date if known, and a one-line note
on its credibility (primary vs secondary, official vs blog, recency).

If a source can't be retrieved, **say so explicitly** and digest the rest —
never silently drop it.

### 4. Synthesize and merge — the core

Reconcile the new claims with the existing note:

- **Dedupe.** Collapse claims that say the same thing. One source repeating
  itself is not corroboration.
- **Corroborate.** A claim asserted by ≥2 independent credible sources →
  `high` confidence. Single credible source → `medium`. Weak/old/inferred →
  `low`. Reflect this in the per-claim phrasing and in the note's aggregate
  frontmatter `confidence`.
- **Resolve contradictions.** If sources disagree, do not pick silently.
  Either (a) state both positions inline with their sources and a short note on
  which is better-supported, or (b) if the note already held a claim that a new,
  more credible source overturns, supersede it and add a one-line `> note:`
  recording the change. Contradictions left unresolved go in **Open questions**.
- **Write synthesis, not a digest.** The reader should get a coherent picture,
  not "Source A said…, Source B said…". Attribution lives in `## Sources` and,
  where a specific claim is contested or load-bearing, an inline `[S1]`-style
  marker keyed to the Sources list.

### 5. Compose the note

Use this shape (semantic template + a `## Sources` ledger, since frontmatter
`source:` is single-valued and these notes are multi-source):

```markdown
---
type: semantic
title: "<Topic>"
created: <YYYY-MM-DD>        # immutable; keep original on update
updated: <YYYY-MM-DD>        # today
author: agent:synthesizer
source: "multi-source"        # the ledger lives in ## Sources below
confidence: <high|medium|low> # aggregate across the note
sensitive: false              # true if the topic is personal/private
scope: <universal|domain|personal>
tags: [<topic-tags>]
related: ["semantic/<domain>/<other>.md", ...]
---

# <Topic>
<!-- Body voice: neutral third-person reference knowledge about the topic.
     No owner name, no first person, no meta-commentary about memory type or
     "the brain". Reads like an encyclopedia entry, not a personal note. -->

## Summary
<!-- 2–5 sentences: the synthesized state of knowledge. The one thing to read. -->

## Details
<!-- The merged claim ledger as readable prose/bullets. Inline [S1] markers on
     contested or pivotal claims. -->

## Open questions
<!-- Unresolved contradictions, gaps, things no source settled. -->

## Sources
<!-- The audit trail. One line per source, stable id + date + credibility note. -->
- [S1] url:https://…  · accessed <YYYY-MM-DD> · <primary/secondary, note>
- [S2] file:/path/to.pdf · <note>
- [S3] video:https://youtu.be/… · transcript · <note>

## See also
<!-- [[semantic/<domain>/<related>]] wikilinks. Link liberally. -->
```

On **update**: preserve `created:`, append new sources to `## Sources` (don't
duplicate ones already listed), bump `updated:` to today, recompute aggregate
`confidence`, and keep `author: agent:synthesizer`.

If you are genuinely unsure about a merge (e.g. a contradiction you can't
adjudicate), set `needs_review: true` and lower `confidence` rather than
canonizing a guess — live but visibly provisional, per the contract.

### 6. Write atomically

Write to a temp file in the same directory and `mv` it over the target (temp +
rename) so a reader never sees a half-written note. Create the domain folder
if new.

### 7. Update the INDEX

- New domain → add a one-line entry under **Domains** in
  `$BRAIN/semantic/INDEX.md` (and create a domain `INDEX.md` if the domain is
  growing past a handful of notes).
- New topic in an existing domain → ensure it's discoverable from the domain's
  index if one exists. Don't hand-edit `meta/indexes/` (those are generated).

### 8. Log the episode

Append a block to today's daily note
`$BRAIN/episodic/daily/YYYY/MM/YYYY-MM-DD.md` (create the file from
`meta/templates/daily.md` if absent):

```markdown
## HH:MM — Digested <topic> from N sources
- <one line on what changed: created / merged X new claims / resolved Y contradiction>.
- Touches [[semantic/<domain>/<topic>]].
_— agent:synthesizer · confidence: <…>_
```

### 9. Commit + push — never skip

```bash
git -C "$BRAIN" add -A
git -C "$BRAIN" commit -m "semantic(<domain>): digest <topic> from N sources"
git -C "$BRAIN" push
```

If the commit hook or push fails: fix the underlying cause and make a **new**
commit. Do not `--amend`, do not `--no-verify`. Uncommitted brain changes are
lost work waiting to happen.

## Return value

End with a tight report (this is what the calling session sees):

- Path written and create-vs-update.
- N sources ingested, and any that failed and why.
- Aggregate confidence, plus anything flagged `needs_review`.
- Open questions worth a human's attention.

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
