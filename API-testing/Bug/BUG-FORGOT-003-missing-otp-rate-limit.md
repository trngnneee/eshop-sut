---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Forgot Password] Endpoint forgot-password không giới hạn tần suất yêu cầu OTP'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`TC-FORGOT-PASSWORD-ST-006`, `TC-FORGOT-PASSWORD-SEC-002`

## Requirement liên quan

FR-03, SEC-07

## Severity / Priority

Major / P1

## Environment

- **OS**: Windows
- **Browser**: N/A
- **URL**: `http://localhost:3000/api/forgot-password`
- **Build/Commit**: Local HW6 EShop SUT

## Steps to reproduce

1. Khởi động backend tại `http://localhost:3000`.
2. Gửi nhiều request `POST /api/forgot-password` liên tiếp cho `test@eshop.com` trong thời gian ngắn.
3. Kiểm tra API có chặn việc sinh thêm OTP sau khi vượt ngưỡng hay không.

## Expected result

Sau quá nhiều lần yêu cầu OTP trong một khoảng thời gian ngắn, API phải trả HTTP `429 Too Many Requests` hoặc một response tương đương thể hiện bị rate limit.

## Actual result

API tiếp tục trả HTTP `200` và tiếp tục sinh OTP. Newman report ghi nhận expected `429` nhưng actual là `200`.

## Link Github Issue

https://github.com/trngnneee/eshop-sut/issues/435#issue-5224600481
