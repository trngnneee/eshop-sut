# HW04 Main Report — Automation Testing

**Student:** Vo Ngoc Bich Tram · **ID:** 23127271 · **Class:** 23KTPM3  
**Course:** CS423 / CSC13003 – Software Testing  
**Date:** 2026-08-10  
**Package:** `SoftwareTesting-HW/HW4/23127271/` · GitHub: `trngnneee/eshop-sut` branch `HW4-Tram`

---

## 1. Scope

| Pool | Feature | Spec cases | Spec file | Data file |
| --- | --- | ---: | --- | --- |
| A | FR-03 Forgot Password (Web) | 14 | `tests/fr03-forgot-password.spec.js` | `test-data/fr03-forgot-password.json` |
| B | FR-08 Checkout | 14 | `tests/fr08-checkout.spec.js` | `test-data/fr08-checkout.json` |
| C | FR-15 Product CRUD (Admin) | 14 | `tests/fr15-admin-product.spec.js` | `test-data/fr15-admin-product.json` |

HW04 Task 1 requirements addressed: data-driven Playwright, ≥12 cases/feature, ≥3 assertion patterns, Chromium/Firefox/WebKit, HTML reports labeled `Run by: 23127271`.

---

## 2. AI collaboration (step-by-step)

Each feature followed: **Analyze → Design → Review → Model data → Map → Generate → Verify**.

Evidence:

- Stage log: `docs/ai-conversion-log.md`
- Prompt appendix: `docs/prompt_log.md`
- AI Audit (A+B+C): `docs/ai-audit-report.md` (+ PDF)
- AI Critique (200–300 words): `docs/ai-critique.md` (+ PDF)

Human review kept **spec oracles** when the SUT was defective (OTP length, checkout auth/total, product validation / FR-12).

---

## 3. Assertion patterns (≥3)

| Pattern | Example API | Used in |
| --- | --- | --- |
| Visibility / hidden | `toBeVisible` / `toBeHidden` | FR-03, FR-08, FR-15 |
| Text / accessible name | `toHaveText` / `toContainText` | FR-03, FR-08, FR-15 |
| URL / navigation | `toHaveURL` | FR-03, FR-08 |
| Value / attribute / count | `toHaveValue` / `toHaveAttribute` / `toHaveCount` | FR-03, FR-08 |
| Plain / API status | `expect(status).toBe(...)` ranges | FR-08 totals, FR-15 API |

---

## 4. Multi-browser execution summary

| Feature | Chromium | Firefox | WebKit | HTML path |
| --- | --- | --- | --- | --- |
| FR-03 | 9 pass / 5 fail | 9 / 5 | 9 / 5 | `reports/html/fr03-forgot-password/<browser>/` |
| FR-08 | 9 / 5 | 9 / 5 | 9 / 5 | `reports/html/fr08-checkout/<browser>/` |
| FR-15 | 6 / 8 | 6 / 8 | 6 / 8 | `reports/html/fr15-admin-product/<browser>/` |

All nine cells stamp **`Run by: 23127271`** (title + header). Manifest: `reports/run-manifest.json`.  
Feature A reports are **frozen** (`EVIDENCE-LOCK.json` + `evidence/feature-a-fr03-frozen-2026-08-07/`).

Failing cases are **product defects**, not softened oracles. See `bug-reports/`.

---

## 5. Bug reports

| Feature | Local Markdown | Count |
| --- | --- | --- |
| FR-03 | `bug-reports/BUG-FR03-001` … `005` | 5 |
| FR-08 | `bug-reports/BUG-FR08-001` … `005` | 5 |
| FR-15 | `bug-reports/BUG-FR15-001` … `008` | 8 |

GitHub Issues filed on `trngnneee/eshop-sut` with screenshots (links updated in `bug-reports/README.md`).

---

## 6. Agent Skill

| Item | Detail |
| --- | --- |
| Skill file | `.cursor/skills/automation-testing/playwright-skill.md` |
| Skill demo (FR-15 E2E) | https://youtu.be/Te25xh0biYI |
| Task 2 demo (FR-15 run + 3 browsers + HTML + AI fix) | https://youtu.be/p5TRjyrvPvg |

---

## 7. How to reproduce

```powershell
cd SoftwareTesting-HW\HW4\23127271
# API :3000, Web :5173, Admin :5174
npm run evidence:verify-fr03
npm run test:matrix:fr08
npm run test:matrix:fr15
```

GitHub automation mirror: `Repo/eshop-sut/hw04-automation` on branch `HW4-Tram`.  
Commit history for `.spec.js`: `git-commit-log.txt`.

---

## 8. Self-assessment

| No. | Criteria | Max | Self |
| --- | ---: | ---: | ---: |
| 1 | Feature A (FR-03) | 25 | 22 |
| 1 | Feature B (FR-08) | 25 | 22 |
| 1 | Feature C (FR-15) | 25 | 22 |
| 2 | Task 2 — Demo video | 15 | 15 |
| 3 | Agent Skills | 10 | 9–10 |
| | **Total** | **100** | **~90–91** |

---

## 9. AI gap review (brief)

AI accelerated scaffolding but repeatedly risked green-washing defective SUT behavior. Mandatory human gate: keep README/FR oracles, fix only automation bugs (dialogs, SPA cart seed, locators), and treat matrix fails as either product bugs or environment blockers — never as a reason to edit expected results.
