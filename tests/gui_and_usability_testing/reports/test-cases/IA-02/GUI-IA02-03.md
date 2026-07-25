# GUI-IA02-03: Field mật khẩu che ký tự khi gõ

## Requirement ID
FR-22 (password masking)

## Module / Test type / Technique
Biểu mẫu (Forms) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA02-03 |
| Interface Aspect | Biểu mẫu (Forms) |
| Actor | Người dùng cuối (khách) |
| Goal | Field mật khẩu che ký tự khi gõ. |
| Screen(s) | Đăng nhập |
| Checklist item | Field Mật khẩu che ký tự khi gõ (hiện `type="text"` — Login.jsx:39-45; 2 form kia đã đúng). |
| Traced to | FR-22 (password masking) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI |
| Endpoint / UI flow | /login |
| Input / Payload | Chuỗi mật khẩu bất kỳ |
| Fixture | Không cần |

## Test steps
1. Mở `/login`, gõ vào ô Mật khẩu.
2. Quan sát ký tự hiển thị.
3. Fail nếu hiện rõ chữ (type=text).

## Expected result
- Ký tự mật khẩu hiển thị dạng chấm tròn, không hiện rõ.

## Status / Related bugs
Failed — xem screenshot & Issue liên quan

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — Playwright/Chromium
- Execution tool: Playwright (Chromium headless) — tự động hoá
- Observed: Ô Mật khẩu trên form Đăng nhập có type="text" → ký tự mật khẩu hiển thị rõ, không được che.
- Execution result: **Failed**
- Screenshot: ![GUI-IA02-03](../screenshots/GUI-IA02-03.png)
