# TC-FR02-UC-007: Báo lỗi khi để trống Email hoặc Password

## Requirement ID
FR02

## Module / Test Type / Technique
Login / Functional / Use Case Testing

## Source Use Case Scenario
- Scenario: UC-SC-07 (Báo lỗi khi để trống thông tin đăng nhập - Exception Flow 5)

## Preconditions
- Mở trang đăng nhập của EShop.

## Test Data
| Field | Value | Note |
| :--- | :--- | :--- |
| Email | [Trống] | Để trống email |
| Password | [Trống] | Để trống password |

## Test Steps
1. Để trống ô nhập Email.
2. Để trống ô nhập Password.
3. Bấm chọn nút "Đăng nhập".

## Expected Result
- Hệ thống hiển thị cảnh báo lỗi trường bắt buộc dưới các ô nhập tương ứng: "Email là bắt buộc", "Mật khẩu là bắt buộc".
- Sự kiện đăng nhập bị chặn lại tại client.

## Status / Related Bugs
- **Result**: Passed
- **Related Bug**: None
