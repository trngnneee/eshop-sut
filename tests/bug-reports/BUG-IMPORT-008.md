Title: [BUG][Import][Backend] Cho phép import tên sản phẩm vượt quá độ dài tối đa (255 ký tự)

## Found by Test Case
[TC-IMPORT-015](../test-cases/import/TC-IMPORT-015.md)

## Requirement liên quan
FR-16: Import Sản phẩm từ CSV (Tên sản phẩm không vượt quá 255 ký tự)

## Severity / Priority
Medium / P2

## Environment
Backend API & CSDL SQLite

## Steps to reproduce
1. Admin đăng nhập hệ thống và lấy JWT token.
2. Gửi API POST đến `/api/admin/import-products` với sản phẩm có tên dài 256 ký tự:
   ```json
   {
     "products": [
       {"name": "A" * 256, "price": 100000, "description": "Mô tả", "imageUrl": "", "category_id": 1}
     ]
   }
   ```

## Expected result
- Hệ thống từ chối import, trả về HTTP 400 Bad Request và báo lỗi tên sản phẩm vượt quá 255 ký tự.

## Actual result
- Hệ thống trả về HTTP 200 OK và lưu thành công sản phẩm có tên dài 256 ký tự vào CSDL.

## Evidence
![Ảnh chụp minh chứng](../bugs-screenshots/BUG-IMPORT-008.png)
---
*Nhãn (Labels) cần gắn:* `type: bug, module: backend, severity: medium, priority: P2, status: new, found-by: test-case`
