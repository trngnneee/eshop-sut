# FR-04 - Quản lý hồ sơ cá nhân

## Nguồn yêu cầu

README.md, dòng 62-68:

- Người dùng đã đăng nhập có thể cập nhật: Họ Tên, Số điện thoại, Địa chỉ giao hàng mặc định.
- Số điện thoại hợp lệ: bắt đầu bằng số `0`, từ 10-11 chữ số.
- Email không được phép thay đổi qua giao diện.
- Người dùng chỉ có thể cập nhật hồ sơ của chính mình; không thể tự thay đổi thuộc tính `role`.

## Assumptions

| ID | Assumption | Lý do |
| :--- | :--- | :--- |
| A1 | `name` bắt buộc, độ dài hợp lệ 1-50 ký tự. | README.md FR-04 không quy định min/max cho `name`; cần assumption để áp dụng BVA. |
| A2 | `shipping_address` bắt buộc, độ dài hợp lệ 5-255 ký tự sau khi trim. | README.md FR-04 không quy định min/max cho address; cần assumption để áp dụng BVA. |
| A3 | `phone` khi cập nhật phải không rỗng, bắt đầu bằng `0` và chỉ gồm 10-11 chữ số. | README.md FR-04 có rule cụ thể cho số điện thoại hợp lệ. |

## Input / Output Variables

| Variable | Loại | Ghi chú |
| :--- | :--- | :--- |
| `name` | User input | Họ tên trong hồ sơ cá nhân. |
| `phone` | User input | Số điện thoại hợp lệ phải bắt đầu bằng `0`, dài 10-11 chữ số. |
| `shipping_address` | User input | Địa chỉ giao hàng mặc định. |
| `email` | System/display field | Chỉ hiển thị, không được chỉnh sửa qua giao diện. |
| `role` | Protected system field | Client không được tự thay đổi. |
| JWT / current user | System state | Chỉ user đã đăng nhập được cập nhật hồ sơ của chính mình. |

## Equivalence Partitions

| Class ID | Domain Class | Representative Values | Expected Status | Reason |
| :--- | :--- | :--- | :--- | :--- |
| N-VALID | `name` hợp lệ | `Nguyen Van A` | Accepted | Tên nằm trong assumption 1-50 ký tự. |
| N-EMPTY | `name` rỗng | `[Để trống]` | Rejected | `name` là trường định danh hồ sơ theo assumption A1. |
| P-VALID-10 | `phone` hợp lệ 10 chữ số | `0123456789` | Accepted | Bắt đầu bằng `0`, đủ 10 chữ số. |
| P-VALID-11 | `phone` hợp lệ 11 chữ số | `01234567890` | Accepted | Bắt đầu bằng `0`, đủ 11 chữ số. |
| P-NO-LEADING-0 | `phone` không bắt đầu bằng `0` | `9123456789` | Rejected | Vi phạm rule phone trong README.md. |
| P-NON-DIGIT | `phone` chứa ký tự không phải số | `01234abcde` | Rejected | Vi phạm rule chỉ gồm chữ số. |
| A-VALID | Address hợp lệ | `123 Nguyen Hue, Quan 1, TP.HCM` | Accepted | Địa chỉ nằm trong assumption 5-255 ký tự. |
| A-EMPTY | Address rỗng hoặc chỉ khoảng trắng | `[Để trống]`, `     ` | Rejected | Không có địa chỉ giao hàng mặc định hợp lệ theo assumption A2. |
| E-READONLY | Email qua giao diện | `changed@eshop.com` | Rejected/unchanged | README.md yêu cầu email không đổi qua UI. |
| R-PROTECTED | Client gửi `role=admin` | `{ "role": "admin" }` | Rejected/unchanged | User không thể tự đổi `role`. |
| U-NO-AUTH | Không có JWT | `[Không gửi Authorization]` | Rejected | FR-04 chỉ cho user đã đăng nhập. |
| U-OTHER-USER | Cố cập nhật hồ sơ user khác | `{ "id": "{user_b_id}" }` | Rejected/unchanged | User chỉ được cập nhật hồ sơ của chính mình. |

## Boundary Values

| Field | Boundary Type | Value | Expected Status | Test Case |
| :--- | :--- | :--- | :--- | :--- |
| `name` | Min-1 | 0 ký tự | Rejected | FR04-N-BVA-TC01 |
| `name` | Min | 1 ký tự | Accepted | FR04-N-BVA-TC02 |
| `name` | Min+1 | 2 ký tự | Accepted | FR04-N-BVA-TC03 |
| `name` | Nominal | 25 ký tự | Accepted | FR04-N-BVA-TC04 |
| `name` | Max-1 | 49 ký tự | Accepted | FR04-N-BVA-TC05 |
| `name` | Max | 50 ký tự | Accepted | FR04-N-BVA-TC06 |
| `name` | Max+1 | 51 ký tự | Rejected | FR04-N-BVA-TC07 |
| `phone` | Min-1 | 9 chữ số | Rejected | FR04-P-BVA-TC01 |
| `phone` | Min | 10 chữ số | Accepted | FR04-P-BVA-TC02 |
| `phone` | Max | 11 chữ số | Accepted | FR04-P-BVA-TC03 |
| `phone` | Max+1 | 12 chữ số | Rejected | FR04-P-BVA-TC04 |
| `shipping_address` | Min-1 | 4 ký tự | Rejected | FR04-A-BVA-TC01 |
| `shipping_address` | Min | 5 ký tự | Accepted | FR04-A-BVA-TC02 |
| `shipping_address` | Min+1 | 6 ký tự | Accepted | FR04-A-BVA-TC03 |
| `shipping_address` | Nominal | 130 ký tự | Accepted | FR04-A-BVA-TC04 |
| `shipping_address` | Max-1 | 254 ký tự | Accepted | FR04-A-BVA-TC05 |
| `shipping_address` | Max | 255 ký tự | Accepted | FR04-A-BVA-TC06 |
| `shipping_address` | Max+1 | 256 ký tự | Rejected | FR04-A-BVA-TC07 |

## Generated Artifacts

| Artifact | Path |
| :--- | :--- |
| JSON config | `tests/test-configs/fr04-config.json` |
| Test cases | `tests/test-cases/profile_management/` |
| Test run template | `tests/test-runs/fr04-profile-management-test-run.md` |
| Traceability matrix | `tests/test-summary/traceability-matrix.md` |

## Count Summary

| Nhóm kiểm thử | Domain TC | BVA TC | Tổng TC |
| :--- | ---: | ---: | ---: |
| Name Input | 2 | 7 | 9 |
| Phone Input | 5 | 4 | 9 |
| Address Input | 3 | 7 | 10 |
| Email Immutability | 1 | 0 | 1 |
| Role Protection | 1 | 0 | 1 |
| User Ownership/Auth | 2 | 0 | 2 |
| **Tổng** | **14** | **18** | **32** |
