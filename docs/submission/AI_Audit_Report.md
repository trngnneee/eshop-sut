**Faculty of Information Technology (FIT) – Ho Chi Minh City University of Science (HCMUS)**

**CS423 / CSC13003 – Software Testing (AI-augmented · 2026)**

**AI POLICY · TEMPLATES — 2026 v1.0**

# **AI Audit Report — 5-section Template per Artifact**

*Mandatory appendix for every AI-assisted homework (HW#01–HW#06, and Seminar).*

*Adapted from Med Kharbach, PhD (2026) — AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0. This adaptation is prepared for FIT@HCMUS – CS423 / CSC15003 Software Testing course.*

## **1. Student Information**

| Field | Value |
| :---- | :---- |
| **Student name (printed):** | Phạm Quốc Thịnh |
| **Student ID:** | 23127231 |
| **Class / Cohort:** | 23CLC1 |
| **Assignment ID (e.g., HW#00, HW#02):** | HW#03 |
| **Assignment date:** | 01/08/2026 |
| **AI tool(s) used:** | Gemini 3.5 Flash (High) |
| **AI tool(s) used:** | [x] Yes  [ ] No |

## **2. Instructions (read before filling)**

* Add one row per AI-generated artifact (test case, script, checklist, OpenAPI spec, JMeter plan, etc.).  
* Paste the verbatim prompt — DO NOT paraphrase.  
* Paste the verbatim AI output (or include a labelled screenshot in the report).  
* Tag the verdict: VALID / INVALID / INCOMPLETE.  
* Reasoning must cite a course slide, ISTQB section, or technical RFC.  
* Show the corrected artifact with the change highlighted.  
* Sample rows are in italic — replace them before submission.

## **3. Audit Table — one row per artifact**

| (1) Prompt + Tool | (2) AI Output | (3) Verdict | (4) Reasoning (ISTQB) | (5) Student Fix |
| :---- | :---- | :---- | :---- | :---- |
| **Tool:** Gemini 3.5 Flash (High)<br>**Time:** 09:39 27/07/2026<br><br>**Prompt:**<br>hãy dựa vào phần 14 trong @[c:\Users\Public\Projects\Testing_HCMUS\HW3\eshop-sut\docs\requirements\2026.HW03.GUI Usability_En.md] để tạo các deliverable cần thiết (mỗi cái là 1 file, nội dung chỉ cần tạo sườn là được, ngôn ngữ tiếng việt). đưa các file đó vào trong @[c:\Users\Public\Projects\Testing_HCMUS\HW3\eshop-sut\docs\submission] . tên file có thể sử dụng tiếng anh | Tôi đã tạo đầy đủ sườn (skeleton) bằng tiếng Việt cho toàn bộ các file bàn giao (deliverables) dựa theo mục 14 (Submission Regulations) trong tài liệu yêu cầu. Tất cả các file đã được đặt trong thư mục [submission](./).<br><br>### Danh sách các file bàn giao được tạo:<br>1. **[README.md](./README.md)**: Chứa bảng tự đánh giá (Self-Assessment Table), báo cáo tóm tắt kiểm thử (Test Summary Report) và bản đồ các file nộp bài.<br>2. **[Main_Report.md](./Main_Report.md)**: Khung báo cáo chính, bao gồm báo cáo kiểm thử GUI Checklist, báo cáo đánh giá Usability, kiểm thử đa nền tảng và phần mô tả Agent Skills.<br>3. **[Bug_Report.md](./Bug_Report.md)**: Khung báo cáo lỗi chi tiết kết nối trực tiếp với GitHub Issues và khu vực gắn ảnh chụp màn hình minh chứng lỗi.<br>4. **[AI_Report.md](./AI_Report.md)**: Mẫu Nhật ký kiểm toán AI (AI Audit Report) và phần hướng dẫn viết nhận xét phê bình AI (AI Critique từ 200–300 từ).<br>5. **[Git_Commit_Log.txt](./Git_Commit_Log.txt)**: Cấu trúc mẫu lịch sử Git commit chi tiết tương ứng với từng giai đoạn thiết kế, thực thi và phân tích kiểm thử.<br>6. **[GUI_Checklist.md](./GUI_Checklist.md)**: Chứa danh sách đầy đủ hơn 40 mục kiểm thử GUI (IA-01 đến IA-04) để bạn dễ dàng điền trạng thái và xuất sang Excel.<br>7. **[Usability_Session_Evidence.md](./Usability_Session_Evidence.md)**: Khung ghi nhận bằng chứng thực nghiệm của 7 phiên test với người dùng thực tế (kịch bản kiểm thử, bảng 7 người tham gia, mẫu bảng điểm SUS, ghi chép hành vi và mức độ nghiêm trọng).<br>8. **[Cross_Platform_Evidence.md](./Cross_Platform_Evidence.md)**: Sườn báo cáo kiểm thử đa trình duyệt/nền tảng kèm hướng dẫn chèn ảnh chụp màn hình minh chứng lỗi. | **INCOMPLETE** | AI đã tạo cấu trúc các file bàn giao chính xác, nhưng tự động điền sẵn 40 mục checklist chi tiết vào GUI_Checklist.md thay vì tạo sườn bảng trống như yêu cầu. | Yêu cầu AI xóa danh sách checklist đi, chỉ giữ lại cấu trúc bảng trống để nạp động qua Agent Skill. |
| **Tool:** Gemini 3.5 Flash (High)<br>**Time:** 10:19 27/07/2026<br><br>**Prompt:**<br>okay, hãy dựa vào @[c:\Users\Public\Projects\Testing_HCMUS\HW3\eshop-sut\docs\materials\gui-testing\GUI_Testing.html] để tạo agent skill cho gui testing nhé, lưu ý: ngoài những hướng dẫn về kỹ thuật kiểm thử gui testing, thì skill còn phải update tài liệu cho quá trình thực hiện vào những file delierables mà bạn vừa tạo ở trên (@[c:\Users\Public\Projects\Testing_HCMUS\HW3\eshop-sut\docs\submission\Main_Report.md] @[c:\Users\Public\Projects\Testing_HCMUS\HW3\eshop-sut\docs\submission\GUI_Checklist.md] @[c:\Users\Public\Projects\Testing_HCMUS\HW3\eshop-sut\docs\submission\Bug_Report.md]). nội dung trình bày vào các tài liệu phải súc tích, đúng trọng tâm, dễ hiểu | Tôi đã tạo thành công Kỹ năng Agent (Agent Skill) dành cho việc kiểm thử giao diện (GUI Testing) tại thư mục `.agents` của workspace.<br><br>### Chi tiết về Agent Skill được tạo:<br>* **Tên kỹ năng:** `gui_testing`<br>* **Đường dẫn tệp cấu hình:** [SKILL.md](file:///c:/Users/Public/Projects/Testing_HCMUS/HW3/eshop-sut/.agents/skills/gui_testing/SKILL.md)<br><br>### Nội dung nổi bật trong Kỹ năng:<br>1. **Cơ sở kỹ thuật kiểm thử:** Tóm tắt 8 khía cạnh cốt lõi từ slide bài học [GUI_Testing.html](file:///c:/Users/Public/Projects/Testing_HCMUS/HW3/eshop-sut/docs/materials/gui-testing/GUI_Testing.html) (Visual, Functional, Validation, Usability, Responsive, Compatibility, Accessibility, Feedback).<br>2. **Quy trình thực thi kiểm thử:** Phân tích các trạng thái của Component (nút bấm, ô nhập liệu, màn hình) để thực hiện rà soát có hệ thống.<br>3. **Quy trình cập nhật tài liệu bàn giao:** Hướng dẫn chi tiết, ngắn gọn cách cập nhật đồng bộ thông tin kết quả kiểm thử vào 3 file tài liệu đã tạo:<br>   - [GUI_Checklist.md](./GUI_Checklist.md): Cập nhật kết quả Pass/Fail và tự động tính toán tỷ lệ đạt ở bảng tóm tắt.<br>   - [Bug_Report.md](./Bug_Report.md): Điền chi tiết từng lỗi (BUG-XX) với các bước tái hiện, phân loại mức độ nghiêm trọng (Severity) rõ ràng và tích hợp liên kết GitHub Issue.<br>   - [Main_Report.md](./Main_Report.md): Cập nhật phạm vi kiểm thử, đúc kết tổng quan các khía cạnh lỗi giao diện và môi trường kiểm thử đa nền tảng.<br>4. **Hướng dẫn viết kịch bản Playwright Automation:** Cách kiểm tra lỗi tràn ngang viewport để test tính Responsive, kiểm tra trạng thái Component, và kiểm tra thông báo lỗi dữ liệu (Validation). | **INCOMPLETE** | AI đã tạo tệp hướng dẫn SKILL.md khá đầy đủ nhưng thiếu hướng dẫn chi tiết cách thiết kế/tự động tạo checklist và thiếu lưu ý quan trọng về bản chất Black-box testing. | Yêu cầu AI cập nhật thêm cách sinh checklist bằng AI và ghi nhận thêm các ràng buộc về kiểm thử hộp đen. |
| **Tool:** Gemini 3.5 Flash (High)<br>**Time:** 10:23 27/07/2026<br><br>**Prompt:**<br>hey, sửa lại @[c:\Users\Public\Projects\Testing_HCMUS\HW3\eshop-sut\docs\submission\GUI_Checklist.md] , tôi chưa yêu cầu bạn tạo checklist bây giờ, nên xóa các checklist đi, giữ lại cấu trúc bảng thôi, phần tạo checklist sẽ có trong skill gui testing | Tôi đã cập nhật lại tệp [GUI_Checklist.md](./GUI_Checklist.md) bằng cách xóa toàn bộ các mục checklist chi tiết được tạo trước đó, chỉ giữ lại cấu trúc tiêu đề bảng và một hàng ví dụ minh họa cấu trúc như yêu cầu của bạn. <br><br>Phần sinh nội dung chi tiết cho checklist này sẽ do Kỹ năng Agent (Agent Skill) đảm nhiệm khi bạn kích hoạt nó. | **VALID** | AI đã xóa thành công các dữ liệu checklist tự sinh dư thừa, đưa GUI_Checklist.md về trạng thái cấu trúc bảng trống chuẩn xác để sẵn sàng cho quá trình thực thi sau này. | Chấp nhận kết quả (Accepted as-is). |
| **Tool:** Gemini 3.5 Flash (High)<br>**Time:** 10:25 27/07/2026<br><br>**Prompt:**<br>bạn update lại skill để hướng dẫn cách tạo checklist đi | Tôi đã cập nhật lại tệp [SKILL.md](file:///c:/Users/Public/Projects/Testing_HCMUS/HW3/eshop-sut/.agents/skills/gui_testing/SKILL.md) để thêm hướng dẫn chi tiết về cách thiết kế và tạo danh sách checklist.<br><br>### Các nội dung được cập nhật trong Kỹ năng Agent (Agent Skill):<br>* **Phương pháp phân tích & Chọn màn hình:** Hướng dẫn Agent cách xác định các màn hình cần kiểm thử và liệt kê các Component chính.<br>* **Quy trình sinh checklist bằng AI:** Cung cấp mẫu Prompt chi tiết với vai trò chuyên gia QA/QC để sinh hơn 40 mục kiểm thử phân loại theo 4 nhóm từ `IA-01` đến `IA-04` dưới dạng bảng Markdown tương thích.<br>* **Quy trình rà soát và bổ sung thủ công:** Hướng dẫn Agent cách lọc các nội dung trùng lặp và chủ động bổ sung các mục kiểm thử quan trọng mà AI thường bỏ sót (khả năng tiếp cận, phím Tab, phản hồi từ server, hiển thị trên thiết bị di động thực tế).<br>* **Quy trình cập nhật tài liệu:** Hướng dẫn chèn kết quả vừa sinh vào tệp [GUI_Checklist.md](./GUI_Checklist.md) để thực hiện chạy kiểm thử sau đó. | **VALID** | AI đã cập nhật đúng và đầy đủ quy trình thiết kế và tạo danh sách checklist bằng cách phối hợp giữa AI và rà soát thủ công (Human Review) vào SKILL.md. | Chấp nhận kết quả (Accepted as-is). |
| **Tool:** Gemini 3.5 Flash (High)<br>**Time:** 10:29 27/07/2026<br><br>**Prompt:**<br>thêm vào skill để chỉ rõ rằng gui test là black box nên đừng inspect code | Tôi đã cập nhật lại tệp tin [SKILL.md](file:///c:/Users/Public/Projects/Testing_HCMUS/HW3/eshop-sut/.agents/skills/gui_testing/SKILL.md) để chỉ rõ rằng **GUI Testing là phương pháp Kiểm thử Hộp đen (Black-box Testing)**.<br><br>### Nội dung cập nhật trong Kỹ năng Agent (Agent Skill):<br>* **Hộp lưu ý quan trọng (Important Alert):** Nhấn mạnh rằng Agent chỉ được phép tương tác, quan sát và đánh giá hệ thống thông qua giao diện người dùng trực quan dưới góc nhìn của người dùng cuối. **Tuyệt đối không** đọc, phân tích hay kiểm tra mã nguồn (inspect code/source code) của ứng dụng SUT để đối chiếu hay tìm kiếm lỗi.<br>* **Bảo toàn tùy chỉnh của bạn:** Giữ nguyên quy tắc chọn màn hình kiểm thử đã chỉnh sửa trước đó. | **VALID** | AI đã bổ sung đúng ghi chú quan trọng về việc giữ nguyên bản chất Black-box testing của GUI Testing theo lý thuyết ISTQB Foundation Level, ngăn ngừa việc inspect business code trái phép. | Chấp nhận kết quả (Accepted as-is). |

## **4. Summary of AI Accuracy**

Aggregate the verdicts from Section 3 and complete the table below.

| Metric | Count | Percentage |
| :---- | :---- | :---- |
| **Total AI-generated artifacts audited** | 5 | 100% |
| **VALID (correct, accepted as-is)** | 3 | 60% |
| **INVALID (wrong; rejected)** | 0 | 0% |
| **INCOMPLETE (acceptable after edits)** | 2 | 40% |

## **5. Conclusion — When should AI be used (or not)?**

Write 80–150 words describing patterns you observed. Where did AI shine? Where did AI fail? What is your recommendation for using AI in this kind of work in the future?

Qua quá trình làm việc với AI để chuẩn bị tài liệu và xây dựng Agent Skill cho dự án EShop, có thể thấy AI thể hiện thế mạnh vượt trội trong việc sinh cấu trúc (skeleton) nhanh chóng và đúng định dạng Markdown. AI cũng hỗ trợ tốt trong việc viết mã Playwright để kiểm thử tự động. Tuy nhiên, AI thường có xu hướng tự điền thông tin chi tiết (như tự động sinh 40 mục checklist giao diện) khi chưa có yêu cầu cụ thể, hoặc chưa nắm rõ quy tắc kiểm thử hộp đen hoàn toàn cho đến khi được nhắc nhở. Khuyến nghị sử dụng AI làm trợ lý đắc lực để sinh khung tài liệu và viết code mẫu, nhưng lập trình viên/QA cần kiểm soát chặt chẽ các ràng buộc nghiệp vụ (như không inspect source code) và điều chỉnh lại cấu trúc để phù hợp nhất với dự án.

## **6. Mandatory Disclosure (paste verbatim)**

*"[Test cases / script / dataset / report] was initially generated by Gemini 3.5 Flash (High); I reviewed and modified [GUI_Checklist.md, SKILL.md], added [black-box guidelines, screen selection rules]; [README.md, Main_Report.md, Bug_Report.md] was written entirely by me. The detailed AI Audit Report is attached as Appendix A. I confirm I did not use AI to generate any artifact listed in the prohibited category."*

## **Signature**

| Student name (printed): | Phạm Quốc Thịnh |
| :---- | :---- |
| **Student ID:** | 23127231 |
| **Class / Cohort:** | 23CLC1 |
| **Course:** | CS423 / CSC13003 – Software Testing |
| **Instructor:** | Dr. Lam Quang Vu / Dr. Tran Duy Hoang |
| **Date:** | 01/08/2026 |
| **Signature:** | Phạm Quốc Thịnh |

## **References**

* Kharbach, M. (2026). AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0.  
* ISTQB Foundation Level Syllabus (latest version).  
* Hardman, P. (2025). A Post-AI Learning Taxonomy.  
* Fuster Rabella, M. (2025). OECD Education Working Paper No. 338.  
* Perkins, M., Roe, J., & Furze, L. (2025). AI Assessment Scale.  
* Anthropic (2025). Building reliable AI test agents — engineering blog.  
* DeepEval & Promptfoo documentation — testing frameworks for LLM systems.