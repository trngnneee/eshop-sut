# TC-IMPORT-031: Từ chối khi price chứa mã độc XSS

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Security Testing

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
Dòng sản phẩm có name: "SP1", price chứa `<script>alert('XSS_price')</script>`, description: "Mô tả", imageUrl: "", category_id: 1

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Tải lên file CSV chứa dòng sản phẩm có price chứa mã độc XSS.
3. Nhấn nút "Import".

## Expected result
- Hệ thống từ chối áp dụng, báo lỗi giá trị không hợp lệ. Trả về HTTP 400 Bad Request.

## Status / Related bugs
Fail / [BUG-IMPORT-021](../../bug-reports/BUG-IMPORT-021.md)
