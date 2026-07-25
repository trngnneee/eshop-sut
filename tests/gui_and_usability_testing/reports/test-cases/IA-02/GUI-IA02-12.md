# GUI-IA02-12: Field Email hồ sơ ở trạng thái không sửa được rõ ràng

## Requirement ID
FR-22 (disabled state) — kỳ vọng Pass

## Module / Test type / Technique
Biểu mẫu (Forms) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA02-12 |
| Interface Aspect | Biểu mẫu (Forms) |
| Actor | Người dùng cuối (khách) |
| Goal | Field Email hồ sơ ở trạng thái không sửa được rõ ràng. |
| Screen(s) | Hồ sơ |
| Checklist item | Field Email disabled đúng chuẩn: nhãn "(Không đổi)", nền xám, không nhận input (Profile.jsx:117-125). |
| Traced to | FR-22 (disabled state) — kỳ vọng Pass |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.
- Đã đăng nhập bằng tài khoản `test@eshop.com` / `Test1234!`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI |
| Endpoint / UI flow | /profile |
| Input / Payload | Thử click/gõ vào ô Email |
| Fixture | Tài khoản test@eshop.com |

## Test steps
1. Đăng nhập, mở `/profile`.
2. Thử click và gõ vào ô Email.
3. Fail nếu ô nhận input hoặc không thể hiện trạng thái disabled.

## Expected result
- Ô Email không focus/gõ được, nền xám, nhãn ghi "(Không đổi)".

## Status / Related bugs
Passed

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — Playwright/Chromium
- Execution tool: Playwright (Chromium headless) — tự động hoá
- Observed: Ô Email hồ sơ ở trạng thái disabled=true, nền rgb(243, 244, 246), nhãn kèm "(Không đổi)" — thể hiện rõ không sửa được (đúng chuẩn).
- Execution result: **Passed**
- Screenshot: _(không có — test Passed)_
