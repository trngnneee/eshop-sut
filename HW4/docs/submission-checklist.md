# HW04 Submission Checklist (Section 14)

**Filename to use:** `23127207_HW04_AI_Automation_<SelfAssessedGrade>.zip`
(`<SelfAssessedGrade>` = 3-digit number 000–100; see `README.md` §8 for the current honest
self-assessment — update the number once the demo video is recorded and issues are filed).

## Status of each required content item

| # | Required content | Status | Location |
|---|---|---|---|
| 1 | Main report (Markdown) | ✅ Done | `HW4/docs/main-report.md` |
| 1b | Main report (PDF) | ⬜ **Manual step** | Export `main-report.md` to PDF (VS Code "Markdown PDF" extension, or open in a browser preview and Print → Save as PDF) |
| 2 | Public GitHub repo link (scripts, data, reports) | ⬜ **Manual step** | Push `HW4-Khoa` branch (or merge to `main`) to `https://github.com/trngnneee/eshop-sut` and copy the link |
| 3 | Multi-browser HTML reports | ✅ Done | `HW4/reports/{login,cart,dashboard}/{chromium,firefox,webkit}/index.html` (9 reports, all labeled `Run by: 23127207` + ISO timestamp) |
| 4 | Unlisted YouTube demo video link | ⬜ **Manual step (you must record)** | Script/checklist: `HW4/docs/demo-video-script.md` |
| 5 | AI Critique (Markdown + PDF) | MD ✅ / PDF ⬜ | `HW4/docs/ai-critique.md` |
| 6 | AI Audit Report (Markdown + PDF) | MD ✅ / PDF ⬜ | `HW4/docs/ai-audit-report.md` |
| 7 | Git commit log (text file) | ✅ Done | `HW4/commit_log.txt` |
| 8 | Bug report + GitHub Issue screenshots | Docs ✅ / Issues ⬜ | `HW4/docs/bug-report-{login,cart,dashboard}.md`; filing real GitHub Issues needs a `GITHUB_TOKEN` or the `gh` CLI, neither available in this environment — see "Filing bugs on GitHub" below |
| 9 | README.md with self-assessment + test summary | ✅ Done | `HW4/README.md` |
| 10 | Any supporting materials | ✅ Done | `HW4/docs/hw02-reference/` (source test-case pool), `HW4/docs/system-analysis.md`, `HW4/docs/prompt-log.md` |

## Filing bugs on GitHub Issues (manual — needs your credentials)

The 10 newly-found bugs (4 login + 3 cart + 3 dashboard, listed with ready-to-paste titles/bodies
in each `bug-report-*.md`) have not been filed as GitHub Issues yet. To do it:

```bash
export GITHUB_TOKEN=<your PAT with repo scope, from https://github.com/settings/tokens>
gh auth login --with-token <<< "$GITHUB_TOKEN"    # if gh CLI is installed
gh issue create --repo trngnneee/eshop-sut --title "<title from bug-report-*.md>" --body "<body>" --label bug
```

Or paste each one manually at `https://github.com/trngnneee/eshop-sut/issues/new`. After creating
each issue, attach a screenshot (from the corresponding failing test's `test-results/**/test-failed-1.png`,
or the HTML report's failure view) as an issue comment, then link the issue number back into the
matching `bug-report-*.md`.

The 29 already-known bugs this run reproduced were mostly already filed in HW02
(`docs/hw02-reference/tests/issues_list.txt` has the links; the 12 FR-02 login bugs were never
filed even then — file them now using the same process, referencing `docs/hw02-reference/tests/bug/login/BUG-FR02-A-*.md` for the original write-ups).

## Before zipping

1. Record the demo video (`docs/demo-video-script.md`), upload Unlisted, paste the link into
   `README.md` §1 and this checklist.
2. Export `main-report.md`, `ai-audit-report.md`, `ai-critique.md` to PDF alongside their `.md`.
3. Push the branch, grab the GitHub repo URL.
4. File the GitHub Issues above (or explicitly note in `README.md` if you choose to skip some).
5. Decide the final self-assessed grade (3 digits) and rename the zip accordingly.
6. `zip -r 23127207_HW04_AI_Automation_<grade>.zip HW4/` from the repo root (or your OS's
   compress-folder equivalent) — include the whole `HW4/` folder so reports/test-data/tests travel
   together with the docs.
