# Test Cases — EShop GUI Checklist (Task 1)

Mỗi file = 1 checklist item từ `../checklist-final.md`, bung thành test case chi tiết theo template chuẩn.

## Kết quả thực thi

- **Người thực thi:** Đặng Trường Nguyên (kiểm thử thủ công trực tiếp trên trình duyệt)
- **Ngày thực thi:** 2026-07-25
- **Môi trường:** Frontend Web `localhost:5173` + Backend `localhost:3000`
- **Screenshot mỗi test Failed:** `screenshots/<ID>.png`

| Aspect | Passed | Failed | Tổng |
|---|---|---|---|
| IA-01 | 3 | 14 | 17 |
| IA-02 | 2 | 13 | 15 |
| IA-03 | 3 | 12 | 15 |
| IA-04 | 1 | 18 | 19 |
| **Tổng** | **9** | **57** | **66** |

Chi tiết Pass/Fail + mô tả quan sát nằm ở mục "Actual result" của từng file.

| # | Test Case | Aspect | Traced to | Screen(s) | Kết quả |
|---|---|---|---|---|---|
| 1 | [GUI-IA01-01](IA-01/GUI-IA01-01.md) | IA-01 | FR-21 (nhất quán ngôn ngữ) | Đăng nhập | ❌ Failed |
| 2 | [GUI-IA01-02](IA-01/GUI-IA01-02.md) | IA-01 | FR-21 (nhất quán ngôn ngữ) | Tất cả 8 màn hình | ❌ Failed |
| 3 | [GUI-IA01-03](IA-01/GUI-IA01-03.md) | IA-01 | FR-21 (nhất quán màu sắc) | Đăng ký | ❌ Failed |
| 4 | [GUI-IA01-04](IA-01/GUI-IA01-04.md) | IA-01 | FR-21 (nhất quán màu sắc) | Chi tiết SP, Giỏ hàng, Thanh toán, Quên MK | ❌ Failed |
| 5 | [GUI-IA01-05](IA-01/GUI-IA01-05.md) | IA-01 | Heuristic (visual hierarchy) | Quên mật khẩu | ❌ Failed |
| 6 | [GUI-IA01-06](IA-01/GUI-IA01-06.md) | IA-01 | FR-21 (nhất quán đơn vị tiền) | Trang chủ | ❌ Failed |
| 7 | [GUI-IA01-07](IA-01/GUI-IA01-07.md) | IA-01 | FR-21 (định dạng tiền) + heuristic | Trang chủ, Chi tiết SP, Giỏ hàng, Thanh toán, Lịch sử ĐH | ✅ Passed |
| 8 | [GUI-IA01-08](IA-01/GUI-IA01-08.md) | IA-01 | FR-21 (định dạng tiền) + heuristic | Chi tiết SP | ✅ Passed |
| 9 | [GUI-IA01-09](IA-01/GUI-IA01-09.md) | IA-01 | FR-21 (tiêu đề trang) | Trang chủ | ❌ Failed |
| 10 | [GUI-IA01-10](IA-01/GUI-IA01-10.md) | IA-01 | FR-21 (tiêu đề trang) | Đăng nhập, Đăng ký, Quên MK, Giỏ hàng, Thanh toán, Hồ sơ/ĐH | ❌ Failed |
| 11 | [GUI-IA01-11](IA-01/GUI-IA01-11.md) | IA-01 | FR-21 (tiêu đề trang) | Đăng nhập | ❌ Failed |
| 12 | [GUI-IA01-12](IA-01/GUI-IA01-12.md) | IA-01 | Heuristic (page title) | Tất cả 8 màn hình | ❌ Failed |
| 13 | [GUI-IA01-13](IA-01/GUI-IA01-13.md) | IA-01 | FR-21 (tab order) | Đăng nhập, Đăng ký, Quên MK, Thanh toán, Hồ sơ | ❌ Failed |
| 14 | [GUI-IA01-14](IA-01/GUI-IA01-14.md) | IA-01 | Heuristic (responsive) | Chi tiết SP | ❌ Failed |
| 15 | [GUI-IA01-15](IA-01/GUI-IA01-15.md) | IA-01 | Heuristic (responsive) | Trang chủ | ✅ Passed |
| 16 | [GUI-IA01-16](IA-01/GUI-IA01-16.md) | IA-01 | Heuristic (text overflow) | Trang chủ | ❌ Failed |
| 17 | [GUI-IA02-01](IA-02/GUI-IA02-01.md) | IA-02 | FR-22 (required indicator) | Đăng ký, Đăng nhập, Quên MK, Hồ sơ | ❌ Failed |
| 18 | [GUI-IA02-02](IA-02/GUI-IA02-02.md) | IA-02 | FR-22 (input type) | Đăng ký, Đăng nhập, Quên MK | ❌ Failed |
| 19 | [GUI-IA02-03](IA-02/GUI-IA02-03.md) | IA-02 | FR-22 (password masking) | Đăng nhập | ❌ Failed |
| 20 | [GUI-IA02-04](IA-02/GUI-IA02-04.md) | IA-02 | FR-22 (message placement — ngược convention) | Đăng nhập, Đăng ký, Quên MK, Hồ sơ | ❌ Failed |
| 21 | [GUI-IA02-05](IA-02/GUI-IA02-05.md) | IA-02 | FR-22 (step indicator) | Quên mật khẩu | ❌ Failed |
| 22 | [GUI-IA02-06](IA-02/GUI-IA02-06.md) | IA-02 | FR-22 (format constraints: phone) | Hồ sơ | ❌ Failed |
| 23 | [GUI-IA02-07](IA-02/GUI-IA02-07.md) | IA-02 | FR-22 (validation) + heuristic | Đăng ký, Quên MK | ❌ Failed |
| 24 | [GUI-IA02-08](IA-02/GUI-IA02-08.md) | IA-02 | FR-22 (format constraints: OTP) | Quên mật khẩu | ❌ Failed |
| 25 | [GUI-IA02-09](IA-02/GUI-IA02-09.md) | IA-02 | FR-22 (format constraints: quantity) | Chi tiết SP | ❌ Failed |
| 26 | [GUI-IA02-10](IA-02/GUI-IA02-10.md) | IA-02 | Heuristic (input constraint — nghiêm trọng) | Thanh toán | ❌ Failed |
| 27 | [GUI-IA02-11](IA-02/GUI-IA02-11.md) | IA-02 | Heuristic (format constraints: coupon) | Thanh toán | ✅ Passed |
| 28 | [GUI-IA02-12](IA-02/GUI-IA02-12.md) | IA-02 | FR-22 (disabled state) — kỳ vọng Pass | Hồ sơ | ✅ Passed |
| 29 | [GUI-IA02-13](IA-02/GUI-IA02-13.md) | IA-02 | Heuristic (confirmation-field matching) | Đăng ký | ❌ Failed |
| 30 | [GUI-IA02-14](IA-02/GUI-IA02-14.md) | IA-02 | Heuristic (validation timing/consistency) | Đăng ký, Đăng nhập, Quên MK | ❌ Failed |
| 31 | [GUI-IA03-01](IA-03/GUI-IA03-01.md) | IA-03 | FR-23 (active highlight) | Tất cả 8 màn hình (Header) | ❌ Failed |
| 32 | [GUI-IA03-02](IA-03/GUI-IA03-02.md) | IA-03 | FR-23 (badge/counter) | Tất cả 8 màn hình (Header) | ❌ Failed |
| 33 | [GUI-IA03-03](IA-03/GUI-IA03-03.md) | IA-03 | FR-23 (exact label wording) | Header (đã đăng nhập) | ❌ Failed |
| 34 | [GUI-IA03-04](IA-03/GUI-IA03-04.md) | IA-03 | FR-23 (breadcrumb) | Chi tiết SP, Giỏ hàng, Thanh toán | ❌ Failed |
| 35 | [GUI-IA03-05](IA-03/GUI-IA03-05.md) | IA-03 | Heuristic (invalid-URL/404) | Toàn app | ❌ Failed |
| 36 | [GUI-IA03-06](IA-03/GUI-IA03-06.md) | IA-03 | Heuristic (not-found handling) | Chi tiết SP | ❌ Failed |
| 37 | [GUI-IA03-07](IA-03/GUI-IA03-07.md) | IA-03 | Heuristic (navigation consistency) | Đăng nhập | ❌ Failed |
| 38 | [GUI-IA03-08](IA-03/GUI-IA03-08.md) | IA-03 | Heuristic (back/continue links) | Thanh toán | ❌ Failed |
| 39 | [GUI-IA03-09](IA-03/GUI-IA03-09.md) | IA-03 | Heuristic (redirect flow) | Giỏ hàng → Đăng nhập | ❌ Failed |
| 40 | [GUI-IA03-10](IA-03/GUI-IA03-10.md) | IA-03 | Heuristic (browser back-button) | Thanh toán | ✅ Passed |
| 41 | [GUI-IA03-11](IA-03/GUI-IA03-11.md) | IA-03 | Heuristic (browser back-button, multi-step) | Quên mật khẩu | ❌ Failed |
| 42 | [GUI-IA03-12](IA-03/GUI-IA03-12.md) | IA-03 | Heuristic (route guarding) | Thanh toán | ❌ Failed |
| 43 | [GUI-IA03-13](IA-03/GUI-IA03-13.md) | IA-03 | Heuristic (dead-end navigation) | Hồ sơ/ĐH | ❌ Failed |
| 44 | [GUI-IA03-14](IA-03/GUI-IA03-14.md) | IA-03 | Heuristic (logo home link) — kỳ vọng Pass | Tất cả 8 màn hình | ✅ Passed |
| 45 | [GUI-IA03-15](IA-03/GUI-IA03-15.md) | IA-03 | Heuristic (pagination) | Trang chủ, Lịch sử ĐH | ✅ Passed |
| 46 | [GUI-IA04-01](IA-04/GUI-IA04-01.md) | IA-04 | FR-24 (add-to-cart feedback) | Trang chủ | ❌ Failed |
| 47 | [GUI-IA04-02](IA-04/GUI-IA04-02.md) | IA-04 | FR-24 (add-to-cart feedback) | Chi tiết SP | ❌ Failed |
| 48 | [GUI-IA04-03](IA-04/GUI-IA04-03.md) | IA-04 | FR-24 (confirmation dialog) | Giỏ hàng | ❌ Failed |
| 49 | [GUI-IA04-04](IA-04/GUI-IA04-04.md) | IA-04 | FR-24 (confirmation dialog) | Lịch sử ĐH | ❌ Failed |
| 50 | [GUI-IA04-05](IA-04/GUI-IA04-05.md) | IA-04 | FR-24 (empty-state visuals) | Giỏ hàng, Lịch sử ĐH | ❌ Failed |
| 51 | [GUI-IA04-06](IA-04/GUI-IA04-06.md) | IA-04 | FR-24 (empty-state visuals) | Trang chủ | ❌ Failed |
| 52 | [GUI-IA04-07](IA-04/GUI-IA04-07.md) | IA-04 | FR-24 (image alt-text) | Trang chủ | ❌ Failed |
| 53 | [GUI-IA04-08](IA-04/GUI-IA04-08.md) | IA-04 | Heuristic (loading indicators) | Trang chủ, Lịch sử ĐH, Chi tiết SP | ❌ Failed |
| 54 | [GUI-IA04-09](IA-04/GUI-IA04-09.md) | IA-04 | Heuristic (error state) | Chi tiết SP | ❌ Failed |
| 55 | [GUI-IA04-10](IA-04/GUI-IA04-10.md) | IA-04 | Heuristic (toast consistency) | Quên MK, Hồ sơ, Giỏ hàng, Thanh toán | ❌ Failed |
| 56 | [GUI-IA04-11](IA-04/GUI-IA04-11.md) | IA-04 | FR-24 + FR-02 (account-lockout messaging) | Đăng nhập | ❌ Failed |
| 57 | [GUI-IA04-12](IA-04/GUI-IA04-12.md) | IA-04 | FR-24 (coupon feedback) — kỳ vọng Pass | Thanh toán | ✅ Passed |
| 58 | [GUI-IA04-13](IA-04/GUI-IA04-13.md) | IA-04 | FR-24 + README mục 1 (safe rendering) | Trang chủ, Header, Hồ sơ | ❌ Failed |
| 59 | [GUI-IA04-14](IA-04/GUI-IA04-14.md) | IA-04 | Heuristic (error feedback) | Trang chủ | ❌ Failed |
| 60 | [GUI-IA04-15](IA-04/GUI-IA04-15.md) | IA-04 | Heuristic (state consistency) | Thanh toán, Giỏ hàng | ❌ Failed |
| 61 | [GUI-IA04-16](IA-04/GUI-IA04-16.md) | IA-04 | Heuristic (error vs empty) | Lịch sử ĐH | ❌ Failed |
| 62 | [GUI-IA04-17](IA-04/GUI-IA04-17.md) | IA-04 | Heuristic (action feedback) | Đăng ký | ❌ Failed |
| 63 | [GUI-GAP-01](IA-04/GUI-GAP-01.md) | IA-04 | Heuristic (state persistence) — bổ sung thủ công | Giỏ hàng (toàn app) | ❌ Failed |
| 64 | [GUI-GAP-02](IA-04/GUI-GAP-02.md) | IA-04 | Heuristic (cart merge) — bổ sung thủ công | Trang chủ, Giỏ hàng | ❌ Failed |
| 65 | [GUI-GAP-03](IA-01/GUI-GAP-03.md) | IA-01 | Heuristic / WCAG 3.1.1 (language of page) — bổ sung thủ công | Toàn app | ❌ Failed |
| 66 | [GUI-GAP-04](IA-02/GUI-GAP-04.md) | IA-02 | Heuristic / WCAG 1.3.1, 4.1.2 (label association) — bổ sung thủ công | Đăng nhập, Đăng ký, Quên MK, Hồ sơ | ❌ Failed |

**Tổng: 66 test case** — IA-01: 17 · IA-02: 15 · IA-03: 15 · IA-04: 19.