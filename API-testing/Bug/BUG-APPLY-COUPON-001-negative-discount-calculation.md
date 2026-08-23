---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Apply Coupon] Coupon SAVE10 trả discount_amount âm khi áp dụng thành công'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`TC-APPLY-COUPON-DP-001`, `TC-APPLY-COUPON-DP-016`, `TC-APPLY-COUPON-ST-001`, `TC-APPLY-COUPON-ST-007`, `TC-APPLY-COUPON-SEC-005`, `TC-APPLY-COUPON-SEC-006`, `TC-APPLY-COUPON-SEC-009`, `TC-APPLY-COUPON-SV-001`, `TC-APPLY-COUPON-SV-002`, `TC-APPLY-COUPON-SV-003`, `TC-APPLY-COUPON-SV-004`, `HT-APPLY-EXT-001`, `HT-APPLY-EXT-003`, `HT-APPLY-EXT-006`

## Requirement liên quan

FR-09

## Severity / Priority

Critical / P0

## Environment

- **OS**: Windows
- **Browser**: N/A
- **URL**: `http://localhost:3000/api/apply-coupon`
- **Build/Commit**: Local HW6 EShop SUT

## Steps to reproduce

1. Khởi động backend tại `http://localhost:3000`.
2. Gửi `POST /api/apply-coupon` với coupon `SAVE10`, `user_id` hợp lệ và `total_amount` đủ điều kiện áp dụng.
3. Kiểm tra response trong Newman report `API-testing/apply-coupon-report.html`.

## Expected result

API phải trả kết quả tính tiền hợp lệ:

- `discount_amount` là số không âm.
- `discount_amount` không được lớn hơn `total_amount`.
- `final_amount = total_amount - discount_amount`.
- Với coupon percent `SAVE10` có `discount_value=10`, mức giảm phải tương ứng 10% của `total_amount`.

## Actual result

Response thành công có `discount_amount` âm. Report ghi nhiều assertion fail với lỗi:

- `expected -4500000 to be at least +0`
- `SAVE10 percent calculation is exact` fail
- `Money values stay within safe bounds` fail

Điều này cho thấy backend đang tính sai công thức coupon percent hoặc nhầm đơn vị khi tính số tiền giảm.

## Link Github Issue

N/A
