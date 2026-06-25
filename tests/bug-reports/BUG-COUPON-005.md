# [BUG][Coupon] Thiếu validate kiểu dữ liệu và khoảng giá trị cho total_amount

## Found by Test Case
TC-COUPON-017, TC-COUPON-018, TC-COUPON-019

## Requirement liên quan
FR-09: Discount coupons (Điều kiện C3)

## Severity / Priority
Minor / P3

## Environment
Backend Node.js API, SQLite Database

## Steps to reproduce
1. Đăng nhập hệ thống (có JWT token).
2. Gửi yêu cầu POST áp dụng mã giảm giá `SAVE10` với các tham số đầu vào không hợp lệ cho `total_amount`:
   - Trường hợp 1: `"total_amount": "invalid_number"` (chuỗi chữ)
   - Trường hợp 2: `"total_amount": null` (hoặc không truyền)
   - Trường hợp 3: `"total_amount": -50000` (số âm)
   ```json
   {
     "code": "SAVE10",
     "total_amount": -50000,
     "user_id": 1
   }
   ```

## Expected result
- Hệ thống từ chối áp dụng và trả về mã HTTP 400.
- Hiển thị thông báo lỗi phản ánh đúng nguyên nhân đầu vào không hợp lệ, ví dụ: "Tổng giá trị đơn hàng không hợp lệ" hoặc "Tổng giá trị đơn hàng phải là một số dương".

## Actual result
- Hệ thống trả về mã HTTP 400 nhưng thông báo lỗi lại là: `"Đơn hàng chưa đủ giá trị tối thiểu 300,000 ₫ để áp dụng mã này"`.
- Lý do là hệ thống không kiểm tra tính hợp lệ của `total_amount` trước khi thực hiện phép so sánh `total_amount > coupon.min_order_amount`. Khi so sánh thất bại (luôn trả về `false` đối với chuỗi, số âm hoặc null), hệ thống nhảy vào nhánh `else` mặc định và xuất ra thông báo lỗi về giá trị tối thiểu của coupon, gây hiểu nhầm cho người dùng/hệ thống tích hợp.

## Cause analysis (Nguyên nhân)
Tại `backend/server.js` dòng 379:
```javascript
if (total_amount > coupon.min_order_amount) {
   ...
} else {
  return res.status(400).json({
    error: `Đơn hàng chưa đủ giá trị tối thiểu ${coupon.min_order_amount.toLocaleString()} ₫ để áp dụng mã này`,
  });
}
```
Hệ thống thiếu bước validate đầu vào cho `total_amount` để đảm bảo nó là kiểu dữ liệu số (`typeof total_amount === 'number'`), không bị NaN, và có giá trị lớn hơn hoặc bằng 0.

Cách sửa đề xuất:
```javascript
if (typeof total_amount !== 'number' || isNaN(total_amount) || total_amount < 0) {
  return res.status(400).json({ error: "Tổng giá trị đơn hàng không hợp lệ" });
}
```
