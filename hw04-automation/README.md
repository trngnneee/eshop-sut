# HW04 — Student 23127271

**Student ID:** 23127271  
**Features:** A FR-03 (done) · B FR-08 (done) · C FR-15 (later)  
**HW04 PDF:** Task 1 — data-driven Playwright, ≥12 cases/feature, ≥3 assertion patterns, 3 browsers, HTML `Run by: 23127271`

## Evidence isolation

| Guard | Detail |
| --- | --- |
| Feature A freeze | `evidence/feature-a-fr03-frozen-2026-08-07/` + `EVIDENCE-LOCK.json` |
| Verify A | `npm run evidence:verify-fr03` |
| Run B only | `npm run test:matrix:fr08` |

## Contents

| Path | Purpose |
| --- | --- |
| `tests/fr03-forgot-password.spec.js` | Feature A |
| `tests/fr08-checkout.spec.js` | Feature B |
| `test-data/fr03-forgot-password.json` | A data (14) |
| `test-data/fr08-checkout.json` | B data (14) |
| `reports/html/fr03-forgot-password/` | A reports (**frozen**) |
| `reports/html/fr08-checkout/` | B reports |
| `bug-reports/BUG-FR03-*` / `BUG-FR08-*` | Product defects |
| `docs/ai-conversion-log.md` | AI stages A+B |
| `docs/ai-audit-report.md` / `ai-critique.md` | HW04 §9–§10 (Feature A; extend for B next) |
| `docs/hw04-pdf-gap-checklist.md` | Full PDF compliance gaps |
| `git-commit-log.txt` | **Placeholder — real git history missing (§12)** |

## Self-assessment

| No. | Criteria | Grade | Self-Assessed |
| --- | --- | ---: | ---: |
| 1 | Task 1 — Feature A (FR-03) | 25 | 22 |
| 1 | Task 1 — Feature B (FR-08) | 25 | 22 |
| 1 | Task 1 — Feature C | 25 | not started |
| 2 | Task 2 — Demo video | 15 | TBD |
| 3 | Agent Skills | 10 | skill present |

## Test summary

| Metric | FR-03 (A) | FR-08 (B) |
| --- | ---: | ---: |
| Cases | 14 | 14 |
| Pass / fail per browser | 9 / 5 | 9 / 5 |
| HTML report cells | 3 | 3 |
| Bugs (Markdown) | 5 | 5 |

## How to run

```powershell
cd SoftwareTesting-HW\HW4\23127271
npm run evidence:verify-fr03
npm run test:matrix:fr08
```
