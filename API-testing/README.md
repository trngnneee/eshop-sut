# API Testing Output

Generated test cases for selected EShop APIs.

| API slug | Method + endpoint | Related requirement | DomainPartition | StateTransition | Security | SchemaValidation | Total | Last run |
|---|---|---|---:|---:|---:|---:|---:|---|
| forgot-password | `POST /api/forgot-password` | FR-03 | 14 | 6 | 11 | 7 | 38 | Sat 08/22/2026 23:36:32.15 Asia/Saigon |
| apply-coupon | `POST /api/apply-coupon` | FR-09 | 17 | 8 | 10 | 7 | 42 | Sun 08/23/2026 01:13 Asia/Saigon |
| admin-coupons | `POST /api/admin/coupons`, `DELETE /api/admin/coupons/:id` | FR-17 | 15 | 8 | 11 | 8 | 42 | Sun 08/23/2026 02:15 Asia/Saigon |

## Files

- `specs/api_specification.md`: copied API specification used for generation.
- `forgot-password/01_domain_partitions.json`: Stage 1 output.
- `forgot-password/02_state_transitions.json`: Stage 2 output.
- `forgot-password/03_security.json`: Stage 3 output.
- `forgot-password/04_schema_validation.json`: Stage 4 output.
- `forgot-password/test_cases_master.csv`: consolidated CSV for Excel.
- `forgot-password/ai_audit_log.md`: AI audit log for the generation pipeline.
- `apply-coupon/01_domain_partitions.json`: Stage 1 output.
- `apply-coupon/02_state_transitions.json`: Stage 2 output.
- `apply-coupon/03_security.json`: Stage 3 output.
- `apply-coupon/04_schema_validation.json`: Stage 4 output.
- `apply-coupon/test_cases_master.csv`: consolidated CSV for Excel.
- `apply-coupon/ai_audit_log.md`: AI audit log for the generation pipeline.
- `admin-coupons/01_domain_partitions.json`: Stage 1 output.
- `admin-coupons/02_state_transitions.json`: Stage 2 output.
- `admin-coupons/03_security.json`: Stage 3 output.
- `admin-coupons/04_schema_validation.json`: Stage 4 output.
- `admin-coupons/test_cases_master.csv`: consolidated CSV for Excel.
- `admin-coupons/ai_audit_log.md`: AI audit log for the generation pipeline.
