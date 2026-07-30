# [BUG-GUI-05] Mobile Login Label & Submit Button Language Inconsistency

**Platform:** Mobile App  
**Screen/Route:** Screen Login  
**Related Requirement:** FR-02 (Mobile Authentication)  
**Severity:** Low | **Priority:** Low  
**Status:** PENDING_EXTERNAL_ACTION  

## Description & Steps to Reproduce
1. Khởi chạy App Mobile trên Expo/Emulator/Trình duyệt.
2. Chuyển tới màn hình Đăng Nhập.
3. Quan sát nhãn phía trên ô Email và tên ghi trên nút submit Đăng nhập.

## Expected Result
- Nhãn phía trên ô email ghi 'Email'
- Nút đăng nhập ghi tiếng Việt 'Đăng nhập'

## Actual Result
- Nhãn phía trên ô ghi 'Username' (trong khi placeholder bên trong ghi 'Email')
- Nút đăng nhập ghi tiếng Anh 'Sign In' lẫn lộn tiếng Việt

## Evidence Screenshot
![Screenshot](../../evidence/mobile-login/BUG-GUI-05_mobile-login.png)
