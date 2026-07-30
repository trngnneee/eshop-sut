# AI Item-Level Critique — Task 1 (EShop GUI Checklist)

**Reviewer:** Senior QA Engineer (Đặng Đăng Khoa - 23127207)  
**Date:** 2026-07-28  
**Scope:** Reviewing 50 items generated in `AI_INITIAL_GUI_Checklist.md` against actual SUT source code.

---

## 1. Item-Level Evaluation Table

| Item ID | Verdict | Problem Found / SUT Reality | Human Correction & Action | Final Decision |
|---|---|---|---|---|
| GUI-WEB-LOGIN-001 | INCOMPLETE | SUT Heading displays `<h2>Đăng Ký</h2>` on `/login` page instead of `Đăng Nhập`. AI assumed happy path expected value. | Update Expected to observe actual SUT defect (`Đăng Ký` heading on login page). | Revise |
| GUI-WEB-LOGIN-002 | INCOMPLETE | SUT label is `Username` and input `type="text"`. AI expected label `Email` and `type="email"`. | Align Expected with SUT code (`label` Username, `type="text"`). | Revise |
| GUI-WEB-LOGIN-003 | INCOMPLETE | SUT password input uses `type="text"` (plain text visible). AI expected `type="password"`. | Update Expected to verify password field masking/type attribute defect. | Revise |
| GUI-WEB-LOGIN-004 | VALID | Basic HTML5 `required` attribute check. | Keep as is. | Keep |
| GUI-WEB-LOGIN-005 | VALID | Basic HTML5 `required` attribute check. | Keep as is. | Keep |
| GUI-WEB-LOGIN-006 | VALID | Verifies error message display on invalid credentials. | Keep as is. | Keep |
| GUI-WEB-LOGIN-007 | INCOMPLETE | SUT uses `<a href="/forgot-password">` causing full page refresh instead of SPA client navigation. AI missed link type. | Update Expected to check if link triggers full browser reload. | Revise |
| GUI-WEB-LOGIN-008 | VALID | Verifies SPA link `<Link to="/register">`. | Keep as is. | Keep |
| GUI-WEB-LOGIN-009 | INCOMPLETE | SUT button text is `Sign In` (English) while form labels are Vietnamese. Button has hardcoded `tabIndex={1}`. | Update Expected to highlight language inconsistency and tabIndex issue. | Revise |
| GUI-WEB-LOGIN-010 | VALID | Verifies account lockout notification after 5 failed login attempts. | Keep as is. | Keep |
| GUI-WEB-REGISTER-001 | VALID | Heading check on `/register`. | Keep as is. | Keep |
| GUI-WEB-REGISTER-002 | INCOMPLETE | SUT Email input has `type="text"` instead of `type="email"`. AI assumed `type="email"`. | Update Expected to inspect input `type` attribute. | Revise |
| GUI-WEB-REGISTER-003 | VALID | Hint text present under password input. | Keep as is. | Keep |
| GUI-WEB-REGISTER-004 | INCOMPLETE | SUT password regex `flawedStrongPasswordRegex` requires whitespace (`\s`), rejecting valid passwords like `Password123!`. | Update Expected to note client-side regex rejection of valid special characters. | Revise |
| GUI-WEB-REGISTER-005 | VALID | Error message displayed on regex failure. | Keep as is. | Keep |
| GUI-WEB-REGISTER-006 | VALID | Backend error message on duplicate email registration. | Keep as is. | Keep |
| GUI-WEB-REGISTER-007 | VALID | Link navigation to login page. | Keep as is. | Keep |
| GUI-WEB-REGISTER-008 | INCOMPLETE | SUT Register button uses `bg-red-500` while Login uses `bg-blue-600` (inconsistent design system). | Update Expected to highlight visual color mismatch. | Revise |
| GUI-WEB-REGISTER-009 | VALID | Browser HTML5 required validation on Name field. | Keep as is. | Keep |
| GUI-WEB-REGISTER-010 | VALID | Browser HTML5 required validation on Email field. | Keep as is. | Keep |
| GUI-ADMIN-LOGIN-001 | VALID | Admin login box visual structure. | Keep as is. | Keep |
| GUI-ADMIN-LOGIN-002 | INCOMPLETE | SUT lacks `<label>` tags for Admin login inputs (uses placeholders only). AI claimed labels exist. | Update Expected to highlight missing `<label>` tags (accessibility defect). | Revise |
| GUI-ADMIN-LOGIN-003 | INCOMPLETE | SUT uses browser `alert("Đăng nhập thất bại")` instead of inline error banner. AI assumed inline banner. | Update Expected to observe browser native alert popup. | Revise |
| GUI-ADMIN-LOGIN-004 | INCOMPLETE | SUT shows browser `alert("Bạn không phải là admin!")` for user role login attempt. | Update Expected to observe native browser alert popup. | Revise |
| GUI-ADMIN-LOGIN-005 | VALID | Redirect to Admin dashboard on valid admin JWT token. | Keep as is. | Keep |
| GUI-ADMIN-LOGIN-006 | VALID | LocalStorage token persistence across F5 refresh. | Keep as is. | Keep |
| GUI-ADMIN-LOGIN-007 | VALID | Logout clears localStorage and resets token state. | Keep as is. | Keep |
| GUI-ADMIN-LOGIN-008 | VALID | Admin password field has `type="password"`. | Keep as is. | Keep |
| GUI-ADMIN-CATEGORY-001 | VALID | Category table layout and headers. | Keep as is. | Keep |
| GUI-ADMIN-CATEGORY-002 | VALID | Add category input and submit button styling. | Keep as is. | Keep |
| GUI-ADMIN-CATEGORY-003 | VALID | Successful category creation updates state and re-fetches list. | Keep as is. | Keep |
| GUI-ADMIN-CATEGORY-004 | INCOMPLETE | SUT input lacks `required` attribute; empty submission sends request and triggers backend alert `Lỗi thêm DM`. | Update Expected to record empty submission alert response. | Revise |
| GUI-ADMIN-CATEGORY-005 | INVALID | SUT source code has **NO EDIT category feature** in UI. AI fabricated edit button & modal. | Remove item or reframe as missing CRUD requirement defect. | Revise (Missing Feature) |
| GUI-ADMIN-CATEGORY-006 | INVALID | SUT has no edit category modal or update action. AI hallucinated feature. | Remove hallucinated item. | Remove |
| GUI-ADMIN-CATEGORY-007 | INCOMPLETE | SUT triggers `axios.delete` immediately without confirmation modal. AI assumed modal existed. | Update Expected to record missing confirmation popup defect. | Revise |
| GUI-ADMIN-CATEGORY-008 | VALID | Category removal from database and list after clicking Delete. | Keep as is. | Keep |
| GUI-ADMIN-CATEGORY-009 | INVALID | SUT has no cancel button because delete happens instantly without prompt. | Remove hallucinated item. | Remove |
| GUI-ADMIN-CATEGORY-010 | INCOMPLETE | SUT displays native browser `alert("Lỗi xóa DM: ...")` when deletion fails. AI expected inline red banner. | Update Expected to observe browser alert dialog. | Revise |
| GUI-ADMIN-CATEGORY-011 | INCOMPLETE | SUT shows empty table body with header rows when list is empty. No empty state message/illustration. | Update Expected to verify absence of empty state messaging. | Revise |
| GUI-ADMIN-CATEGORY-012 | INCOMPLETE | SUT lacks loading spinner/skeleton while fetching categories from API. | Update Expected to record missing loading feedback. | Revise |
| GUI-ADMIN-CATEGORY-013 | VALID | Backend error alert when attempting to insert duplicate category. | Keep as is. | Keep |
| GUI-MOBILE-LOGIN-001 | VALID | Mobile login header title display. | Keep as is. | Keep |
| GUI-MOBILE-LOGIN-002 | INCOMPLETE | SUT Mobile label is `Username` and input placeholder is `Email`. AI claimed label is `Email`. | Update Expected to reflect exact label text `Username`. | Revise |
| GUI-MOBILE-LOGIN-003 | VALID | Mobile password has `secureTextEntry={true}`. | Keep as is. | Keep |
| GUI-MOBILE-LOGIN-004 | INCOMPLETE | SUT button text is `Sign In` (English) in React Native component. | Update Expected to note `Sign In` label text. | Revise |
| GUI-MOBILE-LOGIN-005 | VALID | Mobile login error text rendered in red box. | Keep as is. | Keep |
| GUI-MOBILE-LOGIN-006 | VALID | Back button returns to Mobile Home view (`goHome`). | Keep as is. | Keep |
| GUI-MOBILE-LOGIN-007 | VALID | Touchable navigation to Mobile Register view. | Keep as is. | Keep |
| GUI-MOBILE-LOGIN-008 | VALID | Touchable navigation to Mobile Forgot Password view. | Keep as is. | Keep |
| GUI-MOBILE-LOGIN-009 | VALID | Header nav bar updates to `Chào, <name>` upon login. | Keep as is. | Keep |

---

## 2. Summary of Critique Actions

- **Kept (Valid):** 28 items
- **Revised (Incomplete / SUT Mismatch Fixed):** 19 items
- **Removed (Hallucinated non-existent SUT features):** 3 items (`GUI-ADMIN-CATEGORY-005`, `GUI-ADMIN-CATEGORY-006`, `GUI-ADMIN-CATEGORY-009` reframed/removed)
- **Total Valid AI_INITIAL Items Remaining:** 47 items.
- **HUMAN_ADDED Items Created to fill gaps:** 11 items (bringing total checklist items to **58**).
