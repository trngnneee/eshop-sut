# TC-IMPORT-022: Từ chối import khi category_id để trống hoàn toàn

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
Dòng sản phẩm có category_id để trống (Ví dụ: `SP1,100000,Mô tả,,`)

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Tải lên file CSV chứa sản phẩm có category_id để trống.
3. Nhấn nút "Import".

## Expected result
- Hệ thống từ chối toàn bộ file, thực hiện rollback CSDL và báo lỗi dòng X thiếu trường danh mục sản phẩm. Trả về HTTP 400 Bad Request.

## Status / Related bugs
Fail / [BUG-IMPORT-015](../../bug-reports/BUG-IMPORT-015.md)
