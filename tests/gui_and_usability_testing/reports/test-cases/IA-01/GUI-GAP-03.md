# GUI-GAP-03: Thẻ <html> khai báo đúng ngôn ngữ nội dung

## Requirement ID
Heuristic / WCAG 3.1.1 (language of page) — bổ sung thủ công

## Module / Test type / Technique
Giao diện chung (General UI) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-GAP-03 |
| Interface Aspect | Giao diện chung (General UI) |
| Actor | Người dùng cuối (khách) |
| Goal | Thẻ <html> khai báo đúng ngôn ngữ nội dung. |
| Screen(s) | Toàn app |
| Checklist item | Thẻ `<html>` khai báo đúng ngôn ngữ nội dung (hiện `lang="en"` trong khi UI tiếng Việt — index.html:2). |
| Traced to | Heuristic / WCAG 3.1.1 (language of page) — bổ sung thủ công |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — DevTools Elements |
| Endpoint / UI flow | (mọi trang) |
| Input / Payload | Không có |
| Fixture | Không cần |

## Test steps
1. Mở app, bật DevTools Elements.
2. Đọc thuộc tính `lang` của thẻ `<html>`.
3. Fail nếu `lang="en"` (hoặc khác `vi`).

## Expected result
- Thẻ `<html>` có `lang="vi"`.
- Screen reader đọc nội dung bằng giọng tiếng Việt.

## Status / Related bugs
Failed — xem screenshot & Issue liên quan

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — Playwright/Chromium
- Execution tool: Playwright (Chromium headless) — tự động hoá
- Observed: Thẻ <html> khai báo lang="en" trong khi toàn bộ UI là tiếng Việt — sai ngôn ngữ nội dung (WCAG 3.1.1).
- Execution result: **Failed**
- Screenshot: ![GUI-GAP-03](../screenshots/GUI-GAP-03.png)
