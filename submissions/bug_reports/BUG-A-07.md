---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Auth / Register] Không sanitize SQL Injection trong email'
labels: ['bug', 'API-testing', 'found-by: test-case']
---

## Found by Test Case

TC-A-SEC-01

## Requirement liên quan

FR-01 (Đăng ký tài khoản)

## Severity / Priority

Critical / P0

## Environment

- **OS**: Windows 11 / Ubuntu 22.04 LTS (CI)
- **Browser**: N/A (API Testing via Newman 6.2.2 / Postman Runtime)
- **URL**: http://localhost:3000/api/register
- **Build/Commit**: 26c42a637081edec1344b40665812c4ee7357160

## Steps to reproduce

1. Gửi request `POST` đến `http://localhost:3000/api/register`.
2. Thiết lập header: `Content-Type: application/json` và `X-Student-Id: 23127486`.
3. Truyền request body chứa payload SQL Injection điển hình trong trường email:
   `{"name":"User","email":"' OR 1=1 --","password":"Pass123!"}`.

## Expected result

API từ chối request với mã trạng thái HTTP `400 Bad Request` do địa chỉ email không hợp lệ và chứa các ký tự/chuỗi cú pháp SQL độc hại, không cho phép lưu payload nguy hiểm vào cơ sở dữ liệu.

## Actual result

API phản hồi mã trạng thái HTTP `200 OK`, chấp nhận chuỗi SQL injection làm địa chỉ email và tạo người dùng thành công.

## Evidence

- File Newman HTML Report: `newman_reports/newman_api1_report.html`
- Failed Test Case: `TC-A-SEC-01`

## GitHub Issue

- [https://github.com/trngnneee/eshop-sut/issues/476](https://github.com/trngnneee/eshop-sut/issues/476) (#476)
