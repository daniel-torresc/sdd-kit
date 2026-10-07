# External sync

Anything that writes outside the repository — issue trackers, PR review comments, release notes, design tools, messages — is performed **only after the human approves it**. Pushing `sdd/*` branches and creating or updating **draft** PRs are the only external writes that stay autonomous.

## Pending external writes

Each pending write is an entry under **Waiting for the human** in the feature's `decisions.md` (project-level writes go in `specs/000-foundation/decisions.md`), written by the hub:

```markdown
### H-07: Create Linear issue for F004
type: external-write
prepared-by: hub (from product-lead specify)
status: pending                     # pending | approved | rejected | done | failed
target: linear (team ENG)
action: create issue "Password reset" linking specs/004-password-reset/brief.md
```

The hub adds an entry when:
- `sync.issue_tracker` is set: create or update the feature's issue at intake and on phase changes; link tasks when Build starts.
- `sync.pr_review_comments: true`: after each code review, mirror blocking findings as PR review comments.
- `sync.release_notes: true`: after G3, publish the release notes from `release.md` and the changelog.
- An agent returns an escalation whose item is an external write (a design-tool update, an announcement).

## Approval

At each stop (and on `/sdd sync`), if there are pending external-write entries: list them in one compact table and ask with AskUserQuestion — "Perform all", "Choose items" (follow-up question), "Skip for now". Never perform an entry the human didn't approve in this session.

## Performing

Use the connected tool for each target (GitHub via `gh` or the GitHub MCP; issue-tracker MCPs). Set `status: done` with the resulting URL or ID, or `failed` with the error, and commit (`chore(sdd): record external writes`). If a target's connector isn't available or authorized, mark `failed` and tell the human which connector to connect.
