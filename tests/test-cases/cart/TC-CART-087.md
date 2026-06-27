# TC-CART-087: Gửi GET /api/cart với token của user A sau khi logout

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Token hợp lệ trước khi bấm logout.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
Không có

## Test steps
1. Đăng nhập tài khoản A và lấy token JWT.
2. Nhấn Đăng xuất trên trình duyệt (hoặc gửi API logout).
3. Sử dụng token vừa lấy để gửi request GET tới /api/cart.


## Expected result
- Không trả dữ liệu nếu token đã bị vô hiệu

## Status / Related bugs
Not Run / None
