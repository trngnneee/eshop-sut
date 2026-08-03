---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][GUI] Nút điều hướng "Hồ sơ" không được làm nổi bật / khác với các trang khác khi người dùng đang hoạt động tại trang Hồ sơ'
labels: ['type: bug', 'found-by: gui-checklist']
---

## Found by GUI Checklist Item / Usability Testing Session

IA-03-01: Liên kết điều hướng của "Hồ sơ" trên thanh menu người dùng được làm nổi bật khi đang ở trang cá nhân (khác với khi đang ở các trang khác).

## Requirement liên quan

FR-04: Personal profile management (tham khảo các fr trong [2026.HW03.GUI Usability_En.md](../../requirements/2026.HW03.GUI%20Usability_En.md) )

## Severity / Priority

- **Severity**: Minor
- **Priority**: P2

## Environment

- **OS**: Windows 11
- **Browser**: Chrome (Mặc định)

## Steps to reproduce

1. Đăng nhập và truy cập trang Hồ sơ cá nhân (`http://localhost:5173/profile`).
2. Quan sát nút điều hướng "Chào, Test User" ở góc trên bên phải thanh menu và đối chiếu với nút "Trang chủ" hoặc "Giỏ hàng".

## Expected result

Nút điều hướng active phải hiển thị trạng thái nổi bật (highlight) hoặc đổi màu nền/chữ để chỉ ra phân hệ đang hoạt động.

## Actual result

Nút "Chào, Test User" không thay đổi giao diện, hoàn toàn giống với lúc đang ở trang chủ `/`.

## Evidence

![BUG-04 Screenshot](../screenshots/2,3,4,5-chrome.png)
