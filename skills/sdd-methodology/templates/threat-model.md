---
artifact: threat-model
feature: F000
owner: security-engineer
status: draft
version: 1
upstream: [design.md@1]
---

# Threat model: <feature name>

## Verification target
<!-- OWASP ASVS level for the touched areas (L1 for M without personal data; L2 for L or personal/financial/health data). -->

## Assets
<!-- What an attacker wants. Classification: public | internal | personal | sensitive. -->
| Asset | Classification | Where it lives | Retention |
|---|---|---|---|

## Trust boundaries and entry points
<!-- Every external IF-nn must appear here. -->

## Threats (STRIDE)

### THR-01: <threat>
refs: IF-01
category: spoofing | tampering | repudiation | information-disclosure | denial-of-service | elevation-of-privilege
likelihood: low|medium|high  ·  impact: low|medium|high
mitigation: <control>  ·  verified-by: <test / review / tool>

## Residual risks
