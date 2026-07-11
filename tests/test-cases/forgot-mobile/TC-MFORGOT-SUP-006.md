# TC-MFORGOT-SUP-006: Lỗi validation hiển thị trên nút submit (FR-22) — không dùng Alert

## Requirement ID
FR-22

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Domain Testing – Supplementary

## Preconditions
- Mobile App (React Native + Expo) đang chạy và kết nối Backend API tại IP LAN máy chủ
- Đang ở Bước 2 sau khi lấy OTP hợp lệ

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | [OTP hợp lệ] |
| Mật khẩu mới | weakpass |

## Test steps
1. Hoàn thành Bước 1, vào Bước 2.
2. Nhập OTP hợp lệ và mật khẩu yếu `weakpass`.
3. Bấm "Đặt lại mật khẩu".
4. Quan sát: lỗi phải là **inline text phía trên nút**, không phải `Alert.alert` popup.

## Expected result
- Thông báo lỗi xuất hiện inline (ví dụ `errorBoxText`) **trên** nút submit theo FR-22.
- Không dùng dialog Alert làm phản hồi validation chính.

## Sub-domains covered
GAP-07 — FR-22 error placement on Mobile

## Type
Invalid

## Status / Related bugs
Fail / #21