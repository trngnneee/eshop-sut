# GUI-IA01-16: Tên sản phẩm dài không phá layout card và vẫn xem được đầy đủ

## Requirement ID
Heuristic (text overflow)

## Module / Test type / Technique
Giao diện chung (General UI) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA01-16 |
| Interface Aspect | Giao diện chung (General UI) |
| Actor | Người dùng cuối (khách) |
| Goal | Tên sản phẩm dài không phá layout card và vẫn xem được đầy đủ. |
| Screen(s) | Trang chủ |
| Checklist item | Tên sản phẩm dài bị truncate (Home.jsx:86) vẫn xem được đầy đủ, không phá layout. |
| Traced to | Heuristic (text overflow) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI |
| Endpoint / UI flow | / |
| Input / Payload | Sản phẩm có tên rất dài |
| Fixture | Fixture sản phẩm tên >60 ký tự |

## Test steps
1. Chuẩn bị/seed 1 sản phẩm tên rất dài, mở `/`.
2. Quan sát card có bị vỡ layout không.
3. Rê chuột lên tên kiểm tra có tooltip tên đầy đủ.

## Expected result
- Tên dài hiển thị "..." gọn trong card, không tràn.
- Có cách xem tên đầy đủ (tooltip/title).

## Status / Related bugs
Failed — xem screenshot & Issue liên quan

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — Playwright/Chromium
- Execution tool: Playwright (Chromium headless) — tự động hoá
- Observed: Tên sản phẩm dùng class "truncate" để cắt gọn nhưng KHÔNG có thuộc tính title/tooltip → không có cách xem đầy đủ tên khi bị cắt.
- Execution result: **Failed**
- Screenshot: ![GUI-IA01-16](../screenshots/GUI-IA01-16.png)
