# Decision Table Summary - FR-09 Mã Giảm Giá (Coupon)

## Metadata

| Field | Value |
| :--- | :--- |
| Requirement ID | FR-09 |
| Module | coupon_application |
| Technique | Decision Table + Pairwise reduction when needed |
| Generated test case folder | tests/test-cases/coupon_application/ |
| Generated test run | tests/test-runs/fr09-coupon-application-test-run.md |

## Sources Reviewed

| Source | Evidence / Note |
| :--- | :--- |
| `README.md:110-120` | FR-09 định nghĩa 5 điều kiện bắt buộc: mã tồn tại/active, còn hạn, đủ ngưỡng, đã đăng nhập, chưa dùng hết lượt. |
| `README.md:122-126` | Công thức giảm giá cho `percent`, `fixed`, và `final_amount`. |
| `README.md:128-135` | Coupon mẫu `SAVE10`, `BIGBUY`, `VIP100`, `EXPIRED`. |
| `api_specification.md:151-163` | Endpoint `POST /api/apply-coupon` và body mẫu gồm `code`, `total_amount`, `user_id`. |
| `backend/database.js:28-45` | Schema `coupons` và `coupon_usage`. |
| `backend/database.js:105-110` | Seed coupon mẫu khớp README. |
| `backend/server.js:362-441` | Logic hiện tại của `POST /api/apply-coupon`. |
| `frontend-web/src/pages/Checkout.jsx:23-39` | UI Checkout gọi `POST /api/apply-coupon` với `code`, `total_amount`, `user_id`. |
| `frontend-web/src/pages/Checkout.jsx:106-135` | UI nhập coupon và hiển thị lỗi/thành công. |

## Conditions and Actions

| Condition ID | Condition | Values / Classes | Source / Evidence | Note |
| :--- | :--- | :--- | :--- | :--- |
| C1 | Trạng thái mã giảm giá | Active exists / Missing or inactive / Empty | `README.md:116`, `backend/server.js:366-377` | C1 false phải bị từ chối riêng. |
| C2 | Hạn sử dụng | Valid date / Expired | `README.md:117`, `backend/server.js:380-384` | `EXPIRED` là coupon mẫu đã hết hạn. |
| C3 | Tổng đơn hàng so với `min_order_amount` | Below min / Equal min / Above min | `README.md:118` | Requirement dùng `>=`, nên `Equal min` phải được chấp nhận. |
| C4 | Xác thực người dùng | JWT hợp lệ / Không có JWT | `README.md:119` | FR-09 yêu cầu user đã đăng nhập. |
| C5 | Số lượt đã dùng | Below max / Reached max | `README.md:120`, `backend/server.js:386-395` | Cần dữ liệu trong `coupon_usage`. |
| C6 | Loại giảm giá | percent / fixed | `README.md:122-126` | Không phải một trong 5 điều kiện, nhưng ảnh hưởng expected amount. |

| Action ID | Action / Expected Result | HTTP/UI Expected Status | Note |
| :--- | :--- | :--- | :--- |
| A1 | Áp dụng coupon percent và tính `discount_amount = total * discount_value / 100` | 200 / success | Dùng `SAVE10`. |
| A2 | Áp dụng coupon fixed và tính `discount_amount = discount_value` | 200 / success | Dùng `BIGBUY`. |
| A3 | Từ chối mã rỗng, không tồn tại, hoặc inactive | 400/404 / error | Không áp dụng giảm giá. |
| A4 | Từ chối mã hết hạn | 400 / error | Không áp dụng giảm giá. |
| A5 | Từ chối đơn hàng dưới ngưỡng tối thiểu | 400 / error | Không áp dụng giảm giá. |
| A6 | Từ chối người dùng chưa đăng nhập | 401/403 / auth error | FR-09 yêu cầu JWT hợp lệ. |
| A7 | Từ chối user đã dùng hết lượt | 400 / error | Không áp dụng giảm giá. |

## Full Decision Table

Full matrix thô có `3 x 2 x 3 x 2 x 2 x 2 = 144` tổ hợp nếu tách `Empty` khỏi `Missing/inactive` và thêm `C6` cho công thức tính tiền. Bảng dưới là decision table chuẩn hóa: các giá trị `-` là don't-care vì action đã được quyết định bởi điều kiện fail ưu tiên.

| Rule ID | C1 Code | C2 Expiry | C3 Total vs Min | C4 Auth | C5 Usage | C6 Type | Action | Expected Status | Risk | Keep? | Generated TC | Reason |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| R01 | Active exists | Valid | Above min | JWT valid | Below max | percent | A1 | Accepted | High | Yes | FR09-P-TC01 | Bao phủ công thức percent trên happy path. |
| R02 | Active exists | Valid | Above min | JWT valid | Below max | fixed | A2 | Accepted | Medium | Yes | FR09-F-TC01 | Bao phủ công thức fixed trên happy path. |
| R03 | Active exists | Valid | Equal min | JWT valid | Below max | percent | A1 | Accepted | High | Yes | FR09-T-TC01 | Requirement dùng `>=`; kiểm tra ngưỡng đúng bằng min. |
| R04 | Active exists | Valid | Equal min | JWT valid | Below max | fixed | A2 | Accepted | High | Yes | FR09-T-TC03 | Pairwise giữ cặp `Equal min + fixed`. |
| R05 | Missing or inactive | - | - | JWT valid | - | - | A3 | Rejected | Medium | Yes | FR09-C-TC01 | Mã phải tồn tại và đang active. |
| R06 | Empty | - | - | JWT valid | - | - | A3 | Rejected | Low | Yes | FR09-C-TC02 | API/UI cần validate mã rỗng. |
| R07 | Active exists | Expired | Above min | JWT valid | Below max | percent | A4 | Rejected | Medium | Yes | FR09-E-TC01 | Mã hết hạn không được áp dụng. |
| R08 | Active exists | Valid | Below min | JWT valid | Below max | percent | A5 | Rejected | High | Yes | FR09-T-TC02 | Điều kiện ngưỡng đơn hàng fail. |
| R09 | Active exists | Valid | Above min | No JWT | - | percent | A6 | Rejected | High | Yes | FR09-A-TC01 | FR-09 yêu cầu user đã đăng nhập. |
| R10 | Active exists | Valid | Above min | JWT valid | Reached max | percent | A7 | Rejected | High | Yes | FR09-U-TC01 | Điều kiện số lượt đã dùng fail. |

## Reduction and Pairwise Rationale

- Mandatory rules kept: R01-R10.
- Impossible/duplicate rules removed: các tổ hợp trong đó C1 là `Missing/inactive` hoặc `Empty` làm C2/C3/C5/C6 không còn ý nghĩa; các tổ hợp expired/under-min/anonymous/reached-max với `fixed` bị coi là duplicate expected action so với rule fail tương ứng.
- Pairwise applied: Yes.
- Reason: FR-09 có nhiều condition tương tác (`type`, `total vs min`, `auth`, `usage`) và full matrix phình lớn. Pairwise được dùng để giữ các cặp rủi ro cao như `Equal min + percent`, `Equal min + fixed`, `No JWT + active code`, `Reached max + active code` mà không sinh toàn bộ tổ hợp 144 rule.

## Pairwise Coverage

| Pair | Covered By TC | Note |
| :--- | :--- | :--- |
| C3=Above min + C6=percent | FR09-P-TC01 | Happy path percent. |
| C3=Above min + C6=fixed | FR09-F-TC01 | Happy path fixed. |
| C3=Equal min + C6=percent | FR09-T-TC01 | Kiểm tra `>= min_order_amount` cho percent. |
| C3=Equal min + C6=fixed | FR09-T-TC03 | Kiểm tra `>= min_order_amount` cho fixed. |
| C3=Below min + C6=percent | FR09-T-TC02 | Đại diện lỗi ngưỡng; fixed below-min bị loại vì cùng action A5. |
| C1=Active exists + C2=Expired | FR09-E-TC01 | Coupon tồn tại nhưng hết hạn. |
| C1=Active exists + C4=No JWT | FR09-A-TC01 | Coupon hợp lệ nhưng user chưa đăng nhập. |
| C1=Active exists + C5=Reached max | FR09-U-TC01 | Coupon hợp lệ nhưng hết lượt sử dụng. |
| C1=Missing/inactive + C4=JWT valid | FR09-C-TC01 | User hợp lệ nhưng mã không hợp lệ. |
| C1=Empty + C4=JWT valid | FR09-C-TC02 | Validate input rỗng. |

## Generated Test Cases

| TC ID | Rule ID | Technique | File | Expected Status | Status / Related bugs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| FR09-P-TC01 | R01 | Decision Table / Pairwise | `tests/test-cases/coupon_application/FR09-P-TC01.md` | Accepted | Failed / BUG-FR09-P-01 - Công thức giảm giá percent tính sai `discount_amount` |
| FR09-F-TC01 | R02 | Decision Table / Pairwise | `tests/test-cases/coupon_application/FR09-F-TC01.md` | Accepted | Passed / None |
| FR09-T-TC01 | R03 | Decision Table / Pairwise | `tests/test-cases/coupon_application/FR09-T-TC01.md` | Accepted | Failed / BUG-FR09-T-01 - Hệ thống từ chối đơn hàng bằng đúng ngưỡng tối thiểu |
| FR09-T-TC03 | R04 | Decision Table / Pairwise | `tests/test-cases/coupon_application/FR09-T-TC03.md` | Accepted | Failed / BUG-FR09-T-01 - Hệ thống từ chối đơn hàng bằng đúng ngưỡng tối thiểu |
| FR09-C-TC01 | R05 | Decision Table | `tests/test-cases/coupon_application/FR09-C-TC01.md` | Rejected | Passed / None |
| FR09-C-TC02 | R06 | Decision Table | `tests/test-cases/coupon_application/FR09-C-TC02.md` | Rejected | Passed / None |
| FR09-E-TC01 | R07 | Decision Table | `tests/test-cases/coupon_application/FR09-E-TC01.md` | Rejected | Passed / None |
| FR09-T-TC02 | R08 | Decision Table | `tests/test-cases/coupon_application/FR09-T-TC02.md` | Rejected | Passed / None |
| FR09-A-TC01 | R09 | Decision Table | `tests/test-cases/coupon_application/FR09-A-TC01.md` | Rejected | Failed / BUG-FR09-A-01 - API áp dụng coupon không yêu cầu JWT hợp lệ |
| FR09-U-TC01 | R10 | Decision Table | `tests/test-cases/coupon_application/FR09-U-TC01.md` | Rejected | Passed / None |

## Execution Result Summary

| Total TC | Passed | Failed | Bug IDs |
| ---: | ---: | ---: | :--- |
| 10 | 6 | 4 | `BUG-FR09-P-01`, `BUG-FR09-T-01`, `BUG-FR09-A-01` |

## Generated Test Run

| Artifact | Path |
| :--- | :--- |
| Test run | `tests/test-runs/fr09-coupon-application-test-run.md` |

## AI Steps Log

1. Đọc `.agents/skills/decision-table-pairwise-testing/SKILL.md` để áp dụng quy trình Decision Table + Pairwise.
2. Đọc `README.md` phần FR-09 để trích 5 điều kiện bắt buộc và công thức tính giảm giá.
3. Đọc `api_specification.md`, `backend/database.js`, `backend/server.js`, và `frontend-web/src/pages/Checkout.jsx` để xác định endpoint, dữ liệu seed, schema, UI flow, và implementation evidence.
4. Xác định 6 condition kiểm thử: 5 condition của FR-09 và thêm `discount type` vì ảnh hưởng expected amount.
5. Dựng decision table chuẩn hóa từ full matrix thô 144 tổ hợp.
6. Rút gọn bằng cách giữ rule invalid bắt buộc riêng lẻ và áp dụng Pairwise cho các cặp condition-value rủi ro cao.
7. Sinh 10 file testcase Markdown trong `tests/test-cases/coupon_application/`.
8. Sinh file test run template tại `tests/test-runs/fr09-coupon-application-test-run.md`.
9. Ghi summary tại `tests/test-summary/fr09-coupon_application-decision-table-summary.md`.
10. Đọc lại artifact sau khi sinh để kiểm tra heading, trạng thái mặc định, đường dẫn, test run, và rationale.
11. Chạy 10 testcase FR-09 qua `POST /api/apply-coupon` trên backend `http://localhost:3000`.
12. Cập nhật test run với tester `Đặng Trường Nguyên`, ngày `29/06/2026`, kết quả `6 Passed / 4 Failed`, và Defect Log.
13. Đồng bộ `Status / Related bugs` trong từng file testcase FR-09.
14. Tạo 3 bug report dưới `tests/bug/FR-09/`.
15. Chạy cross-check test-run với testcase status và xác nhận `10` rows, `0` mismatches.

## Assumptions / Open Questions

- Test đã chạy qua API backend local `http://localhost:3000` vào ngày `29/06/2026`.
- `POST /api/apply-coupon` được xem là hành vi áp dụng mã tại Checkout theo API spec và UI Checkout hiện có.
- Với C1 false, testcase dùng `NOTFOUND` để đại diện cho mã không tồn tại; mã inactive có cùng expected action nên không sinh thêm testcase riêng.
- Các biến fail như expired, below-min, anonymous, reached-max được giữ riêng để tránh một lỗi che lấp lỗi khác; các biến don't-care còn lại không được nhân full matrix.
- Các lỗi thực tế đã xác nhận nằm ở `>= min_order_amount`, JWT bắt buộc, và công thức `percent`.
