# TC-IMPORT-026: Import tệp CSV thành công hoàn toàn và hiển thị báo cáo

## Requirement ID
FR-16: Import Sản phẩm từ CSV

## Module / Test type / Technique
Import / Functional / Equivalence Partitioning (Valid Class)

## Preconditions
- Admin đăng nhập hệ thống và lấy JWT token.

## Test data
Tệp CSV gồm các sản phẩm hoàn toàn hợp lệ.

## Test steps
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Tải lên file CSV chứa các dòng sản phẩm hợp lệ.
3. Nhấn nút "Import".

## Expected result
- Import tệp CSV thành công hoàn toàn. Hệ thống hiển thị báo cáo chi tiết chính xác trên giao diện hoặc phản hồi: số dòng thành công bằng tổng số dòng dữ liệu, số dòng lỗi bằng 0. Trả về HTTP 200 OK.

## Status / Related bugs
Pass / None
