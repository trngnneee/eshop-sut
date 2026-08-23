# Domain Testing Report — FR-04, FR-07, FR-19

**Student:** 23127271  
**SUT:** EShop (`Repo/eshop-sut`) · Base URL `http://localhost:3000`  
**Technique:** Domain testing / equivalence partitioning (Skill-01)  
**Pipeline stage:** API Testing Skill — Stage 1 domain partitions + Stage 2 audit  
**Sources:** `Repo/eshop-sut/README.md` (SRS), `Repo/eshop-sut/api_specification.md`  
**Module codes:** `PROFILE` (FR-04), `CART` (FR-07), `ADMINUSERS` (FR-19)

> Commit each test case file on a feature branch, then open a Pull Request for review before merging to main.

---

## Feature Summary

| FR | Name | Endpoint | Auth |
|----|------|----------|------|
| FR-04 | Quản lý hồ sơ cá nhân | `PUT /api/users/me` | JWT of the profile owner (`Authorization: Bearer <token>`) |
| FR-07 | Giỏ hàng | `POST /api/cart` | JWT of the cart owner |
| FR-19 | Quản lý người dùng (Admin) | `DELETE /api/admin/users/:id` | JWT **and** `role=admin` (FR-12 / SEC-03) |

### Spec rules used (not invented)

**FR-04**
- Logged-in user may update **Họ Tên**, **Số điện thoại**, **Địa chỉ giao hàng mặc định**.
- Phone: starts with `0`, **10–11 digits**.
- Email must not be changed.
- User updates only their own profile; **cannot change `role`** (also SEC-06).
- API body documented as `name`, `shipping_address`, `phone`.

**FR-07** (API surface + rules that constrain the add-to-cart resource)
- Documented body: `id`, `name`, `price`, `quantity`.
- Adding the **same product** increases quantity; it must **not** create a new line.
- FR-06 quantity ≥ 1 applies to the **product-detail UI**, not to `POST /api/cart` (Stage 2: do not reuse it as an API rule).

**FR-19 / FR-12 / SEC-02 / SEC-03**
- Admin may delete users **except the currently logged-in account**.
- `/api/admin/*` requires a valid JWT **and** `role=admin`.
- List/delete responses must **not leak passwords**.

### Stage 2 rule (no invented requirements)

If the spec does not state a field is required, a value is invalid, or a status code, the case is **INVALID** or **INCOMPLETE**, not a reject-on-400 test. Corrected oracles are in each TC file and in `docs/stage2-audit.md`.

Stage 1 had assumed required fields, HTTP 400/401/403/404, FR-06 qty on the cart API, and catalogue price/name matching. Those assumptions were **dropped** in Stage 2.

---

## FR-04 — `PUT /api/users/me` (module `PROFILE`)

### Step 1 · Input variables

| # | Variable | Type | Source |
|---|---|---|---|
| 1 | name | string | JSON body |
| 2 | phone | string | JSON body |
| 3 | shipping_address | string | JSON body |
| 4 | Authorization | string (JWT) | HTTP header |
| 5 | role | string / omitted | JSON body (undocumented extra field) |
| 6 | email | string / omitted | JSON body (undocumented extra field) |
| 7 | request body / Content-Type | JSON object + header | HTTP body / header |

### Steps 2–3 · Domains, sub-domains, representative values

**Variable: `name`**

| Sub-domain ID | Description | Valid / Invalid | Rep. Value |
|---|---|---|---|
| P-NAME-01 | Typical non-empty ASCII name | Valid | Nguyen Van A |
| P-NAME-02 | Vietnamese Unicode name | Valid | Nguyễn Văn Á |
| P-NAME-03 | Empty string | Invalid | "" |
| P-NAME-04 | Whitespace only | Invalid | "   " |
| P-NAME-05 | Field omitted | Unspecified (not stated as required) | (omit name) |
| P-NAME-06 | JSON null | Invalid | null |
| P-NAME-07 | Wrong type (number) | Invalid | 12345 |
| P-NAME-08 | HTML / special characters stored as text | Valid | Nguyen <b>A</b> |
| P-NAME-09 | Very long name (500 chars) | ⚠️ unspecified max | A × 500 |

**Variable: `phone`**

| Sub-domain ID | Description | Valid / Invalid | Rep. Value |
|---|---|---|---|
| P-PHONE-01 | 10 digits starting with 0 (min valid) | Valid | 0912345678 |
| P-PHONE-02 | 11 digits starting with 0 (max valid) | Valid | 09123456789 |
| P-PHONE-03 | 9 digits starting with 0 (min−1) | Invalid | 091234567 |
| P-PHONE-04 | 12 digits starting with 0 (max+1) | Invalid | 091234567890 |
| P-PHONE-05 | 10 digits not starting with 0 | Invalid | 1912345678 |
| P-PHONE-06 | Empty string | Invalid | "" |
| P-PHONE-07 | Field omitted | Unspecified (not stated as required) | (omit phone) |
| P-PHONE-08 | Contains letters | Invalid | 09ab345678 |
| P-PHONE-09 | Contains separators | Invalid | 0912-345-678 |
| P-PHONE-10 | International prefix +84 | Invalid | +84912345678 |
| P-PHONE-11 | Leading/trailing whitespace | Invalid | " 0912345678" |
| P-PHONE-12 | JSON null | Invalid | null |
| P-PHONE-13 | Wrong type (number) | Invalid | 912345678 |
| P-PHONE-14 | Ten zeros (format-valid, ⚠️ not a real subscriber number) | Valid | 0000000000 |

**Variable: `shipping_address`**

| Sub-domain ID | Description | Valid / Invalid | Rep. Value |
|---|---|---|---|
| P-ADDR-01 | Typical Vietnamese street address | Valid | 123 Le Loi, Q1, TP.HCM |
| P-ADDR-02 | Unicode address | Valid | 12 Nguyễn Huệ, Quận 1, TP.HCM |
| P-ADDR-03 | Empty string | Unspecified (no non-empty rule) | "" |
| P-ADDR-04 | Field omitted | Unspecified (not stated as required) | (omit shipping_address) |
| P-ADDR-05 | JSON null | Invalid | null |
| P-ADDR-06 | Very long address (500 chars) | ⚠️ unspecified max | x × 500 |
| P-ADDR-07 | HTML in address (stored as text) | Valid | 123 <script>alert(1)</script> |

**Variable: `Authorization`**

| Sub-domain ID | Description | Valid / Invalid | Rep. Value |
|---|---|---|---|
| P-AUTH-01 | Valid user JWT | Valid | Bearer <user_token> |
| P-AUTH-02 | Valid admin JWT (admin updating own profile) | Valid | Bearer <admin_token> |
| P-AUTH-03 | Header omitted | Invalid | (no Authorization) |
| P-AUTH-04 | Empty Bearer token | Invalid | Bearer  |
| P-AUTH-05 | Malformed JWT | Invalid | Bearer not-a-jwt |
| P-AUTH-06 | Well-formed JWT with invalid signature | Invalid | Bearer <tampered> |

**Variable: `role (business rule FR-04 / SEC-06)`**

| Sub-domain ID | Description | Valid / Invalid | Rep. Value |
|---|---|---|---|
| P-ROLE-01 | role omitted (documented body only) | Valid | (omit) |
| P-ROLE-02 | Client sends role=admin | Invalid | admin |
| P-ROLE-03 | Client sends role=user | Invalid | user |

**Variable: `email (business rule FR-04)`**

| Sub-domain ID | Description | Valid / Invalid | Rep. Value |
|---|---|---|---|
| P-EMAIL-01 | email omitted | Valid | (omit) |
| P-EMAIL-02 | Client sends a new email | Invalid | hijack@example.com |

**Variable: `request body`**

| Sub-domain ID | Description | Valid / Invalid | Rep. Value |
|---|---|---|---|
| P-BODY-01 | Valid JSON object + Content-Type application/json | Valid | {name, phone, shipping_address} |
| P-BODY-02 | Empty HTTP body | Invalid | (empty) |
| P-BODY-03 | Malformed JSON | Invalid | {name: |
| P-BODY-04 | Undocumented extra field (not role/email) | ⚠️ unspecified | {"nickname":"A"} |
| P-BODY-05 | JSON array instead of object | Invalid | [{...}] |
| P-BODY-06 | Content-Type text/plain | Invalid | text/plain |


### Step 4 · Test case summary

**Count:** 40 cases (`TC-PROFILE-001` … `TC-PROFILE-040`)

| TC ID | File | Title | Sub-domains | Type | Expected Result |
|---|---|---|---|---|---|
| TC-PROFILE-001 | `tests/test-cases/profile/TC-PROFILE-001.md` | Update profile with all typical valid values (on-point) | P-NAME-01, P-PHONE-01, P-ADDR-01, P-AUTH-01, P-ROLE-01, P-EMAIL-01, P-BODY-01 | Valid | HTTP 200. Profile is updated. Follow-up GET /api/users/me with the same token returns the new name, phone, and shipping_address. email and role are unchanged. ⚠… |
| TC-PROFILE-002 | `tests/test-cases/profile/TC-PROFILE-002.md` | Phone at 11-digit valid maximum | P-PHONE-02, P-NAME-01, P-ADDR-01, P-AUTH-01 | Valid | HTTP 200. Profile is updated. Follow-up GET /api/users/me with the same token returns the new name, phone, and shipping_address. email and role are unchanged. ⚠… |
| TC-PROFILE-003 | `tests/test-cases/profile/TC-PROFILE-003.md` | Unicode name and unicode address (valid combination at language edge) | P-NAME-02, P-ADDR-02, P-PHONE-02, P-AUTH-01 | Valid | HTTP 200. Profile is updated. Follow-up GET /api/users/me with the same token returns the new name, phone, and shipping_address. email and role are unchanged. ⚠… |
| TC-PROFILE-004 | `tests/test-cases/profile/TC-PROFILE-004.md` | Admin updates own profile with valid fields | P-AUTH-02, P-NAME-01, P-PHONE-01, P-ADDR-01 | Valid | HTTP 200. Profile is updated. Follow-up GET /api/users/me with the same token returns the new name, phone, and shipping_address. email and role are unchanged. ⚠… |
| TC-PROFILE-005 | `tests/test-cases/profile/TC-PROFILE-005.md` | Phone 0000000000 is format-valid per FR-04 | P-PHONE-14, P-NAME-01, P-ADDR-01 | Valid | HTTP 200. Phone persisted as 0000000000. ⚠️ Spec only constrains format (start 0, 10–11 digits), not a real numbering plan. |
| TC-PROFILE-006 | `tests/test-cases/profile/TC-PROFILE-006.md` | HTML in name is accepted as plain profile data | P-NAME-08, P-PHONE-01, P-ADDR-01 | Valid | HTTP 200. name is stored as the literal string Nguyen <b>A</b>. (XSS on UI is SEC-04, not this partition.) |
| TC-PROFILE-007 | `tests/test-cases/profile/TC-PROFILE-007.md` | HTML in shipping_address stored as text | P-ADDR-07, P-NAME-01, P-PHONE-01 | Valid | HTTP 200. shipping_address persisted as the literal submitted string. |
| TC-PROFILE-008 | `tests/test-cases/profile/TC-PROFILE-008.md` | Reject empty name | P-NAME-03, P-PHONE-01, P-ADDR-01, P-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). name is not a usable non-empty string. Follow-up GET /api/users/m… |
| TC-PROFILE-009 | `tests/test-cases/profile/TC-PROFILE-009.md` | Reject whitespace-only name | P-NAME-04, P-PHONE-01, P-ADDR-01, P-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). name is not a usable non-empty string. Follow-up GET /api/users/m… |
| TC-PROFILE-011 | `tests/test-cases/profile/TC-PROFILE-011.md` | Reject name=null | P-NAME-06, P-PHONE-01, P-ADDR-01, P-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). name is not a usable non-empty string. Follow-up GET /api/users/m… |
| TC-PROFILE-012 | `tests/test-cases/profile/TC-PROFILE-012.md` | Reject name with wrong type (number) | P-NAME-07, P-PHONE-01, P-ADDR-01, P-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). name is not a usable non-empty string. Follow-up GET /api/users/m… |
| TC-PROFILE-010 | `tests/test-cases/profile/TC-PROFILE-010.md` | Reject omitted name | P-NAME-05, P-PHONE-01, P-ADDR-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). name is missing. ⚠️ Spec lists Họ Tên as an updatable field; trea… |
| TC-PROFILE-013 | `tests/test-cases/profile/TC-PROFILE-013.md` | Very long name (500 chars) — unspecified max | P-NAME-09, P-PHONE-01, P-ADDR-01 | Valid | ⚠️ Spec does not define a max length. Accept (200, persist all 500 chars) unless a documented limit exists. Record actual SUT behaviour. |
| TC-PROFILE-014 | `tests/test-cases/profile/TC-PROFILE-014.md` | Reject 9-digit phone (min−1) | P-PHONE-03, P-NAME-01, P-ADDR-01, P-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). phone violates FR-04 (must start with 0 and be 10–11 digits). Fol… |
| TC-PROFILE-015 | `tests/test-cases/profile/TC-PROFILE-015.md` | Reject 12-digit phone (max+1) | P-PHONE-04, P-NAME-01, P-ADDR-01, P-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). phone violates FR-04 (must start with 0 and be 10–11 digits). Fol… |
| TC-PROFILE-016 | `tests/test-cases/profile/TC-PROFILE-016.md` | Reject phone not starting with 0 | P-PHONE-05, P-NAME-01, P-ADDR-01, P-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). phone violates FR-04 (must start with 0 and be 10–11 digits). Fol… |
| TC-PROFILE-017 | `tests/test-cases/profile/TC-PROFILE-017.md` | Reject empty phone | P-PHONE-06, P-NAME-01, P-ADDR-01, P-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). phone violates FR-04 (must start with 0 and be 10–11 digits). Fol… |
| TC-PROFILE-019 | `tests/test-cases/profile/TC-PROFILE-019.md` | Reject phone containing letters | P-PHONE-08, P-NAME-01, P-ADDR-01, P-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). phone violates FR-04 (must start with 0 and be 10–11 digits). Fol… |
| TC-PROFILE-020 | `tests/test-cases/profile/TC-PROFILE-020.md` | Reject phone with separators | P-PHONE-09, P-NAME-01, P-ADDR-01, P-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). phone violates FR-04 (must start with 0 and be 10–11 digits). Fol… |
| TC-PROFILE-021 | `tests/test-cases/profile/TC-PROFILE-021.md` | Reject +84 international phone | P-PHONE-10, P-NAME-01, P-ADDR-01, P-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). phone violates FR-04 (must start with 0 and be 10–11 digits). Fol… |
| TC-PROFILE-022 | `tests/test-cases/profile/TC-PROFILE-022.md` | Reject phone with leading whitespace | P-PHONE-11, P-NAME-01, P-ADDR-01, P-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). phone violates FR-04 (must start with 0 and be 10–11 digits). Fol… |
| TC-PROFILE-018 | `tests/test-cases/profile/TC-PROFILE-018.md` | Reject omitted phone | P-PHONE-07, P-NAME-01, P-ADDR-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). phone is missing. ⚠️ Treated as required because FR-04 lists it a… |
| TC-PROFILE-023 | `tests/test-cases/profile/TC-PROFILE-023.md` | Reject phone=null | P-PHONE-12, P-NAME-01, P-ADDR-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). phone is null. Follow-up GET /api/users/me shows name, phone, shi… |
| TC-PROFILE-024 | `tests/test-cases/profile/TC-PROFILE-024.md` | Reject phone with wrong type (number) | P-PHONE-13, P-NAME-01, P-ADDR-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). phone is not a digit string starting with 0. Follow-up GET /api/u… |
| TC-PROFILE-025 | `tests/test-cases/profile/TC-PROFILE-025.md` | Reject empty shipping_address | P-ADDR-03, P-NAME-01, P-PHONE-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). shipping_address is empty. ⚠️ Spec does not say required; treated… |
| TC-PROFILE-026 | `tests/test-cases/profile/TC-PROFILE-026.md` | Reject omitted shipping_address | P-ADDR-04, P-NAME-01, P-PHONE-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). shipping_address is missing. ⚠️ Assumed required. Follow-up GET /… |
| TC-PROFILE-027 | `tests/test-cases/profile/TC-PROFILE-027.md` | Reject shipping_address=null | P-ADDR-05, P-NAME-01, P-PHONE-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). shipping_address is null. Follow-up GET /api/users/me shows name,… |
| TC-PROFILE-028 | `tests/test-cases/profile/TC-PROFILE-028.md` | Very long shipping_address (500 chars) — unspecified max | P-ADDR-06, P-NAME-01, P-PHONE-01 | Valid | ⚠️ Spec does not define a max length. Accept (200, persist) unless a documented limit exists. |
| TC-PROFILE-029 | `tests/test-cases/profile/TC-PROFILE-029.md` | Reject update with no Authorization header | P-AUTH-03 | Invalid | HTTP 401 Unauthorized (SEC-02: protected API requires a valid JWT). Profile is not updated. |
| TC-PROFILE-030 | `tests/test-cases/profile/TC-PROFILE-030.md` | Reject empty Bearer token | P-AUTH-04 | Invalid | HTTP 401 Unauthorized (SEC-02: protected API requires a valid JWT) (empty token is not a valid JWT). |
| TC-PROFILE-031 | `tests/test-cases/profile/TC-PROFILE-031.md` | Reject malformed JWT | P-AUTH-05 | Invalid | HTTP 403 Forbidden or 401. Profile is not updated. |
| TC-PROFILE-032 | `tests/test-cases/profile/TC-PROFILE-032.md` | Reject JWT with invalid signature | P-AUTH-06 | Invalid | HTTP 403 Forbidden. Profile is not updated. |
| TC-PROFILE-033 | `tests/test-cases/profile/TC-PROFILE-033.md` | Reject or ignore role=admin in profile body (SEC-06) | P-ROLE-02, P-NAME-01, P-PHONE-01, P-ADDR-01, P-AUTH-01 | Invalid | Request is rejected (4xx) OR extra field is ignored. Either way, role remains user. If name/phone/address were applied while role was silently changed, that is … |
| TC-PROFILE-034 | `tests/test-cases/profile/TC-PROFILE-034.md` | Reject or ignore role=user when sent by client | P-ROLE-03, P-AUTH-01 | Invalid | role is not client-writable. Profile update of documented fields may succeed, but the API must not treat role as a mutable body field. GET shows role unchanged … |
| TC-PROFILE-035 | `tests/test-cases/profile/TC-PROFILE-035.md` | Reject email change via PUT /api/users/me | P-EMAIL-02, P-NAME-01, P-PHONE-01, P-ADDR-01 | Invalid | email remains test@eshop.com. Request is rejected or email is ignored. FR-04: email must not be changed. |
| TC-PROFILE-036 | `tests/test-cases/profile/TC-PROFILE-036.md` | Reject empty HTTP body | P-BODY-02, P-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). body is empty. Follow-up GET /api/users/me shows name, phone, shi… |
| TC-PROFILE-037 | `tests/test-cases/profile/TC-PROFILE-037.md` | Reject malformed JSON body | P-BODY-03, P-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). body is not valid JSON. Follow-up GET /api/users/me shows name, p… |
| TC-PROFILE-038 | `tests/test-cases/profile/TC-PROFILE-038.md` | Undocumented extra field nickname — unspecified | P-BODY-04, P-NAME-01, P-PHONE-01, P-ADDR-01 | Valid | ⚠️ Spec does not define extra-field policy. Documented fields should update. nickname must not become a persisted column / privilege. Record actual behaviour. |
| TC-PROFILE-039 | `tests/test-cases/profile/TC-PROFILE-039.md` | Reject JSON array body | P-BODY-05, P-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). body is not a JSON object. Follow-up GET /api/users/me shows name… |
| TC-PROFILE-040 | `tests/test-cases/profile/TC-PROFILE-040.md` | Reject Content-Type text/plain | P-BODY-06, P-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). Content-Type is not application/json. ⚠️ Spec implies JSON body. … |

---

## FR-07 — `POST /api/cart` (module `CART`)

### Step 1 · Input variables

| # | Variable | Type | Source |
|---|---|---|---|
| 1 | id | integer (product id) | JSON body |
| 2 | quantity | integer | JSON body |
| 3 | price | number | JSON body |
| 4 | name | string | JSON body |
| 5 | Authorization | string (JWT) | HTTP header |
| 6 | cart state (same product already present) | state | server-side cart for the authenticated user |
| 7 | request body / Content-Type | JSON object + header | HTTP body / header |

### Steps 2–3 · Domains, sub-domains, representative values

**Variable: `id`**

| Sub-domain ID | Description | Valid / Invalid | Rep. Value |
|---|---|---|---|
| C-ID-01 | Existing seed product id=1 | Valid | 1 |
| C-ID-02 | Existing seed product id=5 (last seed) | Valid | 5 |
| C-ID-03 | Zero | Unspecified (no id rule) | 0 |
| C-ID-04 | Negative | Unspecified (no id rule) | -1 |
| C-ID-05 | Non-existent product | Unspecified (existence not required) | 99999 |
| C-ID-06 | Field omitted | Unspecified (not stated as required) | (omit id) |
| C-ID-07 | Numeric string | Unspecified (coercion not stated) | "1" |
| C-ID-08 | JSON null | Unspecified (null not stated invalid) | null |
| C-ID-09 | Non-integer (float) | Unspecified (type not stated) | 1.5 |
| C-ID-10 | Non-numeric string | Unspecified (type not stated) | "abc" |

**Variable: `quantity`**

| Sub-domain ID | Description | Valid / Invalid | Rep. Value |
|---|---|---|---|
| C-QTY-01 | Typical quantity 1 (FR-06 is product-detail UI, not this API) | Valid (typical value only) | 1 |
| C-QTY-02 | Typical quantity | Valid | 2 |
| C-QTY-03 | Larger typical quantity | Valid (no max stated) | 10 |
| C-QTY-04 | Zero | Unspecified (FR-06 is not this API) | 0 |
| C-QTY-05 | Negative | Unspecified (not stated for this API) | -1 |
| C-QTY-06 | Field omitted | Unspecified (not stated as required) | (omit quantity) |
| C-QTY-07 | Non-integer (float) | Unspecified (type not stated) | 1.5 |
| C-QTY-08 | Numeric string | Unspecified (coercion not stated) | "2" |
| C-QTY-09 | JSON null | Unspecified (null not stated invalid) | null |
| C-QTY-10 | Extremely large quantity | Unspecified (no max stated) | 999999999 |

**Variable: `price`**

| Sub-domain ID | Description | Valid / Invalid | Rep. Value |
|---|---|---|---|
| C-PRICE-01 | Positive price as in the API example | Valid | 30000000 |
| C-PRICE-02 | Zero | Unspecified (FR-15 > 0 is product CRUD, not this API) | 0 |
| C-PRICE-03 | Negative | Unspecified (not stated for this API) | -1 |
| C-PRICE-04 | Field omitted | Unspecified (not stated as required) | (omit price) |
| C-PRICE-05 | Numeric string | Unspecified (coercion not stated) | "30000000" |
| C-PRICE-06 | JSON null | Unspecified (null not stated invalid) | null |
| C-PRICE-07 | Price does not match catalogue for id | Unspecified (FR-08 is checkout `total_amount`, not cart price) | 1 |

**Variable: `name`**

| Sub-domain ID | Description | Valid / Invalid | Rep. Value |
|---|---|---|---|
| C-NAME-01 | Name matching catalogue for id | Valid | iPhone 15 Pro Max |
| C-NAME-02 | Empty string |  Unspecified (no non-empty rule) | "" |
| C-NAME-03 | Field omitted | Unspecified (not stated as required) | (omit name) |
| C-NAME-04 | Name does not match id | ⚠️ unspecified | Not This Product |
| C-NAME-05 | Unicode name matching catalogue id=5 | Valid | Bàn phím cơ Keychron Q1 |

**Variable: `Authorization`**

| Sub-domain ID | Description | Valid / Invalid | Rep. Value |
|---|---|---|---|
| C-AUTH-01 | Valid user JWT | Valid | Bearer <user_token> |
| C-AUTH-02 | Valid admin JWT (admin may also have a cart) | Valid | Bearer <admin_token> |
| C-AUTH-03 | Header omitted | Invalid | (no Authorization) |
| C-AUTH-04 | Empty Bearer token | Invalid | Bearer  |
| C-AUTH-05 | Malformed JWT | Invalid | Bearer not-a-jwt |

**Variable: `cart state (FR-07 merge rule)`**

| Sub-domain ID | Description | Valid / Invalid | Rep. Value |
|---|---|---|---|
| C-STATE-01 | Cart empty; add a product | Valid | empty → 1 line |
| C-STATE-02 | Same product already in cart | Valid (merge) | qty increases, no new line |
| C-STATE-03 | Different product already in cart | Valid (new line) | 2 distinct lines |

**Variable: `request body`**

| Sub-domain ID | Description | Valid / Invalid | Rep. Value |
|---|---|---|---|
| C-BODY-01 | Valid JSON object | Valid | {id,name,price,quantity} |
| C-BODY-02 | Empty HTTP body | Invalid | (empty) |
| C-BODY-03 | Malformed JSON | Invalid | {id: |
| C-BODY-04 | JSON array | Invalid | [{...}] |
| C-BODY-05 | Extra undocumented field | ⚠️ unspecified | {"color":"red"} |
| C-BODY-06 | Content-Type text/plain | Invalid | text/plain |


### Step 4 · Test case summary

**Count:** 39 cases (`TC-CART-001` … `TC-CART-039`)

| TC ID | File | Title | Sub-domains | Type | Expected Result |
|---|---|---|---|---|---|
| TC-CART-001 | `tests/test-cases/cart/TC-CART-001.md` | Add existing product with typical valid body (on-point) | C-ID-01, C-QTY-02, C-PRICE-01, C-NAME-01, C-AUTH-01, C-STATE-01, C-BODY-01 | Valid | HTTP 200. ⚠️ Success body is not documented; SUT currently returns {"message": "Added to cart"}. Follow-up GET /api/cart as the same user shows the line item wi… |
| TC-CART-002 | `tests/test-cases/cart/TC-CART-002.md` | Add with quantity=1 (FR-06 minimum) and id=1 (valid min combination) | C-QTY-01, C-ID-01, C-PRICE-01, C-NAME-01, C-AUTH-01 | Valid | HTTP 200. ⚠️ Success body is not documented; SUT currently returns {"message": "Added to cart"}. Follow-up GET /api/cart as the same user shows the line item wi… |
| TC-CART-003 | `tests/test-cases/cart/TC-CART-003.md` | Add last seed product id=5 with matching unicode name | C-ID-02, C-NAME-05, C-QTY-02, C-AUTH-01 | Valid | HTTP 200. ⚠️ Success body is not documented; SUT currently returns {"message": "Added to cart"}. Follow-up GET /api/cart as the same user shows the line item wi… |
| TC-CART-004 | `tests/test-cases/cart/TC-CART-004.md` | Quantity=10 (valid, no documented max) | C-QTY-03, C-ID-01, C-AUTH-01 | Valid | HTTP 200. ⚠️ Success body is not documented; SUT currently returns {"message": "Added to cart"}. Follow-up GET /api/cart as the same user shows the line item wi… |
| TC-CART-005 | `tests/test-cases/cart/TC-CART-005.md` | Admin JWT can add to the admin's own cart | C-AUTH-02, C-ID-01, C-QTY-01 | Valid | HTTP 200. ⚠️ Success body is not documented; SUT currently returns {"message": "Added to cart"}. Follow-up GET /api/cart as the same user shows the line item wi… |
| TC-CART-006 | `tests/test-cases/cart/TC-CART-006.md` | Adding the same product again merges quantity (FR-07) | C-STATE-02, C-ID-01, C-QTY-01, C-AUTH-01 | Valid | HTTP 200. GET /api/cart shows exactly one line for product 1 with quantity 2 (merged). A second row for the same product is a fail (FR-07). |
| TC-CART-007 | `tests/test-cases/cart/TC-CART-007.md` | Adding a different product creates a new line | C-STATE-03, C-ID-01, C-ID-02, C-AUTH-01 | Valid | HTTP 200. Cart contains two distinct lines (id=1 and id=2). Product 1 quantity is unchanged. |
| TC-CART-008 | `tests/test-cases/cart/TC-CART-008.md` | Reject product id=0 | C-ID-03, C-QTY-02, C-PRICE-01, C-NAME-01, C-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). id is not an existing product identifier. Follow-up GET /api/cart… |
| TC-CART-009 | `tests/test-cases/cart/TC-CART-009.md` | Reject negative product id | C-ID-04, C-QTY-02, C-PRICE-01, C-NAME-01, C-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). id is not an existing product identifier. Follow-up GET /api/cart… |
| TC-CART-010 | `tests/test-cases/cart/TC-CART-010.md` | Reject non-existent product id | C-ID-05, C-QTY-02, C-PRICE-01, C-NAME-01, C-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). id is not an existing product identifier. Follow-up GET /api/cart… |
| TC-CART-012 | `tests/test-cases/cart/TC-CART-012.md` | Reject id=null | C-ID-08, C-QTY-02, C-PRICE-01, C-NAME-01, C-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). id is not an existing product identifier. Follow-up GET /api/cart… |
| TC-CART-013 | `tests/test-cases/cart/TC-CART-013.md` | Reject non-integer product id | C-ID-09, C-QTY-02, C-PRICE-01, C-NAME-01, C-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). id is not an existing product identifier. Follow-up GET /api/cart… |
| TC-CART-014 | `tests/test-cases/cart/TC-CART-014.md` | Reject non-numeric product id | C-ID-10, C-QTY-02, C-PRICE-01, C-NAME-01, C-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). id is not an existing product identifier. Follow-up GET /api/cart… |
| TC-CART-011 | `tests/test-cases/cart/TC-CART-011.md` | Reject omitted product id | C-ID-06, C-QTY-02, C-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). id is missing. Follow-up GET /api/cart as the same user shows the… |
| TC-CART-015 | `tests/test-cases/cart/TC-CART-015.md` | Numeric-string id — coercion unspecified | C-ID-07, C-QTY-02, C-AUTH-01 | Valid | ⚠️ Spec type is numeric id. Preferred: reject non-number. Acceptable: coerce to 1 and add product 1. Record actual behaviour; do not add a garbage line. |
| TC-CART-016 | `tests/test-cases/cart/TC-CART-016.md` | Reject quantity=0 | C-QTY-04, C-ID-01, C-PRICE-01, C-NAME-01, C-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). quantity must be a positive integer ≥ 1 (FR-06). Follow-up GET /a… |
| TC-CART-017 | `tests/test-cases/cart/TC-CART-017.md` | Reject negative quantity | C-QTY-05, C-ID-01, C-PRICE-01, C-NAME-01, C-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). quantity must be a positive integer ≥ 1 (FR-06). Follow-up GET /a… |
| TC-CART-019 | `tests/test-cases/cart/TC-CART-019.md` | Reject non-integer quantity | C-QTY-07, C-ID-01, C-PRICE-01, C-NAME-01, C-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). quantity must be a positive integer ≥ 1 (FR-06). Follow-up GET /a… |
| TC-CART-021 | `tests/test-cases/cart/TC-CART-021.md` | Reject quantity=null | C-QTY-09, C-ID-01, C-PRICE-01, C-NAME-01, C-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). quantity must be a positive integer ≥ 1 (FR-06). Follow-up GET /a… |
| TC-CART-018 | `tests/test-cases/cart/TC-CART-018.md` | Reject omitted quantity | C-QTY-06, C-ID-01, C-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). quantity is missing. Follow-up GET /api/cart as the same user sho… |
| TC-CART-020 | `tests/test-cases/cart/TC-CART-020.md` | Numeric-string quantity — coercion unspecified | C-QTY-08, C-ID-01, C-AUTH-01 | Valid | ⚠️ Preferred: reject non-number. Acceptable: coerce to 2. Record actual behaviour. |
| TC-CART-022 | `tests/test-cases/cart/TC-CART-022.md` | Extremely large quantity — unspecified max | C-QTY-10, C-ID-01, C-AUTH-01 | Valid | ⚠️ No max in spec. Accept or reject with a documented limit. Must not crash the server or overflow into a negative/zero qty. |
| TC-CART-023 | `tests/test-cases/cart/TC-CART-023.md` | Reject price=0 | C-PRICE-02, C-ID-01, C-QTY-02, C-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). price must be positive. ⚠️ Inferred from FR-15 product price > 0;… |
| TC-CART-024 | `tests/test-cases/cart/TC-CART-024.md` | Reject negative price | C-PRICE-03, C-ID-01, C-QTY-02, C-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). price is negative. Follow-up GET /api/cart as the same user shows… |
| TC-CART-025 | `tests/test-cases/cart/TC-CART-025.md` | Omit price — not specified as required | C-PRICE-04, C-ID-01, C-QTY-02 | Unspecified | price is not specified as required on POST /api/cart. Do not expect rejection. Observe stored line/price. Do not apply FR-15. Audit: INVALID (assumed required). |
| TC-CART-026 | `tests/test-cases/cart/TC-CART-026.md` | Numeric-string price — coercion unspecified | C-PRICE-05, C-ID-01, C-QTY-02 | Valid | ⚠️ Preferred reject or coerce to 30000000. Record actual behaviour. |
| TC-CART-027 | `tests/test-cases/cart/TC-CART-027.md` | Reject price=null | C-PRICE-06, C-ID-01, C-QTY-02 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). price is null. Follow-up GET /api/cart as the same user shows the… |
| TC-CART-028 | `tests/test-cases/cart/TC-CART-028.md` | Client price does not match catalogue for id | C-PRICE-07, C-ID-01, C-QTY-02 | Invalid | ⚠️ Spec does not say the cart API must ignore client price (FR-08 says that for checkout). Expected for a correct design: reject OR persist using catalogue pric… |
| TC-CART-029 | `tests/test-cases/cart/TC-CART-029.md` | Reject empty product name | C-NAME-02, C-ID-01, C-QTY-02 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). name is empty. ⚠️ Assumed required because it is in the documente… |
| TC-CART-030 | `tests/test-cases/cart/TC-CART-030.md` | Reject omitted product name | C-NAME-03, C-ID-01, C-QTY-02 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). name is missing. Follow-up GET /api/cart as the same user shows t… |
| TC-CART-031 | `tests/test-cases/cart/TC-CART-031.md` | Name does not match catalogue for id | C-NAME-04, C-ID-01, C-QTY-02 | Invalid | ⚠️ Spec does not say the server must overwrite client name. Expected: reject OR use catalogue name iPhone 15 Pro Max. Storing a spoofed name for id=1 is a fail … |
| TC-CART-032 | `tests/test-cases/cart/TC-CART-032.md` | Reject add-to-cart with no Authorization header | C-AUTH-03 | Invalid | HTTP 401 Unauthorized (SEC-02: protected API requires a valid JWT). No cart is created for an anonymous user. |
| TC-CART-033 | `tests/test-cases/cart/TC-CART-033.md` | Reject empty Bearer token | C-AUTH-04 | Invalid | HTTP 401 Unauthorized (SEC-02: protected API requires a valid JWT). |
| TC-CART-034 | `tests/test-cases/cart/TC-CART-034.md` | Reject malformed JWT | C-AUTH-05 | Invalid | HTTP 403 Forbidden or 401. Cart unchanged. |
| TC-CART-035 | `tests/test-cases/cart/TC-CART-035.md` | Reject empty HTTP body | C-BODY-02, C-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). body is empty. Follow-up GET /api/cart as the same user shows the… |
| TC-CART-036 | `tests/test-cases/cart/TC-CART-036.md` | Reject malformed JSON | C-BODY-03, C-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). body is not valid JSON. Follow-up GET /api/cart as the same user … |
| TC-CART-037 | `tests/test-cases/cart/TC-CART-037.md` | Reject JSON array body | C-BODY-04, C-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). body is not a JSON object. (Batch add is not specified.) Follow-u… |
| TC-CART-038 | `tests/test-cases/cart/TC-CART-038.md` | Extra undocumented field color | C-BODY-05, C-ID-01, C-QTY-02 | Valid | ⚠️ Extra-field policy unspecified. Documented item should be added. color must not change price, id, or merge behaviour. |
| TC-CART-039 | `tests/test-cases/cart/TC-CART-039.md` | Reject Content-Type text/plain | C-BODY-06, C-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required). Content-Type is not application/json. ⚠️ Spec implies JSON body. … |

---

## FR-19 — `DELETE /api/admin/users/:id` (module `ADMINUSERS`)

### Step 1 · Input variables

| # | Variable | Type | Source |
|---|---|---|---|
| 1 | id | integer (user id) | path parameter /api/admin/users/:id |
| 2 | Authorization | string (JWT) | HTTP header |
| 3 | caller role | enum {admin, user} | JWT claim (not a body field) |
| 4 | id vs caller relationship | self / other | derived: path id compared with token subject |
| 5 | target user existence / state | exists / gone | database |

### Steps 2–3 · Domains, sub-domains, representative values

**Variable: `id`**

| Sub-domain ID | Description | Valid / Invalid | Rep. Value |
|---|---|---|---|
| A-ID-01 | Existing other (non-self) user | Valid | <disposable_user_id> |
| A-ID-02 | Caller's own user id | Invalid (FR-19) | <admin_self_id> |
| A-ID-03 | Zero | Invalid | 0 |
| A-ID-04 | Negative | Invalid | -1 |
| A-ID-05 | Non-existent user | Invalid | 99999 |
| A-ID-06 | Non-numeric path | Invalid | abc |
| A-ID-07 | Non-integer (float) | Invalid | 1.5 |
| A-ID-08 | Empty path segment | Invalid | /api/admin/users/ |
| A-ID-09 | Already-deleted user id (repeat delete) | Invalid | <deleted_id> |
| A-ID-10 | Another admin's id (not self) | ⚠️ spec forbids only self-delete | <other_admin_id> |

**Variable: `Authorization`**

| Sub-domain ID | Description | Valid / Invalid | Rep. Value |
|---|---|---|---|
| A-AUTH-01 | Valid admin JWT | Valid | Bearer <admin_token> |
| A-AUTH-02 | Header omitted | Invalid | (no Authorization) |
| A-AUTH-03 | Empty Bearer token | Invalid | Bearer  |
| A-AUTH-04 | Malformed JWT | Invalid | Bearer not-a-jwt |
| A-AUTH-05 | Valid user (non-admin) JWT | Invalid (FR-12 / SEC-03) | Bearer <user_token> |

**Variable: `caller role`**

| Sub-domain ID | Description | Valid / Invalid | Rep. Value |
|---|---|---|---|
| A-ROLE-01 | role=admin in token | Valid | admin |
| A-ROLE-02 | role=user in token | Invalid | user |

**Variable: `id vs caller`**

| Sub-domain ID | Description | Valid / Invalid | Rep. Value |
|---|---|---|---|
| A-REL-01 | path id ≠ authenticated user id | Valid | other user |
| A-REL-02 | path id = authenticated user id | Invalid | self |


### Step 4 · Test case summary

**Count:** 20 cases (`TC-ADMINUSERS-001` … `TC-ADMINUSERS-020`)

| TC ID | File | Title | Sub-domains | Type | Expected Result |
|---|---|---|---|---|---|
| TC-ADMINUSERS-001 | `tests/test-cases/admin-users/TC-ADMINUSERS-001.md` | Admin deletes another existing user (on-point) | A-ID-01, A-AUTH-01, A-ROLE-01, A-REL-01 | Valid | HTTP 200. Target user is gone from GET /api/admin/users. Password is never present in any response (FR-19). ⚠️ Success body is not documented; SUT currently ret… |
| TC-ADMINUSERS-002 | `tests/test-cases/admin-users/TC-ADMINUSERS-002.md` | Admin cannot delete their own account (FR-19) | A-ID-02, A-REL-02, A-AUTH-01, A-ROLE-01 | Invalid | HTTP 403 Forbidden (or 400). FR-19 forbids deleting the currently logged-in account. GET /api/admin/users still lists the target (if they existed). The caller's… |
| TC-ADMINUSERS-003 | `tests/test-cases/admin-users/TC-ADMINUSERS-003.md` | Reject user id=0 | A-ID-03, A-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required) or HTTP 404 Not Found (⚠️ spec does not name the not-found status … |
| TC-ADMINUSERS-004 | `tests/test-cases/admin-users/TC-ADMINUSERS-004.md` | Reject negative user id | A-ID-04, A-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required) or HTTP 404 Not Found (⚠️ spec does not name the not-found status … |
| TC-ADMINUSERS-005 | `tests/test-cases/admin-users/TC-ADMINUSERS-005.md` | Reject non-existent user id | A-ID-05, A-AUTH-01 | Invalid | HTTP 404 Not Found (⚠️ spec does not name the not-found status code). User does not exist. GET /api/admin/users still lists the target (if they existed). The ca… |
| TC-ADMINUSERS-006 | `tests/test-cases/admin-users/TC-ADMINUSERS-006.md` | Reject non-numeric path id | A-ID-06, A-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required) or HTTP 404 Not Found (⚠️ spec does not name the not-found status … |
| TC-ADMINUSERS-007 | `tests/test-cases/admin-users/TC-ADMINUSERS-007.md` | Reject non-integer (float) path id | A-ID-07, A-AUTH-01 | Invalid | HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required) or HTTP 404 Not Found (⚠️ spec does not name the not-found status … |
| TC-ADMINUSERS-008 | `tests/test-cases/admin-users/TC-ADMINUSERS-008.md` | Empty path is not a valid delete | A-ID-08, A-AUTH-01 | Invalid | Not treated as a successful user delete. 404/405/400. User list unchanged. |
| TC-ADMINUSERS-009 | `tests/test-cases/admin-users/TC-ADMINUSERS-009.md` | Repeat DELETE of an already-deleted user | A-ID-09, A-AUTH-01 | Invalid | HTTP 404 Not Found (⚠️ spec does not name the not-found status code). User no longer exists; second delete is not a silent 200 success against a missing row. GE… |
| TC-ADMINUSERS-010 | `tests/test-cases/admin-users/TC-ADMINUSERS-010.md` | Admin deletes a different admin (not self) — unspecified besides self-rule | A-ID-10, A-REL-01, A-AUTH-01 | Valid | ⚠️ If a second admin can be created: 200 and that admin is removed; caller remains. If the SUT cannot create a second admin, status=Blocked. |
| TC-ADMINUSERS-011 | `tests/test-cases/admin-users/TC-ADMINUSERS-011.md` | Reject delete with no Authorization header | A-AUTH-02 | Invalid | HTTP 401 Unauthorized (SEC-02: protected API requires a valid JWT). Target user is not deleted. |
| TC-ADMINUSERS-012 | `tests/test-cases/admin-users/TC-ADMINUSERS-012.md` | Reject empty Bearer token | A-AUTH-03 | Invalid | HTTP 401 Unauthorized (SEC-02: protected API requires a valid JWT). Target user is not deleted. |
| TC-ADMINUSERS-013 | `tests/test-cases/admin-users/TC-ADMINUSERS-013.md` | Reject malformed JWT | A-AUTH-04 | Invalid | HTTP 403 Forbidden or 401. Target user is not deleted. |
| TC-ADMINUSERS-014 | `tests/test-cases/admin-users/TC-ADMINUSERS-014.md` | Non-admin user cannot delete a user (FR-12 / SEC-03) | A-AUTH-05, A-ROLE-02 | Invalid | HTTP 403 Forbidden. FR-12 / SEC-03: admin APIs require role=admin, not merely a valid token. Target not deleted. |
| TC-ADMINUSERS-015 | `tests/test-cases/admin-users/TC-ADMINUSERS-015.md` | User JWT cannot delete self via admin route | A-AUTH-05, A-REL-02, A-ROLE-02 | Invalid | HTTP 403 Forbidden. Non-admin cannot use the admin delete API, including against themselves. Account remains. |
| TC-ADMINUSERS-016 | `tests/test-cases/admin-users/TC-ADMINUSERS-016.md` | DELETE ignores unexpected JSON body | A-ID-01, A-AUTH-01 | Valid | ⚠️ Spec documents no body. Body must not bypass FR-19 self-delete (this id is not self) and must not change which id is deleted. User is deleted as in the on-po… |
| TC-ADMINUSERS-017 | `tests/test-cases/admin-users/TC-ADMINUSERS-017.md` | Query string does not change which user is deleted | A-ID-01, A-AUTH-01 | Valid | Only the path id is deleted. Query parameter id must not retarget the delete. ⚠️ Query behaviour unspecified; path is the specified identifier. |
| TC-ADMINUSERS-018 | `tests/test-cases/admin-users/TC-ADMINUSERS-018.md` | Very large numeric id is not found (not a crash) | A-ID-05, A-AUTH-01 | Invalid | HTTP 404 Not Found (⚠️ spec does not name the not-found status code) or 400. No such user. Server must not crash or delete an unintended row. GET /api/admin/use… |
| TC-ADMINUSERS-019 | `tests/test-cases/admin-users/TC-ADMINUSERS-019.md` | Self-delete still forbidden when body sends a different id | A-REL-02, A-ID-02, A-AUTH-01 | Invalid | HTTP 403 Forbidden (self path). Disposable user is NOT deleted via the body. Path id is the resource identifier. |
| TC-ADMINUSERS-020 | `tests/test-cases/admin-users/TC-ADMINUSERS-020.md` | Path id with leading zeros must not delete the coerced integer user | A-ID-06, A-ID-07, A-AUTH-01 | Invalid | ⚠️ Coercion of 0001 → 1 is dangerous (would hit self/admin). Expected: 400/404 without deleting user 1. If the SUT canonicalizes to 1, FR-19 self-delete must st… |

---

## Step 5 · Review & refine

### Coverage checklist

| Check | FR-04 | FR-07 | FR-19 |
|-------|-------|-------|-------|
| Every sub-domain has ≥1 TC | Yes | Yes | Yes |
| Each invalid sub-domain has a dedicated off-point TC | Yes (one invalid field, others valid) | Yes | Yes (path/auth/role isolated) |
| Business rules +/− | Phone format +/−; role/email must not change | Merge same product +; new line for different product; qty ≥ 1 − | Delete other user +; self-delete −; non-admin − |
| No duplicate TCs | Distinct SD or combination per ID | Distinct SD or cart state | Distinct id/auth/relationship |
| Preconditions achievable | Seed `test@eshop.com` | Seed products 1–5 | Register disposable user; seed admin |

### Combination (API checklist)

- FR-04 `TC-PROFILE-003`: Unicode name + 11-digit phone + Unicode address (valid edges together).
- FR-07 `TC-CART-002`: `id=1` and `quantity=1` (valid minima together).

### Gaps not turned into SUP cases (out of domain-partition scope)

- **State transitions** of the cart UI (+/−, confirm-delete dialog) — Stage 1 state-transition category, not EP of `POST /api/cart`.
- **Security probes** (SQL injection in `name`/`id`, IDOR on another user’s cart, mass-assignment beyond role/email) — Stage 1 security category (SEC-01…SEC-07). Auth presence/role are included here because they are input variables of the endpoint.
- **Schema** of error envelopes — Stage 1 schema category.
- **Cascade:** deleting a user who owns orders — unspecified; not invented.
- `P-ROLE-01` / `P-EMAIL-01` / `P-BODY-01` / `C-BODY-01` / `A-ROLE-01` are covered by on-point TCs rather than extra files.

### Supplementary TCs (Stage 3 — human-found)

**15 human SUP cases (5 per FR)** — `TC-*-SUP-*`. These are **not** repeated in the Step 5 tables above (those list Stage 1 AI cases only). Full detail and “why missed”: `docs/stage3-extend.md`. All 15 rows are in `sheets/domain-partitions.csv` with `Source=Human`.

| FR | SUP IDs | Themes |
|----|---------|--------|
| FR-04 | PROFILE-SUP-001 … 005 | Partial updates, Unicode phone, duplicate JSON keys, 2-of-3 combinations |
| FR-07 | CART-SUP-001 … 005 | Merge identity, unequal qty, price on merge, minimal body, multi-line cart |
| FR-19 | ADMINUSERS-SUP-001 … 005 | Percent-encoding (single/double), trailing slash, seed id=2, alphanumeric path |

---

## Artifact index

| Artifact | Path |
|----------|------|
| This report | `docs/domain-testing-report.md` |
| Stage 2 audit table | `docs/stage2-audit.md` |
| Stage 3 human extensions | `docs/stage3-extend.md` |
| Per-TC files | `tests/test-cases/profile/`, `cart/`, `admin-users/` |
| API test-case sheet | `sheets/domain-partitions.csv` (**114 rows**: 99 `Source=AI` + 15 `Source=Human` SUP) |
| AI audit log | `ai_audit_log.md` |

**Totals:** 40 PROFILE + 39 CART + 20 ADMINUSERS = **99** AI cases + **15** human SUP (5 per FR) = **114** domain-partition cases.

Stage 2 audit (spec text only, no invented required/HTTP codes): **16 VALID / 42 INVALID / 41 INCOMPLETE**. Details and corrected oracles: `docs/stage2-audit.md`. CSV `AuditStatus` / `AuditReasoning` are filled. INVALID/INCOMPLETE expected results were corrected in place.
