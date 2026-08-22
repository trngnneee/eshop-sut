# Traceability Matrix: Requirement - Test Case - Bug
Bảng truy vết giúp đảm bảo độ bao phủ của kiểm thử và theo dõi trạng thái các lỗi tương ứng.

| Requirement | Test Case | Result | Bug Issue | Status |
| :--- | :--- | :--- | :--- | :--- |
| FR-02 (Authentication) | [TC-LOGIN-001](../test-cases/login/TC-LOGIN-001.md) | Pass | None | Done |
| FR-02 (Authentication) | [TC-LOGIN-002](../test-cases/login/TC-LOGIN-002.md) | Fail | #1, #3 | Open |
| FR-02 (Authentication) | [TC-LOGIN-003](../test-cases/login/TC-LOGIN-003.md) | Fail | #2 | Open |
| FR-21, FR-22 (GUI/Form) | [TC-LOGIN-004](../test-cases/login/TC-LOGIN-004.md) | Fail | #4, #5, #6, #7, #8 | Open |
| FR-02, FR-22 (Validation) | [TC-LOGIN-005](../test-cases/login/TC-LOGIN-005.md) | Fail | #9 | Open |
| FR-02 (Auth Token) | [TC-LOGIN-006](../test-cases/login/TC-LOGIN-006.md) | Pass | None | Done |
| SEC-05 (Security SQLi) | [TC-LOGIN-007](../test-cases/login/TC-LOGIN-007.md) | Pass | None | Done |
| SEC-02 (Security Rate) | [TC-LOGIN-008](../test-cases/login/TC-LOGIN-008.md) | Fail | #10 | Open |
| FR-21, FR-24 (UI/UX) | [TC-LOGIN-009](../test-cases/login/TC-LOGIN-009.md) | Fail | #11 | Open |
| FR-22 (UI/UX) | [TC-LOGIN-010](../test-cases/login/TC-LOGIN-010.md) | Fail | #12 | Open |
| SEC-02 (Session) | [TC-LOGIN-011](../test-cases/login/TC-LOGIN-011.md) | Fail | #13 | Open |
| FR-23 (Session Guard) | [TC-LOGIN-012](../test-cases/login/TC-LOGIN-012.md) | Fail | #14 | Open |
| FR-02 (OAuth) | [TC-LOGIN-013](../test-cases/login/TC-LOGIN-013.md) | Fail | #15 | Open |

## HW06 — API Testing

| Requirement | Test Case | Result | Bug Issue | Status |
| :--- | :--- | :--- | :--- | :--- |
| FR-02 | `TC-API-LOGIN-001` | Pass/Smoke | None | Covered |
| FR-02 | `TC-API-LOGIN-002` | Pass/Smoke | None | Covered |
| FR-02 | `TC-API-LOGIN-003` | Pass/Smoke | None | Covered |
| FR-02 | `TC-API-LOGIN-004` | Fail | D-LOGIN-08 / chưa tạo issue | Open |
| FR-02 | `TC-API-LOGIN-005` | Fail | D-LOGIN-08 / chưa tạo issue | Open |
| FR-02 | `TC-API-LOGIN-006` | Fail | D-LOGIN-08 / chưa tạo issue | Open |
| FR-02 | `TC-API-LOGIN-007` | Pass/Smoke | None | Covered |
| FR-02 | `TC-API-LOGIN-008` | Pass/Smoke | None | Covered |
| FR-02 | `TC-API-LOGIN-009` | Pass/Smoke | None | Covered |
| FR-02 | `TC-API-LOGIN-010` | Fail | D-LOGIN-08 / chưa tạo issue | Open |
| FR-02 | `TC-API-LOGIN-011` | Fail | D-LOGIN-08 / chưa tạo issue | Open |
| FR-02 | `TC-API-LOGIN-012` | Fail | D-LOGIN-08 / chưa tạo issue | Open |
| FR-02 | `TC-API-LOGIN-013` | Fail | D-LOGIN-08 / chưa tạo issue | Open |
| FR-02 | `TC-API-LOGIN-014` | Fail | D-LOGIN-08 / chưa tạo issue | Open |
| FR-02 | `TC-API-LOGIN-015` | Pass/Smoke | None | Covered |
| FR-02 | `TC-API-LOGIN-016` | Pass/Smoke | None | Covered |
| FR-02 | `TC-API-LOGIN-017` | Fail | [D-LOGIN-01 #413](https://github.com/trngnneee/eshop-sut/issues/413) | Open |
| FR-02 | `TC-API-LOGIN-018` | Pass/Smoke | [D-LOGIN-01 #413](https://github.com/trngnneee/eshop-sut/issues/413) | Open |
| FR-02 | `TC-API-LOGIN-019` | Fail | [D-LOGIN-01 #413](https://github.com/trngnneee/eshop-sut/issues/413) | Open |
| FR-02 | `TC-API-LOGIN-020` | Fail | D-LOGIN-07 / chưa tạo issue | Open |
| FR-02 | `TC-API-LOGIN-021` | Pass/Smoke | None | Covered |
| FR-02 | `TC-API-LOGIN-022` | Fail | [D-LOGIN-02 #414](https://github.com/trngnneee/eshop-sut/issues/414) | Open |
| FR-02 | `TC-API-LOGIN-023` | Fail | [D-LOGIN-01 #413](https://github.com/trngnneee/eshop-sut/issues/413) | Open |
| FR-02 | `TC-API-LOGIN-024` | Blocked | [D-LOGIN-01 #413](https://github.com/trngnneee/eshop-sut/issues/413) | Blocked — D-LOGIN-01 chặn tiền đề TC-023 |
| SEC-05 | `TC-API-LOGIN-025` | Pass/Smoke | None | Covered |
| SEC-05 | `TC-API-LOGIN-026` | Pass/Smoke | None | Covered |
| SEC-04 | `TC-API-LOGIN-027` | Pass/Smoke | None | Covered |
| SEC-01 | `TC-API-LOGIN-028` | Fail | [D-LOGIN-03 #415](https://github.com/trngnneee/eshop-sut/issues/415) | Open |
| SEC-01 | `TC-API-LOGIN-029` | Fail | [D-LOGIN-03 #415](https://github.com/trngnneee/eshop-sut/issues/415) | Open |
| SEC-03 | `TC-API-LOGIN-030` | Pass/Smoke | None | Covered |
| SEC-02 | `TC-API-LOGIN-031` | Pass/Smoke | None | Covered |
| FR-02 | `TC-API-LOGIN-032` | Fail | D-LOGIN-07 / chưa tạo issue | Open |
| FR-02 | `TC-API-LOGIN-033` | Pass/Smoke | None | Covered |
| FR-02 | `TC-API-LOGIN-034` | Pass/Smoke | None | Covered |
| FR-02 | `TC-API-LOGIN-035` | Pass/Smoke | None | Covered |
| SEC-01 | `TC-API-LOGIN-036` | Fail | [D-LOGIN-03 #415](https://github.com/trngnneee/eshop-sut/issues/415) | Open |
| FR-02 | `TC-API-LOGIN-037` | Fail | [D-LOGIN-01 #413](https://github.com/trngnneee/eshop-sut/issues/413) | Open |
| FR-02 | `TC-API-LOGIN-038` | Fail | [D-LOGIN-02 #414](https://github.com/trngnneee/eshop-sut/issues/414) | Open |
| SEC-01 | `TC-API-LOGIN-039` | Fail | [D-LOGIN-03 #415](https://github.com/trngnneee/eshop-sut/issues/415) | Open |
| SEC-02 | `TC-API-LOGIN-040` | Fail | [D-LOGIN-05 #416](https://github.com/trngnneee/eshop-sut/issues/416) | Open |
| FR-02 | `TC-API-LOGIN-041` | Not Run | [D-LOGIN-06 #417](https://github.com/trngnneee/eshop-sut/issues/417) | Manual — chờ lock thật 180s, tách khỏi regression tự động |
| SEC-02 | `TC-API-LOGIN-042` | Blocked | [D-LOGIN-05 #416](https://github.com/trngnneee/eshop-sut/issues/416) | Blocked — không nhúng signing secret vào artifact công khai |
| FR-08/FR-10 | `TC-API-CHECKOUT-001` | Fail | [D-CHK-01 #418](https://github.com/trngnneee/eshop-sut/issues/418) | Open |
| FR-08/FR-10 | `TC-API-CHECKOUT-002` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-003` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-004` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-005` | Fail | [D-CHK-02 #419](https://github.com/trngnneee/eshop-sut/issues/419) | Open |
| FR-08/FR-10 | `TC-API-CHECKOUT-006` | Fail | [D-CHK-02 #419](https://github.com/trngnneee/eshop-sut/issues/419) | Open |
| FR-08/FR-10 | `TC-API-CHECKOUT-007` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-008` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-009` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-010` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-011` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-012` | Fail | D-CHK-05 / chưa tạo issue | Open |
| FR-08/FR-10 | `TC-API-CHECKOUT-013` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-014` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-015` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-016` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-017` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-018` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-019` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-020` | Fail | [D-CHK-03 #420](https://github.com/trngnneee/eshop-sut/issues/420) | Open |
| FR-08/FR-10 | `TC-API-CHECKOUT-021` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-022` | Fail | [D-CHK-04 #421](https://github.com/trngnneee/eshop-sut/issues/421) | Open |
| FR-08/FR-10 | `TC-API-CHECKOUT-023` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-024` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-025` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-026` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-027` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-028` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-029` | Blocked | — | Blocked — SUT phát JWT không có exp, không có signing fixture an toàn |
| FR-08/FR-10 | `TC-API-CHECKOUT-030` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-031` | Fail | [D-CHK-07 #422](https://github.com/trngnneee/eshop-sut/issues/422) | Open |
| FR-08/FR-10 | `TC-API-CHECKOUT-032` | Fail | D-CHK-05 / chưa tạo issue | Open |
| FR-08/FR-10 | `TC-API-CHECKOUT-033` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-034` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-035` | Pass/Smoke | None | Covered |
| FR-08/FR-10 | `TC-API-CHECKOUT-036` | Pass/Smoke | None | Covered |
| FR-08/FR-10/SEC-02/SEC-04 | `TC-API-CHECKOUT-037` | Fail | [D-CHK-01 #418](https://github.com/trngnneee/eshop-sut/issues/418) | Open |
| FR-08/FR-10/SEC-02/SEC-04 | `TC-API-CHECKOUT-038` | Fail | [D-CHK-02 #419](https://github.com/trngnneee/eshop-sut/issues/419) | Open |
| FR-08/FR-10/SEC-02/SEC-04 | `TC-API-CHECKOUT-039` | Fail | [D-CHK-03 #420](https://github.com/trngnneee/eshop-sut/issues/420) | Open |
| FR-08/FR-10/SEC-02/SEC-04 | `TC-API-CHECKOUT-040` | Fail | [D-CHK-04 #421](https://github.com/trngnneee/eshop-sut/issues/421) | Open |
| FR-08/FR-10/SEC-02/SEC-04 | `TC-API-CHECKOUT-041` | Fail | [D-CHK-07 #422](https://github.com/trngnneee/eshop-sut/issues/422) | Open |
| FR-08/FR-10/SEC-02/SEC-04 | `TC-API-CHECKOUT-042` | Fail | D-CHK-05 / chưa tạo issue | Open |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-001` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-002` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-003` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-004` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-005` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-006` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-007` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-008` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-009` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-010` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-011` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-012` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-013` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-014` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-015` | Fail | [D-ADM-03 #425](https://github.com/trngnneee/eshop-sut/issues/425) | Open |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-016` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-017` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-018` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-019` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-020` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-021` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-022` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-023` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-024` | Fail | [D-ADM-02 #424](https://github.com/trngnneee/eshop-sut/issues/424) | Open |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-025` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-026` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-027` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-028` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-029` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-030` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-031` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-032` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-033` | Fail | [D-ADM-01 #423](https://github.com/trngnneee/eshop-sut/issues/423) | Open |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-034` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-035` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-036` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-037` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-038` | Pass/Smoke | None | Covered |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-039` | Fail | [D-ADM-01 #423](https://github.com/trngnneee/eshop-sut/issues/423) | Open |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-040` | Fail | [D-ADM-01 #423](https://github.com/trngnneee/eshop-sut/issues/423) | Open |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-041` | Blocked | [D-ADM-02 #424](https://github.com/trngnneee/eshop-sut/issues/424) | Blocked — SUT không có Dashboard/revenue API để quan sát hậu điều kiện |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-042` | Fail | [D-ADM-03 #425](https://github.com/trngnneee/eshop-sut/issues/425) | Open |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-043` | Fail | [D-ADM-08 #427](https://github.com/trngnneee/eshop-sut/issues/427) | Open |
| FR-10/FR-12/FR-18 | `TC-API-ORDER-STATUS-044` | Fail | D-ADM-06 / chưa tạo issue | Open |
