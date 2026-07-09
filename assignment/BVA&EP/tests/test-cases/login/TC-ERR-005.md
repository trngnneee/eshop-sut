# TC-ERR-005: Thông báo lỗi thân thiện khi API Server trả về lỗi hệ thống 500

## Requirement ID
FR-24

## Module / Test type / Technique
Privacy / Reliability Testing

## Preconditions
- Backend Server gặp lỗi hoặc trả về HTTP 500 Internal Server Error.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |

## Test steps
1. Thực hiện đăng nhập.

## Expected result
- Giao diện hiển thị lỗi thân thiện, ví dụ: 'Hệ thống đang gặp sự cố. Vui lòng thử lại sau.'
- Không hiển thị raw code, sql query hay stack trace trên giao diện của người dùng.

## Status / Related bugs
Pass / None
