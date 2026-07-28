Faculty of Information Technology (FIT) – Ho Chi Minh City University of Science (HCMUS)

CS423 / CSC13003 – Software Testing (AI-augmented · 2026)

AI POLICY · TEMPLATES — 2026 v1.0

# Privacy & Responsible AI Use Checklist

Run through this checklist before submitting any AI-assisted work.

Adapted from Med Kharbach, PhD (2026) — AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0. This adaptation is prepared for FIT@HCMUS – CS423 / CSC13003 Software Testing course.

## 1. Before I use AI

- [x] I confirmed the AI Use Category assigned to this assignment.
- [x] I have declared which AI tool(s) I will use in my prompt log.
- [x] I have read the AI Use Agreement for this course.
- [x] I understand which artifacts MUST NOT be AI-generated.

## 2. While I am using AI

- [x] I did not enter personal data of classmates, customers, or patients.
- [x] I did not paste copyrighted reading materials wholesale into the AI.
- [x] I did not paste proprietary employer or open-source license-restricted code.
- [x] I logged each prompt + AI response into the AI Audit Report (Section 3).

**Task 3 note — the screenshots are the sensitive artifact here, not personal data.** §11 (Anti-AI-Cheat) forbids AI-generated or fabricated cross-platform screenshots, so the following controls were applied:

- Every image under `results/` was produced by an actual browser run on this machine: viewport images by `page.screenshot()` inside `harness/run-audit.js`, window images by macOS `screencapture` inside `harness/scripts/capture-platform-proof.js`. **No image was generated, drawn, composited, up-scaled or retouched by any AI model**, and no image file was edited after capture.
- The evidence overlay (student ID / name / e-mail, engine + version, OS, device, viewport, locale, `location.href`, checklist ID, verdict, timestamp) is injected into the **live DOM of the page being captured** immediately before the shot and removed afterwards (`harness/lib/overlay.js`). It is a caption rendered by the browser itself, not post-processing of the picture.
- The window-level images are cropped to the browser window rectangle computed from the page (`window.screenX/screenY/outerWidth/outerHeight`) so that no unrelated application window or personal content of the desktop is captured. Each one was opened and visually checked before being kept.
- The only personal datum deliberately embedded in the artifacts is my own student ID, name and student e-mail (required by §6: "Each screenshot must overlay your username in the form your student email"). No third-party personal data appears anywhere in Task 3; unlike Task 2 there are no human participants in this task.
- Throwaway accounts created by the automated run use synthetic addresses of the form `xp-<timestamp>@t.local` on the local SQLite fixture only. No real e-mail address, phone number or credential of any real person was entered into the SUT or into the AI tool.

## 3. Before I submit my work

- [x] All AI-generated artifacts are tagged in the AI Audit Report.
- [x] All citations from AI have been verified (sources actually exist).
- [x] All AI-generated code has been executed and tested — the 66 checks were executed on the 3 required platforms (198 executions); `harness/scripts/verify-evidence.js` gates the run (fails if any item is missing, any FAIL lacks a screenshot, or any check ended in ERROR).
- [x] My 200–300-word AI Critique is included in the report (`cross-platform-report.md` §9).
- [x] The Mandatory Disclosure paragraph is at the end of my report.
- [x] I attached the AI Use Disclosure Form.
- [x] I am ready for a 5–7-min random oral defense the week after submission.

## 4. Final Statement

Final responsibility for the accuracy, originality, and integrity of this submission rests with me. Any undisclosed AI use is treated as academic misconduct.

## Signature

| Student name (printed): | DANG TRUONG NGUYEN |
| --- | --- |
| Student ID: | 23127438 |
| Class / Cohort: | 23KTPM3 |
| Course: | CS423 / CSC13003 – Software Testing |
| Instructor: | Msc. Tran Thi Bich Hanh |
| Date: | 28/07/2026 |
| Signature: | ![signature](./signature.png) |

## References

- Kharbach, M. (2026). AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0.
- ISTQB Foundation Level Syllabus (latest version).
- Hardman, P. (2025). A Post-AI Learning Taxonomy.
- Fuster Rabella, M. (2025). OECD Education Working Paper No. 338.
- Perkins, M., Roe, J., & Furze, L. (2025). AI Assessment Scale.
- Anthropic (2025). Building reliable AI test agents — engineering blog.
- DeepEval & Promptfoo documentation — testing frameworks for LLM systems.
