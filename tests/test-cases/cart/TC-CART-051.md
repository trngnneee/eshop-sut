# TC-CART-051: Reload trang /cart sau khi đã thêm sản phẩm

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / State Persistence

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng có một số sản phẩm.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Truy cập trang `/cart` và thấy danh sách sản phẩm hiển thị.
2. Nhấn phím F5 hoặc nút Reload của trình duyệt để tải lại trang.
3. Quan sát bảng giỏ hàng sau khi tải xong.

## Expected result
- Giỏ hàng vẫn duy trì đầy đủ dữ liệu các sản phẩm đã thêm, không bị mất trạng thái hoặc bị reset về rỗng.

## Status / Related bugs
Not Run / None
