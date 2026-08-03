---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][GUI] Trang Admin xóa tài khoản người dùng trực tiếp mà không có hộp thoại xác nhận (Confirm Dialog)'
labels: ['type: bug', 'found-by: gui-checklist']
---

## Found by GUI Checklist Item / Usability Testing Session

IA-04-10: Hiển thị hộp thoại xác nhận (Confirm Dialog) trước khi thực hiện xóa người dùng ở phân hệ Admin.

## Requirement liên quan

FR-19: User management (admin) (tham khảo các fr trong [2026.HW03.GUI Usability_En.md](../../requirements/2026.HW03.GUI%20Usability_En.md) )

## Severity / Priority

- **Severity**: Major
- **Priority**: P1

## Environment

- **OS**: Windows 11
- **Browser**: Chrome (Mặc định)

## Steps to reproduce

1. Đăng nhập Admin (`admin@eshop.com` / `Admin123!`) tại `http://localhost:5174/`.
2. Chọn tab "Người dùng" trên thanh sidebar để xem danh sách.
3. Nhấn vào nút "Xóa" tại hàng của một người dùng bất kỳ.

## Expected result

Phải hiển thị hộp thoại xác nhận (Confirm Dialog) để xác thực hành động xóa tài khoản.

## Actual result

Người dùng bị xóa ngay lập tức khỏi bảng danh sách.

## Evidence

![BUG-09 Screenshot](../screenshots/6,8,9-chrome.png)
