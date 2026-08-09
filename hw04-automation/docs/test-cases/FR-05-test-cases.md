# Bộ Test Case FR-05 - Xem Danh Sách Và Tìm Kiếm Sản Phẩm

Tính năng: FR-05 - Xem danh sách và tìm kiếm sản phẩm  
Phạm vi: Trang chủ web, danh sách sản phẩm dạng lưới và chức năng tìm kiếm theo tên sản phẩm  
Nguồn đặc tả: `README.md`, mục FR-05

## Tóm Tắt Yêu Cầu

- Trang chủ hiển thị danh sách tất cả sản phẩm dạng lưới.
- Mỗi sản phẩm hiển thị ảnh đúng tỷ lệ, có `alt` mô tả, tên sản phẩm và giá.
- Giá dùng đơn vị `₫` và có định dạng phân cách hàng nghìn.
- Thanh tìm kiếm tìm theo tên sản phẩm.
- Từ khóa tìm kiếm phải được hiển thị an toàn, không render HTML.
- Khi đang tải dữ liệu phải hiển thị trạng thái loading.
- Khi không có kết quả tìm kiếm phải hiển thị empty state phù hợp.
- Trang chủ chỉ có đúng một thẻ `<h1>`.

## Bảng Test Case

| TC ID | Loại | Tiêu đề | Tiền điều kiện | Các bước | Dữ liệu kiểm thử | Kết quả mong đợi | Độ ưu tiên | Trạng thái |
|---|---|---|---|---|---|---|---|---|
| TC-FR05-01 | Tích cực | Hiển thị tất cả sản phẩm trên trang chủ | Backend và frontend đang chạy; dữ liệu seed đã tồn tại | 1. Mở trang chủ<br>2. Chờ request lấy sản phẩm hoàn tất | data/fr05.json: all_products | Lưới sản phẩm hiển thị và chứa đầy đủ các sản phẩm seed | Cao | Chưa chạy |
| TC-FR05-02 | Tích cực | Thẻ sản phẩm hiển thị đầy đủ thông tin bắt buộc | Trang chủ đã tải xong danh sách sản phẩm | 1. Mở trang chủ<br>2. Kiểm tra từng thẻ sản phẩm | data/fr05.json: all_products | Mỗi thẻ sản phẩm có ảnh, tên, giá định dạng đúng, nút xem chi tiết và nút thêm vào giỏ | Cao | Chưa chạy |
| TC-FR05-03 | Tích cực | Giá sản phẩm hiển thị đúng đơn vị và phân cách hàng nghìn | Trang chủ đã tải xong danh sách sản phẩm | 1. Mở trang chủ<br>2. Kiểm tra văn bản giá của các sản phẩm | data/fr05.json: price_format | Giá hiển thị theo đặc tả, ví dụ `30.000.000 ₫`, không dùng `VND` | Cao | Chưa chạy |
| TC-FR05-04 | Tích cực | Tìm kiếm bằng đúng tên sản phẩm | Trang chủ đang mở | 1. Nhập đúng tên sản phẩm<br>2. Gửi form tìm kiếm | data/fr05.json: exact_match | Chỉ sản phẩm khớp được hiển thị; phần tóm tắt tìm kiếm hiển thị đúng từ khóa | Cao | Chưa chạy |
| TC-FR05-05 | Tích cực | Tìm kiếm bằng một phần tên sản phẩm | Trang chủ đang mở | 1. Nhập một phần tên sản phẩm<br>2. Gửi form tìm kiếm | data/fr05.json: partial_match | Tất cả sản phẩm có tên chứa từ khóa được hiển thị | Cao | Chưa chạy |
| TC-FR05-06 | Biên | Tìm kiếm không có kết quả phù hợp | Trang chủ đang mở | 1. Nhập từ khóa không khớp sản phẩm nào<br>2. Gửi form tìm kiếm | data/fr05.json: no_result | Không có thẻ sản phẩm nào hiển thị và có thông báo empty state phù hợp | Cao | Chưa chạy |
| TC-FR05-07 | Biên | Tìm kiếm với từ khóa rỗng | Trang chủ đang mở | 1. Xóa nội dung ô tìm kiếm<br>2. Gửi form tìm kiếm | data/fr05.json: empty_keyword | Toàn bộ danh sách sản phẩm được hiển thị lại | Trung bình | Chưa chạy |
| TC-FR05-08 | Biên | Tìm kiếm với từ khóa có khoảng trắng đầu/cuối | Trang chủ đang mở | 1. Nhập từ khóa có khoảng trắng ở đầu và cuối<br>2. Gửi form tìm kiếm | data/fr05.json: padded_keyword | Hệ thống xử lý ổn định, không lỗi giao diện hoặc lỗi API, loại bỏ khoảng trắng ở đầu và cuối từ khóa trước khi thực hiện tìm kiếm | Trung bình | Chưa chạy |
| TC-FR05-09 | Tiêu cực | Từ khóa chứa HTML phải được hiển thị an toàn | Trang chủ đang mở | 1. Nhập payload HTML<br>2. Gửi form tìm kiếm<br>3. Kiểm tra phần tóm tắt tìm kiếm | data/fr05.json: html_payload | Payload được hiển thị như văn bản thường; không có phần tử HTML bị chèn vào DOM | Nghiêm trọng | Chưa chạy |
| TC-FR05-10 | Tiêu cực | Từ khóa chứa script không được thực thi | Trang chủ đang mở | 1. Nhập payload script<br>2. Gửi form tìm kiếm<br>3. Kiểm tra dialog và trạng thái trang | data/fr05.json: script_payload | Script không được thực thi và trang vẫn sử dụng bình thường | Nghiêm trọng | Chưa chạy |
| TC-FR05-11 | Tiêu cực | Payload kiểu SQL injection không được trả về dữ liệu ngoài phạm vi tìm kiếm | Trang chủ đang mở | 1. Nhập payload kiểu SQL injection<br>2. Gửi form tìm kiếm<br>3. So sánh danh sách sản phẩm trả về | data/fr05.json: sql_payload | API không lỗi và không trả về toàn bộ sản phẩm ngoài hành vi tìm kiếm mong đợi | Nghiêm trọng | Chưa chạy |
| TC-FR05-12 | Khả năng truy cập | Ảnh sản phẩm có alt text mô tả | Trang chủ đã tải xong danh sách sản phẩm | 1. Mở trang chủ<br>2. Kiểm tra tất cả ảnh sản phẩm | data/fr05.json: all_products | Mỗi ảnh sản phẩm có `alt` khác rỗng và mô tả đúng sản phẩm | Trung bình | Chưa chạy |
| TC-FR05-13 | HTML ngữ nghĩa | Trang chủ chỉ có đúng một thẻ h1 | Trang chủ đã tải xong danh sách sản phẩm | 1. Mở trang chủ<br>2. Đếm số thẻ `<h1>` trong document | data/fr05.json: h1_rule | Trang chỉ có đúng một thẻ `<h1>` | Trung bình | Chưa chạy |
| TC-FR05-14 | Trạng thái tải | Hiển thị loading khi đang tải dữ liệu sản phẩm | Có thể delay hoặc intercept response của API sản phẩm | 1. Delay response API sản phẩm<br>2. Mở trang chủ<br>3. Quan sát UI trước khi response hoàn tất | data/fr05.json: delayed_api | Loading indicator hiển thị trong lúc chờ dữ liệu | Trung bình | Chưa chạy |
| TC-FR05-15 | Bảo mật/biên | Payload `<image onerror>` không được render hoặc thực thi | Trang chủ đang mở | 1. Nhập payload `<image src=1 href=1 onerror="javascript:alert(1)"></image>`<br>2. Gửi form tìm kiếm<br>3. Quan sát dialog và DOM summary | data/fr05.json: image_onerror_payload | Payload hiển thị như text; không có dialog `alert(1)`; không có element `image`/`img[src="1"]` được chèn vào summary | Nghiêm trọng | Chưa chạy |
| TC-FR05-16 | Biên | Tìm kiếm bằng từ khóa rất dài | Trang chủ đang mở | 1. Nhập keyword dài trong data file<br>2. Gửi form tìm kiếm<br>3. Quan sát summary, error panel và danh sách kết quả | data/fr05.json: long_keyword | Không lỗi UI/API; không hiện error panel; summary hiển thị keyword an toàn; không có sản phẩm phù hợp | Trung bình | Chưa chạy |
| TC-FR05-17 | Biên | Tìm kiếm bằng từ khóa Unicode/emoji | Trang chủ đang mở | 1. Nhập keyword Unicode/emoji<br>2. Gửi form tìm kiếm<br>3. Quan sát summary, error panel và danh sách kết quả | data/fr05.json: unicode_keyword | Không lỗi UI/API; summary hiển thị đúng Unicode/emoji; không có sản phẩm phù hợp nếu không có match | Trung bình | Chưa chạy |

## Checklist Bao Phủ

- [x] Có ít nhất 12 test case cho tính năng này; sau review bổ sung thành 17 test case
- [x] Có ít nhất một test case tích cực
- [x] Có ít nhất một test case tiêu cực
- [x] Có ít nhất một test case biên
- [x] Kết quả mong đợi có thể kiểm tra khách quan
- [x] Mỗi test case map tới dữ liệu trong `data/fr05.json`

## Ghi Chú Review Theo Đặc Tả

- Expected result phải theo đặc tả FR-05 trong README, không theo code hiện tại.
- Giá mong đợi dùng đơn vị `₫` và phân cách hàng nghìn theo dạng `30.000.000 ₫`.
- Nếu code hiện tại hiển thị `30,000,000 VND`, test phải fail và được xem là bug so với đặc tả.
- Các case về HTML/script payload kiểm tra yêu cầu “từ khóa tìm kiếm phải được hiển thị an toàn”.
- Các case loading, empty state, alt text và số lượng `<h1>` đều xuất phát trực tiếp từ FR-05.
