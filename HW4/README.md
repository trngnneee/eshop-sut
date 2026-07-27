# HW4 - Automation Testing with Playwright & TypeScript (EShop SUT)

**Student ID**: `23127207`  
**Course**: Software Testing  
**Project**: HW4 - Playwright Data-Driven Testing for Login Feature  

---

## 1. Mục tiêu Bài làm

Xây dựng bộ kịch bản tự động hóa (Automation Test) hoàn chỉnh bằng **Playwright** và **TypeScript** cho tính năng Đăng nhập (Login) của hệ thống EShop. Bài làm tuân thủ kiến trúc **Data-driven Testing**, thực thi độc lập trên **3 trình duyệt (Chromium, Firefox, WebKit)** và xuất ra 3 báo cáo HTML riêng biệt có gắn dấu xác thực **Student ID: 23127207**.

---

## 2. Thông tin Test Case

Trong toàn bộ bộ test suite chỉ duy nhất 01 Playwright test case được khai báo và thực thi:

- **Test Case ID**: `TC-LOGIN-001`
- **Mô tả**: `Login successfully with valid credentials`
- **Các bước thực hiện**:
  1. Truy cập trang đăng nhập (`http://localhost:5173/login`).
  2. Nhập Email hợp lệ (`test@eshop.com`).
  3. Nhập Password hợp lệ (`Test1234!`).
  4. Nhấn nút **Sign In**.
  5. Xác minh đăng nhập thành công bằng 3 Assertion Patterns độc lập.
- **3 Assertion Patterns được sử dụng**:
  - `toHaveURL()`: Kiểm tra URL chuyển hướng tới `http://localhost:5173/`.
  - `toBeVisible()`: Kiểm tra sự xuất hiện của nút đăng xuất `"Thoát"`.
  - `toContainText()`: Kiểm tra tên hiển thị người dùng trên Header chứa `"Test User"`.

---

## 3. Yêu cầu Môi trường

- **Node.js**: `v20.x` trở lên (Đã thử nghiệm thành công trên Node `v24.10.0`).
- **npm**: `v10.x` trở lên.
- **Hệ điều hành**: Windows / macOS / Linux.

---

## 4. Hướng dẫn Cài đặt & Khởi động Hệ thống SUT

### Bước 4.1: Cài đặt Dependency cho HW4
Mở terminal tại thư mục `HW4/` và chạy:
```bash
cd HW4
npm install
```

### Bước 4.2: Cài đặt Trình duyệt Playwright (Chromium, Firefox, WebKit)
```bash
npx playwright install
```

### Bước 4.3: Khởi động Hệ thống SUT (Backend & Frontend)

Để chạy được test case, hệ thống SUT phải được khởi động trước:

1. **Khởi động Backend Service**:
   ```bash
   cd backend
   node server.js
   ```
   *(Backend lắng nghe tại: `http://localhost:3000`)*

2. **Khởi động Frontend Web Client**:
   ```bash
   cd frontend-web
   npm run dev
   ```
   *(Frontend lắng nghe tại: `http://localhost:5173`)*

---

## 5. Hướng dẫn Chạy Automation Test

Tất cả các lệnh chạy test được thực hiện bên trong thư mục `HW4/`:

### Chạy trên trình duyệt Chromium:
```bash
npm run test:chromium
```

### Chạy trên trình duyệt Firefox:
```bash
npm run test:firefox
```

### Chạy trên trình duyệt WebKit (Safari engine):
```bash
npm run test:webkit
```

### Chạy toàn bộ trên cả 3 trình duyệt (Matrix execution):
```bash
npm run test:all
```

---

## 6. Xem Báo cáo HTML (HTML Reports)

Mỗi lần chạy trình duyệt sinh ra 01 báo cáo HTML riêng biệt tại các thư mục tương ứng:

- **Chromium Report**: `HW4/reports/chromium/`
- **Firefox Report**: `HW4/reports/firefox/`
- **WebKit Report**: `HW4/reports/webkit/`

### Cách mở xem từng báo cáo:
- **Chromium Report**:
  ```bash
  npx playwright show-report reports/chromium
  ```
- **Firefox Report**:
  ```bash
  npx playwright show-report reports/firefox
  ```
- **WebKit Report**:
  ```bash
  npx playwright show-report reports/webkit
  ```

*(Mỗi file `index.html` đều hiển thị công khai tiêu đề và banner banner xác nhận: `Run by: 23127207`)*.

---

## 7. Vị trí Artifacts khi Test Fail

Trong trường hợp test bị thất bại (failure):
- **Screenshot**: `HW4/test-results/.../test-failed-1.png`
- **Trace zip**: `HW4/test-results/.../trace.zip`
- **Video webm**: `HW4/test-results/.../video.webm`

Để xem Playwright Trace Viewer cho ca kiểm thử thất bại:
```bash
npx playwright show-trace HW4/test-results/<folder-name>/trace.zip
```

---

## 8. Cấu trúc Thư mục Bài làm HW4

```text
HW4/
├── docs/
│   ├── system-analysis.md    # Tài liệu khảo sát hệ thống, DOM và oracle assertion
│   ├── prompt-log.md         # Nhật ký từng bước thiết kế prompt AI
│   └── ai-review.md          # Đánh giá Senior QA về lỗi AI và giải pháp khắc phục
├── test-data/
│   └── login-data.json       # File JSON lưu dữ liệu test cho TC-LOGIN-001
├── tests/
│   └── login.spec.ts         # File mã nguồn duy nhất chứa Playwright test TC-LOGIN-001
├── reports/
│   ├── chromium/             # Report HTML riêng biệt cho Chromium (Run by: 23127207)
│   ├── firefox/              # Report HTML riêng biệt cho Firefox (Run by: 23127207)
│   └── webkit/               # Report HTML riêng biệt cho WebKit (Run by: 23127207)
├── scripts/
│   └── inject-student-id.js  # Script tiêm và verify Student ID 23127207 vào HTML report
├── test-results/             # Thư mục chứa screenshot/trace/video khi test fail
├── package.json              # Khai báo dependency và các lệnh npm run test:*
├── playwright.config.ts      # Cấu hình 3 trình duyệt, base URL và HTML reporter
├── tsconfig.json             # Cấu hình biên dịch TypeScript
└── README.md                 # Hướng dẫn chi tiết sử dụng và thực thi
```

---

## 9. Các Giới hạn & Blocker Còn Tồn tại

- **Cấu trúc DOM của SUT**: Trang `Login.jsx` của SUT thiếu thuộc tính `htmlFor` trong các thẻ `<label>`, khiến locator chuẩn `getByLabel` tiêu chuẩn không bắt được trực tiếp. Bài làm đã khắc phục ổn định bằng container text filter locator `page.locator('div').filter({ hasText: ... })`.
- **Cơ chế khóa tài khoản SUT**: Hệ thống SUT có tính năng khóa tài khoản tạm thời nếu đăng nhập sai 3 lần liên tiếp (ở các test case khác). Đối với `TC-LOGIN-001`, việc sử dụng đúng tài khoản hợp lệ `test@eshop.com` / `Test1234!` đảm bảo luồng chạy luôn thành công 100%.
