# Test Design for POST /api/register

## 1. Prompt (Dùng để sinh test case)
```text
Viết 12 Postman test script cho request:
- Method: POST
- URL: {{baseUrl}}/api/register
- Body mẫu (JSON): 
{
  "name": "Nguyen Van A",
  "email": "test@domain.com",
  "password": "Password123!"
}
- Response mẫu (status 200): {"message": "User registered successfully", "id": 1}

Yêu cầu sinh ra 12 test case bao phủ:
1. Happy Path: thông tin hợp lệ
2. Negative: Thiếu name, thiếu email, thiếu password (status 400)
3. Negative: Sai định dạng email (status 400)
4. Negative: Password yếu (vd: "123") (status 400)
5. Negative: Email đã tồn tại / trùng email (status 400 hoặc 409)
6. Boundary: Name rất dài hoặc rỗng (status 400)
7. Security: SQL Injection vào trường name hoặc email (vd: "test' OR 1=1--")
8. Schema Validation: Kiểm tra response schema trả về đúng format

Trả về định dạng bảng gồm các cột: tc_id, input, expected status, expected fields, rationale.
Không cần code JS, chỉ cần bảng.
```

## 2. AI Output (Rút gọn)
| tc_id | input | expected status | expected fields | rationale |
|---|---|---|---|---|
| AI-01 | Hợp lệ: name, email chuẩn, password mạnh | 200 | message, id | Happy path |
| AI-02 | Thiếu field `name` | 400 | message/error | Validation required field |
| AI-03 | Thiếu field `email` | 400 | message/error | Validation required field |
| AI-04 | Thiếu field `password` | 400 | message/error | Validation required field |
| AI-05 | Email sai định dạng (vd: `testdomain.com`) | 400 | message/error | Validation định dạng email |
| AI-06 | Password quá ngắn (vd: `123`) | 400 | message/error | Validation độ phức tạp mật khẩu |
| AI-07 | Email đã tồn tại trong hệ thống | 409 | message/error | Tránh đăng ký trùng lặp |
| AI-08 | Name rỗng (`""`) | 400 | message/error | Tên không được để trống |
| AI-09 | Name rất dài (vd: 300 ký tự) | 400 | message/error | Boundary: Vượt quá max length |
| AI-10 | SQL Injection trong email (`test' OR '1'='1`) | 400 | message/error | Security: Chống SQL Injection |
| AI-11 | XSS payload trong name (`<script>alert(1)</script>`) | 400 | message/error | Security: Chặn ký tự XSS |
| AI-12 | Schema response khi thành công | 200 | JSON Schema | Schema validation |

## 3. Bảng Audit (Human review)
| TC | Nhãn | Nhận xét hoặc chỉnh sửa |
|---|---|---|
| AI-01 | VALID | Test case cơ bản hợp lý |
| AI-02 | VALID | Cần thiết để kiểm tra validation missing field |
| AI-03 | VALID | Cần thiết để kiểm tra validation missing field |
| AI-04 | VALID | Cần thiết để kiểm tra validation missing field |
| AI-05 | VALID | Kiểm tra regex email hợp lệ |
| AI-06 | VALID | Giả định API có kiểm tra độ phức tạp password |
| AI-07 | VALID | Quan trọng, API có lưu ý "Cần test trường hợp email trùng" |
| AI-08 | VALID | Tên rỗng là một case biên phổ biến |
| AI-09 | INCOMPLETE | Cần xác định rõ độ dài tối đa là bao nhiêu. Giả sử 255 |
| AI-10 | INCOMPLETE | Nên expect 400 do sai định dạng email trước khi tới SQL Injection. Sửa lại thành inject vào name |
| AI-11 | VALID | Đảm bảo tính bảo mật |
| AI-12 | VALID | Kiểm tra schema là bắt buộc |

## 4. Test case tự bổ sung (Extend)
- **TC-13**: Content-Type header của response phải là `application/json`.
  *Lý do AI bỏ sót:* AI tập trung vào logic nghiệp vụ và dữ liệu body, bỏ sót các header kỹ thuật của HTTP.
- **TC-14**: Phản hồi của API đăng ký không chứa mật khẩu dưới dạng plaintext hoặc hash.
  *Lý do AI bỏ sót:* AI không tự thêm các yêu cầu bảo mật cụ thể về việc leak thông tin ở response nếu không nhắc nhở trong prompt.

## 5. Bảng Postman features
| Feature | Đã dùng? | Ghi chú |
|---|---|---|
| Collections | Có | Gom nhóm request của register API |
| Environment variables | Có | Dùng để lưu trữ `baseUrl` và `studentId` |
| Collection variables | Có | Dùng `pm.variables.set` để tạo body động từ Iteration Data |
| Pre-request scripts | Có | Dùng để thiết lập `X-Student-Id` header và lấy data file |
| Test scripts (assertions) | Có | Viết assertion kiểm tra `status code` và `Content-Type` |
| Data-driven runs | Có | Chạy 5 iteration dùng file `register.data.json` |
| Newman CLI | Có | Tích hợp script chạy trên GitHub Actions CI/CD |
| Monitors | Không | Không yêu cầu cấu hình monitor |
| Mock servers | Không | Đã test trực tiếp với server đang chạy |
| Workspaces | Có | Tạo không gian làm việc tách biệt trên Postman Desktop |
