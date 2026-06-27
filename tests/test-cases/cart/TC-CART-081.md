# TC-CART-081: Tên sản phẩm rất dài

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Có sản phẩm tên rất dài trong kho.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tên sản phẩm | `'Sản phẩm A ' * 30` |

## Test steps
1. Thêm sản phẩm có tên cực kỳ dài (ví dụ: trên 200 ký tự) vào giỏ hàng.
2. Truy cập trang giỏ hàng `/cart` và kiểm tra layout giao diện của dòng sản phẩm đó.


## Expected result
- Tên không phá layout bảng, có wrap/ellipsis hợp lý

## Status / Related bugs
Not Run / None
