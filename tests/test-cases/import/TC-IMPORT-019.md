# TC-IMPORT-019: Từ chối khi description chứa dấu phẩy không bọc nháy kép

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Equivalence Partitioning (Invalid Class - Vi phạm RFC 4180)

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
Dòng sản phẩm có description chứa dấu phẩy nhưng không được bọc nháy kép (Ví dụ: `name,price,description,imageUrl,category_id\nSP1,100,Mô tả, có dấu phẩy,,1`)

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Tải lên file CSV chứa mô tả có dấu phẩy không bọc nháy kép.
3. Nhấn nút "Import".

## Expected result
- Hệ thống nhận diện sai số lượng cột, từ chối toàn bộ file, thực hiện rollback CSDL và báo lỗi cấu trúc dòng không hợp lệ. Trả về HTTP 400 Bad Request.

## Status / Related bugs
Fail / [BUG-IMPORT-012](../../bug-reports/BUG-IMPORT-012.md)
