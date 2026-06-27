# TC-JWT-005: Kiểm tra Token JWT không lộ trên URL trình duyệt sau khi đăng nhập

## Requirement ID
SEC-01

## Module / Test type / Technique
JWT / Security Testing

## Preconditions
- Đăng nhập thành công và chuyển hướng về trang Dashboard.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |

## Test steps
1. Quan sát thanh địa chỉ (URL) của trình duyệt sau khi chuyển hướng.

## Expected result
- URL không chứa bất kỳ JWT token hoặc thông tin session nhạy cảm nào dưới dạng query string.

## Status / Related bugs
Not Run / None
