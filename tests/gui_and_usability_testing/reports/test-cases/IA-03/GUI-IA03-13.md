# GUI-IA03-13: Trang hồ sơ chưa login có đường tới trang đăng nhập

## Requirement ID
Heuristic (dead-end navigation)

## Module / Test type / Technique
Điều hướng (Navigation) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA03-13 |
| Interface Aspect | Điều hướng (Navigation) |
| Actor | Người dùng cuối (khách) |
| Goal | Trang hồ sơ chưa login có đường tới trang đăng nhập. |
| Screen(s) | Hồ sơ/ĐH |
| Checklist item | /profile chưa login: thông báo kèm link tới đăng nhập (hiện text trần — Profile.jsx:109). |
| Traced to | Heuristic (dead-end navigation) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.
- Đã đăng nhập bằng tài khoản `test@eshop.com` / `Test1234!`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI |
| Endpoint / UI flow | /profile |
| Input / Payload | URL `/profile` (chưa login) |
| Fixture | Không cần |

## Test steps
1. Đăng xuất, truy cập `/profile`.
2. Tìm link/nút tới trang đăng nhập.
3. Fail nếu chỉ có text trần, không có đường tiếp tục.

## Expected result
- Truy cập `/profile` khi chưa đăng nhập hiển thị link "Đăng nhập" hoặc tự redirect.
- Không phải chỉ có dòng text "Vui lòng đăng nhập" cụt.

## Status / Related bugs
Failed — xem screenshot & Issue liên quan

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — Playwright/Chromium
- Execution tool: Playwright (Chromium headless) — tự động hoá
- Observed: /profile khi chưa đăng nhập chỉ hiển thị text trần "Vui lòng đăng nhập", không có link tới trang đăng nhập và không tự redirect — ngõ cụt điều hướng.
- Execution result: **Failed**
- Screenshot: ![GUI-IA03-13](../screenshots/GUI-IA03-13.png)
