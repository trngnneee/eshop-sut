# GUI-IA04-07: Mọi ảnh sản phẩm có alt mô tả

## Requirement ID
FR-24 (image alt-text)

## Module / Test type / Technique
Phản hồi & Trạng thái (Feedback & State) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA04-07 |
| Interface Aspect | Phản hồi & Trạng thái (Feedback & State) |
| Actor | Người dùng cuối (khách) |
| Goal | Mọi ảnh sản phẩm có alt mô tả. |
| Screen(s) | Trang chủ |
| Checklist item | Ảnh sản phẩm có alt mô tả (hiện alt="" — Home.jsx:81-85; Chi tiết SP đã đạt). |
| Traced to | FR-24 (image alt-text) |

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
1. Mở `/`, bật DevTools, kiểm tra `alt` của các thẻ `<img>` card.
2. Fail nếu alt rỗng.

## Expected result
- Ảnh card sản phẩm có thuộc tính `alt` = tên sản phẩm, không rỗng.

## Status / Related bugs
Failed — xem screenshot & Issue liên quan

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — Playwright/Chromium
- Execution tool: Playwright (Chromium headless) — tự động hoá
- Observed: Ảnh sản phẩm trên trang chủ có alt="" (rỗng) — thiếu văn bản thay thế mô tả.
- Execution result: **Failed**
- Screenshot: ![GUI-IA04-07](../screenshots/GUI-IA04-07.png)
