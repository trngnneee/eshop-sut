# TC-CART-049: Cart của user A không hiển thị cho user B

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Security / State / Security

## Preconditions
- User A đã thêm một số sản phẩm vào giỏ hàng của mình.
- User B đăng nhập bằng tài khoản khác.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Đăng nhập tài khoản User A, thêm 'Sản phẩm A' vào giỏ hàng và đăng xuất.
2. Đăng nhập tài khoản User B.
3. Truy cập trang `/cart`.

## Expected result
- User B không nhìn thấy bất kỳ sản phẩm nào từ giỏ hàng của User A.
- Dữ liệu giỏ hàng của các user hoàn toàn độc lập và được phân quyền cô lập.

## Status / Related bugs
Pass / None
