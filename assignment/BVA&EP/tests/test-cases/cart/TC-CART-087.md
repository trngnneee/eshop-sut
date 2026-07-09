# TC-CART-087: Refresh trang ngay sau khi thêm sản phẩm

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Mạng có độ trễ nhẹ.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
Không có

## Test steps
1. Bấm thêm sản phẩm vào giỏ hàng.
2. Nhấn F5 / làm mới trang lập tức khi API phản hồi chưa kết thúc.
3. Kiểm tra xem số lượng và badge giỏ hàng có hiển thị nhất quán hay bị lỗi lệch dữ liệu.


## Expected result
- Giỏ hàng sau refresh vẫn đúng dữ liệu vừa thêm

## Status / Related bugs
Pass / None
