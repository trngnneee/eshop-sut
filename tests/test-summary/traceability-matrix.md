# Traceability Matrix: Requirement - Test Case - Bug
Bảng truy vết giúp đảm bảo độ bao phủ của kiểm thử và theo dõi trạng thái các lỗi tương ứng.

| Requirement | Test Case | Result | Bug Issue | Status |
| :--- | :--- | :--- | :--- | :--- |
| FR-02 (Authentication) | [TC-LOGIN-001](../test-cases/login/TC-LOGIN-001.md) | Pass | None | Done |
| FR-02 (Authentication) | [TC-LOGIN-002](../test-cases/login/TC-LOGIN-002.md) | Fail | #31, #33 | Open |
| FR-02 (Authentication) | [TC-LOGIN-003](../test-cases/login/TC-LOGIN-003.md) | Fail | #32 | Open |
| FR-21, FR-22 (GUI/Form) | [TC-LOGIN-004](../test-cases/login/TC-LOGIN-004.md) | Fail | #34, #35, #36, #37, #38, #46, #47 | Open |
| FR-02, FR-22 (Validation) | [TC-LOGIN-005](../test-cases/login/TC-LOGIN-005.md) | Fail | #39 | Open |
| FR-02 (Auth Token) | [TC-LOGIN-006](../test-cases/login/TC-LOGIN-006.md) | Pass | None | Done |
| SEC-05 (Security SQLi) | [TC-LOGIN-007](../test-cases/login/TC-LOGIN-007.md) | Pass | None | Done |
| SEC-02 (Security Rate) | [TC-LOGIN-008](../test-cases/login/TC-LOGIN-008.md) | Fail | #40 | Open |
| FR-21, FR-24 (UI/UX) | [TC-LOGIN-009](../test-cases/login/TC-LOGIN-009.md) | Fail | #41 | Open |
| FR-22 (UI/UX) | [TC-LOGIN-010](../test-cases/login/TC-LOGIN-010.md) | Fail | #42 | Open |
| SEC-02 (Session) | [TC-LOGIN-011](../test-cases/login/TC-LOGIN-011.md) | Fail | #43 | Open |
| FR-23 (Session Guard) | [TC-LOGIN-012](../test-cases/login/TC-LOGIN-012.md) | Fail | #44 | Open |
| FR-02 (OAuth) | [TC-LOGIN-013](../test-cases/login/TC-LOGIN-013.md) | Fail | #45 | Open |
| FR-02 (Reset attempts) | [TC-LOGIN-013](../test-cases/login/TC-LOGIN-013.md) | Fail | #33 | Open |
| FR-02 (Lockout BVA) | [TC-LOGIN-014](../test-cases/login/TC-LOGIN-014.md) | Fail | #32 | Open |
| FR-02 (Backend validation) | [TC-LOGIN-015](../test-cases/login/TC-LOGIN-015.md) | Fail | None | Open |
| SEC-04 (Security XSS) | [TC-LOGIN-016](../test-cases/login/TC-LOGIN-016.md) | Pass | None | Done |
| FR-24 (Reliability Network) | [TC-LOGIN-017](../test-cases/login/TC-LOGIN-017.md) | Pass | None | Done |
| SEC-01 (Security URL Parameters) | [TC-LOGIN-018](../test-cases/login/TC-LOGIN-018.md) | Pass | None | Done |
| SEC-02 (Security JWT Algorithm) | [TC-LOGIN-019](../test-cases/login/TC-LOGIN-019.md) | Pass | None | Done |
| FR-21 (Keyboard Accessibility) | [TC-LOGIN-020](../test-cases/login/TC-LOGIN-020.md) | Fail | #46 | Open |
| FR-22 (Autofill Compatibility) | [TC-LOGIN-021](../test-cases/login/TC-LOGIN-021.md) | Fail | #46 | Open |
| SEC-01 (Security Request Size) | [TC-LOGIN-022](../test-cases/login/TC-LOGIN-022.md) | Pass | None | Done |
| FR-02 (Lockout BVA Min attempts) | [TC-LOGIN-023](../test-cases/login/TC-LOGIN-023.md) | Fail | #31, #33 | Open |
| FR-02 (Lockout State Reset Success) | [TC-LOGIN-024](../test-cases/login/TC-LOGIN-024.md) | Fail | #33 | Open |
| FR-02 (Lockout Duration BVA) | [TC-LOGIN-025](../test-cases/login/TC-LOGIN-025.md) | Fail | #32 | Open |
| FR-02 (Lockout Security Token) | [TC-LOGIN-026](../test-cases/login/TC-LOGIN-026.md) | Pass | None | Done |
| FR-02 (Lockout Synchronization) | [TC-LOGIN-027](../test-cases/login/TC-LOGIN-027.md) | Pass | None | Done |
| FR-02 (Casing Sensitivity Lockout) | [TC-LOGIN-028](../test-cases/login/TC-LOGIN-028.md) | Pass | None | Done |
| FR-02 (Successful Login Counter) | [TC-LOGIN-029](../test-cases/login/TC-LOGIN-029.md) | Pass | None | Done |
| FR-02 (Lockout Password Reset Clears) | [TC-LOGIN-030](../test-cases/login/TC-LOGIN-030.md) | Fail | #49 | Open |
| FR-02, FR-22 (Email Empty) | [TC-LOGIN-031](../test-cases/login/TC-LOGIN-031.md) | Not Run | None | Open |
| FR-02, FR-22 (Email Spaces) | [TC-LOGIN-032](../test-cases/login/TC-LOGIN-032.md) | Not Run | None | Open |
| FR-02, FR-22 (Email Missing @) | [TC-LOGIN-033](../test-cases/login/TC-LOGIN-033.md) | Not Run | None | Open |
| FR-02, FR-22 (Email Missing Domain) | [TC-LOGIN-034](../test-cases/login/TC-LOGIN-034.md) | Not Run | None | Open |
| FR-02, FR-22 (Email Missing Local) | [TC-LOGIN-035](../test-cases/login/TC-LOGIN-035.md) | Not Run | None | Open |
| FR-02, FR-22 (Email Multi @) | [TC-LOGIN-036](../test-cases/login/TC-LOGIN-036.md) | Not Run | None | Open |
| FR-02, FR-22 (Email Unicode) | [TC-LOGIN-037](../test-cases/login/TC-LOGIN-037.md) | Not Run | None | Open |
| FR-02 (Email Subdomain) | [TC-LOGIN-038](../test-cases/login/TC-LOGIN-038.md) | Not Run | None | Open |
| FR-02, FR-22 (Email Not Exist) | [TC-LOGIN-039](../test-cases/login/TC-LOGIN-039.md) | Not Run | None | Open |
| FR-02, FR-22 (Wrong Password) | [TC-LOGIN-040](../test-cases/login/TC-LOGIN-040.md) | Not Run | None | Open |
| FR-02, FR-22 (Email Mid Space) | [TC-LOGIN-041](../test-cases/login/TC-LOGIN-041.md) | Not Run | None | Open |
| FR-02, FR-22 (Email Length Min-1) | [TC-LOGIN-BVA-001](../test-cases/login/TC-LOGIN-BVA-001.md) | Not Run | None | Open |
| FR-02 (Email Length Min) | [TC-LOGIN-BVA-002](../test-cases/login/TC-LOGIN-BVA-002.md) | Not Run | None | Open |
| FR-02 (Email Length Min+1) | [TC-LOGIN-BVA-003](../test-cases/login/TC-LOGIN-BVA-003.md) | Not Run | None | Open |
| FR-02 (Email Length Max-1) | [TC-LOGIN-BVA-004](../test-cases/login/TC-LOGIN-BVA-004.md) | Not Run | None | Open |
| FR-02 (Email Length Max) | [TC-LOGIN-BVA-005](../test-cases/login/TC-LOGIN-BVA-005.md) | Not Run | None | Open |
| FR-02, FR-22 (Email Length Max+1) | [TC-LOGIN-BVA-006](../test-cases/login/TC-LOGIN-BVA-006.md) | Not Run | None | Open |
| FR-02, FR-22 (Password Length Min-1) | [TC-LOGIN-BVA-007](../test-cases/login/TC-LOGIN-BVA-007.md) | Not Run | None | Open |
| FR-02 (Password Length Min) | [TC-LOGIN-BVA-008](../test-cases/login/TC-LOGIN-BVA-008.md) | Not Run | None | Open |
| FR-02 (Password Length Min+1) | [TC-LOGIN-BVA-009](../test-cases/login/TC-LOGIN-BVA-009.md) | Not Run | None | Open |
| FR-02 (Password Length Max-1) | [TC-LOGIN-BVA-010](../test-cases/login/TC-LOGIN-BVA-010.md) | Not Run | None | Open |
| FR-02 (Password Length Max) | [TC-LOGIN-BVA-011](../test-cases/login/TC-LOGIN-BVA-011.md) | Not Run | None | Open |
| FR-02, FR-22 (Password Length Max+1) | [TC-LOGIN-BVA-012](../test-cases/login/TC-LOGIN-BVA-012.md) | Not Run | None | Open |
| FR-02 (Lockout 1 Attempt) | [TC-LOCK-BVA-001](../test-cases/login/TC-LOCK-BVA-001.md) | Not Run | None | Open |
| FR-02 (Lockout Out Window) | [TC-LOCK-BVA-002](../test-cases/login/TC-LOCK-BVA-002.md) | Not Run | None | Open |
| FR-02 (Lockout Exactly 30s) | [TC-LOCK-BVA-003](../test-cases/login/TC-LOCK-BVA-003.md) | Not Run | None | Open |
| FR-02 (Lockout Reset after Duration) | [TC-LOCK-BVA-004](../test-cases/login/TC-LOCK-BVA-004.md) | Not Run | None | Open |
| FR-02, SEC-02 (Lockout Concurrent) | [TC-LOCK-BVA-005](../test-cases/login/TC-LOCK-BVA-005.md) | Not Run | None | Open |
| FR-02 (Lockout End Match) | [TC-LOCK-BVA-006](../test-cases/login/TC-LOCK-BVA-006.md) | Not Run | None | Open |
| FR-02 (Lockout Post-Lock Failures) | [TC-LOCK-BVA-007](../test-cases/login/TC-LOCK-BVA-007.md) | Not Run | None | Open |
| SEC-02 (JWT Missing Exp) | [TC-JWT-001](../test-cases/login/TC-JWT-001.md) | Not Run | None | Open |
| SEC-02 (JWT Expired) | [TC-JWT-002](../test-cases/login/TC-JWT-002.md) | Not Run | None | Open |
| SEC-02 (JWT Tampered) | [TC-JWT-003](../test-cases/login/TC-JWT-003.md) | Not Run | None | Open |
| SEC-02 (JWT Bad Key) | [TC-JWT-004](../test-cases/login/TC-JWT-004.md) | Not Run | None | Open |
| SEC-01 (JWT URL Exposure) | [TC-JWT-005](../test-cases/login/TC-JWT-005.md) | Not Run | None | Open |
| FR-02 (JWT Multiple Login) | [TC-JWT-006](../test-cases/login/TC-JWT-006.md) | Not Run | None | Open |
| FR-22 (Error Email Not Exist) | [TC-ERR-001](../test-cases/login/TC-ERR-001.md) | Not Run | None | Open |
| FR-22 (Error Wrong Password) | [TC-ERR-002](../test-cases/login/TC-ERR-002.md) | Not Run | None | Open |
| FR-22 (Error Account Locked) | [TC-ERR-003](../test-cases/login/TC-ERR-003.md) | Not Run | None | Open |
| FR-22 (Error Account Disabled) | [TC-ERR-004](../test-cases/login/TC-ERR-004.md) | Not Run | None | Open |
| FR-24 (Error HTTP 500 Friendliness) | [TC-ERR-005](../test-cases/login/TC-ERR-005.md) | Not Run | None | Open |
| FR-22 (Error Multi-field Validation) | [TC-ERR-006](../test-cases/login/TC-ERR-006.md) | Not Run | None | Open |
| FR-22, FR-24 (Error Tech Exposure) | [TC-ERR-007](../test-cases/login/TC-ERR-007.md) | Not Run | None | Open |
| SEC-01 (API Missing Email) | [TC-API-001](../test-cases/login/TC-API-001.md) | Pass | None | Done |
| SEC-01 (API Missing Password) | [TC-API-002](../test-cases/login/TC-API-002.md) | Pass | None | Done |
| SEC-01 (API Invalid JSON format) | [TC-API-003](../test-cases/login/TC-API-003.md) | Not Run | None | Open |
| SEC-01 (API Invalid Content-Type) | [TC-API-004](../test-cases/login/TC-API-004.md) | Not Run | None | Open |
| SEC-01 (API Extra fields ignore) | [TC-API-005](../test-cases/login/TC-API-005.md) | Not Run | None | Open |
| SEC-01 (API Success response schema) | [TC-API-006](../test-cases/login/TC-API-006.md) | Not Run | None | Open |
| SEC-01 (API Fail response schema) | [TC-API-007](../test-cases/login/TC-API-007.md) | Not Run | None | Open |
| FR-07 (Giỏ hàng Web) | [TC-CART-001](../test-cases/cart/TC-CART-001.md) | Pass |  | Done |
| FR-07, FR-24 | [TC-CART-002](../test-cases/cart/TC-CART-002.md) | Fail | BUG-FR07-B-08 | Ready for Retest |
| FR-07, FR-23 | [TC-CART-003](../test-cases/cart/TC-CART-003.md) | Pass |  | Done |
| FR-23 (Navigation) | [TC-CART-004](../test-cases/cart/TC-CART-004.md) | Fail | BUG-FR07-B-09 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-005](../test-cases/cart/TC-CART-005.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-006](../test-cases/cart/TC-CART-006.md) | Fail | BUG-FR07-B-07 | Ready for Retest |
| FR-07, FR-21 | [TC-CART-007](../test-cases/cart/TC-CART-007.md) | Pass |  | Done |
| FR-07, FR-21 | [TC-CART-008](../test-cases/cart/TC-CART-008.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-009](../test-cases/cart/TC-CART-009.md) | Fail | BUG-FR07-B-06 | Ready for Retest |
| FR-07, FR-23, FR-24 | [TC-CART-010](../test-cases/cart/TC-CART-010.md) | Pass |  | Done |
| FR-07, FR-24 | [TC-CART-011](../test-cases/cart/TC-CART-011.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-012](../test-cases/cart/TC-CART-012.md) | Fail | BUG-FR07-B-03 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-013](../test-cases/cart/TC-CART-013.md) | Fail | BUG-FR07-B-03 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-014](../test-cases/cart/TC-CART-014.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-015](../test-cases/cart/TC-CART-015.md) | Fail | BUG-FR07-B-04 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-016](../test-cases/cart/TC-CART-016.md) | Fail | BUG-FR07-B-04 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-017](../test-cases/cart/TC-CART-017.md) | Fail | BUG-FR07-B-04 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-018](../test-cases/cart/TC-CART-018.md) | Fail | BUG-FR07-B-04 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-019](../test-cases/cart/TC-CART-019.md) | Fail | BUG-FR07-B-04 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-020](../test-cases/cart/TC-CART-020.md) | Fail | BUG-FR07-B-04 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-021](../test-cases/cart/TC-CART-021.md) | Fail | BUG-FR07-B-04 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-022](../test-cases/cart/TC-CART-022.md) | Fail | BUG-FR07-B-04 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-023](../test-cases/cart/TC-CART-023.md) | Fail | BUG-FR07-B-04 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-024](../test-cases/cart/TC-CART-024.md) | Fail | BUG-FR07-B-04 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-025](../test-cases/cart/TC-CART-025.md) | Fail | BUG-FR07-B-04 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-026](../test-cases/cart/TC-CART-026.md) | Fail | BUG-FR07-B-04 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-027](../test-cases/cart/TC-CART-027.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-028](../test-cases/cart/TC-CART-028.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-029](../test-cases/cart/TC-CART-029.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-030](../test-cases/cart/TC-CART-030.md) | Pass |  | Done |
| FR-07, FR-24 | [TC-CART-031](../test-cases/cart/TC-CART-031.md) | Fail | BUG-FR07-B-05 | Ready for Retest |
| FR-07, FR-24 | [TC-CART-032](../test-cases/cart/TC-CART-032.md) | Fail | BUG-FR07-B-05 | Ready for Retest |
| FR-07, FR-24 | [TC-CART-033](../test-cases/cart/TC-CART-033.md) | Fail | BUG-FR07-B-05 | Ready for Retest |
| FR-07, FR-24 | [TC-CART-034](../test-cases/cart/TC-CART-034.md) | Fail | BUG-FR07-B-05 | Ready for Retest |
| FR-23 (Navigation) | [TC-CART-035](../test-cases/cart/TC-CART-035.md) | Pass |  | Done |
| FR-23, FR-24 | [TC-CART-036](../test-cases/cart/TC-CART-036.md) | Pass |  | Done |
| FR-23 (Navigation) | [TC-CART-037](../test-cases/cart/TC-CART-037.md) | Fail | BUG-FR07-B-04 | Ready for Retest |
| FR-23 (Navigation) | [TC-CART-038](../test-cases/cart/TC-CART-038.md) | Pass |  | Done |
| FR-24 (Feedback) | [TC-CART-039](../test-cases/cart/TC-CART-039.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-040](../test-cases/cart/TC-CART-040.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-041](../test-cases/cart/TC-CART-041.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-042](../test-cases/cart/TC-CART-042.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-043](../test-cases/cart/TC-CART-043.md) | Fail | BUG-FR07-B-02 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-044](../test-cases/cart/TC-CART-044.md) | Fail | BUG-FR07-B-01 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-045](../test-cases/cart/TC-CART-045.md) | Fail | BUG-FR07-B-01 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-046](../test-cases/cart/TC-CART-046.md) | Fail | BUG-FR07-B-01 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-047](../test-cases/cart/TC-CART-047.md) | Fail | BUG-FR07-B-01 | Ready for Retest |

