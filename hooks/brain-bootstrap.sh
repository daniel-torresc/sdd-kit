#!/usr/bin/env bash
# brain-bootstrap — Loads the stable identity layer of Daniel's brain
# into Claude Code context at session start. Part of brain-common.
#
# What loads (intentionally small, cache-friendly):
#   - CLAUDE.md                    — brain orientation + write protocol
#   - self/identity/current.md     — who Daniel is
#   - self/preferences/INDEX.md    — behavioral defaults (digest)
#
# What does NOT load (Read on demand):
#   - meta/SCHEMA.md           — only when writing; CLAUDE.md directs there
#   - self/preferences/<topic>.md — detail files; INDEX has the digest
#   - episodic/daily/YYYY/MM/YYYY-MM-DD.md — only when continuing today's work
#
# Brain resolution (first match wins):
#   1. $BRAIN_PATH                                    — explicit override
#   2. $CLAUDE_PROJECT_DIR/second-brain               — cwd is brain's parent
#   3. $CLAUDE_PROJECT_DIR                            — cwd IS the brain
#   4. $HOME/Library/CloudStorage/OneDrive-Personal/Personal/Second Brain/second-brain
#                                                     — Daniel's known location
#   5. $CLAUDE_PLUGIN_ROOT/../second-brain            — dev sibling layout
#
# Each candidate must contain CLAUDE.md to qualify (cheap sanity check).

set -uo pipefail

is_brain() { [ -f "$1/CLAUDE.md" ] && [ -d "$1/self" ] && [ -d "$1/episodic" ]; }

BRAIN=""
TRIED=()
for candidate in \
  "${BRAIN_PATH:-}" \
  "${CLAUDE_PROJECT_DIR:-}/second-brain" \
  "${CLAUDE_PROJECT_DIR:-}" \
  "${HOME}/Library/CloudStorage/OneDrive-Personal/Personal/Second Brain/second-brain" \
  "${CLAUDE_PLUGIN_ROOT:-}/../second-brain"; do
  [ -z "$candidate" ] && continue
  candidate_abs="$(cd "$candidate" 2>/dev/null && pwd)" || { TRIED+=("$candidate (not a dir)"); continue; }
  if is_brain "$candidate_abs"; then
    BRAIN="$candidate_abs"
    break
  fi
  TRIED+=("$candidate_abs (no CLAUDE.md)")
done

if [ -z "$BRAIN" ]; then
  echo "[brain-bootstrap] could not locate the brain. Tried:"
  for t in "${TRIED[@]}"; do echo "  - $t"; done
  echo "Set BRAIN_PATH to the absolute path of your second-brain/ to override."
  exit 0
fi

emit() {
  local label="$1" path="$2"
  if [ -f "$path" ]; then
    printf '\n===== BRAIN: %s =====\n' "$label"
    cat "$path"
  fi
}

cat <<EOF
===== brain-bootstrap v0.1.2 — resolved brain at: $BRAIN =====

# Second Brain — session bootstrap

You've been loaded with the stable identity layer of Daniel's brain.
The brain is the **sole persistent memory store** — do not write to
Claude Code per-project memory or any parallel cache. The write
protocol (synchronous, context-rich, write-through: pull → read →
merge → stamp → atomic write → commit + push) is in CLAUDE.md below;
step 6 is non-negotiable.

Read on demand (not pre-loaded to save tokens):
  - \`meta/SCHEMA.md\` — when about to write to the brain
  - \`self/preferences/<topic>.md\` — when a specific preference detail matters
  - \`episodic/daily/YYYY/MM/YYYY-MM-DD.md\` — when continuing today's work
EOF

emit "CLAUDE.md (orientation + write protocol)" "$BRAIN/CLAUDE.md"
emit "self/identity/current.md (who Daniel is)" "$BRAIN/self/identity/current.md"
emit "self/preferences/INDEX.md (behavioral defaults)" "$BRAIN/self/preferences/INDEX.md"
