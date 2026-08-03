---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][GUI] Thông báo lỗi nhập liệu Số điện thoại hiển thị qua alert() thay vì thông báo lỗi dưới chân trường nhập'
labels: ['type: bug', 'found-by: gui-checklist']
---

## Found by GUI Checklist Item / Usability Testing Session

IA-02-04: Vị trí các thông báo lỗi biểu mẫu hiển thị gần với trường nhập liệu tương ứng để người dùng dễ nhận biết.

## Requirement liên quan

FR-04: Personal profile management (tham khảo các fr trong [2026.HW03.GUI Usability_En.md](../../requirements/2026.HW03.GUI%20Usability_En.md) )

## Severity / Priority

- **Severity**: Minor
- **Priority**: P2

## Environment

- **OS**: Windows 11
- **Browser**: Chrome (Mặc định)

## Steps to reproduce

1. Vào trang Hồ sơ cá nhân (`http://localhost:5173/profile`).
2. Nhập số điện thoại không đúng định dạng (VD: chứa chữ cái hoặc bắt đầu bằng số 0 do lỗi BUG-02).
3. Nhấn "Cập nhật".

## Expected result

Thông báo lỗi hiển thị động bằng văn bản màu đỏ (inline error message) ngay dưới chân của trường "Số điện thoại" để giữ tính nhất quán giao diện và thân thiện với trải nghiệm.

## Actual result

Trình duyệt bật lên hộp thoại `alert()` hiển thị thông báo lỗi.

## Evidence

![BUG-03 Screenshot](../screenshots/2,3,4,5-chrome.png)
