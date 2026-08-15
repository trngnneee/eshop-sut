**Faculty of Information Technology (FIT) – Ho Chi Minh City University of Science (HCMUS)**

**CS423 / CSC13003 – Software Testing (AI-augmented · 2026\)**

**AI POLICY · TEMPLATES — 2026 v1.0**

# **AI Audit Report — 5-section Template per Artifact**

*Mandatory appendix for every AI-assisted homework (HW\#01–HW\#06, and Seminar).*

*Adapted from Med Kharbach, PhD (2026) — AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0. This adaptation is prepared for FIT@HCMUS – CS423 / CSC15003 Software Testing course.*

## **1\. Student Information**

| Field | Value |
| :---- | :---- |
| **Student name (printed):** | Phan Quốc Thịnh |
| **Student ID:** | 23127486 |
| **Class / Cohort:** | _(Fill in class/cohort)_ |
| **Assignment ID (e.g., HW\#00, HW\#02):** | HW05 |
| **Assignment date:** | 15/08/2026 |
| **AI tool(s) used:** | Claude Sonnet 4.6 |
| **AI used?** | [x] Yes  [ ] No |

## **2\. Instructions (read before filling)**

* Add one row per AI-generated artifact (test case, script, checklist, OpenAPI spec, JMeter plan, etc.).  
* Paste the verbatim prompt — DO NOT paraphrase.  
* Paste the verbatim AI output (or include a labelled screenshot in the report).  
* Tag the verdict: VALID / INVALID / INCOMPLETE.  
* Reasoning must cite a course slide, ISTQB section, or technical RFC.  
* Show the corrected artifact with the change highlighted.  
* Sample rows are in italic — replace them before submission.

## **3\. Audit Table — one row per artifact**

| (1) Prompt \+ Tool | (2) AI Output | (3) Verdict | (4) Reasoning (ISTQB) | (5) Student Fix |
| :---- | :---- | :---- | :---- | :---- |
| **Tool:** Claude Sonnet 4.6<br>**Time:** 20:37 15/08/2026<br>**Prompt:**<br>`dựa vào đề bài trong @[c:\Users\Public\Projects\Testing_HCMUS\HW5\docs\2026.HW05.Performance Testing_En (1).md] , hãy tạo tất cả các file cần thiết (nội dung file chỉ bao gồm sườn, chứ chưa có nội dung cụ thể) để nộp bài, những file hình ảnh chưa có thì chưa cần tạo. tất cả file đó đưa vào thư mục @[c:\Users\Public\Projects\Testing_HCMUS\HW5\eshop-sut\submissions] . biết tôi tên Phan Quốc Thịnh, MSSV: 23127486` | Đã đọc xong đề bài. Tôi sẽ tạo các file skeleton cần thiết cho bài nộp trong thư mục `submissions`.<br><br>Dựa vào đề bài, các file cần thiết bao gồm:<br>1. **Report chính** (Markdown)<br>2. **AI Audit Report** (đã có, cần xem nội dung)<br>3. **AI Critique** (Markdown)<br>4. **README.md**<br>5. **Git commit log** (text file)<br>6. **3 test plans** (JMeter `.jmx` files) theo naming convention `23127486_{ScenarioType}_{YYYYMMDD}`<br>7. **CSV data files** cho workflow<br>8. **3 raw `.jtl` log files**<br>9. **Bug report** (Markdown)<br>10. **Continuous Performance Testing proposal** (có thể tích hợp vào report chính) | INCOMPLETE | AI tự động sinh cả các file thực thi test (.jmx) khi chưa thiết kế kịch bản chi tiết và chưa có yêu cầu cụ thể từ người dùng. Theo ISTQB FL §1.4 (Test Process), giai đoạn chuẩn bị tài liệu cấu trúc (Test Planning/Documentation) tách biệt với giai đoạn sinh artifact thực thi. | Người dùng yêu cầu AI dừng tạo file thực thi (.jmx, .jtl, csv), chỉ tập trung tạo các file tài liệu Markdown (.md) cần thiết. |
| **Tool:** Claude Sonnet 4.6<br>**Time:** 20:43 15/08/2026<br>**Prompt:**<br>`tiếp tục đi, nhưng các file được tạo trong quá trình thực thi test như jtl, test plan, html reports thì chưa cần tạo đâu, chỉ cần tạo các file tài liệu md cần thiết thôi` | Xong! Tất cả các file tài liệu `.md` đã được tạo/cập nhật. Đây là tổng kết:<br><br>---<br><br>## Tổng kết các file đã tạo trong `submissions/`<br><br>\| File \| Mô tả \| Trạng thái \|<br>\|:-----\|:-------\|:----------:\|<br>\| [`README.md`](file:///c:/Users/Public/Projects/Testing_HCMUS/HW5/eshop-sut/submissions/README.md) \| Bảng self-assessment + test summary report \| ✅ Mới \|<br>\| [`Report.md`](file:///c:/Users/Public/Projects/Testing_HCMUS/HW5/eshop-sut/submissions/Report.md) \| Report chính (Task 1, 2, 3) \| ✅ Mới \|<br>\| [`AI_Audit.md`](file:///c:/Users/Public/Projects/Testing_HCMUS/HW5/eshop-sut/submissions/AI_Audit.md) \| AI Audit Report – đã điền tên + MSSV \| ✅ Cập nhật \|<br>\| [`AI_Critique.md`](file:///c:/Users/Public/Projects/Testing_HCMUS/HW5/eshop-sut/submissions/AI_Critique.md) \| AI Critique 200–300 từ \| ✅ Mới \|<br>\| [`bug_report.md`](file:///c:/Users/Public/Projects/Testing_HCMUS\HW5\eshop-sut\submissions\bug_report.md) \| Báo cáo bug/performance issues \| ✅ Mới \|<br>\| [`git_commit_log.txt`](file:///c:/Users/Public/Projects/Testing_HCMUS/HW5/eshop-sut/submissions/git_commit_log.txt) \| Git commit log \| ✅ Mới \|<br><br>---<br><br>**Những gì chưa cần tạo** (sẽ sinh ra trong quá trình thực thi):<br>- `.jmx` — test plans (JMeter)<br>- `.jtl` — raw log files<br>- `html_reports/` — HTML report folders<br>- `test_data.csv` — CSV data<br>- `screenshots/` — ảnh chụp màn hình<br><br>> **Lưu ý:** Tên file zip nộp bài theo format: `23127486_HW05_AI_Performance_<SelfAssessedGrade>.zip` (ví dụ: `23127486_HW05_AI_Performance_090.zip`) | VALID | Đáp ứng chính xác yêu cầu tạo đầy đủ các khung tài liệu báo cáo (.md) theo quy định nộp bài trong HW05 (Mục 14). | Chấp nhận toàn bộ các file tài liệu đã tạo. |
| **Tool:** Claude Sonnet 4.6<br>**Time:** 20:47 15/08/2026<br>**Prompt:**<br>`okay, hãy  dựa vào yêu  cầu đề bài HW5 trong @[c:\Users\Public\Projects\Testing_HCMUS\HW5\docs\2026.HW05.Performance Testing_En (1).md] , rồi tạo  các skill cần thiết cho bài tập này nhé. lưu ý: skill ngoài hướng dẫn ai agent thực hiện từng bước, còn phải hướng dẫn cập nhật các tài liệu báo cáo liên quan trong @[c:\Users\Public\Projects\Testing_HCMUS\HW5\eshop-sut\submissions] trong quá trình thực thi. những yêu cầu nào mà buộc human review, hay đánh giá v.v thì không đưa vào agent skill.<br>lưu ý: task 1 có được giảng viên note lại như sau: you now need to perform load, stress, and spike testing on a single workflow that covers three API endpoint groups.` | Tất cả 4 skills đã được tạo đúng cấu trúc. Dưới đây là tổng kết:<br><br>---<br><br>## 4 Agent Skills đã tạo tại `.agents/skills/`<br><br>\| Skill \| Mô tả \| Task \|<br>\|:------\|:-------\|:-----\|<br>\| [`hw5-test-plan-design`](file:///c:/Users/Public/Projects/Testing_HCMUS/HW5/.agents/skills/hw5-test-plan-design/SKILL.md) \| Khám phá SUT API → thiết kế 1 workflow E2E bao phủ 3 nhóm endpoint → sinh 3 file `.jmx` (Load/Stress/Spike) + CSV → cập nhật `Report.md` Sec 3 & 4.1–4.2 \| Task 1 \|<br>\| [`hw5-jtl-analysis`](file:///c:/Users/Public/Projects/Testing_HCMUS/HW5/.agents/skills/hw5-jtl-analysis/SKILL.md) \| Parse `.jtl` logs → tính metrics → prompt AI theo 4 bước có cấu trúc → scaffold Report.md Sec 5.1–5.3 (chừa trống phần human review) \| Task 2 \|<br>\| [`hw5-ci-perf-proposal`](file:///c:/Users/Public/Projects/Testing_HCMUS/HW5/.agents/skills/hw5-ci-perf-proposal/SKILL.md) \| Thiết kế pipeline CI/CD tự động phát hiện p95 regression → sinh Mermaid flowchart → bàn luận trade-off → cập nhật `Report.md` Sec 6 \| Task 3 \|<br>\| [`hw5-ai-audit-update`](file:///c:/Users/Public/Projects/Testing_HCMUS/HW5/.agents/skills/hw5-ai-audit-update/SKILL.md) \| Ghi verbatim prompt + AI output + verdict vào `AI_Audit.md` → cập nhật bảng thống kê Section 4 → cập nhật `git_commit_log.txt` \| Mọi task \|<br><br>### Những gì **không** đưa vào skill (yêu cầu human review):<br>- ✂️ Phần nhận xét, sửa lỗi test plan của AI (Section 4.3)<br>- ✂️ Xác định AI đọc sai metrics nào (Section 5.2 — chỉ scaffold)<br>- ✂️ Phán quyết optimization feasible/hallucinated (Section 5.3 — chỉ scaffold)<br>- ✂️ Quay video demo<br>- ✂️ AI Critique 200–300 từ | INCOMPLETE | Trong `hw5-test-plan-design`, AI tự gán sẵn các endpoint ví dụ và tự định nghĩa cấu trúc cột CSV mà không dừng lại yêu cầu người dùng chỉ định workflow cụ thể. Vi phạm nguyên tắc phân công giữa thành viên nhóm (Section 5: "no two members may test the same workflow"). | Người dùng yêu cầu cập nhật skill `hw5-test-plan-design` để bắt buộc agent phải dừng lại và nhận workflow từ người dùng trước khi sinh test plan. |
| **Tool:** Claude Sonnet 4.6<br>**Time:** 21:15 15/08/2026<br>**Prompt:**<br>`@[c:\Users\Public\Projects\Testing_HCMUS\HW5\.agents\skills\hw5-test-plan-design\SKILL.md] , sửa lại skill này, các features/workflow phải do người dùng specify chứ không phải do AI chọn` | Xong. Đây là tóm tắt các thay đổi đã thực hiện trong [`SKILL.md`](file:///c:/Users/Public/Projects/Testing_HCMUS/HW5/.agents/skills/hw5-test-plan-design/SKILL.md):<br><br>\| Section \| Thay đổi \|<br>\|:--------\|:---------\|<br>\| **Step 0** \| Sửa typo ký tự thừa `ư` \|<br>\| **Step 1** \| Đổi hoàn toàn thành **"Confirm the Workflow with the User (REQUIRED)"** — có dấu ⚠️ STOP rõ ràng, liệt kê 4 câu hỏi phải hỏi user, yêu cầu **đợi user trả lời trước** khi làm bất cứ điều gì. AI chỉ được dùng để gợi ý think time sau khi đã có workflow từ user \|<br>\| **Step 2** \| Bỏ hardcode cột CSV (`username`, `product_id`, ...) — thay bằng hướng dẫn **suy ra cột từ workflow user đã confirm**, hỏi user về dữ liệu test đã seeded sẵn trong DB \| | VALID | Đã chỉnh sửa Step 1 thành chốt chặn bắt buộc (gate) để người dùng chỉ định workflow, đảm bảo tính cá nhân hóa và tránh trùng lặp giữa các sinh viên. | Chấp nhận sửa đổi của skill. Người dùng tự tinh chỉnh thêm một số câu hỏi khảo sát trong file SKILL.md. |

## **4\. Summary of AI Accuracy**

Aggregate the verdicts from Section 3 and complete the table below.

| Metric | Count | Percentage |
| :---- | :---- | :---- |
| **Total AI-generated artifacts audited** | 4 | 100% |
| **VALID (correct, accepted as-is)** | 2 | 50% |
| **INVALID (wrong; rejected)** | 0 | 0% |
| **INCOMPLETE (acceptable after edits)** | 2 | 50% |

## **5\. Conclusion — When should AI be used (or not)?**

Write 80–150 words describing patterns you observed. Where did AI shine? Where did AI fail? What is your recommendation for using AI in this kind of work in the future?

Qua quá trình thực hiện, AI (Claude Sonnet 4.6) thể hiện thế mạnh rất rõ ràng trong việc nhanh chóng phân tích tài liệu đặc tả, tạo cấu trúc khung (scaffolding) cho các file báo cáo Markdown và xây dựng các bộ Agent Skill theo đúng chuẩn. Tuy nhiên, AI có xu hướng "nhảy cóc" tự suy diễn các giá trị cụ thể (như tự chọn workflow, tự sinh file JMX khi chưa có dữ liệu test thực tế) thay vì chờ hướng dẫn từ con người. Khuyến nghị: Cần sử dụng AI theo chiến lược AI-First có kiểm soát (Human-in-the-Loop), thiết lập các bước kiểm tra (gates) nghiêm ngặt để con người quyết định phạm vi thử nghiệm trước khi để AI tự động sinh các artifact thực thi.

## **6\. Mandatory Disclosure (paste verbatim)**

*"Submission skeletons, report templates, and agent skills were initially generated by Claude Sonnet 4.6; I reviewed and modified the test plan design skill to enforce human-specified workflows and endpoint selections; the final skill refinements and workflow specifications were written/verified by me. The detailed AI Audit Report is attached as Appendix A. I confirm I did not use AI to generate any artifact listed in the prohibited category."*

## **Signature**

| Student name (printed): | Phan Quốc Thịnh |
| :---- | :---- |
| **Student ID:** | 23127486 |
| **Class / Cohort:** | _(Fill in class/cohort)_ |
| **Course:** | CS423 / CSC13003 – Software Testing |
| **Instructor:** | Dr. Lam Quang Vu / Dr. Tran Duy Hoang |
| **Date:** | 15/08/2026 |
| **Signature:** | _(Sign here)_ |

## **References**

* Kharbach, M. (2026). AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0.  
* ISTQB Foundation Level Syllabus (latest version).  
* Hardman, P. (2025). A Post-AI Learning Taxonomy.  
* Fuster Rabella, M. (2025). OECD Education Working Paper No. 338\.  
* Perkins, M., Roe, J., & Furze, L. (2025). AI Assessment Scale.  
* Anthropic (2025). Building reliable AI test agents — engineering blog.  
* DeepEval & Promptfoo documentation — testing frameworks for LLM systems.