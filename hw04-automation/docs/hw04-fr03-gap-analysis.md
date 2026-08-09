# HW04 PDF gap analysis — Feature A (FR-03)

**Student:** 23127271 · **Date:** 2026-08-09  
**Sources:** `2026.HW04.Automation Testing_En.pdf` §5–§14 · current package `HW4/23127271/`

## 1. Feature A Task 1 checklist (FR-03 only)

| HW04 requirement | Status | Evidence / note |
| --- | --- | --- |
| Same HW02 Feature A (Pool A FR-03) | Met | HW02 Feature A = FR-03 web |
| ≥12 automated cases (pos/neg/edge mix) | Met | 14 cases in `test-data/fr03-forgot-password.json` |
| Step-by-step AI (not one generic prompt) | Met | `docs/ai-conversion-log.md` stages 1–7 |
| Data-driven external `.json` / `.csv` | Met | External JSON; loader validates ≥12, IDs, assertion vocab |
| ≥3 distinct assertion patterns | Met | Visibility, text, attribute, URL, plain value |
| Run on 3 browsers (Chromium/Firefox/WebKit) | Met | `playwright.config.js` + `npm run test:matrix` |
| Each run → HTML report with `Run by: StudentID` | Met | 3 reports; title/header/meta + ISO timestamp |
| Human review of AI scripts + what AI got wrong | Met (strengthened) | Conversion log §7 + this gap file + AI Audit |
| Bug report when assertion reveals defect | Partial → fixed in docs | Notes existed; formal Markdown bugs added under `bug-reports/` |
| Log bugs on GitHub Issues + screenshot | **Gap (process)** | Local screenshots in `test-results/`; GitHub Issues not filed yet |
| Document cases not automated | Met below | See §2 coverage gaps |

## 2. FR-03 functional coverage gaps (vs README / HW02)

Automated suite covers happy path, empty/invalid/unregistered email, wrong/empty/short OTP, weak password (length + missing uppercase), and five spec UI oracles.

| Gap ID | Spec / HW02 rule | Automated? | Why / impact |
| --- | --- | --- | --- |
| G-01 | Confirm password **mismatch** (FR-03) | No | SUT has no confirm field; 010 asserts field presence only. Mismatch journey blocked until UI exists. |
| G-02 | Password missing digit / lowercase / special (`@$!…`) | Partial | 008–009 cover length + uppercase. Other FR-01 classes left for later expansion. |
| G-03 | OTP valid only for the requested email (cross-email) | No | Needs two accounts + token reuse; deferred (API/UI isolation heavier). |
| G-04 | OTP reuse after successful reset (SUP from HW02) | No | State/API supplementary; not required for ≥12 minimum. |
| G-05 | Server accepts weak password if client bypassed | No | Would need API-only or request interception; document as non-UI. |

None of G-01–G-05 drop Feature A below the HW04 ≥12 floor; they are quality/coverage improvements.

## 3. Full HW04 package gaps (outside Feature A slice)

These are **not** FR-03 script defects; they block a complete Moodle zip later:

| Item | PDF § | Status for current folder |
| --- | --- | --- |
| Feature B (≥12 + 3 browser reports) | Task 1 | Missing (HW02 FR-08 planned) |
| Feature C (≥12 + 3 browser reports) | Task 1 | Missing (HW02 FR-15 planned) |
| 9 HTML report cells | Task 1 | Only 3 (FR-03 × 3 browsers) |
| Demo video ≥5 min VN + whoami/hostname | Task 2 | Missing |
| Agent Skill demo video | §7 | Skill exists under `.cursor/skills/automation-testing/`; demo link TBD |
| AI Audit Report appendix | §9 | **Added** `docs/ai-audit-report.md` |
| AI Critique 200–300 words | §10 | **Added** `docs/ai-critique.md` |
| Git commit log ≥8 commits / ≥4 days on `.spec` | §12 | Missing in this folder |
| Public GitHub repo link | §14 | TBD |
| Main report Markdown + PDF | §14 | Feature A docs only so far |
| README self-assess + demo link | §14 | Partial (no demo link yet) |

## 4. Verdict for Feature A

**Task 1 — Feature A (FR-03): implementation + matrix evidence are submission-ready for the A slice**, with remaining process gaps: file GitHub Issues for BUG-FR03-001…005, and expand B/C for the full 100-point package.

**Self-assess Feature A:** 22 / 25 (deduct for GitHub issue filing + a few domain cases not yet automated).
