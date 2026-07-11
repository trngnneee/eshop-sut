# TC-PRODUCT-SUP-001: API từ chối category_id không tồn tại

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Domain Testing – Supplementary

## Preconditions
- Backend API đang chạy tại `http://localhost:3000`
- Admin JWT hợp lệ

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Authorization | Bearer {admin JWT} |
| name | Valid API Product |
| price | 100000 |
| category_id | 99999 (không tồn tại) |

## Test steps
1. Đăng nhập admin để lấy JWT.
2. Gửi `POST /api/products` với `category_id: 99999`.
3. Đọc mã trạng thái và response.

## Expected result
- API từ chối tạo sản phẩm (400/404/422).
- Sản phẩm **không** được lưu với danh mục không hợp lệ.

## Sub-domains covered
GAP-01 — category_id không thuộc danh sách có sẵn

## Type
Invalid

## Status / Related bugs
Fail / #17
