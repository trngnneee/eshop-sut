## Title
[Major] Form Đăng nhập dùng tiếng Anh: "Username", "Sign In"

## Description
Nhãn ô nhập là "Username" và nút submit là "Sign In" (Login.jsx:28,58), lẫn tiếng Anh giữa UI tiếng Việt.

## Steps to Reproduce
1. Mở `/login`.
2. Đọc nhãn field và nút submit.

## Expected Result
Nhãn tiếng Việt ("Email"/"Tên đăng nhập"), nút "Đăng nhập".

## Actual Result
- (GUI-IA01-01) Nhãn field: "Username | Mật khẩu"; nút submit: "Sign In". Màn đăng nhập vẫn dùng chuỗi tiếng Anh ("Username", "Sign In") thay vì tiếng Việt.
- (GUI-IA01-02) Còn chuỗi tiếng Anh không phải thuật ngữ chuẩn trên UI: Username, Sign In (màn Đăng nhập).

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA01-01, GUI-IA01-02

## Requirement
FR-21 (nhất quán ngôn ngữ)

## Severity
Major — Vi phạm quy tắc nhất quán ngôn ngữ FR-21 trên màn hình chính.

## Screenshot
![GUI-IA01-01](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965687/eshop-hw03/gui-checklist/GUI-IA01-01.png) ![GUI-IA01-02](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965688/eshop-hw03/gui-checklist/GUI-IA01-02.png)