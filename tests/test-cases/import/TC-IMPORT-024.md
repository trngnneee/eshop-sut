# TC-IMPORT-024: Xử lý tệp CSV có chứa dòng trống ở giữa hoặc ở cuối tệp

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Equivalence Partitioning (Invalid/Valid Class)

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
Tệp CSV có chứa các dòng trống xen kẽ hoặc ở dòng cuối.

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Tải lên file CSV có chứa dòng trống ở giữa hoặc cuối tệp.
3. Nhấn nút "Import".

## Expected result
- Hệ thống tự động bỏ qua dòng trống hoặc từ chối áp dụng và thực hiện rollback theo quy tắc nguyên tử để không sinh dữ liệu rác. Trả về HTTP 400 (hoặc HTTP 200 nếu bỏ qua an toàn).

## Status / Related bugs
Fail / [BUG-IMPORT-017](../../bug-reports/BUG-IMPORT-017.md)
