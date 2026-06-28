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
| FR-07, FR-24 | [TC-CART-002](../test-cases/cart/TC-CART-002.md) | Fail | BUG-FR07-B-07 | Ready for Retest |
| FR-07, FR-23 | [TC-CART-003](../test-cases/cart/TC-CART-003.md) | Pass |  | Done |
| FR-23 (Navigation) | [TC-CART-004](../test-cases/cart/TC-CART-004.md) | Fail | BUG-FR07-B-08 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-005](../test-cases/cart/TC-CART-005.md) | Pass |  | Done |
| FR-07, FR-21 | [TC-CART-006](../test-cases/cart/TC-CART-006.md) | Pass |  | Done |
| FR-07, FR-21 | [TC-CART-007](../test-cases/cart/TC-CART-007.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-008](../test-cases/cart/TC-CART-008.md) | Fail |  | Ready for Retest |
| FR-07, FR-23, FR-24 | [TC-CART-009](../test-cases/cart/TC-CART-009.md) | Fail | BUG-FR07-B-06 | Ready for Retest |
| FR-07, FR-24 | [TC-CART-010](../test-cases/cart/TC-CART-010.md) | Fail | BUG-FR07-B-11 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-011](../test-cases/cart/TC-CART-011.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-012](../test-cases/cart/TC-CART-012.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-013](../test-cases/cart/TC-CART-013.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-014](../test-cases/cart/TC-CART-014.md) | Fail |  | Ready for Retest |
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
| FR-07 (Giỏ hàng Web) | [TC-CART-026](../test-cases/cart/TC-CART-026.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-027](../test-cases/cart/TC-CART-027.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-028](../test-cases/cart/TC-CART-028.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-029](../test-cases/cart/TC-CART-029.md) | Pass |  | Done |
| FR-07, FR-24 | [TC-CART-030](../test-cases/cart/TC-CART-030.md) | Fail |  | Ready for Retest |
| FR-07, FR-24 | [TC-CART-031](../test-cases/cart/TC-CART-031.md) | Fail | BUG-FR07-B-05 | Ready for Retest |
| FR-07, FR-24 | [TC-CART-032](../test-cases/cart/TC-CART-032.md) | Fail | BUG-FR07-B-05 | Ready for Retest |
| FR-07, FR-24 | [TC-CART-033](../test-cases/cart/TC-CART-033.md) | Fail | BUG-FR07-B-05 | Ready for Retest |
| FR-23 (Navigation) | [TC-CART-034](../test-cases/cart/TC-CART-034.md) | Pass |  | Done |
| FR-23, FR-24 | [TC-CART-035](../test-cases/cart/TC-CART-035.md) | Pass |  | Done |
| FR-23 (Navigation) | [TC-CART-036](../test-cases/cart/TC-CART-036.md) | Fail |  | Ready for Retest |
| FR-23 (Navigation) | [TC-CART-037](../test-cases/cart/TC-CART-037.md) | Pass |  | Done |
| FR-24 (Feedback) | [TC-CART-038](../test-cases/cart/TC-CART-038.md) | Fail | BUG-FR07-B-11 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-039](../test-cases/cart/TC-CART-039.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-040](../test-cases/cart/TC-CART-040.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-041](../test-cases/cart/TC-CART-041.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-042](../test-cases/cart/TC-CART-042.md) | Pass |  | Done |
| FR-07 (Giỏ hàng Web) | [TC-CART-043](../test-cases/cart/TC-CART-043.md) | Fail | BUG-FR07-B-02 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-044](../test-cases/cart/TC-CART-044.md) | Fail | BUG-FR07-B-01 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-045](../test-cases/cart/TC-CART-045.md) | Fail | BUG-FR07-B-01 | Ready for Retest |
| FR-07 (Giỏ hàng Web) | [TC-CART-046](../test-cases/cart/TC-CART-046.md) | Fail | BUG-FR07-B-01 | Ready for Retest |
| FR-07, FR-23 | [TC-CART-047](../test-cases/cart/TC-CART-047.md) | Fail | BUG-FR07-B-01 | Ready for Retest |
| FR-07, FR-23 | [TC-CART-048](../test-cases/cart/TC-CART-048.md) | Pass |  | Done |
| FR-07 | [TC-CART-049](../test-cases/cart/TC-CART-049.md) | Pass |  | Done |
| FR-07 | [TC-CART-050](../test-cases/cart/TC-CART-050.md) | Pass |  | Done |
| FR-07, FR-24 | [TC-CART-051](../test-cases/cart/TC-CART-051.md) | Fail | BUG-FR07-B-10 | Ready for Retest |
| FR-07, FR-24 | [TC-CART-052](../test-cases/cart/TC-CART-052.md) | Fail |  | Ready for Retest |
| FR-07 | [TC-CART-053](../test-cases/cart/TC-CART-053.md) | Fail | BUG-FR07-B-10 | Ready for Retest |
| FR-07, FR-24 | [TC-CART-054](../test-cases/cart/TC-CART-054.md) | Pass |  | Done |
| FR-07, FR-21 | [TC-CART-055](../test-cases/cart/TC-CART-055.md) | Pass |  | Done |
| FR-07, SEC-04 | [TC-CART-056](../test-cases/cart/TC-CART-056.md) | Pass |  | Done |
| FR-07 | [TC-CART-057](../test-cases/cart/TC-CART-057.md) | Fail | BUG-FR07-B-10 | Ready for Retest |
| FR-07 | [TC-CART-058](../test-cases/cart/TC-CART-058.md) | Fail | BUG-FR07-B-10 | Ready for Retest |
| FR-07 | [TC-CART-059](../test-cases/cart/TC-CART-059.md) | Fail | BUG-FR07-B-10 | Ready for Retest |
| FR-07 | [TC-CART-060](../test-cases/cart/TC-CART-060.md) | Fail | BUG-FR07-B-12 | Ready for Retest |
| FR-07 | [TC-CART-061](../test-cases/cart/TC-CART-061.md) | Fail | BUG-FR07-B-14 | Ready for Retest |
| FR-07 | [TC-CART-062](../test-cases/cart/TC-CART-062.md) | Fail | BUG-FR07-B-14 | Ready for Retest |
| FR-07 | [TC-CART-063](../test-cases/cart/TC-CART-063.md) | Fail | BUG-FR07-B-13 | Ready for Retest |
| FR-07 | [TC-CART-064](../test-cases/cart/TC-CART-064.md) | Fail | BUG-FR07-B-13 | Ready for Retest |
| FR-07 | [TC-CART-065](../test-cases/cart/TC-CART-065.md) | Fail | BUG-FR07-B-15 | Ready for Retest |
| FR-07 | [TC-CART-066](../test-cases/cart/TC-CART-066.md) | Fail | BUG-FR07-B-15 | Ready for Retest |
| FR-07 | [TC-CART-067](../test-cases/cart/TC-CART-067.md) | Fail | BUG-FR07-B-15 | Ready for Retest |
| FR-07 | [TC-CART-068](../test-cases/cart/TC-CART-068.md) | Fail | BUG-FR07-B-15 | Ready for Retest |
| FR-07 | [TC-CART-069](../test-cases/cart/TC-CART-069.md) | Pass |  | Done |
| FR-07 | [TC-CART-070](../test-cases/cart/TC-CART-070.md) | Fail | BUG-FR07-B-16 | Ready for Retest |
| FR-07 | [TC-CART-071](../test-cases/cart/TC-CART-071.md) | Pass |  | Done |
| FR-07 | [TC-CART-072](../test-cases/cart/TC-CART-072.md) | Pass |  | Done |
| FR-07 | [TC-CART-073](../test-cases/cart/TC-CART-073.md) | Pass |  | Done |
| FR-07 | [TC-CART-074](../test-cases/cart/TC-CART-074.md) | Fail | BUG-FR07-B-11 | Ready for Retest |
| FR-07 | [TC-CART-075](../test-cases/cart/TC-CART-075.md) | Fail | BUG-FR07-B-05 | Ready for Retest |
| FR-07 | [TC-CART-076](../test-cases/cart/TC-CART-076.md) | Fail | BUG-FR07-B-17 | Ready for Retest |
| FR-07 | [TC-CART-077](../test-cases/cart/TC-CART-077.md) | Fail | BUG-FR07-B-17 | Ready for Retest |
| FR-07 | [TC-CART-078](../test-cases/cart/TC-CART-078.md) | Fail | BUG-FR07-B-14 | Ready for Retest |
| FR-07 | [TC-CART-079](../test-cases/cart/TC-CART-079.md) | Fail | BUG-FR07-B-12 | Ready for Retest |
| FR-07 | [TC-CART-080](../test-cases/cart/TC-CART-080.md) | Fail | BUG-FR07-B-13 | Ready for Retest |
| FR-07 | [TC-CART-081](../test-cases/cart/TC-CART-081.md) | Pass |  | Done |
| FR-07 | [TC-CART-082](../test-cases/cart/TC-CART-082.md) | Pass |  | Done |
| FR-07 | [TC-CART-083](../test-cases/cart/TC-CART-083.md) | Pass |  | Done |
| FR-07 | [TC-CART-084](../test-cases/cart/TC-CART-084.md) | Pass |  | Done |
| FR-07 | [TC-CART-085](../test-cases/cart/TC-CART-085.md) | Pass |  | Done |
| FR-07 | [TC-CART-086](../test-cases/cart/TC-CART-086.md) | Pass |  | Done |
| FR-07 | [TC-CART-087](../test-cases/cart/TC-CART-087.md) | Pass |  | Done |
| FR-07 | [TC-CART-088](../test-cases/cart/TC-CART-088.md) | Fail |  | Ready for Retest |
| FR-07 | [TC-CART-089](../test-cases/cart/TC-CART-089.md) | Fail | BUG-FR07-B-19 | Ready for Retest |
| FR-07 | [TC-CART-090](../test-cases/cart/TC-CART-090.md) | Fail | BUG-FR07-B-20 | Ready for Retest |
| FR-13 (Dashboard) | [TC-DASHBOARD-DT-001](../test-cases/dashboard/TC-DASHBOARD-DT-001.md) | Fail | BUG-FR13-C-01 | Open |
| FR-13 (Access Guest) | [TC-DASHBOARD-DT-002](../test-cases/dashboard/TC-DASHBOARD-DT-002.md) | Pass | None | Done |
| FR-13 (Access Cust) | [TC-DASHBOARD-DT-003](../test-cases/dashboard/TC-DASHBOARD-DT-003.md) | Pass | None | Done |
| FR-13 (API Auth Check) | [TC-DASHBOARD-DT-004](../test-cases/dashboard/TC-DASHBOARD-DT-004.md) | Fail | BUG-FR13-C-02 | Open |
| FR-13 (Token Change) | [TC-DASHBOARD-DT-005](../test-cases/dashboard/TC-DASHBOARD-DT-005.md) | Pass | None | Done |
| FR-13 (Empty State) | [TC-DASHBOARD-DT-006](../test-cases/dashboard/TC-DASHBOARD-DT-006.md) | Pass | None | Done |
| FR-13 (Non-delivered) | [TC-DASHBOARD-DT-007](../test-cases/dashboard/TC-DASHBOARD-DT-007.md) | Pass | None | Done |
| FR-13 (API Lỗi 500) | [TC-DASHBOARD-DT-008](../test-cases/dashboard/TC-DASHBOARD-DT-008.md) | Pass | None | Done |
| FR-13 (Doanh thu âm) | [TC-DASHBOARD-DT-009](../test-cases/dashboard/TC-DASHBOARD-DT-009.md) | Pass | None | Done |
| FR-13 (Số tiền Null/NaN) | [TC-DASHBOARD-DT-010](../test-cases/dashboard/TC-DASHBOARD-DT-010.md) | Pass | None | Done |
| FR-13 (API Sai Format) | [TC-DASHBOARD-DT-011](../test-cases/dashboard/TC-DASHBOARD-DT-011.md) | Pass | None | Done |
| FR-13 (Responsive UI) | [TC-DASHBOARD-DT-012](../test-cases/dashboard/TC-DASHBOARD-DT-012.md) | Pass | None | Done |
| FR-13 (Order Count BVA Min) | [TC-DASHBOARD-BVA-001](../test-cases/dashboard/TC-DASHBOARD-BVA-001.md) | Pass | None | Done |
| FR-13 (Order Count BVA Min+1) | [TC-DASHBOARD-BVA-002](../test-cases/dashboard/TC-DASHBOARD-BVA-002.md) | Pass | None | Done |
| FR-13 (Order Count BVA Min-1) | [TC-DASHBOARD-BVA-003](../test-cases/dashboard/TC-DASHBOARD-BVA-003.md) | Pass | None | Done |
| FR-13 (Order Count BVA Max) | [TC-DASHBOARD-BVA-004](../test-cases/dashboard/TC-DASHBOARD-BVA-004.md) | Pass | None | Done |
| FR-13 (Revenue BVA Min) | [TC-DASHBOARD-BVA-005](../test-cases/dashboard/TC-DASHBOARD-BVA-005.md) | Pass | None | Done |
| FR-13 (Revenue BVA Min+1) | [TC-DASHBOARD-BVA-006](../test-cases/dashboard/TC-DASHBOARD-BVA-006.md) | Fail | BUG-FR13-C-01 | Open |
| FR-13 (Revenue BVA Min-1) | [TC-DASHBOARD-BVA-007](../test-cases/dashboard/TC-DASHBOARD-BVA-007.md) | Pass | None | Done |
| FR-13 (Revenue BVA Max) | [TC-DASHBOARD-BVA-008](../test-cases/dashboard/TC-DASHBOARD-BVA-008.md) | Pass | None | Done |
| FR-13 (Response Delay BVA Min) | [TC-DASHBOARD-BVA-009](../test-cases/dashboard/TC-DASHBOARD-BVA-009.md) | Pass | None | Done |
| FR-13 (Response Delay BVA Max) | [TC-DASHBOARD-BVA-010](../test-cases/dashboard/TC-DASHBOARD-BVA-010.md) | Pass | None | Done |
| FR-13 (Security API Users) | [TC-DASHBOARD-DT-013](../test-cases/dashboard/TC-DASHBOARD-DT-013.md) | Fail | BUG-FR13-C-02 | Open |
| FR-13 (Security API Orders) | [TC-DASHBOARD-DT-014](../test-cases/dashboard/TC-DASHBOARD-DT-014.md) | Fail | BUG-FR13-C-02 | Open |
| FR-13 (Security Token Tamper) | [TC-DASHBOARD-DT-015](../test-cases/dashboard/TC-DASHBOARD-DT-015.md) | Pass | None | Done |
| FR-13 (Empty Orders Array) | [TC-DASHBOARD-DT-016](../test-cases/dashboard/TC-DASHBOARD-DT-016.md) | Pass | None | Done |
| FR-13 (API Users Error 500) | [TC-DASHBOARD-DT-017](../test-cases/dashboard/TC-DASHBOARD-DT-017.md) | Fail | BUG-FR13-C-03 | Open |
| FR-13 (Pending Orders Only) | [TC-DASHBOARD-DT-018](../test-cases/dashboard/TC-DASHBOARD-DT-018.md) | Pass | None | Done |
| FR-13 (Cancelled Orders Only) | [TC-DASHBOARD-DT-019](../test-cases/dashboard/TC-DASHBOARD-DT-019.md) | Pass | None | Done |
| FR-13 (Missing Field Amount) | [TC-DASHBOARD-DT-020](../test-cases/dashboard/TC-DASHBOARD-DT-020.md) | Fail | BUG-FR13-C-04 | Open |
| FR-13 (Hide API Raw Error) | [TC-DASHBOARD-DT-021](../test-cases/dashboard/TC-DASHBOARD-DT-021.md) | Pass | None | Done |
| FR-13 (Navigation Click) | [TC-DASHBOARD-DT-022](../test-cases/dashboard/TC-DASHBOARD-DT-022.md) | Pass | None | Done |
| FR-13 (Regression Revenue) | [TC-DASHBOARD-DT-023](../test-cases/dashboard/TC-DASHBOARD-DT-023.md) | Fail | BUG-FR13-C-01 | Open |
| FR-13 (Regression Auth) | [TC-DASHBOARD-DT-024](../test-cases/dashboard/TC-DASHBOARD-DT-024.md) | Fail | BUG-FR13-C-02 | Open |
| FR-13 (Recent Orders BVA Min) | [TC-DASHBOARD-BVA-011](../test-cases/dashboard/TC-DASHBOARD-BVA-011.md) | Pass | None | Done |
| FR-13 (Recent Orders BVA Min+1) | [TC-DASHBOARD-BVA-012](../test-cases/dashboard/TC-DASHBOARD-BVA-012.md) | Pass | None | Done |
| FR-13 (Recent Orders BVA Max) | [TC-DASHBOARD-BVA-013](../test-cases/dashboard/TC-DASHBOARD-BVA-013.md) | Pass | None | Done |
| FR-13 (Recent Orders BVA Max+1) | [TC-DASHBOARD-BVA-014](../test-cases/dashboard/TC-DASHBOARD-BVA-014.md) | Pass | None | Done |
| FR-13 (Revenue BVA UI Limit) | [TC-DASHBOARD-BVA-015](../test-cases/dashboard/TC-DASHBOARD-BVA-015.md) | Pass | None | Done |
| FR-13 (Revenue BVA BigInt) | [TC-DASHBOARD-BVA-016](../test-cases/dashboard/TC-DASHBOARD-BVA-016.md) | Pass | None | Done |
| FR-13 (Response Threshold BVA) | [TC-DASHBOARD-BVA-017](../test-cases/dashboard/TC-DASHBOARD-BVA-017.md) | Pass | None | Done |
| FR-13 (Users Count Negative) | [TC-DASHBOARD-BVA-018](../test-cases/dashboard/TC-DASHBOARD-BVA-018.md) | Fail | BUG-FR13-C-05 | Open |
| FR-13 (Products Count Decimal) | [TC-DASHBOARD-BVA-019](../test-cases/dashboard/TC-DASHBOARD-BVA-019.md) | Fail | BUG-FR13-C-05 | Open |
| FR-13 (Responsive Breakpoint) | [TC-DASHBOARD-BVA-020](../test-cases/dashboard/TC-DASHBOARD-BVA-020.md) | Pass | None | Done |
| FR-13 (Responsive Breakpoint-1) | [TC-DASHBOARD-BVA-021](../test-cases/dashboard/TC-DASHBOARD-BVA-021.md) | Pass | None | Done |
| FR-13 (Responsive Breakpoint+1) | [TC-DASHBOARD-BVA-022](../test-cases/dashboard/TC-DASHBOARD-BVA-022.md) | Pass | None | Done |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-DT-001](../test-cases/mobile-cart/TC-MOBILE-CART-DT-001.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-DT-002](../test-cases/mobile-cart/TC-MOBILE-CART-DT-002.md) | Pass | None | Done |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-DT-003](../test-cases/mobile-cart/TC-MOBILE-CART-DT-003.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-DT-004](../test-cases/mobile-cart/TC-MOBILE-CART-DT-004.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-DT-005](../test-cases/mobile-cart/TC-MOBILE-CART-DT-005.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-DT-006](../test-cases/mobile-cart/TC-MOBILE-CART-DT-006.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-DT-007](../test-cases/mobile-cart/TC-MOBILE-CART-DT-007.md) | Not Run | BUG-FR21-D-02 | Open (Issue #162) |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-DT-008](../test-cases/mobile-cart/TC-MOBILE-CART-DT-008.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-DT-009](../test-cases/mobile-cart/TC-MOBILE-CART-DT-009.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-DT-010](../test-cases/mobile-cart/TC-MOBILE-CART-DT-010.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-DT-011](../test-cases/mobile-cart/TC-MOBILE-CART-DT-011.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-DT-012](../test-cases/mobile-cart/TC-MOBILE-CART-DT-012.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-DT-013](../test-cases/mobile-cart/TC-MOBILE-CART-DT-013.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-DT-014](../test-cases/mobile-cart/TC-MOBILE-CART-DT-014.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-DT-015](../test-cases/mobile-cart/TC-MOBILE-CART-DT-015.md) | Not Run | BUG-FR21-D-03 | Open (Issue #163) |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-DT-016](../test-cases/mobile-cart/TC-MOBILE-CART-DT-016.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-DT-017](../test-cases/mobile-cart/TC-MOBILE-CART-DT-017.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-DT-018](../test-cases/mobile-cart/TC-MOBILE-CART-DT-018.md) | Not Run | BUG-FR21-D-04 | Open (Issue #164) |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-DT-019](../test-cases/mobile-cart/TC-MOBILE-CART-DT-019.md) | Not Run | BUG-FR21-D-01 | Open (Issue #161) |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-001](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-001.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-002](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-002.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-003](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-003.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-004](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-004.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-005](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-005.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-006](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-006.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-007](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-007.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-008](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-008.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-009](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-009.md) | Not Run | BUG-FR21-D-03 | Open (Issue #163) |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-010](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-010.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-011](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-011.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-012](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-012.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-013](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-013.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-014](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-014.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-015](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-015.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-016](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-016.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-017](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-017.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-018](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-018.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-019](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-019.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-020](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-020.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-021](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-021.md) | Not Run | None | Open |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-022](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-022.md) | Pass | None | Done |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-BVA-023](../test-cases/mobile-cart/TC-MOBILE-CART-BVA-023.md) | Fail | BUG-FR21-D-05 | Open (Issue #165) |
| FR-21 (Mobile Cart & Checkout) | [TC-MOBILE-CART-DT-020](../test-cases/mobile-cart/TC-MOBILE-CART-DT-020.md) | Fail | BUG-FR21-D-06 | Open (Issue #166) |
