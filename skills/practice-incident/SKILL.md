---
name: practice-incident
description: Incident response practice for SDD — declaring and classifying incidents (SEV1–SEV4), assessing user impact and blast radius from observability data, choosing the fastest safe mitigation (rollback, feature flag off, scale, failover) and handing it to the human for execution, keeping a timestamped timeline, communication updates, root-cause and contributing-factor analysis, blameless postmortems, and routing action items back into the SDD workflow (bug fixes, requirement, design, test, reliability and alerting changes). Use when something is wrong in a deployed environment.
---

# Practice: Incident response

## 1. Declare and classify

| Severity | Definition | Response |
|---|---|---|
| SEV1 | Critical journey down or data loss/exposure for many users; security breach | Immediate; mitigation first; human notified at once |
| SEV2 | Major degradation (SLO fast-burn), a critical journey impaired for a subset | Immediate mitigation; human notified |
| SEV3 | Minor degradation, workaround exists | Fix through a normal S/M feature |
| SEV4 | Cosmetic or internal-only | Backlog |

Open `.sdd/incidents/INC-nnn-<slug>/incident.md` immediately; record every observation and action with a UTC timestamp.

## 2. Assess

From dashboards, alerts, logs, traces and recent changes (deploys, flag changes, config, dependency updates, traffic): **what** users experience, **how many**, **since when**, **which** journeys/SLOs, and the **most recent change** that correlates. Do not start deep root-causing before impact is understood and mitigation chosen.

## 3. Mitigate first

Pick the fastest **safe, reversible** action that stops user harm:
1. Roll back the last release (platform-engineer's documented rollback).
2. Turn off the feature flag.
3. Scale out / restart unhealthy instances (if saturation).
4. Fail over or disable a non-critical dependency (degradation mode).
Production actions are executed by the human (or approved by them in the protected workflow) — your job is to recommend the action, its expected effect, its risk, and how to verify it worked, as a fast-path decision package. Confirm recovery against the SLI before standing down.

## 4. Communicate

Short updates at a regular cadence (SEV1: every 30 min) in the incident file: status, impact, actions taken, next update time. External/customer communication is a human action.

## 5. Investigate

After mitigation: reconstruct the timeline; identify the trigger, the **root cause(s)** and **contributing factors** (detection gaps, missing tests, unclear runbooks, design weaknesses, process gaps); use causal analysis (5 whys per factor, not one chain); cite evidence (logs, commits, dashboards). If reproduction is needed, request a failing test from engineer (`debug`).

## 6. Postmortem (blameless)

`postmortem.md` from the template for SEV1–SEV2 (and SEV3 if instructive): summary, impact (users, duration, SLO budget burned), timeline, root causes and contributing factors, what went well, what went poorly, where we got lucky, action items. Focus on systems and conditions, never individuals.

## 7. Action items into the workflow

Each action item has an owner agent, priority and a link:
- code defect → new class T/S feature (`/sdd new`) with a regression test;
- missing or wrong requirement → change request to product-lead;
- design weakness → architect (ADR or debt);
- detection gap (alert, SLO, dashboard) → reliability-engineer / platform-engineer;
- test gap → test-engineer;
- runbook gap → platform-engineer;
- lesson → librarian (`.sdd/knowledge/lessons.md`).
Track them in the postmortem until done.
