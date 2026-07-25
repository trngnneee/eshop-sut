# GUI-IA01-03: Nút hành động tích cực dùng màu xanh dương, màu đỏ chỉ cho hành động nguy hiểm/hủy

## Requirement ID
FR-21 (nhất quán màu sắc)

## Module / Test type / Technique
Giao diện chung (General UI) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA01-03 |
| Interface Aspect | Giao diện chung (General UI) |
| Actor | Người dùng cuối (khách) |
| Goal | Nút hành động tích cực dùng màu xanh dương, màu đỏ chỉ cho hành động nguy hiểm/hủy. |
| Screen(s) | Đăng ký |
| Checklist item | Nút submit "Đăng Ký" dùng màu hành động tích cực (hiện nền đỏ bg-red-500 — Register.jsx:71-76). |
| Traced to | FR-21 (nhất quán màu sắc) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI |
| Endpoint / UI flow | /register |
| Input / Payload | Không có (quan sát tĩnh) |
| Fixture | Không cần |

## Test steps
1. Mở `localhost:5173/register`.
2. Quan sát màu nền nút "Đăng Ký".
3. Đối chiếu với quy tắc màu của FR-21.

## Expected result
- Nút "Đăng Ký" có màu xanh dương.
- Màu đỏ không được dùng cho nút submit tích cực.

## Status / Related bugs
Failed — xem screenshot & Issue liên quan

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — Playwright/Chromium
- Execution tool: Playwright (Chromium headless) — tự động hoá
- Observed: Nút "Đăng Ký" có màu nền rgb(239, 68, 68) (đỏ, bg-red-500) — dùng màu cảnh báo cho hành động tích cực thay vì xanh dương.
- Execution result: **Failed**
- Screenshot: ![GUI-IA01-03](../screenshots/GUI-IA01-03.png)
