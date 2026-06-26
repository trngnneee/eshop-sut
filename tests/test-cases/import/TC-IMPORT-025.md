# TC-IMPORT-025: Kiểm tra rollback CSDL khi dòng thứ 3 bị lỗi price âm

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Equivalence Partitioning (Invalid Class - Tính nguyên tử)

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
File CSV gồm 3 dòng: Dòng 1 hợp lệ, Dòng 2 hợp lệ, Dòng 3 lỗi (price âm `-100`).

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Tải lên file CSV có 3 dòng sản phẩm nêu trên.
3. Nhấn nút "Import".

## Expected result
- Hệ thống từ chối import toàn bộ, rollback CSDL (không lưu bất kỳ sản phẩm nào, đảm bảo dòng 1 và dòng 2 không bị lưu dở dang). Trả về HTTP 400 Bad Request.

## Status / Related bugs
Fail / [BUG-IMPORT-001](../../bug-reports/BUG-IMPORT-001.md)
