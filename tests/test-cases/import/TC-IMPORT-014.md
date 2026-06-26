# TC-IMPORT-014: Import thành công khi name có độ dài bằng 255 ký tự

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Boundary Value Analysis (Valid Class - Biên trên)

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
Dòng sản phẩm có name dài đúng 255 ký tự, price: 100000

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Tải lên file CSV chứa dòng sản phẩm có tên dài đúng 255 ký tự.
3. Nhấn nút "Import".

## Expected result
- Import thành công toàn bộ sản phẩm. Trả về HTTP 200 OK.

## Status / Related bugs
Pass / None
