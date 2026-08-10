# Bug reports — HW04

Student **23127271**

## FR-03 — Forgot Password (Feature A)

| ID | Title | Severity | Case | GitHub |
| --- | --- | --- | --- | --- |
| BUG-FR03-001 | Missing confirm-password field | High | TC-FORGOT-010 | TBD |
| BUG-FR03-002 | Missing step indicator | Medium | TC-FORGOT-011 | TBD |
| BUG-FR03-003 | No Quay lại đăng nhập | Medium | TC-FORGOT-012 | TBD |
| BUG-FR03-004 | Email type=text | Medium | TC-FORGOT-013 | TBD |
| BUG-FR03-005 | OTP 4 digits not 6 | High | TC-FORGOT-014 | TBD |

## FR-08 — Checkout (Feature B)

| ID | Title | Severity | Case | GitHub |
| --- | --- | --- | --- | --- |
| BUG-FR08-001 | No auth guard on `/checkout` | High | TC-CHECKOUT-002 | TBD |
| BUG-FR08-002 | Empty cart checkout allowed | High | TC-CHECKOUT-003 | TBD |
| BUG-FR08-003 | Payment total editable | High | TC-CHECKOUT-007 | TBD |
| BUG-FR08-004 | Backend trusts client total | Critical | TC-CHECKOUT-008 | TBD |
| BUG-FR08-005 | Cart not cleared after checkout | High | TC-CHECKOUT-009 | TBD |

## FR-15 — Product CRUD Admin (Feature C)

| ID | Title | Severity | Case | GitHub |
| --- | --- | --- | --- | --- |
| BUG-FR15-001 | Edit mass-renames sibling UI rows | High | TC-PRODUCT-004 | TBD |
| BUG-FR15-002 | Empty name accepted (200) | High | TC-PRODUCT-006 | TBD |
| BUG-FR15-003 | Name length 256 accepted (200) | Medium | TC-PRODUCT-008 | TBD |
| BUG-FR15-004 | Price 0 accepted (200) | High | TC-PRODUCT-009 | TBD |
| BUG-FR15-005 | Negative price accepted (200) | High | TC-PRODUCT-010 | TBD |
| BUG-FR15-006 | Invalid category_id accepted (200) | High | TC-PRODUCT-012 | TBD |
| BUG-FR15-007 | Create without JWT returns 200 (FR-12) | Critical | TC-PRODUCT-013 | TBD |
| BUG-FR15-008 | Non-admin JWT can create products (FR-12) | Critical | TC-PRODUCT-014 | TBD |

Evidence: `test-results/<feature>/<browser>/`. File GitHub Issues with screenshots before Moodle zip (HW04 §6).
