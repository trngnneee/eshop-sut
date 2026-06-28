## Test Case ID

TC-USERMGMT-021

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

## Testing Technique

Domain Testing

## Test Objective

Kiểm tra Admin xóa người dùng đang có dữ liệu liên quan (đơn hàng, giỏ hàng, lịch sử mua hàng) và đảm bảo hệ thống xử lý dữ liệu liên kết đúng cách, không gây lỗi hoặc mất dữ liệu ngoài mong muốn.

## Preconditions

* Admin đã đăng nhập thành công.
* Tồn tại một tài khoản user thường có dữ liệu liên quan trong hệ thống.
* User cần xóa có ít nhất:

  * 1 đơn hàng hoặc
  * dữ liệu giỏ hàng/lịch sử giao dịch.

## Test Data

| Parameter         | Value                            |
| ----------------- | -------------------------------- |
| Người dùng bị xóa | user_A                           |
| Dữ liệu liên quan | order_001, cart_001, history_001 |

## Test Steps

1. Đăng nhập với tài khoản Admin.
2. Vào trang Quản lý Người dùng.
3. Xác định user_A đang có dữ liệu liên quan trong hệ thống.
4. Thực hiện xóa user_A.
5. Xác nhận thao tác xóa.
6. Kiểm tra trạng thái xóa và dữ liệu liên quan sau khi hoàn tất.

## Expected Result

* Hệ thống xử lý thao tác xóa user đúng theo thiết kế.
* Không xảy ra lỗi database hoặc crash hệ thống.
* Dữ liệu liên quan của user được xử lý đúng:

  * Xóa cascade nếu hệ thống hỗ trợ.
  * Hoặc từ chối xóa nếu dữ liệu liên quan không cho phép xóa.
* Không ảnh hưởng đến dữ liệu của các tài khoản khác.

## Actual Result

User đã bị xóa tài khoản nhưng hệ thống vẫn còn dữ liệu đơn hàng liên quan đến user đã bị xóa. Hệ thống không cảnh báo hoặ chặn xóa user có dữ liệu liên quan.

## Status

FAILED

## Bug Reference
[\[BUG\]\[User Management\] Xóa người dùng có dữ liệu liên quan nhưng không xử lý dữ liệu liên kết](https://github.com/trngnneee/eshop-sut/issues/153#issue-4762495069)




