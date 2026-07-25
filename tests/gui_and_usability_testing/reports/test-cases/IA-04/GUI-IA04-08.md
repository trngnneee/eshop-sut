# GUI-IA04-08: Thao tác tải dữ liệu có loading indicator

## Requirement ID
Heuristic (loading indicators)

## Module / Test type / Technique
Phản hồi & Trạng thái (Feedback & State) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA04-08 |
| Interface Aspect | Phản hồi & Trạng thái (Feedback & State) |
| Actor | Người dùng cuối (khách) |
| Goal | Thao tác tải dữ liệu có loading indicator. |
| Screen(s) | Trang chủ, Lịch sử ĐH, Chi tiết SP |
| Checklist item | Thao tác tải dữ liệu có loading indicator (hiện không có/chỉ text — Home.jsx:13-30, Profile.jsx:15-30, ProductDetail.jsx:34); test với Slow 3G. |
| Traced to | Heuristic (loading indicators) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.
- Đã đăng nhập bằng tài khoản `test@eshop.com` / `Test1234!`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — DevTools Network throttling |
| Endpoint / UI flow | / , /profile , /product/:id |
| Input / Payload | Throttle Slow 3G |
| Fixture | Sản phẩm + đơn hàng seed |

## Test steps
1. Bật DevTools Network, chọn Slow 3G.
2. Mở lần lượt `/`, `/profile`, `/product/1`.
3. Fail nếu không có loading indicator trong lúc chờ.

## Expected result
- Trong lúc chờ dữ liệu có spinner/skeleton rõ ràng, không chỉ là text trần.

## Status / Related bugs
Failed — xem screenshot & Issue liên quan

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — Playwright/Chromium (throttle API)
- Execution tool: Playwright (Chromium headless) — tự động hoá
- Observed: Khi API bị làm chậm, trang chủ không hiển thị spinner/skeleton nào (số phần tử loading: 0) — người dùng thấy trang trống trong lúc chờ.
- Execution result: **Failed**
- Screenshot: ![GUI-IA04-08](../screenshots/GUI-IA04-08.png)
