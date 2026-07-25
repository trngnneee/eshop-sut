# GUI-IA03-11: Back ở bước 2 quên mật khẩu không mất tiến trình

## Requirement ID
Heuristic (browser back-button, multi-step)

## Module / Test type / Technique
Điều hướng (Navigation) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA03-11 |
| Interface Aspect | Điều hướng (Navigation) |
| Actor | Người dùng cuối (khách) |
| Goal | Back ở bước 2 quên mật khẩu không mất tiến trình. |
| Screen(s) | Quên mật khẩu |
| Checklist item | Ở bước 2 bấm Back trình duyệt: không mất tiến trình (step là state, không gắn URL — ForgotPassword.jsx:8). |
| Traced to | Heuristic (browser back-button, multi-step) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI |
| Endpoint / UI flow | /forgot-password |
| Input / Payload | Nút Back trình duyệt |
| Fixture | Tài khoản test@eshop.com |

## Test steps
1. Vào `/forgot-password`, lấy OTP để sang bước 2.
2. Bấm Back của trình duyệt.
3. Fail nếu Back rời hẳn trang và mất tiến trình OTP.

## Expected result
- Bấm Back ở bước 2 quay về bước 1 (hoặc giữ tiến trình), không rời hẳn trang.

## Status / Related bugs
Failed — xem screenshot & Issue liên quan

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — Playwright/Chromium
- Execution tool: Playwright (Chromium headless) — tự động hoá
- Observed: Ở bước 2, bấm Back trình duyệt rời hẳn trang Quên mật khẩu (URL: "about:blank") — step là state không gắn URL nên mất toàn bộ tiến trình OTP.
- Execution result: **Failed**
- Screenshot: ![GUI-IA03-11](../screenshots/GUI-IA03-11.png)
