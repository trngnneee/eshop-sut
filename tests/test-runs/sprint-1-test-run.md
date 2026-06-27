# Test Run - Sprint 1

**Ngày thực hiện**: 25/06/2026  
**Người thực hiện**: Thịnh
**Môi trường thử nghiệm**: Local Backend API & Frontend Web (demo)

| Test Case ID                                        | Module | Tester | Result | Related Bug                  | Note                                                                   |
| :-------------------------------------------------- | :----- | :----- | :----- | :--------------------------- | :--------------------------------------------------------------------- |
| [TC-COUPON-001](../test-cases/coupon/TC-COUPON-001.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-001](../bug-reports/BUG-COUPON-001.md) | Từ chối áp dụng khi đơn hàng đạt chính xác 300k (Strict inequality bug) và tính sai công thức |
| [TC-COUPON-002](../test-cases/coupon/TC-COUPON-002.md) | Coupon | Thịnh   | Pass   | None                         | Từ chối chính xác khi đơn hàng 299,999 ₫ |
| [TC-COUPON-003](../test-cases/coupon/TC-COUPON-003.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-002](../bug-reports/BUG-COUPON-002.md) | Số tiền giảm giá tính ra số âm và tổng tiền thanh toán tăng vọt |
| [TC-COUPON-004](../test-cases/coupon/TC-COUPON-004.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-001](../bug-reports/BUG-COUPON-001.md) | Từ chối áp dụng khi đơn hàng đạt chính xác 500k |
| [TC-COUPON-005](../test-cases/coupon/TC-COUPON-005.md) | Coupon | Thịnh   | Pass   | None                         | Từ chối chính xác khi đơn hàng 499,999 ₫ |
| [TC-COUPON-006](../test-cases/coupon/TC-COUPON-006.md) | Coupon | Thịnh   | Pass   | None                         | Từ chối chính xác đối với mã hết hạn |
| [TC-COUPON-007](../test-cases/coupon/TC-COUPON-007.md) | Coupon | Thịnh   | Pass   | None                         | Từ chối chính xác đối với mã không tồn tại |
| [TC-COUPON-008](../test-cases/coupon/TC-COUPON-008.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-003](../bug-reports/BUG-COUPON-003.md) | Áp dụng thành công dù không có JWT Token do thiếu authenticateToken |
| [TC-COUPON-009](../test-cases/coupon/TC-COUPON-009.md) | Coupon | Thịnh   | Pass   | None                         | Từ chối chính xác khi số lần dùng đạt giới hạn (2 lần) |
| [TC-COUPON-010](../test-cases/coupon/TC-COUPON-010.md) | Coupon | Thịnh   | Pass   | None                         | Áp dụng thành công khi số lần dùng là 1 < 2 |
| [TC-COUPON-011](../test-cases/coupon/TC-COUPON-011.md) | Coupon | Thịnh   | Pass   | None                         | Từ chối chính xác khi mã tồn tại nhưng bị tắt (is_active = 0) |
| [TC-COUPON-012](../test-cases/coupon/TC-COUPON-012.md) | Coupon | Thịnh   | Fail   | None | Từ chối chính xác khi mã quá hạn |
| [TC-COUPON-013](../test-cases/coupon/TC-COUPON-013.md) | Coupon | Thịnh   | Pass   | None                         | Từ chối chính xác khi số lần sử dụng trong DB lớn hơn mức tối đa |
| [TC-COUPON-014](../test-cases/coupon/TC-COUPON-014.md) | Coupon | Thịnh   | Pass   | None                         | Từ chối chính xác khi mã coupon để trống |
| [TC-COUPON-015](../test-cases/coupon/TC-COUPON-015.md) | Coupon | Thịnh   | Pass   | None                         | Từ chối chính xác khi mã coupon chứa ký tự đặc biệt |
| [TC-COUPON-016](../test-cases/coupon/TC-COUPON-016.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-005](../bug-reports/BUG-COUPON-005.md) | Báo sai thông báo lỗi (đơn hàng chưa đủ tối thiểu) khi total_amount là chuỗi |
| [TC-COUPON-017](../test-cases/coupon/TC-COUPON-017.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-005](../bug-reports/BUG-COUPON-005.md) | Báo sai thông báo lỗi khi total_amount là null |
| [TC-COUPON-018](../test-cases/coupon/TC-COUPON-018.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-005](../bug-reports/BUG-COUPON-005.md) | Báo sai thông báo lỗi khi total_amount là số âm |
| [TC-COUPON-020](../test-cases/coupon/TC-COUPON-020.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-004](../bug-reports/BUG-COUPON-004.md) | Từ chối áp dụng và trả về lỗi 404 khi có khoảng trắng ở đầu mã |
| [TC-COUPON-021](../test-cases/coupon/TC-COUPON-021.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-004](../bug-reports/BUG-COUPON-004.md) | Từ chối áp dụng và trả về lỗi 404 khi có khoảng trắng ở cuối mã |
| [TC-COUPON-022](../test-cases/coupon/TC-COUPON-022.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-004](../bug-reports/BUG-COUPON-004.md) | Từ chối áp dụng và trả về lỗi 404 khi có khoảng trắng ở giữa mã |
| [TC-COUPON-023](../test-cases/coupon/TC-COUPON-023.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-006](../bug-reports/BUG-COUPON-006.md) | Phân biệt chữ hoa/thường, không tự động chuyển thành chữ hoa |
| [TC-COUPON-024](../test-cases/coupon/TC-COUPON-024.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-007](../bug-reports/BUG-COUPON-007.md) | Cho phép final_amount nhận giá trị âm khi fixed discount > total_amount |
| [TC-COUPON-025](../test-cases/coupon/TC-COUPON-025.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-008](../bug-reports/BUG-COUPON-008.md) | Thiếu validate giới hạn sử dụng trên API /api/coupon-usage, cho phép ghi nhận trùng lặp |
| [TC-COUPON-026](../test-cases/coupon/TC-COUPON-026.md) | Coupon | Thịnh   | Fail   | [BUG-COUPON-009](../bug-reports/BUG-COUPON-009.md) | Cho phép tài khoản Admin áp dụng mã giảm giá |
| [TC-COUPON-027](../test-cases/coupon/TC-COUPON-027.md) | Coupon | Thịnh   | Pass   | None                         | Từ chối chính xác khi giỏ hàng trống (total_amount = 0) |
| [TC-COUPON-028](../test-cases/coupon/TC-COUPON-028.md) | Coupon | Thịnh   | Pass   | None                         | Chặn chính xác mã hết hạn, không phụ thuộc múi giờ client |
| [TC-REG-001](../test-cases/register/TC-REG-001.md) | Register | Thịnh   | Pass   | None                         | Đăng ký thành công với thông tin hợp lệ |
| [TC-REG-002](../test-cases/register/TC-REG-002.md) | Register | Thịnh   | Fail   | [BUG-REG-002](../bug-reports/BUG-REG-002.md) | Cho phép đăng ký khi Họ tên trống |
| [TC-REG-003](../test-cases/register/TC-REG-003.md) | Register | Thịnh   | Fail   | [BUG-REG-001](../bug-reports/BUG-REG-001.md) | Cho phép đăng ký khi Email sai định dạng |
| [TC-REG-004](../test-cases/register/TC-REG-004.md) | Register | Thịnh   | Fail   | [BUG-REG-007](../bug-reports/BUG-REG-007.md) | Cho phép đăng ký khi Email trùng lặp |
| [TC-REG-005](../test-cases/register/TC-REG-005.md) | Register | Thịnh   | Fail   | [BUG-REG-003](../bug-reports/BUG-REG-003.md) | Cho phép đăng ký khi Mật khẩu ngắn hơn 8 ký tự |
| [TC-REG-006](../test-cases/register/TC-REG-006.md) | Register | Thịnh   | Pass   | None                         | Đăng ký thành công với mật khẩu dài 8 ký tự |
| [TC-REG-007](../test-cases/register/TC-REG-007.md) | Register | Thịnh   | Fail   | [BUG-REG-008](../bug-reports/BUG-REG-008.md) | Cho phép đăng ký khi Mật khẩu thiếu chữ hoa |
| [TC-REG-008](../test-cases/register/TC-REG-008.md) | Register | Thịnh   | Fail   | [BUG-REG-008](../bug-reports/BUG-REG-008.md) | Cho phép đăng ký khi Mật khẩu thiếu chữ thường |
| [TC-REG-009](../test-cases/register/TC-REG-009.md) | Register | Thịnh   | Fail   | [BUG-REG-008](../bug-reports/BUG-REG-008.md) | Cho phép đăng ký khi Mật khẩu thiếu chữ số |
| [TC-REG-010](../test-cases/register/TC-REG-010.md) | Register | Thịnh   | Fail   | [BUG-REG-008](../bug-reports/BUG-REG-008.md) | Cho phép đăng ký khi Mật khẩu thiếu ký tự đặc biệt |
| [TC-REG-011](../test-cases/register/TC-REG-011.md) | Register | Thịnh   | Fail   | [BUG-REG-009](../bug-reports/BUG-REG-009.md) | Cho phép đăng ký khi Mật khẩu xác nhận không khớp |
| [TC-REG-012](../test-cases/register/TC-REG-012.md) | Register | Thịnh   | Fail   | [BUG-REG-004](../bug-reports/BUG-REG-004.md) | Cho phép đăng ký với Họ Tên chứa chữ số |
| [TC-REG-013](../test-cases/register/TC-REG-013.md) | Register | Thịnh   | Fail   | [BUG-REG-010](../bug-reports/BUG-REG-010.md) | Cho phép đăng ký với Họ Tên chứa ký tự đặc biệt |
| [TC-REG-014](../test-cases/register/TC-REG-014.md) | Register | Thịnh   | Fail   | [BUG-REG-005](../bug-reports/BUG-REG-005.md) | Cho phép lưu trữ mã độc XSS trong trường Họ Tên |
| [TC-REG-015](../test-cases/register/TC-REG-015.md) | Register | Thịnh   | Fail   | [BUG-REG-014](../bug-reports/BUG-REG-014.md) | Cho phép nhập lệnh SQL Injection trong trường Họ Tên |
| [TC-REG-016](../test-cases/register/TC-REG-016.md) | Register | Thịnh   | Fail   | [BUG-REG-011](../bug-reports/BUG-REG-011.md) | Cho phép đăng ký khi Họ Tên chỉ toàn khoảng trắng |
| [TC-REG-017](../test-cases/register/TC-REG-017.md) | Register | Thịnh   | Fail   | [BUG-REG-006](../bug-reports/BUG-REG-006.md) | Không chuẩn hóa viết hoa chữ cái đầu cho Họ Tên |
| [TC-REG-018](../test-cases/register/TC-REG-018.md) | Register | Thịnh   | Fail   | [BUG-REG-012](../bug-reports/BUG-REG-012.md) | Cho phép đăng ký khi Họ Tên chỉ dài 1 ký tự (biên dưới lỗi) |
| [TC-REG-019](../test-cases/register/TC-REG-019.md) | Register | Thịnh   | Fail   | [BUG-REG-013](../bug-reports/BUG-REG-013.md) | Cho phép đăng ký khi Họ Tên dài 101 ký tự (biên trên lỗi) |
| [TC-REG-020](../test-cases/register/TC-REG-020.md) | Register | Thịnh   | Fail   | [BUG-REG-001](../bug-reports/BUG-REG-001.md) | Cho phép đăng ký Email thiếu ký tự '@' |
| [TC-REG-021](../test-cases/register/TC-REG-021.md) | Register | Thịnh   | Fail   | [BUG-REG-001](../bug-reports/BUG-REG-001.md) | Cho phép đăng ký Email thiếu dấu chấm ở domain-part |
| [TC-REG-022](../test-cases/register/TC-REG-022.md) | Register | Thịnh   | Fail   | [BUG-REG-001](../bug-reports/BUG-REG-001.md) | Cho phép đăng ký Email thiếu phần local-part |
| [TC-REG-023](../test-cases/register/TC-REG-023.md) | Register | Thịnh   | Fail   | [BUG-REG-001](../bug-reports/BUG-REG-001.md) | Cho phép đăng ký Email thiếu phần domain-part |
| [TC-REG-024](../test-cases/register/TC-REG-024.md) | Register | Thịnh   | Fail   | [BUG-REG-001](../bug-reports/BUG-REG-001.md) | Cho phép đăng ký Email chứa nhiều hơn 1 ký tự '@' |
| [TC-REG-025](../test-cases/register/TC-REG-025.md) | Register | Thịnh   | Fail   | [BUG-REG-001](../bug-reports/BUG-REG-001.md) | Cho phép đăng ký Email chứa 2 dấu chấm liên tiếp ở domain-part |
| [TC-REG-026](../test-cases/register/TC-REG-026.md) | Register | Thịnh   | Fail   | [BUG-REG-001](../bug-reports/BUG-REG-001.md) | Cho phép đăng ký Email chứa khoảng trắng |
| [TC-REG-027](../test-cases/register/TC-REG-027.md) | Register | Thịnh   | Fail   | [BUG-REG-001](../bug-reports/BUG-REG-001.md) | Cho phép đăng ký Email có ký tự '@' nằm ở đầu tiên |
| [TC-REG-028](../test-cases/register/TC-REG-028.md) | Register | Thịnh   | Fail   | [BUG-REG-001](../bug-reports/BUG-REG-001.md) | Cho phép đăng ký Email có ký tự '@' nằm ở cuối cùng |
| [TC-REG-029](../test-cases/register/TC-REG-029.md) | Register | Thịnh   | Fail   | [BUG-REG-001](../bug-reports/BUG-REG-001.md) | Cho phép đăng ký Email có dấu chấm '.' nằm ở đầu tiên |
| [TC-REG-030](../test-cases/register/TC-REG-030.md) | Register | Thịnh   | Fail   | [BUG-REG-001](../bug-reports/BUG-REG-001.md) | Cho phép đăng ký Email có dấu chấm '.' nằm ở cuối cùng |
| [TC-REG-031](../test-cases/register/TC-REG-031.md) | Register | Thịnh   | Fail   | [BUG-REG-015](../bug-reports/BUG-REG-015.md) | Không chuẩn hóa domain-part của Email thành chữ thường |
| [TC-REG-032](../test-cases/register/TC-REG-032.md) | Register | Thịnh   | Fail   | [BUG-REG-001](../bug-reports/BUG-REG-001.md) | Cho phép đăng ký Email có độ dài domain-part bằng 1 ký tự |
| [TC-REG-033](../test-cases/register/TC-REG-033.md) | Register | Thịnh   | Fail   | [BUG-REG-001](../bug-reports/BUG-REG-001.md) | Cho phép đăng ký Email có tổng độ dài 5 ký tự (biên dưới lỗi) |
| [TC-REG-034](../test-cases/register/TC-REG-034.md) | Register | Thịnh   | Fail   | [BUG-REG-001](../bug-reports/BUG-REG-001.md) | Cho phép đăng ký Email có tổng độ dài 255 ký tự (biên trên lỗi) |
| [TC-REG-035](../test-cases/register/TC-REG-035.md) | Register | Thịnh   | Fail   | [BUG-REG-005](../bug-reports/BUG-REG-005.md) | Cho phép lưu trữ mã độc XSS trong trường Email |
| [TC-REG-036](../test-cases/register/TC-REG-036.md) | Register | Thịnh   | Fail   | [BUG-REG-014](../bug-reports/BUG-REG-014.md) | Cho phép nhập lệnh SQL Injection trong trường Email |
| [TC-REG-037](../test-cases/register/TC-REG-037.md) | Register | Thịnh   | Fail   | [BUG-REG-005](../bug-reports/BUG-REG-005.md) | Cho phép lưu trữ mã độc XSS trong trường Mật khẩu |
| [TC-REG-038](../test-cases/register/TC-REG-038.md) | Register | Thịnh   | Fail   | [BUG-REG-014](../bug-reports/BUG-REG-014.md) | Cho phép nhập lệnh SQL Injection trong trường Mật khẩu |
| [TC-REG-039](../test-cases/register/TC-REG-039.md) | Register | Thịnh   | Fail   | [BUG-REG-005](../bug-reports/BUG-REG-005.md) | Cho phép lưu trữ mã độc XSS trong Xác nhận mật khẩu |
| [TC-REG-040](../test-cases/register/TC-REG-040.md) | Register | Thịnh   | Fail   | [BUG-REG-014](../bug-reports/BUG-REG-014.md) | Cho phép nhập lệnh SQL Injection trong Xác nhận mật khẩu |
| [TC-REG-041](../test-cases/register/TC-REG-041.md) | Register | Thịnh   | Pass   | None                         | Hệ thống lưu CSDL thành công khi mất mạng lúc redirect |
| [TC-REG-042](../test-cases/register/TC-REG-042.md) | Register | Thịnh   | Fail   | [BUG-REG-016](../bug-reports/BUG-REG-016.md) | Lỗi regex mật khẩu mạnh chặn ký tự đặc biệt thực tế và thiếu trường xác nhận mật khẩu ở Frontend |
| [TC-IMPORT-001](../test-cases/import/TC-IMPORT-001.md) | Import | Thịnh   | Pass   | None                         | Import thành công tệp CSV gồm nhiều sản phẩm |
| [TC-IMPORT-002](../test-cases/import/TC-IMPORT-002.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-002](../bug-reports/BUG-IMPORT-002.md) | Frontend cho phép chọn và tải lên tệp không phải .csv |
| [TC-IMPORT-003](../test-cases/import/TC-IMPORT-003.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-003](../bug-reports/BUG-IMPORT-003.md) | Frontend cho phép import tệp thiếu dòng header định dạng |
| [TC-IMPORT-004](../test-cases/import/TC-IMPORT-004.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-003](../bug-reports/BUG-IMPORT-003.md) | Frontend cho phép import tệp có header sai tên cột bắt buộc |
| [TC-IMPORT-005](../test-cases/import/TC-IMPORT-005.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-004](../bug-reports/BUG-IMPORT-004.md) | Backend trả về HTTP 200 OK khi có sản phẩm trống tên |
| [TC-IMPORT-006](../test-cases/import/TC-IMPORT-006.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-005](../bug-reports/BUG-IMPORT-005.md) | Cho phép import sản phẩm có giá price bằng 0 |
| [TC-IMPORT-007](../test-cases/import/TC-IMPORT-007.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-005](../bug-reports/BUG-IMPORT-005.md) | Cho phép import sản phẩm có giá price âm |
| [TC-IMPORT-008](../test-cases/import/TC-IMPORT-008.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-005](../bug-reports/BUG-IMPORT-005.md) | Cho phép import sản phẩm có giá price không phải là số |
| [TC-IMPORT-009](../test-cases/import/TC-IMPORT-009.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-001](../bug-reports/BUG-IMPORT-001.md) | Không thực hiện rollback khi có dòng lỗi (thiếu tính nguyên tử) |
| [TC-IMPORT-010](../test-cases/import/TC-IMPORT-010.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-006](../bug-reports/BUG-IMPORT-006.md) | Tách cột sai khi giá trị chứa dấu phẩy được bọc nháy kép (RFC 4180) |
| [TC-IMPORT-011](../test-cases/import/TC-IMPORT-011.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-003](../bug-reports/BUG-IMPORT-003.md) | Frontend cho phép import tệp trống không có dữ liệu |
| [TC-IMPORT-012](../test-cases/import/TC-IMPORT-012.md) | Import | Thịnh   | Pass   | None                         | Import thành công sản phẩm với giá tối thiểu (0.01) |
| [TC-IMPORT-013](../test-cases/import/TC-IMPORT-013.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-007](../bug-reports/BUG-IMPORT-007.md) | Cho phép import khi tên chỉ chứa khoảng trắng |
| [TC-IMPORT-014](../test-cases/import/TC-IMPORT-014.md) | Import | Thịnh   | Pass   | None                         | Import thành công khi tên sản phẩm dài đúng 255 ký tự |
| [TC-IMPORT-015](../test-cases/import/TC-IMPORT-015.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-008](../bug-reports/BUG-IMPORT-008.md) | Cho phép import khi tên sản phẩm dài 256 ký tự |
| [TC-IMPORT-016](../test-cases/import/TC-IMPORT-016.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-009](../bug-reports/BUG-IMPORT-009.md) | Cho phép import tên chứa thẻ HTML/mã độc XSS vào CSDL |
| [TC-IMPORT-017](../test-cases/import/TC-IMPORT-017.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-010](../bug-reports/BUG-IMPORT-010.md) | Cho phép import price chứa payload SQL Injection |
| [TC-IMPORT-018](../test-cases/import/TC-IMPORT-018.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-011](../bug-reports/BUG-IMPORT-011.md) | Không hỗ trợ tự động chuẩn hóa/từ chối khi header viết hoa |
| [TC-IMPORT-019](../test-cases/import/TC-IMPORT-019.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-012](../bug-reports/BUG-IMPORT-012.md) | Lệch cấu trúc và category_id bị NaN khi mô tả có dấu phẩy không bọc nháy |
| [TC-IMPORT-020](../test-cases/import/TC-IMPORT-020.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-013](../bug-reports/BUG-IMPORT-013.md) | Cho phép import sản phẩm thiếu trường giá (price) |
| [TC-IMPORT-021](../test-cases/import/TC-IMPORT-021.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-014](../bug-reports/BUG-IMPORT-014.md) | Chấp nhận category_id không tồn tại trong hệ thống |
| [TC-IMPORT-022](../test-cases/import/TC-IMPORT-022.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-015](../bug-reports/BUG-IMPORT-015.md) | Cho phép import sản phẩm thiếu category_id |
| [TC-IMPORT-023](../test-cases/import/TC-IMPORT-023.md) | Import | Thịnh   | Pass   | None                         | Từ chối chính xác khi tệp CSV trống (0 bytes) |
| [TC-IMPORT-024](../test-cases/import/TC-IMPORT-024.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-016](../bug-reports/BUG-IMPORT-016.md) | Không rollback toàn bộ khi tệp CSV chứa dòng trống ở giữa |
| [TC-IMPORT-025](../test-cases/import/TC-IMPORT-025.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-001](../bug-reports/BUG-IMPORT-001.md) | Không rollback toàn bộ CSDL khi dòng thứ 3 bị price âm |
| [TC-IMPORT-026](../test-cases/import/TC-IMPORT-026.md) | Import | Thịnh   | Pass   | None                         | Import thành công hoàn toàn với các dòng dữ liệu hợp lệ |
| [TC-IMPORT-027](../test-cases/import/TC-IMPORT-027.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-017](../bug-reports/BUG-IMPORT-017.md) | Cho phép lưu trữ mã độc XSS nguyên bản vào database trong trường description |
| [TC-IMPORT-028](../test-cases/import/TC-IMPORT-028.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-018](../bug-reports/BUG-IMPORT-018.md) | Cho phép lưu trữ SQL Injection payload trong trường description |
| [TC-IMPORT-029](../test-cases/import/TC-IMPORT-029.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-019](../bug-reports/BUG-IMPORT-019.md) | Lưu trữ URI nguy hiểm javascript: trong trường imageUrl |
| [TC-IMPORT-030](../test-cases/import/TC-IMPORT-030.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-020](../bug-reports/BUG-IMPORT-020.md) | Cho phép lưu trữ SQL Injection payload trong trường imageUrl |
| [TC-IMPORT-031](../test-cases/import/TC-IMPORT-031.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-021](../bug-reports/BUG-IMPORT-021.md) | Lưu trữ mã độc XSS nguyên bản vào database trong cột price |
| [TC-IMPORT-032](../test-cases/import/TC-IMPORT-032.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-022](../bug-reports/BUG-IMPORT-022.md) | Lưu trữ mã độc XSS nguyên bản vào database trong cột category_id |
| [TC-IMPORT-033](../test-cases/import/TC-IMPORT-033.md) | Import | Thịnh   | Fail   | [BUG-IMPORT-023](../bug-reports/BUG-IMPORT-023.md) | Cho phép lưu trữ SQL Injection payload trong cột category_id |

