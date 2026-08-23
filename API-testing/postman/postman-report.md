# 3. Các tính năng Postman đã sử dụng

| Tính năng | Cách sử dụng | Mục đích |
|---|---|---|
| Collections | Ba collection riêng: `forgot_password`, `apply_coupon`, `admin_coupons` | Giữ từng API độc lập, dễ chạy và review |
| Environment Variables | `baseUrl`, `studentId`, seed credentials, token placeholders | Tái sử dụng cấu hình local và CI |
| Collection Variables | Lưu `adminToken`, `userToken`, OTP, run IDs, fixture coupon IDs | Chia sẻ state giữa pre-request và test scripts |
| Pre-request Scripts | Build request động, login khi cần, sinh forged tokens, tạo/xóa fixtures | Hỗ trợ stateful và security tests |
| Test Scripts | Assert status, JSON schema, business values, sensitive fields, skip/blocked behavior | Biến mỗi CSV/data row thành executable validation |
| Data-driven Testing | Các file `data/*.test-data.json` điều khiển iterations | Một iteration tương ứng một test case |
| Collection Runner / Newman | Newman chạy collection từ CLI | Thực thi lặp lại được ở local và CI |

### Bằng chứng `X-Student-Id`
![](../artifacts/student-id-header-attached.png)

![](../artifacts/student-id-header.png)
