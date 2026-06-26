# TC-IMPORT-030: Từ chối khi imageUrl chứa lệnh SQL Injection

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Security Testing

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
Dòng sản phẩm có name: "SP1", price: 100000, description: "Mô tả", imageUrl chứa `"' OR 1=1 --"`, category_id: 1

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Tải lên file CSV chứa dòng sản phẩm có imageUrl chứa SQL Injection.
3. Nhấn nút "Import".

## Expected result
- Hệ thống từ chối áp dụng, báo lỗi dữ liệu không hợp lệ và xử lý chuỗi an toàn. Trả về HTTP 400 Bad Request.

## Status / Related bugs
Fail / [BUG-IMPORT-020](../../bug-reports/BUG-IMPORT-020.md)
