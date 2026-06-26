# HW02 – Báo cáo Kiểm thử Phần mềm

---

# 1. Giới thiệu

## 1.1 Thông tin sinh viên
- Họ và tên: Nguyễn Thanh Gia Bảo
- Mã số sinh viên: 23127158
- Lớp: 23KTPM3
- Môn học: Kiểm thử phần mềm / Cơ sở QA
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

1. Xác định input cần kiểm thử: từ khóa tìm kiếm và các điều kiện hiển thị liên quan đến sản phẩm trên trang chủ.
2. Xác định miền giá trị của input: chuỗi tìm kiếm, số lượng h1, nội dung alt text, giá hiển thị và trạng thái giao diện.
3. Xác định dữ liệu hợp lệ: tên sản phẩm hợp lệ, một h1 duy nhất, alt text mô tả, giá được định dạng đúng.
4. Xác định dữ liệu không hợp lệ: HTML/JS trong từ khóa, h1 bằng 0 hoặc lớn hơn 1, alt text rỗng.
5. Xác định các trường hợp cần kiểm thử: hiển thị danh sách, tìm kiếm, empty state, loading state, an toàn hiển thị và kiểm tra cấu trúc DOM.


## 2.3 Boundary Value Analysis
FR-05 không định nghĩa giới hạn số lượng ký tự của từ khóa tìm kiếm nên không có biên min/max cho trường này. Biên giá trị rõ ràng nhất của FR-05 là số lượng thẻ h1 trên mỗi trang phải bằng 1. Do đó, BVA được áp dụng cho quy tắc này để kiểm tra các giá trị sát biên:

- min-1: 0 h1
- min: 1 h1
- min+1: 2 h1

### Boundary values

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


| Test Case ID       | Mục tiêu kiểm thử                                                        | Kỹ thuật                |
| ------------------ | ------------------------------------------------------------------------ | ----------------------- |
| TC-PRODUCT-001     | Hiển thị danh sách sản phẩm dạng grid                                    | Domain Testing          |
| TC-PRODUCT-002     | Hiển thị tên sản phẩm trên card                                          | Domain Testing          |
| TC-PRODUCT-003     | Hiển thị giá đúng định dạng ₫ và phân cách hàng nghìn                    | Domain Testing          |
| TC-PRODUCT-004     | Hiển thị ảnh sản phẩm với alt text mô tả                                 | Domain Testing          |
| TC-PRODUCT-005     | Hiển thị trạng thái loading khi dữ liệu đang tải                         | Domain Testing          |
| TC-PRODUCT-006     | Hiển thị empty state khi không có kết quả tìm kiếm                       | Domain Testing          |
| TC-PRODUCT-007     | Tìm kiếm theo tên sản phẩm hợp lệ                                        | Domain Testing          |
| TC-PRODUCT-008     | Hiển thị an toàn từ khóa chứa HTML                                       | Domain Testing          |
| TC-PRODUCT-009     | Trang chủ chỉ có đúng một h1                                             | Boundary Value Analysis |
| TC-PRODUCT-010     | Sau khi tìm kiếm vẫn chỉ có đúng một h1                                  | Boundary Value Analysis |
| TC-PRODUCT-011     | Lưới hiển thị đầy đủ tất cả sản phẩm trả về                              | Domain Testing          |
| TC-PRODUCT-012     | Ảnh sản phẩm hiển thị đúng tỷ lệ, không méo                              | Domain Testing          |
| TC-PRODUCT-013 | Kiểm tra XSS injection qua input tìm kiếm không được thực thi JavaScript | Domain Testing          |
| TC-PRODUCT-014 | Kiểm tra SQL Injection không làm thay đổi logic tìm kiếm sản phẩm        | Domain Testing          |


## 2.5 Phân tích khoảng trống kiểm thử do AI hỗ trợ

### Các test case AI bị bỏ sót:

* **TC-PRODUCT-013 – XSS Injection nâng cao**

    AI chỉ đề xuất test case XSS cơ bản (`<script>`), nhưng bỏ sót payload phức tạp hơn:
    `<image onerror=javascript:alert(1)>`

    **Lý do AI bỏ sót:**
    - Prompt ban đầu chưa yêu cầu “advanced payload / real-world exploit”
    - AI thiên về pattern đơn giản, không generate attack payload đa dạng

* **TC-PRODUCT-014 – SQL Injection logic bypass**

    AI không tạo test case SQL injection:
    `' OR 1=1 --`

    **Lý do AI bỏ sót:**
    - Feature mô tả tập trung UI frontend -> AI assume không có DB logic ảnh hưởng
    - Thiếu prompt nhấn mạnh “backend query behavior testing”