---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Apply Coupon] Không chặn user đã dùng hết giới hạn coupon'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`TC-APPLY-COUPON-ST-006`

## Requirement liên quan

FR-09

## Severity / Priority

Major / P1

## Environment

- **OS**: Windows
- **Browser**: N/A
- **URL**: `http://localhost:3000/api/apply-coupon`
- **Build/Commit**: Local HW6 EShop SUT

## Steps to reproduce

1. Khởi động backend tại `http://localhost:3000`.
2. Chuẩn bị coupon `SAVE10` có `max_uses_per_user=1`.
3. Gửi request apply-coupon cho `user_id=1` sau khi user này đã dùng hết quota.
4. Kiểm tra HTTP status và response trong Newman report.

## Expected result

API phải trả HTTP `400 Bad Request` và không trả schema thành công, vì user đã đạt giới hạn sử dụng coupon.

## Actual result

Report ghi:

- `expected status list: expected [ 400 ] to include 200`
- `Exceeded per-user usage is rejected: expected -4500000 to equal undefined`

Backend vẫn trả HTTP `200` và response tính giảm giá, nghĩa là quota theo user không được enforce ở endpoint apply-coupon hoặc đang kiểm tra sai trạng thái usage.

## Link Github Issue

https://github.com/trngnneee/eshop-sut/issues/464#issue-5227178980