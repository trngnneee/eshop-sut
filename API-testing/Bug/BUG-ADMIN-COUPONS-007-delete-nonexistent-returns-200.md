---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Admin Coupons] DELETE coupon không tồn tại vẫn trả 200'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`TC-ADMIN-COUPONS-ST-004`, `TC-ADMIN-COUPONS-SV-008`

## Requirement liên quan

FR-17

## Severity / Priority

Major / P1

## Environment

- **OS**: Windows
- **Browser**: N/A
- **URL**: `http://localhost:3000/api/admin/coupons/:id`
- **Build/Commit**: Local HW6 EShop SUT

## Steps to reproduce

1. Khởi động backend tại `http://localhost:3000`.
2. Đăng nhập admin và lấy JWT hợp lệ.
3. Gọi `DELETE /api/admin/coupons/:id` với coupon đã bị xóa trước đó, hoặc với id không tồn tại như `999999`.
4. Kiểm tra HTTP status và response body trong Newman report.

## Expected result

API phải trả HTTP `404 Not Found` với JSON error rõ ràng khi coupon không tồn tại hoặc đã bị xóa; không nên báo thành công cho thao tác không tác động resource nào.

## Actual result

Report `admin-coupons-report.html` ghi các request trên trả HTTP `200` với body `{"message":"Coupon deleted"}`. Cụ thể, `TC-ADMIN-COUPONS-ST-004` expected `404` nhưng actual `200`, và `TC-ADMIN-COUPONS-SV-008` expected `404` nhưng actual `200`. Backend đang không kiểm tra `this.changes` sau câu lệnh DELETE nên không phân biệt xóa thành công với không tìm thấy coupon.

## Link Github Issue

https://github.com/trngnneee/eshop-sut/issues/493#issue-5227642718
