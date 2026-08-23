---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Admin Coupons] Tạo coupon trùng code trả 500 và lộ lỗi SQLite thay vì 409'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`TC-ADMIN-COUPONS-DP-007`, `TC-ADMIN-COUPONS-ST-002`, `HT-ADMIN-EXT-001`

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
3. Gửi `POST /api/admin/coupons` với `code` đã tồn tại trong seed data, ví dụ `SAVE10`, hoặc gửi hai request cùng một `code`.
4. Kiểm tra response trong Newman report.

## Expected result

API phải trả HTTP `409 Conflict` với JSON error nghiệp vụ rõ ràng, không tạo coupon trùng và không lộ chi tiết database.

## Actual result

Report ghi actual status là HTTP `500 Internal Server Error`; response body là `{"error":"SQLITE_CONSTRAINT: UNIQUE constraint failed: coupons.code"}`. Backend đang để lỗi unique constraint rơi ra response thay vì map sang lỗi conflict ổn định.

## Link Github Issue

https://github.com/trngnneee/eshop-sut/issues/469#issue-5227450823
