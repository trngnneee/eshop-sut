---
name: Bug Report
about: Báo cáo lỗi khi thực hiện test case thất bại
title: '[BUG][Admin Coupons] Token rỗng/sai/hết hạn trả 403 thay vì 401'
labels: ['type: bug', 'status: new', 'found-by: test-case']
assignees: ''
---

## Found by Test Case

`TC-ADMIN-COUPONS-SEC-002`, `TC-ADMIN-COUPONS-SEC-003`, `TC-ADMIN-COUPONS-SEC-004`, `HT-ADMIN-EXT-007`

## Requirement liên quan

FR-17, SEC-02, SEC-03

## Severity / Priority

Minor / P2

## Environment

- **OS**: Windows
- **Browser**: N/A
- **URL**: `http://localhost:3000/api/admin/coupons`
- **Build/Commit**: Local HW6 EShop SUT

## Steps to reproduce

1. Khởi động backend tại `http://localhost:3000`.
2. Gửi `POST /api/admin/coupons` với `Authorization` rỗng, token không phải JWT, JWT hết hạn, hoặc JWT bị sửa payload nhưng signature sai.
3. Kiểm tra status code trong Newman report.

## Expected result

API nên trả HTTP `401 Unauthorized` cho token thiếu/không hợp lệ/hết hạn hoặc token bị tamper, kèm JSON error rõ ràng và không xử lý body tạo coupon.

## Actual result

Report ghi các case trên trả HTTP `403 Forbidden` với body `{"error":"Forbidden"}` trong khi expected là `401`. API đang không phân biệt lỗi authentication với lỗi authorization, làm response contract mơ hồ.

## Link Github Issue

https://github.com/trngnneee/eshop-sut/issues/490#issue-5227481285
