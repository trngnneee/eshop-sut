# TC-IMPORT-023: Từ chối import khi tệp CSV hoàn toàn trống (0 bytes)

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Boundary Value Analysis (Invalid Class - Biên dưới)

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
Tệp CSV trống không chứa dữ liệu (0 bytes).

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Tải lên tệp CSV trống hoàn toàn (0 bytes).
3. Nhấn nút "Import".

## Expected result
- Hệ thống từ chối áp dụng, báo lỗi tệp không có dữ liệu. Trả về HTTP 400 Bad Request.

## Status / Related bugs
Fail / [BUG-IMPORT-016](../../bug-reports/BUG-IMPORT-016.md)
