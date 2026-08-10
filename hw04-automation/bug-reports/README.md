# Bug reports — HW04

Student **23127271**  
GitHub Issues: [#372](https://github.com/trngnneee/eshop-sut/issues/372)–[#389](https://github.com/trngnneee/eshop-sut/issues/389) on `trngnneee/eshop-sut`  
Screenshots: `bug-reports/screenshots/BUG-*.png` (Chromium) + attached on each issue

## FR-03 — Forgot Password (Feature A)

| ID | Title | Severity | Case | GitHub |
| --- | --- | --- | --- | --- |
| BUG-FR03-001 | Missing confirm-password field | High | TC-FORGOT-010 | [#372](https://github.com/trngnneee/eshop-sut/issues/372) |
| BUG-FR03-002 | Missing step indicator | Medium | TC-FORGOT-011 | [#373](https://github.com/trngnneee/eshop-sut/issues/373) |
| BUG-FR03-003 | No Quay lại đăng nhập | Medium | TC-FORGOT-012 | [#374](https://github.com/trngnneee/eshop-sut/issues/374) |
| BUG-FR03-004 | Email type=text | Medium | TC-FORGOT-013 | [#375](https://github.com/trngnneee/eshop-sut/issues/375) |
| BUG-FR03-005 | OTP 4 digits not 6 | High | TC-FORGOT-014 | [#376](https://github.com/trngnneee/eshop-sut/issues/376) |

## FR-08 — Checkout (Feature B)

| ID | Title | Severity | Case | GitHub |
| --- | --- | --- | --- | --- |
| BUG-FR08-001 | No auth guard on `/checkout` | High | TC-CHECKOUT-002 | [#377](https://github.com/trngnneee/eshop-sut/issues/377) |
| BUG-FR08-002 | Empty cart checkout allowed | High | TC-CHECKOUT-003 | [#378](https://github.com/trngnneee/eshop-sut/issues/378) |
| BUG-FR08-003 | Payment total editable | High | TC-CHECKOUT-007 | [#379](https://github.com/trngnneee/eshop-sut/issues/379) |
| BUG-FR08-004 | Backend trusts client total | Critical | TC-CHECKOUT-008 | [#380](https://github.com/trngnneee/eshop-sut/issues/380) |
| BUG-FR08-005 | Cart not cleared after checkout | High | TC-CHECKOUT-009 | [#381](https://github.com/trngnneee/eshop-sut/issues/381) |

## FR-15 — Product CRUD Admin (Feature C)

| ID | Title | Severity | Case | GitHub |
| --- | --- | --- | --- | --- |
| BUG-FR15-001 | Edit mass-renames sibling UI rows | High | TC-PRODUCT-004 | [#382](https://github.com/trngnneee/eshop-sut/issues/382) |
| BUG-FR15-002 | Empty name accepted (200) | High | TC-PRODUCT-006 | [#383](https://github.com/trngnneee/eshop-sut/issues/383) |
| BUG-FR15-003 | Name length 256 accepted (200) | Medium | TC-PRODUCT-008 | [#384](https://github.com/trngnneee/eshop-sut/issues/384) |
| BUG-FR15-004 | Price 0 accepted (200) | High | TC-PRODUCT-009 | [#385](https://github.com/trngnneee/eshop-sut/issues/385) |
| BUG-FR15-005 | Negative price accepted (200) | High | TC-PRODUCT-010 | [#386](https://github.com/trngnneee/eshop-sut/issues/386) |
| BUG-FR15-006 | Invalid category_id accepted (200) | High | TC-PRODUCT-012 | [#387](https://github.com/trngnneee/eshop-sut/issues/387) |
| BUG-FR15-007 | Create without JWT returns 200 (FR-12) | Critical | TC-PRODUCT-013 | [#388](https://github.com/trngnneee/eshop-sut/issues/388) |
| BUG-FR15-008 | Non-admin JWT can create products (FR-12) | Critical | TC-PRODUCT-014 | [#389](https://github.com/trngnneee/eshop-sut/issues/389) |

Evidence also under `test-results/<feature>/<browser>/`.
