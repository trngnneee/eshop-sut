# Locator Review - FR-11 Order History View

Nguồn DOM đã đọc: `frontend-web/src/pages/Profile.jsx`.

## Page Object

File: `tests/pages/OrderHistoryPage.js`

## Locator Inventory

| Element | Locator / Helper | Used by test cases | Stability |
|---|---|---|---|
| Trang profile | `page.goto("/profile")` | TC-FR11-01..11, TC-FR11-14 | Ổn định vì route được khai báo trong `App.jsx` |
| Thông báo chưa đăng nhập | `page.getByText("Vui lòng đăng nhập", { exact: false })` | TC-FR11-11 | Trung bình; phụ thuộc copy tiếng Việt |
| Heading hồ sơ | `page.getByRole("heading", { level: 2, name: "Hồ sơ của bạn" })` | hỗ trợ định vị trang | Trung bình; phụ thuộc text |
| Heading lịch sử | `page.getByRole("heading", { level: 2, name: "Lịch sử đơn hàng" })` | TC-FR11-01, TC-FR11-11, TC-FR11-14 | Trung bình; role tốt nhưng phụ thuộc text |
| Section lịch sử | `div.w-full.md\:w-2\/3.bg-white` filtered by heading | TC-FR11-01..10, TC-FR11-14 | Trung bình/thấp; phụ thuộc Tailwind class vì app chưa có `data-testid` |
| Empty state | `page.getByText("Bạn chưa có đơn hàng nào.", { exact: true })` | TC-FR11-14 | Trung bình; phụ thuộc copy |
| Bảng đơn hàng | `orderHistorySection.locator("table").first()` | TC-FR11-01..10 | Khá ổn trong phạm vi section |
| Header bảng | `ordersTable.locator("thead th")` và `headerByName(name)` | TC-FR11-02 | Khá ổn; dựa vào semantic table |
| Dòng đơn hàng | `ordersTable.locator("tbody tr")` | TC-FR11-01..10 | Khá ổn; dựa vào semantic table |
| Dòng theo mã đơn | `rowByOrderId(orderId)` | TC-FR11-03, TC-FR11-05..09 | Khá ổn nếu format mã đơn `#<id>` giữ nguyên |
| Dòng theo tổng tiền | `rowByAmountText(amountText)` | TC-FR11-04, TC-FR11-10 | Trung bình; phụ thuộc format tiền |
| Dòng theo trạng thái | `rowByStatusLabel(statusLabel)` | TC-FR11-05..09 | Trung bình; phụ thuộc label tiếng Việt |
| Cell mã đơn/ngày/tổng tiền/trạng thái/thao tác | `row.locator("td").nth(0..4)` | TC-FR11-02..10 | Khá ổn nếu thứ tự cột không đổi |
| Badge trạng thái | `orderStatusCell(row).locator("span").first()` | TC-FR11-05..09 | Khá ổn; badge hiện là `span` duy nhất trong cell trạng thái |
| Nút hủy đơn | `getByRole("button", { name: "Hủy đơn" })` trong action cell | quan sát liên quan FR-10 nếu cần | Trung bình; ngoài core FR-11 và phụ thuộc text |

## Review Notes

- App hiện chưa có `data-testid`, nên page object ưu tiên role/semantic locators trước, sau đó mới dùng CSS/Tailwind để khoanh vùng section.
- Các selector bảng dựa trên HTML semantic `table`, `thead`, `tbody`, `tr`, `td`; phù hợp với DOM hiện tại và ít phụ thuộc layout.
- Selector trạng thái dùng label tiếng Việt vì FR-11 yêu cầu kiểm tra bản dịch trạng thái. Đây là phụ thuộc có chủ đích.
- Locator section lịch sử là điểm yếu nhất vì dùng Tailwind class có ký tự escape (`md\:w-2\/3`). Nếu được phép sửa frontend, nên thêm `data-testid="order-history-section"`, `data-testid="orders-table"`, `data-testid="order-row-${id}"`, và `data-testid="order-status-${id}"`.
