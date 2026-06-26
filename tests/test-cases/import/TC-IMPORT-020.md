# TC-IMPORT-020: Từ chối import khi price để trống hoàn toàn

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
Dòng sản phẩm có price để trống (Ví dụ: `SP1,,Mô tả,,1`)

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Tải lên file CSV chứa sản phẩm có trường price để trống.
3. Nhấn nút "Import".

## Expected result
- Hệ thống từ chối toàn bộ file, thực hiện rollback CSDL và báo lỗi dòng X thiếu trường giá sản phẩm. Trả về HTTP 400 Bad Request.

## Status / Related bugs
Fail / [BUG-IMPORT-013](../../bug-reports/BUG-IMPORT-013.md)
