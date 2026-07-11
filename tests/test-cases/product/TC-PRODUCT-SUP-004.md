# TC-PRODUCT-SUP-004: POST /api/products với JWT user thường → 403 (SEC-03)

## Requirement ID
FR-15, FR-12, SEC-03

## Module / Test type / Technique
Admin Product / Security / Domain Testing – Supplementary

## Preconditions
- Tài khoản `test@eshop.com` tồn tại

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Authorization | Bearer {JWT của test@eshop.com} |
| Body | `{ "name": "Hack", "price": 1, "category_id": 1 }` |

## Test steps
1. Lấy JWT của user thường.
2. Gửi `POST /api/products` kèm JWT user.
3. Đọc mã trạng thái HTTP.

## Expected result
- API trả về **403 Forbidden**.
- Sản phẩm không được tạo.

## Sub-domains covered
GAP-02 — JWT không phải admin

## Type
Invalid

## Status / Related bugs
Fail / #16
