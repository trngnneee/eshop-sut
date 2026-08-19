# API-1 — Human-review worksheet for AI-generated login cases

> Phạm vi audit: 36/36 case trong `01-ai-generated.md`. Oracle: `README.md` FR-02 và SEC-01/02/05; `api_specification.md` §1.2; `backend/server.js:32-67`; `docs/hw06/02-sut-defect-catalog.md` §1.
>
> **Quan trọng:** Bảng dưới đây là phân tích hỗ trợ do Codex chuẩn bị. R-02 chỉ hoàn tất khi sinh viên tự đối chiếu từng dòng và ký xác nhận ở cuối file.

## Kiểm chứng SUT trước audit

- SUT thật chạy local tại `http://127.0.0.1:3100` (cổng `3000` đang bị ứng dụng khác chiếm), mọi request có `X-Student-Id: 23127207`.
- Login đúng trả token và các field user: `id,name,email,password,role,login_attempts,locked_until,reset_token,shipping_address,phone` — xác nhận D-LOGIN-03 có thể quan sát qua API.
- SQL injection email `' OR 1=1 --` trả `401` — xác nhận query parameterized, không có SQLi bypass ở login.

## Bảng audit 100% test case AI sinh

| TC ID | Nhãn | Lý do đối chiếu đặc tả | Hành động sửa |
| :--- | :---: | :--- | :--- |
| TC-API-LOGIN-001 | VALID | Bao phủ happy path được API spec mô tả; status và field tối thiểu đúng. | Giữ nguyên. |
| TC-API-LOGIN-002 | VALID | FR-02 yêu cầu lỗi chung khi credential sai; `401` là oracle hiện có cho credential không hợp lệ. | Giữ nguyên. |
| TC-API-LOGIN-003 | VALID | Cùng thông báo với sai password giúp chống user enumeration. | Giữ nguyên. |
| TC-API-LOGIN-004 | VALID | Thiếu field bắt buộc phải bị từ chối ở biên API; phát hiện D-LOGIN-08 nếu SUT trả `401` thay vì validation error. | Giữ nguyên. |
| TC-API-LOGIN-005 | VALID | Tương tự case 004 cho password bắt buộc. | Giữ nguyên. |
| TC-API-LOGIN-006 | VALID | Chuỗi rỗng thuộc phân vùng không hợp lệ và phải bị từ chối trước truy vấn. | Giữ nguyên. |
| TC-API-LOGIN-007 | INVALID | AI áp chính sách mật khẩu mạnh của FR-01 (register) sang login. FR-02 không cấm credential ngắn nếu tài khoản thực sự có credential đó. | Sửa expected: với seed hiện tại, password `abc` là credential sai nên trả `401` chung và tăng attempts đúng 1; không assert lỗi độ mạnh. |
| TC-API-LOGIN-008 | INCOMPLETE | FR-02 ghi input UI dùng `type=email`, nhưng API spec không quy định status/body cho email sai format. `400` là giả định chưa có oracle rõ. | Sửa expected thành “controlled 4xx, không 5xx, không phản chiếu input”; ghi rõ đây là robustness test. |
| TC-API-LOGIN-009 | INVALID | Không tài liệu nào yêu cầu server tự trim email; AI đã bịa hành vi tiện ích. | Sửa expected: `401` generic với chuỗi chứa khoảng trắng; không khóa nếu chưa đủ 3 lần sai. |
| TC-API-LOGIN-010 | VALID | `null` sai kiểu string; test boundary hợp lệ và truy vết D-LOGIN-08. | Giữ nguyên. |
| TC-API-LOGIN-011 | VALID | `null` password sai kiểu; test boundary hợp lệ và truy vết D-LOGIN-08. | Giữ nguyên. |
| TC-API-LOGIN-012 | VALID | Number ở email là type partition riêng; phải từ chối có kiểm soát. | Giữ nguyên. |
| TC-API-LOGIN-013 | VALID | Object ở password là type partition riêng; phải từ chối có kiểm soát. | Giữ nguyên. |
| TC-API-LOGIN-014 | VALID | Array body không thỏa object schema; `400` là expected validation đúng. | Giữ nguyên. |
| TC-API-LOGIN-015 | INCOMPLETE | API spec yêu cầu JSON body nhưng không quy định bắt buộc `415` khi thiếu header; Express có thể diễn giải body rỗng rồi trả `400`. | Sửa expected: một controlled client error (`400` hoặc `415` theo contract được chốt), tuyệt đối không `500`; ghi actual status khi execute. |
| TC-API-LOGIN-016 | VALID | Field không nhạy cảm ngoài schema có thể được bỏ qua; không làm thay đổi authentication result. | Giữ nguyên. |
| TC-API-LOGIN-017 | VALID | Kiểm tra đúng biến trạng thái cốt lõi: lần sai thứ nhất tăng đúng 1. | Giữ nguyên. |
| TC-API-LOGIN-018 | VALID | Đo chính xác biên ngay dưới threshold 3; sẽ phát hiện D-LOGIN-01 vì SUT khóa sớm. | Giữ nguyên. |
| TC-API-LOGIN-019 | VALID | Bao phủ transition Active-2 → Locked-30s theo FR-02. | Giữ nguyên. |
| TC-API-LOGIN-020 | VALID | Bao phủ hành vi khi gọi trong locked state và yêu cầu không tiết lộ chi tiết. | Giữ nguyên. |
| TC-API-LOGIN-021 | VALID | BVA thời gian ngay dưới biên 30 giây. | Giữ nguyên. |
| TC-API-LOGIN-022 | VALID | BVA thời gian ngay trên biên 30 giây; phát hiện D-LOGIN-02. | Giữ nguyên. |
| TC-API-LOGIN-023 | VALID | FR-02 dùng khái niệm “liên tiếp”; login đúng phải reset chuỗi sai. | Giữ nguyên. |
| TC-API-LOGIN-024 | VALID | Xác minh hậu điều kiện reset sau login đúng. | Giữ nguyên. |
| TC-API-LOGIN-025 | INVALID | Expected “bypass thành công” mô tả kết quả tấn công chứ không phải expected an toàn. Mã nguồn dùng parameterized query nên đây không phải bug. | Sửa expected thành `401`, không token, không bypass, DB không đổi. |
| TC-API-LOGIN-026 | VALID | Password không được đưa vào câu SQL; expected từ chối an toàn là đúng. | Giữ nguyên. |
| TC-API-LOGIN-027 | VALID | Kiểm tra input độc hại không được phản chiếu; phù hợp SEC-04 ở biên response. | Giữ nguyên. |
| TC-API-LOGIN-028 | VALID | SEC-01 cấm lộ password; case này trực tiếp phát hiện D-LOGIN-03. | Giữ nguyên. |
| TC-API-LOGIN-029 | VALID | Negative-schema assertion cho field nhạy cảm; phát hiện D-LOGIN-03. | Giữ nguyên. |
| TC-API-LOGIN-030 | VALID | Client không được chi phối role; payload JWT phải lấy role từ DB. | Giữ nguyên. |
| TC-API-LOGIN-031 | VALID | Kiểm tra token có giá trị sử dụng thực, không chỉ kiểm tra chuỗi tồn tại; phù hợp SEC-02. | Giữ nguyên. |
| TC-API-LOGIN-032 | VALID | FR-02 yêu cầu thông báo phù hợp và không lộ chi tiết nguyên nhân; case phát hiện D-LOGIN-07. | Giữ nguyên. |
| TC-API-LOGIN-033 | INCOMPLETE | API spec chỉ nói có `token` và `user`, chưa định nghĩa schema chi tiết của `user` nên chưa thể gọi là exact-schema validation. | Sửa thành schema tối thiểu: root object, `token` non-empty string, `user` object có `id/email/role`; đồng thời áp negative schema cho field nhạy cảm. |
| TC-API-LOGIN-034 | VALID | JSON endpoint phải trả JSON content type; assertion rõ và chạy được. | Giữ nguyên. |
| TC-API-LOGIN-035 | INCOMPLETE | Spec không công bố schema nhánh `401`; từ “chỉ có” quá mạnh nếu chưa có schema chính thức. | Sửa thành `401`, object có duy nhất contract tối thiểu `error:string`; ghi đây là contract được suy ra từ oracle mã nguồn và yêu cầu không tiết lộ. |
| TC-API-LOGIN-036 | INCOMPLETE | API spec nói trả `token` và `user` nhưng không nói rõ có cấm field root `message`; AI suy diễn “không field khác”. | Không cấm `message`; chỉ cấm field nhạy cảm ở root và trong `user`, đồng thời yêu cầu `token/user` hiện diện. |

## Phiên bản đã sửa cho case INVALID / INCOMPLETE

| TC ID | Test data giữ lại | Expected result sau audit |
| :--- | :--- | :--- |
| TC-API-LOGIN-007 | `test@eshop.com` / `abc` | `401 {"error":"Invalid email or password"}`; đây là wrong-credential case, không phải password-policy case. |
| TC-API-LOGIN-008 | `not-an-email` / `Test1234!` | Controlled 4xx; JSON error; không `500`; không phản chiếu input. Contract status cụ thể cần người học xác nhận. |
| TC-API-LOGIN-009 | Email có whitespace | `401` generic; không tự trim nếu đặc tả không yêu cầu. |
| TC-API-LOGIN-015 | Raw JSON thiếu `Content-Type` | `400` hoặc `415` theo contract chốt; không `500`; response JSON nếu server nhận request. |
| TC-API-LOGIN-025 | email SQLi | `401`; không token; không bypass; không thay đổi dữ liệu. |
| TC-API-LOGIN-033 | Credentials đúng | `200`; `token` là non-empty string; `user.id/email/role` đúng kiểu; không field nhạy cảm. |
| TC-API-LOGIN-035 | Wrong password | `401`; root object có `error:string`; message không tiết lộ email tồn tại hay không. |
| TC-API-LOGIN-036 | Credentials đúng | Có `token` và `user`; cho phép metadata vô hại như `message`; cấm `password/reset_token/login_attempts/locked_until`. |

## Thống kê audit

| Nhãn | Số case | Tỷ lệ |
| :--- | ---: | ---: |
| VALID | 28 | 77.78% |
| INVALID | 3 | 8.33% |
| INCOMPLETE | 5 | 13.89% |
| **Tổng đã audit** | **36/36** | **100%** |

## HUMAN checkpoint — bắt buộc trước khi sang API-2

- [x] Tôi đã đối chiếu đủ 36 dòng với FR-02, API spec và mã nguồn.
- [x] Tôi đồng ý hoặc đã chỉnh lại nhãn/lý do cho 8 case cần sửa.
- [x] Tôi hiểu vì sao expected phải theo đặc tả, không sửa để khớp bug của SUT.

**Reviewed by:** Đặng Đăng Khoa 
**Student ID:** `23127207`  
**Reviewed at:** 10:25 19-08-2026
**Signature / confirmation:** Đã duyệt
