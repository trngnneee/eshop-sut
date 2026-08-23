---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Order / My-Orders] Trả mã lỗi 403 Forbidden thay vì 401 Unauthorized khi token invalid / forged / expired'
labels: ['bug', 'API-testing', 'found-by: test-case']
---

## Found by Test Case

TC-B-DP-06, TC-B-DP-07, TC-B-ST-07, TC-B-SEC-04, TC-B-SEC-05

## Requirement liên quan

FR-11 (Xem lịch sử đơn hàng cá nhân)

## Severity / Priority

Major / P2

## Environment

- **OS**: Windows 11 / Ubuntu 22.04 LTS (CI)
- **Browser**: N/A (API Testing via Newman 6.2.2 / Postman Runtime)
- **URL**: http://localhost:3000/api/orders/my-orders
- **Build/Commit**: 26c42a637081edec1344b40665812c4ee7357160

## Steps to reproduce

1. Gửi request `GET` đến `http://localhost:3000/api/orders/my-orders`.
2. Truyền header xác thực không hợp lệ:
   - Token giả mạo: `Authorization: Bearer invalidfaketoken123`
   - Token đã hết hạn: `Authorization: Bearer <expired_token>`
3. Kèm header `X-Student-Id: 23127486`.

## Expected result

Theo tiêu chuẩn HTTP và REST API, khi xác thực danh tính client không thành công (token sai, giả mạo hoặc hết hạn), server phải trả về mã trạng thái HTTP `401 Unauthorized` để client biết cần thực hiện xác thực lại (re-authenticate).

## Actual result

Server trả về mã trạng thái HTTP `403 Forbidden` (mã trạng thái chỉ dùng khi client đã được xác thực nhưng không có quyền truy cập tài nguyên).

## Evidence

- File Newman HTML Report: `newman_reports/newman_api2_report.html`
- Failed Test Cases: `TC-B-DP-06`, `TC-B-DP-07`, `TC-B-ST-07`, `TC-B-SEC-04`, `TC-B-SEC-05`

## GitHub Issue

- [https://github.com/trngnneee/eshop-sut/issues/480](https://github.com/trngnneee/eshop-sut/issues/480) (#480)
