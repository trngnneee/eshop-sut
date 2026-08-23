---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Admin Coupons] User thường dùng JWT hợp lệ vẫn tạo được coupon admin'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`TC-ADMIN-COUPONS-SEC-005`, `TC-ADMIN-COUPONS-SV-006`

## Requirement liên quan

FR-17, SEC-03

## Severity / Priority

Critical / P0

## Environment

- **OS**: Windows
- **Browser**: N/A
- **URL**: `http://localhost:3000/api/admin/coupons`
- **Build/Commit**: Local HW6 EShop SUT

## Steps to reproduce

1. Khởi động backend tại `http://localhost:3000`.
2. Đăng nhập bằng tài khoản user thường `test@eshop.com / Test1234!`.
3. Dùng JWT của user thường gửi `POST /api/admin/coupons` với body tạo coupon hợp lệ.
4. Kiểm tra HTTP status và response body trong Newman report.

## Expected result

API admin phải kiểm tra role trong JWT và trả HTTP `403 Forbidden`; coupon không được tạo.

## Actual result

Report ghi expected `403` nhưng actual là HTTP `200`; response body là `{"message":"Coupon created","id":48}` hoặc `{"message":"Coupon created","id":55}`. Điều này cho thấy endpoint chỉ xác thực token mà không enforce role admin.

## Link Github Issue

https://github.com/trngnneee/eshop-sut/issues/489#issue-5227473193
