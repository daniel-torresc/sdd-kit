#!/usr/bin/env bash
# brain-bootstrap — Loads the canonical declarative-memory files from the
# sibling `second-brain/` repo into Claude Code context at session start.
# Shipped by the `brain-common` plugin. See README for design rationale.
#
# Resolution: brain location is `$BRAIN_PATH` if set, otherwise the
# sibling `../second-brain/` of this plugin (the architecture's
# sibling-repo layout).

set -uo pipefail

BRAIN="${BRAIN_PATH:-$(cd "${CLAUDE_PLUGIN_ROOT}/.." && pwd)/second-brain}"

if [ ! -d "$BRAIN" ]; then
  printf '[brain-bootstrap] brain not found at %s — set BRAIN_PATH or place brain-common/ next to second-brain/.\n' "$BRAIN" >&2
  exit 0
fi

emit() {
  local label="$1" path="$2"
  if [ -f "$path" ]; then
    printf '\n===== BRAIN: %s =====\n' "$label"
    cat "$path"
  fi
}

cat <<'EOF'
# Second Brain — session bootstrap

You have been loaded with the canonical declarative-memory files for
Daniel's second brain. The brain is the **sole persistent memory store**
— do not write to Claude Code per-project memory (`~/.claude/projects/.../memory/`)
or any parallel cache. Anything worth remembering across sessions goes
in the brain per the contract in CLAUDE.md / meta/SCHEMA.md below.

Write protocol (synchronous, context-rich, write-through):
pull → read → merge → stamp provenance → atomic write → commit + push.
Step 6 is non-negotiable.
EOF

emit "CLAUDE.md (orientation + write protocol)" "$BRAIN/CLAUDE.md"
emit "meta/SCHEMA.md (frontmatter + path contract)" "$BRAIN/meta/SCHEMA.md"
emit "self/identity/current.md (who Daniel is)" "$BRAIN/self/identity/current.md"
emit "self/preferences.md (how Daniel works)" "$BRAIN/self/preferences.md"

YEAR=$(date +%Y); MONTH=$(date +%m); TODAY=$(date +%Y-%m-%d)
emit "episodic/daily/$YEAR/$MONTH/$TODAY.md (today's daily)" \
  "$BRAIN/episodic/daily/$YEAR/$MONTH/$TODAY.md"
