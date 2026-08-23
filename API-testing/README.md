# HW06 – API Testing — `README.md`

**Student:** Nguyễn Thanh Gia Bảo | **MSSV:** 23127158 | **Lớp:** 23KTPM3

**Repository:** https://github.com/trngnneee/eshop-sut/tree/HW6-Bao

---

## Self-Assessment Table

| No. | Criteria | Grade | Self-Assessed Grade |
|---|---|---|---|
| 1 | API 1 — full pipeline (generate + audit + extend + execute + bugs) | 30 | 30 |
| 2 | API 2 — full pipeline (same criteria) | 30 | 30 |
| 3 | API 3 — full pipeline (same criteria) | 30 | 30 |
| 4 | Agent Skills (AI-driven test generator) | 10 | 10 |
| | **Total** | **100** | **100** |

---

## Test Summary Report

- **Number of APIs tested:** 3
- **Total test cases generated (AI):** 122
- **Total test cases added (Human):** 21
- **Total test cases (combined):** 143
- **Total executed:** 139 _(4 Not Executed — out-of-scope rows kept for traceability)_
- **Total passed:** 53
- **Total failed:** 85
- **Total blocked:** 1
- **Total confirmed bugs:** 22

| API | Endpoint(s) | Pool | FR | Domain<br>Partition | State<br>Transition | Security | Schema<br>Validation | Total | Passed | Failed |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| forgot-password | `POST /api/forgot-password` | A | FR-03 | 14 | 9 | 15 | 7 | **45** | 22 | 23 |
| apply-coupon | `POST /api/apply-coupon` | B | FR-09 | 18 | 9 | 13 | 9 | **49** | 17 | 31 |
| admin-coupons | `POST /api/admin/coupons`<br>`DELETE /api/admin/coupons/:id` | C | FR-17 | 18 | 10 | 13 | 8 | **49** | 14 | 31 |
| **Total** | | | | **50** | **28** | **41** | **24** | **143** | **53** | **85** |

---

## Agent Skill — Demonstration Video

YouTube link: https://youtu.be/VteHAszZx9A

---

## Running the Tests

```bash
# Install dependencies (from API-testing/)
npm ci

# Run individual collections
npm run forgot   # FR-03 forgot-password
npm run apply    # FR-09 apply-coupon
npm run admin    # FR-17 admin-coupons
npm run ci-pass  # Smoke test (CI all-passing demo)
```

Reports are saved to `report/html-report/`.

---
