# Bộ Test Case FR-11 - Xem Lịch Sử Đơn Hàng

Tính năng: FR-11 - Xem lịch sử đơn hàng của người dùng  
Phạm vi: Trang `/profile`, khu vực "Lịch sử đơn hàng", API `GET /api/orders/my-orders`  
Nguồn đặc tả: `README.md` mục FR-11, `api_specification.md` mục 4.4, ràng buộc trạng thái từ FR-10

## Tóm Tắt Yêu Cầu

- Người dùng đã đăng nhập chỉ xem được đơn hàng của chính mình.
- Mỗi đơn hàng cần hiển thị mã đơn, ngày đặt, tổng tiền và trạng thái hiện tại.
- Trạng thái phải được dịch sang tiếng Việt rõ ràng.
- Trạng thái phải có phân biệt màu sắc.
- API lịch sử đơn hàng yêu cầu token hợp lệ.
- Danh sách đơn hàng cá nhân được lấy từ `GET /api/orders/my-orders`.
- UI hiện tại đặt lịch sử đơn hàng trong trang hồ sơ `/profile`.

## Bảng Test Case

| TC ID | Loại | Tiêu đề | Tiền điều kiện | Các bước | Dữ liệu kiểm thử | Kết quả mong đợi | Độ ưu tiên | Trạng thái |
|---|---|---|---|---|---|---|---|---|
| TC-FR11-01 | Tích cực | User đã đăng nhập xem được bảng lịch sử đơn hàng | Backend/frontend đang chạy; user chính có ít nhất 3 đơn hàng | 1. Đăng nhập bằng user chính<br>2. Mở `/profile`<br>3. Chờ API lịch sử đơn hàng hoàn tất | data/fr11.json: primary_user_orders | Khu vực "Lịch sử đơn hàng" hiển thị bảng; bảng có ít nhất 3 dòng đơn hàng của user chính | Cao | Passed |
| TC-FR11-02 | Tích cực | Mỗi dòng đơn hiển thị đủ các trường bắt buộc | User chính đã đăng nhập và có dữ liệu đơn hàng | 1. Mở `/profile`<br>2. Kiểm tra từng dòng đơn hàng trong bảng | data/fr11.json: required_columns | Mỗi dòng có mã đơn, ngày đặt, tổng tiền và trạng thái hiện tại; không có ô bắt buộc bị rỗng | Cao | Passed |
| TC-FR11-03 | Tích cực | Mã đơn hiển thị theo đúng order id | User chính có các đơn đã setup qua API | 1. Mở `/profile`<br>2. So sánh mã đơn hiển thị với id trả về từ API | data/fr11.json: order_id_display | Mã đơn hiển thị có dạng `#<id>` và khớp với order id trong response `GET /api/orders/my-orders` | Cao | Passed |
| TC-FR11-04 | Tích cực | Tổng tiền hiển thị theo định dạng tiền tệ dễ đọc | User chính có đơn với các tổng tiền khác nhau | 1. Mở `/profile`<br>2. Kiểm tra cột tổng tiền của từng đơn | data/fr11.json: amount_format | Tổng tiền được format có phân cách hàng nghìn và đơn vị `₫`; giá trị số khớp `total_amount` từ API | Cao | Passed |
| TC-FR11-05 | Tích cực | Trạng thái `pending` được dịch tiếng Việt và có màu riêng | User chính có một đơn trạng thái `pending` | 1. Mở `/profile`<br>2. Tìm dòng đơn pending<br>3. Kiểm tra nhãn và class màu trạng thái | data/fr11.json: status_pending | Trạng thái hiển thị là `Chờ xác nhận` và có style nhóm màu vàng | Cao | Passed |
| TC-FR11-06 | Tích cực | Trạng thái `confirmed` được dịch tiếng Việt và có màu riêng | User chính có một đơn trạng thái `confirmed` | 1. Mở `/profile`<br>2. Tìm dòng đơn confirmed<br>3. Kiểm tra nhãn và class màu trạng thái | data/fr11.json: status_confirmed | Trạng thái hiển thị là `Đã xác nhận` và có style nhóm màu indigo | Cao | Passed |
| TC-FR11-07 | Tích cực | Trạng thái `shipping` được dịch tiếng Việt và có màu riêng | User chính có một đơn trạng thái `shipping` | 1. Mở `/profile`<br>2. Tìm dòng đơn shipping<br>3. Kiểm tra nhãn và class màu trạng thái | data/fr11.json: status_shipping | Trạng thái hiển thị là `Đang giao` và có style nhóm màu xanh dương | Cao | Passed |
| TC-FR11-08 | Tích cực | Trạng thái `delivered` được dịch tiếng Việt và có màu riêng | User chính có một đơn trạng thái `delivered` | 1. Mở `/profile`<br>2. Tìm dòng đơn delivered<br>3. Kiểm tra nhãn và class màu trạng thái | data/fr11.json: status_delivered | Trạng thái hiển thị là `Đã giao` và có style nhóm màu xanh lá | Cao | Passed |
| TC-FR11-09 | Tích cực | Trạng thái `canceled` được dịch tiếng Việt và có màu riêng | User chính có một đơn trạng thái `canceled` | 1. Mở `/profile`<br>2. Tìm dòng đơn canceled<br>3. Kiểm tra nhãn và class màu trạng thái | data/fr11.json: status_canceled | Trạng thái hiển thị là `Đã hủy` và có style nhóm màu đỏ | Cao | Passed |
| TC-FR11-10 | Bảo mật | User không thấy đơn hàng của user khác | User chính và user phụ đều có đơn hàng riêng | 1. Đăng nhập user chính<br>2. Mở `/profile`<br>3. So sánh danh sách trên UI/API với danh sách đơn của user phụ | data/fr11.json: other_user_isolation | Không có mã đơn hoặc tổng tiền đặc trưng của user phụ xuất hiện trong lịch sử của user chính | Nghiêm trọng | Passed |
| TC-FR11-11 | Tiêu cực | Chưa đăng nhập không xem được lịch sử đơn hàng qua UI | Local storage không có token | 1. Xóa token khỏi localStorage<br>2. Mở `/profile` | data/fr11.json: unauthenticated_profile | Trang hiển thị thông báo yêu cầu đăng nhập và không hiển thị bảng lịch sử đơn hàng | Cao | Passed |
| TC-FR11-12 | Tiêu cực | API lịch sử đơn hàng từ chối request không có token | Không gửi header Authorization | 1. Gọi `GET /api/orders/my-orders` không có token | data/fr11.json: api_without_token | API trả `401 Unauthorized` và không trả danh sách đơn hàng | Nghiêm trọng | Passed |
| TC-FR11-13 | Tiêu cực | API lịch sử đơn hàng từ chối token không hợp lệ | Gửi token sai định dạng/không verify được | 1. Gọi `GET /api/orders/my-orders` với token không hợp lệ | data/fr11.json: api_invalid_token | API trả `403 Forbidden` và không trả danh sách đơn hàng | Nghiêm trọng | Passed |
| TC-FR11-14 | Biên | User chưa có đơn hàng thấy empty state phù hợp | User rỗng đơn đã đăng nhập và chưa checkout | 1. Đăng nhập user chưa có đơn<br>2. Mở `/profile`<br>3. Chờ API lịch sử hoàn tất | data/fr11.json: empty_order_history | Không hiển thị bảng đơn hàng; hiển thị thông báo `Bạn chưa có đơn hàng nào.` | Trung bình | Passed |

## Checklist Bao Phủ

- [x] Có ít nhất 12 test case cho tính năng này
- [x] Có ít nhất một test case tích cực
- [x] Có ít nhất một test case tiêu cực
- [x] Có ít nhất một test case biên
- [x] Có kiểm tra phân quyền/chỉ xem đơn của chính mình
- [x] Có kiểm tra đủ 5 trạng thái đơn hàng
- [x] Kết quả mong đợi có thể kiểm tra khách quan
- [x] Mỗi test case map tới dữ liệu trong `data/fr11.json`
- [x] Có file Markdown riêng cho từng test case từ `TC-FR11-01.md` đến `TC-FR11-14.md`

## File Riêng Từng Test Case

- `docs/test-cases/TC-FR11-01.md`
- `docs/test-cases/TC-FR11-02.md`
- `docs/test-cases/TC-FR11-03.md`
- `docs/test-cases/TC-FR11-04.md`
- `docs/test-cases/TC-FR11-05.md`
- `docs/test-cases/TC-FR11-06.md`
- `docs/test-cases/TC-FR11-07.md`
- `docs/test-cases/TC-FR11-08.md`
- `docs/test-cases/TC-FR11-09.md`
- `docs/test-cases/TC-FR11-10.md`
- `docs/test-cases/TC-FR11-11.md`
- `docs/test-cases/TC-FR11-12.md`
- `docs/test-cases/TC-FR11-13.md`
- `docs/test-cases/TC-FR11-14.md`

## Ghi Chú Review Theo Đặc Tả

- Expected result bám đặc tả FR-11: chỉ xem đơn hàng của chính user, hiển thị mã đơn/ngày/tổng tiền/trạng thái, trạng thái tiếng Việt và phân biệt màu.
- Các case về nút hủy đơn không đưa vào bộ core của FR-11 vì thuộc hành vi liên quan FR-10; nếu cần có thể bổ sung sau như test liên thông.
- Format ngày chưa được README quy định, nên test chỉ kiểm tra ngày có hiển thị và parse được từ `created_at`, không ép định dạng cụ thể.
- Format tiền được kiểm tra theo hướng dễ đọc, có phân cách hàng nghìn và đơn vị `₫`, vì đặc tả yêu cầu hiển thị tổng tiền rõ ràng.
