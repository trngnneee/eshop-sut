---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Auth / Register] Không enforce password minimum length'
labels: ['bug', 'API-testing', 'found-by: test-case']
---

## Found by Test Case

TC-A-DP-12, TC-A-DP-14

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
3. Truyền request body chứa mật khẩu có độ dài nhỏ hơn 8 ký tự (dưới ngưỡng tối thiểu):
   - Payload 1 (1 ký tự): `{"name":"User A","email":"pw1@test.com","password":"A"}`
   - Payload 2 (7 ký tự): `{"name":"User A","email":"pw7@test.com","password":"Aa1!xxY"}`

## Expected result

API từ chối request với mã trạng thái HTTP `400 Bad Request` cùng thông báo lỗi yêu cầu mật khẩu phải đạt độ dài tối thiểu ít nhất 8 ký tự.

## Actual result

API phản hồi mã trạng thái HTTP `200 OK` và tạo người dùng thành công với mật khẩu không đủ độ dài bảo mật.

## Evidence

- File Newman HTML Report: `newman_reports/newman_api1_report.html`
- Failed Test Cases: `TC-A-DP-12`, `TC-A-DP-14`

## GitHub Issue

- [https://github.com/trngnneee/eshop-sut/issues/472](https://github.com/trngnneee/eshop-sut/issues/472) (#472)
