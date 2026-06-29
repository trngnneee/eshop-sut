# Test Run - Sprint 3 (FR-03 Forgot Password)

**Ngày thực hiện**: 29/06/2026  
**Người thực hiện**: Playwright E2E (eshop-tests)  
**Môi trường thử nghiệm**: Frontend Web `http://localhost:5173` · Backend API `http://localhost:3000` · Chromium · Playwright 1.61.1  
**Nguồn kết quả**: `eshop-tests/test-results/results.json` (`.last-run.json`: 39 failed / 44 total)

## Tổng kết

| Chỉ số | Giá trị |
| :--- | :--- |
| Tổng TC | 44 |
| Pass | 5 |
| Fail | 39 |
| Blocked | 0 |
| Pass rate | 11.4% |

## Kết quả chi tiết

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [TC-FORGOT-001](../test-cases/forgot/TC-FORGOT-001.md) | Forgot Password | Playwright | Fail | TBD | Bước 2 thiếu trường Xác nhận mật khẩu (FR-03). |
| [TC-FORGOT-002](../test-cases/forgot/TC-FORGOT-002.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi Email rỗng. |
| [TC-FORGOT-003](../test-cases/forgot/TC-FORGOT-003.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi Email sai định dạng. |
| [TC-FORGOT-004](../test-cases/forgot/TC-FORGOT-004.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi Email chưa đăng ký. |
| [TC-FORGOT-005](../test-cases/forgot/TC-FORGOT-005.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi OTP rỗng. |
| [TC-FORGOT-006](../test-cases/forgot/TC-FORGOT-006.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi OTP chứa ký tự không phải số. |
| [TC-FORGOT-007](../test-cases/forgot/TC-FORGOT-007.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi OTP 5 chữ số. |
| [TC-FORGOT-008](../test-cases/forgot/TC-FORGOT-008.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi OTP 7 chữ số. |
| [TC-FORGOT-009](../test-cases/forgot/TC-FORGOT-009.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi OTP sai giá trị. |
| [TC-FORGOT-010](../test-cases/forgot/TC-FORGOT-010.md) | Forgot Password | Playwright | Pass | None | API từ chối OTP của email A dùng cho email B — đúng đặc tả. |
| [TC-FORGOT-011](../test-cases/forgot/TC-FORGOT-011.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi mật khẩu mới rỗng. |
| [TC-FORGOT-012](../test-cases/forgot/TC-FORGOT-012.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi mật khẩu quá ngắn. |
| [TC-FORGOT-013](../test-cases/forgot/TC-FORGOT-013.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi thiếu chữ hoa. |
| [TC-FORGOT-014](../test-cases/forgot/TC-FORGOT-014.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi thiếu chữ thường. |
| [TC-FORGOT-015](../test-cases/forgot/TC-FORGOT-015.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi thiếu chữ số. |
| [TC-FORGOT-016](../test-cases/forgot/TC-FORGOT-016.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi thiếu ký tự đặc biệt. |
| [TC-FORGOT-017](../test-cases/forgot/TC-FORGOT-017.md) | Forgot Password | Playwright | Fail | TBD | Thiếu trường Xác nhận mật khẩu — không thể kiểm thử từ chối rỗng. |
| [TC-FORGOT-018](../test-cases/forgot/TC-FORGOT-018.md) | Forgot Password | Playwright | Fail | TBD | Thiếu trường Xác nhận mật khẩu — không thể kiểm thử không khớp. |
| [TC-FORGOT-019](../test-cases/forgot/TC-FORGOT-019.md) | Forgot Password | Playwright | Fail | TBD | Giao diện không hiển thị Step Indicator (Bước 1/2). |
| [TC-FORGOT-020](../test-cases/forgot/TC-FORGOT-020.md) | Forgot Password | Playwright | Fail | TBD | Không có nút/link "Quay lại đăng nhập" (chỉ có "← Quay lại"). |
| [TC-FORGOT-021](../test-cases/forgot/TC-FORGOT-021.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện lỗi độ dài Email 4 ký tự. |
| [TC-FORGOT-022](../test-cases/forgot/TC-FORGOT-022.md) | Forgot Password | Playwright | Pass | None | Không báo lỗi độ dài với Email 5 ký tự (biên min). |
| [TC-FORGOT-023](../test-cases/forgot/TC-FORGOT-023.md) | Forgot Password | Playwright | Pass | None | Không báo lỗi độ dài với Email 6 ký tự (min+). |
| [TC-FORGOT-024](../test-cases/forgot/TC-FORGOT-024.md) | Forgot Password | Playwright | Pass | None | Không báo lỗi độ dài với Email 99 ký tự (max−). |
| [TC-FORGOT-025](../test-cases/forgot/TC-FORGOT-025.md) | Forgot Password | Playwright | Pass | None | Không báo lỗi độ dài với Email 100 ký tự (max). |
| [TC-FORGOT-026](../test-cases/forgot/TC-FORGOT-026.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện lỗi độ dài Email 101 ký tự. |
| [TC-FORGOT-027](../test-cases/forgot/TC-FORGOT-027.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi OTP 5 chữ số (BVA). |
| [TC-FORGOT-028](../test-cases/forgot/TC-FORGOT-028.md) | Forgot Password | Playwright | Fail | TBD | Đặt lại mật khẩu không thành công / không chuyển về `/login`. |
| [TC-FORGOT-029](../test-cases/forgot/TC-FORGOT-029.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi OTP 7 chữ số (BVA). |
| [TC-FORGOT-030](../test-cases/forgot/TC-FORGOT-030.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi mật khẩu 7 ký tự (BVA). |
| [TC-FORGOT-031](../test-cases/forgot/TC-FORGOT-031.md) | Forgot Password | Playwright | Fail | TBD | Đặt lại mật khẩu hợp lệ 8 ký tự không redirect `/login`. |
| [TC-FORGOT-032](../test-cases/forgot/TC-FORGOT-032.md) | Forgot Password | Playwright | Fail | TBD | Đặt lại mật khẩu hợp lệ 9 ký tự không redirect `/login`. |
| [TC-FORGOT-033](../test-cases/forgot/TC-FORGOT-033.md) | Forgot Password | Playwright | Fail | TBD | Đặt lại mật khẩu hợp lệ 49 ký tự không redirect `/login`. |
| [TC-FORGOT-034](../test-cases/forgot/TC-FORGOT-034.md) | Forgot Password | Playwright | Fail | TBD | Đặt lại mật khẩu hợp lệ 50 ký tự không redirect `/login`. |
| [TC-FORGOT-035](../test-cases/forgot/TC-FORGOT-035.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi mật khẩu 51 ký tự. |
| [TC-FORGOT-036](../test-cases/forgot/TC-FORGOT-036.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi xác nhận 7 ký tự. |
| [TC-FORGOT-037](../test-cases/forgot/TC-FORGOT-037.md) | Forgot Password | Playwright | Fail | TBD | Đặt lại mật khẩu với xác nhận 8 ký tự không redirect `/login`. |
| [TC-FORGOT-038](../test-cases/forgot/TC-FORGOT-038.md) | Forgot Password | Playwright | Fail | TBD | Đặt lại mật khẩu với xác nhận 9 ký tự không redirect `/login`. |
| [TC-FORGOT-039](../test-cases/forgot/TC-FORGOT-039.md) | Forgot Password | Playwright | Fail | TBD | Đặt lại mật khẩu với xác nhận 49 ký tự không redirect `/login`. |
| [TC-FORGOT-040](../test-cases/forgot/TC-FORGOT-040.md) | Forgot Password | Playwright | Fail | TBD | Đặt lại mật khẩu với xác nhận 50 ký tự không redirect `/login`. |
| [TC-FORGOT-041](../test-cases/forgot/TC-FORGOT-041.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi xác nhận 51 ký tự. |
| [TC-FORGOT-042](../test-cases/forgot/TC-FORGOT-042.md) | Forgot Password | Playwright | Fail | TBD | Cross-boundary min (8) — reset không thành công. |
| [TC-FORGOT-043](../test-cases/forgot/TC-FORGOT-043.md) | Forgot Password | Playwright | Fail | TBD | Cross-boundary max (50) — reset không thành công. |
| [TC-FORGOT-044](../test-cases/forgot/TC-FORGOT-044.md) | Forgot Password | Playwright | Fail | TBD | Timeout — không phát hiện phản hồi lỗi khi xác nhận min− (7). |

## Các lỗi phát hiện (nhóm theo nguyên nhân)

> **Related Bug** trong bảng trên đang để `TBD` — cập nhật thành `#NN` sau khi tạo GitHub Issue (Skill-04).

1. **Thiếu trường Xác nhận mật khẩu (Bước 2)** — `ForgotPassword.jsx` chỉ có OTP + Mật khẩu mới. Ảnh hưởng: TC-FORGOT-001, 017, 018.
2. **Thiếu Step Indicator** — Không hiển thị "Bước 1 / 2" / "Bước 2 / 2". Ảnh hưởng: TC-FORGOT-019.
3. **Thiếu nút "Quay lại đăng nhập"** — Chỉ có nút "← Quay lại" (không điều hướng `/login`). Ảnh hưởng: TC-FORGOT-020.
4. **Regex mật khẩu sai + OTP 4 chữ số** — Frontend dùng regex yêu cầu khoảng trắng thay vì ký tự đặc biệt FR-01; backend sinh OTP 4 số thay vì 6. Reset hợp lệ không hoàn tất. Ảnh hưởng: TC-FORGOT-028, 031–034, 037–040, 042–043.
5. **Không có phản hồi lỗi rõ ràng cho input không hợp lệ** — Nhiều TC từ chối (Email/OTP/mật khẩu) timeout 30s vì không có inline error hoặc alert được automation bắt kịp. Ảnh hưởng: phần lớn TC Fail còn lại.

## Evidence

Screenshots / trace nằm tại `eshop-tests/test-results/` (thư mục con theo từng test case Playwright).
