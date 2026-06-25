# [BUG][Coupon] Lỗi so sánh nghiêm ngặt tại ngưỡng đơn hàng tối thiểu (min_order_amount)

## Found by Test Case
TC-COUPON-001, TC-COUPON-004

## Requirement liên quan
FR-09: Discount coupons (Điều kiện C3)

## Severity / Priority
Major / P1

## Environment
Backend Node.js API, SQLite Database

## Steps to reproduce
1. Thực hiện cuộc gọi API POST đến `/api/apply-coupon` với các tham số:
   ```json
   {
     "code": "SAVE10",
     "total_amount": 300000,
     "user_id": 1
   }
   ```
   *(Ngưỡng tối thiểu của mã SAVE10 là 300,000 ₫)*

## Expected result
- Trả về mã HTTP 200.
- Áp dụng thành công mã giảm giá.

## Actual result
- Trả về mã HTTP 400.
- Báo lỗi: "Đơn hàng chưa đủ giá trị tối thiểu 300,000 ₫ để áp dụng mã này".

## Cause analysis (Nguyên nhân)
Tại `backend/server.js` dòng 379:
```javascript
if (total_amount > coupon.min_order_amount)
```
Hệ thống sử dụng toán tử so sánh lớn hơn (`>`) thay vì lớn hơn hoặc bằng (`>=`), dẫn đến việc từ chối áp dụng khi đơn hàng đạt chính xác giá trị ngưỡng tối thiểu.
