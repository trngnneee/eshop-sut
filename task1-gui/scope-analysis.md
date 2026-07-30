# Scope Analysis — Task 1: GUI Checklist (EShop)

**Tester:** Đặng Đăng Khoa  
**Student ID:** 23127207  
**Course:** Software Testing — HW03  
**SUT:** EShop (https://github.com/ttbhanh/eshop-sut)  

---

## 1. Scope Boundaries (Phạm vi kiểm thử của Đặng Đăng Khoa)

This scope strictly covers 5 screens/modules across Web Frontend, Web Admin, and Mobile App:

| # | Platform | Module / Screen | Related Requirements | Key UI Components & Route |
|---|---|---|---|---|
| 1 | Web Frontend | Web Login | FR-02: Login & account lockout | Route `/login`. Title `<h2>`, Email `<input>`, Password `<input>`, Submit `<button>`, Forgot password link `<a href="/forgot-password">`, Link to Register. |
| 2 | Web Frontend | Web Register | FR-01: Account registration | Route `/register`. Title `<h2>`, Full Name `<input>`, Email `<input>`, Password `<input>`, Password policy hint `<p>`, Submit `<button>`, Link to Login. |
| 3 | Web Admin | Admin Login | FR-12: Access control (Admin auth) | Route `/` (Unauthenticated state `!token`). Title `<h2>Admin Login</h2>`, Email `<input>`, Password `<input>`, Submit `<button>`. |
| 4 | Web Admin | Admin Category Management | FR-14: Category management CRUD | Route `/` (Tab `categories`). Heading `<h2>`, Add category form (`<input>`, `<button>`), Category data table (`<table>`, `<th>`, `<tr>`, `<td>`, Delete `<button>`). |
| 5 | Mobile App | Mobile Login | FR-02: Mobile authentication | Expo / React Native App login view (`view === "login"`). Brand header, Email `<TextInput>`, Password `<TextInput>`, Sign In button, Forgot password touchable, Register touchable, Back touchable, Error banner. |

*Note: Out-of-scope modules (Product, Cart, Checkout, Dashboard, Coupon, Order Management) are excluded except where navigation links boundary exists.*

---

## 2. Platform Architecture & Server Configuration

### 2.1 Backend Server
- **Tech Stack:** Node.js, Express, SQLite (`sqlite3`)
- **Port / Base URL:** `http://localhost:3000`
- **Database Seed Script:** `node database.js` (Resets and seeds default accounts & initial categories)

### 2.2 Frontend Web
- **Tech Stack:** React 19, Vite, TailwindCSS, React Router DOM v7
- **Port / URL:** `http://localhost:5173/`
- **Main Routes:**
  - `/login`: `Login.jsx`
  - `/register`: `Register.jsx`

### 2.3 Frontend Admin
- **Tech Stack:** React 19, Vite, TailwindCSS, Axios
- **Port / URL:** `http://localhost:5174/`
- **Main Tab:** `categories` in `App.jsx`

### 2.4 Frontend Mobile
- **Tech Stack:** React Native, Expo SDK
- **Execution Target:** Metro Bundler / Expo Go / Android Emulator
- **API LAN URL:** `http://192.168.10.13:3000/api` or `http://localhost:3000/api`

---

## 3. Predefined Test Accounts & Data

- **Admin Account (Default):**
  - Email: `admin@eshop.com`
  - Password: `Admin123!` (or `admin123` depending on backend/frontend payload)
- **Standard User Account (Default):**
  - Email: `test@eshop.com`
  - Password: `Test1234!`
- **Khoa's Student Specific Test Data Pattern:**
  - `23127207_gui_<n>@hcmus.edu.vn` (e.g., `23127207_gui_01@hcmus.edu.vn`)
  - Dynamic registration & lockout test accounts to prevent corrupting default test accounts.

---

## 4. Discovered System Limitations & Initial Blockers

1. **Web Login Title Defect:** Heading displays `<h2>Đăng Ký</h2>` instead of `<h2>Đăng Nhập</h2>`.
2. **Password Input Masking Defect:** Web Login password field uses `type="text"` instead of `type="password"`.
3. **Password Validation Regex Defect in Register:** Client-side regex requires whitespace (`\s`) instead of special characters, contradicting the displayed helper hint text.
4. **Missing Category Edit Functionality in Admin:** Admin UI contains no edit category button or modal, rendering Category Update impossible via GUI.
5. **No Confirmation Modal on Delete Category:** Category deletion triggers immediately upon clicking "Xóa" without user confirmation.
6. **Mobile Environment:** Expo Go / Emulator requires local IP alignment or mock runner for automated visual verification.
