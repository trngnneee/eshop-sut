# GUI-IA04-12: Feedback coupon đúng cả 2 nhánh, số tiền chính xác

## Requirement ID
FR-24 (coupon feedback) — kỳ vọng Pass

## Module / Test type / Technique
Phản hồi & Trạng thái (Feedback & State) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA04-12 |
| Interface Aspect | Phản hồi & Trạng thái (Feedback & State) |
| Actor | Người dùng cuối (khách) |
| Goal | Feedback coupon đúng cả 2 nhánh, số tiền chính xác. |
| Screen(s) | Thanh toán |
| Checklist item | Feedback coupon đủ 2 nhánh: hợp lệ → message + tiết kiệm + thành tiền; sai → lỗi đỏ (Checkout.jsx:125-134); kiểm tra số tiền tính đúng. |
| Traced to | FR-24 (coupon feedback) — kỳ vọng Pass |

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
| Input / Payload | Mã hợp lệ + mã sai |
| Fixture | Coupon seed; giỏ có hàng |

## Test steps
1. Mở `/checkout` với giỏ có hàng.
2. Áp 1 mã hợp lệ, kiểm tra message + số tiền.
3. Áp 1 mã sai, kiểm tra message lỗi.
4. Fail nếu thiếu nhánh nào hoặc số tiền sai.

## Expected result
- Mã hợp lệ → hiện message + số tiền tiết kiệm + thành tiền, tính đúng.
- Mã sai → message lỗi đỏ rõ ràng.

## Status / Related bugs
Passed

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — Playwright/Chromium
- Execution tool: Playwright (Chromium headless) — tự động hoá
- Observed: Feedback coupon đủ 2 nhánh: mã hợp lệ "SAVE10" hiện Tiết kiệm + thành tiền (có); mã sai hiện lỗi đỏ (có) — hoạt động đúng.
- Execution result: **Passed**
- Screenshot: _(không có — test Passed)_
