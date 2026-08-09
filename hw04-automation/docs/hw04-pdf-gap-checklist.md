# HW04 PDF compliance checklist — current package

**Student:** 23127271 · **Date:** 2026-08-09  
**Source:** `2026.HW04.Automation Testing_En.pdf` §5–§15  
**Package:** `SoftwareTesting-HW/HW4/23127271/`

Legend: **Met** · **Partial** · **Missing**

---

## Task 1 — Automation scripts

| Requirement | Status | Notes |
| --- | --- | --- |
| 3 features (Pools A/B/C = HW02 FR-03, FR-08, FR-15) | **Partial** | A + B done; **Feature C (FR-15) missing** |
| ≥12 cases per feature | **Met** (A,B) | A: 14 · B: 14 · C: 0 |
| Step-by-step AI (not one prompt) | **Met** (A,B) | `docs/ai-conversion-log.md` |
| External JSON/CSV data-driven | **Met** (A,B) | `test-data/fr03-*.json`, `fr08-*.json` |
| ≥3 assertion patterns | **Met** (A,B) | visibility, text, URL, attribute/count, plain/API |
| 3 browsers × each feature | **Partial** | A×3 + B×3 = **6** cells; need **9** with C |
| HTML report `Run by: StudentID` + ISO timestamp | **Met** (A,B) | stamped title/header/meta |
| Human review of AI mistakes | **Partial** | In conversion log / FR-03 audit; B not fully folded into audit |
| Bug reports for failing oracles | **Partial** | Markdown BUG-FR03/FR08 present; **GitHub Issues + screenshots not filed** |
| Document non-automated cases | **Partial** | Noted in FR-03 gap file; FR-08 thinner |

## Task 2 — Demo video (§6)

| Requirement | Status |
| --- | --- |
| Unlisted YouTube ≥5 min, Vietnamese narration | **Missing** |
| Show multi-browser run + HTML report | **Missing** |
| Narrate ≥1 AI-script fix | **Missing** |
| Face-cam **or** `whoami` + `hostname` | **Missing** |
| Link in README | **Missing** |

## Agent Skill (§7)

| Requirement | Status |
| --- | --- |
| Skill submitted | **Partial** — `.cursor/skills/automation-testing/playwright-skill.md` exists locally |
| Skill demo YouTube (end-to-end on one feature) | **Missing** |

## AI documents (§9–§10)

| Requirement | Status |
| --- | --- |
| AI Audit Report (tool, datetime, prompt, output per interaction) | **Partial** — Feature A written; **needs Feature B (+ C) rows** |
| AI Critique 200–300 words | **Partial** — Feature A only; should mention B lessons (SPA cart, etc.) |
| Markdown **+ PDF** of audit/critique | **Missing PDF** exports |

## Anti-cheat (§11)

| Requirement | Status |
| --- | --- |
| Real HTML reports with StudentID + ISO timestamp | **Met** for A+B (do not regenerate fake timestamps) |
| Real demo video authorship | **Missing** (video not shot) |

## Git commit log (§12) — you are right, this is missing

| Requirement | Status |
| --- | --- |
| Public GitHub repository | **Missing** |
| ≥ **8** commits that change `.spec.js` / `.spec.ts` (or equivalent) | **Missing** |
| Spread over ≥ **4 different days** | **Missing** |
| `git-commit-log.txt` (or similar text file) in submission | **Missing** |
| Local `.git` under `23127271/` or parent | **None found** |

**Important:** Only commits that touch test-script files count. README-only commits do **not** count toward the 8.

### Suggested commit plan (do this yourself over ≥4 calendar days)

Do **not** backdate or squash into one day if the TA checks timestamps.

| Day | Example `.spec` change (counts) |
| --- | --- |
| Day 1 | Add/scaffold `fr03-forgot-password.spec.js` |
| Day 1–2 | Expand FR-03 cases / fix dialog handling in `.spec.js` |
| Day 2 | Add `fr08-checkout.spec.js` skeleton |
| Day 2–3 | Fix SPA cart navigation in FR-08 `.spec.js` |
| Day 3 | Assert total-readonly / orderTotalEquals in FR-08 `.spec.js` |
| Day 3–4 | Add `fr15-admin-product.spec.js` skeleton |
| Day 4 | Expand FR-15 to ≥12 + matrix greps |
| Day 4+ | Repair flaky waits / locators in any `.spec.js` |

Then:

```powershell
cd SoftwareTesting-HW\HW4\23127271   # after git init + remote
git log --oneline --follow -- tests/*.spec.js > git-commit-log.txt
# or fuller:
git log --date=iso --name-only -- tests/ > git-commit-log.txt
```

Push to a **public** GitHub repo and put the URL in the main report / README.

## Submission zip (§14)

| Required zip content | Status |
| --- | --- |
| Main report Markdown + PDF (automation + AI gap review) | **Missing** consolidated report/PDF |
| Public GitHub link | **Missing** |
| Multi-browser HTML reports | **Partial** (6/9 cells) |
| YouTube demo link | **Missing** |
| AI Critique + AI Audit (MD + PDF) | **Partial** (MD A only; no PDF) |
| Git commit log text file | **Missing** |
| Bug reports + GitHub Issues w/ screenshots | **Partial** (local MD only) |
| README self-assess + test summary + demo link | **Partial** (no demo link; C missing) |
| Filename `23127271_HW04_AI_Automation_XXX.zip` | Not packed yet |

## Assessment scoreboard (honest)

| No. | Criteria | Max | Current readiness |
| --- | ---: | ---: | --- |
| 1 | Feature A | 25 | Strong (~22) |
| 1 | Feature B | 25 | Strong (~22) |
| 1 | Feature C | 25 | **0 — not started** |
| 2 | Demo video | 15 | **0** |
| 3 | Agent Skills | 10 | Partial (~5–7) until skill demo video |
| | **Total** | **100** | **~49–51** until C + video + git + Issues |

---

## Priority order to close gaps

1. **Init public GitHub repo** and start `.spec.js` commits across **≥4 days** (cannot compress legally for §12).
2. **Feature C — FR-15** (≥12 cases × 3 browsers × labeled HTML).
3. **File GitHub Issues** for BUG-FR03/FR08 with screenshots.
4. **Demo video** (Task 2) + skill demo video (§7).
5. Refresh **AI Audit / Critique** for B (+ C) and export **PDFs**.
6. Write **main report** MD+PDF + `git-commit-log.txt` + pack zip.
