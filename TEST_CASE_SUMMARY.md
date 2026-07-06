# EShop Test Case Summary

Ngày tổng hợp: 2026-07-06  
Phạm vi: toàn bộ test case Markdown đang tồn tại trong các folder test hiện tại:

- `tests/domain_bva_testing/`
- `tests/decision_table_testing/`
- `tests/state-transition-testing/FR-10/`
- `tests/use-case-testing/FR-10/`

## Nguồn đã đọc

- Domain/BVA test cases: `tests/domain_bva_testing/test-cases/**/*.md`
- Domain/BVA test runs: `tests/domain_bva_testing/test-runs/*.md`
- Decision Table test cases: `tests/decision_table_testing/test-cases/**/*.md`
- Decision Table test run: `tests/decision_table_testing/test-runs/fr09-coupon-application-test-run.md`
- Decision Table summary: `tests/decision_table_testing/test-summary/fr09-coupon_application-decision-table-summary.md`
- State Transition test cases: `tests/state-transition-testing/FR-10/test-cases/**/*.md`
- State Transition test run: `tests/state-transition-testing/FR-10/test-runs/fr10-order-state-machine-test-run.md`
- Use Case test cases: `tests/use-case-testing/FR-10/test-cases/**/*.md`
- Use Case test run: `tests/use-case-testing/FR-10/test-runs/fr10-order-state-machine-test-run.md`
- Bug artifacts: `tests/domain_bva_testing/bug/*/*.md`, `tests/decision_table_testing/bug/*/*.md`, `tests/state-transition-testing/FR-10/bug/*/*.md`, `tests/use-case-testing/FR-10/bug/*/*.md`

Ghi chú: `tests/domain_bva_testing/test-cases/coupon_application/` và `tests/domain_bva_testing/test-cases/product_list_search/` đang là thư mục rỗng tại thời điểm tổng hợp, nên không được tính vào tổng số test case hiện hữu.

## Tổng quan

| Metric | Count |
| :--- | ---: |
| Số feature đã có test case | 5 |
| Số test suite/folder chính | 4 |
| Số test case artifact đã thiết kế | 150 |
| Số test case artifact đã execute | 150 |
| Passed | 118 |
| Failed | 32 |
| Not Run | 0 |
| Bug artifact | 20 |

## Summary Theo Test Suite

| Test suite | Scope | Test case folder | Test run | Designed | Executed | Passed | Failed | Bugs |
| :--- | :--- | :--- | :--- | ---: | ---: | ---: | ---: | ---: |
| Domain/BVA Testing | FR-04, FR-10, FR-18, FR-20 | [`tests/domain_bva_testing/test-cases/`](tests/domain_bva_testing/test-cases/) | [`tests/domain_bva_testing/test-runs/`](tests/domain_bva_testing/test-runs/) | 100 | 100 | 79 | 21 | 10 |
| Decision Table Testing | FR-09 | [`tests/decision_table_testing/test-cases/`](tests/decision_table_testing/test-cases/) | [`fr09-coupon-application-test-run.md`](tests/decision_table_testing/test-runs/fr09-coupon-application-test-run.md) | 10 | 10 | 6 | 4 | 3 |
| State Transition Testing | FR-10 | [`tests/state-transition-testing/FR-10/test-cases/`](tests/state-transition-testing/FR-10/test-cases/) | [`fr10-order-state-machine-test-run.md`](tests/state-transition-testing/FR-10/test-runs/fr10-order-state-machine-test-run.md) | 20 | 20 | 18 | 2 | 2 |
| Use Case Testing | FR-10 | [`tests/use-case-testing/FR-10/test-cases/`](tests/use-case-testing/FR-10/test-cases/) | [`fr10-order-state-machine-test-run.md`](tests/use-case-testing/FR-10/test-runs/fr10-order-state-machine-test-run.md) | 20 | 20 | 15 | 5 | 5 |
| **Total** |  |  |  | **150** | **150** | **118** | **32** | **20** |

## Domain/BVA Summary Theo Feature

| Feature | Test case folder | Test run | Designed | Executed | Passed | Failed | Bugs |
| :--- | :--- | :--- | ---: | ---: | ---: | ---: | ---: |
| FR-04 Profile Management | [`tests/domain_bva_testing/test-cases/profile_management/`](tests/domain_bva_testing/test-cases/profile_management/) | [`fr04-profile-management-test-run.md`](tests/domain_bva_testing/test-runs/fr04-profile-management-test-run.md) | 32 | 32 | 20 | 12 | 4 |
| FR-10 Order State Machine | [`tests/domain_bva_testing/test-cases/order_state_machine/`](tests/domain_bva_testing/test-cases/order_state_machine/) | [`fr10-order-state-machine-test-run.md`](tests/domain_bva_testing/test-runs/fr10-order-state-machine-test-run.md) | 23 | 23 | 21 | 2 | 2 |
| FR-18 Admin Order Management | [`tests/domain_bva_testing/test-cases/admin_order_management/`](tests/domain_bva_testing/test-cases/admin_order_management/) | [`fr18-admin-order-management-test-run.md`](tests/domain_bva_testing/test-runs/fr18-admin-order-management-test-run.md) | 27 | 27 | 21 | 6 | 3 |
| FR-20 Mobile Product List & Search | [`tests/domain_bva_testing/test-cases/mobile_product_list_search/`](tests/domain_bva_testing/test-cases/mobile_product_list_search/) | [`fr20-mobile-product-list-search-test-run.md`](tests/domain_bva_testing/test-runs/fr20-mobile-product-list-search-test-run.md) | 18 | 18 | 17 | 1 | 1 |
| **Total** |  |  | **100** | **100** | **79** | **21** | **10** |

## Kỹ Thuật Kiểm Thử

| Suite | Technique chính | TC | Tag bổ sung |
| :--- | :--- | ---: | :--- |
| Domain/BVA Testing | Equivalence Partitioning / Boundary Value Analysis | 100 | Security, Authorization, Mobile, State Transition tag trong FR-10/FR-18 |
| Decision Table Testing | Decision Table / Pairwise | 10 | FR-09 coupon condition/action rules |
| State Transition Testing | State Transition Testing | 20 | FR-10 order state machine |
| Use Case Testing | Use Case Testing | 20 | Main, Alternate, Exception flows |
| **Total** |  | **150** |  |

### Domain/BVA Technique Breakdown

| Feature | Domain / EP TC | BVA TC | Tag bổ sung |
| :--- | ---: | ---: | :--- |
| FR-04 | 14 | 18 | Security, Authorization |
| FR-10 | 20 | 3 | State Transition |
| FR-18 | 24 | 3 | State Transition, Authorization, Security |
| FR-20 | 11 | 7 | Security, Mobile |
| **Total Domain/BVA** | **69** | **31** |  |

## Bug Summary

| Bug ID | Feature | Related failed TC | Severity | Artifact |
| :--- | :--- | :--- | :--- | :--- |
| BUG-FR04-N-01 | FR-04 (Domain/BVA) | FR04-N-BVA-TC07 | Low | [`BUG-FR04-N-01.md`](tests/domain_bva_testing/bug/FR-04/BUG-FR04-N-01.md) |
| BUG-FR04-P-01 | FR-04 (Domain/BVA) | FR04-P-BVA-TC02, FR04-P-BVA-TC03, FR04-P-BVA-TC04, FR04-P-TC02, FR04-P-TC03, FR04-P-TC05 | High | [`BUG-FR04-P-01.md`](tests/domain_bva_testing/bug/FR-04/BUG-FR04-P-01.md) |
| BUG-FR04-A-01 | FR-04 (Domain/BVA) | FR04-A-TC01, FR04-A-BVA-TC01, FR04-A-BVA-TC07, FR04-A-TC03 | Medium | [`BUG-FR04-A-01.md`](tests/domain_bva_testing/bug/FR-04/BUG-FR04-A-01.md) |
| BUG-FR04-R-01 | FR-04 (Domain/BVA) | FR04-R-TC01 | High | [`BUG-FR04-R-01.md`](tests/domain_bva_testing/bug/FR-04/BUG-FR04-R-01.md) |
| BUG-FR10-S-01 | FR-10 (Domain/BVA) | FR10-S-TC12 | High | [`BUG-FR10-S-01.md`](tests/domain_bva_testing/bug/FR-10/BUG-FR10-S-01.md) |
| BUG-FR10-S-02 | FR-10 (Domain/BVA) | FR10-S-TC16 | High | [`BUG-FR10-S-02.md`](tests/domain_bva_testing/bug/FR-10/BUG-FR10-S-02.md) |
| BUG-FR18-S-01 | FR-18 (Domain/BVA) | FR18-S-TC11 | High | [`BUG-FR18-S-01.md`](tests/domain_bva_testing/bug/FR-18/BUG-FR18-S-01.md) |
| BUG-FR18-A-01 | FR-18 (Domain/BVA) | FR18-A-TC01, FR18-A-TC03 | High | [`BUG-FR18-A-01.md`](tests/domain_bva_testing/bug/FR-18/BUG-FR18-A-01.md) |
| BUG-FR18-X-01 | FR-18 (Domain/BVA) | FR18-X-TC01, FR18-X-TC02, FR18-X-TC03 | Medium | [`BUG-FR18-X-01.md`](tests/domain_bva_testing/bug/FR-18/BUG-FR18-X-01.md) |
| BUG-FR20-X-01 | FR-20 (Domain/BVA) | FR20-X-TC03 | High | [`BUG-FR20-X-01.md`](tests/domain_bva_testing/bug/FR-20/BUG-FR20-X-01.md) |
| BUG-FR09-P-01 | FR-09 (Decision Table) | FR09-P-TC01 | High | [`BUG-FR09-P-01.md`](tests/decision_table_testing/bug/FR-09/BUG-FR09-P-01.md) |
| BUG-FR09-T-01 | FR-09 (Decision Table) | FR09-T-TC01, FR09-T-TC03 | High | [`BUG-FR09-T-01.md`](tests/decision_table_testing/bug/FR-09/BUG-FR09-T-01.md) |
| BUG-FR09-A-01 | FR-09 (Decision Table) | FR09-A-TC01 | High | [`BUG-FR09-A-01.md`](tests/decision_table_testing/bug/FR-09/BUG-FR09-A-01.md) |
| BUG-FR10-S-01 | FR-10 (State Transition) | FR10-S-TC12 | High | [`BUG-FR10-S-01.md`](tests/state-transition-testing/FR-10/bug/FR-10/BUG-FR10-S-01.md) |
| BUG-FR10-S-02 | FR-10 (State Transition) | FR10-S-TC16 | High | [`BUG-FR10-S-02.md`](tests/state-transition-testing/FR-10/bug/FR-10/BUG-FR10-S-02.md) |
| BUG-FR10-UC01-TC05 | FR-10 (Use Case) | FR10-UC01-TC05 | High | [`BUG-FR10-UC01-TC05.md`](tests/use-case-testing/FR-10/bug/FR-10/BUG-FR10-UC01-TC05.md) |
| BUG-FR10-UC01-TC06 | FR-10 (Use Case) | FR10-UC01-TC06 | High | [`BUG-FR10-UC01-TC06.md`](tests/use-case-testing/FR-10/bug/FR-10/BUG-FR10-UC01-TC06.md) |
| BUG-FR10-UC01-TC07 | FR-10 (Use Case) | FR10-UC01-TC07 | High | [`BUG-FR10-UC01-TC07.md`](tests/use-case-testing/FR-10/bug/FR-10/BUG-FR10-UC01-TC07.md) |
| BUG-FR10-UC02-TC04 | FR-10 (Use Case) | FR10-UC02-TC04 | High | [`BUG-FR10-UC02-TC04.md`](tests/use-case-testing/FR-10/bug/FR-10/BUG-FR10-UC02-TC04.md) |
| BUG-FR10-UC02-TC08 | FR-10 (Use Case) | FR10-UC02-TC08 | High | [`BUG-FR10-UC02-TC08.md`](tests/use-case-testing/FR-10/bug/FR-10/BUG-FR10-UC02-TC08.md) |

## Artifact Map

| Artifact type | Path |
| :--- | :--- |
| Domain/BVA README | [`tests/domain_bva_testing/README.md`](tests/domain_bva_testing/README.md) |
| Domain/BVA traceability matrix | [`tests/domain_bva_testing/test-summary/traceability-matrix.md`](tests/domain_bva_testing/test-summary/traceability-matrix.md) |
| Domain/BVA summaries | [`tests/domain_bva_testing/test-summary/`](tests/domain_bva_testing/test-summary/) |
| Domain/BVA configs | [`tests/domain_bva_testing/test-configs/`](tests/domain_bva_testing/test-configs/) |
| Domain/BVA bug reports | [`tests/domain_bva_testing/bug/`](tests/domain_bva_testing/bug/) |
| Domain/BVA AI logs | [`tests/domain_bva_testing/ai_log/`](tests/domain_bva_testing/ai_log/) |
| Decision Table summary | [`tests/decision_table_testing/test-summary/fr09-coupon_application-decision-table-summary.md`](tests/decision_table_testing/test-summary/fr09-coupon_application-decision-table-summary.md) |
| Decision Table test run | [`tests/decision_table_testing/test-runs/fr09-coupon-application-test-run.md`](tests/decision_table_testing/test-runs/fr09-coupon-application-test-run.md) |
| Decision Table bug reports | [`tests/decision_table_testing/bug/FR-09/`](tests/decision_table_testing/bug/FR-09/) |
| State Transition summary | [`tests/state-transition-testing/FR-10/test-summary/fr10-order-state-machine-state-transition-summary.md`](tests/state-transition-testing/FR-10/test-summary/fr10-order-state-machine-state-transition-summary.md) |
| State Transition traceability matrix | [`tests/state-transition-testing/FR-10/test-summary/traceability-matrix.md`](tests/state-transition-testing/FR-10/test-summary/traceability-matrix.md) |
| State Transition config | [`tests/state-transition-testing/FR-10/test-configs/fr10-order-state-machine-state-transition-config.json`](tests/state-transition-testing/FR-10/test-configs/fr10-order-state-machine-state-transition-config.json) |
| State Transition bug reports | [`tests/state-transition-testing/FR-10/bug/FR-10/`](tests/state-transition-testing/FR-10/bug/FR-10/) |
| Use Case summary | [`tests/use-case-testing/FR-10/test-summary/fr10-order-state-machine-use-case-summary.md`](tests/use-case-testing/FR-10/test-summary/fr10-order-state-machine-use-case-summary.md) |
| Use Case traceability matrix | [`tests/use-case-testing/FR-10/test-summary/traceability-matrix.md`](tests/use-case-testing/FR-10/test-summary/traceability-matrix.md) |
| Use Case config | [`tests/use-case-testing/FR-10/test-configs/fr10-order-state-machine-use-case-config.json`](tests/use-case-testing/FR-10/test-configs/fr10-order-state-machine-use-case-config.json) |
| Use Case bug reports | [`tests/use-case-testing/FR-10/bug/FR-10/`](tests/use-case-testing/FR-10/bug/FR-10/) |

## Full Test Case Index

### FR-04

| Test case | Nội dung | Kỹ thuật/tag | Status | Bug |
| :--- | :--- | :--- | :--- | :--- |
| [FR04-A-BVA-TC01](tests/domain_bva_testing/test-cases/profile_management/FR04-A-BVA-TC01.md) | Kiểm thử Địa chỉ giao hàng mặc định với độ dài dưới tối thiểu (4 ký tự) | Boundary Value Analysis | Failed | BUG-FR04-A-01 |
| [FR04-A-BVA-TC02](tests/domain_bva_testing/test-cases/profile_management/FR04-A-BVA-TC02.md) | Kiểm thử Địa chỉ giao hàng mặc định với độ dài biên tối thiểu (5 ký tự) | Boundary Value Analysis | Passed | None |
| [FR04-A-BVA-TC03](tests/domain_bva_testing/test-cases/profile_management/FR04-A-BVA-TC03.md) | Kiểm thử Địa chỉ giao hàng mặc định với độ dài Min+1 (6 ký tự) | Boundary Value Analysis | Passed | None |
| [FR04-A-BVA-TC04](tests/domain_bva_testing/test-cases/profile_management/FR04-A-BVA-TC04.md) | Kiểm thử Địa chỉ giao hàng mặc định với độ dài Nominal (130 ký tự) | Boundary Value Analysis | Passed | None |
| [FR04-A-BVA-TC05](tests/domain_bva_testing/test-cases/profile_management/FR04-A-BVA-TC05.md) | Kiểm thử Địa chỉ giao hàng mặc định với độ dài Max-1 (254 ký tự) | Boundary Value Analysis | Passed | None |
| [FR04-A-BVA-TC06](tests/domain_bva_testing/test-cases/profile_management/FR04-A-BVA-TC06.md) | Kiểm thử Địa chỉ giao hàng mặc định với độ dài biên tối đa (255 ký tự) | Boundary Value Analysis | Passed | None |
| [FR04-A-BVA-TC07](tests/domain_bva_testing/test-cases/profile_management/FR04-A-BVA-TC07.md) | Kiểm thử Địa chỉ giao hàng mặc định với độ dài vượt quá tối đa (256 ký tự) | Boundary Value Analysis | Failed | BUG-FR04-A-01 |
| [FR04-A-TC01](tests/domain_bva_testing/test-cases/profile_management/FR04-A-TC01.md) | Kiểm thử Địa chỉ giao hàng mặc định để trống | Equivalence Partitioning | Failed | BUG-FR04-A-01 |
| [FR04-A-TC02](tests/domain_bva_testing/test-cases/profile_management/FR04-A-TC02.md) | Cập nhật địa chỉ giao hàng hợp lệ | Equivalence Partitioning | Passed | None |
| [FR04-A-TC03](tests/domain_bva_testing/test-cases/profile_management/FR04-A-TC03.md) | Từ chối địa chỉ chỉ gồm khoảng trắng | Equivalence Partitioning | Failed | BUG-FR04-A-01 |
| [FR04-E-TC01](tests/domain_bva_testing/test-cases/profile_management/FR04-E-TC01.md) | Email không thể thay đổi qua giao diện hồ sơ | Equivalence Partitioning | Passed | None |
| [FR04-N-BVA-TC01](tests/domain_bva_testing/test-cases/profile_management/FR04-N-BVA-TC01.md) | Kiểm thử Họ Tên với độ dài dưới tối thiểu (0 ký tự) | Boundary Value Analysis | Passed | None |
| [FR04-N-BVA-TC02](tests/domain_bva_testing/test-cases/profile_management/FR04-N-BVA-TC02.md) | Kiểm thử Họ Tên với độ dài biên tối thiểu (1 ký tự) | Boundary Value Analysis | Passed | None |
| [FR04-N-BVA-TC03](tests/domain_bva_testing/test-cases/profile_management/FR04-N-BVA-TC03.md) | Kiểm thử Họ Tên với độ dài Min+1 (2 ký tự) | Boundary Value Analysis | Passed | None |
| [FR04-N-BVA-TC04](tests/domain_bva_testing/test-cases/profile_management/FR04-N-BVA-TC04.md) | Kiểm thử Họ Tên với độ dài Nominal (25 ký tự) | Boundary Value Analysis | Passed | None |
| [FR04-N-BVA-TC05](tests/domain_bva_testing/test-cases/profile_management/FR04-N-BVA-TC05.md) | Kiểm thử Họ Tên với độ dài Max-1 (49 ký tự) | Boundary Value Analysis | Passed | None |
| [FR04-N-BVA-TC06](tests/domain_bva_testing/test-cases/profile_management/FR04-N-BVA-TC06.md) | Kiểm thử Họ Tên với độ dài biên tối đa (50 ký tự) | Boundary Value Analysis | Passed | None |
| [FR04-N-BVA-TC07](tests/domain_bva_testing/test-cases/profile_management/FR04-N-BVA-TC07.md) | Kiểm thử Họ Tên với độ dài vượt quá tối đa (51 ký tự) | Boundary Value Analysis | Failed | BUG-FR04-N-01 |
| [FR04-N-TC01](tests/domain_bva_testing/test-cases/profile_management/FR04-N-TC01.md) | Kiểm thử Họ Tên để trống | Equivalence Partitioning | Passed | None |
| [FR04-N-TC02](tests/domain_bva_testing/test-cases/profile_management/FR04-N-TC02.md) | Cập nhật họ tên hợp lệ | Equivalence Partitioning | Passed | None |
| [FR04-P-BVA-TC01](tests/domain_bva_testing/test-cases/profile_management/FR04-P-BVA-TC01.md) | Kiểm thử Số điện thoại với độ dài dưới tối thiểu (9 ký tự) | Boundary Value Analysis | Passed | None |
| [FR04-P-BVA-TC02](tests/domain_bva_testing/test-cases/profile_management/FR04-P-BVA-TC02.md) | Kiểm thử Số điện thoại với độ dài biên tối thiểu (10 ký tự) | Boundary Value Analysis | Failed | BUG-FR04-P-01 |
| [FR04-P-BVA-TC03](tests/domain_bva_testing/test-cases/profile_management/FR04-P-BVA-TC03.md) | Kiểm thử Số điện thoại với độ dài Min+1 (11 ký tự) | Boundary Value Analysis | Failed | BUG-FR04-P-01 |
| [FR04-P-BVA-TC04](tests/domain_bva_testing/test-cases/profile_management/FR04-P-BVA-TC04.md) | Kiểm thử Số điện thoại với độ dài vượt quá tối đa (12 ký tự) | Boundary Value Analysis | Failed | BUG-FR04-P-01 |
| [FR04-P-TC01](tests/domain_bva_testing/test-cases/profile_management/FR04-P-TC01.md) | Kiểm thử Số điện thoại để trống | Equivalence Partitioning | Passed | None |
| [FR04-P-TC02](tests/domain_bva_testing/test-cases/profile_management/FR04-P-TC02.md) | Cập nhật số điện thoại hợp lệ 10 chữ số bắt đầu bằng 0 | Equivalence Partitioning | Failed | BUG-FR04-P-01 |
| [FR04-P-TC03](tests/domain_bva_testing/test-cases/profile_management/FR04-P-TC03.md) | Cập nhật số điện thoại hợp lệ 11 chữ số bắt đầu bằng 0 | Equivalence Partitioning | Failed | BUG-FR04-P-01 |
| [FR04-P-TC04](tests/domain_bva_testing/test-cases/profile_management/FR04-P-TC04.md) | Từ chối số điện thoại không bắt đầu bằng 0 | Equivalence Partitioning | Passed | None |
| [FR04-P-TC05](tests/domain_bva_testing/test-cases/profile_management/FR04-P-TC05.md) | Từ chối số điện thoại chứa ký tự không phải chữ số | Equivalence Partitioning | Failed | BUG-FR04-P-01 |
| [FR04-R-TC01](tests/domain_bva_testing/test-cases/profile_management/FR04-R-TC01.md) | Không cho phép user tự thay đổi role | Equivalence Partitioning / Security | Failed | BUG-FR04-R-01 |
| [FR04-U-TC01](tests/domain_bva_testing/test-cases/profile_management/FR04-U-TC01.md) | Từ chối cập nhật hồ sơ khi chưa đăng nhập | Equivalence Partitioning / Authorization | Passed | None |
| [FR04-U-TC02](tests/domain_bva_testing/test-cases/profile_management/FR04-U-TC02.md) | Không cho phép cập nhật hồ sơ của user khác | Equivalence Partitioning / Authorization | Passed | None |

### FR-09 Decision Table Testing

| Test case | Nội dung | Kỹ thuật/tag | Status | Bug |
| :--- | :--- | :--- | :--- | :--- |
| [FR09-P-TC01](tests/decision_table_testing/test-cases/coupon_application/FR09-P-TC01.md) | Áp dụng mã percent khi tất cả điều kiện hợp lệ | Decision Table / Pairwise | Failed | BUG-FR09-P-01 |
| [FR09-F-TC01](tests/decision_table_testing/test-cases/coupon_application/FR09-F-TC01.md) | Áp dụng mã fixed khi tất cả điều kiện hợp lệ | Decision Table / Pairwise | Passed | None |
| [FR09-T-TC01](tests/decision_table_testing/test-cases/coupon_application/FR09-T-TC01.md) | Chấp nhận mã percent khi tổng đơn hàng bằng đúng ngưỡng tối thiểu | Decision Table / Pairwise | Failed | BUG-FR09-T-01 |
| [FR09-T-TC02](tests/decision_table_testing/test-cases/coupon_application/FR09-T-TC02.md) | Từ chối mã khi tổng đơn hàng thấp hơn ngưỡng tối thiểu | Decision Table | Passed | None |
| [FR09-T-TC03](tests/decision_table_testing/test-cases/coupon_application/FR09-T-TC03.md) | Chấp nhận mã fixed khi tổng đơn hàng bằng đúng ngưỡng tối thiểu | Decision Table / Pairwise | Failed | BUG-FR09-T-01 |
| [FR09-C-TC01](tests/decision_table_testing/test-cases/coupon_application/FR09-C-TC01.md) | Từ chối mã giảm giá không tồn tại hoặc không hoạt động | Decision Table | Passed | None |
| [FR09-C-TC02](tests/decision_table_testing/test-cases/coupon_application/FR09-C-TC02.md) | Từ chối request áp dụng mã khi code rỗng | Decision Table | Passed | None |
| [FR09-E-TC01](tests/decision_table_testing/test-cases/coupon_application/FR09-E-TC01.md) | Từ chối mã giảm giá đã hết hạn | Decision Table | Passed | None |
| [FR09-A-TC01](tests/decision_table_testing/test-cases/coupon_application/FR09-A-TC01.md) | Từ chối người dùng chưa đăng nhập áp dụng mã giảm giá | Decision Table | Failed | BUG-FR09-A-01 |
| [FR09-U-TC01](tests/decision_table_testing/test-cases/coupon_application/FR09-U-TC01.md) | Từ chối mã khi user đã dùng hết số lượt cho phép | Decision Table | Passed | None |

### FR-10

| Test case | Nội dung | Kỹ thuật/tag | Status | Bug |
| :--- | :--- | :--- | :--- | :--- |
| [FR10-O-BVA-TC01](tests/domain_bva_testing/test-cases/order_state_machine/FR10-O-BVA-TC01.md) | Kiểm thử Order ID ngay dưới biên tối thiểu | Boundary Value Analysis | Passed | None |
| [FR10-O-BVA-TC02](tests/domain_bva_testing/test-cases/order_state_machine/FR10-O-BVA-TC02.md) | Kiểm thử Order ID tại biên tối thiểu | Boundary Value Analysis | Passed | None |
| [FR10-O-BVA-TC03](tests/domain_bva_testing/test-cases/order_state_machine/FR10-O-BVA-TC03.md) | Kiểm thử Order ID ngay trên biên tối thiểu | Boundary Value Analysis | Passed | None |
| [FR10-S-TC01](tests/domain_bva_testing/test-cases/order_state_machine/FR10-S-TC01.md) | Admin xác nhận đơn hàng từ pending sang confirmed | Equivalence Partitioning / State Transition | Passed | None |
| [FR10-S-TC02](tests/domain_bva_testing/test-cases/order_state_machine/FR10-S-TC02.md) | Admin giao hàng từ confirmed sang shipping | Equivalence Partitioning / State Transition | Passed | None |
| [FR10-S-TC03](tests/domain_bva_testing/test-cases/order_state_machine/FR10-S-TC03.md) | Admin hoàn tất đơn hàng từ shipping sang delivered | Equivalence Partitioning / State Transition | Passed | None |
| [FR10-S-TC04](tests/domain_bva_testing/test-cases/order_state_machine/FR10-S-TC04.md) | User hủy đơn hàng ở trạng thái pending | Equivalence Partitioning / State Transition | Passed | None |
| [FR10-S-TC05](tests/domain_bva_testing/test-cases/order_state_machine/FR10-S-TC05.md) | Admin hủy đơn hàng ở trạng thái pending | Equivalence Partitioning / State Transition | Passed | None |
| [FR10-S-TC06](tests/domain_bva_testing/test-cases/order_state_machine/FR10-S-TC06.md) | User hủy đơn hàng ở trạng thái confirmed | Equivalence Partitioning / State Transition | Passed | None |
| [FR10-S-TC07](tests/domain_bva_testing/test-cases/order_state_machine/FR10-S-TC07.md) | Admin hủy đơn hàng ở trạng thái confirmed | Equivalence Partitioning / State Transition | Passed | None |
| [FR10-S-TC08](tests/domain_bva_testing/test-cases/order_state_machine/FR10-S-TC08.md) | Từ chối Admin chuyển tắt pending sang shipping | Equivalence Partitioning / State Transition | Passed | None |
| [FR10-S-TC09](tests/domain_bva_testing/test-cases/order_state_machine/FR10-S-TC09.md) | Từ chối Admin chuyển tắt confirmed sang delivered | Equivalence Partitioning / State Transition | Passed | None |
| [FR10-S-TC10](tests/domain_bva_testing/test-cases/order_state_machine/FR10-S-TC10.md) | Từ chối Admin chuyển ngược shipping sang confirmed | Equivalence Partitioning / State Transition | Passed | None |
| [FR10-S-TC11](tests/domain_bva_testing/test-cases/order_state_machine/FR10-S-TC11.md) | Từ chối Admin hủy đơn hàng đang shipping | Equivalence Partitioning / State Transition | Passed | None |
| [FR10-S-TC12](tests/domain_bva_testing/test-cases/order_state_machine/FR10-S-TC12.md) | Từ chối User tự hủy đơn hàng đang shipping | Equivalence Partitioning / State Transition | Failed | BUG-FR10-S-01 |
| [FR10-S-TC13](tests/domain_bva_testing/test-cases/order_state_machine/FR10-S-TC13.md) | Từ chối User hủy đơn hàng đã delivered | Equivalence Partitioning / State Transition | Passed | None |
| [FR10-S-TC14](tests/domain_bva_testing/test-cases/order_state_machine/FR10-S-TC14.md) | Từ chối User hủy lại đơn hàng đã canceled | Equivalence Partitioning / State Transition | Passed | None |
| [FR10-S-TC15](tests/domain_bva_testing/test-cases/order_state_machine/FR10-S-TC15.md) | Từ chối Admin chuyển delivered sang canceled | Equivalence Partitioning / State Transition | Passed | None |
| [FR10-S-TC16](tests/domain_bva_testing/test-cases/order_state_machine/FR10-S-TC16.md) | Từ chối Admin chuyển canceled sang delivered | Equivalence Partitioning / State Transition | Failed | BUG-FR10-S-02 |
| [FR10-S-TC17](tests/domain_bva_testing/test-cases/order_state_machine/FR10-S-TC17.md) | Từ chối Admin cập nhật pending sang chính pending | Equivalence Partitioning / State Transition | Passed | None |
| [FR10-S-TC18](tests/domain_bva_testing/test-cases/order_state_machine/FR10-S-TC18.md) | Từ chối status không nằm trong state machine: refund | Equivalence Partitioning | Passed | None |
| [FR10-S-TC19](tests/domain_bva_testing/test-cases/order_state_machine/FR10-S-TC19.md) | Từ chối status rỗng | Equivalence Partitioning | Passed | None |
| [FR10-S-TC20](tests/domain_bva_testing/test-cases/order_state_machine/FR10-S-TC20.md) | Từ chối status null | Equivalence Partitioning | Passed | None |

### FR-18

| Test case | Nội dung | Kỹ thuật/tag | Status | Bug |
| :--- | :--- | :--- | :--- | :--- |
| [FR18-A-TC01](tests/domain_bva_testing/test-cases/admin_order_management/FR18-A-TC01.md) | Từ chối user thường xem danh sách đơn hàng Admin | Equivalence Partitioning / Authorization | Failed | BUG-FR18-A-01 |
| [FR18-A-TC02](tests/domain_bva_testing/test-cases/admin_order_management/FR18-A-TC02.md) | Từ chối request không có token xem danh sách đơn hàng Admin | Equivalence Partitioning / Authorization | Passed | None |
| [FR18-A-TC03](tests/domain_bva_testing/test-cases/admin_order_management/FR18-A-TC03.md) | Từ chối user thường cập nhật trạng thái đơn hàng qua endpoint Admin | Equivalence Partitioning / Authorization | Failed | BUG-FR18-A-01 |
| [FR18-A-TC04](tests/domain_bva_testing/test-cases/admin_order_management/FR18-A-TC04.md) | Từ chối request không có token cập nhật trạng thái đơn hàng | Equivalence Partitioning / Authorization | Passed | None |
| [FR18-O-BVA-TC01](tests/domain_bva_testing/test-cases/admin_order_management/FR18-O-BVA-TC01.md) | Kiểm thử Order ID ngay dưới biên tối thiểu | Boundary Value Analysis | Passed | None |
| [FR18-O-BVA-TC02](tests/domain_bva_testing/test-cases/admin_order_management/FR18-O-BVA-TC02.md) | Kiểm thử Order ID tại biên tối thiểu | Boundary Value Analysis | Passed | None |
| [FR18-O-BVA-TC03](tests/domain_bva_testing/test-cases/admin_order_management/FR18-O-BVA-TC03.md) | Kiểm thử Order ID ngay trên biên tối thiểu | Boundary Value Analysis | Passed | None |
| [FR18-S-TC01](tests/domain_bva_testing/test-cases/admin_order_management/FR18-S-TC01.md) | Admin xác nhận đơn hàng từ pending sang confirmed | Equivalence Partitioning / State Transition | Passed | None |
| [FR18-S-TC02](tests/domain_bva_testing/test-cases/admin_order_management/FR18-S-TC02.md) | Admin hủy đơn hàng ở trạng thái pending | Equivalence Partitioning / State Transition | Passed | None |
| [FR18-S-TC03](tests/domain_bva_testing/test-cases/admin_order_management/FR18-S-TC03.md) | Admin giao hàng từ confirmed sang shipping | Equivalence Partitioning / State Transition | Passed | None |
| [FR18-S-TC04](tests/domain_bva_testing/test-cases/admin_order_management/FR18-S-TC04.md) | Admin hủy đơn hàng ở trạng thái confirmed | Equivalence Partitioning / State Transition | Passed | None |
| [FR18-S-TC05](tests/domain_bva_testing/test-cases/admin_order_management/FR18-S-TC05.md) | Admin hoàn tất đơn hàng từ shipping sang delivered | Equivalence Partitioning / State Transition | Passed | None |
| [FR18-S-TC06](tests/domain_bva_testing/test-cases/admin_order_management/FR18-S-TC06.md) | Từ chối Admin chuyển tắt pending sang shipping | Equivalence Partitioning / State Transition | Passed | None |
| [FR18-S-TC07](tests/domain_bva_testing/test-cases/admin_order_management/FR18-S-TC07.md) | Từ chối Admin chuyển tắt confirmed sang delivered | Equivalence Partitioning / State Transition | Passed | None |
| [FR18-S-TC08](tests/domain_bva_testing/test-cases/admin_order_management/FR18-S-TC08.md) | Từ chối Admin chuyển ngược shipping sang confirmed | Equivalence Partitioning / State Transition | Passed | None |
| [FR18-S-TC09](tests/domain_bva_testing/test-cases/admin_order_management/FR18-S-TC09.md) | Từ chối Admin hủy đơn hàng đang shipping | Equivalence Partitioning / State Transition | Passed | None |
| [FR18-S-TC10](tests/domain_bva_testing/test-cases/admin_order_management/FR18-S-TC10.md) | Từ chối Admin chuyển delivered sang canceled | Equivalence Partitioning / State Transition | Passed | None |
| [FR18-S-TC11](tests/domain_bva_testing/test-cases/admin_order_management/FR18-S-TC11.md) | Từ chối Admin chuyển canceled sang delivered | Equivalence Partitioning / State Transition | Failed | BUG-FR18-S-01 |
| [FR18-S-TC12](tests/domain_bva_testing/test-cases/admin_order_management/FR18-S-TC12.md) | Từ chối Admin cập nhật pending sang chính pending | Equivalence Partitioning / State Transition | Passed | None |
| [FR18-S-TC13](tests/domain_bva_testing/test-cases/admin_order_management/FR18-S-TC13.md) | Từ chối status không nằm trong state machine: refund | Equivalence Partitioning | Passed | None |
| [FR18-S-TC14](tests/domain_bva_testing/test-cases/admin_order_management/FR18-S-TC14.md) | Từ chối status rỗng | Equivalence Partitioning | Passed | None |
| [FR18-S-TC15](tests/domain_bva_testing/test-cases/admin_order_management/FR18-S-TC15.md) | Từ chối status null | Equivalence Partitioning | Passed | None |
| [FR18-V-TC01](tests/domain_bva_testing/test-cases/admin_order_management/FR18-V-TC01.md) | Admin xem toàn bộ đơn hàng của nhiều người dùng | Equivalence Partitioning | Passed | None |
| [FR18-V-TC02](tests/domain_bva_testing/test-cases/admin_order_management/FR18-V-TC02.md) | Danh sách đơn hàng Admin không lộ dữ liệu nhạy cảm ngoài phạm vi | Equivalence Partitioning / Security | Passed | None |
| [FR18-X-TC01](tests/domain_bva_testing/test-cases/admin_order_management/FR18-X-TC01.md) | Hiển thị địa chỉ giao hàng chứa thẻ script dưới dạng văn bản an toàn | Equivalence Partitioning / Security | Failed | BUG-FR18-X-01 |
| [FR18-X-TC02](tests/domain_bva_testing/test-cases/admin_order_management/FR18-X-TC02.md) | Hiển thị địa chỉ giao hàng chứa HTML event handler dưới dạng văn bản an toàn | Equivalence Partitioning / Security | Failed | BUG-FR18-X-01 |
| [FR18-X-TC03](tests/domain_bva_testing/test-cases/admin_order_management/FR18-X-TC03.md) | Hiển thị địa chỉ giao hàng hợp lệ bình thường | Equivalence Partitioning | Failed | BUG-FR18-X-01 |

### FR-20

| Test case | Nội dung | Kỹ thuật/tag | Status | Bug |
| :--- | :--- | :--- | :--- | :--- |
| [FR20-E-TC01](tests/domain_bva_testing/test-cases/mobile_product_list_search/FR20-E-TC01.md) | Mobile hiển thị empty state khi tìm kiếm không có kết quả | Equivalence Partitioning | Passed | None |
| [FR20-L-TC01](tests/domain_bva_testing/test-cases/mobile_product_list_search/FR20-L-TC01.md) | Mobile hiển thị danh sách tất cả sản phẩm khi vào trang chủ | Equivalence Partitioning | Passed | None |
| [FR20-L-TC02](tests/domain_bva_testing/test-cases/mobile_product_list_search/FR20-L-TC02.md) | Mobile card sản phẩm hiển thị đủ ảnh, tên và giá | Equivalence Partitioning | Passed | None |
| [FR20-L-TC03](tests/domain_bva_testing/test-cases/mobile_product_list_search/FR20-L-TC03.md) | Mobile hiển thị trạng thái loading khi đang tải danh sách | Equivalence Partitioning | Passed | None |
| [FR20-S-BVA-TC01](tests/domain_bva_testing/test-cases/mobile_product_list_search/FR20-S-BVA-TC01.md) | Kiểm thử Search Keyword tại biên rỗng 0 ký tự | Boundary Value Analysis | Passed | None |
| [FR20-S-BVA-TC02](tests/domain_bva_testing/test-cases/mobile_product_list_search/FR20-S-BVA-TC02.md) | Kiểm thử Search Keyword với độ dài 1 ký tự | Boundary Value Analysis | Passed | None |
| [FR20-S-BVA-TC03](tests/domain_bva_testing/test-cases/mobile_product_list_search/FR20-S-BVA-TC03.md) | Kiểm thử Search Keyword với độ dài 2 ký tự | Boundary Value Analysis | Passed | None |
| [FR20-S-BVA-TC04](tests/domain_bva_testing/test-cases/mobile_product_list_search/FR20-S-BVA-TC04.md) | Kiểm thử Search Keyword với độ dài danh nghĩa 20 ký tự | Boundary Value Analysis | Passed | None |
| [FR20-S-BVA-TC05](tests/domain_bva_testing/test-cases/mobile_product_list_search/FR20-S-BVA-TC05.md) | Kiểm thử Search Keyword ngay dưới biên tối đa 254 ký tự | Boundary Value Analysis | Passed | None |
| [FR20-S-BVA-TC06](tests/domain_bva_testing/test-cases/mobile_product_list_search/FR20-S-BVA-TC06.md) | Kiểm thử Search Keyword tại biên tối đa 255 ký tự | Boundary Value Analysis | Passed | None |
| [FR20-S-BVA-TC07](tests/domain_bva_testing/test-cases/mobile_product_list_search/FR20-S-BVA-TC07.md) | Kiểm thử Search Keyword vượt biên tối đa 256 ký tự | Boundary Value Analysis | Passed | None |
| [FR20-S-TC01](tests/domain_bva_testing/test-cases/mobile_product_list_search/FR20-S-TC01.md) | Mobile tìm kiếm sản phẩm theo từ khóa khớp một phần tên | Equivalence Partitioning | Passed | None |
| [FR20-S-TC02](tests/domain_bva_testing/test-cases/mobile_product_list_search/FR20-S-TC02.md) | Mobile tìm kiếm sản phẩm bằng từ khóa chữ thường | Equivalence Partitioning | Passed | None |
| [FR20-S-TC03](tests/domain_bva_testing/test-cases/mobile_product_list_search/FR20-S-TC03.md) | Mobile tìm kiếm với từ khóa rỗng để quay về toàn bộ danh sách | Equivalence Partitioning | Passed | None |
| [FR20-S-TC04](tests/domain_bva_testing/test-cases/mobile_product_list_search/FR20-S-TC04.md) | Mobile xử lý từ khóa có ký tự đặc biệt không khớp sản phẩm | Equivalence Partitioning | Passed | None |
| [FR20-X-TC01](tests/domain_bva_testing/test-cases/mobile_product_list_search/FR20-X-TC01.md) | Mobile hiển thị an toàn từ khóa dạng script tag | Equivalence Partitioning / Security | Passed | None |
| [FR20-X-TC02](tests/domain_bva_testing/test-cases/mobile_product_list_search/FR20-X-TC02.md) | Mobile hiển thị an toàn từ khóa có HTML event handler | Equivalence Partitioning / Security | Passed | None |
| [FR20-X-TC03](tests/domain_bva_testing/test-cases/mobile_product_list_search/FR20-X-TC03.md) | Mobile chống SQL injection qua từ khóa tìm kiếm | Equivalence Partitioning / Security | Failed | BUG-FR20-X-01 |

### FR-10 State Transition Testing

| Test case | Nội dung | Kỹ thuật/tag | Status | Bug |
| :--- | :--- | :--- | :--- | :--- |
| [FR10-S-TC01](tests/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC01.md) | Admin xác nhận đơn hàng từ pending sang confirmed | State Transition Testing | Passed | None |
| [FR10-S-TC02](tests/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC02.md) | Admin giao hàng từ confirmed sang shipping | State Transition Testing | Passed | None |
| [FR10-S-TC03](tests/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC03.md) | Admin hoàn tất đơn hàng từ shipping sang delivered | State Transition Testing | Passed | None |
| [FR10-S-TC04](tests/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC04.md) | User hủy đơn hàng ở trạng thái pending | State Transition Testing | Passed | None |
| [FR10-S-TC05](tests/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC05.md) | Admin hủy đơn hàng ở trạng thái pending | State Transition Testing | Passed | None |
| [FR10-S-TC06](tests/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC06.md) | User hủy đơn hàng ở trạng thái confirmed | State Transition Testing | Passed | None |
| [FR10-S-TC07](tests/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC07.md) | Admin hủy đơn hàng ở trạng thái confirmed | State Transition Testing | Passed | None |
| [FR10-S-TC08](tests/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC08.md) | Từ chối Admin chuyển tắt pending sang shipping | State Transition Testing | Passed | None |
| [FR10-S-TC09](tests/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC09.md) | Từ chối Admin chuyển tắt confirmed sang delivered | State Transition Testing | Passed | None |
| [FR10-S-TC10](tests/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC10.md) | Từ chối Admin chuyển ngược shipping sang confirmed | State Transition Testing | Passed | None |
| [FR10-S-TC11](tests/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC11.md) | Từ chối Admin hủy đơn hàng đang shipping | State Transition Testing | Passed | None |
| [FR10-S-TC12](tests/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC12.md) | Từ chối User tự hủy đơn hàng đang shipping | State Transition Testing | Failed | BUG-FR10-S-01 |
| [FR10-S-TC13](tests/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC13.md) | Từ chối User hủy đơn hàng đã delivered | State Transition Testing | Passed | None |
| [FR10-S-TC14](tests/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC14.md) | Từ chối User hủy lại đơn hàng đã canceled | State Transition Testing | Passed | None |
| [FR10-S-TC15](tests/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC15.md) | Từ chối Admin chuyển delivered sang canceled | State Transition Testing | Passed | None |
| [FR10-S-TC16](tests/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC16.md) | Từ chối Admin chuyển canceled sang delivered | State Transition Testing | Failed | BUG-FR10-S-02 |
| [FR10-S-TC17](tests/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC17.md) | Từ chối Admin cập nhật pending sang chính pending | State Transition Testing | Passed | None |
| [FR10-S-TC18](tests/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC18.md) | Từ chối status không nằm trong state machine: refund | State Transition Testing | Passed | None |
| [FR10-S-TC19](tests/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC19.md) | Từ chối status rỗng | State Transition Testing | Passed | None |
| [FR10-S-TC20](tests/state-transition-testing/FR-10/test-cases/order_state_machine/FR10-S-TC20.md) | Từ chối status null | State Transition Testing | Passed | None |

### FR-10 Use Case Testing

| Test case | Nội dung | Kỹ thuật/tag | Status | Bug |
| :--- | :--- | :--- | :--- | :--- |
| [FR10-UC01-TC01](tests/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC01-TC01.md) | Admin xác nhận đơn hàng pending | Use Case Testing | Passed | None |
| [FR10-UC01-TC02](tests/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC01-TC02.md) | Admin chuyển đơn hàng confirmed sang shipping | Use Case Testing | Passed | None |
| [FR10-UC01-TC03](tests/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC01-TC03.md) | Admin hoàn tất đơn hàng shipping sang delivered | Use Case Testing | Passed | None |
| [FR10-UC01-TC04](tests/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC01-TC04.md) | Admin bị từ chối khi chuyển tắt pending sang shipping | Use Case Testing | Passed | None |
| [FR10-UC01-TC05](tests/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC01-TC05.md) | Admin bị từ chối khi chuyển final state canceled sang delivered | Use Case Testing | Failed | BUG-FR10-UC01-TC05 |
| [FR10-UC01-TC06](tests/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC01-TC06.md) | Admin UI không hiển thị action chuyển tiếp cho final state | Use Case Testing | Failed | BUG-FR10-UC01-TC06 |
| [FR10-UC01-TC07](tests/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC01-TC07.md) | User thường bị từ chối khi gọi Admin status API | Use Case Testing | Failed | BUG-FR10-UC01-TC07 |
| [FR10-UC01-TC08](tests/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC01-TC08.md) | Admin bị từ chối khi gửi status ngoài state machine | Use Case Testing | Passed | None |
| [FR10-UC02-TC01](tests/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC02-TC01.md) | User hủy đơn hàng của mình khi đơn pending | Use Case Testing | Passed | None |
| [FR10-UC02-TC02](tests/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC02-TC02.md) | User hủy đơn hàng của mình khi đơn confirmed | Use Case Testing | Passed | None |
| [FR10-UC02-TC03](tests/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC02-TC03.md) | Mobile chỉ hiển thị nút hủy cho đơn pending hoặc confirmed | Use Case Testing | Passed | None |
| [FR10-UC02-TC04](tests/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC02-TC04.md) | User bị từ chối khi hủy đơn đang shipping | Use Case Testing | Failed | BUG-FR10-UC02-TC04 |
| [FR10-UC02-TC05](tests/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC02-TC05.md) | User bị từ chối khi hủy đơn đã delivered | Use Case Testing | Passed | None |
| [FR10-UC02-TC06](tests/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC02-TC06.md) | User bị từ chối khi hủy đơn của user khác | Use Case Testing | Passed | None |
| [FR10-UC02-TC07](tests/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC02-TC07.md) | Guest bị từ chối khi gọi API hủy đơn | Use Case Testing | Passed | None |
| [FR10-UC02-TC08](tests/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC02-TC08.md) | Web UI không hiển thị nút hủy cho đơn shipping | Use Case Testing | Failed | BUG-FR10-UC02-TC08 |
| [FR10-UC03-TC01](tests/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC03-TC01.md) | Admin hủy đơn pending | Use Case Testing | Passed | None |
| [FR10-UC03-TC02](tests/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC03-TC02.md) | Admin hủy đơn confirmed | Use Case Testing | Passed | None |
| [FR10-UC03-TC03](tests/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC03-TC03.md) | Admin bị từ chối khi hủy đơn shipping | Use Case Testing | Passed | None |
| [FR10-UC03-TC04](tests/use-case-testing/FR-10/test-cases/order_state_machine/FR10-UC03-TC04.md) | Admin bị từ chối khi hủy đơn delivered | Use Case Testing | Passed | None |

## Kiểm tra nhất quán

- Đã đối chiếu 150 test case file với 150 row trong các test-run hiện tại.
- Không có test case thiếu dòng run tương ứng trong từng suite.
- Không có run row thiếu file test case tương ứng trong từng suite.
- Không có mismatch giữa `Status / Related bugs` trong test case và `Result / Related Bug` trong test-run.
