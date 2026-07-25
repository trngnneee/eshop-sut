## Title
[Minor] Field bắt buộc không có dấu * cạnh nhãn

## Description
Không field `required` nào hiển thị dấu `*`.

## Steps to Reproduce
1. Mở các form, đối chiếu field required với dấu *.

## Expected Result
Mỗi field bắt buộc có dấu `*` cạnh nhãn.

## Actual Result
- (GUI-IA02-01) Không field bắt buộc nào có dấu "*" cạnh nhãn trên các form (Đăng ký, Đăng nhập, Quên MK, Hồ sơ).

## Environment
Frontend Web (khách) localhost:5173 · React+Vite+Tailwind · Google Chrome · macOS · kiểm thử thủ công

## Related checklist item(s)
GUI-IA02-01

## Requirement
FR-22 (required indicator)

## Severity
Minor — Người dùng không biết field nào bắt buộc.

## Screenshot
![GUI-IA02-01](https://res.cloudinary.com/dnqinxiwo/image/upload/v1784965709/eshop-hw03/gui-checklist/GUI-IA02-01.png)