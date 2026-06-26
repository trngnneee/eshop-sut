# TC-IMPORT-029: Từ chối hoặc mã hóa an toàn khi imageUrl chứa mã độc XSS / URL nguy hiểm

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Security Testing

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
Dòng sản phẩm có name: "SP1", price: 100000, description: "Mô tả", imageUrl chứa `"javascript:alert(1)"` hoặc `<script>alert(1)</script>`, category_id: 1

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Tải lên file CSV chứa dòng sản phẩm có imageUrl chứa mã độc XSS.
3. Nhấn nút "Import".

## Expected result
- Hệ thống từ chối áp dụng, báo lỗi dữ liệu không hợp lệ hoặc thực hiện mã hóa an toàn chuỗi trước khi lưu CSDL. Trả về HTTP 400 Bad Request.

## Status / Related bugs
Fail / [BUG-IMPORT-019](../../bug-reports/BUG-IMPORT-019.md)
