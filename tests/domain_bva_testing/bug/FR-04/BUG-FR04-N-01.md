## BUG-FR04-N-01 - Thiếu validate độ dài tối đa Họ Tên

**GitHub issue title:** `[BUG][FR-04][Profile Management] Thiếu validate độ dài tối đa Họ Tên`

**GitHub issue:** [#54](https://github.com/trngnneee/eshop-sut/issues/54)

**Labels:** `type: bug`, `status: new`, `found-by: test-case`

## Found by Test Case

- `FR04-N-BVA-TC07`
- Path: `eshop-sut/tests/test-cases/profile_management/FR04-N-BVA-TC07.md`

## Requirement liên quan

- `FR-04`
- Test assumption: `name` bắt buộc, độ dài hợp lệ 1-50 ký tự.
- Source: `eshop-sut/tests/test-summary/fr04-profile-management-summary.md`

## Severity / Priority

Minor / P2

## Environment

- **OS**: Ubuntu 24.04.4 LTS
- **Browser**: Brave Browser 149.1.91.178 
- **URL**: `http://localhost:5173`, `http://localhost:3000`
- **Build/Commit**: Latest

## Steps to reproduce

1. Đăng nhập bằng user hợp lệ.
2. Mở trang Hồ sơ.
3. Nhập Họ Tên dài 51 ký tự, các trường còn lại hợp lệ.
4. Bấm Cập nhật.

## Expected result

- Hệ thống từ chối submit và hiển thị lỗi độ dài Họ Tên vượt quá 50 ký tự theo assumption BVA.
- Giá trị Họ Tên cũ không bị thay đổi.

## Actual result

- Hệ thống chấp nhận giá trị và không báo lỗi độ dài ở trường Họ Tên.

## Evidence

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/a1394546-2de7-4e81-98b1-987c05fe30f7" />
