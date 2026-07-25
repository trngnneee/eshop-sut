# GUI-IA02-01: Mọi field bắt buộc có dấu * cạnh nhãn

## Requirement ID
FR-22 (required indicator)

## Module / Test type / Technique
Biểu mẫu (Forms) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA02-01 |
| Interface Aspect | Biểu mẫu (Forms) |
| Actor | Người dùng cuối (khách) |
| Goal | Mọi field bắt buộc có dấu * cạnh nhãn. |
| Screen(s) | Đăng ký, Đăng nhập, Quên MK, Hồ sơ |
| Checklist item | Mọi field `required` hiển thị dấu `*` cạnh nhãn (hiện không field nào có). |
| Traced to | FR-22 (required indicator) |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.
- Đã đăng nhập bằng tài khoản `test@eshop.com` / `Test1234!`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI |
| Endpoint / UI flow | /register , /login , /forgot-password , /profile |
| Input / Payload | Không có (quan sát tĩnh) |
| Fixture | Không cần |

## Test steps
1. Mở lần lượt 4 form.
2. Đối chiếu field có thuộc tính required với dấu * trên nhãn.
3. Fail cho từng field bắt buộc thiếu dấu *.

## Expected result
- Mỗi field bắt buộc có dấu `*` ngay cạnh nhãn trên cả 4 form.

## Status / Related bugs
Failed — BUG-24 (https://github.com/trngnneee/eshop-sut/issues/217)

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — kiểm thử thủ công trên trình duyệt Chrome
- Observed: Không field bắt buộc nào có dấu "*" cạnh nhãn trên các form (Đăng ký, Đăng nhập, Quên MK, Hồ sơ).
- Execution result: **Failed**
- Screenshot: ![GUI-IA02-01](../screenshots/GUI-IA02-01.png)
