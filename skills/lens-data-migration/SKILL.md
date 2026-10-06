---
name: lens-data-migration
description: Data-migration lens for SDD consultants, independent of technology — changing schemas and transforming existing data safely: classifying the change, expand/migrate/contract across releases, compatibility with the previous release, avoiding long locks and downtime, batched and resumable backfills, dual writes and read switching, validation before and after, rollback and point-of-no-return analysis, rehearsal on production-sized data, and running the migration in production. Use when a feature changes a schema, moves data between stores, or transforms existing records.
---

# Lens: Data migration

Data outlives code. A bad deploy is rolled back in minutes; corrupted or lost data may never come back. This lens makes every data change **reversible until the last possible moment, and verified at every step**.

## 1. Classify the change

| Change | Risk | Typical approach |
|---|---|---|
| Additive (new table, new optional column, new index) | Low (watch for locks) | Single release, non-blocking creation |
| Rename or restructure | Medium | Expand → migrate → contract over several releases |
| Type or semantics change of existing data | High | New field, backfill with transformation, switch reads, retire old |
| Removal of data or structure | High (irreversible) | Only after a verified period of non-use; backup and explicit human acceptance |
| Moving data between stores or services | High | Dual write or change capture, reconciliation, cutover, fallback window |

## 2. Expand → migrate → contract

1. **Expand**: add the new structures without breaking the current version (nullable or defaulted, non-blocking creation). Deploy.
2. **Migrate**: write to both shapes (or derive one from the other), backfill existing data, then switch reads to the new shape. Each sub-step is a deploy, and each is compatible with the previous version.
3. **Contract**: once nothing reads or writes the old shape (verified by telemetry or code search) for an agreed period, remove it in a **later** release.

Every release must work with the data as the previous release left it. That is what keeps rollback possible.

## 3. Locks, downtime and load

- Know which operations take blocking locks in the chosen datastore, and how long they hold them at production volume.
- Prefer online or non-blocking variants of index and constraint creation, and add constraints in an unvalidated state and validate them separately where the store allows.
- Set timeouts on migration statements so a lock wait fails fast instead of queuing production traffic.
- Schedule heavy work for low-traffic windows only when online approaches don't exist.

## 4. Backfills

- Run outside the request path, in bounded batches, throttled to protect production load.
- **Idempotent and resumable**: record checkpoints, so a restart continues and never duplicates.
- Handle rows created or changed during the backfill (dual writes, or a final catch-up pass).
- Measure throughput on production-sized data, and estimate the total duration before starting.

## 5. Validation

Before, during and after:
- row counts and checksums or aggregates per partition;
- invariants checked by queries (no nulls where required, referential integrity, value ranges);
- sampled record-level comparisons between old and new shapes;
- a dry-run mode that reports what would change.

The migration fails loudly if validation fails. It never "mostly succeeds".

## 6. Rollback and the point of no return

For every step, write down the reverse operation and what happens to data written by the new version. Identify the **point of no return**, the step after which rollback means data repair rather than redeploy. Place it as late as possible and back it with a verified backup and an explicit human acceptance (D3).

## 7. Rehearsal and execution

- Rehearse on a copy of production-sized data. Record duration, lock waits, resource usage and validation results in the evidence pack.
- `release.md` lists the migration steps in order, the go/no-go checks, who watches what during execution, and the abort criteria.
- During execution: monitor locks, error rates, replication lag and backfill progress. Stop on abort criteria.

## Review checklist

- [ ] Change classified; multi-release plan for anything beyond additive
- [ ] Each step compatible with the previous release
- [ ] Lock and duration impact estimated at production volume; statement timeouts set
- [ ] Backfills batched, idempotent, resumable, throttled, catch-up handled
- [ ] Validation defined before, during and after
- [ ] Reverse steps written; point of no return identified, late, backed up, accepted
- [ ] Rehearsed on production-sized data; evidence recorded

Severity: risk of data loss or unrecoverable corruption → **critical**; a long blocking lock in production, or an irreversible step without acceptance → **major**.
