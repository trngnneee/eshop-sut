# TC-LOGIN-032: Đăng nhập thất bại khi Email chỉ chứa khoảng trắng

## Requirement ID
FR-02, FR-22

## Module / Test type / Technique
Login / Equivalence Partitioning (EP)

## Preconditions
- Trang đăng nhập đang mở.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email |     |
| Mật khẩu | ValidPassword1! |

## Test steps
1. Nhập chuỗi chỉ gồm các khoảng trắng vào trường Email.
2. Nhập mật khẩu đúng.
3. Nhấn nút 'Đăng nhập'.

## Expected result
- Hệ thống hiển thị lỗi bắt buộc hoặc định dạng không hợp lệ.
- Ngăn không cho gửi yêu cầu lên backend.

## Status / Related bugs
Pass / None
