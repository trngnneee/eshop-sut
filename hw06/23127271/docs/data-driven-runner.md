# Data-driven Collection Runner — FR-04 phone partitions

**Student:** 23127271 · **API:** `PUT /api/users/me` · **SUT:** `http://localhost:3000`

This folder supplements the 280 manual TC folders — it does **not** replace them. Use it to exercise **five phone partitions** in one Runner pass with a CSV data file.

---

## Artifacts

| File | Purpose |
|------|---------|
| `postman/runner-data-profile-phone.csv` | 5 data rows (plus header) — varies `test_phone` |
| `postman/eshop-hw06.postman_collection.json` | Folder **`99 — Data-driven Runner (CSV)`** |
| `postman/eshop-hw06.postman_environment.json` | Optional env overrides (`baseUrl`, `studentId`) |

### CSV columns

| Column | Description |
|--------|-------------|
| `tc_id` | Row label for logs (DD-PHONE-01 … 05) |
| `test_phone` | Phone sent in PUT body |
| `test_name` | Profile name (constant across rows) |
| `test_shipping_address` | Address (constant across rows) |
| `partition_note` | Human oracle hint (observe-only) |

### Phone partitions (5 rows)

| tc_id | test_phone | Partition |
|-------|------------|-----------|
| DD-PHONE-01 | `0912345678` | Valid — 10 digits, starts with 0 |
| DD-PHONE-02 | `09123456789` | Valid — 11 digits (FR-04 max) |
| DD-PHONE-03 | `0987654321` | Valid — alternate 10-digit |
| DD-PHONE-04 | `1234567890` | Invalid — does not start with 0 |
| DD-PHONE-05 | `091234567` | Invalid — 9 digits (too short) |

**Oracle (observe-only):** HTTP status not specified in api_spec. After each iteration, `GET /api/users/me` and record whether stored `phone` matches FR-04 (10–11 ASCII digits starting with `0`). Do not invent mandatory 400/422.

---

## Postman GUI

1. Import collection + environment.
2. Open collection → folder **`99 — Data-driven Runner (CSV)`**.
3. Click **Run**.
4. **Select file** → `postman/runner-data-profile-phone.csv`.
5. Iterations = **5** (one per CSV row).
6. Run.

Each iteration executes:

1. **Login** — `POST /api/login` (test@eshop.com) → saves `userToken`
2. **PUT** — `/api/users/me` with `{{test_phone}}`, `{{test_name}}`, `{{test_shipping_address}}`

`X-Student-Id: 23127271` is injected by the collection pre-request script.

---

## Newman (CLI)

From `SoftwareTesting-HW/HW06/23127271`:

```bash
newman run postman/eshop-hw06.postman_collection.json ^
  --folder "99 — Data-driven Runner (CSV)" ^
  -d postman/runner-data-profile-phone.csv ^
  -r cli
```

PowerShell:

```powershell
newman run postman/eshop-hw06.postman_collection.json `
  --folder "99 — Data-driven Runner (CSV)" `
  -d postman/runner-data-profile-phone.csv `
  -r cli
```

Optional environment (only if you need non-default `baseUrl`):

```bash
newman run postman/eshop-hw06.postman_collection.json \
  -e postman/eshop-hw06.postman_environment.json \
  --folder "99 — Data-driven Runner (CSV)" \
  -d postman/runner-data-profile-phone.csv
```

**Note:** Skip `-e` when env tokens are empty and would override Setup/login tokens (same rule as full collection run).

---

## Test scripts (observe-only)

Per iteration the PUT request logs:

- `tc_id`, `test_phone`, HTTP status
- `partition_note` from CSV
- Reminder to verify stored phone on GET

Assertions (same pattern as 280 TC folders):

- Response code in 100–599
- JSON body when Content-Type is JSON
- Response time &lt; 10s

No hard-coded expected status — human pass/fail against FR-04 after GET.

---

## Re-apply after collection rebuild

If you regenerate the collection from sheets, re-run:

```bash
python scripts/append_data_driven_runner.py
```

This replaces only folder `99` and leaves the 280 TC folders unchanged.

---

## Related docs

- [`docs/execution-artifacts.md`](execution-artifacts.md) — full Postman feature list
- [`sheets/domain-partitions.csv`](../sheets/domain-partitions.csv) — full phone partition TCs (TC-PROFILE-*)
