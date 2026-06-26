# TC-IMPORT-005: Từ chối import khi có dòng sản phẩm có name rỗng

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
| name | price | description | imageUrl | category_id |
| :--- | :--- | :--- | :--- | :--- |
| "" | 150000 | "Mô tả A" | "http://image.url/a.png" | 1 |

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Gọi API POST `/api/admin/import-products` với dòng sản phẩm có trường `name` rỗng.

## Expected result
- Hệ thống từ chối import và trả về HTTP 400.
- Thông báo lỗi chi tiết dòng bị lỗi (Thiếu tên sản phẩm).

## Status / Related bugs
Fail / [BUG-IMPORT-004](../../bug-reports/BUG-IMPORT-004.md)
