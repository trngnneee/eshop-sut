---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Usability] Kích thước phông chữ hiển thị trong bảng xem trước (preview table) quá nhỏ, gây khó đọc'
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

1. Upload file CSV bất kỳ lên vùng Import sản phẩm.
2. Quan sát bảng dữ liệu xem trước hiển thị ngay bên dưới.

## Expected result

Cỡ chữ trong bảng xem trước phải đồng nhất với cỡ chữ của bảng danh sách sản phẩm chính để đảm bảo khả năng đọc tốt.

## Actual result

Cỡ chữ trong bảng xem trước nhỏ hơn đáng kể so với cỡ chữ tiêu chuẩn của trang web.

## Evidence

![BUG-14 Screenshot](../screenshots/admin_users.png)
- Video minh chứng (Session 1 - Võ Ngọc Bích Trâm): [Link Drive Video Session 1](https://drive.google.com/file/d/1_eDBRoShbDevvvGxupqKQ7pgHaDXcCv6/view?usp=drive_link)
