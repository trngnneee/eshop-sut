# GUI-IA01-15: Grid sản phẩm responsive đúng số cột, không tràn ngang

## Requirement ID
Heuristic (responsive)

## Module / Test type / Technique
Giao diện chung (General UI) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA01-15 |
| Interface Aspect | Giao diện chung (General UI) |
| Actor | Người dùng cuối (khách) |
| Goal | Grid sản phẩm responsive đúng số cột, không tràn ngang. |
| Screen(s) | Trang chủ |
| Checklist item | Grid sản phẩm 1/2/3 cột theo breakpoint (Home.jsx:75), không horizontal scroll ở 375/768/1280px. |
| Traced to | Heuristic (responsive) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — DevTools device toolbar |
| Endpoint / UI flow | / |
| Input / Payload | Viewport 375 / 768 / 1280px |
| Fixture | ≥3 sản phẩm seed |

## Test steps
1. Mở `/`, lần lượt đặt viewport 375, 768, 1280px.
2. Đếm số cột grid và kiểm tra thanh cuộn ngang.
3. Fail nếu sai số cột hoặc có horizontal scroll.

## Expected result
- 375px → 1 cột, 768px → 2 cột, 1280px → 3 cột.
- Không xuất hiện thanh cuộn ngang ở cả 3 kích thước.

## Status / Related bugs
Passed

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — Playwright/Chromium
- Execution tool: Playwright (Chromium headless) — tự động hoá
- Observed: Grid sản phẩm co giãn theo breakpoint (1/2/3 cột), không xuất hiện cuộn ngang ở 375/768/1280px.
- Execution result: **Passed**
- Screenshot: _(không có — test Passed)_
