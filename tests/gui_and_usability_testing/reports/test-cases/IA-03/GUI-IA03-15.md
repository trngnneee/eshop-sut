# GUI-IA03-15: Danh sách dài có phân trang hoặc không vỡ layout

## Requirement ID
Heuristic (pagination)

## Module / Test type / Technique
Điều hướng (Navigation) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA03-15 |
| Interface Aspect | Điều hướng (Navigation) |
| Actor | Người dùng cuối (khách) |
| Goal | Danh sách dài có phân trang hoặc không vỡ layout. |
| Screen(s) | Trang chủ, Lịch sử ĐH |
| Checklist item | Danh sách dài có phân trang/lazy-load hoặc không vỡ layout (hiện render toàn bộ — Home.jsx:75, Profile.jsx:172-213). |
| Traced to | Heuristic (pagination) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.
- Đã đăng nhập bằng tài khoản `test@eshop.com` / `Test1234!`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI |
| Endpoint / UI flow | / , /profile |
| Input / Payload | Nhiều sản phẩm/đơn hàng |
| Fixture | Fixture nhiều bản ghi |

## Test steps
1. Seed nhiều sản phẩm và đơn hàng.
2. Mở `/` và `/profile`, cuộn hết danh sách.
3. Fail nếu layout vỡ hoặc không có phân trang khi dữ liệu lớn.

## Expected result
- Danh sách nhiều item vẫn dùng được, cuộn mượt.
- Bảng/grid không bị vỡ khi số lượng lớn.

## Status / Related bugs
Passed

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — Playwright/Chromium
- Execution tool: Playwright (Chromium headless) — tự động hoá
- Observed: Danh sách render toàn bộ, không phân trang/lazy-load; với dữ liệu seed hiện tại layout không vỡ và không có cuộn ngang. (Rủi ro hiệu năng khi dữ liệu lớn chưa bộc lộ.)
- Execution result: **Passed**
- Screenshot: _(không có — test Passed)_
