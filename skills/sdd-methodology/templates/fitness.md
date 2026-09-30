---
artifact: fitness
owner: architect
status: draft
version: 1
upstream: []
---

# Fitness functions

<!-- Architecture rules enforced automatically in CI. The architect defines them; platform-engineer wires them. -->

### FF-01: <rule>
protects: <ADR / NFR / module boundary>
check: <tool and configuration, e.g. import-linter contract "modules-only-through-api">
runs: <on every PR | nightly>
status: proposed        # proposed | wired | retired
