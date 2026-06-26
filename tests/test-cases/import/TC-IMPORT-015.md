# TC-IMPORT-015: Từ chối import khi name có độ dài bằng 256 ký tự

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Boundary Value Analysis (Invalid Class - Biên trên lỗi)

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
Dòng sản phẩm có name dài đúng 256 ký tự, price: 100000

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Tải lên file CSV chứa dòng sản phẩm có tên dài đúng 256 ký tự.
3. Nhấn nút "Import".

## Expected result
- Hệ thống từ chối import toàn bộ file, thực hiện rollback CSDL. Báo lỗi dòng X có tên sản phẩm vượt quá 255 ký tự. Trả về HTTP 400 Bad Request.

## Status / Related bugs
Fail / [BUG-IMPORT-008](../../bug-reports/BUG-IMPORT-008.md)
