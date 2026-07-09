# TC-FR02-UC-006: Báo lỗi khi email sai định dạng

## Requirement ID
FR02

## Module / Test Type / Technique
Login / Functional / Use Case Testing

## Source Use Case Scenario
- Scenario: UC-SC-06 (Báo lỗi khi email sai định dạng - Exception Flow 4)

## Preconditions
- Mở trang đăng nhập của EShop.

## Test Data
| Field | Value | Note |
| :--- | :--- | :--- |
| Email | invalid-email-format | Định dạng email không hợp lệ |
| Password | Test1234! | Mật khẩu bất kỳ |

## Test Steps
1. Nhập Email `invalid-email-format` vào trường Email.
2. Nhập Password `Test1234!`.
3. Bấm nút "Đăng nhập".

## Expected Result
- Hệ thống chặn sự kiện submit ngay ở phía Client (Frontend Validation) hoặc nhận diện lỗi ở Backend API.
- Hiển thị thông báo lỗi cụ thể dưới ô nhập email: "Email không hợp lệ" hoặc tương đương.
- Không gửi request xác thực lên server nếu frontend validation được cài đặt tốt.

## Status / Related Bugs
- **Result**: Passed
- **Related Bug**: None
