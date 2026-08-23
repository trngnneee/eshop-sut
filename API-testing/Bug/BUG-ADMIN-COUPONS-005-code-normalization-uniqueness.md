---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Admin Coupons] Coupon code chưa được normalize trước khi lưu và kiểm tra uniqueness'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`TC-ADMIN-COUPONS-DP-006`, `HT-ADMIN-EXT-004`, `HT-ADMIN-EXT-005`

## Requirement liên quan

FR-17

## Severity / Priority

Major / P1

## Environment

- **OS**: Windows
- **Browser**: N/A
- **URL**: `http://localhost:3000/api/admin/coupons`
- **Build/Commit**: Local HW6 EShop SUT

## Steps to reproduce

1. Khởi động backend tại `http://localhost:3000`.
2. Đăng nhập admin và lấy JWT hợp lệ.
3. Gửi `POST /api/admin/coupons` với `code` chỉ gồm khoảng trắng, có khoảng trắng đầu/cuối như `" TRIMADMIN "`, hoặc khác hoa/thường với seed coupon như `"save10"`.
4. Kiểm tra status và dữ liệu response trong Newman report.

## Expected result

API phải trim/canonicalize coupon code hoặc từ chối input không canonical; không được tạo coupon chỉ khác whitespace/casing với coupon đã có.

## Actual result

Report ghi `HT-ADMIN-EXT-004` trả HTTP `200` và tạo coupon id `59` dù code có khoảng trắng đầu/cuối. `HT-ADMIN-EXT-005` trả HTTP `200` và tạo coupon id `60` cho `save10` dù seed data đã có `SAVE10`. Với `TC-ADMIN-COUPONS-DP-006`, request whitespace còn có thể dẫn đến HTTP `500` do unique constraint ở lần chạy sau.

## Link Github Issue

https://github.com/trngnneee/eshop-sut/issues/491#issue-5227487957
