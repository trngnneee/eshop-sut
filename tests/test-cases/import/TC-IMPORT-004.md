# TC-IMPORT-004: Từ chối import khi dòng Header sai tên cột bắt buộc

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
Dòng header: `ten_sp,gia,mo_ta,hinh_anh,danh_muc` (sai chuẩn `name,price,description,imageUrl,category_id`)

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Gọi API POST `/api/admin/import-products` với header cột sai tên.

## Expected result
- Hệ thống từ chối import và trả về HTTP 400.
- Báo lỗi thiếu cột bắt buộc (name, price).

## Status / Related bugs
Fail / [BUG-IMPORT-003](../../bug-reports/BUG-IMPORT-003.md)
