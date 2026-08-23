---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Order / My-Orders] Chấp nhận token không có chữ ký (alg: none)'
labels: ['bug', 'API-testing', 'found-by: test-case']
---

## Found by Test Case

TC-B-EXT-02

## Requirement liên quan

FR-11 (Xem lịch sử đơn hàng cá nhân)

## Severity / Priority

Major / P1

## Environment

- **OS**: Windows 11 / Ubuntu 22.04 LTS (CI)
- **Browser**: N/A (API Testing via Newman 6.2.2 / Postman Runtime)
- **URL**: http://localhost:3000/api/orders/my-orders
- **Build/Commit**: 26c42a637081edec1344b40665812c4ee7357160

## Steps to reproduce

1. Gửi request `GET` đến `http://localhost:3000/api/orders/my-orders`.
2. Tạo unsigned JWT token với header `{"alg":"none","typ":"JWT"}` và payload chứa thông tin user bất kỳ không có signature.
3. Truyền header: `Authorization: Bearer <unsigned_jwt_token>` và `X-Student-Id: 23127486`.

## Expected result

Server phải kiểm tra và từ chối token không an toàn (thuật toán none / unsigned token) với mã trạng thái HTTP `401 Unauthorized` do vi phạm tính toàn vẹn xác thực danh tính.

## Actual result

Server không xử lý xác thực chuẩn xác và trả về HTTP `403 Forbidden` thay vì `401 Unauthorized`.

## Evidence

- File Newman HTML Report: `newman_reports/newman_api2_report.html`
- Failed Test Case: `TC-B-EXT-02`

## GitHub Issue

- [https://github.com/trngnneee/eshop-sut/issues/481](https://github.com/trngnneee/eshop-sut/issues/481) (#481)
