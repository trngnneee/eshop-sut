## BUG-FR18-X-01 - Admin UI không hiển thị địa chỉ giao hàng

**GitHub issue title:** `[BUG][FR-18][Admin Order Management] Admin UI không hiển thị địa chỉ giao hàng`

**GitHub issue:** [#63](https://github.com/trngnneee/eshop-sut/issues/63)

**Labels:** `type: bug`, `status: new`, `found-by: test-case`

## Found by Test Case

- `FR18-X-TC01`
- `FR18-X-TC02`
- `FR18-X-TC03`
- Paths:
  - `eshop-sut/tests/test-cases/admin_order_management/FR18-X-TC01.md`
  - `eshop-sut/tests/test-cases/admin_order_management/FR18-X-TC02.md`
  - `eshop-sut/tests/test-cases/admin_order_management/FR18-X-TC03.md`

## Requirement liên quan

- `FR-18`
- Địa chỉ giao hàng phải được hiển thị an toàn, không render HTML.
- `SEC-04`: Mọi dữ liệu từ user nhập vào khi hiển thị trên UI phải được escape đúng cách, không dùng `innerHTML` trực tiếp.
- Source: `eshop-sut/README.md`

## Severity / Priority

Major / P2

## Environment

- **OS**: Ubuntu 24.04.4 LTS
- **Browser**: Brave Browser 149.1.91.178
- **URL**: `http://localhost:5174`
- **Build/Commit**: Latest

## Steps to reproduce

1. Đăng nhập bằng tài khoản `admin` hợp lệ.
2. Tạo hoặc seed các đơn hàng có `shipping_address` lần lượt là `<script>alert("xss")</script>12 Le Loi`, `<img src=x onerror=alert("xss")>34 Nguyen Hue`, và `12 Le Loi, Quan 1, TP.HCM`.
3. Mở tab Quản lý Đơn hàng trong Admin UI.
4. Quan sát ô Địa chỉ của các đơn hàng.

## Expected result

- Admin UI hiển thị đúng địa chỉ giao hàng.
- Với dữ liệu chứa HTML/script, địa chỉ được hiển thị như text đã escape.
- Browser không thực thi script/event handler và không tạo node HTML từ `shipping_address`.

## Actual result

- Địa chỉ giao hàng không được hiển thị.

## Evidence
- Mặc dù địa chỉ đã được cập nhật từ profile, nó vẫn chưa được cập nhật trên đơn hàng
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/e3d23196-7aa0-4f7b-8eca-2d7fab3212e9" />

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/fed3acb9-0645-4d64-857e-284fbd2c14f2" />
