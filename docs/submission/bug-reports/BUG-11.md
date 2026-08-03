---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Usability] Hộp cảnh báo kết quả import hiển thị mâu thuẫn trực quan (Chữ báo lỗi màu đỏ nằm trong khung thông báo thành công màu xanh lá)'
labels: ['type: bug', 'found-by: usability-session']
---

## Found by GUI Checklist Item / Usability Testing Session

Usability Testing Session - Task "Import CSV"

## Requirement liên quan

FR-16: Product import from CSV (tham khảo các fr trong [2026.HW03.GUI Usability_En.md](../../requirements/2026.HW03.GUI%20Usability_En.md) )

## Severity / Priority

- **Severity**: Major
- **Priority**: P1

## Environment

- **OS**: Windows 11
- **Browser**: Chrome (Mặc định)

## Steps to reproduce

1. Đăng nhập Admin và vào mục Quản lý sản phẩm.
2. Upload file `import_i.csv` và bấm "Import sản phẩm".

## Expected result

Khi có lỗi xảy ra hoặc tác vụ chạy không trọn vẹn, hệ thống phải hiển thị hộp thông báo màu đỏ (danger/error alert) để nhất quán về mặt thị giác và cảnh báo đúng trạng thái cho người dùng.

## Actual result

Hộp thông báo có màu nền xanh lá (success) nhưng hiển thị dòng lỗi màu đỏ "Hàng 2: Thiếu tên sản phẩm" bên trong.

## Evidence

![BUG-11 Screenshot](../screenshots/admin_users.png)
- Video minh chứng (Session 2 - Nguyễn Thanh Gia Bảo): [Link Drive Video Session 2](https://drive.google.com/file/d/1ZEw_L40uTdZ-6w9aEDTMiFzY0cWm4kbY/view?usp=drive_link)
