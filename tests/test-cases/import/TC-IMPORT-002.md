# TC-IMPORT-002: Từ chối import file có phần mở rộng khác .csv

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
File đính kèm: `products.txt` hoặc `products.xlsx`.

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Tải lên file có định dạng khác `.csv` (Ví dụ: `.txt`).

## Expected result
- Hệ thống từ chối import và hiển thị thông báo lỗi định dạng file không hợp lệ.
- Trả về HTTP 400 Bad Request.

## Status / Related bugs
Fail / [BUG-IMPORT-002](../../bug-reports/BUG-IMPORT-002.md)
