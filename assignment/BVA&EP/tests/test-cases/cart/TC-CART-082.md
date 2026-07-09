# TC-CART-082: Tên sản phẩm chứa HTML/script

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Có sản phẩm chứa thẻ HTML/script trong kho.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tên sản phẩm | `"<script>alert('xss')</script>"` |

## Test steps
1. Thêm sản phẩm có tên chứa mã script `<script>alert('xss')</script>` vào giỏ.
2. Truy cập trang giỏ hàng và kiểm tra xem hộp thoại alert có bật lên hay không.


## Expected result
- Không thực thi script, chỉ hiển thị text an toàn

## Status / Related bugs
Pass / None
