# API-1 — AI-generated test cases for `POST /api/login`

> Đây là output ở bước Generate (R-01), được giữ nguyên trước human audit. Những giả định sai hoặc thiếu của AI được ghi nhận và sửa tại `02-audit.md`.

## P1 — Phân tích tham số và trạng thái

### Tham số đầu vào

| Tham số | Vị trí | Kiểu AI suy luận | Bắt buộc | Ràng buộc / phân vùng AI nhận diện |
| :--- | :--- | :--- | :---: | :--- |
| `email` | JSON body | string | Có | Email của tài khoản; định dạng `local@domain`; tồn tại / không tồn tại; rỗng / null / sai kiểu; SQLi/XSS |
| `password` | JSON body | string | Có | Khớp mật khẩu tài khoản; rỗng / null / sai kiểu; AI giả định tối thiểu 8 ký tự ở login |
| `Content-Type` | header | string | Có | `application/json`; thiếu hoặc không phải JSON |
| `X-Student-Id` | header | string | Có trong bài HW06 | Mọi request phải mang đúng `23127207`; đây là ràng buộc kiểm toán bài làm, không phải nghiệp vụ của SUT |
| trường thừa (`role`, `__proto__`) | JSON body | any | Không | Không được làm thay đổi quyền hoặc prototype phía server |

### Trạng thái hệ thống

| Trạng thái | Điều kiện vào | Sự kiện | Trạng thái đúng theo FR-02 |
| :--- | :--- | :--- | :--- |
| Active-0 | Tài khoản không khóa, `login_attempts=0` | Sai mật khẩu | Active-1 |
| Active-1 | Một lần sai liên tiếp | Sai mật khẩu | Active-2 |
| Active-2 | Hai lần sai liên tiếp | Sai mật khẩu lần 3 | Locked-30s |
| Active-n | Chưa đủ 3 lần sai | Đăng nhập đúng | Active-0, trả JWT |
| Locked-30s | `locked_until` còn hiệu lực | Đúng hoặc sai mật khẩu | Giữ Locked, trả lỗi không tiết lộ nguyên nhân |
| Lock-expired | Đã quá 30 giây | Đăng nhập đúng | Active-0, trả JWT |
| Lock-expired | Đã quá 30 giây | Sai mật khẩu lần đầu | Active-1, không khóa lại ngay |

## P2–P5 — Danh sách test case AI sinh

| TC ID | Nhóm | Tiêu đề | Preconditions | Test data | Expected result theo output AI |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TC-API-LOGIN-001 | Partition | Email và mật khẩu hợp lệ | Seed user tồn tại, không khóa | `test@eshop.com` / `Test1234!` | `200`; body có `token` và `user` |
| TC-API-LOGIN-002 | Partition | Mật khẩu không khớp | Seed user tồn tại, attempts=0 | `test@eshop.com` / `Wrong123!` | `401`; lỗi chung `Invalid email or password` |
| TC-API-LOGIN-003 | Partition | Email không tồn tại | Không có user tương ứng | `missing@eshop.com` / `Any1234!` | `401`; cùng thông báo như sai mật khẩu |
| TC-API-LOGIN-004 | Partition | Thiếu email | DB sạch | `{"password":"Test1234!"}` | `400`; body có field `error` |
| TC-API-LOGIN-005 | Partition | Thiếu password | DB sạch | `{"email":"test@eshop.com"}` | `400`; body có field `error` |
| TC-API-LOGIN-006 | Partition | Email rỗng | DB sạch | `{"email":"","password":"Test1234!"}` | `400`; không truy vấn tài khoản |
| TC-API-LOGIN-007 | Partition | Mật khẩu dưới 8 ký tự | User tồn tại | `test@eshop.com` / `abc` | `400` vì mật khẩu login phải đạt chính sách độ mạnh |
| TC-API-LOGIN-008 | Partition | Email sai định dạng | DB sạch | `not-an-email` / `Test1234!` | `400`; lỗi validation email |
| TC-API-LOGIN-009 | Partition | Email có khoảng trắng hai đầu | User tồn tại | ` test@eshop.com ` / `Test1234!` | `200`; server tự trim email |
| TC-API-LOGIN-010 | Partition | Email null | DB sạch | `{"email":null,"password":"Test1234!"}` | `400`; lỗi kiểu dữ liệu |
| TC-API-LOGIN-011 | Partition | Password null | DB sạch | `{"email":"test@eshop.com","password":null}` | `400`; lỗi kiểu dữ liệu |
| TC-API-LOGIN-012 | Partition | Email kiểu number | DB sạch | `{"email":123,"password":"Test1234!"}` | `400`; lỗi kiểu dữ liệu |
| TC-API-LOGIN-013 | Partition | Password kiểu object | DB sạch | `{"email":"test@eshop.com","password":{}}` | `400`; lỗi kiểu dữ liệu |
| TC-API-LOGIN-014 | Partition | Body là JSON array | DB sạch | `[]` | `400`; lỗi cấu trúc body |
| TC-API-LOGIN-015 | Partition | Thiếu Content-Type JSON | DB sạch | Raw JSON nhưng không có `Content-Type` | `415 Unsupported Media Type` |
| TC-API-LOGIN-016 | Partition | Có field nghiệp vụ thừa | Seed user tồn tại, không khóa | Credentials đúng + `{"rememberMe":true}` | `200`; field thừa bị bỏ qua an toàn |
| TC-API-LOGIN-017 | State | Sai mật khẩu lần thứ nhất | User dùng-một-lần, attempts=0 | Wrong password một lần | `401`; attempts tăng thành 1, chưa khóa |
| TC-API-LOGIN-018 | State | Sai mật khẩu lần thứ hai | User dùng-một-lần, attempts=1 | Wrong password lần 2 | `401`; attempts tăng thành 2, chưa khóa |
| TC-API-LOGIN-019 | State | Sai mật khẩu lần thứ ba | User dùng-một-lần, attempts=2 | Wrong password lần 3 | `401`; hệ thống đặt khóa 30 giây |
| TC-API-LOGIN-020 | State | Đăng nhập đúng trong lúc khóa | User đã sai 3 lần, chưa qua 30 giây | Correct password | Lỗi không tiết lộ tài khoản bị khóa; không trả token |
| TC-API-LOGIN-021 | State | Khóa vẫn hiệu lực tại 29 giây | User vừa bị khóa | Chờ 29 giây rồi correct password | Vẫn bị từ chối, không trả token |
| TC-API-LOGIN-022 | State | Khóa hết hạn sau 31 giây | User vừa bị khóa | Chờ 31 giây rồi correct password | `200`; trả JWT; reset attempts và lock |
| TC-API-LOGIN-023 | State | Thành công reset chuỗi hai lần sai | User dùng-một-lần, attempts=0 | Sai 2 lần rồi đăng nhập đúng | Lần đúng trả `200`, tài khoản không bị khóa |
| TC-API-LOGIN-024 | State | Một lần sai sau khi reset thành công | Case 023 vừa hoàn tất | Sai password một lần | `401`; chỉ là lần sai thứ nhất, chưa khóa |
| TC-API-LOGIN-025 | Security | SQL injection qua email | Seed user tồn tại | email=`' OR 1=1 --`, password bất kỳ | Đăng nhập bypass thành công nếu truy vấn dễ tổn thương |
| TC-API-LOGIN-026 | Security | SQL injection qua password | Seed user tồn tại | password=`' OR '1'='1` | `401`; không bypass xác thực |
| TC-API-LOGIN-027 | Security | XSS payload trong email | DB sạch | `<script>alert(1)</script>` | `401/400`; payload không được phản chiếu trong body |
| TC-API-LOGIN-028 | Security | Không lộ password trong response thành công | Seed user tồn tại | Credentials đúng | `200`; `user` không có `password` |
| TC-API-LOGIN-029 | Security | Không lộ field xác thực nội bộ | Seed user tồn tại | Credentials đúng | Không có `reset_token`, `login_attempts`, `locked_until` |
| TC-API-LOGIN-030 | Security | Không thể chèn role admin từ body | Seed user role=user | Credentials đúng + `role:"admin"` | `200`; role trong token/user vẫn là `user` |
| TC-API-LOGIN-031 | Security | Token trả về dùng được với API bảo mật | Seed user tồn tại | Login rồi `GET /api/users/me` với Bearer token | Login `200`; API bảo mật `200` với đúng user |
| TC-API-LOGIN-032 | Security | Không tiết lộ trạng thái khóa | User đang bị khóa | Credentials đúng | Cùng status/message chung như thông tin đăng nhập không hợp lệ |
| TC-API-LOGIN-033 | Schema | Schema response thành công | Seed user tồn tại | Credentials đúng | `200`; object bắt buộc có `token:string`, `user:object` |
| TC-API-LOGIN-034 | Schema | Content-Type response thành công | Seed user tồn tại | Credentials đúng | Header khớp `application/json` |
| TC-API-LOGIN-035 | Schema | Schema response sai credential | Seed user tồn tại | Wrong password | `401`; object chỉ có `error:string` |
| TC-API-LOGIN-036 | Schema | Không có field thừa ở success | Seed user tồn tại | Credentials đúng | Body chỉ có `token` và `user`, không có field khác |

## Thống kê output AI

| Nhóm | Số lượng |
| :--- | ---: |
| Domain partition / BVA | 16 |
| State transition | 8 |
| Security | 8 |
| Schema validation | 4 |
| **Tổng** | **36** |
