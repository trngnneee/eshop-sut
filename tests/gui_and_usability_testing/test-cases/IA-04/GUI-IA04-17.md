# GUI-IA04-17: Đăng ký thành công có thông báo xác nhận

## Requirement ID
Heuristic (action feedback)

## Module / Test type / Technique
Phản hồi & Trạng thái (Feedback & State) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA04-17 |
| Interface Aspect | Phản hồi & Trạng thái (Feedback & State) |
| Actor | Người dùng cuối (khách) |
| Goal | Đăng ký thành công có thông báo xác nhận. |
| Screen(s) | Đăng ký |
| Checklist item | Đăng ký thành công có thông báo xác nhận (hiện navigate thẳng /login không message — Register.jsx:25). |
| Traced to | Heuristic (action feedback) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI |
| Endpoint / UI flow | /register |
| Input / Payload | Đăng ký tài khoản mới hợp lệ |
| Fixture | Email chưa tồn tại |

## Test steps
1. Mở `/register`, nhập thông tin hợp lệ, submit.
2. Quan sát có thông báo thành công không trước khi sang `/login`.
3. Fail nếu chuyển trang thẳng không có feedback.

## Expected result
- Đăng ký thành công → hiển thị toast/message "Đăng ký thành công, mời đăng nhập" trước/khi chuyển trang.

## Status / Related bugs
Failed — BUG-46 (https://github.com/trngnneee/eshop-sut/issues/239)

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — kiểm thử thủ công trên trình duyệt Chrome
- Observed: Đăng ký thành công điều hướng thẳng sang /login không có thông báo xác nhận ("Đăng ký thành công, mời đăng nhập").
- Execution result: **Failed**
- Screenshot: ![GUI-IA04-17](../screenshots/GUI-IA04-17.png)
