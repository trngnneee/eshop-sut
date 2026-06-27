# HW02 – Báo cáo Kiểm thử Phần mềm

---

# 1. Giới thiệu

## 1.1 Thông tin sinh viên
- Họ và tên: Nguyễn Thanh Gia Bảo
- Mã số sinh viên: 23127158
- Lớp: 23KTPM3
- Môn học: Kiểm thử phần mềm
- Giảng viên: [Lecturer Name]

## 1.2 Thông tin bài tập
- Bài tập: HW02 – Domain Testing & Boundary Value Analysis
- Dự án: Hệ thống EShop
- Phạm vi: Kiểm thử các yêu cầu chức năng (FRs)

---

# 2. FR-05: Xem danh sách & Tìm kiếm sản phẩm

## 2.1 Tổng quan yêu cầu
Trang chủ hiển thị danh sách tất cả sản phẩm dạng lưới. Mỗi sản phẩm phải có ảnh, tên sản phẩm, giá hiển thị theo định dạng tiền tệ Việt Nam. Thanh tìm kiếm cho phép tìm theo tên sản phẩm. Trạng thái loading, empty state, an toàn khi hiển thị từ khóa tìm kiếm và quy định chỉ có đúng một thẻ h1 trên mỗi trang đều là yêu cầu bắt buộc.

## 2.2 Domain Testing
Với FR-05, kỹ thuật này được áp dụng cho từ khóa tìm kiếm, nội dung hiển thị trên card sản phẩm và số lượng thẻ h1 trên trang.

### Phân tích miền dữ liệu

| Biến | Domain | Loại giá trị | Khoảng giá trị | Mô tả |
|-|-|-|-|-|
| Từ khóa tìm kiếm | Chuỗi ký tự | Hợp lệ | Bất kỳ chuỗi tên sản phẩm hợp lệ | Dùng để tìm sản phẩm theo tên. |
| Từ khóa tìm kiếm | Chuỗi ký tự | Không hợp lệ / rủi ro bảo mật | Chuỗi chứa HTML/JS như `<script>`, `<img onerror=...>` | Phải được hiển thị an toàn, không render HTML. |
| Từ khóa tìm kiếm | Chuỗi ký tự | Không xác định trong đặc tả | Chuỗi có khoảng trắng đầu/cuối, chuỗi rất dài | Đặc tả không định nghĩa quy tắc này. |
| Số lượng h1 trên trang | Số nguyên | Hợp lệ | 1 | Trang chỉ được có đúng một h1 duy nhất. |
| Số lượng h1 trên trang | Số nguyên | Không hợp lệ | 0 hoặc lớn hơn 1 | Phát hiện lỗi cấu trúc trang và lỗi truy cập. |
| Alt text ảnh sản phẩm | Chuỗi ký tự | Hợp lệ | Chuỗi mô tả ngắn, rõ nghĩa | Ảnh phải có alt text mô tả. |
| Alt text ảnh sản phẩm | Chuỗi ký tự | Không hợp lệ | Rỗng hoặc null | Không đáp ứng yêu cầu mô tả ảnh. |
| Giá sản phẩm hiển thị | Số tiền | Hợp lệ | Giá dương đã định dạng theo ₫ | Hiển thị giá theo chuẩn tiền tệ Việt Nam. |
| Trạng thái dữ liệu | Trạng thái giao diện | Hợp lệ | loading, empty state, danh sách sản phẩm | Phải phản hồi đúng theo trạng thái dữ liệu. |


### Quy trình phân tích

1. Xác định input cần kiểm thử: 
    * Từ khóa tìm kiếm.
    * Số lượng thẻ h1.
    * Nội dung alt text. 
    * Giá sản phẩm.
    * Trạng thái giao diện.
2. Xác định miền giá trị của input: 
    * Chuỗi tìm kiếm hợp lệ/không hợp lệ.
    * Số lượng h1 (0, 1, >1).
    * Alt text hợp lệ/rỗng.
    * Giá đã định dạng.
    * Các trạng thái loading/empty/list.
3. Xác định dữ liệu hợp lệ:
    * Tên sản phẩm hợp lệ.
    * Hiển thị đúng 1 thẻ h1.
    * Alt text có mô tả rõ ràng.
    * Giá hiển thị đúng định dạng tiền tệ ₫.
    * Trạng thái giao diện hợp lệ (loading, empty, có dữ liệu).
4. Xác định dữ liệu không hợp lệ:
    * Input chứa HTML/JS không được sanitize.
    * Số lượng h1 bằng 0 hoặc lớn hơn 1.
    * Alt text rỗng hoặc null.
    * Dữ liệu không hiển thị hoặc hiển thị sai định dạng.
5. Xác định các trường hợp cần kiểm thử:
    * Hiển thị danh sách sản phẩm.
    * Tìm kiếm sản phẩm.
    * Empty state khi không có dữ liệu.
    * Loading state khi đang tải dữ liệu.
    * Kiểm tra an toàn hiển thị dữ liệu (XSS).
    * Kiểm tra cấu trúc DOM (h1, layout).


## 2.3 Boundary Value Analysis
FR-05 không định nghĩa giới hạn số lượng ký tự của từ khóa tìm kiếm nên không có biên min/max cho trường này. Biên giá trị rõ ràng nhất của FR-05 là số lượng thẻ h1 trên mỗi trang phải bằng 1. Do đó, BVA được áp dụng cho quy tắc này để kiểm tra các giá trị sát biên:

- min-1: 0 h1
- min: 1 h1
- min+1: 2 h1

### Phân tích boundary

| Biến | Constraint | Boundary | Ý nghĩa |
|-|-|-|-|
| Số lượng h1 trên trang | Chính xác 1 | 0 | Phát hiện thiếu heading chính. |
| Số lượng h1 trên trang | Chính xác 1 | 1 | Trạng thái đúng theo yêu cầu. |
| Số lượng h1 trên trang | Chính xác 1 | 2 | Phát hiện trùng heading chính. |

### Vì sao chọn boundary này

- 0 h1 cho thấy trang thiếu heading chính, có thể ảnh hưởng đến khả năng truy cập và SEO.
- 1 h1 là giá trị hợp lệ duy nhất theo đặc tả.
- 2 h1 cho thấy trang có heading chính trùng lặp, làm sai cấu trúc tài liệu.

### Boundary này có thể phát hiện lỗi gì

- Lỗi render cấu trúc trang.
- Lỗi điều hướng nội dung hoặc component lồng sai.
- Lỗi accessibility liên quan đến heading hierarchy.

## 2.4 Danh sách test case


| Test Case ID | Mục tiêu kiểm thử | Kỹ thuật |
|---|---|---|
| TC-PRODUCT-001 | Hiển thị danh sách sản phẩm dạng grid | Domain Testing |
| TC-PRODUCT-002 | Hiển thị tên sản phẩm trên card | Domain Testing |
| TC-PRODUCT-003 | Hiển thị giá đúng định dạng ₫ và phân cách hàng nghìn | Domain Testing |
| TC-PRODUCT-004 | Hiển thị ảnh sản phẩm với alt text mô tả | Domain Testing |
| TC-PRODUCT-005 | Hiển thị trạng thái loading khi dữ liệu đang tải | Domain Testing |
| TC-PRODUCT-006 | Hiển thị empty state khi không có kết quả tìm kiếm (Boundary: 0 sản phẩm) | Boundary Value Analysis |
| TC-PRODUCT-007 | Tìm kiếm theo tên sản phẩm hợp lệ | Domain Testing |
| TC-PRODUCT-008 | Hiển thị an toàn từ khóa chứa HTML không render nội dung HTML | Domain Testing |
| TC-PRODUCT-009 | Kiểm tra trang chủ chỉ có đúng một thẻ h1 (Boundary: 1 h1) | Boundary Value Analysis |
| TC-PRODUCT-010 | Kiểm tra trang kết quả tìm kiếm chỉ có đúng một thẻ h1 | Boundary Value Analysis |
| TC-PRODUCT-011 | Kiểm tra lưới hiển thị đầy đủ tất cả sản phẩm trả về | Domain Testing |
| TC-PRODUCT-012 | Kiểm tra ảnh sản phẩm hiển thị đúng tỷ lệ, không bị méo | Domain Testing |
| TC-PRODUCT-013 | Kiểm tra XSS injection qua input tìm kiếm không được thực thi JavaScript | Domain Testing |
| TC-PRODUCT-014 | Kiểm tra SQL Injection không làm thay đổi logic tìm kiếm sản phẩm | Domain Testing |


## 2.5 Phân tích khoảng trống kiểm thử do AI hỗ trợ

### Bổ sung test case bị AI bỏ sót

| Test Case ID | Test Objective | Testing Technique | Lý do bổ sung |
|---|---|---|---|
| TC-PRODUCT-013 | Kiểm tra XSS injection qua input tìm kiếm không được thực thi JavaScript | Domain Testing | Kiểm tra trường hợp input chứa payload JavaScript nâng cao, đảm bảo dữ liệu người dùng được xử lý an toàn trước khi hiển thị trên UI. |
| TC-PRODUCT-014 | Kiểm tra SQL Injection không làm thay đổi logic tìm kiếm sản phẩm | Domain Testing | Kiểm tra khả năng xử lý input đặc biệt có thể ảnh hưởng đến câu truy vấn backend, đảm bảo dữ liệu tìm kiếm không bị thay đổi ngoài mong muốn. |


### AI Gap Analysis - Lý do AI bỏ sót 2 test case

| Test Case bị bỏ sót | Lý do AI có thể bỏ sót |
|---|---|
| TC-PRODUCT-013 | AI chỉ tạo test case XSS ở mức cơ bản với các thẻ HTML/JavaScript đơn giản. AI chưa sinh thêm các payload thực tế như event handler (`onerror`) do prompt ban đầu chưa yêu cầu kiểm thử security nâng cao hoặc các trường hợp exploit phức tạp. |
| TC-PRODUCT-014 | AI tập trung phân tích chức năng tìm kiếm ở góc nhìn frontend (nhập từ khóa và hiển thị kết quả), nhưng chưa mở rộng sang hành vi xử lý dữ liệu ở backend/database. Việc bỏ sót xảy ra do requirement không mô tả trực tiếp về query database và cần có tư duy kiểm thử bảo mật bổ sung. |


### Tổng kết

AI đã bao phủ được các test case chính liên quan đến:
- Hiển thị danh sách sản phẩm.
- Hiển thị thông tin sản phẩm.
- Tìm kiếm theo tên sản phẩm.
- Các trạng thái giao diện như loading và empty state.
- Kiểm tra cấu trúc HTML của trang.

Tuy nhiên, AI còn thiếu các kiểm thử mở rộng về:
- Security testing với payload thực tế.
- Khả năng xử lý input không an toàn.
- Kiểm tra tương tác giữa frontend input và backend query.

Các test case bổ sung giúp tăng độ bao phủ về **bảo mật và input validation** cho FR-05.


# 3. FR-11: Xem lịch sử đơn hàng (User)

## 3.1 Tổng quan yêu cầu

Chức năng cho phép người dùng đã đăng nhập xem lịch sử các đơn hàng của chính mình.
Danh sách đơn hàng phải hiển thị đầy đủ các thông tin quan trọng như mã đơn, ngày đặt, tổng tiền và trạng thái hiện tại.

Hệ thống phải đảm bảo:

* Người dùng chỉ được xem đơn hàng thuộc tài khoản của mình.
* Người chưa đăng nhập không được truy cập dữ liệu đơn hàng.
* Trạng thái đơn hàng phải được dịch sang tiếng Việt và hiển thị màu sắc phân biệt.
* Hệ thống phải xử lý đúng khi người dùng có 0 hoặc nhiều đơn hàng.


## 3.2 Domain Testing

Với FR-11, Domain Testing được áp dụng để phân tích các input liên quan đến authentication, authorization, dữ liệu đơn hàng và trạng thái đơn hàng.

### Phân tích miền dữ liệu

| Biến                    | Domain                | Loại giá trị | Khoảng giá trị                                    | Mô tả                                                |
| ----------------------- | --------------------- | ------------ | ------------------------------------------------- | ---------------------------------------------------- |
| Trạng thái đăng nhập    | Authentication        | Boolean      | True, False                                       | Kiểm soát quyền truy cập chức năng lịch sử đơn hàng. |
| Dữ liệu đơn hàng        | Số lượng              | Integer      | 0, >0                                             | Xử lý trường hợp không có hoặc có nhiều đơn hàng.    |
| Quyền truy cập đơn hàng | Authorization         | Object Match | Khớp, Không khớp                                  | Đảm bảo user chỉ xem được đơn hàng của chính mình.   |
| Trạng thái đơn hàng     | Order State           | Enum         | pending, confirmed, shipping, delivered, canceled | Kiểm tra hiển thị tiếng Việt và màu sắc tương ứng.   |
| Authorization Token     | Authentication Header | String       | Có token, Không có token                          | Kiểm tra API có yêu cầu xác thực hay không.          |
| Order ID                | Identifier            | Integer      | ID hợp lệ, ID không tồn tại                       | Kiểm tra truy cập chi tiết đơn hàng.                 |

### Quy trình phân tích

1. Xác định input cần kiểm thử:

   * Trạng thái đăng nhập.
   * Token xác thực.
   * Số lượng đơn hàng.
   * Quyền sở hữu đơn hàng.
   * Trạng thái đơn hàng.

2. Xác định miền giá trị:

   * User đã đăng nhập / chưa đăng nhập.
   * Có token / không có token.
   * Đơn hàng thuộc user hiện tại / user khác.
   * Các trạng thái hợp lệ của đơn hàng.

3. Xác định dữ liệu hợp lệ:

   * Người dùng đã đăng nhập.
   * Token hợp lệ.
   * Đơn hàng thuộc về user hiện tại.
   * Trạng thái đơn hàng nằm trong danh sách cho phép.

4. Xác định dữ liệu không hợp lệ:

   * Không có token.
   * Truy cập đơn hàng của người khác.
   * Truy cập chi tiết đơn hàng khi chưa đăng nhập.

5. Xác định các trường hợp kiểm thử:

   * Kiểm tra hiển thị lịch sử đơn hàng.
   * Kiểm tra quyền truy cập dữ liệu.
   * Kiểm tra trạng thái hiển thị.
   * Kiểm tra bảo mật API.

## 3.3 Boundary Value Analysis

FR-11 áp dụng Boundary Value Analysis chủ yếu cho **số lượng đơn hàng của người dùng**.

### Phân tích boundary

* Giá trị nhỏ nhất của số lượng đơn hàng là 0.
* Không tồn tại trường hợp số lượng đơn hàng âm.
* Boundary được chọn:

| Biến              | Constraint | Boundary       | Ý nghĩa                                                       |
| ----------------- | ---------- | -------------- | ------------------------------------------------------------- |
| Số lượng đơn hàng | >= 0       | 0              | Người dùng chưa có đơn hàng, hiển thị empty state.            |
| Số lượng đơn hàng | >= 0       | 1              | Người dùng có đơn hàng đầu tiên, kiểm tra hiển thị danh sách. |
| Số lượng đơn hàng | > 1        | Nhiều đơn hàng | Kiểm tra hiển thị nhiều dữ liệu và pagination.                |

### Vì sao chọn boundary này

* **0 đơn hàng**:

  * Kiểm tra hệ thống xử lý dữ liệu rỗng.
  * Đảm bảo hiển thị empty state thay vì lỗi giao diện.

* **1 đơn hàng**:

  * Kiểm tra trường hợp nhỏ nhất khi danh sách có dữ liệu.
  * Đảm bảo card đơn hàng được render đúng.

* **Nhiều đơn hàng**:

  * Kiểm tra khả năng xử lý khi dữ liệu lớn.
  * Đảm bảo không mất dữ liệu hoặc hiển thị sai.

### Boundary này có thể phát hiện lỗi gì

* Không xử lý empty state.
* Render sai khi danh sách có dữ liệu.
* Lỗi hiển thị nhiều đơn hàng.
* Không hỗ trợ phân trang khi dữ liệu lớn.

---

# 3.4 Danh sách test case

| Test Case ID        | Mục tiêu kiểm thử                                                            | Kỹ thuật                |
| ------------------- | ---------------------------------------------------------------------------- | ----------------------- |
| TC-ORDERHISTORY-001 | Người dùng chưa đăng nhập không thể xem lịch sử đơn hàng                     | Domain Testing          |
| TC-ORDERHISTORY-002 | Hiển thị khi người dùng không có đơn hàng (Boundary: 0 đơn hàng)             | Boundary Value Analysis |
| TC-ORDERHISTORY-003 | Hiển thị khi người dùng có ít nhất 1 đơn hàng (Boundary: 1 đơn hàng)         | Boundary Value Analysis |
| TC-ORDERHISTORY-004 | Người dùng không thể xem đơn hàng của người khác                             | Domain Testing          |
| TC-ORDERHISTORY-005 | Hiển thị đầy đủ thông tin đơn hàng (mã đơn, ngày đặt, tổng tiền, trạng thái) | Domain Testing          |
| TC-ORDERHISTORY-006 | Hiển thị trạng thái pending (chờ xác nhận)                                   | Domain Testing          |
| TC-ORDERHISTORY-007 | Hiển thị trạng thái confirmed (đã xác nhận)                                  | Domain Testing          |
| TC-ORDERHISTORY-008 | Hiển thị trạng thái shipping (đang giao)                                     | Domain Testing          |
| TC-ORDERHISTORY-009 | Hiển thị trạng thái delivered (đã giao)                                      | Domain Testing          |
| TC-ORDERHISTORY-010 | Hiển thị trạng thái canceled (đã hủy)                                        | Domain Testing          |
| TC-ORDERHISTORY-011 | Hệ thống hỗ trợ phân trang khi số lượng đơn hàng lớn                         | Boundary Value Analysis |
| TC-ORDERHISTORY-012 | API lịch sử đơn hàng yêu cầu token xác thực                                  | Domain Testing          |
| TC-ORDERHISTORY-013 | User chỉ nhận được lịch sử đơn hàng của chính mình                           | Domain Testing          |
| TC-ORDERHISTORY-014 | Người dùng chưa đăng nhập không thể truy cập chi tiết đơn hàng               | Domain Testing          |


## 3.5 Phân tích khoảng trống kiểm thử do AI hỗ trợ

### Bổ sung test case bị AI bỏ sót

| Test Case ID | Mục tiêu kiểm thử | Kỹ thuật | Lý do bổ sung |
|---|---|---|---|
| TC-ORDERHISTORY-011 | Kiểm tra hệ thống hỗ trợ phân trang khi số lượng đơn hàng lớn | Boundary Value Analysis | Đảm bảo hệ thống xử lý tốt khi dữ liệu lịch sử đơn hàng tăng, tránh trả về toàn bộ dữ liệu gây ảnh hưởng hiệu năng. |
| TC-ORDERHISTORY-012 | Kiểm tra API lịch sử đơn hàng yêu cầu xác thực khi không có token | Domain Testing | Kiểm tra domain authentication với giá trị không hợp lệ (chưa đăng nhập), đảm bảo người dùng không thể truy cập dữ liệu trái phép. |
| TC-ORDERHISTORY-013 | Kiểm tra người dùng chỉ nhận được lịch sử đơn hàng của chính mình | Domain Testing | Kiểm tra domain authorization, đảm bảo dữ liệu đơn hàng được phân tách theo từng người dùng. |
| TC-ORDERHISTORY-014 | Kiểm tra người dùng chưa đăng nhập không thể truy cập chi tiết đơn hàng | Domain Testing | Kiểm tra endpoint chi tiết đơn hàng có thực hiện authentication hay không, tránh lỗi truy cập dữ liệu trực tiếp thông qua Order ID. |


### AI Gap Analysis - Lý do AI bỏ sót 4 test case

| Test Case bị bỏ sót | Lý do AI có thể bỏ sót |
|---|---|
| TC-ORDERHISTORY-011 | AI tập trung vào chức năng hiển thị lịch sử đơn hàng và dữ liệu giao diện, nhưng chưa mở rộng sang khía cạnh hiệu năng và scalability. Requirement FR-11 không mô tả rõ pagination nên AI không ưu tiên sinh test case liên quan đến xử lý dữ liệu lớn. Ngoài ra, agent skill chưa yêu cầu phân tích các vấn đề về hiệu năng hoặc kiểm tra API pagination nên trường hợp này dễ bị bỏ sót. |
| TC-ORDERHISTORY-012 | AI chủ yếu kiểm tra luồng UI hoặc API hợp lệ có token, nhưng chưa đi sâu vào trường hợp thiếu authentication ở tầng API. Nguyên nhân một phần do agent skill chưa yêu cầu đọc và phân tích API documentation, nên AI chưa xác định được endpoint `/api/orders/my-orders` cần kiểm tra header Authorization và các trường hợp request không có token. |
| TC-ORDERHISTORY-013 | AI tập trung vào việc hiển thị đúng dữ liệu của user hiện tại, nhưng chưa mở rộng sang kiểm thử authorization giữa nhiều user, dẫn đến bỏ sót nguy cơ rò rỉ dữ liệu. Việc agent skill chưa yêu cầu phân tích API permission hoặc ownership validation cũng khiến AI chưa ưu tiên tạo test case kiểm tra quyền truy cập giữa các tài khoản. |
| TC-ORDERHISTORY-014 | AI tập trung vào luồng chính “xem lịch sử đơn hàng”, chưa mở rộng sang các endpoint liên quan như `/api/orders/:id`, dẫn đến thiếu kiểm thử authentication bypass ở chức năng chi tiết đơn hàng. Ngoài ra, agent skill chưa yêu cầu đọc API docs nên AI không nhận diện được các API liên quan trong module Order cần được kiểm thử bảo mật. |


### Tổng kết

AI đã bao phủ được các nhóm kiểm thử chính:
- Hiển thị danh sách đơn hàng.
- Trạng thái đơn hàng.
- Empty state và boundary cơ bản.
- Kiểm tra logic hiển thị UI.

Tuy nhiên, còn thiếu các kiểm thử quan trọng liên quan đến:
- Scalability (phân trang khi dữ liệu lớn).
- Authentication ở API level.
- Authorization giữa nhiều người dùng.
- Kiểm thử các endpoint liên quan ngoài luồng UI chính.

Các test case bổ sung giúp tăng độ bao phủ về **bảo mật, hiệu năng và phân quyền hệ thống**.
