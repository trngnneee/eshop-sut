# TC-IMPORT-009: Kiểm tra tính nguyên tử (Atomicity): Rollback toàn bộ import khi có ít nhất một dòng bị lỗi

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Equivalence Partitioning (Invalid Class)

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
Dòng 1: Hợp lệ (`Sản phẩm A`, `150000`)
Dòng 2: Lỗi (`name` bị rỗng)
Dòng 3: Hợp lệ (`Sản phẩm C`, `250000`)

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Truy vấn số lượng sản phẩm hiện tại trong CSDL.
3. Gọi API POST `/api/admin/import-products` với payload 3 dòng trên.
4. Truy vấn lại CSDL sản phẩm để xác minh xem có bất kỳ sản phẩm nào từ payload được lưu hay không.

## Expected result
- Hệ thống từ chối import toàn bộ file và trả về HTTP 400.
- Không có sản phẩm nào (kể cả Dòng 1 và Dòng 3) được ghi nhận vào CSDL (Rollback thành công).

## Status / Related bugs
Fail / [BUG-IMPORT-001](../../bug-reports/BUG-IMPORT-001.md)
