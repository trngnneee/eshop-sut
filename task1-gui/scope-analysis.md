# Scope Analysis — Task 1: GUI Checklist

**Student:** Đặng Đăng Khoa
**Student ID:** 23127207
**SUT repository:** `trngnneee/eshop-sut`
**Review date:** 2026-08-02
**Status:** `HUMAN_REVIEWED`

## In-scope screens

| Platform | Screen | Requirement mapping | Observable boundary |
|---|---|---|---|
| Web frontend | Login (`/login`) | FR-02 | Labels, fields, password masking, validation, authentication feedback, three-attempt/30-second lockout requirement, keyboard order, 320 px layout and navigation links. |
| Web frontend | Register (`/register`) | FR-01 | Name/email/password inputs, valid registration, invalid/duplicate input, password-policy feedback, navigation, responsive and request-failure states. |
| Web admin | Admin Login (unauthenticated `/`) | FR-12 | Authentication fields, validation, feedback, keyboard order and protected-entry behavior. |
| Web admin | Category tab | FR-14 | Navigation to the tab plus add, view and delete behaviors; empty/loading/error/long-input/double-submit states. FR-14 does **not** define Edit Category, so absence of Edit is not reported as a defect. |
| Mobile UI | Login view | FR-02 / mobile UI quality | Labels, fields, password masking, navigation, error states, 320 px layout and minimum touch target. Native soft-keyboard behavior requires a real Android/iOS target. |

Product, cart, checkout, coupon, dashboard and order-management behavior is out of scope except when an in-scope control navigates to one of those destinations.

## Execution environment

- Current item-level evidence source: the corrected Task 3 Chrome/Windows execution, run against the local EShop applications and copied into `evidence/executed-chrome/`.
- Core integration paths use `LIVE_LOCAL_SUT`; deterministic loading/network/error demonstrations use `MOCKED` and are labelled as such in every row.
- Each of the 58 rows has an Actual Result, execution mode, evidence ID, capture time and screenshot reference.
- Forty distinct screenshots include the student identity overlay `23127207 — Đặng Đăng Khoa`.
- Expo Web/mobile viewport evidence is valid for responsive layout checks, but it is not presented as a physical-device or native soft-keyboard run. `GUI-MOBILE-LOGIN-011` therefore remains `Blocked`.

## Test data and safety

- Student-specific accounts use the `23127207` identifier to avoid mutating shared default users.
- Admin test data is limited to reversible category records created for the run.
- Credentials appearing in screenshots are test credentials only.
- GitHub issues are reused only after duplicate review; a URL is never invented.

## Corrected requirement decisions

1. `GUI-WEB-LOGIN-010` checks the written FR-02 boundary: lock after three failed attempts for 30 seconds. The observed implementation differs and is a Fail.
2. `GUI-WEB-LOGIN-013` tests whether surrounding whitespace causes an unsafe or broken response; it does not invent a mandatory automatic-trim requirement.
3. `GUI-ADMIN-CATEGORY-005` checks navigation to Category Management, not a nonexistent Edit requirement.
4. `GUI-ADMIN-CATEGORY-011` checks deterministic add/view behavior for a repeated name; uniqueness is not assumed when the requirement does not require it.
5. `GUI-ADMIN-CATEGORY-008` records the observed unsafe deletion of an in-use category as a software defect.

## Completion boundary

The local package is structurally validated. Full external completion still requires a real public Task 1 GUI-skill YouTube link and a real native-device soft-keyboard run. Those records cannot be synthesized from local files.
