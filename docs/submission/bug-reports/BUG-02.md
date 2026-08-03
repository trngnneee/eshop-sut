---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: "[BUG][GUI] Ràng buộc Regex số điện thoại tại form cập nhật hồ sơ chặn các số điện thoại bắt đầu bằng '0'"
labels: ['type: bug', 'found-by: gui-checklist']
---

## Found by GUI Checklist Item / Usability Testing Session

IA-02-03: Trường số điện thoại giới hạn định dạng và kiểm tra tính hợp lệ khi người dùng nhập sai số chữ số hoặc ký tự lạ.

## Requirement liên quan

FR-04: Personal profile management (tham khảo các fr trong [2026.HW03.GUI Usability_En.md](../../requirements/2026.HW03.GUI%20Usability_En.md) )

## Severity / Priority

- **Severity**: Major
- **Priority**: P1

## Environment

- **OS**: Windows 11
- **Browser**: Chrome (Mặc định)

## Steps to reproduce

1. Đăng nhập cổng người dùng bằng tài khoản `test@eshop.com` / `Test1234!`.
2. Bấm vào tên người dùng ở góc trên bên phải để vào trang Hồ sơ cá nhân (`http://localhost:5173/profile`).
3. Nhập số điện thoại `0987654321` vào trường "Số điện thoại".
4. Bấm nút "Cập nhật".

## Expected result

Cho phép nhập và lưu số điện thoại Việt Nam hợp lệ bắt đầu bằng số `0` (regex nên là `/^0[0-9]{8,9}$/` hoặc `/^[0-9]{9,10}$/`).

## Actual result

Hiển thị hộp thoại cảnh báo (alert): "Số điện thoại không hợp lệ. Vui lòng nhập đúng 9-10 chữ số." và ngăn không gửi yêu cầu lưu lên backend.

## Evidence

![BUG-02 Screenshot](../screenshots/2,3,4,5-chrome.png)
