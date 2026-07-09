# TC-CART-022: Để trống ô quantity

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / EP - Invalid

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng có sản phẩm A.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Quantity input | `` |

## Test steps
1. Truy cập trang `/cart`.
2. Xóa hết nội dung trong ô số lượng của sản phẩm A (để trống).
3. Nhấn nhấp ra ngoài ô nhập.

## Expected result
- Hành động không hợp lệ. Ô nhập không được để trống.
- Số lượng tự động được phục hồi về giá trị hợp lệ trước đó hoặc hiển thị thông báo lỗi.
- Subtotal và tổng cộng giỏ hàng không bị lỗi hiển thị (như NaN hay trống).

## Status / Related bugs
Fail / BUG-FR07-B-04
