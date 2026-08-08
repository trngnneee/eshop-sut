---
name: gui-testing-skill
description: Thiết kế, thực thi và kiểm tra tính đầy đủ của GUI Checklist Task 1 HW03 cho EShop; bắt buộc >=41 item, đủ IA-01..IA-04, AI critique, evidence lỗi và bug/GitHub traceability.
---

# GUI Testing Skill — HW03

## 1. Nguyên tắc không thương lượng

- SUT mặc định là EShop của HW03. Không dùng artifact của đề/SUT khác.
- Checklist phải có **ít nhất 41 item phi lặp lại** và phủ cả `IA-01`, `IA-02`, `IA-03`, `IA-04`.
- Mỗi item phải có: `ID`, `Screen/Route`, `IA`, `Category`, `Origin`, `Checklist Item`, `Expected`, `Actual`, `Status`, `Notes`, `Evidence`, `Bug ID`.
- `Origin` chỉ nhận `AI_INITIAL` hoặc `HUMAN_ADDED` để chứng minh human review.
- Mọi item phải được thực thi. Không tuyên bố `COMPLETE` nếu còn `Not Run` hoặc `Blocked`.
- Mỗi item `Fail` phải có Actual Result, Notes, Bug ID và screenshot tồn tại. Chỉ Pass không bắt buộc screenshot.
- Không bịa GitHub Issue URL. Khi chưa post thật, ghi `PENDING_EXTERNAL_ACTION` và trạng thái bài vẫn chưa Complete.

## 2. Workflow bắt buộc

### Gate A — Scope

1. Đọc requirement HW03 và xác nhận EShop.
2. Chọn đủ màn hình để đạt 41 item có chiều sâu; khuyến nghị Product Listing, Product Detail, Cart/Checkout.
3. Ghi môi trường: Desktop 1440x900, Tablet 768x1024, Mobile 390x844.

### Gate B — Design

1. Sinh bộ `AI_INITIAL`.
2. Kiểm tra trùng ý bằng ID và Expected Result.
3. Bổ sung `HUMAN_ADDED` cho accessibility, keyboard, 320px, chuỗi dài/ký tự đặc biệt, XSS, API slow/empty/4xx/5xx, browser Back/Forward và focus sau navigation.
4. Với từng item human-added, ghi lý do AI bỏ sót.
5. Xác nhận `count >= 41` và mỗi IA có coverage thực chất; IA-03 phải có hành vi navigation, không chỉ kiểm tra link tồn tại.

### Gate C — Execution

- Thực thi trên SUT. Automation có thể mock API để tạo slow/empty/error state nhưng phải ghi rõ; luồng tích hợp chính phải có ít nhất một lần chạy live SUT.
- Status chỉ nhận `Pass`, `Fail`, `Blocked`, `Not Run`.
- Screenshot/video/trace lưu theo tên ổn định: `evidence/BUG-GUI-XX.png`.
- Không xóa artifact của lần chạy đã dùng trong báo cáo.

### Gate D — Report

Tạo tối thiểu `GUI_Checklist_HW3.md/.xlsx`, `GUI_Bug_Report_HW3.md`, `GUI_Test_Summary_HW3.md`, evidence cho từng Fail, nội dung GitHub Issue, bảng AI Critique item-level và đoạn critique tổng thể 200–300 từ.

### Gate E — Completion validator

Chạy `scripts/validate-gui.ps1`. Chỉ báo `COMPLETE` khi >=41 item, không ID trùng, đủ bốn IA, không còn Not Run/Blocked, mọi Fail có Bug ID/evidence tồn tại, có Markdown/Excel/bug report/summary/AI critique, và mọi bug có GitHub Issue URL thật.

## 3. Quy tắc chất lượng

- Expected Result phải quan sát/đo được; không dùng “đẹp” hoặc “hoạt động tốt”.
- Không gộp nhiều assertion không liên quan.
- Pass/Fail phản ánh SUT; locator/test harness sai phải sửa trước khi log bug.
- Severity: Critical (security/data loss), High (blocker/core flow), Medium (degraded flow/accessibility), Low (minor visual/copy).
- Evidence dùng đường dẫn tương đối; không dùng `file:///`.

## 4. Definition of Done

Chưa hoàn tất nếu thiếu bất kỳ mục nào: 41 item, đủ IA, execution, fail screenshots, bug Markdown, GitHub traceability, Excel, AI Audit, AI Critique, commit log và demo-video link. Hành động cần tài khoản/quyền ngoài workspace phải ghi blocker, không giả lập.
