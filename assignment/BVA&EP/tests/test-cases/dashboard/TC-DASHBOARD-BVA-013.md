# TC-DASHBOARD-BVA-013: Kiểm tra recent orders list đúng giới hạn hiển thị tối đa
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Positive / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công.
- Giao diện Dashboard được thiết lập giới hạn hiển thị `displayLimit` đơn hàng gần đây (ví dụ: 5 hoặc 10).
- Mock API trả về danh sách có số lượng đơn hàng đúng bằng `displayLimit`.
## Test data
- `recentOrders.length = displayLimit` (ví dụ: 5 hoặc 10 đơn hàng).
## Test steps
1. Seed hoặc Mock dữ liệu danh sách orders gần đây có số lượng đúng bằng giới hạn tối đa hiển thị.
2. Mở Dashboard và kiểm tra bảng recent orders.
## Expected result
- Bảng hiển thị đầy đủ và chính xác tất cả các đơn hàng trong danh sách.
- Không bị dư thừa hoặc thiếu hụt dòng nào.
- Layout không bị lỗi hoặc vỡ giao diện.
## Status / Related bugs
Pass / None
