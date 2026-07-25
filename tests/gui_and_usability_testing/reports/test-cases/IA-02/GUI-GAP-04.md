# GUI-GAP-04: Mọi label gắn với input qua htmlFor/id

## Requirement ID
Heuristic / WCAG 1.3.1, 4.1.2 (label association) — bổ sung thủ công

## Module / Test type / Technique
Biểu mẫu (Forms) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-GAP-04 |
| Interface Aspect | Biểu mẫu (Forms) |
| Actor | Người dùng cuối (khách) |
| Goal | Mọi label gắn với input qua htmlFor/id. |
| Screen(s) | Đăng nhập, Đăng ký, Quên MK, Hồ sơ |
| Checklist item | Mọi label gắn với input qua htmlFor/id — click nhãn focus vào ô nhập (hiện 0 label nào có htmlFor trên cả 4 form). |
| Traced to | Heuristic / WCAG 1.3.1, 4.1.2 (label association) — bổ sung thủ công |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.
- Đã đăng nhập bằng tài khoản `test@eshop.com` / `Test1234!`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI + screen reader |
| Endpoint / UI flow | /login , /register , /forgot-password , /profile |
| Input / Payload | Click vào text nhãn field |
| Fixture | Không cần |

## Test steps
1. Mở từng form.
2. Click vào chữ nhãn (vd "Mật khẩu") thay vì ô input.
3. Fail nếu con trỏ không nhảy vào ô input tương ứng.

## Expected result
- Click vào nhãn field → con trỏ focus vào ô input tương ứng.
- Screen reader đọc được tên field khi focus vào input.

## Status / Related bugs
Failed — BUG-22 (https://github.com/trngnneee/eshop-sut/issues/215)

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — kiểm thử thủ công trên trình duyệt Chrome
- Observed: Không label nào trên các form (Đăng nhập/Đăng ký/Quên MK/Hồ sơ) có thuộc tính htmlFor/for gắn với input — click nhãn không focus vào ô, screen reader không đọc được tên field (WCAG 1.3.1, 4.1.2).
- Execution result: **Failed**
- Screenshot: ![GUI-GAP-04](../screenshots/GUI-GAP-04.png)
