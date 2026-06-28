## BUG-FR04-A-01 - Thiếu validate Địa chỉ giao hàng

**GitHub issue title:** `[BUG][FR-04][Profile Management] Thiếu validate bắt buộc và độ dài Địa chỉ giao hàng`

**Labels:** `type: bug`, `status: new`, `found-by: test-case`

## Found by Test Case

- `FR04-A-TC01`
- `FR04-A-BVA-TC01`
- `FR04-A-BVA-TC07`
- `FR04-A-TC03`
- Paths:
  - `eshop-sut/tests/test-cases/profile_management/FR04-A-TC01.md`
  - `eshop-sut/tests/test-cases/profile_management/FR04-A-BVA-TC01.md`
  - `eshop-sut/tests/test-cases/profile_management/FR04-A-BVA-TC07.md`
  - `eshop-sut/tests/test-cases/profile_management/FR04-A-TC03.md`

## Requirement liên quan

- `FR-04`
- Test assumption: `shipping_address` bắt buộc, độ dài hợp lệ 5-255 ký tự sau khi trim.
- Source: `eshop-sut/tests/test-summary/fr04-profile-management-summary.md`

## Severity / Priority

Major / P2

## Environment

- **OS**: Ubuntu 24.04.4 LTS
- **Browser**: Brave Browser 149.1.91.178 
- **URL**: `http://localhost:5173`, `http://localhost:3000`
- **Build/Commit**: Latest

## Steps to reproduce

1. Đăng nhập bằng user hợp lệ.
2. Mở trang Hồ sơ.
3. Nhập address rỗng, address 4 ký tự, address 256 ký tự hoặc address chỉ gồm khoảng trắng.
4. Bấm Cập nhật.

## Expected result

- Hệ thống từ chối submit và hiển thị lỗi address tương ứng.
- Địa chỉ giao hàng cũ không bị thay đổi.

## Actual result

- Hệ thống cập nhật thành công với address không hợp lệ.
- Với address chỉ gồm khoảng trắng, địa chỉ mới gồm các khoảng trắng được hiển thị trên hồ sơ người dùng.

## Evidence
- Địa chỉ rỗng
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/4f120a0f-bc80-419a-a8d4-12193074ed68" />
- Địa chỉ 4 kí tự
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/1d456981-1953-4d4c-947d-d20ec6be16c5" />
- Địa chỉ 256 kí tự
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/de97b751-2e9e-4fb5-8759-38edee5c9b81" />
- Địa chỉ chỉ toàn khoảng trắng
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/007e3e3b-3df1-46cf-bce1-fde1750c621c" />
