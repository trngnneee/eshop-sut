# AI Audit Report

## Interaction 001

### AI Tool
GitHub Copilot

### Date & Time

### Prompt

### AI Output Summary

### Human Review
Accepted:
Modified:
Rejected:

## Interaction 002

### AI Tool
GitHub Copilot

### Date & Time
06/25/2026 08:02 AM

### Prompt
using skill domain-testing to analyze FR-05

### AI Output Summary
Phân tích đặc tả FR-05, tạo báo cáo Domain Testing, sinh 12 test case cho module product và ghi nhận audit log theo yêu cầu.

### Human Review
Accepted:
Modified:
Rejected:

## Interaction 003

### AI Tool
Gemini

### Date & Time
06/27/2026 08:03 AM

### Prompt
using domain-testing to analyze FR11

### AI Output Summary
Phân tích đặc tả FR-11, tạo báo cáo Domain Testing và Boundary Value Analysis, sinh 10 test case cho module ORDER-HISTORY và cập nhật audit report.

### Human Review
Accepted:
Modified:
Rejected:

## Interaction 004

### AI Tool
Antigravity (Claude Sonnet 4.6 Thinking)

### Date & Time
06/28/2026 12:26 AM

### Prompt
using domain-testing skill to analyze FR-19

### AI Output Summary
Phân tích đặc tả FR-19 (Quản lý Người dùng - Admin), áp dụng Domain Testing và Boundary Value Analysis. Sinh 20 test case cho module USERMGMT bao gồm: kiểm tra xem danh sách (không lộ mật khẩu), kiểm tra phân quyền (admin/user/unauthenticated), kiểm tra xóa người dùng hợp lệ và không hợp lệ, kiểm tra ràng buộc self-delete, BVA cho user_id (0, 1, 2, 999999, "abc") và số lượng user (0, 1, 50+). Cập nhật docs/domain-testing-report.md và docs/ai-audit-report.md.

### Human Review
Accepted:
Modified:
Rejected:

## Interaction 005

### AI Tool
Antigravity (Claude Opus 4.6 Thinking)

### Date & Time
06/28/2026 09:40 PM

### Prompt
sử dụng skill domain-testing để phân tích FR-10: Trạng thái Đơn hàng (Order State Machine) nhưng ở phân hệ mobile chứ không phải phân hệ website bạn có thể đọc thêm FR-20 để biết thêm thông tin.

### AI Output Summary
Phân tích đặc tả FR-10 (Order State Machine) kết hợp FR-20 (Tính năng Mobile), áp dụng Domain Testing và Boundary Value Analysis cho phân hệ Mobile. Ban đầu sinh 30 test case bao gồm cả kiểm thử API, sau đó được chỉnh sửa trong Interaction 006.

### Human Review
Accepted:
Modified: Yêu cầu bỏ các test case hướng API, chỉ giữ UI testing.
Rejected:

## Interaction 006

### AI Tool
Antigravity (Claude Opus 4.6 Thinking)

### Date & Time
06/28/2026 10:07 PM

### Prompt
Hiện tại test case có một số cái đang hướng đến test API nhưng với phân hệ mobile thì không cần, test UI thôi bạn hãy sửa lại và có thể bỏ bớt các test case test API đi update cả domain-testing report.

### AI Output Summary
Chỉnh sửa bộ test case FR-10 Mobile từ 30 xuống 22 test case, chỉ giữ kiểm thử giao diện (UI Testing). Xóa 8 test case API-focused: hủy đơn người khác qua API, JWT Token hết hạn, BVA order_id (0, 1, 2, 999999, "abc"), API validation. Sửa 6 test case (TC-003, 004, 005, 012, 013, 020) bỏ đề cập API, chỉ giữ kiểm tra UI. Đánh lại số liên tục 001→022. Loại bỏ BVA cho order_id (thuộc phạm vi API), giữ BVA cho biên trạng thái (pending/confirmed vs shipping). Cập nhật docs/domain-testing-report.md ghi rõ phạm vi chỉ UI testing.

### Human Review
Accepted:
Modified:
Rejected:

