# [BUG][Coupon] Thiếu middleware xác thực (Authorization) cho API áp dụng mã giảm giá

## Found by Test Case
TC-COUPON-008

## Requirement liên quan
FR-09: Discount coupons (Điều kiện C4 - Đã đăng nhập)

## Severity / Priority
Major / P1

## Environment
Backend Node.js API

## Steps to reproduce
1. Gửi một yêu cầu POST đến `/api/apply-coupon` mà không truyền header `Authorization` (hoặc truyền JWT token trống/không hợp lệ) nhưng vẫn truyền `user_id` và mã giảm giá hợp lệ:
   ```json
   {
     "code": "SAVE10",
     "total_amount": 350000,
     "user_id": 1
   }
   ```

## Expected result
- Trả về mã HTTP 401 Unauthorized do người dùng chưa đăng nhập.

## Actual result
- Hệ thống trả về HTTP 200 OK và áp dụng thành công mã giảm giá.

## Cause analysis (Nguyên nhân)
Tại `backend/server.js` dòng 363:
```javascript
app.post("/api/apply-coupon", (req, res) => {
```
API này không được khai báo với middleware `authenticateToken`. Đúng ra phải là:
```javascript
app.post("/api/apply-coupon", authenticateToken, (req, res) => {
```
