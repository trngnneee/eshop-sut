# GUI-IA03-10: Back sau thanh toán không cho re-submit đơn cũ

## Requirement ID
Heuristic (browser back-button)

## Module / Test type / Technique
Điều hướng (Navigation) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA03-10 |
| Interface Aspect | Điều hướng (Navigation) |
| Actor | Người dùng cuối (khách) |
| Goal | Back sau thanh toán không cho re-submit đơn cũ. |
| Screen(s) | Thanh toán |
| Checklist item | Sau thanh toán thành công, Back trình duyệt không quay lại form có thể re-submit (Checkout.jsx:69-77). |
| Traced to | Heuristic (browser back-button) |

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
| Input / Payload | Nút Back trình duyệt |
| Fixture | Giỏ có hàng; tài khoản test@eshop.com |

## Test steps
1. Hoàn tất 1 đơn hàng ở `/checkout` (màn Thanh toán thành công).
2. Bấm Back của trình duyệt.
3. Fail nếu quay lại form cho phép submit lại đơn.

## Expected result
- Bấm Back sau khi đặt hàng thành công không hiển thị form checkout có thể submit lại đơn cũ.
- Trạng thái giỏ/form nhất quán.

## Status / Related bugs
Passed

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — kiểm thử thủ công trên trình duyệt Chrome
- Observed: Sau thanh toán thành công, bấm Back không quay lại form có nút "Xác Nhận Thanh Toán" có thể re-submit đơn cũ.
- Execution result: **Passed**
- Screenshot: _(không có — test Passed)_
