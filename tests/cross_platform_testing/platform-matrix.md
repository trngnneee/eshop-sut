# Task 3 — Platform matrix & khai báo môi trường

## 1. Máy chủ chạy SUT và chạy test (cùng một máy)

| Thuộc tính | Giá trị (xác minh bằng `sw_vers`, `system_profiler`) |
|---|---|
| OS | macOS 15.5, build 24F74 |
| Device | MacBook Pro, Apple Silicon |
| Display | built-in 2560×1664 Retina (UI scale 2×) + màn ngoài 1920×1080 |
| SUT web | `http://localhost:5173` (Vite 8.0.12 dev server, `frontend-web`) |
| SUT API | `http://localhost:3000` (Express + SQLite, `backend/server.js`) |
| Node | v26.4.0 |
| Driver | Playwright 1.56 (browser build đã cài trong `~/Library/Caches/ms-playwright`) |
| Chế độ chạy | __headed__ (cửa sổ thật, không headless) |

## 2. Ba platform bắt buộc

| # | Platform key | Browser / engine | Version thật (`browser.version()`) | OS | Device / viewport | Vai trò theo đề |
|---|---|---|---|---|---|---|
| P1 | `P1-chromium-macos` | Google Chrome for Testing / **Blink** | 151.0.7922.34 | macOS 15.5 | MacBook Pro · 1280×800 @2x | "Chrome" |
| P2 | `P2-firefox-macos` | Firefox / **Gecko** | 153.0 | macOS 15.5 | MacBook Pro · 1280×800 @1x | "Firefox" |
| P3 | `P3-webkit-macos` | Playwright WebKit / **WebKit** | 26.5 (`Version/26.5 Safari/605.1.15`) | macOS 15.5 | MacBook Pro · 1280×800 @1x | "Safari" |

`results/`, `results-matrix.md` và `divergences.md` vì vậy chỉ chứa **3 platform P1–P3** (66 item × 3 = 198 lượt thực thi).

## 4. Khai báo trung thực

1. **Không dùng BrowserStack / LambdaTest.** Không có trial còn hiệu lực tại thời điểm làm bài. Đề cho phép phương án thay thế: *"or use real physical devices, provided your screenshots clearly show the browser / OS / device name alongside the SUT's localhost URL"*. Phương án đã dùng là **browser thật chạy trên máy thật (không cloud, không ảo hoá)**, và mọi ảnh đều mang overlay browser/engine/version + OS + device + URL `localhost:5173` + email sinh viên.
2. **P1 là "Google Chrome for Testing"** — cùng engine Blink, cùng dòng phiên bản Chrome, do Playwright quản lý. Không phải Chrome bản tải từ google.com (máy không cài Chrome).
3. **P3 là WebKit build của Playwright**, không phải `Safari.app`. Cùng engine WebKit (`AppleWebKit/605.1.15`, `Version/26.5`) — tức cùng lớp render/JS/CSS với Safari — nhưng vỏ ứng dụng là `Playwright.app`, nên trong ảnh cửa sổ thật, menu bar macOS hiện tên "Playwright" chứ không phải "Safari".
4. **P2 dùng Firefox build của Playwright**, bundle tên `Nightly.app`; `browser.version()` trả `153.0` và UA là `Firefox/153.0`.
5. **Không có platform mobile trong bộ bằng chứng.** Hai profile emulation P4/P5 đã bị loại khỏi deliverable (xem §3): emulation không phải máy thật nên không thoả §6. Bộ kết quả chính thức chỉ gồm P1–P3.
6. **Locale engine không bị ép.** Harness *không* set `locale` cho browser context, để lộ đúng hành vi mặc định của từng engine — và đây chính là nguồn của phát hiện lớn nhất trong `divergences.md` (`Intl`/`toLocaleString()` resolve locale khác nhau: `vi` trên Chromium, `en-US` trên Firefox, `vi-VN` trên WebKit).
7. **Ảnh không dàn dựng.** Ảnh viewport do `page.screenshot()` chụp trong chính lần chạy audit; ảnh cửa sổ do `screencapture` của macOS chụp cửa sổ browser thật. Overlay được stamp vào DOM của trang *trước khi* chụp (chú thích bằng chứng), không hề sửa file ảnh sau khi chụp.
