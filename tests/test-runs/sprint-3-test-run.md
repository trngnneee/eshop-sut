# Test Run - Sprint 3 (FR-03 Forgot Password)

**Ngày thực hiện**: 29/06/2026  
**Người thực hiện**: Playwright E2E (aligned spec)  
**Môi trường thử nghiệm**: Frontend `http://localhost:5173` · Backend `http://localhost:3000` · Chromium · Playwright 1.61  
**Nguồn kết quả**: `test-results/results.json` — `npx playwright test tests/e2e/forgot-password.spec.js` (44 tests)  
**Gap analysis**: [gap-analysis-FR-03.md](../test-summary/gap-analysis-FR-03.md)

## Tổng kết

| Chỉ số | Giá trị |
| :--- | :--- |
| Markdown TC (DT + BVA) | 44 |
| Supplementary TC | 4 |
| Pass | 5 |
| Fail | 39 |
| Pass rate | 11% |

> **Ghi chú:** Spec E2E đã đồng bộ ID với markdown TC 001–044 (GAP-06 đã khắc phục). Nhiều case Fail do timeout 30s — SUT không hiển thị thông báo lỗi mà automation chờ.

## Kết quả chi tiết

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [TC-FORGOT-001](../test-cases/forgot/TC-FORGOT-001.md) | Forgot Password | Playwright | Fail | #4, #7 | Thiếu confirm-password; regex client từ chối `NewPass1!`. |
| [TC-FORGOT-002](../test-cases/forgot/TC-FORGOT-002.md) | Forgot Password | Playwright | Fail | None | Timeout — automation không phát hiện phản hồi lỗi email rỗng. |
| [TC-FORGOT-003](../test-cases/forgot/TC-FORGOT-003.md) | Forgot Password | Playwright | Fail | #8 | type=text; không chặn format email (timeout). |
| [TC-FORGOT-004](../test-cases/forgot/TC-FORGOT-004.md) | Forgot Password | Playwright | Fail | None | Timeout — không phát hiện lỗi email chưa đăng ký. |
| [TC-FORGOT-005](../test-cases/forgot/TC-FORGOT-005.md) | Forgot Password | Playwright | Fail | None | Timeout — OTP rỗng không có phản hồi lỗi rõ. |
| [TC-FORGOT-006](../test-cases/forgot/TC-FORGOT-006.md) | Forgot Password | Playwright | Fail | #6 | Timeout — OTP chứa chữ cái không bị từ chối rõ. |
| [TC-FORGOT-007](../test-cases/forgot/TC-FORGOT-007.md) | Forgot Password | Playwright | Fail | #6 | Timeout — OTP 5 số không bị từ chối rõ. |
| [TC-FORGOT-008](../test-cases/forgot/TC-FORGOT-008.md) | Forgot Password | Playwright | Fail | #6 | Timeout — OTP 7 số không bị từ chối (spec yêu cầu 6). |
| [TC-FORGOT-009](../test-cases/forgot/TC-FORGOT-009.md) | Forgot Password | Playwright | Fail | #7 | Timeout — OTP sai không hiển thị lỗi rõ. |
| [TC-FORGOT-010](../test-cases/forgot/TC-FORGOT-010.md) | Forgot Password | Playwright | Pass | None | API từ chối OTP cross-email — đúng spec. |
| [TC-FORGOT-011](../test-cases/forgot/TC-FORGOT-011.md) | Forgot Password | Playwright | Fail | #4, #7 | Timeout — mật khẩu rỗng; thiếu confirm field. |
| [TC-FORGOT-012](../test-cases/forgot/TC-FORGOT-012.md) | Forgot Password | Playwright | Fail | #7 | Timeout — MK 7 ký tự không báo lỗi FR-01. |
| [TC-FORGOT-013](../test-cases/forgot/TC-FORGOT-013.md) | Forgot Password | Playwright | Fail | #7 | Timeout — thiếu chữ hoa. |
| [TC-FORGOT-014](../test-cases/forgot/TC-FORGOT-014.md) | Forgot Password | Playwright | Fail | #7 | Timeout — thiếu chữ thường. |
| [TC-FORGOT-015](../test-cases/forgot/TC-FORGOT-015.md) | Forgot Password | Playwright | Fail | #7 | Timeout — thiếu chữ số. |
| [TC-FORGOT-016](../test-cases/forgot/TC-FORGOT-016.md) | Forgot Password | Playwright | Fail | #7 | Regex yêu cầu space thay vì ký tự đặc biệt. |
| [TC-FORGOT-017](../test-cases/forgot/TC-FORGOT-017.md) | Forgot Password | Playwright | Fail | #4 | Không có trường xác nhận mật khẩu. |
| [TC-FORGOT-018](../test-cases/forgot/TC-FORGOT-018.md) | Forgot Password | Playwright | Fail | #4 | Không kiểm tra khớp mật khẩu. |
| [TC-FORGOT-019](../test-cases/forgot/TC-FORGOT-019.md) | Forgot Password | Playwright | Fail | #5 | Không có Step Indicator. |
| [TC-FORGOT-020](../test-cases/forgot/TC-FORGOT-020.md) | Forgot Password | Playwright | Fail | #9 | "Quay lại" không về `/login`. |
| [TC-FORGOT-021](../test-cases/forgot/TC-FORGOT-021.md) | Forgot Password | Playwright | Fail | None | Timeout — email 4 ký tự không báo lỗi độ dài. |
| [TC-FORGOT-022](../test-cases/forgot/TC-FORGOT-022.md) | Forgot Password | Playwright | Pass | None | Email 5 ký tự — không báo lỗi độ dài (đúng BVA min). |
| [TC-FORGOT-023](../test-cases/forgot/TC-FORGOT-023.md) | Forgot Password | Playwright | Pass | None | Email 6 ký tự — không báo lỗi độ dài (đúng BVA min+). |
| [TC-FORGOT-024](../test-cases/forgot/TC-FORGOT-024.md) | Forgot Password | Playwright | Pass | None | Email 99 ký tự — không báo lỗi độ dài (đúng BVA max−). |
| [TC-FORGOT-025](../test-cases/forgot/TC-FORGOT-025.md) | Forgot Password | Playwright | Pass | None | Email 100 ký tự — không báo lỗi độ dài (đúng BVA max). |
| [TC-FORGOT-026](../test-cases/forgot/TC-FORGOT-026.md) | Forgot Password | Playwright | Fail | None | Timeout — email 101 ký tự không báo lỗi độ dài. |
| [TC-FORGOT-027](../test-cases/forgot/TC-FORGOT-027.md) | Forgot Password | Playwright | Fail | #6 | Timeout — OTP BVA 5 số không bị từ chối. |
| [TC-FORGOT-028](../test-cases/forgot/TC-FORGOT-028.md) | Forgot Password | Playwright | Fail | #7 | Reset MK 6 ký tự không redirect `/login`. |
| [TC-FORGOT-029](../test-cases/forgot/TC-FORGOT-029.md) | Forgot Password | Playwright | Fail | #6 | Timeout — OTP BVA 7 số không bị từ chối. |
| [TC-FORGOT-030](../test-cases/forgot/TC-FORGOT-030.md) | Forgot Password | Playwright | Fail | #7 | Timeout — MK 7 ký tự BVA không báo lỗi. |
| [TC-FORGOT-031](../test-cases/forgot/TC-FORGOT-031.md) | Forgot Password | Playwright | Fail | #7 | Reset MK 8 ký tự (min) không thành công. |
| [TC-FORGOT-032](../test-cases/forgot/TC-FORGOT-032.md) | Forgot Password | Playwright | Fail | #7 | Reset MK 9 ký tự (min+) không thành công. |
| [TC-FORGOT-033](../test-cases/forgot/TC-FORGOT-033.md) | Forgot Password | Playwright | Fail | #7 | Reset MK 49 ký tự (max−) không thành công. |
| [TC-FORGOT-034](../test-cases/forgot/TC-FORGOT-034.md) | Forgot Password | Playwright | Fail | #7 | Reset MK 50 ký tự (max) không thành công. |
| [TC-FORGOT-035](../test-cases/forgot/TC-FORGOT-035.md) | Forgot Password | Playwright | Fail | #7 | Timeout — MK 51 ký tự không báo lỗi. |
| [TC-FORGOT-036](../test-cases/forgot/TC-FORGOT-036.md) | Forgot Password | Playwright | Fail | #4 | Timeout — thiếu trường confirm; MK 7 ký tự. |
| [TC-FORGOT-037](../test-cases/forgot/TC-FORGOT-037.md) | Forgot Password | Playwright | Fail | #7 | Reset confirm 8 ký tự không thành công. |
| [TC-FORGOT-038](../test-cases/forgot/TC-FORGOT-038.md) | Forgot Password | Playwright | Fail | #7 | Reset confirm 9 ký tự không thành công. |
| [TC-FORGOT-039](../test-cases/forgot/TC-FORGOT-039.md) | Forgot Password | Playwright | Fail | #7 | Reset confirm 49 ký tự không thành công. |
| [TC-FORGOT-040](../test-cases/forgot/TC-FORGOT-040.md) | Forgot Password | Playwright | Fail | #7 | Reset confirm 50 ký tự không thành công. |
| [TC-FORGOT-041](../test-cases/forgot/TC-FORGOT-041.md) | Forgot Password | Playwright | Fail | #4 | Timeout — confirm 51 ký tự; thiếu trường confirm. |
| [TC-FORGOT-042](../test-cases/forgot/TC-FORGOT-042.md) | Forgot Password | Playwright | Fail | #7 | Cross-boundary min (MK 8 + confirm 8) — reset fail. |
| [TC-FORGOT-043](../test-cases/forgot/TC-FORGOT-043.md) | Forgot Password | Playwright | Fail | #7 | Cross-boundary max (MK 50 + confirm 50) — reset fail. |
| [TC-FORGOT-044](../test-cases/forgot/TC-FORGOT-044.md) | Forgot Password | Playwright | Fail | #4 | Timeout — confirm min− mismatch; thiếu trường confirm. |
| [TC-FORGOT-SUP-001](../test-cases/forgot/TC-FORGOT-SUP-001.md) | Forgot Password | — | Not Run | #6 | Gap remediation — OTP 6 digits. |
| [TC-FORGOT-SUP-002](../test-cases/forgot/TC-FORGOT-SUP-002.md) | Forgot Password | — | Not Run | #10 | Gap remediation — server password validation. |
| [TC-FORGOT-SUP-003](../test-cases/forgot/TC-FORGOT-SUP-003.md) | Forgot Password | — | Not Run | #8 | Gap remediation — FR-22 email type. |
| [TC-FORGOT-SUP-004](../test-cases/forgot/TC-FORGOT-SUP-004.md) | Forgot Password | — | Not Run | None | Gap remediation — OTP one-time use. |

## Phân loại lỗi automation

| Mẫu lỗi | Số TC | Mô tả |
| :--- | :--- | :--- |
| Timeout (30s) | 24 | Invalid input không có phản hồi lỗi UI/API rõ ràng |
| Assertion fail | 15 | Thiếu UI (#4, #5, #9), reset không redirect (#7), regex chặn MK hợp lệ |
| Pass | 5 | TC-010, 022, 023, 024, 025 |

## Bug reports (paste vào GitHub Issues)

| Issue | Title | Found by (this run) |
| :--- | :--- | :--- |
| #4 | Missing confirm-password field | TC-FORGOT-001, 017, 018, 036, 041, 044 |
| #5 | Missing Step Indicator | TC-FORGOT-019 |
| #6 | OTP 4 digits not 6 | TC-FORGOT-006–008, 027, 029, SUP-001 |
| #7 | Wrong password regex | TC-FORGOT-001, 009, 011–016, 028, 030–035, 037–043 |
| #8 | Email type text not email | TC-FORGOT-003, SUP-003 |
| #9 | Back button not to login | TC-FORGOT-020 |
| #10 | No server password validation | TC-FORGOT-SUP-002 |

Chi tiết: `tests/bug-reports/issue-004` … `issue-010.md`  
Artifacts: `test-results/` (screenshots, traces, video)
