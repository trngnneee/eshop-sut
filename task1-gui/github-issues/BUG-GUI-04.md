# [BUG-GUI-04] Admin Category CRUD Missing Features & Missing Delete Confirmation

**Platform:** Web Admin  
**Screen/Route:** / (Tab categories)  
**Related Requirement:** FR-14 (Category Management CRUD)  
**Severity:** High | **Priority:** High  
**Status:** PENDING_EXTERNAL_ACTION  

## Description & Steps to Reproduce
1. Đăng nhập Admin và chuyển sang tab 'Danh mục'.
2. Tìm nút 'Sửa' (Edit) trên từng dòng danh mục.
3. Nhấn nút 'Xóa' trên một danh mục.
4. Để trống ô tên danh mục mới và nhấn 'Thêm mới'.

## Expected Result
- Có nút 'Sửa' để chỉnh sửa tên danh mục.
- Nhấn 'Xóa' hiển thị modal xác nhận 'Bạn có chắc chắn muốn xóa?'.
- Tên danh mục rỗng bị chặn ngay tại client-side.

## Actual Result
- Hoàn toàn KHÔNG CÓ nút Sửa hay modal chỉnh sửa danh mục nào trên UI.
- Nhấn nút 'Xóa' lập tức kích hoạt API delete mà KHÔNG hỏi xác nhận.
- Tên danh mục rỗng gửi API gây bật popup alert() từ backend.

## Evidence Screenshot
![Screenshot](../../evidence/admin-category/BUG-GUI-04_admin-category.png)
