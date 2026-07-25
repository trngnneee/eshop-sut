# GUI-IA01-08: Giá luôn là số có định dạng, không hiện NaN

## Requirement ID
FR-21 (định dạng tiền) + heuristic

## Module / Test type / Technique
Giao diện chung (General UI) / GUI/Usability / Checklist-based GUI Testing

## Checklist coverage
| Thuộc tính | Giá trị |
| :--- | :--- |
| Checklist ID | GUI-IA01-08 |
| Interface Aspect | Giao diện chung (General UI) |
| Actor | Người dùng cuối (khách) |
| Goal | Giá luôn là số có định dạng, không hiện NaN. |
| Screen(s) | Chi tiết SP |
| Checklist item | Giá luôn render là số có định dạng kể cả khi backend trả price sai kiểu (ProductDetail.jsx:49-52). |
| Traced to | FR-21 (định dạng tiền) + heuristic |

## Preconditions
- SUT đang chạy (`run_servers.sh`); Frontend Web khách hàng tại `localhost:5173`, backend tại `localhost:3000`.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Actor | Người dùng cuối (khách) |
| Interface | Frontend Web (khách) — UI |
| Endpoint / UI flow | /product/:id |
| Input / Payload | Sản phẩm có price hợp lệ và (nếu tạo được) price sai định dạng |
| Fixture | Sản phẩm seed id=1 |

## Test steps
1. Mở `/product/1`, quan sát giá.
2. Nếu tạo được fixture price lỗi định dạng, mở chi tiết sản phẩm đó.
3. Kiểm tra không xuất hiện "NaN".

## Expected result
- Giá hiển thị dạng số có phân cách + ₫.
- Không bao giờ hiển thị "NaN ₫".

## Status / Related bugs
Passed

## Actual result
- Executed by: Đặng Trường Nguyên
- Execution date: 2026-07-25
- Execution interface: Frontend Web (khách) — kiểm thử thủ công trên trình duyệt Chrome
- Observed: Giá sản phẩm hiển thị "30,000,000 ₫" — là số có định dạng, không xuất hiện "NaN" với dữ liệu seed hợp lệ.
- Execution result: **Passed**
- Screenshot: _(không có — test Passed)_
