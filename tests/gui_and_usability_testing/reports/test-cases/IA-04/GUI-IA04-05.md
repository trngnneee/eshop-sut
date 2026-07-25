# GUI-IA04-05: Empty state có icon/hình + message thân thiện

## Requirement ID
FR-24 (empty-state visuals)

## Module / Test type / Technique
Phản hồi & Trạng thái (Feedback & State) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA04-05 |
| Interface Aspect | Phản hồi & Trạng thái (Feedback & State) |
| Actor | Người dùng cuối (khách) |
| Goal | Empty state có icon/hình + message thân thiện. |
| Screen(s) | Giỏ hàng, Lịch sử ĐH |
| Checklist item | Empty state có icon/hình + message thân thiện (hiện text trần — Cart.jsx:20-27, Profile.jsx:169-170). |
| Traced to | FR-24 (empty-state visuals) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.
- Đã đăng nhập bằng tài khoản `test@eshop.com` / `Test1234!`.
- Giỏ hàng có sẵn ít nhất 1 sản phẩm.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI |
| Endpoint / UI flow | /cart , /profile |
| Input / Payload | Giỏ trống / chưa có đơn |
| Fixture | Tài khoản chưa có đơn hàng |

## Test steps
1. Mở `/cart` khi giỏ trống.
2. Đăng nhập tài khoản chưa có đơn, mở `/profile`.
3. Fail nếu empty state chỉ là dòng text trần, không có icon/CTA.

## Expected result
- Giỏ hàng trống và Lịch sử đơn hàng trống hiển thị icon/hình minh hoạ + message thân thiện + CTA.

## Status / Related bugs
Failed — xem screenshot & Issue liên quan

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — Playwright/Chromium
- Execution tool: Playwright (Chromium headless) — tự động hoá
- Observed: Empty state Giỏ hàng chỉ có text + link, không có icon/hình minh hoạ (số ảnh/SVG trong main: 0). Lịch sử ĐH trống cũng chỉ là text trần.
- Execution result: **Failed**
- Screenshot: ![GUI-IA04-05](../screenshots/GUI-IA04-05.png)
