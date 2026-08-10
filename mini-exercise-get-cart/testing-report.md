# Báo cáo Mini Exercise - API Testing

## 1. Thông tin bài làm

| Mục | Nội dung |
| --- | --- |
| API được chọn | `GET /api/cart` |
| Chức năng | Lấy giỏ hàng hiện tại của người dùng đã đăng nhập |
| Authentication | Bắt buộc header `Authorization: Bearer <token>` |
| Provider | `eshop-sut` backend tại `http://localhost:3000` |
| Công cụ kiểm thử | Postman, Newman, GitHub Actions |
| Dạng kiểm thử | Data-driven API testing |

Hành vi API được xác định từ `backend/server.js`: nếu thiếu token thì trả `401 Unauthorized`, token không hợp lệ trả `403 Forbidden`, token hợp lệ trả về một mảng giỏ hàng của user hiện tại. Giỏ hàng được lưu trong biến bộ nhớ `userCarts`, vì vậy dữ liệu cart sẽ mất khi backend restart.

## 2. Generate with AI

### Prompt đã sử dụng

> Design at least 12 API test cases for `GET /api/cart` in an Express e-shop backend. The endpoint requires `Authorization: Bearer <token>` and returns the authenticated user's cart array. The auth token is obtained from `POST /api/login` using seeded account `test@eshop.com` / `Test1234!`. The API should be tested for domain partitions, security, schema validation, response headers, response time, and data-driven execution. Return columns: `id`, `input`, `expected status`, `expected fields`, and `rationale`.

### Kết quả test case AI đề xuất

| ID | Input | Expected status | Expected fields | Rationale |
| --- | --- | --- | --- | --- |
| AI-01 | Token hợp lệ, user chưa có sản phẩm trong giỏ | 200 | Response là JSON array, length `0` | Kiểm tra positive case cơ bản với cart rỗng. |
| AI-02 | Token hợp lệ, đã thêm 1 sản phẩm trước khi gọi GET | 200 | Array có item đầu tiên gồm `id`, `name`, `price`, `quantity` | Kiểm tra luồng lấy giỏ hàng sau khi có dữ liệu. |
| AI-03 | Token hợp lệ, đã thêm nhiều sản phẩm | 200 | Array length >= 2 | Kiểm tra API trả danh sách nhiều dòng cart. |
| AI-04 | Không gửi `Authorization` header | 401 | Object có field `error` | Xác nhận API bắt buộc xác thực. |
| AI-05 | `Authorization: Bearer invalid-token` | 403 | Object có field `error` | Kiểm tra JWT không hợp lệ bị từ chối. |
| AI-06 | Header sai scheme: `Token <jwt>` | 403 | Object có field `error` | Kiểm tra xử lý định dạng auth header không chuẩn. |
| AI-07 | Header `Authorization: Bearer` không có token | 401 | Object có field `error` | Boundary case cho auth header thiếu giá trị token. |
| AI-08 | Token hợp lệ của admin | 200 | Response là JSON array | API chỉ yêu cầu authenticated user, không giới hạn role. |
| AI-09 | Token dạng chuỗi tấn công như SQL injection | 403 | Object có field `error` | Kiểm tra đầu vào độc hại ở lớp xác thực. |
| AI-10 | Token hợp lệ kèm query string không tài liệu hóa `?debug=true` | 200 | Response là JSON array | API nên bỏ qua query không liên quan một cách an toàn. |
| AI-11 | Token hợp lệ, kiểm tra `Content-Type` | 200 | Header có `application/json` | Kiểm tra contract response header. |
| AI-12 | Token hợp lệ, kiểm tra response time | 200 | Response time `< 1000 ms` | API đọc dữ liệu trong bộ nhớ nên cần phản hồi nhanh. |

## 3. Audit kết quả AI

| TC | Nhãn | Nhận xét hoặc chỉnh sửa |
| --- | --- | --- |
| AI-01 | VALID | Phù hợp với implementation vì backend khởi tạo `userCarts[userId] = []` nếu user chưa có cart. |
| AI-02 | VALID | Phù hợp với luồng chính, nhưng cần setup bằng `POST /api/cart` trước khi gọi `GET /api/cart`. |
| AI-03 | IMPROVED | Case nhiều item có giá trị, nhưng trong phạm vi data-driven 5 iterations chỉ chọn 1 setup item để giữ bộ test gọn và ổn định. |
| AI-04 | VALID | Khớp với middleware `authenticateToken`, thiếu token trả `401`. |
| AI-05 | VALID | Khớp với `jwt.verify`, token sai trả `403`. |
| AI-06 | IMPROVED | Backend lấy token bằng `authHeader.split(" ")[1]`, nên sai scheme nhưng có token thật vẫn có thể đi qua; chỉnh test thành malformed/invalid token để kỳ vọng `403` ổn định hơn. |
| AI-07 | VALID | Header `Bearer` không có token tạo token rỗng, middleware trả `401`. |
| AI-08 | VALID | Route không kiểm tra role, nên admin token vẫn được phép gọi API. |
| AI-09 | VALID | Token không đưa vào SQL, nhưng chuỗi độc hại vẫn phải bị JWT validation từ chối. |
| AI-10 | VALID | Query không tài liệu hóa không ảnh hưởng route hiện tại, response vẫn là cart array. |
| AI-11 | VALID | Header JSON là một phần contract cần xác minh. |
| AI-12 | VALID | Response time assertion phù hợp với API nhẹ, ít logic xử lý. |

## 4. Extend - Test case tự bổ sung

| ID | Input | Expected status | Expected fields | Lý do AI có thể bỏ sót |
| --- | --- | --- | --- | --- |
| EX-01 | User A đã có item trong cart, sau đó gọi API bằng token của User B/admin | 200 | Response của User B/admin không chứa item của User A | AI thường bỏ sót kiểm thử cô lập dữ liệu giữa người dùng và rủi ro IDOR. |
| EX-02 | Token hợp lệ sau khi backend restart | 200 | Response là `[]` | AI thường giả định cart được lưu bền vững, trong khi implementation hiện tại lưu cart trong memory. |

## 5. Thiết kế data-driven test

Các test case được chọn để chạy tự động trong Postman/Newman được lưu tại `get-cart-data.json`. Bộ dữ liệu gồm 5 iterations, bao phủ positive case, setup dữ liệu cart, thiếu token, token sai và token malformed.

| Case ID | Auth mode | Setup cart | Expected status | Expected body |
| --- | --- | --- | --- | --- |
| `GET_CART_EMPTY_VALID_TOKEN` | Valid user token | No | 200 | JSON array, có thể rỗng |
| `GET_CART_WITH_ITEM_VALID_TOKEN` | Valid user token | Yes | 200 | JSON array có ít nhất 1 item |
| `GET_CART_MISSING_TOKEN` | Missing token | No | 401 | Object có field `error` |
| `GET_CART_INVALID_TOKEN` | Invalid token | No | 403 | Object có field `error` |
| `GET_CART_MALFORMED_BEARER` | Malformed bearer token | No | 403 | Object có field `error` |

## 6. Execution summary

| Nội dung | Kết quả |
| --- | --- |
| Postman collection | `get-cart.postman_collection.json` |
| Postman environment | `get-cart.postman_environment.json` |
| Iteration data | `get-cart-data.json` |
| Newman report | `get-cart-newman-report.json` |
| Số iterations kỳ vọng | 5 |
| Assertion chính | Status code, JSON content type, response time, `X-Student-Id`, body schema, error schema |
| Kết quả mong đợi | 5 iterations pass, 0 failed assertions |

Collection sử dụng pre-request script để login bằng seeded account `test@eshop.com` / `Test1234!`, lấy token, gắn `Authorization` header và chuẩn bị cart item khi iteration yêu cầu. Test script kiểm tra response theo dữ liệu từng iteration.

## 7. Postman features đã sử dụng

| Feature | Áp dụng? | Ghi chú |
| --- | --- | --- |
| Collections | Có | Tạo collection `Mini Exercise - GET /api/cart` để tổ chức request kiểm thử. |
| Environment variables | Có | Dùng `base_url`, `student_id`, `auth_token` để quản lý cấu hình chạy. |
| Collection variables | Không | Không cần dùng vì biến dùng chung đã đặt trong environment và data file. |
| Pre-request scripts | Có | Dùng để gắn `X-Student-Id`, login, set bearer token và setup cart item. |
| Test scripts (assertions) | Có | Dùng assertion cho status code, content type, response time, header, body schema và error schema. |
| Data-driven runs (Collection Runner + data file) | Có | Dùng `get-cart-data.json` để chạy 5 iterations tự động. |
| Newman CLI | Có | Dùng Newman để chạy collection và xuất JSON report. |
| Monitors | Không | Không dùng vì phạm vi bài tập chạy local và CI. |
| Mock servers | Không | Không dùng vì có backend provider thật của `eshop-sut`. |
| Workspaces | Có | Dùng workspace/project hiện tại để quản lý collection, environment và export file. |

## 8. CI/CD summary

Workflow CI/CD được tạo tại `.github/workflows/get-cart-newman-tests.yml`. Workflow chạy trên GitHub Actions khi có `push` hoặc `pull_request`, tự cài dependencies backend, khởi động provider, đợi backend sẵn sàng, chạy Newman và upload report artifact.

| Minh chứng CI/CD | File/ghi chú |
| --- | --- |
| Workflow file | `.github/workflows/get-cart-newman-tests.yml` |
| Pass pipeline screenshot | `ci-pass.png` |
| Fail pipeline screenshot | `ci-fail.png` |
| Report artifact | `get-cart-newman-report.json` |
| Trạng thái cuối cùng | Pipeline cần được khôi phục về pass sau commit fail có chủ đích |

## 9. Thành phần nộp bài

| Thành phần | File |
| --- | --- |
| Báo cáo test design | `testing-report.md` |
| Postman collection | `get-cart.postman_collection.json` |
| Postman environment | `get-cart.postman_environment.json` |
| Iteration data | `get-cart-data.json` |
| Newman report | `get-cart-newman-report.json` |
| GitHub Actions workflow | `.github/workflows/get-cart-newman-tests.yml` |
| Ảnh pipeline pass | `ci-pass.png` |
| Ảnh pipeline fail | `ci-fail.png` |
