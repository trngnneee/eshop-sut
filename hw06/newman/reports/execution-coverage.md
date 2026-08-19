# HW06 Newman execution coverage

> Nguồn duy nhất cho cột Executed là TC ID xuất hiện trong tên assertion của các file Newman JSON thật. Dòng có trong data file/collection nhưng không có assertion không được tính.

## Summary

| Metric | Value |
| :--- | ---: |
| Final test cases | 128 |
| Executed by Newman assertion | 123 |
| Execution coverage | 96.1% |
| Manual | 1 |
| Blocked | 4 |
| Unclassified gap | 0 |

| API | Final | Executed | Coverage |
| :--- | ---: | ---: | ---: |
| API-1 | 42 | 39 | 92.9% |
| API-2 | 42 | 41 | 97.6% |
| API-3 | 44 | 43 | 97.7% |

Parsed Newman suites (8): `00-canary-suite`, `00-ddt-setup`, `00-ddt-status-prep`, `00-full-suite`, `00-off-suite`, `01-ddt-login`, `02-ddt-checkout`, `03-ddt-order-status`.

## Reconciliation

| TC ID | Executed? | Suite | Assertion result |
| :--- | :---: | :--- | :--- |
| TC-API-LOGIN-001 | Yes | `00-canary-suite`, `00-full-suite`, `00-off-suite`, `01-ddt-login` | `00-canary-suite`: PASS; `00-full-suite`: PASS; `00-off-suite`: PASS; `01-ddt-login`: PASS |
| TC-API-LOGIN-002 | Yes | `01-ddt-login` | `01-ddt-login`: PASS |
| TC-API-LOGIN-003 | Yes | `01-ddt-login` | `01-ddt-login`: PASS |
| TC-API-LOGIN-004 | Yes | `00-canary-suite`, `00-full-suite`, `00-off-suite`, `01-ddt-login` | `00-canary-suite`: PASS; `00-full-suite`: FAIL — expected response to have status code 400 but got 401; `00-off-suite`: PASS; `01-ddt-login`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-LOGIN-005 | Yes | `01-ddt-login` | `01-ddt-login`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-LOGIN-006 | Yes | `01-ddt-login` | `01-ddt-login`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-LOGIN-007 | Yes | `01-ddt-login` | `01-ddt-login`: PASS |
| TC-API-LOGIN-008 | Yes | `01-ddt-login` | `01-ddt-login`: PASS |
| TC-API-LOGIN-009 | Yes | `01-ddt-login` | `01-ddt-login`: PASS |
| TC-API-LOGIN-010 | Yes | `01-ddt-login` | `01-ddt-login`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-LOGIN-011 | Yes | `01-ddt-login` | `01-ddt-login`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-LOGIN-012 | Yes | `01-ddt-login` | `01-ddt-login`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-LOGIN-013 | Yes | `01-ddt-login` | `01-ddt-login`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-LOGIN-014 | Yes | `01-ddt-login` | `01-ddt-login`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-LOGIN-015 | Yes | `01-ddt-login` | `01-ddt-login`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-LOGIN-016 | Yes | `01-ddt-login` | `01-ddt-login`: PASS |
| TC-API-LOGIN-017 | Yes | `01-ddt-login` | `01-ddt-login`: FAIL — expected 2 to deeply equal 1 |
| TC-API-LOGIN-018 | Yes | `00-canary-suite`, `00-full-suite`, `00-off-suite`, `01-ddt-login` | `00-canary-suite`: FAIL — expected response to have status code 200 but got 403; `00-full-suite`: FAIL — expected response to have status code 200 but got 403; `00-off-suite`: PASS; `01-ddt-login`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-LOGIN-019 | Yes | `01-ddt-login` | `01-ddt-login`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-LOGIN-020 | Yes | `01-ddt-login` | `01-ddt-login`: FAIL — expected 'Tài khoản đã bị khóa. Vui lòng thử lạ…' to deeply equal 'Invalid email or password' |
| TC-API-LOGIN-021 | Yes | `01-ddt-login` | `01-ddt-login`: PASS |
| TC-API-LOGIN-022 | Yes | `01-ddt-login` | `01-ddt-login`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-LOGIN-023 | Yes | `01-ddt-login` | `01-ddt-login`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-LOGIN-024 | No — Blocked | — | Tiền điều kiện yêu cầu TC-023 đăng nhập thành công sau hai lần sai, nhưng D-LOGIN-01 khóa tài khoản sớm nên không thể đi tới trạng thái reset cần kiểm thử. |
| TC-API-LOGIN-025 | Yes | `00-canary-suite`, `00-full-suite`, `00-off-suite`, `01-ddt-login` | `00-canary-suite`: PASS; `00-full-suite`: PASS; `00-off-suite`: PASS; `01-ddt-login`: PASS |
| TC-API-LOGIN-026 | Yes | `01-ddt-login` | `01-ddt-login`: PASS |
| TC-API-LOGIN-027 | Yes | `01-ddt-login` | `01-ddt-login`: PASS |
| TC-API-LOGIN-028 | Yes | `00-canary-suite`, `00-full-suite`, `00-off-suite`, `01-ddt-login` | `00-canary-suite`: PASS; `00-full-suite`: FAIL — expected '<redacted-user-password>' to be undefined; `00-off-suite`: PASS; `01-ddt-login`: FAIL — expected false to deeply equal true |
| TC-API-LOGIN-029 | Yes | `01-ddt-login` | `01-ddt-login`: FAIL — expected false to deeply equal true |
| TC-API-LOGIN-030 | Yes | `01-ddt-login` | `01-ddt-login`: PASS |
| TC-API-LOGIN-031 | Yes | `01-ddt-login` | `01-ddt-login`: PASS |
| TC-API-LOGIN-032 | Yes | `01-ddt-login` | `01-ddt-login`: FAIL — expected 'Tài khoản đã bị khóa. Vui lòng thử lạ…' to deeply equal 'Invalid email or password' |
| TC-API-LOGIN-033 | Yes | `01-ddt-login` | `01-ddt-login`: PASS |
| TC-API-LOGIN-034 | Yes | `01-ddt-login` | `01-ddt-login`: PASS |
| TC-API-LOGIN-035 | Yes | `01-ddt-login` | `01-ddt-login`: PASS |
| TC-API-LOGIN-036 | Yes | `01-ddt-login` | `01-ddt-login`: FAIL — expected false to deeply equal true |
| TC-API-LOGIN-037 | Yes | `01-ddt-login` | `01-ddt-login`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-LOGIN-038 | Yes | `01-ddt-login` | `01-ddt-login`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-LOGIN-039 | Yes | `01-ddt-login` | `01-ddt-login`: FAIL — expected false to deeply equal true |
| TC-API-LOGIN-040 | Yes | `01-ddt-login` | `01-ddt-login`: FAIL — expected undefined to be a number |
| TC-API-LOGIN-041 | No — Manual | — | Phải chờ lock thực tế 180 giây rồi kiểm tra residual state; tách khỏi regression tự động để tránh một iteration kéo dài và dễ nhiễu thời gian. |
| TC-API-LOGIN-042 | No — Blocked | — | Cần ký JWT bằng secret của SUT; không nhúng signing secret hoặc forged token vào collection/report công khai. |
| TC-API-CHECKOUT-001 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-002 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-003 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-CHECKOUT-004 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-005 | Yes | `00-canary-suite`, `00-ddt-status-prep`, `00-full-suite`, `00-off-suite`, `02-ddt-checkout` | `00-canary-suite`: PASS; `00-ddt-status-prep`: PASS; `00-full-suite`: FAIL — expected response to have status code 400 but got 200; `00-off-suite`: PASS; `02-ddt-checkout`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-CHECKOUT-006 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-CHECKOUT-007 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-CHECKOUT-008 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-CHECKOUT-009 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-010 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-011 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-012 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: FAIL — expected '<img src=x onerror=alert(1)>' to not deeply equal '<img src=x onerror=alert(1)>' |
| TC-API-CHECKOUT-013 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-014 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-015 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-CHECKOUT-016 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-017 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-018 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-019 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-020 | Yes | `00-canary-suite`, `00-ddt-status-prep`, `00-full-suite`, `00-off-suite`, `02-ddt-checkout` | `00-canary-suite`: PASS; `00-ddt-status-prep`: PASS; `00-full-suite`: FAIL — expected [ { id: 1, name: 'Laptop', …(2) } ] to be empty; `00-off-suite`: PASS; `02-ddt-checkout`: FAIL — expected [ Array(1) ] to be empty |
| TC-API-CHECKOUT-021 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-022 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-CHECKOUT-023 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-024 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-025 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-026 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-027 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-028 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-029 | No — Blocked | — | SUT phát JWT không có exp và không cung cấp signing fixture an toàn, nên không thể tạo token hợp lệ nhưng đã hết hạn mà không sao chép secret vào artifact. |
| TC-API-CHECKOUT-030 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-031 | Yes | `00-canary-suite`, `00-ddt-status-prep`, `00-full-suite`, `00-off-suite`, `02-ddt-checkout` | `00-canary-suite`: PASS; `00-ddt-status-prep`: PASS; `00-full-suite`: FAIL — expected [ 401, 403 ] to include 200; `00-off-suite`: PASS; `02-ddt-checkout`: FAIL — expected [ 401, 403 ] to include 200 |
| TC-API-CHECKOUT-032 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: FAIL — expected '<script>alert(1)</script>' to not deeply equal '<script>alert(1)</script>' |
| TC-API-CHECKOUT-033 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-034 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-035 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-036 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: PASS |
| TC-API-CHECKOUT-037 | Yes | `00-canary-suite`, `00-ddt-status-prep`, `00-full-suite`, `00-off-suite`, `02-ddt-checkout` | `00-canary-suite`: PASS; `00-ddt-status-prep`: PASS; `00-full-suite`: PASS; `00-off-suite`: PASS; `02-ddt-checkout`: FAIL — expected 1 to deeply equal 30000000 |
| TC-API-CHECKOUT-038 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-CHECKOUT-039 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: FAIL — expected [ Array(1) ] to be empty |
| TC-API-CHECKOUT-040 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-CHECKOUT-041 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: FAIL — expected [ 401, 403 ] to include 200 |
| TC-API-CHECKOUT-042 | Yes | `02-ddt-checkout` | `02-ddt-checkout`: FAIL — expected '<img src=x onerror=alert(1)>' to not deeply equal '<img src=x onerror=alert(1)>' |
| TC-API-ORDER-STATUS-001 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-002 | Yes | `00-canary-suite`, `00-full-suite`, `00-off-suite`, `03-ddt-order-status` | `00-canary-suite`: PASS; `00-full-suite`: PASS; `00-off-suite`: PASS; `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-003 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-004 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-005 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-006 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-007 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-008 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-009 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-010 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-011 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-012 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-013 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-014 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-015 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-016 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-017 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-018 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-019 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-020 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-021 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-022 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-023 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-024 | Yes | `00-canary-suite`, `00-full-suite`, `00-off-suite`, `03-ddt-order-status` | `00-canary-suite`: PASS; `00-full-suite`: FAIL — expected response to have status code 400 but got 200; `00-off-suite`: PASS; `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-025 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-026 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-027 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-028 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-029 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-030 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-031 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-032 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-033 | Yes | `00-canary-suite`, `00-full-suite`, `00-off-suite`, `03-ddt-order-status` | `00-canary-suite`: PASS; `00-full-suite`: FAIL — expected response to have status code 403 but got 200; `00-off-suite`: PASS; `03-ddt-order-status`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-ORDER-STATUS-034 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-ORDER-STATUS-035 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-036 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-037 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-038 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: PASS |
| TC-API-ORDER-STATUS-039 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-ORDER-STATUS-040 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-ORDER-STATUS-041 | No — Blocked | — | SUT không có Dashboard/revenue API để quan sát hậu điều kiện doanh thu; transition canceled→delivered được phủ riêng bởi TC-024. |
| TC-API-ORDER-STATUS-042 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-ORDER-STATUS-043 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: FAIL — HTTP status follows specification: expected false to deeply equal true |
| TC-API-ORDER-STATUS-044 | Yes | `03-ddt-order-status` | `03-ddt-order-status`: FAIL — expected 'invalid state transition from pending…' to not include 'state transition' |
