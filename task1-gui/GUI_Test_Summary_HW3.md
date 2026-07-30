# GUI Test Summary Report — Task 1 (HW03)

**Tester:** Đặng Đăng Khoa (MSSV: 23127207)  
**System Under Test:** EShop (Web Frontend, Web Admin, Mobile App)  
**Execution Date:** 2026-07-28  

---  

## 1. High-Level Metrics Summary

| Metric | Value |
|---|---|
| **Total Target Screens** | 5 Screens (Web Login, Web Register, Admin Login, Admin Category, Mobile Login) |
| **Total Designed Items** | 58 Items |
| **Total Executed Items** | 58 Items |
| **Passed Items** | 40 Items |
| **Failed Items** | 18 Items |
| **Blocked Items** | 0 Items |
| **Not Run Items** | 0 Items |
| **Pass Rate (Pass / Executed)** | **68.97%** |
| **Total Distinct Bugs Logged** | 5 Bugs (BUG-GUI-01 to BUG-GUI-05) |
| **AI Initial Items** | 47 Items |
| **Human Added Items** | 11 Items |
| **GitHub Traceability Status** | **PENDING_EXTERNAL_ACTION** (Prepared offline files in `github-issues/`) |
| **Final Deliverables Validator Status** | **INCOMPLETE (Pending Student Manual GitHub Post)** |

---  

## 2. Bug Distribution by Severity

| Severity | Bug Count | Bug IDs |
|---|---|---|
| **Critical** | 0 | None |
| **High** | 3 | BUG-GUI-01, BUG-GUI-02, BUG-GUI-04 |
| **Medium** | 1 | BUG-GUI-03 |
| **Low** | 1 | BUG-GUI-05 |
| **Total** | **5** | |

---  

## 3. Platform & Information Architecture Breakdown

| Platform | Total Items | Pass | Fail | Pass Rate |
|---|---|---|---|---|
| Web Frontend | 25 | 16 | 9 | 64.0% |
| Web Admin | 22 | 13 | 9 | 59.1% |
| Mobile App | 11 | 9 | 2 | 81.8% |
| **Total** | **58** | **40** | **18** | **68.97%** |

---  

## 4. Key Findings & Recommendations

1. **Web Login (FR-02):** Urgent fix needed for plaintext password input (`type='text'`) and heading title semantic mismatch (`Đăng Ký` on login page).
2. **Web Register (FR-01):** Fix regex validation bug (`\s` required instead of special characters) which prevents user account creation.
3. **Admin Category (FR-14):** Implement missing Edit Category feature in UI and add immediate confirmation modal before category deletion.
4. **Accessibility:** Add missing `<label>` elements and replace browser native `alert()` calls with accessible inline UI alert banners.
