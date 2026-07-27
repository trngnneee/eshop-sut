# System Analysis & Survey Report (Khảo sát Hệ thống EShop)

**Student ID**: `23127207`  
**Target Application**: EShop SUT (System Under Test)  
**Feature**: Authentication - Login (`TC-LOGIN-001`)  
**Date**: 2026-07-27

---

## 1. Môi trường & Khởi động Hệ thống (SUT Startup Procedure)

Hệ thống EShop bao gồm 2 thành phần chính cần vận hành song song:

### 1.1 Backend Service (Node.js + Express + SQLite)
- **Thư mục**: `backend/`
- **Lệnh khởi động**: `cd backend && node server.js`
- **Địa chỉ/Port**: `http://localhost:3000`
- **Database**: SQLite (`backend/database.sqlite`), được khởi tạo và seed dữ liệu sẵn từ `backend/database.js`.

### 1.2 Frontend Web Client (React + Vite + TailwindCSS)
- **Thư mục**: `frontend-web/`
- **Lệnh khởi động**: `cd frontend-web && npm run dev`
- **Địa chỉ/Port**: `http://localhost:5173`
- **Cấu hình API**: Gọi API backend tại `http://localhost:3000/api/login`.

---

## 2. Thông tin Tài khoản Hợp lệ trong Hệ thống

Từ việc khảo sát file seed `backend/database.js`, các tài khoản người dùng đã được khởi tạo sẵn trong cơ sở dữ liệu:

| Role | Email | Password | Full Name |
| :--- | :--- | :--- | :--- |
| **user** | `test@eshop.com` | `Test1234!` | Test User |
| **admin** | `admin@eshop.com` | `Admin123!` | Admin User |

-> **Tài khoản sử dụng cho test case `TC-LOGIN-001`**: `test@eshop.com` / `Test1234!`.

---

## 3. Khảo sát Giao diện & Selector Trang Đăng nhập (`http://localhost:5173/login`)

Khảo sát trực tiếp file mã nguồn `frontend-web/src/pages/Login.jsx`:

1. **URL Trang Đăng nhập**: `http://localhost:5173/login`
2. **Trường Email (Username)**:
   - Cấu trúc HTML: `<label className="...">Username</label><input type="text" value={email} ... />`
   - Nhận xét: Thẻ `<label>` không chứa thuộc tính `htmlFor` và không bọc ngoài `<input>`. Do đó, `getByLabel('Username')` tiêu chuẩn không bắt trực tiếp được.
   - Locator tối ưu: `page.locator('div').filter({ hasText: /^Username$/ }).locator('input')`
3. **Trường Mật khẩu (Password)**:
   - Cấu trúc HTML: `<label className="...">Mật khẩu</label><input type="text" value={password} ... />`
   - Locator tối ưu: `page.locator('div').filter({ hasText: /^Mật khẩu$/ }).locator('input')`
4. **Nút Đăng nhập**:
   - Cấu trúc HTML: `<button type="submit" className="...">Sign In</button>`
   - Locator tối ưu: `page.getByRole('button', { name: 'Sign In' })`

---

## 4. Hành vi Thực tế Sau khi Đăng nhập Thành công

Khi người dùng nhập đúng thông tin (`test@eshop.com` / `Test1234!`) và nhấn nút **Sign In**:
1. Frontend thực hiện API POST request `/api/login` nhận `token` và thông tin `user`.
2. Trạng thái AuthContext chuyển sang đăng nhập, token được lưu vào `localStorage`.
3. Trang chuyển hướng tự động sang Trang chủ (`navigate('/')`).
4. Thanh Header thay đổi:
   - URL chuyển thành `http://localhost:5173/`.
   - Hiển thị nút **Thoát** (`<button>Thoát</button>`).
   - Hiển thị liên kết Profile cá nhân với văn bản `"Chào, Test User"`.

---

## 5. Xác nhận Oracle & Assertion Patterns

Dựa trên hành vi thực tế, 3 Pattern Assertion độc lập và có ý nghĩa được lựa chọn:

1. **Pattern 1 (`toHaveURL`)**: Xác minh chuyển hướng tới trang chủ (`http://localhost:5173/`).
2. **Pattern 2 (`toBeVisible`)**: Xác minh sự hiện diện của nút nút đăng xuất `"Thoát"`.
3. **Pattern 3 (`toContainText`)**: Xác minh tên hiển thị người dùng trên Header chứa `"Test User"`.
