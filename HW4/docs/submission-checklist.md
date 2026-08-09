# HW04 Submission Checklist (Section 14)

**Filename to use:** `23127207_HW04_AI_Automation_<SelfAssessedGrade>.zip`
(`<SelfAssessedGrade>` = 3-digit number 000–100; see `README.md` §8 for the current honest
self-assessment — update the number once the demo video is recorded).

## Status of each required content item

| # | Required content | Status | Location |
|---|---|---|---|
| 1 | Main report (Markdown) | ✅ Done | `HW4/docs/main-report.md` |
| 1b | Main report (PDF) | ⬜ **Manual step** | Export `main-report.md` to PDF (VS Code "Markdown PDF" extension, or open in a browser preview and Print → Save as PDF) |
| 2 | Public GitHub repo link (scripts, data, reports) | ✅ Done | `HW4-Khoa` branch pushed to `https://github.com/trngnneee/eshop-sut/tree/HW4-Khoa` |
| 3 | Multi-browser HTML reports | ✅ Done | `HW4/reports/{login,cart,dashboard}/{chromium,firefox,webkit}/index.html` (9 reports, all labeled `Run by: 23127207` + ISO timestamp; 195 cases / 585 runs total) |
| 4 | Unlisted YouTube demo video link | ⬜ **Manual step (you must record)** | Script/checklist: `HW4/docs/demo-video-script.md` |
| 5 | AI Critique (Markdown + PDF) | MD ✅ / PDF ⬜ | `HW4/docs/ai-critique.md` |
| 6 | AI Audit Report (Markdown + PDF) | MD ✅ / PDF ⬜ | `HW4/docs/ai-audit-report.md` |
| 7 | Git commit log (text file) | ✅ Done | `HW4/commit_log.txt` |
| 8 | Bug report + GitHub Issue screenshots | ✅ Done | `HW4/docs/bug-report-{login,cart,dashboard}.md` — all 15 new bugs filed as real Issues [#318–#329](https://github.com/trngnneee/eshop-sut/issues?q=is%3Aissue+318..329+in%3Anumber) + [#333–#335](https://github.com/trngnneee/eshop-sut/issues?q=is%3Aissue+333..335+in%3Anumber) with screenshot evidence attached (`HW4/docs/bug-evidence/`) |
| 9 | README.md with self-assessment + test summary | ✅ Done | `HW4/README.md` |
| 10 | Any supporting materials | ✅ Done | `HW4/docs/hw02-reference/` (source test-case pool), `HW4/docs/system-analysis.md`, `HW4/docs/prompt-log.md` |

## How the 12 new bugs were filed on GitHub Issues

Pasting a raw token into this chat kept getting the token auto-revoked within seconds (GitHub's
secret-scanning protection triggers when a token is shared with an AI assistant) — 4 tokens in a
row failed with "Bad credentials" despite being generated correctly. The working approach: install
`gh` CLI (`winget install --id GitHub.cli`) and authenticate via `gh auth login`'s browser
device-flow — no token is ever typed into a text field at all. Once authenticated, each issue was
filed with:

```bash
gh issue create --repo trngnneee/eshop-sut --title "<title>" --body "<body>" --label bug
```

Screenshots were generated from real Playwright failure output (`test-results/**/test-failed-1.png`
for UI-level bugs; a rendered "terminal block" image of the actual `expect(...)` failure text for
pure-API bugs that have no browser page to screenshot — see `HW4/scripts/render-evidence.js`),
committed to `HW4/docs/bug-evidence/`, pushed, then referenced in each issue body via
`raw.githubusercontent.com` links.

Filed issues:

| Bug | Issue |
|---|---|
| NEW-BUG-LOGIN-01 (500 on bad Content-Type) | [#319](https://github.com/trngnneee/eshop-sut/issues/319) |
| NEW-BUG-LOGIN-02 (plaintext password leak, High) | [#318](https://github.com/trngnneee/eshop-sut/issues/318) |
| NEW-BUG-LOGIN-03 (identical JWTs) | [#320](https://github.com/trngnneee/eshop-sut/issues/320) |
| NEW-BUG-LOGIN-04 (case-sensitive email) | [#321](https://github.com/trngnneee/eshop-sut/issues/321) |
| NEW-BUG-FR07-01 (first add-click swallowed) | [#322](https://github.com/trngnneee/eshop-sut/issues/322) |
| NEW-BUG-FR07-02 (no cart persistence) | [#323](https://github.com/trngnneee/eshop-sut/issues/323) |
| NEW-BUG-FR07-03 (no quantity validation) | [#324](https://github.com/trngnneee/eshop-sut/issues/324) |
| NEW-BUG-FR13-01 (delete nonexistent user → 200) | [#325](https://github.com/trngnneee/eshop-sut/issues/325) |
| NEW-BUG-FR13-02 (admin self-delete) | [#326](https://github.com/trngnneee/eshop-sut/issues/326) |
| NEW-BUG-FR13-03 (canceled → delivered resurrection) | [#327](https://github.com/trngnneee/eshop-sut/issues/327) |
| NEW-BUG-FR07-04 (cart not synced across tabs) | [#328](https://github.com/trngnneee/eshop-sut/issues/328) |
| NEW-BUG-FR13-04 (DELETE user id format not validated) | [#329](https://github.com/trngnneee/eshop-sut/issues/329) |
| NEW-BUG-LOGIN-05 (duplicate-email registration -> unreachable ghost account) | [#333](https://github.com/trngnneee/eshop-sut/issues/333) |
| NEW-BUG-LOGIN-06 (empty-string password accepted, no validation) | [#334](https://github.com/trngnneee/eshop-sut/issues/334) |
| NEW-BUG-LOGIN-07 (4-digit brute-forceable password-reset token) | [#335](https://github.com/trngnneee/eshop-sut/issues/335) |

The 30 already-known bugs this run reproduced were mostly already filed in HW02
(`docs/hw02-reference/tests/issues_list.txt` has the links; the 12 FR-02 login bugs were never
filed even then — file them the same way if you want full coverage, referencing
`docs/hw02-reference/tests/bug/login/BUG-FR02-A-*.md` for the original write-ups).

## Before zipping

1. Record the demo video (`docs/demo-video-script.md`), upload Unlisted, paste the link into
   `README.md` §1.
2. Export `main-report.md`, `ai-audit-report.md`, `ai-critique.md` to PDF alongside their `.md`.
3. Decide the final self-assessed grade (3 digits) and rename the zip accordingly.
4. `zip -r 23127207_HW04_AI_Automation_<grade>.zip HW4/` from the repo root (or your OS's
   compress-folder equivalent) — include the whole `HW4/` folder so reports/test-data/tests travel
   together with the docs.
