# Test Run — FR-08 Checkout

**Ngày thực hiện**: 29/06/2026  
**Người thực hiện**: Playwright E2E  
**Môi trường thử nghiệm**: Frontend `http://localhost:5173` · Backend `http://localhost:3000` · Chromium · Playwright  
**Lệnh chạy**: `npx playwright test tests/e2e/checkout.spec.js`  
**Gap analysis**: [gap-analysis-FR-08.md](../test-summary/gap-analysis-FR-08.md)

## Tổng kết

| Chỉ số | Giá trị |
| :--- | :--- |
| Markdown TC (DT + BVA) | 44 |
| Supplementary TC | 6 |
| **Tổng automation** | **50** |
| Pass | 12 |
| Fail | 38 |
| Pass rate | 24% |

> **Ghi chú:** Nhiều case UI Fail do automation không seed giỏ hàng đáng tin (`getProductLineCount() === 0`). Các defect SUT đã xác nhận qua API/UI tamper: #11–#14.

## Kết quả chi tiết

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [TC-CHECKOUT-001](../test-cases/checkout/TC-CHECKOUT-001.md) | Checkout | Playwright | Fail | #14 | `logout()` SecurityError trên `about:blank` — automation. |
| [TC-CHECKOUT-002](../test-cases/checkout/TC-CHECKOUT-002.md) | Checkout | Playwright | Fail | None | Giỏ trống trên checkout — automation seed cart. |
| [TC-CHECKOUT-003](../test-cases/checkout/TC-CHECKOUT-003.md) | Checkout | Playwright | Fail | None | `getProductLineCount() === 0` — automation. |
| [TC-CHECKOUT-004](../test-cases/checkout/TC-CHECKOUT-004.md) | Checkout | Playwright | Fail | **#11** | Tổng tiền là `input[type=number]` — editable. |
| [TC-CHECKOUT-005](../test-cases/checkout/TC-CHECKOUT-005.md) | Checkout | Playwright | Fail | None | Không có sản phẩm để so sánh tổng — automation. |
| [TC-CHECKOUT-006](../test-cases/checkout/TC-CHECKOUT-006.md) | Checkout | Playwright | Pass | None | Checkout thành công (có thể với giỏ rỗng). |
| [TC-CHECKOUT-007](../test-cases/checkout/TC-CHECKOUT-007.md) | Checkout | Playwright | Pass | None | Cần xác minh lại — SUT không gọi `clearCart()` trong code. |
| [TC-CHECKOUT-008](../test-cases/checkout/TC-CHECKOUT-008.md) | Checkout | Playwright | Pass | None | Empty cart — assertion pass; mâu thuẫn TC-028. |
| [TC-CHECKOUT-009](../test-cases/checkout/TC-CHECKOUT-009.md) | Checkout | Playwright | Fail | None | Danh sách sản phẩm trống — automation. |
| [TC-CHECKOUT-010](../test-cases/checkout/TC-CHECKOUT-010.md) | Checkout | Playwright | Fail | None | qty=1 — không seed cart. |
| [TC-CHECKOUT-011](../test-cases/checkout/TC-CHECKOUT-011.md) | Checkout | Playwright | Fail | None | qty=2 — không seed cart. |
| [TC-CHECKOUT-012](../test-cases/checkout/TC-CHECKOUT-012.md) | Checkout | Playwright | Fail | #13 | Timeout click nút checkout từ cart. |
| [TC-CHECKOUT-013](../test-cases/checkout/TC-CHECKOUT-013.md) | Checkout | Playwright | Fail | None | 1 product type — list empty. |
| [TC-CHECKOUT-014](../test-cases/checkout/TC-CHECKOUT-014.md) | Checkout | Playwright | Fail | None | 2 product types — list empty. |
| [TC-CHECKOUT-015](../test-cases/checkout/TC-CHECKOUT-015.md) | Checkout | Playwright | Fail | **#12** | API chấp nhận `total_amount=0`. |
| [TC-CHECKOUT-016](../test-cases/checkout/TC-CHECKOUT-016.md) | Checkout | Playwright | Fail | **#12** | API chấp nhận `total_amount=cartTotal−1`. |
| [TC-CHECKOUT-017](../test-cases/checkout/TC-CHECKOUT-017.md) | Checkout | Playwright | Pass | None | API chấp nhận tổng đúng — expected (SUT lưu client value). |
| [TC-CHECKOUT-018](../test-cases/checkout/TC-CHECKOUT-018.md) | Checkout | Playwright | Fail | **#12** | API chấp nhận `total_amount=cartTotal+1`. |
| [TC-CHECKOUT-019](../test-cases/checkout/TC-CHECKOUT-019.md) | Checkout | Playwright | Fail | **#14** | `logout()` SecurityError — chưa assert route guard. |
| [TC-CHECKOUT-020](../test-cases/checkout/TC-CHECKOUT-020.md) | Checkout | Playwright | Pass | None | Invalid token → API từ chối. |
| [TC-CHECKOUT-021](../test-cases/checkout/TC-CHECKOUT-021.md) | Checkout | Playwright | Fail | None | Product name — list empty. |
| [TC-CHECKOUT-022](../test-cases/checkout/TC-CHECKOUT-022.md) | Checkout | Playwright | Fail | None | Quantity — list empty. |
| [TC-CHECKOUT-023](../test-cases/checkout/TC-CHECKOUT-023.md) | Checkout | Playwright | Fail | None | Subtotal — list empty. |
| [TC-CHECKOUT-024](../test-cases/checkout/TC-CHECKOUT-024.md) | Checkout | Playwright | Fail | None | 3 product types — list empty. |
| [TC-CHECKOUT-025](../test-cases/checkout/TC-CHECKOUT-025.md) | Checkout | Playwright | Fail | None | Merged qty — automation. |
| [TC-CHECKOUT-026](../test-cases/checkout/TC-CHECKOUT-026.md) | Checkout | Playwright | Fail | **#11, #12** | UI tamper `1` → order lưu `total_amount=1`. |
| [TC-CHECKOUT-027](../test-cases/checkout/TC-CHECKOUT-027.md) | Checkout | Playwright | Fail | None | Strict mode: locator `header, nav` — automation. |
| [TC-CHECKOUT-028](../test-cases/checkout/TC-CHECKOUT-028.md) | Checkout | Playwright | Fail | **#13** | Thanh toán lần 2 khi giỏ trống vẫn thành công. |
| [TC-CHECKOUT-029](../test-cases/checkout/TC-CHECKOUT-029.md) | Checkout | Playwright | Fail | **#12** | API chấp nhận `total_amount` âm. |
| [TC-CHECKOUT-030](../test-cases/checkout/TC-CHECKOUT-030.md) | Checkout | Playwright | Pass | None | Missing `total_amount` → lỗi/xử lý đúng. |
| [TC-CHECKOUT-031](../test-cases/checkout/TC-CHECKOUT-031.md) | Checkout | Playwright | Fail | **#12** | API chấp nhận `total_amount` non-numeric. |
| [TC-CHECKOUT-032](../test-cases/checkout/TC-CHECKOUT-032.md) | Checkout | Playwright | Pass | None | Empty items + positive total → rejected. |
| [TC-CHECKOUT-033](../test-cases/checkout/TC-CHECKOUT-033.md) | Checkout | Playwright | Pass | None | Admin checkout thành công. |
| [TC-CHECKOUT-034](../test-cases/checkout/TC-CHECKOUT-034.md) | Checkout | Playwright | Fail | None | qty=3 — automation. |
| [TC-CHECKOUT-035](../test-cases/checkout/TC-CHECKOUT-035.md) | Checkout | Playwright | Fail | None | qty=10 — automation. |
| [TC-CHECKOUT-036](../test-cases/checkout/TC-CHECKOUT-036.md) | Checkout | Playwright | Fail | None | 3 product types — automation. |
| [TC-CHECKOUT-037](../test-cases/checkout/TC-CHECKOUT-037.md) | Checkout | Playwright | Fail | None | Lowest price product — automation. |
| [TC-CHECKOUT-038](../test-cases/checkout/TC-CHECKOUT-038.md) | Checkout | Playwright | Fail | **#12** | API chấp nhận `total_amount=−1`. |
| [TC-CHECKOUT-039](../test-cases/checkout/TC-CHECKOUT-039.md) | Checkout | Playwright | Fail | **#12** | API chấp nhận `total_amount=1` khi cart lớn. |
| [TC-CHECKOUT-040](../test-cases/checkout/TC-CHECKOUT-040.md) | Checkout | Playwright | Fail | None | qty=99 — automation. |
| [TC-CHECKOUT-041](../test-cases/checkout/TC-CHECKOUT-041.md) | Checkout | Playwright | Fail | None | 4 product types — automation. |
| [TC-CHECKOUT-042](../test-cases/checkout/TC-CHECKOUT-042.md) | Checkout | Playwright | Fail | **#12** | API chấp nhận `2×cartTotal`. |
| [TC-CHECKOUT-043](../test-cases/checkout/TC-CHECKOUT-043.md) | Checkout | Playwright | Fail | **#12** | API chấp nhận decimal `total_amount`. |
| [TC-CHECKOUT-044](../test-cases/checkout/TC-CHECKOUT-044.md) | Checkout | Playwright | Fail | None | Total update khi tăng qty — automation. |
| [TC-CHECKOUT-SUP-001](../test-cases/checkout/TC-CHECKOUT-SUP-001.md) | Checkout | Playwright | Pass | None | Invalid JWT → 401. |
| [TC-CHECKOUT-SUP-002](../test-cases/checkout/TC-CHECKOUT-SUP-002.md) | Checkout | Playwright | Pass | None | No JWT → 401. |
| [TC-CHECKOUT-SUP-003](../test-cases/checkout/TC-CHECKOUT-SUP-003.md) | Checkout | Playwright | Fail | **#12** | Backend không tính lại tổng. |
| [TC-CHECKOUT-SUP-004](../test-cases/checkout/TC-CHECKOUT-SUP-004.md) | Checkout | Playwright | Fail | **#12** | Client `items` mismatch — không validate. |
| [TC-CHECKOUT-SUP-005](../test-cases/checkout/TC-CHECKOUT-SUP-005.md) | Checkout | Playwright | Pass | None | Malformed Authorization → 401. |
| [TC-CHECKOUT-SUP-006](../test-cases/checkout/TC-CHECKOUT-SUP-006.md) | Checkout | Playwright | Pass | None | Order total = Σ(price×qty) khi gửi đúng. |

## Phân loại lỗi

| Mẫu lỗi | Số TC (ước lượng) | Mô tả |
| :--- | :--- | :--- |
| SUT — backend `total_amount` | 12 | #12: API tin client, không recalculate |
| SUT — UI editable total | 2 | #11: TC-004, TC-026 |
| SUT — empty cart / repeat checkout | 1–2 | #13: TC-028; TC-012 timeout liên quan |
| SUT — no route guard | 1 | #14: TC-019 (chưa assert đầy đủ) |
| Automation — cart seed | ~22 | `getProductLineCount() === 0` |
| Automation — helper/locator | 3 | logout, navbar locator, cart button timeout |

## Bug reports (paste vào GitHub Issues)

| Issue | Title | Found by (this run) |
| :--- | :--- | :--- |
| [#11](../bug-reports/issue-011-editable-checkout-total.md) | Editable checkout total on UI | TC-004, TC-026 |
| [#12](../bug-reports/issue-012-backend-accepts-client-total.md) | Backend accepts client `total_amount` | TC-015, 016, 018, 026, 029, 031, 038, 039, 042, 043, SUP-003, SUP-004 |
| [#13](../bug-reports/issue-013-empty-cart-checkout-allowed.md) | Empty cart / repeat checkout allowed | TC-028 |
| [#14](../bug-reports/issue-014-no-checkout-route-guard.md) | No auth route guard on `/checkout` | TC-019 (design + code review) |

Artifacts: `test-results/` (screenshots, traces, video per failed test)

## Khuyến nghị automation (lần chạy sau)

1. Sửa `logout()` — `goto('/')` trước khi xóa `localStorage`.
2. Seed cart qua nút **"Thêm vào giỏ"** trên Home thay vì product-detail double-click.
3. Sửa locator TC-027 (navbar cart badge).
4. Chạy lại để tách rõ automation fail vs SUT fail trên danh sách sản phẩm (FR-08 rule 3).
