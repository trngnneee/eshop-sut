## BUG-FR04-P-01 - Sai rule validate Số điện thoại

**GitHub issue title:** `[BUG][FR-04][Profile Management] Sai rule validate Số điện thoại so với yêu cầu`

**Labels:** `type: bug`, `status: new`, `found-by: test-case`

## Found by Test Case

- `FR04-P-BVA-TC02`
- `FR04-P-BVA-TC03`
- `FR04-P-BVA-TC04`
- `FR04-P-TC02`
- `FR04-P-TC03`
- `FR04-P-TC05`
- Paths:
  - `eshop-sut/tests/test-cases/profile_management/FR04-P-BVA-TC02.md`
  - `eshop-sut/tests/test-cases/profile_management/FR04-P-BVA-TC03.md`
  - `eshop-sut/tests/test-cases/profile_management/FR04-P-BVA-TC04.md`
  - `eshop-sut/tests/test-cases/profile_management/FR04-P-TC02.md`
  - `eshop-sut/tests/test-cases/profile_management/FR04-P-TC03.md`
  - `eshop-sut/tests/test-cases/profile_management/FR04-P-TC05.md`

## Requirement liên quan

- `FR-04`
- Số điện thoại hợp lệ phải bắt đầu bằng `0`, từ 10-11 chữ số.
- Source: `eshop-sut/README.md`

## Severity / Priority

Major / P1

## Environment

- **OS**: Ubuntu 24.04.4 LTS
- **Browser**: Brave Browser 149.1.91.178 
- **URL**: `http://localhost:5173`, `http://localhost:3000`
- **Build/Commit**: Latest

## Steps to reproduce

1. Đăng nhập bằng user hợp lệ.
2. Mở trang Hồ sơ.
3. Nhập lần lượt các số điện thoại theo test case: `0123456789`, `01234567890`, `012345678901`, `01234abcde`.
4. Bấm Cập nhật và quan sát thông báo validation.

## Expected result

- Hệ thống chấp nhận số điện thoại bắt đầu bằng `0` và có 10-11 chữ số.
- Hệ thống từ chối số điện thoại không đúng rule và hiển thị thông báo phù hợp với rule FR-04.

## Actual result

- Hệ thống từ chối số điện thoại hợp lệ bắt đầu bằng `0`.
- Thông báo validation yêu cầu nhập đúng 9-10 chữ số, không khớp rule FR-04 là bắt đầu bằng `0` và dài 10-11 chữ số.

## Evidence

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/39b7a11a-9196-4cb9-925f-d540e11a4630" />

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/092fd7f2-0a0d-4498-8594-42cd34ffa80e" />

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/e1793c1e-2103-4b36-9d28-a03674fc7c9a" />

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/fa830592-db28-46f0-b4b2-6d7ad8963873" />
