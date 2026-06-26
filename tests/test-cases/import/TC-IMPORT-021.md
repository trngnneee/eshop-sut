# TC-IMPORT-021: Từ chối import khi category_id không tồn tại trong hệ thống

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
Dòng sản phẩm có category_id là `9999` (không tồn tại trong CSDL)

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Tải lên file CSV chứa sản phẩm có category_id không tồn tại.
3. Nhấn nút "Import".

## Expected result
- Hệ thống từ chối toàn bộ file, thực hiện rollback CSDL và báo lỗi dòng X có danh mục không hợp lệ. Trả về HTTP 400 Bad Request.

## Status / Related bugs
Fail / [BUG-IMPORT-014](../../bug-reports/BUG-IMPORT-014.md)
