# TC-IMPORT-016: Từ chối hoặc mã hóa an toàn khi name chứa mã độc XSS

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Security Testing

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
Dòng sản phẩm có name chứa `<script>alert(1)</script>`, price: 100000

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Tải lên file CSV chứa dòng sản phẩm có tên chứa mã độc XSS.
3. Nhấn nút "Import".

## Expected result
- Hệ thống từ chối áp dụng, báo lỗi dữ liệu không hợp lệ hoặc thực hiện mã hóa an toàn chuỗi trước khi lưu CSDL, không thực thi script. Trả về HTTP 400 Bad Request (hoặc HTTP 200 nếu mã hóa thành công).

## Status / Related bugs
Fail / [BUG-IMPORT-009](../../bug-reports/BUG-IMPORT-009.md)
