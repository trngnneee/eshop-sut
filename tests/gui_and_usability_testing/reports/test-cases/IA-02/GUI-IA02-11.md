# GUI-IA02-11: Mã giảm giá chuẩn hoá hoa/thường nhất quán

## Requirement ID
Heuristic (format constraints: coupon)

## Module / Test type / Technique
Biểu mẫu (Forms) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA02-11 |
| Interface Aspect | Biểu mẫu (Forms) |
| Actor | Người dùng cuối (khách) |
| Goal | Mã giảm giá chuẩn hoá hoa/thường nhất quán. |
| Screen(s) | Thanh toán |
| Checklist item | Mã giảm giá chuẩn hoá hoa/thường: "sale10" xử lý như "SALE10" (Checkout.jsx:110-116, 30). |
| Traced to | Heuristic (format constraints: coupon) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.
- Đã đăng nhập bằng tài khoản `test@eshop.com` / `Test1234!`.
- Giỏ hàng có sẵn ít nhất 1 sản phẩm.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI |
| Endpoint / UI flow | /checkout |
| Input / Payload | "sale10" và "SALE10" |
| Fixture | Coupon seed hợp lệ |

## Test steps
1. Mở `/checkout` với giỏ có hàng.
2. Áp mã "sale10", ghi kết quả; xoá, áp "SALE10", ghi kết quả.
3. Fail nếu 2 lần cho kết quả khác nhau.

## Expected result
- Nhập "sale10" cho kết quả như "SALE10".
- Mã hiển thị nhất quán ở dạng chữ hoa.

## Status / Related bugs
Passed

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — kiểm thử thủ công trên trình duyệt Chrome
- Observed: Nhập mã chữ thường "save10" được chuẩn hoá (toUpperCase + CSS uppercase) và áp dụng như "SAVE10" (hiện thông báo Tiết kiệm) — xử lý hoa/thường nhất quán.
- Execution result: **Passed**
- Screenshot: _(không có — test Passed)_
