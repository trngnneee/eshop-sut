---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Auth / Register] Không validate định dạng email'
labels: ['bug', 'API-testing', 'found-by: test-case']
---

## Found by Test Case

TC-A-DP-06, TC-A-DP-07

## Requirement liên quan

FR-01 (Đăng ký tài khoản)

## Severity / Priority

Major / P1

## Environment

- **OS**: Windows 11 / Ubuntu 22.04 LTS (CI)
- **Browser**: N/A (API Testing via Newman 6.2.2 / Postman Runtime)
- **URL**: http://localhost:3000/api/register
- **Build/Commit**: 26c42a637081edec1344b40665812c4ee7357160

## Steps to reproduce

1. Gửi request `POST` đến `http://localhost:3000/api/register`.
2. Thiết lập header: `Content-Type: application/json` và `X-Student-Id: 23127486`.
3. Truyền request body chứa email không đúng định dạng (thiếu ký tự `@` hoặc thiếu tên miền domain):
   - Payload 1: `{"name":"User A","email":"invalidemail.com","password":"Pass123!"}`
   - Payload 2: `{"name":"User A","email":"user@","password":"Pass123!"}`

## Expected result

API từ chối request với mã trạng thái HTTP `400 Bad Request` và thông báo lỗi định dạng email không hợp lệ (không tuân thủ chuẩn RFC 5321 / RFC 5322).

## Actual result

API phản hồi mã trạng thái HTTP `200 OK` và đăng ký tài khoản thành công với địa chỉ email sai định dạng.

## Evidence

- File Newman HTML Report: `newman_reports/newman_api1_report.html`
- Failed Test Cases: `TC-A-DP-06`, `TC-A-DP-07`

## GitHub Issue

- [https://github.com/trngnneee/eshop-sut/issues/471](https://github.com/trngnneee/eshop-sut/issues/471) (#471)
