# Task Scenario Draft

## 1. Kịch bản đọc cho participant

Sinh nhật em trai bạn sắp tới, và cậu ấy nhắc từ lâu là muốn có một chiếc **tai nghe chống ồn** để tập trung ôn thi. Bạn dự định chi khoảng **6–7 triệu đồng** cho món quà này. Bạn nghe nói cửa hàng trực tuyến **EShop** có bán đúng loại đó với giá hợp lý, nhưng bạn **chưa từng mua ở đây bao giờ**. Tuần trước, bạn nhận được email khuyến mãi của EShop kèm mã giảm giá **SAVE10**, và bạn muốn tận dụng nó để tiết kiệm được đồng nào hay đồng đó. Hãy mua món quà đó trên EShop. Vì cần quà đến kịp sinh nhật, trước khi rời đi bạn muốn **chắc chắn rằng đơn hàng của mình đã được cửa hàng ghi nhận**.

**"Hoàn thành" theo góc nhìn người dùng:** tự xác nhận được rằng đơn hàng đã được cửa hàng ghi nhận.

---

## 2. Bảng mapping scenario → flow (CHỈ cho moderator — không đọc cho participant)

| Yếu tố trong scenario | Bước flow được kích hoạt | Ghi chú quan sát |
|---|---|---|
| "chưa từng mua ở đây bao giờ" | Đăng ký (FR-01) | Điểm thu dữ liệu chính cho **O1**; không nói "hãy đăng ký" — quan sát xem họ tự nhận ra cần tài khoản lúc nào |
| "tai nghe chống ồn" | Tìm kiếm / danh sách (FR-05) | **O6**: từ khoá tự nhiên. "tai nghe" khớp tên sản phẩm; cụm đầy đủ "tai nghe chống ồn" nhiều khả năng ra 0 kết quả không có empty state (BUG-42) → là dữ liệu O6, không phải sự cố |
| "khoảng 6–7 triệu đồng" | Chi tiết sản phẩm (FR-06) | Buộc đối chiếu giá → AirPods Pro 2 (6.000.000₫) là đáp án tự nhiên duy nhất trong catalog seed |
| "mua món quà đó" | Thêm giỏ (FR-07) → Checkout (FR-08) | **O2**: quan sát bấm lặp / tự mở giỏ kiểm tra (BUG-16/17) |
| "mã giảm giá SAVE10 từ email" | Áp coupon (FR-09) | Đơn 6M ≥ 300k nên mã luôn đủ điều kiện; giảm 10% = 600.000₫ — đủ lớn để người dùng có động cơ kiểm tra tổng tiền |
| "chắc chắn đơn đã được ghi nhận" | Lịch sử đơn hàng (FR-11) | Không nói "vào lịch sử đơn hàng" — quan sát xem họ tự tìm bằng chứng ở đâu (BUG-20: giỏ không reset dễ gây hoang mang) |

---

## 3. Ghi chú thiết kế

- **Từ cấm đã kiểm tra:** scenario không chứa "nút", "menu", "biểu tượng", "trang", "tab", "click", "nhấn vào", không nhắc tên màn hình/thành phần giao diện nào của app.
- **Ràng buộc catalog:** seed chỉ có 5 sản phẩm, rẻ nhất 4.000.000₫ (Keychron Q1) → ngân sách kiểu "dưới 500k" như ví dụ trong đề là bất khả thi trên app này; ngân sách 6–7 triệu được neo vào AirPods Pro 2 (6.000.000₫). Ngưỡng 300k của SAVE10 luôn tự thoả với mọi sản phẩm.
- **Mã SAVE10 ghi thẳng trong scenario** ("nhận qua email" là cái cớ tự nhiên). Tuỳ chọn tăng độ thật: đưa mã trên tờ giấy rời như email in ra khi chạy session.
- Scenario chỉ định **loại** sản phẩm + ngân sách, không định **tên** sản phẩm — participant phải tự tìm và tự đối chiếu giá (phần việc của O6).

---

## 4. Bản sau pilot — quyết định chốt

Pilot được chạy gộp vào session P1 (Đặng Đăng Khoa, 21/07/2026) — buổi đó vừa là pilot vừa là session chính thức đầu tiên, cộng với dry-run của chính người thực hiện trước đó. Hạn chế của cách gộp này được khai rõ trong `report.md` mục 5 và 10.

**Kịch bản ở mục 1 được giữ nguyên, không chỉnh sửa, cho cả 7 session chính thức** — pilot (P1) không phát hiện chỗ nào phải sửa: participant hiểu goal ngay, không hỏi lại nghĩa, thời lượng nằm trong khung dự kiến; các session sau cũng không ghi nhận ai hiểu sai kịch bản. Các mục "trước → sau pilot" vì vậy không phát sinh. Việc dùng đúng một bản kịch bản xuyên suốt cũng giữ cho 7 session so sánh được với nhau.
