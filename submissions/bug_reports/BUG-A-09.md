---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Auth / Register] Không validate email XSS payload'
labels: ['bug', 'API-testing', 'found-by: test-case']
---

## Found by Test Case

TC-A-EXT-12

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
3. Truyền request body chứa payload XSS trong trường email:
   `{"name":"User A","email":"<script>alert(1)</script>@test.com","password":"Pass123!"}`.

## Expected result

API từ chối request với mã trạng thái HTTP `400 Bad Request` do email chứa các ký tự đặc biệt nguy hiểm `< >` vi phạm định dạng email tiêu chuẩn và nguy cơ gây Stored XSS.

## Actual result

API phản hồi mã trạng thái HTTP `200 OK`, lưu trữ email chứa payload XSS vào database mà không thực hiện kiểm tra hoặc lọc ký tự nguy hại.

## Evidence

- File Newman HTML Report: `newman_reports/newman_api1_report.html`
- Failed Test Case: `TC-A-EXT-12`

## GitHub Issue

- [https://github.com/trngnneee/eshop-sut/issues/478](https://github.com/trngnneee/eshop-sut/issues/478) (#478)
