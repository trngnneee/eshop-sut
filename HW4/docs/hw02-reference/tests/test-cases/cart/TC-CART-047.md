# TC-CART-047: Thêm sản phẩm vào giỏ hàng khi chưa đăng nhập

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
| Số lượng mua | `1` |

## Test steps
1. Xóa toàn bộ token / sử dụng trình duyệt ẩn danh để đảm bảo chưa đăng nhập.
2. Truy cập trang chi tiết sản phẩm bất kỳ.
3. Nhập số lượng là 1 và bấm nút "Thêm vào giỏ hàng" (hoặc gửi request `POST /api/cart` không kèm token xác thực).

## Expected result
- Hệ thống từ chối cho phép thêm sản phẩm và yêu cầu người dùng đăng nhập (hoặc tự động chuyển hướng về trang `/login`).
- API backend từ chối yêu cầu và phản hồi mã lỗi `401 Unauthorized`.

## Status / Related bugs
Failed / BUG-FR07-B-09
