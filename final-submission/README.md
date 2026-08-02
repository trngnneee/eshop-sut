# HW03 Consolidated Submission

**Student:** Đặng Đăng Khoa  
**Student ID:** 23127207  
**Student email used in evidence overlays:** `23127207@student.hcmus.edu.vn`  
**System under test:** EShop  
**Prepared:** 2026-08-02 — Asia/Bangkok (UTC+7)  
**Human-review state:** `HUMAN_REVIEWED`

## Purpose

This directory is the six-file consolidated entry point for HW03. It replaces the need to open multiple top-level reports while preserving the original Task 1, Task 2 and Task 3 folders as the evidence archive. The evidence archive is intentionally not deleted: the consolidated documents link to its item-level CSV/JSON, screenshots, SUS calculations, session coding, validators and private submission controls.

Exactly six files belong in this directory:

| File | Purpose |
|---|---|
| `README.md` | Opening instructions, status dashboard, privacy and evidence rules. |
| `Main_Report.md` | One combined report for GUI checklist testing, usability testing and cross-platform testing. |
| `Bug_Report.md` | One combined, severity-ranked register separating software bugs from usability issues. |
| `AI_Critique.md` | Three human-reviewed critique sections, one for each task. |
| `AI_Audit_Report.md` | Consolidated AI interaction, correction, validation and anti-fabrication record. |
| `git-commit-log.txt` | Authentic repository history snapshot using full Git hashes. |

## Current status dashboard

| Area | Default/local validator | Strict completion gate | Honest status |
|---|---:|---:|---|
| Task 1 — GUI checklist | Exit 0 | Exit 2 | 58 unique items, 37 Pass, 20 Fail, 1 Blocked; GUI-skill demo is verified; 12 GitHub mappings and native soft-keyboard evidence remain external. |
| Task 2 — usability | Exit 0 | Exit 2 | Package closure and submission validation pass; absent pilot, consent, probes and some environment/timing evidence remain disclosed. |
| Task 3 — cross-platform | Exit 0 | Exit 2 | 232 result rows and 160 screenshots are structurally valid; only 2/3 rubric-eligible platforms are evidenced. |

An exit-2 strict gate is not relabelled as success. It records an unavailable external/fieldwork requirement without fabricating replacement evidence.

## Demo links

| Task | Public YouTube link | Verification |
|---|---|---|
| Task 1 — GUI-testing skill | [GUI-testing-skill demo](https://youtu.be/tMar6OyMG80) | `PUBLIC_LINK_VERIFIED` through YouTube oEmbed; title `GUI-testing-skill demo`, author `Đặng Đăng Khoa`. |
| Task 2 — usability-testing skill | [Usability-testing demo](https://youtu.be/QAh6W9AJXiU) | `PUBLIC_LINK_VERIFIED`; YouTube-link-only submission. |

No local MP4 is required or retained.

## Evidence archive

- Task 1 source of truth: [`../task1-gui/results/Task1_Execution_Chrome.csv`](../task1-gui/results/Task1_Execution_Chrome.csv).
- Task 1 screenshots: [`../task1-gui/evidence/executed-chrome/`](../task1-gui/evidence/executed-chrome/).
- Task 2 session coding: [`../task2-usability/Sessions/`](../task2-usability/Sessions/).
- Task 2 SUS source and calculations: [`../task2-usability/Analysis/`](../task2-usability/Analysis/).
- Task 2 private roster: [`../task2-usability/Participant_Roster.md`](../task2-usability/Participant_Roster.md); submission-only, not for public issue publication.
- Task 3 matrix and result data: [`../task3-cross-platform/Cross_Platform_Matrix.md`](../task3-cross-platform/Cross_Platform_Matrix.md) and [`../task3-cross-platform/results/`](../task3-cross-platform/results/).
- Task 3 screenshots: [`../task3-cross-platform/evidence/`](../task3-cross-platform/evidence/).

The three source task directories are supporting evidence, not additional top-level reports in this consolidated entry point.

## Privacy and publication boundary

- Consolidated analytical files use participant IDs P01–P07 only; participant names and masked contacts remain in the private roster.
- Raw participant recordings and frames are not copied into this directory.
- Synthetic technical screenshots are used for GitHub defect reproduction.
- The current local branch contains submission-only Task 2 material and must not be pushed wholesale to a public repository.
- Public Task 1/Task 3 evidence requires an explicitly approved sanitized branch because screenshots contain the student name, ID and email overlay.
- A GitHub URL is recorded only if it is an existing verified issue or returned by GitHub after publication; pending URLs are never invented.

## Reading order

1. Open `Main_Report.md` for methods, metrics, SUS, platform coverage and completion status.
2. Open `Bug_Report.md` for defect/usability separation, severity, evidence and issue traceability.
3. Open `AI_Critique.md` for the human-reviewed evaluation of AI limitations.
4. Open `AI_Audit_Report.md` for prompts, corrections, validator results and anti-fabrication decisions.
5. Use `git-commit-log.txt` to verify the procedure history.

## Reproduction and validation

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\task1-gui\scripts\validate-gui.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\task2-usability\scripts\analyze-sus.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\task2-usability\scripts\validate-usability.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\task2-usability\scripts\validate-submission-files.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\task3-cross-platform\scripts\validate-task3.ps1
```

For the deliberately stricter evidence gates, add `-RequireComplete` to the Task 1/Task 3 validators and `-RequireCompleteEvidence` to the Task 2 validator. These strict commands are expected to return exit code 2 until their documented external evidence is supplied.
