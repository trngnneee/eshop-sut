# TC-PRODUCT-SUP-007: Backend từ chối payload không hợp lệ (server-side validation)

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Domain Testing – Supplementary

## Preconditions
- Backend API đang chạy
- Admin JWT hợp lệ

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Case A | name = 256 ký tự `A`, price = 100000, category_id = 1 |
| Case B | name = Valid, price = 0, category_id = 1 |

## Test steps
1. Gửi `POST /api/products` (admin JWT) với Tên 256 ký tự.
2. Gửi `POST /api/products` (admin JWT) với Giá = 0.
3. Đọc mã trạng thái từng response.

## Expected result
- Cả hai request đều bị từ chối (4xx).
- Backend validate đồng bộ với ràng buộc FR-15 (max 255 ký tự; Giá > 0).

## Sub-domains covered
GAP-05 — server-side validation

## Type
Invalid

## Status / Related bugs
Fail / #17
