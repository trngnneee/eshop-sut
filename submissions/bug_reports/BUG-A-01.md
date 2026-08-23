---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Auth / Register] Không validate input bắt buộc (name, email, password)'
labels: ['bug', 'API-testing', 'found-by: test-case']
---

## Found by Test Case

TC-A-DP-04, TC-A-DP-05, TC-A-DP-08, TC-A-DP-09, TC-A-DP-10, TC-A-DP-11, TC-A-DP-18

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
3. Truyền request body là JSON rỗng `{}` hoặc body có các trường bắt buộc rỗng `{"name":"","email":"","password":""}`, hoặc thiếu bất kỳ trường nào trong 3 trường bắt buộc (`name`, `email`, `password`).

## Expected result

API từ chối request, trả về mã trạng thái HTTP `400 Bad Request` kèm theo thông báo lỗi validation chi tiết xác định trường dữ liệu bắt buộc bị thiếu hoặc không hợp lệ.

## Actual result

API phản hồi mã trạng thái HTTP `200 OK`, chấp nhận dữ liệu rỗng/thiếu và tạo người dùng mới thành công trong cơ sở dữ liệu.

## Evidence

- File Newman HTML Report: `newman_reports/newman_api1_report.html`
- Failed Test Cases: `TC-A-DP-04`, `TC-A-DP-05`, `TC-A-DP-08`, `TC-A-DP-09`, `TC-A-DP-10`, `TC-A-DP-11`, `TC-A-DP-18`

## GitHub Issue

- [https://github.com/trngnneee/eshop-sut/issues/470](https://github.com/trngnneee/eshop-sut/issues/470) (#470)
