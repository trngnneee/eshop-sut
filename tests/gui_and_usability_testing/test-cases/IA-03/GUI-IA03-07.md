# GUI-IA03-07: Link Quên mật khẩu điều hướng SPA, không reload cả trang

## Requirement ID
Heuristic (navigation consistency)

## Module / Test type / Technique
Điều hướng (Navigation) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA03-07 |
| Interface Aspect | Điều hướng (Navigation) |
| Actor | Người dùng cuối (khách) |
| Goal | Link Quên mật khẩu điều hướng SPA, không reload cả trang. |
| Screen(s) | Đăng nhập |
| Checklist item | Link "Quên mật khẩu?" điều hướng SPA không reload trang (hiện dùng `<a href>` — Login.jsx:49-51). |
| Traced to | Heuristic (navigation consistency) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI + Network tab |
| Endpoint / UI flow | /login |
| Input / Payload | Không có |
| Fixture | Không cần |

## Test steps
1. Mở `/login`, mở Network tab.
2. Bấm "Quên mật khẩu?", quan sát có full document request không.
3. Fail nếu trang reload toàn bộ (full page load).

## Expected result
- Bấm "Quên mật khẩu?" chuyển trang mượt như các link SPA khác.
- Trang không bị trắng/refresh toàn bộ.

## Status / Related bugs
Failed — BUG-37 (https://github.com/trngnneee/eshop-sut/issues/230)

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — kiểm thử thủ công trên trình duyệt Chrome + Network
- Observed: Link "Quên mật khẩu?" dùng <a href> gây tải lại toàn trang (cờ SPA đặt trước khi click đã mất) — không điều hướng kiểu SPA như các link khác.
- Execution result: **Failed**
- Screenshot: ![GUI-IA03-07](../screenshots/GUI-IA03-07.png)
