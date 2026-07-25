## Title
[Minor] Message khoá tài khoản không phân biệt với sai mật khẩu

## Description
Sau 3 lần sai, UI vẫn hiện "Đăng nhập thất bại. Vui lòng kiểm tra lại." (Login.jsx:17-19).

## Steps to Reproduce
1. Đăng nhập sai 3 lần, thử lần 4, quan sát thông báo.

## Expected Result
Message phân biệt "sai mật khẩu" và "tài khoản đang khoá" (kèm thời gian).

## Actual Result
- (GUI-IA04-11) Sau 3 lần đăng nhập sai (tài khoản đã bị backend khoá), UI vẫn hiện message chung "Đăng nhập thất bại. Vui lòng kiểm tra lại." — không phân biệt "sai mật khẩu" với "đang bị khoá", không nói thời gian mở khoá.

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA04-11

## Requirement
FR-24 + FR-02 (lockout messaging)

## Severity
Minor — Người dùng không biết tài khoản đang bị khoá 30s.

## Screenshot
![GUI-IA04-11](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965770/eshop-hw03/gui-checklist/GUI-IA04-11.png)