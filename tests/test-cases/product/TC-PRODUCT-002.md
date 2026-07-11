# TC-PRODUCT-002: Xem danh sách sản phẩm hiển thị đầy đủ thông tin

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Admin đã đăng nhập vào phân hệ Web Admin
- CSDL có ít nhất một sản phẩm

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Chức năng | Xem danh sách sản phẩm |

## Test steps
1. Mở chức năng Quản lý Sản phẩm (FR-15).
2. Quan sát danh sách sản phẩm hiển thị trên giao diện.
3. Đối chiếu với dữ liệu sản phẩm đã biết trong hệ thống.

## Expected result
- Danh sách sản phẩm được hiển thị (chức năng Xem — Read).
- Mỗi dòng hiển thị thông tin cốt lõi: Tên, Giá (và Danh mục nếu có cột tương ứng).
- Có đường dẫn hoặc nút thao tác Sửa / Xóa cho từng sản phẩm.

## Sub-domains covered
SD-V01 (xem danh sách — Read)

## Type
Valid

## Status / Related bugs
Fail / #15, #18
