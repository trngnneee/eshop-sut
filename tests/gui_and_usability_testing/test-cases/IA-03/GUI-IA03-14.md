# GUI-IA03-14: Logo luôn điều hướng về trang chủ

## Requirement ID
Heuristic (logo home link) — kỳ vọng Pass

## Module / Test type / Technique
Điều hướng (Navigation) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA03-14 |
| Interface Aspect | Điều hướng (Navigation) |
| Actor | Người dùng cuối (khách) |
| Goal | Logo luôn điều hướng về trang chủ. |
| Screen(s) | Tất cả 8 màn hình |
| Checklist item | Logo "EShop" luôn về trang chủ từ mọi màn (App.jsx:21). |
| Traced to | Heuristic (logo home link) — kỳ vọng Pass |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI |
| Endpoint / UI flow | (8 màn hình khảo sát) |
| Input / Payload | Click logo |
| Fixture | Không cần |

## Test steps
1. Từ vài trang khác nhau, bấm logo "EShop".
2. Xác nhận điều hướng về `/`.
3. Fail nếu logo không dẫn về trang chủ.

## Expected result
- Click logo "EShop" từ bất kỳ trang nào đều về `/`.

## Status / Related bugs
Passed

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — kiểm thử thủ công trên trình duyệt Chrome
- Observed: Click logo "EShop" từ trang khác điều hướng đúng về trang chủ (/) — hoạt động như kỳ vọng.
- Execution result: **Passed**
- Screenshot: _(không có — test Passed)_
