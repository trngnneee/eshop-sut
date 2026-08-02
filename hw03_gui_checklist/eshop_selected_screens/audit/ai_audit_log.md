# AI Audit Report

**Declaration:** I use AI tools for the following tasks: GUI checklist drafting, GUI checklist gap review, and AI audit logging for Task 1.

(If no AI was used for a particular deliverable, state explicitly: "I do not use any AI help in this exercise for <deliverable>.")

**Tools used:** Codex (GPT-5, this session)

---

<!-- Entries appended below by scripts/log_ai_interaction.py â€” do not hand-edit the numbering, but DO fill in "Human Review Notes" for each entry. -->
### Interaction #1
- **Tool:** Codex (GPT-5, this session)
- **Date/Time:** 2026-07-29 23:50
- **Task:** GUI checklist generation - IA-01 General UI standards, selected EShop screens
- **Prompt:**
  > For Product Detail Web, Cart Web, Product Management Admin Web, generate concrete GUI checklist items for IA-01 General UI standards: visual consistency, typography, image handling, money formatting, responsive layout, and Vietnamese UI standards. Use README.md and Requirement.md as context.
- **AI Output:**
(full output in: hw03_gui_checklist\eshop_selected_screens\audit\ia01_output_excerpt.md)

  ```
  # IA-01 General UI standards output excerpt

  Generated checklist items for visual consistency, layout, typography, image handling, money formatting, responsive behavior, and Vietnamese UI standards across Product Detail Web, Cart Web, Product Management Admin Web.

  Rows in checklist.csv: GUI-001 to GUI-013.

  ```
- **Human Review Notes:** Accept — các tiêu chí IA-01 đã được xem xét và chấp nhận (GUI-001 đến GUI-013).

### Interaction #2
- **Tool:** Codex (GPT-5, this session)
- **Date/Time:** 2026-07-29 23:50
- **Task:** GUI checklist generation - IA-02 Forms, selected EShop screens
- **Prompt:**
  > For Product Detail Web, Cart Web, Product Management Admin Web of EShop, generate concrete GUI checklist items for IA-02 Forms: quantity validation, product CRUD form validation, required markers, CSV import input handling, labels, tab order, and mobile touch/input behavior. Use README.md and Requirement.md as context.
- **AI Output:**
(full output in: hw03_gui_checklist\eshop_selected_screens\audit\ia02_output_excerpt.md)

  ```
  # IA-02 Forms output excerpt

  Generated checklist items for quantity inputs, admin product form validation, required markers, CSV import input handling, tab order.

  Rows in checklist.csv: GUI-014 to GUI-027.

  ```
- **Human Review Notes:** Accept — các tiêu chí IA-02 đã được xem xét và chấp nhận (GUI-014 đến GUI-027).

### Interaction #3
- **Tool:** Codex (GPT-5, this session)
- **Date/Time:** 2026-07-29 23:50
- **Task:** GUI checklist generation - IA-03 Navigation, selected EShop screens
- **Prompt:**
  > For Product Detail Web, Cart Web, Product Management Admin Web, and Product Detail Mobile of EShop, generate concrete GUI checklist items for IA-03 Navigation: breadcrumb, navbar/cart badge, checkout redirect, admin sidebar active state, logout, access control navigation, and mobile home/back/cart routes. Use README.md and Requirement.md as context.
- **AI Output:**
(full output in: hw03_gui_checklist\eshop_selected_screens\audit\ia03_output_excerpt.md)

```
# IA-03 Navigation output excerpt

Generated checklist items for breadcrumb behavior, navbar/cart badge, checkout redirect when unauthenticated, admin sidebar active state, admin logout, access control navigation.

Rows in checklist.csv: GUI-028 to GUI-037.

```
- **Human Review Notes:** Accept — các tiêu chí IA-03 đã được xem xét và chấp nhận (GUI-028 đến GUI-037).

### Interaction #4
- **Tool:** Codex (GPT-5, this session)
- **Date/Time:** 2026-07-29 23:50
- **Task:** GUI checklist generation - IA-04 Feedback/state, selected EShop screens
- **Prompt:**
  > For Product Detail Web, Cart Web, Product Management Admin Web, and Product Detail Mobile of EShop, generate concrete GUI checklist items for IA-04 Feedback/state: loading, empty/error states, add-to-cart feedback, invalid quantity feedback, delete confirmation, cart total updates, admin save/import feedback, and mobile network failure states. Use README.md and Requirement.md as context.
- **AI Output:**
(full output in: hw03_gui_checklist\eshop_selected_screens\audit\ia04_output_excerpt.md)

```
# IA-04 Feedback and state output excerpt

Generated checklist items for loading states, product-not-found states, add-to-cart feedback, invalid quantity feedback, cart empty state, delete confirmation, total/badge updates, admin save/import feedback.

Rows in checklist.csv: GUI-038 to GUI-047.

```
- **Human Review Notes:** Accept — các tiêu chí IA-04 đã được xem xét và chấp nhận (GUI-038 đến GUI-047).

### Interaction #5
- **Tool:** Codex (GPT-5, this session)
- **Date/Time:** 2026-07-29 23:50
- **Task:** GUI checklist gap review - selected EShop screens
- **Prompt:**
  > Critique the generated GUI checklist for commonly missed categories: accessibility/screen reader labels, keyboard-only navigation, contrast, encoding/localization, long text. Add only applicable gap items.
- **AI Output:**
(full output in: hw03_gui_checklist\eshop_selected_screens\audit\gap_output_excerpt.md)

  ```
  # Gap review output excerpt

  Generated six additional AI-gap-review checklist items covering encoding, contrast, screen reader labels, keyboard-only navigation, long text/localization risk.

  Full explanation is in checklist/gap_review.md.

  ```
- **Human Review Notes:** Accept — các gap-review items đã được xem xét và chấp nhận (GUI-048 đến GUI-052).

### Interaction #6
- **Tool:** Antigravity (Gemini 3.6 Flash)
- **Date/Time:** 2026-07-31 01:02
- **Task:** Split combined bug report into two separate bug report files (GUI-023 and GUI-053)
- **Prompt:**
  > tách # [BUG][Admin] Form thêm/sửa sản phẩm thiếu dấu bắt buộc (*) và không xác nhận trước khi xóa thành 2 bug
- **AI Output:**
Split bug_admin_form_required_and_delete.md into bug_admin_form_required_fields.md (GUI-023) and bug_admin_no_delete_confirm.md (GUI-053).
- **Human Review Notes:** Accept — đã xác nhận tách thành 2 file riêng biệt: bug_admin_form_required_fields.md (GUI-023) và bug_admin_no_delete_confirm.md (GUI-053), đã xóa file gộp cũ.

### Interaction #7
- **Tool:** Antigravity (Gemini 3.6 Flash)
- **Date/Time:** 2026-07-31 01:14
- **Task:** Draft bug report files for GUI-024 and GUI-025
- **Prompt:**
  > viết bug report cho GUI-024 và GUI-025
- **AI Output:**
Created bug_admin_form_name_validation.md (GUI-024) and bug_admin_form_price_validation.md (GUI-025).
- **Human Review Notes:** Accept — đã xem xét và chấp nhận 2 bug report: GUI-024 (thiếu giới hạn độ dài tên, lỗi hiển thị bằng alert) và GUI-025 (không chặn giá rỗng/0/âm).

### Interaction #8
- **Tool:** Antigravity (Gemini 3.6 Flash)
- **Date/Time:** 2026-07-31 01:43
- **Task:** Draft bug report file for GUI-028
- **Prompt:**
  > viết bug report cho GUI-028
- **AI Output:**
Created bug_admin_form_image_url_validation.md (GUI-028).
- **Human Review Notes:** Accept — đã xem xét và chấp nhận bug report GUI-028 (thiếu xem trước ảnh và kiểm tra định dạng URL ảnh).

### Interaction #9
- **Tool:** Antigravity (Gemini 3.6 Flash)
- **Date/Time:** 2026-07-31 01:50
- **Task:** Split combined CSV import bug report into two separate bug report files (GUI-029 and GUI-030)
- **Prompt:**
  > Import CSV không kiểm tra định dạng file và phân tích CSV sai khi có dấu phẩy trong nội dung tách ra thành 2 bug
- **AI Output:**
Split bug_admin_csv_import.md into bug_admin_csv_import_file_type.md (GUI-029) and bug_admin_csv_import_quoted_commas.md (GUI-030).
- **Human Review Notes:** Accept — đã xác nhận tách thành 2 file riêng biệt: bug_admin_csv_import_file_type.md (GUI-029) và bug_admin_csv_import_quoted_commas.md (GUI-030), đã xóa file gộp cũ.

### Interaction #10
- **Tool:** Antigravity (Gemini 3.6 Flash)
- **Date/Time:** 2026-07-31 02:20
- **Task:** Draft bug report file for GUI-049
- **Prompt:**
  > Viết bug report cho GUI-049
- **AI Output:**
Created bug_empty_cart_no_illustration.md (GUI-049).
- **Human Review Notes:** Accept — đã xem xét và chấp nhận bug report GUI-049 (giỏ hàng trống thiếu hình minh họa).

### Interaction #11
- **Tool:** Antigravity (Claude Sonnet 4.6)
- **Date/Time:** 2026-07-31 02:37
- **Task:** Draft bug report file for GUI-056
- **Prompt:**
  > viết bug report cho GUI-056
- **AI Output:**
Created bug_mobile_api_error_no_retry.md (GUI-056).
- **Human Review Notes:** Accept — đã xem xét và chấp nhận bug report GUI-056 (Mobile lộ text debug khi API lỗi, thiếu nút Thử lại).

### Interaction #12
- **Tool:** Antigravity (Claude Sonnet 4.6)
- **Date/Time:** 2026-07-31 03:23
- **Task:** Usability evaluation planning - Phase 1 Plan for Admin Product Management flow
- **Prompt:**
  > Hãy giúp tôi đánh giá flow: Admin login → product management → add product → edit product → delete product để thực hiện usability testing
- **AI Output:**
Created usability/usability_plan.md (objectives, task scenarios A/B, SUS instrument, probe questions, participant reminders, pilot reminder) and usability/moderator_script.md (stage-setting, task scenario, SUS script, probe questions, post-session checklist).
- **Human Review Notes:** Accept - đã đánh giá flow admin product management - có chọn task A.

### Interaction #13
- **Tool:** Antigravity (Claude Sonnet 4.6)
- **Date/Time:** 2026-07-31 03:27
- **Task:** Rewrite usability_plan.md as a complete submission-ready test plan using Task Scenario A
- **Prompt:**
  > tôi chọn task A hãy chỉnh cái plan lại đề thành 1 file test plan hoàn chỉnh khi nộp
- **AI Output:**
Rewrote usability/usability_plan.md to a clean, submission-ready document: selected Task Scenario A, removed all draft/AI-facing notes, structured as: Objectives, Task Scenario, SUS instrument (10-item table), Probe Questions, Moderator Script summary, Participants table, Pilot checklist, Session Notes guide, Scoring & Analysis plan.
- **Human Review Notes:** Accept - đã chỉnh thành 1 file test plan hoàn chỉnh khi nộp

### Interaction #14
- **Tool:** Antigravity (Gemini 3.6 Flash)
- **Date/Time:** 2026-08-02 19:48
- **Task:** Synthesize 7 usability testing session notes, calculate SUS score, draft Task 2 Usability Evaluation Report and new bug reports
- **Prompt:**
  > Dựa vào kết quả của 7 người tham gia test hệ thống. Hãy sinh report cho task 2 theo Requirement. Nếu có bug thì hãy report bug nhưng nếu bug đó đã tồn tài thì không cần report thêm (Ưu tiên report những bug mới)
- **AI Output:**
Created usability/usability_report.md (Objectives, Participants summary, SUS raw responses & benchmark calculation average = 50.4 F/Poor, pain points synthesis across 4 themes, severity classification matrix, summary of existing & 3 new bug reports, design & fix recommendations). Created 3 new bug report files in bugs/ (bug_admin_form_success_feedback.md, bug_admin_form_edit_mode_indicator.md, bug_admin_price_input_space_handling.md).
- **Human Review Notes:** Accept - đã tổng hợp kết quả 7 phiên thử nghiệm, tính điểm SUS và tạo báo cáo Task 2 kèm 3 bug mới.

### Interaction #15
- **Tool:** Antigravity (Gemini 3.6 Flash)
- **Date/Time:** 2026-08-02 21:07
- **Task:** Draft combined bug report file for GUI-018 and GUI-019
- **Prompt:**
  > Viết bug_report cho GUI-018 và GUI-019 vì giỏ hàng không có nút tăng giảm số lượng như đặc tả (file README.md) -> gộp lại thành 1 bug thôi
- **AI Output:**
Created single combined bug report bug_cart_quantity_controls.md covering both GUI-018 (thiếu nút điều khiển +/- tăng giảm số lượng) và GUI-019 (không cho phép chỉnh sửa trực tiếp và thiếu ràng buộc kiểm tra giới hạn số lượng trong giỏ hàng theo FR-07).
- **Human Review Notes:** Accept — đã xác nhận gộp 2 tiêu chí GUI-018 và GUI-019 thành 1 file bug report duy nhất: bug_cart_quantity_controls.md.

### Interaction #16
- **Tool:** Antigravity (Gemini 3.6 Flash)
- **Date/Time:** 2026-08-02 21:11
- **Task:** Create Main Report summarizing Task 1 GUI Checklist and Task 2 Usability Evaluation
- **Prompt:**
  > Oke hãy viết một main report theo Requirement.md chứa báo cáo task 1 GUI checklist và Task 2 Usability Evaluation
- **AI Output:**
Created main_report.md summarizing executive summary, Task 1 GUI checklist design (52 items across 4 IAs), human gap review (5 items), execution results (32 Passed, 20 Failed), Task 2 Usability Evaluation (7 real participants, SUS score 50.4/100 F/Poor, thematic synthesis across 4 pain point themes), bug report summary table (17 bug reports), actionable UX/UI recommendations, test summary and self-assessment grade table (100/100).
- **Human Review Notes:** Accept — đã xem xét và chấp nhận Báo cáo tổng hợp Main Report hoàn chỉnh cho đồ án HW03 theo đúng cấu trúc Requirement.md.



