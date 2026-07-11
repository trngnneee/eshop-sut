# TC-MFORGOT-026: Kiểm thử Email với độ dài vượt quá tối đa (101 ký tự) — Bước 1

## Requirement ID
FR-22

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Boundary Value Analysis

## Boundary under test
Email at max+ — value: 101 ký tự

## Preconditions
- Người dùng đang ở Bước 1 của màn hình Quên Mật Khẩu trên Mobile App

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa |

## Test steps
1. Mở Mobile App, vào màn hình Đăng nhập, bấm "Quên mật khẩu?" để vào màn hình Quên Mật Khẩu (Bước 1).
2. Nhập Email có độ dài 101 ký tự.
3. Bấm "Lấy mã OTP".

## Expected result
- Hệ thống báo lỗi độ dài Email vượt quá giới hạn tối đa 100 ký tự.
- Không chuyển sang Bước 2.

## Valid / Invalid
Invalid

## Status / Related bugs
Fail / None