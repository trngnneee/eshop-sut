# GUI-IA01-01: Toàn bộ giao diện dùng tiếng Việt, không lẫn chữ tiếng Anh ngoài thuật ngữ chuẩn

## Requirement ID
FR-21 (nhất quán ngôn ngữ)

## Module / Test type / Technique
Giao diện chung (General UI) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA01-01 |
| Interface Aspect | Giao diện chung (General UI) |
| Actor | Người dùng cuối (khách) |
| Goal | Toàn bộ giao diện dùng tiếng Việt, không lẫn chữ tiếng Anh ngoài thuật ngữ chuẩn. |
| Screen(s) | Đăng nhập |
| Checklist item | Nhãn field và nút trên form đăng nhập hiển thị bằng tiếng Việt (hiện là "Username", "Sign In" — Login.jsx:28,58). |
| Traced to | FR-21 (nhất quán ngôn ngữ) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI |
| Endpoint / UI flow | /login |
| Input / Payload | Không có (quan sát tĩnh) |
| Fixture | Không cần |

## Test steps
1. Mở `localhost:5173/login`.
2. Đọc nhãn của các ô nhập và nhãn nút submit.
3. Đối chiếu với yêu cầu ngôn ngữ tiếng Việt của FR-21.

## Expected result
- Nhãn field là "Email" (hoặc "Tên đăng nhập"), nút submit là "Đăng nhập".
- Không còn chuỗi tiếng Anh nào trên màn hình đăng nhập.

## Status / Related bugs
Failed — xem screenshot & Issue liên quan

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — Playwright/Chromium
- Execution tool: Playwright (Chromium headless) — tự động hoá
- Observed: Nhãn field: "Username | Mật khẩu"; nút submit: "Sign In". Màn đăng nhập vẫn dùng chuỗi tiếng Anh ("Username", "Sign In") thay vì tiếng Việt.
- Execution result: **Failed**
- Screenshot: ![GUI-IA01-01](../screenshots/GUI-IA01-01.png)
