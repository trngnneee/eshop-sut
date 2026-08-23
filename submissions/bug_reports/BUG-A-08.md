---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Auth / Register] Chấp nhận JSON null cho name/email/password'
labels: ['bug', 'API-testing', 'found-by: test-case']
---

## Found by Test Case

TC-A-EXT-07, TC-A-EXT-08, TC-A-EXT-09

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
3. Truyền request body chứa giá trị `null` đối với các trường bắt buộc (kiểu dữ liệu JSON `null`):
   - Payload 1 (null email): `{"name":"User A","email":null,"password":"Pass123!"}`
   - Payload 2 (null name): `{"name":null,"email":"nullname@test.com","password":"Pass123!"}`
   - Payload 3 (null password): `{"name":"User A","email":"nullpwd@test.com","password":null}`

## Expected result

API từ chối request với mã trạng thái HTTP `400 Bad Request` và thông báo lỗi các trường bắt buộc không được mang giá trị `null` và phải là kiểu chuỗi hợp lệ.

## Actual result

API phản hồi mã trạng thái HTTP `200 OK`, xử lý giá trị `null` như dữ liệu hợp lệ và đăng ký tài khoản thành công.

## Evidence

- File Newman HTML Report: `newman_reports/newman_api1_report.html`
- Failed Test Cases: `TC-A-EXT-07`, `TC-A-EXT-08`, `TC-A-EXT-09`

## GitHub Issue

- [https://github.com/trngnneee/eshop-sut/issues/477](https://github.com/trngnneee/eshop-sut/issues/477) (#477)
