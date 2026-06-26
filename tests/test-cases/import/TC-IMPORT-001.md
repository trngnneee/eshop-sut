# TC-IMPORT-001: Import thành công file CSV hợp lệ gồm nhiều dòng sản phẩm

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Equivalence Partitioning (Valid Class)

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
| name | price | description | imageUrl | category_id |
| :--- | :--- | :--- | :--- | :--- |
| "Sản phẩm A" | 150000 | "Mô tả A" | "http://image.url/a.png" | 1 |
| "Sản phẩm B" | 200000 | "Mô tả B" | "http://image.url/b.png" | 1 |

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Gọi API POST `/api/admin/import-products` với payload chứa danh sách sản phẩm hợp lệ trên.

## Expected result
- Hệ thống thực hiện import thành công toàn bộ sản phẩm.
- Trả về HTTP 200 OK và danh sách thông báo thành công.

## Status / Related bugs
Pass / None
