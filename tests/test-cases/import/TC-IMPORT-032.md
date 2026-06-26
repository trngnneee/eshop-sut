# TC-IMPORT-032: Từ chối khi category_id chứa mã độc XSS

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Security Testing

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
Dòng sản phẩm có name: "SP1", price: 100000, description: "Mô tả", imageUrl: "", category_id chứa `<script>alert('XSS_cat')</script>`

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Tải lên file CSV chứa dòng sản phẩm có category_id chứa mã độc XSS.
3. Nhấn nút "Import".

## Expected result
- Hệ thống từ chối áp dụng, báo lỗi danh mục không hợp lệ. Trả về HTTP 400 Bad Request.

## Status / Related bugs
Fail / [BUG-IMPORT-022](../../bug-reports/BUG-IMPORT-022.md)
