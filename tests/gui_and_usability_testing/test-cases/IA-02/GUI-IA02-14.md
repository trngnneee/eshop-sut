# GUI-IA02-14: Thông báo bắt buộc nhập nhất quán tiếng Việt

## Requirement ID
Heuristic (validation timing/consistency)

## Module / Test type / Technique
Biểu mẫu (Forms) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA02-14 |
| Interface Aspect | Biểu mẫu (Forms) |
| Actor | Người dùng cuối (khách) |
| Goal | Thông báo bắt buộc nhập nhất quán tiếng Việt. |
| Screen(s) | Đăng ký, Đăng nhập, Quên MK |
| Checklist item | Thông báo bắt buộc nhập nhất quán tiếng Việt (hiện dựa HTML5 required native → tooltip theo ngôn ngữ trình duyệt, có thể tiếng Anh). |
| Traced to | Heuristic (validation timing/consistency) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI |
| Endpoint / UI flow | /register , /login , /forgot-password |
| Input / Payload | Submit form khi để trống field bắt buộc |
| Fixture | Không cần |

## Test steps
1. Mở từng form, để trống field bắt buộc rồi submit.
2. Quan sát ngôn ngữ và kiểu thông báo required.
3. Fail nếu tooltip tiếng Anh của trình duyệt (vd "Please fill out this field").

## Expected result
- Submit form để trống → thông báo "bắt buộc nhập" bằng tiếng Việt.
- Thông báo cùng style với các lỗi khác của app.

## Status / Related bugs
Failed — BUG-33 (https://github.com/trngnneee/eshop-sut/issues/226) · ⚠️ **Task 3: kết quả phụ thuộc trình duyệt** — Pass trên Chromium, Fail trên Firefox/WebKit (XP-01, issue #242); xem mục "Retest — Task 3" cuối file

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — kiểm thử thủ công trên trình duyệt Chrome
- Observed: Thông báo required dựa vào HTML5 native → hiển thị theo ngôn ngữ trình duyệt: "Please fill out this field." (tiếng Anh), không nhất quán tiếng Việt với các lỗi khác của app.
- Execution result: **Failed**
- Screenshot: ![GUI-IA02-14](../screenshots/GUI-IA02-14.png)

## Retest — Task 3 (28/07/2026)

- Kết quả đo lại **khác nhau theo platform** — đây là item duy nhất trong 66 item đổi hẳn Pass/Fail giữa các engine:

| Platform | `navigator.language` | Chuỗi engine hiện ra | Kết quả |
|---|---|---|---|
| Chromium 151 | `vi-VN` | "Vui lòng điền vào trường này." | ✅ Pass |
| Firefox 153 | `en-US` | "Please fill out this field." | ❌ Fail |
| WebKit 26.5 | `vi-VN` | "Fill out this field" | ❌ Fail |

- WebKit báo locale `vi-VN` mà vẫn hiện tiếng Anh → không sửa được bằng cách đặt locale; message này là chuỗi của trình duyệt, không phải của app.
- Báo cáo riêng thành XP-01 (issue #242, `cross_platform_testing/report.md` §3) bên cạnh BUG-33 của Task 1.
