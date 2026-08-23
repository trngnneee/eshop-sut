---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Order / My-Orders] Xử lý sai mã lỗi khi dùng Basic auth scheme'
labels: ['bug', 'API-testing', 'found-by: test-case']
---

## Found by Test Case

TC-B-EXT-05

## Requirement liên quan

FR-11 (Xem lịch sử đơn hàng cá nhân)

## Severity / Priority

Minor / P2

## Environment

- **OS**: Windows 11 / Ubuntu 22.04 LTS (CI)
- **Browser**: N/A (API Testing via Newman 6.2.2 / Postman Runtime)
- **URL**: http://localhost:3000/api/orders/my-orders
- **Build/Commit**: 26c42a637081edec1344b40665812c4ee7357160

## Steps to reproduce

1. Gửi request `GET` đến `http://localhost:3000/api/orders/my-orders`.
2. Thiết lập header xác thực sử dụng scheme `Basic` thay vì `Bearer`: `Authorization: Basic dXNlcjpwYXNzd29yZA==`.
3. Kèm header `X-Student-Id: 23127486`.

## Expected result

Server reject scheme xác thực không hỗ trợ hoặc thông tin credentials không đúng chuẩn với mã trạng thái HTTP `401 Unauthorized` (kèm header `WWW-Authenticate: Bearer`).

## Actual result

Server phản hồi mã trạng thái HTTP `403 Forbidden`.

## Evidence

- File Newman HTML Report: `newman_reports/newman_api2_report.html`
- Failed Test Case: `TC-B-EXT-05`

## GitHub Issue

- [https://github.com/trngnneee/eshop-sut/issues/482](https://github.com/trngnneee/eshop-sut/issues/482) (#482)
