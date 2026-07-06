# FR09-A-TC01: Từ chối người dùng chưa đăng nhập áp dụng mã giảm giá

## Requirement ID

FR-09

## Module / Test type / Technique

Coupon Application / Functional / Decision Table

## Preconditions

- Không có JWT hợp lệ trong request.
- Coupon `SAVE10` tồn tại, còn hạn và đang hoạt động.
- Giỏ hàng có tổng tiền `500000`.

## Test data

| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | anonymous |
| Endpoint | POST /api/apply-coupon |
| Coupon code | SAVE10 |
| Total amount | 500000 |
| Token | Không có |
| User ID | null |

## Test steps

1. Không đăng nhập hoặc xóa JWT khỏi request.
2. Chuẩn bị giỏ hàng có tổng tiền `500000`.
3. Gửi request `POST /api/apply-coupon` với body `{"code":"SAVE10","total_amount":500000,"user_id":null}` và không kèm `Authorization` header.
4. Kiểm tra response xác thực.

## Expected result

- Hệ thống trả về HTTP 401/403 hoặc lỗi xác thực phù hợp.
- Mã giảm giá không được áp dụng cho người dùng chưa đăng nhập.
- Response không trả về `discount_amount`/`final_amount` thành công.

## Status / Related bugs

Failed / BUG-FR09-A-01 - API áp dụng coupon không yêu cầu JWT hợp lệ
