# External sync (outbox)

Anything that writes outside the repository — issue trackers, PR review comments, release notes, knowledge bases, design tools, messages — goes through an outbox and is performed **only after the human approves it**. Pushing `sdd/*` branches and creating/updating **draft** PRs are the only external writes that stay autonomous.

## Outbox

`.sdd/outbox.md` (hub-owned), one entry per pending external write:

```markdown
### OUT-07: Create Linear issue for F004
target: linear (team ENG)
action: create issue "Password reset" with link to specs/004-password-reset/brief.md
source: product-lead discover (F004)
status: pending        # pending | approved | done | rejected | failed
```

Entries are added by the hub when:
- `sync.issue_tracker` is set: create/update the issue for each feature at intake, and on phase changes; link tasks when Build starts.
- `sync.pr_review_comments: true`: after each code review, mirror blocking findings as PR review comments.
- `sync.release_notes: true`: after G3, publish the release notes from `release.md` / the changelog.
- `sync.knowledge` is set: after librarian `sync-bundle`, push `.sdd/knowledge/outbox/` to the configured knowledge base.
- An agent returns an escalation whose item is an external write (e.g. a Figma update, an announcement).

## Approval

At each stop (and on `/sdd sync`), if the outbox has pending entries: list them in one compact table and ask with AskUserQuestion — "Perform all", "Choose items" (follow-up question), "Skip for now". Never perform an entry the human didn't approve in this session.

## Performing

Use the connected tool for each target (GitHub via `gh` or the GitHub MCP, Linear/Jira/knowledge-base MCPs). Record `done` with the resulting URL or ID, or `failed` with the error. If a target's connector isn't available or isn't authorized, mark `failed` and tell the human which connector to connect.
