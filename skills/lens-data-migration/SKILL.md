---
name: lens-data-migration
description: Data-migration lens for SDD consultants — schema changes and backfills done safely: expand/migrate/contract, backward compatibility with the previous release, locking and long-running migrations on large tables, batched backfills with checkpoints, data validation before and after, rollback paths, and production-volume rehearsal. Use when a feature changes a schema or transforms existing data.
---

# Lens: Data migration

## Design
- **Expand → migrate → contract** across releases: add new structures (nullable / defaults), dual-write or backfill, switch reads, remove old structures in a later release. Every step backward compatible with the previous app version so rollback works.
- **Locking**: avoid long exclusive locks — add columns without volatile defaults, create indexes concurrently, add constraints as `NOT VALID` then validate separately (PostgreSQL).
- **Backfills**: batched (bounded batch size), idempotent, resumable with checkpoints, throttled, run outside the request path; measure throughput on production-like volume.
- **Validation**: counts and checksums before/after; invariants checked by queries; a dry-run mode.
- **Rollback**: for each step, the reverse operation and its data implications (rows written by the new version).

## Plan
Migration steps are separate tasks, sequenced (one migration head at a time), each with up/down tests and a rehearsal task on a copy of production-sized data.

## Review
Locks taken, runtime estimate on real volume, idempotency, reversibility, compatibility with N−1 app version, monitoring during the run.

## Verify / Release
Rehearsal evidence (duration, lock waits, validation results) in the evidence pack; `release.md` lists migration order and the go/no-go checks.

Severity: data loss or unrecoverable corruption risk → **critical**; long table lock in production or non-reversible step without acceptance → **major**.
