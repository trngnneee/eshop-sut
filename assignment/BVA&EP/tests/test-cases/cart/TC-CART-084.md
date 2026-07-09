# TC-CART-084: Tổng tiền có giá trị rất lớn

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Có sản phẩm giá trị cao.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
Không có

## Test steps
1. Thêm các sản phẩm có giá trị cực lớn hoặc tăng số lượng để tổng tiền giỏ hàng đạt giá trị khổng lồ (ví dụ: vài chục tỷ đồng).
2. Xác minh nhãn Tổng cộng hiển thị đúng định dạng tiền tệ và không hiển thị lỗi như NaN, Infinity.


## Expected result
- Format VND vẫn đúng, không hiển thị NaN, Infinity, số âm

## Status / Related bugs
Pass / None
