---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Usability] Vị trí khu vực Import sản phẩm từ CSV chưa đủ nổi bật, gây khó tìm đối với người dùng mới'
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

1. Đăng nhập Admin và chuyển sang trang Quản lý sản phẩm.
2. Cố gắng tìm khu vực upload file CSV để nhập sản phẩm.

## Expected result

Khu vực Import CSV cần được đóng khung riêng biệt, có nhãn rõ ràng hoặc đặt tại góc trên cùng với phong cách thiết kế nổi bật để người dùng dễ định vị.

## Actual result

Vị trí nút và vùng upload nằm lẫn lộn với thanh tìm kiếm và bộ lọc sản phẩm, không có tiêu đề phân biệt rõ ràng.

## Evidence

![BUG-12 Screenshot](../screenshots/admin_users.png)
- Video minh chứng (Session 5 - Trương Lý Khải): [Link Drive Video Session 5](https://drive.google.com/file/d/13LPt6ndcqLb8iYGL18GO2cGp5EN0PVoh/view?usp=drive_link)
