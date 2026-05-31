# brain-common

The domain-agnostic substrate for Daniel's [second brain][brain]. A
Claude Code plugin providing lifecycle hooks, shared skills, and
infrastructure agents — read by every `brain-<domain>` plugin as
they're built.

[brain]: ../second-brain/

## Why this exists

Per the [founding architecture][arch], the second-brain system splits
along one seam:

- **Brain** (`second-brain/`) — *nouns*, declarative memory: self,
  episodic, semantic + entity hubs. Sole persistent memory store.
- **Kit** (`brain-common/` + future `brain-<domain>/`) — *verbs*,
  procedural memory: skills, agents, hooks, MCPs. Shareable plugins.

`brain-common` is the kit's domain-agnostic substrate. Every domain
plugin depends on `brain-common`; `brain-common` depends on no domain.

[arch]: ../docs/second-brain-architecture.md

## Current capabilities (v0.1.0)

**SessionStart bootstrap hook** (`hooks/brain-bootstrap.sh`) — loads
the canonical declarative-memory files into Claude Code context at
session start:

- `CLAUDE.md` — brain orientation + write protocol
- `meta/SCHEMA.md` — frontmatter + path contract
- `self/identity/current.md` — who Daniel is
- `self/preferences.md` — how Daniel works
- Today's daily note (if present)

This replaces the per-harness Claude Code memory system. Per the
founding decision [the brain is the sole memory store][sole-mem], all
persistent context lives in the brain and is loaded on demand by this
hook.

[sole-mem]: ../second-brain/self/decisions/2026-05-31-brain-is-sole-memory.md

## Layout (Anthropic plugin convention)

```
brain-common/
├── .claude-plugin/
│   └── plugin.json          # manifest
├── hooks/
│   ├── hooks.json           # hook declarations
│   └── brain-bootstrap.sh   # SessionStart bootstrap
├── skills/                  # future: brain-write, brain-navigation, capture, memory-consolidation
├── agents/                  # future: librarian, diarist, optional router
├── .mcp.json                # future: shared MCPs (Todoist, Gmail, Calendar)
└── README.md
```

## Install

### Dev mode (single session, this machine)

```bash
claude --plugin-dir "/Users/danieltorres/Library/CloudStorage/OneDrive-Personal/Personal/Second Brain/brain-common"
```

### Permanent local install (recommended once stable)

Symlink the plugin into Claude Code's user plugins directory so it
auto-loads in every session:

```bash
ln -s "/Users/danieltorres/Library/CloudStorage/OneDrive-Personal/Personal/Second Brain/brain-common" ~/.claude/plugins/brain-common
```

Or via `/plugin install` once a marketplace catalog (`brain-marketplace/`)
exists — see [architecture §6][arch-kit] for the marketplace design.

[arch-kit]: ../docs/second-brain-architecture.md

## Dependencies

- Sibling brain at `../second-brain/` (override with `$BRAIN_PATH`).
- Bash 4+ on the host machine.

## Conventions

- Hooks bundled here use `${CLAUDE_PLUGIN_ROOT}` to resolve their own
  paths — never assume the working directory.
- Future skills invoke as `common:<skill>` (Claude Code namespaces
  plugin skills by plugin name).
- One-way dependency: every domain plugin may depend on `brain-common`;
  `brain-common` depends on no domain. Shared need → promote to common.

## Versioning

Semver. v0.x = pre-stable; expect breaking changes. v1.0.0 will lock
the hook contract and the eventual `skills/` interface.
