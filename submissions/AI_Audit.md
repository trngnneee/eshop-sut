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
| **Class / Cohort:** | 23KTPM3 |
| **Assignment ID (e.g., HW\#00, HW\#02):** | HW06 – API Testing |
| **Assignment date:** | 18/08/2026 |
| **AI tool(s) used:** | Claude Sonnet 4.6 (Anthropic) |
| **AI used?:** | \[x\] Yes  \[ \] No |

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
| **Tool:** Claude Sonnet 4.6<br>**Time:** 10:29 18/08/2026<br>**Prompt:**<br>```okay, bạn hãy tạo các skill cần thiết để hoàn thành bài tập này nhé, không cần tạo skill update file ai audit đâu. lưu ý: những bước nào cần con người review hoặc đánh giá thì AI sẽ không thực hiện các bước đó, thay vào đó chỉ đề xuất khung sườn cho các tài liệu liên quan thôi. skill ngoài hướng dẫn từng bước về các kỹ thuật, còn phải yêu cầu agent cập nhật vào các tài liệu markdown liên quan.``` | Tất cả 5 skills đã được tạo thành công. Đây là tóm tắt:<br><br>---<br><br>## ✅ Các Skills đã tạo<br><br>Tất cả nằm trong [`.agents/skills/`](file:///c:/Users/Public/Projects/Testing_HCMUS/HW6/eshop-sut/.agents/skills):<br><br>\| Skill \| File \| Mục đích \|<br>\|:------\|:-----\|:---------\|<br>\| **`hw6-generate-testcases`** \| [SKILL.md](file:///c:/Users/Public/Projects/Testing_HCMUS/HW6/eshop-sut/.agents/skills/hw6-generate-testcases/SKILL.md) \| Sinh ≥35 TC bằng 4 prompt riêng biệt (DP, ST, SEC, SV) + cập nhật `test_cases_apiN.md` và `report.md` \|<br>\| **`hw6-audit-testcases`** \| [SKILL.md](file:///c:/Users/Public/Projects/Testing_HCMUS\HW6\eshop-sut\.agents\skills\hw6-audit-testcases\SKILL.md) \| Tạo khung bảng audit sẵn sàng để người review điền — AI không tự đánh nhãn VALID/INVALID \|<br>\| **`hw6-extend-testcases`** \| [SKILL.md](file:///c:/Users/Public/Projects/Testing_HCMUS/HW6/eshop-sut/.agents/skills/hw6-extend-testcases/SKILL.md) \| Phân tích blind spots + gợi ý ≥8 ý tưởng TC mà AI thường bỏ sót, tạo khung phần Extend \|<br>\| **`hw6-execute-newman`** \| [SKILL.md](file:///c:/Users/Public/Projects/Testing_HCMUS/HW6/eshop-sut/.agents/skills/hw6-execute-newman/SKILL.md) \| Tạo Postman Collection JSON + script Newman + cập nhật `bug_report.md` và `report.md` \|<br>\| **`hw6-cicd-setup`** \| [SKILL.md](file:///c:/Users/Public/Projects/Testing_HCMUS/HW6/eshop-sut/.agents/skills/hw6-cicd-setup/SKILL.md) \| Tạo GitHub Actions workflow + hướng dẫn 2 commits + cập nhật `cicd_report.md` \|<br>\| **`hw6-agent-skill-design`** \| [SKILL.md](file:///c:/Users/Public/Projects/Testing_HCMUS/HW6/eshop-sut/.agents/skills/hw6-agent-skill-design/SKILL.md) \| Thiết kế kiến trúc 5-module test generator, pseudocode, prototype Python + cập nhật `agent_skill.md` \|<br><br>### Nguyên tắc thiết kế chung<br><br>- **Các bước cần con người review** (audit VALID/INVALID, viết lý do AI bỏ sót, link GitHub Issues, chụp screenshot, tự vẽ diagram) → AI **chỉ tạo placeholder sườn**, không tự điền<br>- **Mỗi skill đều có section "Cập nhật tài liệu (BẮT BUỘC)"** → nhắc agent ghi kết quả vào đúng các file markdown liên quan<br>- **Checklist cuối mỗi skill** → agent tự kiểm tra trước khi kết thúc | INCOMPLETE | AI đã tạo đầy đủ các skills và tuân thủ yêu cầu để lại khung cho con người review. Tuy nhiên, phần kỹ thuật Domain Partition chưa chi tiết hóa nguyên tắc Boundary Value Analysis (2-point/3-point), Error Isolation (mỗi ca lỗi chỉ test 1 biến sai) và State Transition chưa phân loại rõ vòng đời CRUD / Auth Session theo ISTQB FL v4.0 §4.2 & §4.3. Tên file báo cáo tham chiếu cũng còn ở dạng cũ `report.md`. | Sinh viên trực tiếp chỉnh sửa và chuẩn hóa lại nội dung kỹ thuật Domain Testing (EP & BVA), State Transition & Lifecycle trong skill `generate-api-testcases/SKILL.md`, đồng thời đổi tên file báo cáo chính sang `MainReport.md`. |
| **Tool:** Claude Sonnet 4.6<br>**Time:** 11:14 18/08/2026<br>**Prompt:**<br>```tôi vừa mới update lại 1 số nội dung về domain testing và state transition testing trong skill @[c:\Users\Public\Projects\Testing_HCMUS\HW6\eshop-sut\.agents\skills\generate-api-testcases] , bạn hãy update lại các phần nội dung liên quan nhé``` | Mình đã đồng bộ và cập nhật toàn bộ các tài liệu và kỹ năng liên quan theo đúng các nội dung bạn vừa cập nhật:<br><br>---<br><br>### 1. Cập nhật Skill [`generate-api-testcases/SKILL.md`](file:///c:/Users/Public/Projects/Testing_HCMUS/HW6/eshop-sut/.agents/skills/generate-api-testcases/SKILL.md)<br>- **Tên & Tiêu đề Skill:** Đồng bộ tên `# Skill: generate-api-testcases`.<br>- **Mục tiêu kỹ thuật:** Cập nhật mô tả kỹ thuật **Domain Testing (EP & BVA - Phân lớp tương đương & Phân tích giá trị biên)** và **State Transition & Lifecycle (Chuyển trạng thái nghiệp vụ, Session/Auth, CRUD Lifecycle)**.<br>- **Mẫu báo cáo `MainReport.md`:** Đồng bộ cấu trúc báo cáo 4 prompts riêng biệt (Domain EP/BVA, State Transition & Lifecycle, Security, Schema Validation) và thống kê chi tiết `(DP/BVA: X \| ST: Y \| SEC: Z \| SV: W)`.<br><br>---<br><br>### 2. Cập nhật các bảng trong Test Cases (`submissions/test_cases_api1.md`, `api2.md`, `api3.md`)<br>- **Bảng A (Domain EP & BVA):** Cập nhật cấu trúc cột chuẩn:<br>  `\| TC ID \| Mô tả \| Tham số kiểm tra \| Phân vùng / Điểm biên \| Input Payload (Params/Body) \| Expected HTTP Status & Output \| Audit \| Ghi chú \|`<br>- **Bảng B (State Transition & Lifecycle):** Cập nhật cấu trúc cột chuẩn:<br>  `\| TC ID \| Mô tả kịch bản \| Trạng thái ban đầu (Pre-state) \| Hành động / Payload \| Trạng thái kỳ vọng (Post-state) \| Expected HTTP Status & Error Code \| Audit \| Ghi chú \|`<br><br>---<br><br>### 3. Cập nhật Báo cáo chính [`submissions/MainReport.md`](file:///c:/Users/Public/Projects/Testing_HCMUS/HW6/eshop-sut/submissions/MainReport.md)<br>- Cập nhật mục 2.1, 3.1, 4.1 để phân tách thành 4 block prompt và tóm tắt output rõ ràng tương ứng 4 kỹ thuật (Domain EP/BVA, State Transition & Lifecycle, Security, Schema Validation).<br><br>---<br><br>### 4. Đồng bộ các Skill phụ trợ còn lại<br>- Đã cập nhật tất cả đường dẫn báo cáo từ `report.md` thành `MainReport.md` trong các skill:<br>  - [`hw6-audit-testcases/SKILL.md`](file:///c:/Users/Public/Projects/Testing_HCMUS/HW6/eshop-sut/.agents/skills/hw6-audit-testcases/SKILL.md)<br>  - [`hw6-extend-testcases/SKILL.md`](file:///c:/Users/Public/Projects/Testing_HCMUS/HW6/eshop-sut/.agents/skills/hw6-extend-testcases/SKILL.md)<br>  - [`hw6-execute-newman/SKILL.md`](file:///c:/Users/Public/Projects/Testing_HCMUS/HW6/eshop-sut/.agents/skills/hw6-execute-newman/SKILL.md)<br>  - [`hw6-cicd-setup/SKILL.md`](file:///c:/Users/Public/Projects/Testing_HCMUS/HW6/eshop-sut/.agents/skills/hw6-cicd-setup/SKILL.md)<br>  - [`hw6-agent-skill-design/SKILL.md`](file:///c:/Users/Public/Projects/Testing_HCMUS/HW6/eshop-sut/.agents/skills/hw6-agent-skill-design/SKILL.md) | VALID | Toàn bộ các tài liệu markdown (`MainReport.md`, `test_cases_api1/2/3.md`) và các skills phụ trợ đã được đồng bộ chính xác theo các quy tắc thiết kế ca kiểm thử Domain Testing & State Transition mới, tuân thủ ISTQB FL v4.0 §4.2 & §4.3 và tài liệu đặc tả `2026.HW06.API Testing_En.md`. | Chấp nhận toàn bộ kết quả cập nhật (Accepted as-is). |

## **4\. Summary of AI Accuracy**

Aggregate the verdicts from Section 3 and complete the table below.

| Metric | Count | Percentage |
| :---- | :---- | :---- |
| **Total AI-generated artifacts audited** | 2 | 100% |
| **VALID (correct, accepted as-is)** | 1 | 50% |
| **INVALID (wrong; rejected)** | 0 | 0% |
| **INCOMPLETE (acceptable after edits)** | 1 | 50% |

## **5\. Conclusion — When should AI be used (or not)?**

AI (Claude Sonnet 4.6) thể hiện năng lực vượt trội trong việc tự động hóa xây dựng cấu trúc các kỹ năng (Agent Skills), sinh khung sườn tài liệu markdown có cấu trúc rõ ràng và thiết lập quy trình kiểm thử API theo chuỗi hoạt động chuẩn mực. Tuy nhiên, AI ban đầu có xu hướng khái quát hóa các kỹ thuật kiểm thử nếu prompt chưa cung cấp ràng buộc cụ thể (ví dụ: nguyên tắc Error Isolation trong EP/BVA hoặc bao phủ trạng thái chuỗi N-switch). Do đó, sự can thiệp và kiểm soát của con người (Human-in-the-loop) là bắt buộc để tinh chỉnh prompt, audit nhãn kiểm thử và đảm bảo tính chính xác kỹ thuật theo chuẩn ISTQB. AI nên được dùng làm trợ lý tăng tốc triển khai khung sườn và sinh test case ban đầu, nhưng con người phải là người ra quyết định đánh giá và hoàn thiện cuối cùng.

## **6\. Mandatory Disclosure (paste verbatim)**

*"Các Agent Skills và khung tài liệu bài tập ban đầu được sinh bởi Claude Sonnet 4.6; tôi đã xem xét, chuẩn hóa lại các nguyên tắc kỹ thuật Domain Testing (EP & BVA) và State Transition & Lifecycle trong skill generate-api-testcases, cập nhật các bảng test cases và đồng bộ toàn bộ tài liệu sang MainReport.md; phần đánh giá audit và mở rộng test cases do tôi trực tiếp thực hiện. Báo cáo AI Audit chi tiết được đính kèm tại Phụ lục A. Tôi xác nhận không sử dụng AI để sinh bất kỳ sản phẩm nào thuộc danh mục bị cấm."*

## **Signature**

| Student name (printed): | Phan Quốc Thịnh |
| :---- | :---- |
| **Student ID:** | 23127486 |
| **Class / Cohort:** | 23KTPM3 |
| **Course:** | CS423 / CSC13003 – Software Testing |
| **Instructor:** | Dr. Lam Quang Vu / Dr. Tran Duy Hoang |
| **Date:** | 18/08/2026 |
| **Signature:** | Phan Quốc Thịnh |

## **References**

* Kharbach, M. (2026). AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0.  
* ISTQB Foundation Level Syllabus (latest version).  
* Hardman, P. (2025). A Post-AI Learning Taxonomy.  
* Fuster Rabella, M. (2025). OECD Education Working Paper No. 338\.  
* Perkins, M., Roe, J., & Furze, L. (2025). AI Assessment Scale.  
* Anthropic (2025). Building reliable AI test agents — engineering blog.  
* DeepEval & Promptfoo documentation — testing frameworks for LLM systems.
