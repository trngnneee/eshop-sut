# TC-IMPORT-017: Từ chối khi name hoặc price chứa lệnh SQL Injection

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Security Testing

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
Dòng sản phẩm có name hoặc price chứa lệnh SQLi (Ví dụ: `"' OR 1=1 --"`)

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Tải lên file CSV chứa dòng sản phẩm có name hoặc price chứa SQL Injection.
3. Nhấn nút "Import".

## Expected result
- Hệ thống từ chối áp dụng, báo lỗi dữ liệu không hợp lệ và xử lý chuỗi an toàn, không thực thi lệnh SQL. Trả về HTTP 400 Bad Request.

## Status / Related bugs
Fail / [BUG-IMPORT-010](../../bug-reports/BUG-IMPORT-010.md)
