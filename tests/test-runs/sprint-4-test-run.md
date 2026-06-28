# Test Run - Sprint 4 (Dashboard Module FR-13)

**Ngày thực hiện**: 28/06/2026  
**Người thực hiện**: Khoa  
**Môi trường thử nghiệm**: Local Backend API & Web Admin Frontend Source Code  

## Bảng kết quả thực thi (Test Run Table)

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [TC-DASHBOARD-DT-001](../test-cases/dashboard/TC-DASHBOARD-DT-001.md) | Dashboard | Khoa | Fail | BUG-FR13-C-01 | Giao diện Dashboard hiển thị Tổng doanh thu bị nhân đôi. |
| [TC-DASHBOARD-DT-002](../test-cases/dashboard/TC-DASHBOARD-DT-002.md) | Dashboard | Khoa | Pass | None | Khách vãng lai bị chặn truy cập giao diện dashboard. |
| [TC-DASHBOARD-DT-003](../test-cases/dashboard/TC-DASHBOARD-DT-003.md) | Dashboard | Khoa | Pass | None | Khách hàng thường bị chặn truy cập dashboard. |
| [TC-DASHBOARD-DT-004](../test-cases/dashboard/TC-DASHBOARD-DT-004.md) | Dashboard | Khoa | Fail | BUG-FR13-C-02 | Backend API /api/admin/orders và /api/admin/users thiếu kiểm soát phân quyền (role). |
| [TC-DASHBOARD-DT-005](../test-cases/dashboard/TC-DASHBOARD-DT-005.md) | Dashboard | Khoa | Pass | None | Thay đổi token hoặc hết hạn sẽ trả về lỗi xác thực. |
| [TC-DASHBOARD-DT-006](../test-cases/dashboard/TC-DASHBOARD-DT-006.md) | Dashboard | Khoa | Pass | None | Giao diện xử lý chính xác khi database trống (hiển thị 0). |
| [TC-DASHBOARD-DT-007](../test-cases/dashboard/TC-DASHBOARD-DT-007.md) | Dashboard | Khoa | Pass | None | Giao diện xử lý chính xác khi có các đơn hàng trạng thái khác delivered (không tính doanh thu). |
| [TC-DASHBOARD-DT-008](../test-cases/dashboard/TC-DASHBOARD-DT-008.md) | Dashboard | Khoa | Pass | None | Hiển thị thông báo lỗi thân thiện khi API orders bị lỗi 500. |
| [TC-DASHBOARD-DT-009](../test-cases/dashboard/TC-DASHBOARD-DT-009.md) | Dashboard | Khoa | Pass | None | Xử lý chính xác khi orders có số tiền âm (không cộng dồn hoặc hiển thị lỗi). |
| [TC-DASHBOARD-DT-010](../test-cases/dashboard/TC-DASHBOARD-DT-010.md) | Dashboard | Khoa | Pass | None | Xử lý chính xác khi orders có số tiền Null/NaN. |
| [TC-DASHBOARD-DT-011](../test-cases/dashboard/TC-DASHBOARD-DT-011.md) | Dashboard | Khoa | Pass | None | Xử lý chính xác khi API trả về sai cấu trúc dữ liệu (object thay vì array). |
| [TC-DASHBOARD-DT-012](../test-cases/dashboard/TC-DASHBOARD-DT-012.md) | Dashboard | Khoa | Pass | None | Giao diện co giãn tốt trên Mobile/Tablet. |
| [TC-DASHBOARD-BVA-001](../test-cases/dashboard/TC-DASHBOARD-BVA-001.md) | Dashboard | Khoa | Pass | None | Kiểm tra biên dưới của Tổng số đơn hàng bằng 0. |
| [TC-DASHBOARD-BVA-002](../test-cases/dashboard/TC-DASHBOARD-BVA-002.md) | Dashboard | Khoa | Pass | None | Kiểm tra biên dưới của Tổng số đơn hàng bằng 1. |
| [TC-DASHBOARD-BVA-003](../test-cases/dashboard/TC-DASHBOARD-BVA-003.md) | Dashboard | Khoa | Pass | None | Kiểm tra biên dưới hợp lệ ngoại lệ với đơn hàng âm (-1 đơn hàng). |
| [TC-DASHBOARD-BVA-004](../test-cases/dashboard/TC-DASHBOARD-BVA-004.md) | Dashboard | Khoa | Pass | None | Kiểm tra biên trên của Tổng số đơn hàng (100,000). |
| [TC-DASHBOARD-BVA-005](../test-cases/dashboard/TC-DASHBOARD-BVA-005.md) | Dashboard | Khoa | Pass | None | Kiểm tra biên dưới của doanh thu (0đ). |
| [TC-DASHBOARD-BVA-006](../test-cases/dashboard/TC-DASHBOARD-BVA-006.md) | Dashboard | Khoa | Fail | BUG-FR13-C-01 | Kiểm tra biên dưới của doanh thu (1đ), doanh thu bị nhân đôi thành 2đ. |
| [TC-DASHBOARD-BVA-007](../test-cases/dashboard/TC-DASHBOARD-BVA-007.md) | Dashboard | Khoa | Pass | None | Kiểm tra biên của doanh thu âm (-1đ). |
| [TC-DASHBOARD-BVA-008](../test-cases/dashboard/TC-DASHBOARD-BVA-008.md) | Dashboard | Khoa | Pass | None | Kiểm tra biên trên của doanh thu (999,999,999,999đ). |
| [TC-DASHBOARD-BVA-009](../test-cases/dashboard/TC-DASHBOARD-BVA-009.md) | Dashboard | Khoa | Pass | None | Kiểm tra biên API Response Time cận timeout (4900ms). |
| [TC-DASHBOARD-BVA-010](../test-cases/dashboard/TC-DASHBOARD-BVA-010.md) | Dashboard | Khoa | Pass | None | Kiểm tra biên API Response Time quá timeout (5100ms). |
| [TC-DASHBOARD-DT-013](../test-cases/dashboard/TC-DASHBOARD-DT-013.md) | Dashboard | Khoa | Fail | BUG-FR13-C-02 | Chặn user customer gọi API /api/admin/users. |
| [TC-DASHBOARD-DT-014](../test-cases/dashboard/TC-DASHBOARD-DT-014.md) | Dashboard | Khoa | Fail | BUG-FR13-C-02 | Chặn user customer gọi API /api/admin/orders. |
| [TC-DASHBOARD-DT-015](../test-cases/dashboard/TC-DASHBOARD-DT-015.md) | Dashboard | Khoa | Pass | None | Từ chối token bị đổi role nhưng sai signature. |
| [TC-DASHBOARD-DT-016](../test-cases/dashboard/TC-DASHBOARD-DT-016.md) | Dashboard | Khoa | Pass | None | Dashboard xử lý đúng khi API orders trả về mảng rỗng. |
| [TC-DASHBOARD-DT-017](../test-cases/dashboard/TC-DASHBOARD-DT-017.md) | Dashboard | Khoa | Fail | BUG-FR13-C-03 | Lỗi API /api/admin/users 500 ngắt toàn bộ tiến trình fetchData của dashboard. |
| [TC-DASHBOARD-DT-018](../test-cases/dashboard/TC-DASHBOARD-DT-018.md) | Dashboard | Khoa | Pass | None | Doanh thu bằng 0đ khi chỉ có đơn hàng pending. |
| [TC-DASHBOARD-DT-019](../test-cases/dashboard/TC-DASHBOARD-DT-019.md) | Dashboard | Khoa | Pass | None | Doanh thu không tính đơn hàng cancelled. |
| [TC-DASHBOARD-DT-020](../test-cases/dashboard/TC-DASHBOARD-DT-020.md) | Dashboard | Khoa | Fail | BUG-FR13-C-04 | Order thiếu total_amount dẫn đến tính toán ra NaN, UI hiển thị NaN ₫. |
| [TC-DASHBOARD-DT-021](../test-cases/dashboard/TC-DASHBOARD-DT-021.md) | Dashboard | Khoa | Pass | None | Không để lộ raw error hoặc stack trace trên giao diện khi API lỗi. |
| [TC-DASHBOARD-DT-022](../test-cases/dashboard/TC-DASHBOARD-DT-022.md) | Dashboard | Khoa | Pass | None | Các card dashboard điều hướng đúng sang trang quản lý tương ứng. |
| [TC-DASHBOARD-DT-023](../test-cases/dashboard/TC-DASHBOARD-DT-023.md) | Dashboard | Khoa | Fail | BUG-FR13-C-01 | Kiểm tra doanh thu không bị nhân đôi (Retest). |
| [TC-DASHBOARD-DT-024](../test-cases/dashboard/TC-DASHBOARD-DT-024.md) | Dashboard | Khoa | Fail | BUG-FR13-C-02 | Kiểm tra backend admin APIs đã kiểm tra role (Retest). |
| [TC-DASHBOARD-BVA-011](../test-cases/dashboard/TC-DASHBOARD-BVA-011.md) | Dashboard | Khoa | Pass | None | Recent orders list ở biên 0 item. |
| [TC-DASHBOARD-BVA-012](../test-cases/dashboard/TC-DASHBOARD-BVA-012.md) | Dashboard | Khoa | Pass | None | Recent orders list ở biên 1 item. |
| [TC-DASHBOARD-BVA-013](../test-cases/dashboard/TC-DASHBOARD-BVA-013.md) | Dashboard | Khoa | Pass | None | Recent orders list đúng giới hạn hiển thị tối đa. |
| [TC-DASHBOARD-BVA-014](../test-cases/dashboard/TC-DASHBOARD-BVA-014.md) | Dashboard | Khoa | Pass | None | Recent orders list vượt giới hạn hiển thị. |
| [TC-DASHBOARD-BVA-015](../test-cases/dashboard/TC-DASHBOARD-BVA-015.md) | Dashboard | Khoa | Pass | None | Doanh thu rất lớn không làm vỡ layout giao diện. |
| [TC-DASHBOARD-BVA-016](../test-cases/dashboard/TC-DASHBOARD-BVA-016.md) | Dashboard | Khoa | Pass | None | Doanh thu vượt giới hạn Number an toàn. |
| [TC-DASHBOARD-BVA-017](../test-cases/dashboard/TC-DASHBOARD-BVA-017.md) | Dashboard | Khoa | Pass | None | API response đúng ngưỡng timeout 5000ms. |
| [TC-DASHBOARD-BVA-018](../test-cases/dashboard/TC-DASHBOARD-BVA-018.md) | Dashboard | Khoa | Fail | BUG-FR13-C-05 | Hiển thị số lượng người dùng là số âm trên UI. |
| [TC-DASHBOARD-BVA-019](../test-cases/dashboard/TC-DASHBOARD-BVA-019.md) | Dashboard | Khoa | Fail | BUG-FR13-C-05 | Hiển thị số lượng sản phẩm là số thập phân trên UI. |
| [TC-DASHBOARD-BVA-020](../test-cases/dashboard/TC-DASHBOARD-BVA-020.md) | Dashboard | Khoa | Pass | None | Kiểm tra responsive tại đúng breakpoint tablet 768px. |
| [TC-DASHBOARD-BVA-021](../test-cases/dashboard/TC-DASHBOARD-BVA-021.md) | Dashboard | Khoa | Pass | None | Kiểm tra responsive tại 767px (tablet - 1px). |
| [TC-DASHBOARD-BVA-022](../test-cases/dashboard/TC-DASHBOARD-BVA-022.md) | Dashboard | Khoa | Pass | None | Kiểm tra responsive tại 769px (tablet + 1px). |

