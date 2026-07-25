# GUI-IA01-11: Heading mô tả đúng chức năng trang

## Requirement ID
FR-21 (tiêu đề trang)

## Module / Test type / Technique
Giao diện chung (General UI) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA01-11 |
| Interface Aspect | Giao diện chung (General UI) |
| Actor | Người dùng cuối (khách) |
| Goal | Heading mô tả đúng chức năng trang. |
| Screen(s) | Đăng nhập |
| Checklist item | Heading mô tả đúng chức năng trang (trang Đăng nhập nhưng heading ghi "Đăng Ký" — Login.jsx:24). |
| Traced to | FR-21 (tiêu đề trang) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI |
| Endpoint / UI flow | /login |
| Input / Payload | Không có |
| Fixture | Không cần |

## Test steps
1. Mở `/login`.
2. Đọc heading đầu form.
3. Fail nếu heading không phải "Đăng Nhập".

## Expected result
- Heading trang `/login` là "Đăng Nhập".

## Status / Related bugs
Failed — BUG-06 (https://github.com/trngnneee/eshop-sut/issues/199)

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — kiểm thử thủ công trên trình duyệt Chrome
- Observed: Heading trang /login là "Đăng Ký" — sai chức năng (ghi "Đăng Ký" trên trang Đăng nhập).
- Execution result: **Failed**
- Screenshot: ![GUI-IA01-11](../screenshots/GUI-IA01-11.png)
