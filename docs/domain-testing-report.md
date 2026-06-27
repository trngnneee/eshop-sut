# Tóm tắt yêu cầu

- **Chức năng:** Xem lịch sử đơn hàng (User)
- **Requirement ID:** FR-11
- **Module:** ORDER-HISTORY
- **Mô tả:** Người dùng đã đăng nhập có thể xem lịch sử các đơn hàng của chính mình. Giao diện hiển thị các thông tin quan trọng của đơn hàng và chuyển đổi ngôn ngữ/màu sắc cho các trạng thái đơn hàng một cách trực quan.
- **Input:** Trạng thái đăng nhập của người dùng, Lịch sử dữ liệu đơn hàng (0 hoặc nhiều).
- **Ràng buộc:** Người dùng chỉ xem được đơn hàng của chính mình.
- **Quy tắc validation:** Trạng thái đơn hàng phải được dịch sang tiếng Việt và có màu sắc phân biệt.

# Giải thích Domain Testing

Domain Testing được áp dụng để phân tích các giá trị đầu vào hợp lệ và không hợp lệ (mặc dù với FR-11, input chủ yếu đến từ trạng thái hệ thống và authentication).

1. **Xác định input cần kiểm thử:** Trạng thái đăng nhập, số lượng đơn hàng, quyền sở hữu đơn hàng, và các giá trị trạng thái.
2. **Xác định miền giá trị của input:** Như được mô tả trong bảng Domain Analysis.
3. **Xác định dữ liệu hợp lệ:** Đã đăng nhập, truy cập đơn hàng của chính mình, các trạng thái hợp lệ.
4. **Xác định dữ liệu không hợp lệ:** Chưa đăng nhập, cố gắng truy cập đơn hàng người khác.
5. **Xác định các trường hợp cần kiểm thử:** Tạo ra các test case bao phủ toàn bộ các domain này.

## Domain analysis table

| Biến | Domain | Loại giá trị | Khoảng giá trị | Mô tả |
|---|---|---|---|---|
| Trạng thái đăng nhập | Authentication | Boolean | True, False | Kiểm soát việc truy cập trang lịch sử. |
| Dữ liệu đơn hàng | Số lượng | Integer | 0, >0 | Đơn hàng của người dùng. |
| Quyền truy cập (Authz) | Chủ sở hữu | Object Match | Khớp, Không khớp | Đảm bảo không xem được đơn của người khác. |
| Trạng thái đơn hàng | Order State | Enum | pending, confirmed, shipping, delivered, canceled | Đảm bảo UI dịch ra tiếng Việt và phân biệt màu. |

# Giải thích Boundary Value Analysis

- Kỹ thuật Boundary Value Analysis (BVA) được áp dụng cho **số lượng đơn hàng** mà một người dùng có.
- **Minimum boundary:** Số lượng đơn hàng nhỏ nhất là 0.
- **Boundary 1 (0):** Kiểm tra hiển thị giao diện trống (Empty state) khi chưa mua hàng.
- **Boundary 2 (1):** Kiểm tra hiển thị danh sách khi vừa có 1 đơn hàng đầu tiên (min + 1). Không thể có -1 đơn hàng.
- Việc áp dụng BVA giúp đảm bảo logic render danh sách và empty state hoạt động hoàn hảo ở các cạnh của dữ liệu.

# Danh sách test case

- `TC-ORDERHISTORY-001`: Kiểm tra người dùng chưa đăng nhập không thể xem lịch sử đơn hàng
- `TC-ORDERHISTORY-002`: Kiểm tra hiển thị khi người dùng không có đơn hàng nào (BVA: 0 đơn hàng)
- `TC-ORDERHISTORY-003`: Kiểm tra hiển thị khi người dùng có ít nhất 1 đơn hàng (BVA: 1 đơn hàng)
- `TC-ORDERHISTORY-004`: Kiểm tra người dùng không thể xem đơn hàng của người khác
- `TC-ORDERHISTORY-005`: Kiểm tra hiển thị đầy đủ và đúng định dạng các trường thông tin
- `TC-ORDERHISTORY-006`: Kiểm tra hiển thị trạng thái "pending" (chờ xác nhận)
- `TC-ORDERHISTORY-007`: Kiểm tra hiển thị trạng thái "confirmed" (đã xác nhận)
- `TC-ORDERHISTORY-008`: Kiểm tra hiển thị trạng thái "shipping" (đang giao)
- `TC-ORDERHISTORY-009`: Kiểm tra hiển thị trạng thái "delivered" (đã giao)
- `TC-ORDERHISTORY-010`: Kiểm tra hiển thị trạng thái "canceled" (đã hủy)

# Coverage summary

- **Domain Coverage:** 100% các miền giá trị (đã đăng nhập/chưa đăng nhập, sở hữu/không sở hữu, 5 trạng thái đơn hàng).
- **Boundary Coverage:** Bao phủ trường hợp 0 đơn hàng và 1 đơn hàng.
- **Positive & Negative:** Bao gồm cả trường hợp hợp lệ (đã đăng nhập, xem đơn mình) và không hợp lệ (chưa đăng nhập, xem đơn người khác).
