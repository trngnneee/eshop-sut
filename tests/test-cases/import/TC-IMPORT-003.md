# TC-IMPORT-003: Từ chối import khi file CSV thiếu dòng Header đầu tiên

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
Dữ liệu bắt đầu ngay bằng:
`Sản phẩm A,150000,Mô tả A,http://image.url/a.png,1` (không có dòng header)

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Tải lên file CSV không có dòng header định nghĩa trường.

## Expected result
- Hệ thống từ chối import và trả về HTTP 400.
- Báo lỗi dòng Header không hợp lệ hoặc thiếu cột bắt buộc.

## Status / Related bugs
Fail / [BUG-IMPORT-003](../../bug-reports/BUG-IMPORT-003.md)
