# TC-CART-073: Mở 2 tab, tab A xóa sản phẩm, tab B vẫn đang ở giỏ hàng

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Đã có sản phẩm trong giỏ hàng.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
Không có

## Test steps
1. Mở song song 2 tab trình duyệt cùng truy cập giỏ hàng /cart của tài khoản hiện tại.
2. Ở tab A: Nhấn nút xóa sản phẩm.
3. Ở tab B: F5 hoặc nhấn nút tương tác bất kỳ gửi request lên server.


## Expected result
- Tab B khi reload/fetch lại không còn sản phẩm đã xóa

## Status / Related bugs
Pass / None
