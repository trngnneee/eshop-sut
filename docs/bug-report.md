## FR-05: Xem danh sách & Tìm kiếm sản phẩm

### [BUG][Product] Giá sản phẩm không hiển thị đúng định dạng tiền tệ Việt Nam

**Short Description:**  
Lỗi hiển thị đơn vị tiền tệ của sản phẩm. Giá sản phẩm hiển thị là 28,000,000 VND. Nhưng theo đặc tả thì giá được hiển thị theo định dạng tiền tệ Việt Nam, có ký hiệu ₫ và phân cách hàng nghìn.

**GitHub Issue:**  
https://github.com/trngnneee/eshop-sut/issues/25#issue-4746056657


### [BUG][Product] Hình ảnh sản phẩm lỗi không hiển thị nội dung thay thế

**Short Description:**  
Khi hình ảnh sản phẩm không tải được thì không hiển thị nội dung mô tả thay thế.

**GitHub Issue:**  
https://github.com/trngnneee/eshop-sut/issues/26#issue-4746328476


### [BUG][Product] Trang hiển thị màn hình trắng khi đang tải dữ liệu

**Short Description:**  
Lỗi hiển thị trạng thái loading. Trang hiển thị màn hình trắng cho đến khi dữ liệu được tải xong.

**GitHub Issue:**  
https://github.com/trngnneee/eshop-sut/issues/27#issue-4746377610


### [BUG][Product] Không hiển thị thông báo khi danh sách sản phẩm trống

**Short Description:**  
Khi không có sản phẩm thì trang hiển thị màn hình trắng, không hiển thị thông tin là không có sản phẩm cho người dùng.

**GitHub Issue:**  
https://github.com/trngnneee/eshop-sut/issues/28#issue-4746603879


### [BUG][Product] Trang chủ chứa nhiều hơn một thẻ h1

**Short Description:**  
Trang chủ có đến 2 thẻ `<h1>`. Trong khi đặc tả yêu cầu trang chủ chỉ có đúng một thẻ `<h1>`.

**GitHub Issue:**  
https://github.com/trngnneee/eshop-sut/issues/29#issue-4746987185


### [BUG][Search] Trang kết quả tìm kiếm chứa nhiều hơn một thẻ h1

**Short Description:**  
Sau khi tìm kiếm sản phẩm, trang kết quả hiển thị có 2 thẻ `<h1>`. Trong khi đặc tả yêu cầu mỗi trang chỉ có 1 thẻ `<h1>` duy nhất.

**GitHub Issue:**  
https://github.com/trngnneee/eshop-sut/issues/30#issue-4747029719


### [BUG][Search] Chức năng tìm kiếm không sanitize input dẫn đến XSS vulnerability

**Short Description:**  
Chức năng tìm kiếm không sanitize input, dẫn đến việc JavaScript trong dữ liệu nhập vào được thực thi trên trình duyệt.

**GitHub Issue:**  
https://github.com/trngnneee/eshop-sut/issues/53#issue-4748338316


### [BUG][Search] Chức năng tìm kiếm không xử lý input đặc biệt dẫn đến SQL Injection vulnerability

**Short Description:**  
Chức năng tìm kiếm không xử lý đúng input đặc biệt, dẫn đến điều kiện truy vấn bị thay đổi và trả về toàn bộ dữ liệu sản phẩm trong database.

**GitHub Issue:**  
https://github.com/trngnneee/eshop-sut/issues/60#issue-4753686069


---

## FR-11: Xem lịch sử đơn hàng (User)

### [BUG][Order History] API lịch sử đơn hàng bỏ qua tham số phân trang

**Short Description:**  
Chức năng xem lịch sử đơn hàng không xử lý tham số phân trang (`page`, `limit`), dẫn đến API trả về toàn bộ danh sách đơn hàng thay vì giới hạn dữ liệu theo từng trang.

**GitHub Issue:**  
https://github.com/trngnneee/eshop-sut/issues/64#issue-4758846657


### [BUG][Order History] API xem chi tiết đơn hàng không yêu cầu xác thực người dùng

**Short Description:**  
Chức năng xem chi tiết đơn hàng không yêu cầu xác thực người dùng, dẫn đến việc người dùng chưa đăng nhập vẫn có thể truy cập dữ liệu đơn hàng bằng Order ID hợp lệ.

**GitHub Issue:**  
https://github.com/trngnneee/eshop-sut/issues/65#issue-4758951568