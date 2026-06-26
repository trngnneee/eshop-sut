# TC-IMPORT-013: Từ chối import khi name chỉ chứa khoảng trắng

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
Dòng sản phẩm có name là `"   "`, price: 100000

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Tải lên file CSV chứa dòng sản phẩm có tên chỉ chứa khoảng trắng ("   ").
3. Nhấn nút "Import".

## Expected result
- Hệ thống từ chối import toàn bộ file, thực hiện rollback CSDL. Báo lỗi dòng X có trường name không được để trống. Trả về HTTP 400 Bad Request.

## Status / Related bugs
Fail / [BUG-IMPORT-007](../../bug-reports/BUG-IMPORT-007.md)
