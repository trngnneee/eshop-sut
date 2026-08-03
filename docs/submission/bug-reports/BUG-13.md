---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Usability] Giao diện Import CSV thiếu nút xóa/hủy file đã chọn hoặc kết quả import cũ'
labels: ['type: bug', 'found-by: usability-session']
---

## Found by GUI Checklist Item / Usability Testing Session

Usability Testing Session - Task "Import CSV"

## Requirement liên quan

FR-16: Product import from CSV (tham khảo các fr trong [2026.HW03.GUI Usability_En.md](../../requirements/2026.HW03.GUI%20Usability_En.md) )

## Severity / Priority

- **Severity**: Minor
- **Priority**: P2

## Environment

- **OS**: Windows 11
- **Browser**: Chrome (Mặc định)

## Steps to reproduce

1. Thực hiện upload và import file lỗi `import_i.csv`.
2. Cố gắng dọn dẹp hoặc xóa thông báo lỗi để chuẩn bị thực hiện lần import tiếp theo.

## Expected result

Cần có nút đóng hộp thông báo lỗi (nút `x`) và nút "Hủy" hoặc "Xóa" file đã chọn bên cạnh tên file.

## Actual result

Không có phần tử giao diện nào hỗ trợ xóa thông báo lỗi hoặc hủy file đã chọn. Người dùng buộc phải upload đè file mới lên.

## Evidence

![BUG-13 Screenshot](../screenshots/admin_users.png)
- Video minh chứng (Session 5 - Trương Lý Khải): [Link Drive Video Session 5](https://drive.google.com/file/d/13LPt6ndcqLb8iYGL18GO2cGp5EN0PVoh/view?usp=drive_link)
