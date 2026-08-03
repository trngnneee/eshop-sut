---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][GUI] Thiếu hiệu ứng làm nổi bật hàng (row hover highlight) khi di chuột qua các bảng dữ liệu'
labels: ['type: bug', 'found-by: gui-checklist']
---

## Found by GUI Checklist Item / Usability Testing Session

IA-04-07: Khi di chuột qua các hàng của bảng, hàng tương ứng được làm nổi bật (row hover highlight).

## Requirement liên quan

FR-11: Order history view (user) & FR-19: User management (admin) (tham khảo các fr trong [2026.HW03.GUI Usability_En.md](../../requirements/2026.HW03.GUI%20Usability_En.md) )

## Severity / Priority

- **Severity**: Minor
- **Priority**: P2

## Environment

- **OS**: Windows 11
- **Browser**: Chrome (Mặc định)

## Steps to reproduce

1. Truy cập bảng Lịch sử đơn hàng (User) hoặc bảng danh sách Người dùng (Admin).
2. Rê chuột qua các dòng dữ liệu trong bảng.

## Expected result

Hàng được rê chuột qua phải đổi màu nền nhẹ (ví dụ: xám nhạt hoặc xanh nhạt) để người dùng dễ theo dõi thông tin dòng ngang.

## Actual result

Hàng dữ liệu giữ nguyên màu sắc, không có phản hồi thị giác nào khi rê chuột qua.

## Evidence

![BUG-07 Screenshot](../screenshots/7-chrome.png)
