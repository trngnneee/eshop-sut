# GUI-IA01-02: 100% text UI tĩnh bằng tiếng Việt trên toàn bộ 8 màn hình

## Requirement ID
FR-21 (nhất quán ngôn ngữ)

## Module / Test type / Technique
Giao diện chung (General UI) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA01-02 |
| Interface Aspect | Giao diện chung (General UI) |
| Actor | Người dùng cuối (khách) |
| Goal | 100% text UI tĩnh bằng tiếng Việt trên toàn bộ 8 màn hình. |
| Screen(s) | Tất cả 8 màn hình |
| Checklist item | Rà toàn bộ text UI tĩnh (nhãn, nút, placeholder, heading, thông báo) — không có chuỗi tiếng Anh ngoài thuật ngữ kỹ thuật chuẩn (Email, OTP). |
| Traced to | FR-21 (nhất quán ngôn ngữ) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI |
| Endpoint / UI flow | (8 màn hình khảo sát) |
| Input / Payload | Không có (quan sát tĩnh) |
| Fixture | Không cần |

## Test steps
1. Lần lượt mở 8 màn hình trong phạm vi.
2. Ghi lại mọi chuỗi tiếng Anh xuất hiện (vd "Username", "Sign In").
3. Đánh dấu Fail nếu có chuỗi tiếng Anh không phải thuật ngữ chuẩn.

## Expected result
- Mọi text UI tĩnh hiển thị bằng tiếng Việt.
- Chỉ chấp nhận thuật ngữ chuẩn (Email, OTP) ở dạng nguyên gốc.

## Status / Related bugs
Failed — xem screenshot & Issue liên quan

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — Playwright/Chromium
- Execution tool: Playwright (Chromium headless) — tự động hoá
- Observed: Còn chuỗi tiếng Anh không phải thuật ngữ chuẩn trên UI: Username, Sign In (màn Đăng nhập).
- Execution result: **Failed**
- Screenshot: ![GUI-IA01-02](../screenshots/GUI-IA01-02.png)
