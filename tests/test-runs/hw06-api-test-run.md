# HW06 API test run

> Bảng theo format `Rule.pdf` §H.6 — mỗi dòng là một test case. Sinh bằng `hw06/tooling/build_test_run.py` từ `execution-coverage.md` (nguồn Executed) và `traceability-matrix.md` (nguồn Requirement/Bug). Không có số liệu nhập tay.

**Tester:** 23127207 · **Môi trường:** `http://127.0.0.1:3001` · **Runner:** Newman (`hw06/newman/run-newman.ps1`)

**Tổng 128 test case** — Pass: 80 · Fail: 43 · Blocked: 4 · Not Run: 1

Mọi dòng `Fail`/`Blocked` đều có Related Bug hoặc lý do rõ ràng theo §H.6. Các dòng `Blocked`/`Not Run` là test case đã thiết kế nhưng chưa có assertion Newman — lý do ghi ở cột Note, không suy diễn kết quả Pass/Fail.

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `TC-API-CHECKOUT-001` | api-checkout | 23127207 | Fail | [#418](https://github.com/trngnneee/eshop-sut/issues/418) (D-CHK-01) | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-002` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-003` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-004` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-005` | api-checkout | 23127207 | Fail | [#419](https://github.com/trngnneee/eshop-sut/issues/419) (D-CHK-02) | FR-08/FR-10 · `00-canary-suite`, `00-ddt-status-prep`, `00-full-suite`, `00-off-suite`, `02-ddt-checkout` |
| `TC-API-CHECKOUT-006` | api-checkout | 23127207 | Fail | [#419](https://github.com/trngnneee/eshop-sut/issues/419) (D-CHK-02) | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-007` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-008` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-009` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-010` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-011` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-012` | api-checkout | 23127207 | Fail | [#431](https://github.com/trngnneee/eshop-sut/issues/431) (D-CHK-05) | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-013` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-014` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-015` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-016` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-017` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-018` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-019` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-020` | api-checkout | 23127207 | Fail | [#420](https://github.com/trngnneee/eshop-sut/issues/420) (D-CHK-03) | FR-08/FR-10 · `00-canary-suite`, `00-ddt-status-prep`, `00-full-suite`, `00-off-suite`, `02-ddt-checkout` |
| `TC-API-CHECKOUT-021` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-022` | api-checkout | 23127207 | Fail | [#421](https://github.com/trngnneee/eshop-sut/issues/421) (D-CHK-04) | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-023` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-024` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-025` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-026` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-027` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-028` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-029` | api-checkout | 23127207 | Blocked | — | SUT phát JWT không có exp và không cung cấp signing fixture an toàn, nên không thể tạo token hợp lệ nhưng đã hết hạn mà không sao chép secret vào artifact. |
| `TC-API-CHECKOUT-030` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-031` | api-checkout | 23127207 | Fail | [#422](https://github.com/trngnneee/eshop-sut/issues/422) (D-CHK-07) | FR-08/FR-10 · `00-canary-suite`, `00-ddt-status-prep`, `00-full-suite`, `00-off-suite`, `02-ddt-checkout` |
| `TC-API-CHECKOUT-032` | api-checkout | 23127207 | Fail | [#431](https://github.com/trngnneee/eshop-sut/issues/431) (D-CHK-05) | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-033` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-034` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-035` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-036` | api-checkout | 23127207 | Pass | — | FR-08/FR-10 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-037` | api-checkout | 23127207 | Fail | [#418](https://github.com/trngnneee/eshop-sut/issues/418) (D-CHK-01) | FR-08/FR-10/SEC-02/SEC-04 · `00-canary-suite`, `00-ddt-status-prep`, `00-full-suite`, `00-off-suite`, `02-ddt-checkout` |
| `TC-API-CHECKOUT-038` | api-checkout | 23127207 | Fail | [#419](https://github.com/trngnneee/eshop-sut/issues/419) (D-CHK-02) | FR-08/FR-10/SEC-02/SEC-04 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-039` | api-checkout | 23127207 | Fail | [#420](https://github.com/trngnneee/eshop-sut/issues/420) (D-CHK-03) | FR-08/FR-10/SEC-02/SEC-04 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-040` | api-checkout | 23127207 | Fail | [#421](https://github.com/trngnneee/eshop-sut/issues/421) (D-CHK-04) | FR-08/FR-10/SEC-02/SEC-04 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-041` | api-checkout | 23127207 | Fail | [#422](https://github.com/trngnneee/eshop-sut/issues/422) (D-CHK-07) | FR-08/FR-10/SEC-02/SEC-04 · `02-ddt-checkout` |
| `TC-API-CHECKOUT-042` | api-checkout | 23127207 | Fail | [#431](https://github.com/trngnneee/eshop-sut/issues/431) (D-CHK-05) | FR-08/FR-10/SEC-02/SEC-04 · `02-ddt-checkout` |
| `TC-API-LOGIN-001` | api-login | 23127207 | Pass | — | FR-02 · `00-canary-suite`, `00-full-suite`, `00-off-suite`, `01-ddt-login` |
| `TC-API-LOGIN-002` | api-login | 23127207 | Pass | — | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-003` | api-login | 23127207 | Pass | — | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-004` | api-login | 23127207 | Fail | [#430](https://github.com/trngnneee/eshop-sut/issues/430) (D-LOGIN-08) | FR-02 · `00-canary-suite`, `00-full-suite`, `00-off-suite`, `01-ddt-login` |
| `TC-API-LOGIN-005` | api-login | 23127207 | Fail | [#430](https://github.com/trngnneee/eshop-sut/issues/430) (D-LOGIN-08) | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-006` | api-login | 23127207 | Fail | [#430](https://github.com/trngnneee/eshop-sut/issues/430) (D-LOGIN-08) | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-007` | api-login | 23127207 | Pass | — | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-008` | api-login | 23127207 | Pass | — | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-009` | api-login | 23127207 | Pass | — | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-010` | api-login | 23127207 | Fail | [#430](https://github.com/trngnneee/eshop-sut/issues/430) (D-LOGIN-08) | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-011` | api-login | 23127207 | Fail | [#430](https://github.com/trngnneee/eshop-sut/issues/430) (D-LOGIN-08) | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-012` | api-login | 23127207 | Fail | [#430](https://github.com/trngnneee/eshop-sut/issues/430) (D-LOGIN-08) | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-013` | api-login | 23127207 | Fail | [#430](https://github.com/trngnneee/eshop-sut/issues/430) (D-LOGIN-08) | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-014` | api-login | 23127207 | Fail | [#430](https://github.com/trngnneee/eshop-sut/issues/430) (D-LOGIN-08) | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-015` | api-login | 23127207 | Pass | — | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-016` | api-login | 23127207 | Pass | — | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-017` | api-login | 23127207 | Fail | [#413](https://github.com/trngnneee/eshop-sut/issues/413) (D-LOGIN-01) | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-018` | api-login | 23127207 | Pass | [#413](https://github.com/trngnneee/eshop-sut/issues/413) (D-LOGIN-01) | FR-02 · `00-canary-suite`, `00-full-suite`, `00-off-suite`, `01-ddt-login` |
| `TC-API-LOGIN-019` | api-login | 23127207 | Fail | [#413](https://github.com/trngnneee/eshop-sut/issues/413) (D-LOGIN-01) | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-020` | api-login | 23127207 | Fail | [#429](https://github.com/trngnneee/eshop-sut/issues/429) (D-LOGIN-07) | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-021` | api-login | 23127207 | Pass | — | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-022` | api-login | 23127207 | Fail | [#414](https://github.com/trngnneee/eshop-sut/issues/414) (D-LOGIN-02) | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-023` | api-login | 23127207 | Fail | [#413](https://github.com/trngnneee/eshop-sut/issues/413) (D-LOGIN-01) | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-024` | api-login | 23127207 | Blocked | [#413](https://github.com/trngnneee/eshop-sut/issues/413) (D-LOGIN-01) | Tiền điều kiện yêu cầu TC-023 đăng nhập thành công sau hai lần sai, nhưng D-LOGIN-01 khóa tài khoản sớm nên không thể đi tới trạng thái reset cần kiểm thử. |
| `TC-API-LOGIN-025` | api-login | 23127207 | Pass | — | SEC-05 · `00-canary-suite`, `00-full-suite`, `00-off-suite`, `01-ddt-login` |
| `TC-API-LOGIN-026` | api-login | 23127207 | Pass | — | SEC-05 · `01-ddt-login` |
| `TC-API-LOGIN-027` | api-login | 23127207 | Pass | — | SEC-04 · `01-ddt-login` |
| `TC-API-LOGIN-028` | api-login | 23127207 | Fail | [#415](https://github.com/trngnneee/eshop-sut/issues/415) (D-LOGIN-03) | SEC-01 · `00-canary-suite`, `00-full-suite`, `00-off-suite`, `01-ddt-login` |
| `TC-API-LOGIN-029` | api-login | 23127207 | Fail | [#415](https://github.com/trngnneee/eshop-sut/issues/415) (D-LOGIN-03) | SEC-01 · `01-ddt-login` |
| `TC-API-LOGIN-030` | api-login | 23127207 | Pass | — | SEC-03 · `01-ddt-login` |
| `TC-API-LOGIN-031` | api-login | 23127207 | Pass | — | SEC-02 · `01-ddt-login` |
| `TC-API-LOGIN-032` | api-login | 23127207 | Fail | [#429](https://github.com/trngnneee/eshop-sut/issues/429) (D-LOGIN-07) | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-033` | api-login | 23127207 | Pass | — | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-034` | api-login | 23127207 | Pass | — | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-035` | api-login | 23127207 | Pass | — | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-036` | api-login | 23127207 | Fail | [#415](https://github.com/trngnneee/eshop-sut/issues/415) (D-LOGIN-03) | SEC-01 · `01-ddt-login` |
| `TC-API-LOGIN-037` | api-login | 23127207 | Fail | [#413](https://github.com/trngnneee/eshop-sut/issues/413) (D-LOGIN-01) | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-038` | api-login | 23127207 | Fail | [#414](https://github.com/trngnneee/eshop-sut/issues/414) (D-LOGIN-02) | FR-02 · `01-ddt-login` |
| `TC-API-LOGIN-039` | api-login | 23127207 | Fail | [#415](https://github.com/trngnneee/eshop-sut/issues/415) (D-LOGIN-03) | SEC-01 · `01-ddt-login` |
| `TC-API-LOGIN-040` | api-login | 23127207 | Fail | [#416](https://github.com/trngnneee/eshop-sut/issues/416) (D-LOGIN-05) | SEC-02 · `01-ddt-login` |
| `TC-API-LOGIN-041` | api-login | 23127207 | Not Run | [#417](https://github.com/trngnneee/eshop-sut/issues/417) (D-LOGIN-06) | Phải chờ lock thực tế 180 giây rồi kiểm tra residual state; tách khỏi regression tự động để tránh một iteration kéo dài và dễ nhiễu thời gian. |
| `TC-API-LOGIN-042` | api-login | 23127207 | Blocked | [#416](https://github.com/trngnneee/eshop-sut/issues/416) (D-LOGIN-05) | Cần ký JWT bằng secret của SUT; không nhúng signing secret hoặc forged token vào collection/report công khai. |
| `TC-API-ORDER-STATUS-001` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-002` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `00-canary-suite`, `00-full-suite`, `00-off-suite`, `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-003` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-004` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-005` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-006` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-007` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-008` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-009` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-010` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-011` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-012` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-013` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-014` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-015` | api-order-status | 23127207 | Fail | [#425](https://github.com/trngnneee/eshop-sut/issues/425) (D-ADM-03) | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-016` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-017` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-018` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-019` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-020` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-021` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-022` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-023` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-024` | api-order-status | 23127207 | Fail | [#424](https://github.com/trngnneee/eshop-sut/issues/424) (D-ADM-02) | FR-10/FR-12/FR-18 · `00-canary-suite`, `00-full-suite`, `00-off-suite`, `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-025` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-026` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-027` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-028` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-029` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-030` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-031` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-032` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-033` | api-order-status | 23127207 | Fail | [#423](https://github.com/trngnneee/eshop-sut/issues/423) (D-ADM-01) | FR-10/FR-12/FR-18 · `00-canary-suite`, `00-full-suite`, `00-off-suite`, `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-034` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-035` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-036` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-037` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-038` | api-order-status | 23127207 | Pass | — | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-039` | api-order-status | 23127207 | Fail | [#423](https://github.com/trngnneee/eshop-sut/issues/423) (D-ADM-01) | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-040` | api-order-status | 23127207 | Fail | [#423](https://github.com/trngnneee/eshop-sut/issues/423) (D-ADM-01) | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-041` | api-order-status | 23127207 | Blocked | [#424](https://github.com/trngnneee/eshop-sut/issues/424) (D-ADM-02) | SUT không có Dashboard/revenue API để quan sát hậu điều kiện doanh thu; transition canceled→delivered được phủ riêng bởi TC-024. |
| `TC-API-ORDER-STATUS-042` | api-order-status | 23127207 | Fail | [#425](https://github.com/trngnneee/eshop-sut/issues/425) (D-ADM-03) | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-043` | api-order-status | 23127207 | Fail | [#427](https://github.com/trngnneee/eshop-sut/issues/427) (D-ADM-08) | FR-10/FR-12/FR-18 · `03-ddt-order-status` |
| `TC-API-ORDER-STATUS-044` | api-order-status | 23127207 | Fail | [#432](https://github.com/trngnneee/eshop-sut/issues/432) (D-ADM-06) | FR-10/FR-12/FR-18 · `03-ddt-order-status` |

## Tổng hợp theo suite

| Suite | Iterations | Requests | Assertions | Failed | Result |
| :--- | ---: | ---: | ---: | ---: | :--- |
| `00-off-suite` | 1 | 19 | 18 | 0 | PASS |
| `00-canary-suite` | 1 | 19 | 19 | 1 | FAIL (expected defect/oracle mismatch) |
| `00-full-suite` | 1 | 19 | 26 | 8 | FAIL (expected defect/oracle mismatch) |
| `01-ddt-login` | 39 | 89 | 39 | 23 | FAIL (expected defect/oracle mismatch) |
| `02-ddt-checkout` | 41 | 178 | 41 | 17 | FAIL (expected defect/oracle mismatch) |
| `03-ddt-order-status` | 43 | 127 | 43 | 7 | FAIL (expected defect/oracle mismatch) |

Canary run trên GitHub Actions: `TC-API-LOGIN-018` → D-LOGIN-01 ([run #32231020920](https://github.com/trngnneee/eshop-sut/actions/runs/32231020920)).
Mọi request đều gửi `X-Student-Id: 23127207`; report gốc ở `hw06/newman/reports/`.
