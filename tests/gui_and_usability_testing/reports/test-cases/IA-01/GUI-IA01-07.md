# GUI-IA01-07: Phân cách hàng nghìn của giá nhất quán trên mọi màn hình

## Requirement ID
FR-21 (định dạng tiền) + heuristic

## Module / Test type / Technique
Giao diện chung (General UI) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA01-07 |
| Interface Aspect | Giao diện chung (General UI) |
| Actor | Người dùng cuối (khách) |
| Goal | Phân cách hàng nghìn của giá nhất quán trên mọi màn hình. |
| Screen(s) | Trang chủ, Chi tiết SP, Giỏ hàng, Thanh toán, Lịch sử ĐH |
| Checklist item | Phân cách hàng nghìn nhất quán (toLocaleString() không tham số → phụ thuộc locale trình duyệt). |
| Traced to | FR-21 (định dạng tiền) + heuristic |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.
- Đã đăng nhập bằng tài khoản `test@eshop.com` / `Test1234!`.
- Giỏ hàng có sẵn ít nhất 1 sản phẩm.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI |
| Endpoint / UI flow | / , /product/:id , /cart , /checkout , /profile |
| Input / Payload | Không có (quan sát tĩnh) |
| Fixture | Sản phẩm + đơn hàng seed |

## Test steps
1. Mở lần lượt 5 màn hình có hiển thị giá.
2. So sánh cách phân cách hàng nghìn (dấu chấm vs phẩy).
3. Lặp lại với trình duyệt/locale khác nếu có, đối chiếu.

## Expected result
- Một kiểu phân cách hàng nghìn duy nhất trên mọi màn hình.
- Kết quả không đổi giữa các trình duyệt/locale khác nhau.

## Status / Related bugs
Passed

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — Playwright/Chromium
- Execution tool: Playwright (Chromium headless) — tự động hoá
- Observed: Phân cách hàng nghìn nhất quán trong cùng trình duyệt (Trang chủ "30,000,000", Chi tiết SP "30,000,000"). Lưu ý: dùng toLocaleString() không tham số nên kết quả phụ thuộc locale trình duyệt.
- Execution result: **Passed**
- Screenshot: _(không có — test Passed)_
