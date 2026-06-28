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



---

## FR-19: Quản lý Người dùng (Admin)

### [BUG][User Management] User thường có thể truy cập API quản lý người dùng của Admin

**Short Description:**
API quản lý người dùng của Admin không kiểm tra quyền truy cập theo role, dẫn đến việc tài khoản user thường vẫn có thể truy cập danh sách người dùng trong hệ thống bằng JWT Token hợp lệ.

**GitHub Issue:**
https://github.com/trngnneee/eshop-sut/issues/147#issue-4761377756

### [BUG][User Management] Admin có thể tự xóa chính tài khoản đang đăng nhập

**Short Description:**
Chức năng xóa người dùng không kiểm tra trường hợp Admin đang cố xóa chính tài khoản hiện tại, dẫn đến việc Admin có thể tự xóa tài khoản đang đăng nhập và làm mất quyền truy cập vào hệ thống.

**GitHub Issue:**
https://github.com/trngnneee/eshop-sut/issues/148#issue-4761415336

### [BUG][User Management] API xóa người dùng trả về thành công khi user_id không tồn tại

**Short Description:**
API xóa người dùng không kiểm tra sự tồn tại của `user_id` trước khi thực hiện thao tác xóa, dẫn đến việc hệ thống trả về trạng thái thành công giả (`200 OK`) mặc dù người dùng không tồn tại trong hệ thống.

**GitHub Issue:**
https://github.com/trngnneee/eshop-sut/issues/149#issue-4761431614


### [BUG][User Management] API xóa người dùng chấp nhận user_id không hợp lệ và trả về thành công

**Short Description:**
API xóa người dùng không kiểm tra tính hợp lệ của tham số `user_id` trước khi xử lý, dẫn đến việc hệ thống chấp nhận giá trị sai định dạng như chuỗi `"abc"` và trả về trạng thái thành công giả (`200 OK`) thay vì từ chối yêu cầu.

**GitHub Issue:**
https://github.com/trngnneee/eshop-sut/issues/150#issue-4762344302

### [BUG][User Management] Trang quản lý người dùng không có phân trang khi hiển thị nhiều tài khoản

**Short Description:**
Trang quản lý người dùng của Admin không hỗ trợ phân trang hoặc cơ chế tải dữ liệu phù hợp khi số lượng tài khoản lớn, dẫn đến việc hệ thống tải và render toàn bộ danh sách người dùng trong một lần, gây ảnh hưởng đến hiệu năng và khả năng quản lý dữ liệu.

**GitHub Issue:**
https://github.com/trngnneee/eshop-sut/issues/151#issue-4762361602


### [BUG][User Management] User thường có thể xóa tài khoản khác thông qua API Admin

**Short Description:**
API xóa người dùng của Admin không kiểm tra quyền authorization theo role, dẫn đến việc tài khoản user thường có thể sử dụng JWT Token hợp lệ để gọi API Admin và xóa tài khoản người dùng khác trong hệ thống, gây ra lỗ hổng Privilege Escalation.

**GitHub Issue:**
https://github.com/trngnneee/eshop-sut/issues/152#issue-4762394237

### [BUG][User Management] Xóa người dùng có dữ liệu liên quan nhưng không xử lý dữ liệu liên kết

**Short Description:**
Chức năng xóa người dùng không kiểm tra hoặc xử lý các dữ liệu liên kết trước khi xóa tài khoản, dẫn đến việc người dùng bị xóa thành công trong khi các dữ liệu liên quan như đơn hàng, giỏ hàng, lịch sử mua hàng vẫn tồn tại, gây ra dữ liệu mồ côi (orphan data) và làm sai lệch tính toàn vẹn dữ liệu.

**GitHub Issue:**
https://github.com/trngnneee/eshop-sut/issues/153#issue-4762495069
