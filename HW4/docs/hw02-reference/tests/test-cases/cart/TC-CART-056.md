# TC-CART-056: Sản phẩm có tên chứa ký tự đặc biệt an toàn

## Requirement ID
FR-07, SEC-04

## Module / Test type / Technique
Cart / Security / Security / XSS

## Preconditions
- Hệ thống có sản phẩm mang tên chứa mã độc XSS: `<script>alert('xss')</script>`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Thêm sản phẩm có tên chứa script trên vào giỏ hàng.
2. Truy cập `/cart`.

## Expected result
- Mã script không được thực thi (không hiện popup alert).
- Tên sản phẩm được hiển thị an toàn dưới dạng văn bản thô: `<script>alert('xss')</script>`.

## Status / Related bugs
Not Run / None
