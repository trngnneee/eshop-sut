# TC-CART-011: Cộng dồn sản phẩm trùng ID

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / State + Domain Testing

## Preconditions
- Người dùng đã đăng nhập.
- Sản phẩm A đã có trong giỏ hàng với số lượng ban đầu là 2.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Sản phẩm | `Sản phẩm A` |
| Số lượng thêm tiếp | `3` |

## Test steps
1. Tìm sản phẩm A và thực hiện thêm vào giỏ hàng với số lượng là 3.
2. Truy cập vào trang giỏ hàng `/cart` và kiểm tra dòng sản phẩm A.

## Expected result
- Trong giỏ hàng `/cart` chỉ hiển thị 1 dòng duy nhất cho sản phẩm A.
- Số lượng sản phẩm A được cập nhật cộng dồn chính xác thành 5 (2 + 3 = 5).

## Status / Related bugs
Pass / None
