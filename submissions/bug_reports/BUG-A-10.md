---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Auth / Register] Không validate email @domain.com (thiếu local-part)'
labels: ['bug', 'API-testing', 'found-by: test-case']
---

## Found by Test Case

TC-A-EXT-11

## Requirement liên quan

FR-01 (Đăng ký tài khoản)

## Severity / Priority

Minor / P2

## Environment

- **OS**: Windows 11 / Ubuntu 22.04 LTS (CI)
- **Browser**: N/A (API Testing via Newman 6.2.2 / Postman Runtime)
- **URL**: http://localhost:3000/api/register
- **Build/Commit**: 26c42a637081edec1344b40665812c4ee7357160

## Steps to reproduce

1. Gửi request `POST` đến `http://localhost:3000/api/register`.
2. Thiết lập header: `Content-Type: application/json` và `X-Student-Id: 23127486`.
3. Truyền request body chứa email thiếu phần local-part (chỉ bắt đầu bằng `@domain.com`):
   `{"name":"User A","email":"@domain.com","password":"Pass123!"}`.

## Expected result

API từ chối request với mã trạng thái HTTP `400 Bad Request` do email không tuân thủ định dạng RFC 5321 (bắt buộc phải có local-part trước ký tự `@`).

## Actual result

API phản hồi mã trạng thái HTTP `200 OK` và tạo tài khoản thành công với email `@domain.com`.

## Evidence

- File Newman HTML Report: `newman_reports/newman_api1_report.html`
- Failed Test Case: `TC-A-EXT-11`

## GitHub Issue

- [https://github.com/trngnneee/eshop-sut/issues/479](https://github.com/trngnneee/eshop-sut/issues/479) (#479)
