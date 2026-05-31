#!/usr/bin/env bash
# brain-bootstrap — Loads the stable identity layer of Daniel's brain
# into Claude Code context at session start. Part of brain-common.
#
# What loads (intentionally small, cache-friendly):
#   - CLAUDE.md             — brain orientation + write protocol
#   - self/identity/current.md  — who Daniel is
#   - self/preferences/INDEX.md — behavioral defaults (digest)
#
# What does NOT load (Read on demand):
#   - meta/SCHEMA.md           — only needed when writing; CLAUDE.md
#                                already directs agents there
#   - self/preferences/<topic>.md — detail files; INDEX has the digest
#   - episodic/daily/YYYY/MM/YYYY-MM-DD.md — only when continuing
#                                today's work; grows unboundedly
#
# Resolution: brain location is $BRAIN_PATH if set, otherwise the
# sibling `../second-brain/` of this plugin (sibling-repo layout).

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

You've been loaded with the stable identity layer of Daniel's brain.
The brain is the **sole persistent memory store** — do not write to
Claude Code per-project memory or any parallel cache. The write
protocol (synchronous, context-rich, write-through: pull → read →
merge → stamp → atomic write → commit + push) is in CLAUDE.md below;
step 6 is non-negotiable.

Read on demand (not pre-loaded to save tokens):
  - `meta/SCHEMA.md` — when about to write to the brain
  - `self/preferences/<topic>.md` — when a specific preference detail matters
  - `episodic/daily/YYYY/MM/YYYY-MM-DD.md` — when continuing today's work
EOF

emit "CLAUDE.md (orientation + write protocol)" "$BRAIN/CLAUDE.md"
emit "self/identity/current.md (who Daniel is)" "$BRAIN/self/identity/current.md"
emit "self/preferences/INDEX.md (behavioral defaults)" "$BRAIN/self/preferences/INDEX.md"
