# GUI-IA01-09: Trang chủ có đúng 1 thẻ h1

## Requirement ID
FR-21 (tiêu đề trang)

## Module / Test type / Technique
Giao diện chung (General UI) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA01-09 |
| Interface Aspect | Giao diện chung (General UI) |
| Actor | Người dùng cuối (khách) |
| Goal | Trang chủ có đúng 1 thẻ h1. |
| Screen(s) | Trang chủ |
| Checklist item | Trang có đúng 1 thẻ h1 (hiện có 2: Home.jsx:44 và dòng đếm :110-114). |
| Traced to | FR-21 (tiêu đề trang) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — DevTools Elements |
| Endpoint / UI flow | / |
| Input / Payload | Không có |
| Fixture | Sản phẩm seed |

## Test steps
1. Mở `/`, bật DevTools.
2. Chạy `document.querySelectorAll('h1').length` trong Console.
3. Fail nếu kết quả khác 1.

## Expected result
- Trang chủ có đúng 1 thẻ `<h1>`.
- Dòng "Hiển thị N sản phẩm" dùng thẻ phi-heading (vd `<p>`).

## Status / Related bugs
Failed — xem screenshot & Issue liên quan

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — Playwright/Chromium
- Execution tool: Playwright (Chromium headless) — tự động hoá
- Observed: Trang chủ có 2 thẻ <h1> (tiêu đề "Danh sách sản phẩm" và dòng đếm "Hiển thị N sản phẩm" đều là h1) — vượt quá 1.
- Execution result: **Failed**
- Screenshot: ![GUI-IA01-09](../screenshots/GUI-IA01-09.png)
