---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Apply Coupon] Endpoint apply-coupon không bắt buộc JWT và không bind user theo token'
labels: ['type: bug', 'status: new', 'found-by: test-case', 'security']
assignees: ''
---

## Found by Test Case

`TC-APPLY-COUPON-SEC-003`, `TC-APPLY-COUPON-SEC-004`

## Requirement liên quan

FR-09, SEC-02

## Severity / Priority

Critical / P0

## Environment

- **OS**: Windows
- **Browser**: N/A
- **URL**: `http://localhost:3000/api/apply-coupon`
- **Build/Commit**: Local HW6 EShop SUT

## Steps to reproduce

1. Khởi động backend tại `http://localhost:3000`.
2. Gửi `POST /api/apply-coupon` với coupon `SAVE10`, `total_amount` đủ điều kiện và `user_id=1` nhưng không gửi header `Authorization`.
3. Gửi lại request với JWT hợp lệ của user test nhưng body cố tình dùng `user_id=2`.
4. Kiểm tra status code và response trong Newman report `API-testing/apply-coupon-report.html`.

## Expected result

Theo FR-09 điều kiện C4, người dùng phải có JWT Token hợp lệ khi áp dụng coupon.

- Request không có JWT phải bị từ chối bằng `401 Unauthorized`.
- Request có token của user này nhưng body dùng `user_id` khác phải bị từ chối bằng `403 Forbidden`, hoặc backend phải bỏ qua `user_id` từ client và chỉ dùng user id trong JWT.
- API không được áp dụng coupon thành công cho user không được xác thực hoặc user khác với token.

## Actual result

Endpoint vẫn trả `200 OK` và response áp dụng coupon thành công:

- `TC-APPLY-COUPON-SEC-003`: expected `401` nhưng actual là `200`.
- `TC-APPLY-COUPON-SEC-004`: expected `403` nhưng actual là `200`.

Điều này cho thấy `/api/apply-coupon` chưa dùng middleware xác thực JWT và còn tin `user_id` do client gửi trong body.

## Link Github Issue

N/A
