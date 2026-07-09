# TC-JWT-003: Kiểm tra Token JWT bị thay đổi thông tin Payload

## Requirement ID
SEC-02

## Module / Test type / Technique
JWT / Security Testing

## Preconditions
- Có token JWT hợp lệ từ server, sau đó chỉnh sửa payload bằng tay (ví dụ đổi role thành 'admin').

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Payload | Tampered JWT |

## Test steps
1. Gửi yêu cầu API private kèm token đã bị chỉnh sửa payload nhưng giữ nguyên signature cũ.

## Expected result
- Backend phát hiện chữ ký signature không khớp với payload mới và trả về HTTP 401/403.

## Status / Related bugs
Pass / None
