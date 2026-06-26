# TC-REG-041: Đăng ký thành công nhưng gặp sự cố mạng/mất kết nối ngay lúc chuyển hướng

## Requirement ID
FR-01: Account registration

## Module / Test type / Technique
Register / Functional / Equivalence Partitioning

## Preconditions
- Không có.

## Test data
| Tham số | Giá trị |
| :--- | :--- |
| **name** | "Tester Network Lost" |
| **email** | "tester_network@domain.com" |
| **password** | "Secure123!" |
| **confirm_password** | "Secure123!" |

## Test steps
1. Gửi yêu cầu POST đăng ký đến `/api/register` với dữ liệu trên.

## Expected result
- Hệ thống không bị treo luồng, lưu trạng thái đăng ký thành công và hiển thị thông báo lỗi kết nối rõ ràng cho người dùng.

## Status / Related bugs
Pass / None
