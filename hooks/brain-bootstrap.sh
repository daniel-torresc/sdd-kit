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
# Brain resolution: BRAIN_PATH only.
#   The brain lives in a different place on each machine (personal, work,
#   …), so its location is configured per-machine via the BRAIN_PATH
#   environment variable — the absolute path to your second-brain/ dir.
#   Set it in ~/.claude/settings.json ("env": { "BRAIN_PATH": "…" }) or
#   export it from your shell profile. If BRAIN_PATH is unset or does not
#   point at a valid brain, this hook prints a warning and loads nothing.

set -uo pipefail

is_brain() { [ -f "$1/CLAUDE.md" ] && [ -d "$1/self" ] && [ -d "$1/episodic" ]; }

warn() {
  cat <<'WARN'
===== brain-bootstrap — brain NOT loaded =====

⚠️  BRAIN_PATH is not set (or does not point at a valid brain), so your
second brain was not loaded into this session.

Set it to the absolute path of your second-brain/ directory — either:

  • ~/.claude/settings.json  (applies to every session on this machine):
        "env": { "BRAIN_PATH": "/absolute/path/to/second-brain" }

  • or your shell profile (~/.zshrc):
        export BRAIN_PATH="/absolute/path/to/second-brain"

Then start a new Claude Code session.
WARN
}

if [ -z "${BRAIN_PATH:-}" ]; then
  warn
  exit 0
fi

BRAIN="$(cd "${BRAIN_PATH}" 2>/dev/null && pwd)" || BRAIN=""
if [ -z "$BRAIN" ] || ! is_brain "$BRAIN"; then
  echo "[brain-bootstrap] BRAIN_PATH=\"${BRAIN_PATH}\" is not a valid brain"
  echo "  (expected a directory containing CLAUDE.md, self/ and episodic/)."
  warn
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
===== brain-bootstrap v0.3.0 — resolved brain at: $BRAIN =====

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
