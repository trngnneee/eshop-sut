# Test Run — FR-22 Mobile Forgot Password (Manual + API)

**Date:** 2026-06-29  
**Environment:** Backend `http://localhost:3000`, Mobile `frontend-mobile/App.js` (Expo), API runner `scripts/run-mforgot-manual-tests.js`  
**Gap analysis:** [gap-analysis-FR-22.md](../test-summary/gap-analysis-FR-22.md)  
**Results JSON:** [mforgot-manual-results.json](./mforgot-manual-results.json)

---

## Summary

| Metric | Count |
| :--- | ---: |
| Total TC | 51 |
| Pass | 7 |
| Fail | 44 |
| Blocked | 0 |

**Suite composition:** 20 EP (`TC-MFORGOT-001`–`020`) + 24 BVA (`021`–`044`) + 7 SUP (`SUP-001`–`007`)

---

## Supplementary (GAP remediation)

| Test Case | Result | Bug | Notes |
| :--- | :--- | :--- | :--- |
| [TC-MFORGOT-SUP-001](../test-cases/forgot-mobile/TC-MFORGOT-SUP-001.md) | Fail | #6 | API OTP `5439` (4 digits); label "Mã OTP (4 số)" |
| [TC-MFORGOT-SUP-002](../test-cases/forgot-mobile/TC-MFORGOT-SUP-002.md) | Fail | #6 | Demo message không hiển thị OTP trên màn hình |
| [TC-MFORGOT-SUP-003](../test-cases/forgot-mobile/TC-MFORGOT-SUP-003.md) | Fail | #10 | API chấp nhận `weakpass` (HTTP 200) |
| [TC-MFORGOT-SUP-004](../test-cases/forgot-mobile/TC-MFORGOT-SUP-004.md) | Pass | None | OTP vô hiệu sau reset lần 1 |
| [TC-MFORGOT-SUP-005](../test-cases/forgot-mobile/TC-MFORGOT-SUP-005.md) | Fail | #4 | Chỉ 1 trường `secureTextEntry`, không có xác nhận |
| [TC-MFORGOT-SUP-006](../test-cases/forgot-mobile/TC-MFORGOT-SUP-006.md) | Fail | None | `handleResetPassword` dùng `Alert.alert` |
| [TC-MFORGOT-SUP-007](../test-cases/forgot-mobile/TC-MFORGOT-SUP-007.md) | Fail | #7 | Client chấp nhận `Test1234+` (ngoài whitelist FR-01) |

---

## Domain Testing (EP) — highlights

| Test Case | Result | Bug |
| :--- | :--- | :--- |
| TC-MFORGOT-001 | Fail | #4, #6, #7 |
| TC-MFORGOT-004 | Pass | None |
| TC-MFORGOT-010 | Pass | None |
| TC-MFORGOT-019 | Fail | #5 |
| TC-MFORGOT-020 | Fail | #9 |

---

## BVA — highlights

| Test Case | Result | Bug |
| :--- | :--- | :--- |
| TC-MFORGOT-022 … 025 | Pass | None |
| TC-MFORGOT-028 (OTP 6-digit on-point) | Fail | #7 |
| TC-MFORGOT-031 (password min 8) | Fail | #7 |

---

## Execution method

1. **API:** `POST /api/forgot-password`, `POST /api/reset-password` cho SUP-001, 003, 004.
2. **Static UI review:** `frontend-mobile/App.js` cho SUP-002, 005, 006, 007 và EP UI (019, 020).
3. **Parity:** BVA kết quả đồng bộ từ thực thi FR-03 web + hành vi Mobile tương đương.

> **Expo device:** Chạy `npm start` trong `frontend-mobile/` và xác nhận thủ công trên simulator/thiết bị; runner tự động hóa phần API + phân tích mã nguồn Mobile.
