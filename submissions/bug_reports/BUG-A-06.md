---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Auth / Register] Server crash (500) khi nhận body text/plain hoặc thiếu Content-Type'
labels: ['bug', 'API-testing', 'found-by: test-case']
---

## Found by Test Case

TC-A-DP-19, TC-A-SEC-09

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
2. Thiết lập header: `Content-Type: text/plain` hoặc không truyền header `Content-Type`.
3. Kèm header `X-Student-Id: 23127486`.
4. Truyền request body dạng plain text `name=User&email=a@b.com`.

## Expected result

Server xử lý ngoại lệ graceful, từ chối định dạng dữ liệu không được hỗ trợ bằng mã trạng thái HTTP `400 Bad Request` hoặc `415 Unsupported Media Type`, không làm sập hoặc crash server.

## Actual result

Server phát sinh ngoại lệ không được bắt (`TypeError` / unhandled exception khi truy cập thuộc tính của `req.body`) và trả về HTTP `500 Internal Server Error`.

## Evidence

- File Newman HTML Report: `newman_reports/newman_api1_report.html`
- Failed Test Cases: `TC-A-DP-19`, `TC-A-SEC-09`

## GitHub Issue

- [https://github.com/trngnneee/eshop-sut/issues/475](https://github.com/trngnneee/eshop-sut/issues/475) (#475)
