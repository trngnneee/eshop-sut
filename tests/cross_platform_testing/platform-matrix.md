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

## 3. Platform đã cân nhắc rồi loại

| # | Phương án | Trạng thái | Lý do loại |
|---|---|---|---|
| P4 | iPhone 14 (Playwright device emulation) | **Đã xoá khỏi code** | Emulation chỉ đổi viewport + UA + touch flag, engine vẫn là WebKit trên macOS — không phải thiết bị thật, nên không thoả §6 của đề ("real physical devices"). Ghi nhận là platform sẽ làm loãng bộ bằng chứng: 5 platform nhưng chỉ 3 môi trường thật |
| P5 | Pixel 7 (Playwright device emulation) | **Đã xoá khỏi code** | Như trên. Thêm một điểm nữa: emulation Pixel vẫn chạy WebKit trên máy này, tức *không* đo được Blink-on-Android — đúng thứ mà tên "Pixel 7" gợi ý, nên để lại còn dễ gây hiểu sai hơn là bỏ |
| — | BrowserStack / LambdaTest | Không dùng | Không còn trial hiệu lực tại thời điểm làm bài (xem §4.1) |
| — | `Safari.app` thật qua `safaridriver` | Không dùng lần này | Cần đổi driver, không chỉ đổi cấu hình — xem §5 |

Xoá thật, không phải ẩn: `harness/lib/platforms.js` hiện export đúng 3 entry, nên `--platforms all` cũng chỉ trả về P1–P3.

## 4. Khai báo trung thực

1. **Không dùng BrowserStack / LambdaTest.** Không có trial còn hiệu lực tại thời điểm làm bài. Đề cho phép phương án thay thế: *"or use real physical devices, provided your screenshots clearly show the browser / OS / device name alongside the SUT's localhost URL"*. Phương án đã dùng là **browser thật chạy trên máy thật (không cloud, không ảo hoá)**, và mọi ảnh đều mang overlay browser/engine/version + OS + device + URL `localhost:5173` + email sinh viên.
2. **P1 là "Google Chrome for Testing"** — cùng engine Blink, cùng dòng phiên bản Chrome, do Playwright quản lý. Không phải Chrome bản tải từ google.com (máy không cài Chrome).
3. **P3 là WebKit build của Playwright**, không phải `Safari.app`. Cùng engine WebKit (`AppleWebKit/605.1.15`, `Version/26.5`) — tức cùng lớp render/JS/CSS với Safari — nhưng vỏ ứng dụng là `Playwright.app`, nên trong ảnh cửa sổ thật, menu bar macOS hiện tên "Playwright" chứ không phải "Safari".
4. **P2 dùng Firefox build của Playwright**, bundle tên `Nightly.app`; `browser.version()` trả `153.0` và UA là `Firefox/153.0`.
5. **Không có platform mobile trong bộ bằng chứng.** Hai profile emulation P4/P5 đã bị **xoá khỏi code**, không phải chỉ loại khỏi deliverable (xem §3): emulation không phải máy thật nên không thoả §6. Bộ kết quả chính thức chỉ gồm P1–P3.
6. **Locale engine không bị ép.** Harness *không* set `locale` cho browser context, để lộ đúng hành vi mặc định của từng engine — và đây chính là nguồn của phát hiện lớn nhất trong `divergences.md` (`Intl`/`toLocaleString()` resolve locale khác nhau: `vi` trên Chromium, `en-US` trên Firefox, `vi-VN` trên WebKit).
7. **Ảnh không dàn dựng.** Ảnh viewport do `page.screenshot()` chụp trong chính lần chạy audit; ảnh cửa sổ do `screencapture` của macOS chụp cửa sổ browser thật. Overlay được stamp vào DOM của trang *trước khi* chụp (chú thích bằng chứng), không hề sửa file ảnh sau khi chụp.

## 5. Cách đóng khoảng cách về sau (chưa làm trong lần nộp này)

Hai khoảng cách đã khai ở §4 đều đóng được, và đây là các bước cụ thể — ghi ra để §4.3 và §4.5 không chỉ là lời xin lỗi:

**a) Safari thật thay cho WebKit build.** Không phải đổi cấu hình mà là đổi driver: Playwright **không** attach được vào `Safari.app` (`webkit` của nó là build riêng). Muốn dùng Safari thật:

1. `sudo safaridriver --enable` (một lần cho mỗi máy).
2. Trong Safari: menu **Develop → Allow Remote Automation**.
3. Điều khiển bằng WebDriver — Selenium hoặc WebdriverIO với capability `browserName: 'safari'` — chứ không phải Playwright.
4. Hệ quả phải chấp nhận: viết lại lớp `ctx` của harness theo API WebDriver, và mất `page.route()` — tức 4 check đang giả lỗi API (`GUI-IA04-09`, `IA04-16`, `IA01-08`, và nhánh 500 của `IA04-12`) phải đổi cách dựng lỗi, ví dụ tắt backend hoặc chèn proxy.

Đánh giá: engine của P3 vốn **đã là** WebKit `605.1.15 / Version 26.5` — cùng lớp render/JS/CSS với Safari — nên việc đổi sang Safari thật thay đổi *vỏ ứng dụng và chứng cứ ảnh*, gần như không thay đổi kết quả 66 item. Vì vậy đây là việc đáng làm để chặt chẽ về hình thức, không phải để sửa số liệu.

**b) Platform thứ tư là thiết bị thật (Expo Go).** Đề cho phép Expo Go tính là một trong ba platform bắt buộc:

1. `cd frontend-mobile && npx expo start` trên máy chủ.
2. Điện thoại thật cài Expo Go, **cùng mạng LAN**, quét QR.
3. Đổi base URL của API từ `localhost:3000` sang **IP LAN của máy chủ** — đây là chỗ luôn quên, vì `localhost` trên điện thoại trỏ về chính điện thoại.
4. Chụp ảnh bằng chính điện thoại (screenshot hệ điều hành), overlay vẫn stamp được MSSV + họ tên + email qua `lib/overlay.js` vì nó chèn vào DOM.

Đánh giá: đây là cách duy nhất còn lại để bộ bằng chứng có **hai OS khác nhau**. Hiện cả P1–P3 đều là macOS 15.5 trên cùng một máy — đúng luật (đề chỉ đòi Chrome/Firefox/Safari trên web frontend) nhưng là điểm yếu thật của chữ "cross-platform", và nói thẳng ra ở đây đúng hơn là để người đọc tự phát hiện.
