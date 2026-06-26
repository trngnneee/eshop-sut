# TC-IMPORT-010: Hỗ trợ dấu phẩy bọc trong dấu nháy kép đúng chuẩn RFC 4180

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Equivalence Partitioning (Valid Class)

## Preconditions
- Admin đăng nhập và lấy JWT token.

## Test data
File CSV chứa chuỗi bọc trong dấu nháy kép:
`"Sản phẩm, đặc biệt",150000,"Mô tả",http://image.url/a.png,1`

## Test steps
1. Admin đăng nhập và lấy JWT token.
2. Gọi API POST `/api/admin/import-products` với dữ liệu chứa dấu phẩy được bọc nháy kép.

## Expected result
- Hệ thống import thành công.
- Sản phẩm lưu vào CSDL có tên đầy đủ là: `Sản phẩm, đặc biệt`.

## Status / Related bugs
Fail / [BUG-IMPORT-006](../../bug-reports/BUG-IMPORT-006.md)
