---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][GUI] Thiếu chỉ báo tải dữ liệu (loading indicator) khi bảng Lịch sử đơn hàng đang tải thông tin'
labels: ['type: bug', 'found-by: gui-checklist']
---

## Found by GUI Checklist Item / Usability Testing Session

IA-04-09: Hiển thị chỉ báo loading (spinner hoặc chữ "Đang tải...") khi dữ liệu đơn hàng đang được tải từ server.

## Requirement liên quan

FR-11: Order history view (user) (tham khảo các fr trong [2026.HW03.GUI Usability_En.md](../../requirements/2026.HW03.GUI%20Usability_En.md) )

## Severity / Priority

- **Severity**: Minor
- **Priority**: P2

## Environment

- **OS**: Windows 11
- **Browser**: Chrome (Mặc định)

## Steps to reproduce

1. Đăng nhập tài khoản khách hàng có nhiều đơn hàng.
2. Vào trang Profile và quan sát bảng đơn hàng ngay khi trang vừa tải (hoặc giả lập mạng chậm).

## Expected result

Phải có spinner hoặc chữ "Đang tải dữ liệu đơn hàng..." để thông báo cho người dùng biết hệ thống đang xử lý.

## Actual result

Bảng trống trơn không có thông tin gì trong 0.5s - 1s đầu trước khi đơn hàng xuất hiện.

## Evidence

![BUG-08 Screenshot](../screenshots/6,8,9-chrome.png)
