---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][GUI] Form cập nhật thông tin cá nhân thiếu dấu sao đỏ (*) bắt buộc ở trường "Họ Tên"'
labels: ['type: bug', 'found-by: gui-checklist']
---

## Found by GUI Checklist Item / Usability Testing Session

IA-02-01: Form cập nhật thông tin cá nhân hiển thị dấu sao đỏ ở field "Họ Tên".

## Requirement liên quan

FR-04: Personal profile management (tham khảo các fr trong [2026.HW03.GUI Usability_En.md](../../requirements/2026.HW03.GUI%20Usability_En.md) )

## Severity / Priority

- **Severity**: Minor
- **Priority**: P2

## Environment

- **OS**: Windows 11
- **Browser**: Chrome (Mặc định)

## Steps to reproduce

1. Đăng nhập cổng người dùng bằng tài khoản `test@eshop.com` / `Test1234!`.
2. Bấm vào tên người dùng ở góc trên bên phải để vào trang Hồ sơ cá nhân (`http://localhost:5173/profile`).
3. Quan sát nhãn của trường "Họ Tên".

## Expected result

Nhãn hiển thị dạng "Họ Tên *" hoặc có ký tự màu đỏ biểu thị đây là trường bắt buộc nhập.

## Actual result

Nhãn chỉ hiển thị chữ "Họ Tên" mà không có dấu sao đỏ `*` bên cạnh.

## Evidence

![BUG-01 Screenshot](../screenshots/1-chrome.png)
