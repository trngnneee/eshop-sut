# TC-OAUTH-003: Người dùng hủy (Cancel) quá trình cấp quyền tại màn hình Google Consent

## Requirement ID
FR-02

## Module / Test type / Technique
OAuth / Functional Testing

## Preconditions
- Trang đăng nhập đang mở.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |

## Test steps
1. Click đăng nhập bằng Google.
2. Tại màn hình cấp quyền của Google, click 'Hủy' (Cancel) hoặc quay lại.

## Expected result
- Hệ thống chuyển hướng an toàn trở lại trang Login.
- Hiển thị thông báo phù hợp hoặc không báo lỗi crash hệ thống.

## Status / Related bugs
Failed / #45
