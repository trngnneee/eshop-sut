---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Auth / Register] Không enforce giới hạn độ dài name (max 255)'
labels: ['bug', 'API-testing', 'found-by: test-case']
---

## Found by Test Case

TC-A-DP-15

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
3. Truyền request body chứa trường `name` có độ dài 256 ký tự (vượt giới hạn quy định 255 ký tự): `{"name":"A...[256 ký tự]...","email":"name256@test.com","password":"Pass123!"}`.

## Expected result

API từ chối request với mã trạng thái HTTP `400 Bad Request` và thông báo lỗi trường `name` vượt quá độ dài tối đa 255 ký tự.

## Actual result

API phản hồi mã trạng thái HTTP `200 OK` và lưu trữ người dùng với tên có độ dài 256 ký tự vào cơ sở dữ liệu.

## Evidence

- File Newman HTML Report: `newman_reports/newman_api1_report.html`
- Failed Test Case: `TC-A-DP-15`

## GitHub Issue

- [https://github.com/trngnneee/eshop-sut/issues/473](https://github.com/trngnneee/eshop-sut/issues/473) (#473)
