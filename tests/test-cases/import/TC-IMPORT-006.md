# TC-IMPORT-006: Từ chối import khi có dòng sản phẩm có price bằng 0

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Boundary Value Analysis (Boundary value)

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
| name | price | description | imageUrl | category_id |
| :--- | :--- | :--- | :--- | :--- |
| "Sản phẩm A" | 0 | "Mô tả A" | "http://image.url/a.png" | 1 |

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Gọi API POST `/api/admin/import-products` với dòng sản phẩm có `price = 0`.

## Expected result
- Hệ thống từ chối import và trả về HTTP 400.
- Thông báo lỗi chi tiết dòng bị lỗi (Giá sản phẩm phải là số thực dương).

## Status / Related bugs
Fail / [BUG-IMPORT-005](../../bug-reports/BUG-IMPORT-005.md)
