---
name: Bug Report
about: Mẫu báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Auth / Register] Cho phép đăng ký email trùng (duplicate)'
labels: ['bug', 'API-testing', 'found-by: test-case']
---

## Found by Test Case

TC-A-DP-17, TC-A-ST-02, TC-A-ST-04

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

1. Gửi request `POST` đến `http://localhost:3000/api/register` với payload `{"name":"User A","email":"existing@domain.com","password":"Pass123!"}` và nhận kết quả tạo tài khoản thành công (`200 OK`).
2. Gửi lại request `POST` đến `http://localhost:3000/api/register` với cùng địa chỉ email `existing@domain.com` đã đăng ký trước đó.
3. Kèm header `Content-Type: application/json` và `X-Student-Id: 23127486`.

## Expected result

API từ chối request đăng ký lần thứ hai, trả về mã trạng thái HTTP `400 Bad Request` hoặc `409 Conflict` kèm thông báo lỗi email đã tồn tại trong hệ thống (vi phạm ràng buộc unique email).

## Actual result

API phản hồi mã trạng thái HTTP `200 OK` và tiếp tục tạo thêm bản ghi người dùng mới với cùng email trùng lặp.

## Evidence

- File Newman HTML Report: `newman_reports/newman_api1_report.html`
- Failed Test Cases: `TC-A-DP-17`, `TC-A-ST-02`, `TC-A-ST-04`

## GitHub Issue

- [https://github.com/trngnneee/eshop-sut/issues/474](https://github.com/trngnneee/eshop-sut/issues/474) (#474)
