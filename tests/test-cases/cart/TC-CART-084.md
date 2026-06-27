# TC-CART-084: Giỏ hàng có nhiều sản phẩm, ví dụ 50–100 dòng

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Trong kho hàng có trên 50 sản phẩm khác nhau.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
Không có

## Test steps
1. Thêm liên tục từ 50 đến 100 sản phẩm khác nhau vào giỏ hàng.
2. Truy cập trang giỏ hàng, cuộn trang xem bảng hiển thị có mượt mà, tổng tiền có tính toán chính xác hay không.


## Expected result
- Trang vẫn render ổn, total tính đúng, không lag nghiêm trọng

## Status / Related bugs
Not Run / None
