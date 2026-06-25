# [BUG][Coupon] Sai công thức tính giá trị giảm giá theo tỷ lệ phần trăm (percent)

## Found by Test Case
TC-COUPON-001, TC-COUPON-003

## Requirement liên quan
FR-09: Discount coupons (Công thức tính giảm giá phần trăm)

## Severity / Priority
Critical / P0

## Environment
Backend Node.js API, SQLite Database

## Steps to reproduce
1. Thực hiện cuộc gọi API POST đến `/api/apply-coupon` để áp dụng mã giảm giá tỷ lệ phần trăm (Ví dụ mã `SAVE10` có giá trị 10%):
   ```json
   {
     "code": "SAVE10",
     "total_amount": 300001,
     "user_id": 1
   }
   ```

## Expected result
- Số tiền giảm giá (`discount_amount`) phải là `30,000 ₫` (10% của 300,001 ₫).
- Số tiền thanh toán cuối cùng (`final_amount`) phải là `270,001 ₫`.

## Actual result
- Số tiền giảm giá tính ra âm: `discount_amount = -2,700,009 ₫`.
- Số tiền thanh toán cuối cùng tăng vọt: `final_amount = 3,000,010 ₫`.

## Cause analysis (Nguyên nhân)
Tại `backend/server.js` dòng 398-401 và 418-421:
```javascript
if (coupon.type === "percent") {
  discount_amount = Math.floor(
    total_amount * (1 - coupon.discount_value),
  );
}
```
Mã nguồn tính `1 - coupon.discount_value` (ví dụ `1 - 10 = -9`). Công thức đúng phải là:
```javascript
discount_amount = Math.floor(
  total_amount * (coupon.discount_value / 100)
);
```
