# GUI-IA02-13: Form đăng ký có field xác nhận mật khẩu và kiểm tra khớp

## Requirement ID
Heuristic (confirmation-field matching)

## Module / Test type / Technique
Biểu mẫu (Forms) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA02-13 |
| Interface Aspect | Biểu mẫu (Forms) |
| Actor | Người dùng cuối (khách) |
| Goal | Form đăng ký có field xác nhận mật khẩu và kiểm tra khớp. |
| Screen(s) | Đăng ký |
| Checklist item | Form có field "Xác nhận mật khẩu" bắt buộc khớp (hiện không tồn tại — Register.jsx:35-81). |
| Traced to | Heuristic (confirmation-field matching) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI |
| Endpoint / UI flow | /register |
| Input / Payload | Mật khẩu + xác nhận khác nhau |
| Fixture | Không cần |

## Test steps
1. Mở `/register`, tìm field "Xác nhận mật khẩu".
2. Nếu có, nhập 2 giá trị khác nhau và submit.
3. Fail nếu không có field xác nhận, hoặc có mà không kiểm tra khớp.

## Expected result
- Có field "Xác nhận mật khẩu".
- Nhập không khớp với ô Mật khẩu → lỗi hiển thị trên nút submit.

## Status / Related bugs
Failed — BUG-32 (https://github.com/trngnneee/eshop-sut/issues/225)

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — kiểm thử thủ công trên trình duyệt Chrome
- Observed: Form đăng ký KHÔNG có field "Xác nhận mật khẩu" — thiếu cơ chế kiểm tra khớp mật khẩu.
- Execution result: **Failed**
- Screenshot: ![GUI-IA02-13](../screenshots/GUI-IA02-13.png)
