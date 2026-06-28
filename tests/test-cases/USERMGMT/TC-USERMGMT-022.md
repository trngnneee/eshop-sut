## Test Case ID

TC-USERMGMT-022

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

## Testing Technique

Domain Testing

## Test Objective

Kiểm tra API xóa người dùng không trả về hoặc làm lộ dữ liệu nhạy cảm của người dùng sau khi thực hiện thao tác xóa (đặc biệt là mật khẩu).

## Preconditions

* Admin đã đăng nhập thành công.
* Tồn tại ít nhất một user thường trong hệ thống.
* User có dữ liệu đầy đủ trong database bao gồm thông tin bảo mật.

## Test Data

| Parameter                     | Value                              |
| ----------------------------- | ---------------------------------- |
| Người dùng bị xóa             | user_A                             |
| Dữ liệu nhạy cảm cần kiểm tra | password, token, thông tin bảo mật |

## Test Steps

1. Đăng nhập bằng tài khoản Admin.

2. Gọi API xóa user:

   ```
   DELETE /api/admin/users/{user_id}
   ```

3. Quan sát response trả về từ API.

4. Kiểm tra dữ liệu trong response sau khi xóa.

5. Kiểm tra API danh sách người dùng sau khi xóa.

## Expected Result

* API xóa user trả về kết quả thành công hoặc thông báo phù hợp.
* Response không chứa:

  * password
  * mật khẩu đã mã hóa
  * token
  * thông tin bảo mật khác
* Danh sách user sau khi xóa không còn user đã bị xóa.
* Không có dữ liệu nhạy cảm bị lộ qua API.

## Actual Result

Response API không trả về dữ liệu nhạy cảm. Danh sách user được cập nhật đúng sau khi xóa.

## Status

PASSED

## Bug Reference

None