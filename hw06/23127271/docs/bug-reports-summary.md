# Bug reports — HW06 API testing (23127271)

Manual triage of `reports/newman-run.log` (343 requests, 0 automated assertion failures).  
Product bugs below violate **written SRS / SEC requirements** or cause **500 crashes** on in-scope endpoints.

| ID | Title | Severity | Found via | SEC/FR |
|----|-------|----------|-----------|--------|
| [BUG-001](bugs/BUG-001-sec03-user-list-admin-api.md) | Non-admin can list all users | **Critical** | TC-ADMINUSERS-SEC-SUP-002 (Human) | SEC-03 / FR-12 |
| [BUG-002](bugs/BUG-002-sec03-user-delete-admin-api.md) | Non-admin receives success on admin DELETE | **Critical** | TC-ADMINUSERS-SEC-002 (AI) | SEC-03 / FR-12 |
| [BUG-003](bugs/BUG-003-sec06-role-escalation-profile.md) | User can set `role=admin` via profile PUT | **Critical** | TC-PROFILE-SEC-007 (AI) | SEC-06 / FR-04 |
| [BUG-004](bugs/BUG-004-sec01-password-hash-profile-get.md) | GET profile returns password hash | **Critical** | TC-PROFILE-SCH-SUP-003 (Human) | SEC-01 |
| [BUG-005](bugs/BUG-005-fr19-admin-self-delete.md) | Admin can delete own account | **High** | TC-ADMINUSERS-SEC-003 (AI) | FR-19 |
| [BUG-006](bugs/BUG-006-sec02-text-plain-profile-500.md) | Profile PUT with `text/plain` returns 500 | **Medium** | TC-PROFILE-SEC-SUP-004 (Human) | SEC-02 |
| [BUG-007](bugs/BUG-007-cart-negative-quantity.md) | Cart accepts negative quantity | **Medium** | TC-CART-SEC-SUP-002 (Human) | Integrity |
| [BUG-008](bugs/BUG-008-admin-list-schema-overexposure.md) | Admin list exposes undocumented columns | **Medium** | TC-ADMINUSERS-SCH-SUP-001 (Human) | Schema / SEC-01 |

**Evidence source:** Newman log lines cited in each report; root-cause pointers in `Repo/eshop-sut/backend/server.js`.

**Not filed as product bugs** (spec observe-only or test defect):

- Client cart price tampering (`TC-CART-SEC-006`) — FR-08 checkout scope; storing client price not forbidden at POST.
- `TC-ADMINUSERS-SEC-002` DELETE path used literal `<3>` in collection URL — fix collection, re-run for delete impact confirmation.
- `TC-PROFILE-040` — test case audited INVALID (Content-Type rule not in spec); 500 still noted under BUG-006 pattern.

See also: [`docs/newman-execution-summary.md`](newman-execution-summary.md)
