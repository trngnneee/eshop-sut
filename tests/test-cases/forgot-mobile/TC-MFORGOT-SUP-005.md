# TC-MFORGOT-SUP-005: Bước 2 phải có trường Xác nhận mật khẩu mới

## Requirement ID
FR-22

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Domain Testing – Supplementary

## Preconditions
- Mobile App (React Native + Expo) đang chạy và kết nối Backend API tại IP LAN máy chủ
- Đã hoàn thành Bước 1 với Email `test@eshop.com`

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| (Không áp dụng) | — |

## Test steps
1. Mở Mobile App, vào màn hình Đăng nhập, bấm "Quên mật khẩu?" để vào màn hình Quên Mật Khẩu; hoàn thành Bước 1 với `test@eshop.com`.
2. Trên Bước 2, đếm các trường nhập mật khẩu (`secureTextEntry`) hoặc tìm label "Xác nhận mật khẩu".

## Expected result
- Có **hai** trường mật khẩu: "Mật khẩu mới" và "Xác nhận mật khẩu mới".
- Hiện tại SUT chỉ có một trường → Fail.

## Sub-domains covered
GAP-06 — confirm-password field present

## Type
Valid

## Status / Related bugs
Fail / #4