# Task 3 — Ma trận thực thi checklist trên nhiều platform

> Sinh tự động bởi `harness/scripts/build-matrix.js` từ `results/raw/*.json`. Không sửa tay.

## Platform đã chạy

| # | Platform | Engine + version | OS | Device / viewport | Locale engine | Thời điểm chạy |
|---|---|---|---|---|---|---|
| P1 | Chrome / Chromium — macOS | Blink (Chromium) 151.0.7922.34 | macOS 15.5 (24F74) | MacBook Pro (Apple Silicon) — 2560×1664 Retina · 1280×800 | vi | 2026-07-28 20:17:11 (+07) |
| P2 | Firefox — macOS | Gecko (Firefox) 153.0 | macOS 15.5 (24F74) | MacBook Pro (Apple Silicon) — 2560×1664 Retina · 1280×800 | en-US | 2026-07-28 20:23:37 (+07) |
| P3 | Safari / WebKit — macOS | WebKit (Safari) 26.5 | macOS 15.5 (24F74) | MacBook Pro (Apple Silicon) — 2560×1664 Retina · 1280×800 | vi-VN | 2026-07-28 20:30:13 (+07) |

> **Cột "Platform" là vai trò theo đề, không phải tên bundle đã chạy.** Ba engine đều là browser build do Playwright quản lý, chạy headed trên máy thật: P1 = *Google Chrome for Testing* (Blink, vai trò "Chrome") · P2 = Firefox bundle `Nightly.app` (Gecko, vai trò "Firefox") · P3 = **WebKit build của Playwright, KHÔNG phải `Safari.app`** (cùng engine `AppleWebKit/605.1.15` — `Version/26.5` — nên cùng lớp render/JS/CSS/validation với Safari, nhưng vỏ ứng dụng là `Playwright.app`, vì vậy menu bar macOS trong ảnh cửa sổ hiện "Playwright"). Khai báo đầy đủ: [platform-matrix.md](platform-matrix.md) §4.

## Tổng hợp theo platform

| Platform | Pass | Fail | Blocked | Error | Tổng |
|---|---|---|---|---|---|
| P1 — Chrome / Chromium — macOS | 7 | 59 | 0 | 0 | 66 |
| P2 — Firefox — macOS | 6 | 60 | 0 | 0 | 66 |
| P3 — Safari / WebKit — macOS | 6 | 60 | 0 | 0 | 66 |

## Tổng hợp theo Interface Aspect

| Aspect | P1 P/F/B | P2 P/F/B | P3 P/F/B |
|---|---|---|---|
| IA-01 | 1 / 16 / 0 | 1 / 16 / 0 | 1 / 16 / 0 |
| IA-02 | 3 / 12 / 0 | 2 / 13 / 0 | 2 / 13 / 0 |
| IA-03 | 3 / 12 / 0 | 3 / 12 / 0 | 3 / 12 / 0 |
| IA-04 | 0 / 19 / 0 | 0 / 19 / 0 | 0 / 19 / 0 |

## Ma trận chi tiết (66 item × platform)

| ID | Aspect | Task 1 (Chrome, thủ công) | P1 | P2 | P3 | Khác biệt giữa platform |
|---|---|---|---|---|---|---|
| [GUI-GAP-01](results/raw/) | IA-04 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-GAP-02](results/raw/) | IA-04 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-GAP-03](results/raw/) | IA-01 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-GAP-04](results/raw/) | IA-02 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA01-01](results/raw/) | IA-01 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA01-02](results/raw/) | IA-01 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA01-03](results/raw/) | IA-01 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA01-04](results/raw/) | IA-01 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA01-05](results/raw/) | IA-01 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA01-06](results/raw/) | IA-01 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA01-07](results/raw/) | IA-01 | Passed | ✅ Pass | ✅ Pass | ✅ Pass | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA01-08](results/raw/) | IA-01 | Passed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA01-09](results/raw/) | IA-01 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA01-10](results/raw/) | IA-01 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA01-11](results/raw/) | IA-01 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA01-12](results/raw/) | IA-01 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA01-13](results/raw/) | IA-01 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA01-14](results/raw/) | IA-01 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA01-15](results/raw/) | IA-01 | Passed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA01-16](results/raw/) | IA-01 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA02-01](results/raw/) | IA-02 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA02-02](results/raw/) | IA-02 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA02-03](results/raw/) | IA-02 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA02-04](results/raw/) | IA-02 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA02-05](results/raw/) | IA-02 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA02-06](results/raw/) | IA-02 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA02-07](results/raw/) | IA-02 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA02-08](results/raw/) | IA-02 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA02-09](results/raw/) | IA-02 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA02-10](results/raw/) | IA-02 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA02-11](results/raw/) | IA-02 | Passed | ✅ Pass | ✅ Pass | ✅ Pass | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA02-12](results/raw/) | IA-02 | Passed | ✅ Pass | ✅ Pass | ✅ Pass | — |
| [GUI-IA02-13](results/raw/) | IA-02 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA02-14](results/raw/) | IA-02 | Failed | ✅ Pass | ❌ Fail | ❌ Fail | 🔴 kết quả khác nhau |
| [GUI-IA03-01](results/raw/) | IA-03 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA03-02](results/raw/) | IA-03 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA03-03](results/raw/) | IA-03 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA03-04](results/raw/) | IA-03 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA03-05](results/raw/) | IA-03 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA03-06](results/raw/) | IA-03 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA03-07](results/raw/) | IA-03 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA03-08](results/raw/) | IA-03 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA03-09](results/raw/) | IA-03 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA03-10](results/raw/) | IA-03 | Passed | ✅ Pass | ✅ Pass | ✅ Pass | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA03-11](results/raw/) | IA-03 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA03-12](results/raw/) | IA-03 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA03-13](results/raw/) | IA-03 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA03-14](results/raw/) | IA-03 | Passed | ✅ Pass | ✅ Pass | ✅ Pass | — |
| [GUI-IA03-15](results/raw/) | IA-03 | Passed | ✅ Pass | ✅ Pass | ✅ Pass | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA04-01](results/raw/) | IA-04 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA04-02](results/raw/) | IA-04 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA04-03](results/raw/) | IA-04 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA04-04](results/raw/) | IA-04 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA04-05](results/raw/) | IA-04 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA04-06](results/raw/) | IA-04 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA04-07](results/raw/) | IA-04 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA04-08](results/raw/) | IA-04 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA04-09](results/raw/) | IA-04 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA04-10](results/raw/) | IA-04 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA04-11](results/raw/) | IA-04 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA04-12](results/raw/) | IA-04 | Passed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA04-13](results/raw/) | IA-04 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA04-14](results/raw/) | IA-04 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |
| [GUI-IA04-15](results/raw/) | IA-04 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA04-16](results/raw/) | IA-04 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | 🟡 giá trị hiển thị khác nhau |
| [GUI-IA04-17](results/raw/) | IA-04 | Failed | ❌ Fail | ❌ Fail | ❌ Fail | — |

**Item có kết quả khác nhau giữa các platform: 1** · **item cùng kết quả nhưng giá trị hiển thị khác nhau: 28** · xem [divergences.md](divergences.md).

## Đối chiếu với Task 1

| ID | Task 1 | P1 | P2 | P3 | Ghi chú |
|---|---|---|---|---|---|
| GUI-IA01-08 | Passed | ❌ Fail | ❌ Fail | ❌ Fail | Giá luôn render là số có định dạng kể cả khi backend trả price sai kiểu (không bao giờ "Na |
| GUI-IA01-15 | Passed | ❌ Fail | ❌ Fail | ❌ Fail | Grid sản phẩm 1/2/3 cột theo breakpoint, không horizontal scroll ở 375/768/1280px |
| GUI-IA02-14 | Failed | ✅ Pass | ❌ Fail | ❌ Fail | Thông báo "bắt buộc nhập" nhất quán tiếng Việt (hiện dùng tooltip native) |
| GUI-IA04-12 | Passed | ❌ Fail | ❌ Fail | ❌ Fail | Feedback coupon đủ 2 nhánh (hợp lệ → message + tiết kiệm + thành tiền; sai → lỗi đỏ) và số |

Tổng số item mà kết quả tự động khác kết luận Task 1 trên ít nhất 1 platform: **4**.

