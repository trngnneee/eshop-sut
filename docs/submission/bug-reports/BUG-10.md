---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Usability] Chức năng Import CSV không thực hiện rollback giao dịch khi có dòng dữ liệu bị lỗi (Không đảm bảo tính nguyên tử)'
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

1. Đăng nhập Admin (`admin@eshop.com` / `Admin123!`) tại `http://localhost:5174/`.
2. Vào trang Quản lý sản phẩm, chọn upload file chứa dòng lỗi `import_i.csv`.
3. Nhấn nút "Import sản phẩm".
4. Kéo xuống danh sách sản phẩm bên dưới để kiểm tra.

## Expected result

Hệ thống phải rollback toàn bộ giao dịch và hiển thị thông báo lỗi, không thêm bất kỳ sản phẩm nào từ file CSV nếu có bất kỳ dòng nào bị lỗi.

## Actual result

Dòng sản phẩm hợp lệ thứ nhất vẫn được thêm vào danh sách hiển thị, hệ thống không rollback giao dịch.

## Evidence

![BUG-10 Screenshot](../screenshots/admin_users.png)
- Video minh chứng (Session 1 - Võ Ngọc Bích Trâm): [Link Drive Video Session 1](https://drive.google.com/file/d/1_eDBRoShbDevvvGxupqKQ7pgHaDXcCv6/view?usp=drive_link)
