---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Apply Coupon] Không rate limit khi brute-force coupon code'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`TC-APPLY-COUPON-SEC-008`

## Requirement liên quan

FR-09

## Severity / Priority

Major / P2

## Environment

- **OS**: Windows
- **Browser**: N/A
- **URL**: `http://localhost:3000/api/apply-coupon`
- **Build/Commit**: Local HW6 EShop SUT

## Steps to reproduce

1. Khởi động backend tại `http://localhost:3000`.
2. Gửi nhiều request liên tiếp tới `POST /api/apply-coupon` với các coupon code không tồn tại từ cùng client/IP.
3. Kiểm tra HTTP status trong Newman report.

## Expected result

Sau nhiều lần thử coupon sai trong thời gian ngắn, API phải trả HTTP `429 Too Many Requests` hoặc có cơ chế chặn tương đương để hạn chế brute-force coupon code.

## Actual result

Report ghi:

- `expected status list: expected [ 429 ] to include 404`

Backend chỉ tiếp tục trả `404` cho coupon không tồn tại, chưa có dấu hiệu rate limit/chặn brute-force.

## Link Github Issue

https://github.com/trngnneee/eshop-sut/issues/466#issue-5227190957
