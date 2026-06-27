# TC-CART-048: Truy cập /cart khi chưa đăng nhập

## Requirement ID
FR-07, FR-23

## Module / Test type / Technique
Cart / Security / Access Control / Negative

## Preconditions
- Người dùng chưa thực hiện đăng nhập vào hệ thống.
- Không có token JWT được lưu trữ trong cookies hoặc localStorage.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Mở trình duyệt ở chế độ ẩn danh hoặc xóa toàn bộ cookies/localStorage.
2. Truy cập trực tiếp vào đường dẫn `/cart`.

## Expected result
- Hệ thống không hiển thị giao diện giỏ hàng cá nhân.
- Người dùng được điều hướng về trang đăng nhập `/login` hoặc nhận thông báo yêu cầu đăng nhập.

## Status / Related bugs
Not Run / None
