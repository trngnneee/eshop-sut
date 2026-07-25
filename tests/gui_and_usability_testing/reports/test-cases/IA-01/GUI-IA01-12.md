# GUI-IA01-12: Title tab trình duyệt mô tả trang, đổi theo từng màn hình

## Requirement ID
Heuristic (page title)

## Module / Test type / Technique
Giao diện chung (General UI) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA01-12 |
| Interface Aspect | Giao diện chung (General UI) |
| Actor | Người dùng cuối (khách) |
| Goal | Title tab trình duyệt mô tả trang, đổi theo từng màn hình. |
| Screen(s) | Tất cả 8 màn hình |
| Checklist item | Title tab trình duyệt mô tả trang (hiện cố định "frontend-web" — index.html:7). |
| Traced to | Heuristic (page title) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — tab title |
| Endpoint / UI flow | (8 màn hình khảo sát) |
| Input / Payload | Không có |
| Fixture | Không cần |

## Test steps
1. Mở lần lượt các trang, quan sát tiêu đề tab trình duyệt.
2. Fail nếu title cố định "frontend-web" không đổi theo trang.

## Expected result
- Title tab dạng "EShop — <tên trang>".
- Title thay đổi khi điều hướng giữa các trang.

## Status / Related bugs
Failed — xem screenshot & Issue liên quan

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — Playwright/Chromium
- Execution tool: Playwright (Chromium headless) — tự động hoá
- Observed: Title tab cố định "frontend-web" ở trang chủ và "frontend-web" ở /login — không đổi theo trang, không mô tả nội dung.
- Execution result: **Failed**
- Screenshot: ![GUI-IA01-12](../screenshots/GUI-IA01-12.png)
