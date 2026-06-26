# TC-IMPORT-011: Từ chối import khi file CSV trống (0 dòng dữ liệu)

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Boundary Value Analysis (Boundary value)

## Preconditions
- Admin đăng nhập và lấy JWT token.

## Test data
Chỉ có dòng Header:
`name,price,description,imageUrl,category_id` (không có dữ liệu phía dưới)

## Test steps
1. Admin đăng nhập và lấy JWT token.
2. Gọi API POST `/api/admin/import-products` với file CSV trống.

## Expected result
- Hệ thống từ chối import và trả về HTTP 400.
- Hiển thị thông báo lỗi: "Không có dữ liệu để import".

## Status / Related bugs
Fail / [BUG-IMPORT-003](../../bug-reports/BUG-IMPORT-003.md)
