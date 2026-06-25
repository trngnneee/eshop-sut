# TC-ERR-006: Hiển thị thông báo lỗi tương ứng khi Validation thất bại trên nhiều trường

## Requirement ID
FR-22

## Module / Test type / Technique
Privacy / UI Testing

## Preconditions
- Trang đăng nhập đang mở.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | invalidemail |
| Mật khẩu | short |

## Test steps
1. Nhập email sai định dạng.
2. Nhập mật khẩu quá ngắn.
3. Nhấn Đăng nhập.

## Expected result
- Hệ thống hiển thị lỗi cụ thể của cả hai trường bên dưới hoặc bên cạnh ô nhập liệu tương ứng.

## Status / Related bugs
Not Run / None
