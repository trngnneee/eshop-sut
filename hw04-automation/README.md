# HW04 — Student 23127271

**Student ID:** 23127271  
**Features:** A FR-03 (done) · B FR-08 (done) · C FR-15 (done — 6 pass / 8 fail × 3 browsers)  
**HW04 PDF:** Task 1 — data-driven Playwright, ≥12 cases/feature, ≥3 assertion patterns, 3 browsers, HTML `Run by: 23127271`  
**Main report:** `docs/hw04-main-report.md` (+ PDF)  
**GitHub:** https://github.com/trngnneee/eshop-sut/tree/HW4-Tram (`hw04-automation/`)

## Demo / Agent Skill links

| Item | Link | Status |
| --- | --- | --- |
| Agent Skill demo (FR-15 end-to-end) | https://youtu.be/Te25xh0biYI | Done |
| Task 2 demo video (≥5 min, multi-browser + report + AI fix) | https://youtu.be/p5TRjyrvPvg | Done |
| Skill file | `.cursor/skills/automation-testing/playwright-skill.md` | Present |

## Evidence isolation

| Guard | Detail |
| --- | --- |
| Feature A freeze | `evidence/feature-a-fr03-frozen-2026-08-07/` + `EVIDENCE-LOCK.json` |
| Verify A | `npm run evidence:verify-fr03` |
| Run B only | `npm run test:matrix:fr08` |
| Run C only | `npm run test:matrix:fr15` |

## Contents

| Path | Purpose |
| --- | --- |
| `tests/fr03-forgot-password.spec.js` | Feature A |
| `tests/fr08-checkout.spec.js` | Feature B |
| `tests/fr15-admin-product.spec.js` | Feature C |
| `test-data/fr03-forgot-password.json` | A data (14) |
| `test-data/fr08-checkout.json` | B data (14) |
| `test-data/fr15-admin-product.json` | C data (14) |
| `pages/AdminProductPage.js` | C page object |
| `reports/html/fr03-forgot-password/` | A reports (**frozen**) |
| `reports/html/fr08-checkout/` | B reports |
| `reports/html/fr15-admin-product/` | C reports (3 browsers) |
| `bug-reports/BUG-FR03-*` / `BUG-FR08-*` / `BUG-FR15-*` | Product defects |
| `docs/ai-conversion-log.md` | AI stages A+B+C |
| `docs/ai-audit-report.md` / `.pdf` | HW04 §9 (A+B+C) |
| `docs/ai-critique.md` / `.pdf` | HW04 §10 |
| `docs/hw04-main-report.md` / `.pdf` | Consolidated report |
| `docs/hw04-pdf-gap-checklist.md` | Compliance checklist |
| `git-commit-log.txt` | Counting `.spec.js` history (§12) |

## Self-assessment

| No. | Criteria | Grade | Self-Assessed |
| --- | --- | ---: | ---: |
| 1 | Task 1 — Feature A (FR-03) | 25 | 22 |
| 1 | Task 1 — Feature B (FR-08) | 25 | 22 |
| 1 | Task 1 — Feature C (FR-15) | 25 | 22 |
| 2 | Task 2 — Demo video | 15 | 15 ([YouTube](https://youtu.be/p5TRjyrvPvg)) |
| 3 | Agent Skills | 10 | skill + [YouTube demo](https://youtu.be/Te25xh0biYI) |

## Test summary

| Metric | FR-03 (A) | FR-08 (B) | FR-15 (C) |
| --- | ---: | ---: | ---: |
| Cases | 14 | 14 | 14 |
| Pass / fail per browser | 9 / 5 | 9 / 5 | 6 / 8 |
| HTML report cells | 3 | 3 | 3 |
| Bugs (Markdown) | 5 | 5 | 8 |

## How to run

```powershell
cd SoftwareTesting-HW\HW4\23127271
npm run evidence:verify-fr03
npm run test:matrix:fr08
npm run test:matrix:fr15
```
