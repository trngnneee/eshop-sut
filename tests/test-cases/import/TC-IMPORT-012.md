# TC-IMPORT-012: Import thành công sản phẩm có giá trị price thực dương tối thiểu

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Boundary Value Analysis (Boundary value)

## Preconditions
- Admin đăng nhập và lấy JWT token.

## Test data
| name | price | description | imageUrl | category_id |
| :--- | :--- | :--- | :--- | :--- |
| "Sản phẩm Giá Tối Thiểu" | 0.01 | "Mô tả" | "http://image.url/min.png" | 1 |

## Test steps
1. Admin đăng nhập và lấy JWT token.
2. Gọi API POST `/api/admin/import-products` với dòng sản phẩm có `price = 0.01`.

## Expected result
- Hệ thống import thành công sản phẩm có giá tối thiểu.
- Trả về HTTP 200 OK.

## Status / Related bugs
Pass / None
