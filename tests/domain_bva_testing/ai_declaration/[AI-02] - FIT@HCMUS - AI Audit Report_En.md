Faculty of Information Technology (FIT) – Ho Chi Minh City University of Science (HCMUS)

CS423 / CSC13003 – Software Testing (AI-augmented · 2026)

AI POLICY · TEMPLATES — 2026 v1.0

# AI Audit Report — 5-section Template per Artifact

Mandatory appendix for every AI-assisted homework (HW#01–HW#06, and Seminar).

Adapted from Med Kharbach, PhD (2026) — AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0. This adaptation is prepared for FIT@HCMUS – CS423 / CSC15003 Software Testing course.

## 1. Student Information

| Field | Value |
| --- | --- |
| Student name (printed): | DANG TRUONG NGUYEN |
| Student ID: | 23127438 |
| Class / Cohort: | 23KTPM3 |
| Assignment ID (e.g., HW#00, HW#02): | HW02 |
| Assignment date: | 28/06/2026 |
| AI tool(s) used: | Codex GPT 5.5 |
| AI tool(s) used: | [X] Yes  [ ] No |

## 2. Instructions (read before filling)

- Add one row per AI-generated artifact (test case, script, checklist, OpenAPI spec, JMeter plan, etc.).
- Paste the verbatim prompt — DO NOT paraphrase.
- Paste the verbatim AI output (or include a labelled screenshot in the report).
- Tag the verdict: VALID / INVALID / INCOMPLETE.
- Reasoning must cite a course slide, ISTQB section, or technical RFC.
- Show the corrected artifact with the change highlighted.
- Sample rows are in italic — replace them before submission.

## 3. Audit Table — one row per artifact

| (1) Prompt + Tool | (2) AI Output | (3) Verdict | (4) Reasoning (ISTQB) | (5) Student Fix |
| --- | --- | --- | --- | --- |
| **Tool:** Codex<br>**Source:** `tests/ai_log/2026-06-26-fr04-fr10-bug-mapping-session-log.md`<br>**Prompt recorded in ai_log:**<br>1. Map BUG IDs, đặt tên bug, update status cho các test case FR-04 sau khi test xong trong file test run.<br>2. Tạo folder bug trong `tests`, dùng issue template để ghi list bug cho FR-04, để trống evidence cho tester bổ sung sau.<br>3. Làm tương tự cho FR-10.<br>4. Export session này ra `ai_log` trong `tests`. | Updated FR-04 test run to 32 total test cases with 20 Passed / 12 Failed; mapped failed FR-04 rows to `BUG-FR04-*`; updated all FR-04 testcase statuses; created `tests/bug/FR-04.md`.<br><br>Updated FR-10 test run to 23 total test cases with 21 Passed / 2 Failed; mapped failed FR-10 rows to `BUG-FR10-*`; updated all FR-10 testcase statuses; created `tests/bug/FR-10.md`.<br><br>Created the audit log at `tests/ai_log/2026-06-26-fr04-fr10-bug-mapping-session-log.md`. | INCOMPLETE | ISTQB Foundation Level guidance on defect management requires defect reports to be traceable, reproducible, and supported by actual/expected results. The AI produced useful bug IDs and traceability, but the evidence fields were intentionally left for the tester, so the artifact was not submission-ready as-is. | I reviewed the mapped failed rows against the test-run files, kept the grouped bug IDs, and left `[Bổ sung evidence sau]` placeholders for screenshots/API responses to be added after manual verification. |
| **Tool:** GPT-5 Codex<br>**Source:** `tests/ai_log/2026-06-27-fr18-test-generation-session-log.md`<br>**Prompt recorded in AI Audit Extract:**<br>Sử dụng SKILL.md để gen test case dựa trên yêu cầu FR-18 trong README.md, sau đó export session này ra ai_log trong tests.<br><br>**Follow-up prompt recorded in AI Audit Extract:**<br>Map kết quả chạy giống nhau từ FR-10 sang FR-18, tạo bug FR-18 riêng, tạo issue list trong tests/bug, đồng bộ Status / Related bugs trong các file testcase, rồi chèn session này vào ai_log. | Generated `tests/test-configs/fr18-config.json`, 27 FR-18 testcase Markdown files, `tests/test-runs/fr18-admin-order-management-test-run.md`, `tests/test-summary/fr18-admin-order-management-summary.md`, and the FR-18 traceability block.<br><br>Follow-up updated FR-18 execution results to 21 Passed / 6 Failed, created `tests/bug/FR-18.md`, mapped failures to `BUG-FR18-S-01`, `BUG-FR18-A-01`, and `BUG-FR18-X-01`, and synchronized testcase statuses with the test-run file. | INCOMPLETE | ISTQB test design guidance requires test cases to be derived from the test basis and reviewed for coverage. The AI correctly reused FR-10 state-machine behavior for FR-18, but the mapping from FR-10 to FR-18 required human judgment because user-cancel cases are not applicable to Admin Order Management. Evidence for defects also remained pending. | I checked the FR-18 requirement sources, kept only applicable Admin transitions, used FR-18-specific bug IDs instead of reusing FR-10 IDs, and verified testcase/test-run status synchronization before accepting the artifact. |
| **Tool:** GPT-5 Codex<br>**Source:** `tests/ai_log/2026-06-28-fr20-bug-mapping-session-log.md`<br>**Prompt recorded in AI Audit Extract:**<br>hãy map các test case failed sang BUG defect ở bảng dưới, không dùng lại BUG của FR-10. Ngoài ra, tạo 1 folder bug trong tests, với FR-20 này, hãy dùng template issue để ghi 1 list bug trong đó để t dễ dàng tạo issue trên Github dựa vào file đó, các chỗ evidence t sẽ bổ sung sau. Đường dẫn bắt đầu từ eshop-sut<br><br>**Follow-up prompt recorded in AI Audit Extract:**<br>export session này ra ai_log | Mapped failed `FR20-X-TC03` to new bug `BUG-FR20-X-01`, updated the FR-20 test-run summary to 18 total with 17 Passed / 1 Failed, replaced the defect-log placeholder, synchronized all 18 FR-20 testcase statuses, created `tests/bug/FR-20.md`, and exported the session log to `tests/ai_log/2026-06-28-fr20-bug-mapping-session-log.md`. | INCOMPLETE | ISTQB defect reporting guidance requires enough information for reproduction and confirmation. The AI identified the failed case and prepared an issue-ready defect, but the evidence remained intentionally blank and the SQL-like payload behavior still needed tester-provided proof before submission. | I kept the new FR-20-specific bug ID, verified that no `BUG-FR10-*` references remained, checked the 17 Passed / 1 Failed totals, and left the evidence field open for manual screenshots/logs. |

## 4. Summary of AI Accuracy

Aggregate the verdicts from Section 3 and complete the table below.

| Metric | Count | Percentage |
| --- | --- | --- |
| Total AI-generated artifacts audited | 3 | 100% |
| VALID (correct, accepted as-is) | 0 | 0% |
| INVALID (wrong; rejected) | 0 | 0% |
| INCOMPLETE (acceptable after edits) | 3 | 100% |

## 5. Conclusion — When should AI be used (or not)?

Write 80–150 words describing patterns you observed. Where did AI shine? Where did AI fail? What is your recommendation for using AI in this kind of work in the future?

I use Codex GPT 5.5 to generate test cases for the eShop application. The AI was able to produce a variety of test cases, but many of them were incomplete or did not fully adhere to the requirements specified in the assignment. While AI can be a useful tool for generating initial drafts of test cases, it is clear that human oversight is necessary to ensure accuracy and completeness. In future assignments, I recommend using AI as a supplementary tool rather than a primary source for test case generation. It can help speed up the process, but students should always review and refine the output to meet the required standards.

## 6. Mandatory Disclosure (paste verbatim)

"[Test cases / script / dataset / report] was initially generated by [AI tool name]; I reviewed and modified [section X], added [edge cases Y, Z]; [section W] was written entirely by me. The detailed AI Audit Report is attached as Appendix A. I confirm I did not use AI to generate any artifact listed in the prohibited category."

## Signature

| Student name (printed): | DANG TRUONG NGUYEN |
| --- | --- |
| Student ID: | 23127438 |
| Class / Cohort: | 23KTPM3 |
| Course: | CS423 / CSC13003 – Software Testing |
| Instructor: | Msc. Tran Thi Bich Hanh |
| Date: | 28/06/2026 |
| Signature: | ![signature](./signature.png) |

## References

- Kharbach, M. (2026). AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0.
- ISTQB Foundation Level Syllabus (latest version).
- Hardman, P. (2025). A Post-AI Learning Taxonomy.
- Fuster Rabella, M. (2025). OECD Education Working Paper No. 338.
- Perkins, M., Roe, J., & Furze, L. (2025). AI Assessment Scale.
- Anthropic (2025). Building reliable AI test agents — engineering blog.
- DeepEval & Promptfoo documentation — testing frameworks for LLM systems.
