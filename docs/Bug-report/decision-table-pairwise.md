[BUG][Order State Machine] API cập nhật trạng thái đơn hàng của Admin không kiểm tra quyền truy cập theo vai trò (Role-based Authorization Bypass)

## Found by Test Case

TC-ORDER-002, TC-ORDER-007, TC-ORDER-012

## Requirement liên quan

FR-10

## Severity / Priority

Critical / P1

## Environment

* **OS**: Android / iOS

* **Application**: Mobile App / Admin API

* **Feature**: Order State Machine - Cập nhật trạng thái đơn hàng

* **API Endpoint**:

```text
PUT /api/admin/orders/:id/status
```

* **Build/Commit**: Latest

## Steps to reproduce

1. Tạo hoặc sử dụng một tài khoản người dùng thông thường với:

```text
role = user
```

2. Đăng nhập vào hệ thống bằng tài khoản user.

3. Lấy access token của tài khoản user sau khi đăng nhập.

4. Gửi request cập nhật trạng thái đơn hàng tới API Admin:

```http
PUT /api/admin/orders/:id/status
```

với header:

```http
Authorization: Bearer <user_token>
```

và body:

```json
{
  "status": "confirmed"
}
```

5. Thử cập nhật trạng thái sang các trạng thái khác:

```text
confirmed
shipping
delivered
```

6. Quan sát kết quả trả về từ API và trạng thái đơn hàng.

## Expected result

API phải:

* Kiểm tra quyền truy cập của người dùng trước khi thực hiện cập nhật.

* Chỉ cho phép tài khoản có:

```text
role = admin
```

được phép gọi API:

```text
PUT /api/admin/orders/:id/status
```

* Nếu người dùng không có quyền:

Ví dụ:

```text
role = user
```

API phải trả về lỗi:

```http
403 Forbidden
```

và không thay đổi trạng thái đơn hàng.

Ví dụ response:

```json
{
  "message": "Access denied. Admin role required."
}
```

* Trạng thái đơn hàng phải giữ nguyên.

## Actual result

API chỉ kiểm tra token thông qua middleware:

```text
authenticateToken
```

nhưng không kiểm tra quyền:

```text
role = admin
```

Người dùng thông thường (`role = user`) vẫn có thể gọi trực tiếp API Admin bằng token hợp lệ và thay đổi trạng thái của bất kỳ đơn hàng nào.

Ví dụ:

Request:

```http
PUT /api/admin/orders/12/status
```

Body:

```json
{
  "status": "delivered"
}
```

được xử lý thành công dù tài khoản gọi API không có quyền Admin.

Điều này dẫn đến việc user có thể:

* Xác nhận đơn hàng trái phép.
* Chuyển đơn hàng sang trạng thái đang giao.
* Đánh dấu đơn hàng đã hoàn tất.

Bug này gây sai lệch dữ liệu Order State Machine và tạo lỗ hổng **Role-based Authorization Bypass**.

---


# [BUG][Order State Machine] Khách hàng có thể tự hủy đơn hàng khi đã chuyển sang trạng thái shipping

## Found by Test Case

TC-ORDER-014

## Requirement liên quan

FR-10, FR-20

## Severity / Priority

Major / P2

## Environment

* **OS**: Android / iOS / Web API

* **Application**: Mobile App + Backend API

* **Feature**: Hủy đơn hàng (Cancel Order)

* **API Endpoint**:

```text
PUT /api/orders/:id/cancel
```

* **Build/Commit**: Latest

## Steps to reproduce

1. Đăng nhập bằng tài khoản khách hàng có đơn hàng thuộc quyền sở hữu.

2. Đảm bảo đơn hàng đang ở trạng thái:

```text
shipping
```

3. Truy cập:

```text
Lịch sử đơn hàng
```

4. Chọn đơn hàng đang giao.

5. Thực hiện thao tác:

```text
Hủy đơn hàng
```

hoặc gửi trực tiếp API request:

```http
PUT /api/orders/:id/cancel
```

6. Quan sát kết quả trả về.

## Expected result

Hệ thống phải kiểm tra trạng thái hiện tại của đơn hàng trước khi cho phép hủy.

Theo rule của Order State Machine:

* Chỉ cho phép hủy khi đơn hàng ở trạng thái:

```text
pending
```

hoặc trạng thái được định nghĩa cho phép hủy.

* Không cho phép hủy khi đơn hàng đã chuyển sang:

```text
shipping
```

* API phải trả về lỗi:

```text
400 Bad Request
```

hoặc

```text
409 Conflict
```

và giữ nguyên trạng thái đơn hàng.

## Actual result

API chỉ kiểm tra đơn hàng có đang ở trạng thái kết thúc hay không:

```text
delivered
canceled
```

mà không kiểm tra các trạng thái trung gian.

Khi đơn hàng đang ở trạng thái:

```text
shipping
```

khách hàng vẫn có thể gọi API:

```text
PUT /api/orders/:id/cancel
```

và hệ thống cập nhật thành công trạng thái:

```text
canceled
```

Điều này làm sai luồng chuyển trạng thái của Order State Machine, cho phép khách hàng hủy đơn khi đơn đã được giao cho vận chuyển.

Đơn hàng bị hủy thành công dù trạng thái hiện tại không thuộc nhóm trạng thái được phép hủy.

---