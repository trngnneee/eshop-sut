# TC-PRODUCT-SUP-003: POST /api/products không có JWT → 401 (SEC-02)

## Requirement ID
FR-15, FR-12, SEC-02

## Module / Test type / Technique
Admin Product / Security / Domain Testing – Supplementary

## Preconditions
- Backend API đang chạy

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Authorization | [Không có] |
| Body | `{ "name": "Hack", "price": 1, "category_id": 1 }` |

## Test steps
1. Gửi `POST /api/products` không kèm header `Authorization`.
2. Đọc mã trạng thái HTTP.

## Expected result
- API trả về **401 Unauthorized**.
- Sản phẩm không được tạo.

## Sub-domains covered
GAP-02 — không có JWT

## Type
Invalid

## Status / Related bugs
Fail / #16
