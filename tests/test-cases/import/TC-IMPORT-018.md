# TC-IMPORT-018: Hệ thống xử lý hoặc từ chối khi header chứa các trường viết hoa

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Equivalence Partitioning (Invalid/Valid Class)

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
Dòng header đầu tiên: `NAME,PRICE,DESCRIPTION,IMAGEURL,CATEGORY_ID`

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Tải lên file CSV có header viết hoa hoàn toàn.
3. Nhấn nút "Import".

## Expected result
- Hệ thống tự động chuẩn hóa về chữ thường để xử lý tiếp hoặc từ chối áp dụng, báo lỗi cấu trúc tệp không hợp lệ. Trả về HTTP 400 (hoặc HTTP 200 nếu chuẩn hóa tốt).

## Status / Related bugs
Fail / [BUG-IMPORT-011](../../bug-reports/BUG-IMPORT-011.md)
