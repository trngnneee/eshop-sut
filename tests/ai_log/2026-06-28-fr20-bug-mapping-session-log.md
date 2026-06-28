# AI Session Log - FR-20 Bug Mapping

## Metadata

| Field | Value |
| :--- | :--- |
| Date / Time | 2026-06-28 08:16:14 +07 |
| Workspace | `eshop-sut` |
| AI Agent | Codex |
| Tester in test run | Đặng Trường Nguyên |
| Scope | Map failed FR-20 test cases to BUG IDs, update test case statuses, create a GitHub issue-ready bug file, and export this session into `tests/ai_log`. |

## User Requests

1. Map các test case failed của FR-20 sang BUG defect ở defect log bên dưới.
2. Không dùng lại BUG ID của FR-10.
3. Tạo bug artifact cho FR-20 trong `tests/bug`, dùng issue-template style để dễ tạo GitHub issue.
4. Để trống phần evidence để tester bổ sung sau.
5. Bảo đảm các đường dẫn trong issue list bắt đầu từ `eshop-sut`.
6. Export session này ra `ai_log`.

## Source Artifacts Used

| Source | Purpose |
| :--- | :--- |
| `tests/test-runs/fr20-mobile-product-list-search-test-run.md` | Input execution report and defect log target for FR-20. |
| `tests/test-cases/mobile_product_list_search/` | Per-testcase Markdown files with `Status / Related bugs` sections. |
| `.github/ISSUE_TEMPLATE/bug_report.md` | Repository issue template structure used for the FR-20 bug list. |
| `tests/bug/FR-10.md`, `tests/bug/FR-18.md` | Existing bug artifact style references; FR-10 bug IDs were not reused. |
| `README.md` | Requirement references for FR-20 and inherited product search behavior. |
| `api_specification.md` | `GET /api/products?search=keyword` endpoint reference. |
| `backend/server.js` | Technical note source for likely root cause of SQL-like search payload broadening. |

## Work Summary

### Input Snapshot

- FR-20 test-run had 18 execution rows.
- One failed row was present: `FR20-X-TC03`.
- Failed row still had `Related Bug = None`.
- Defect log still contained the placeholder row `[BUG-ID]`.
- FR-20 testcase files still had `Not Run / None` in `Status / Related bugs`.

### Updates Applied

| Artifact | Change |
| :--- | :--- |
| `tests/test-runs/fr20-mobile-product-list-search-test-run.md` | Updated summary totals to 17 Passed / 1 Failed. |
| `tests/test-runs/fr20-mobile-product-list-search-test-run.md` | Mapped failed `FR20-X-TC03` row to `BUG-FR20-X-01`. |
| `tests/test-runs/fr20-mobile-product-list-search-test-run.md` | Replaced defect log placeholder with `BUG-FR20-X-01`. |
| `tests/test-cases/mobile_product_list_search/FR20-X-TC03.md` | Updated status to `Failed / BUG-FR20-X-01 - SQL injection qua từ khóa tìm kiếm trả về toàn bộ danh sách sản phẩm`. |
| `tests/test-cases/mobile_product_list_search/FR20-*.md` | Updated the remaining 17 FR-20 test cases to `Passed / None` based on the test-run results. |
| `tests/bug/FR-20.md` | Created GitHub issue-ready bug list with evidence placeholder and `eshop-sut/...` paths. |

### Current Test Run Snapshot

| Nhóm kiểm thử | Domain TC | BVA TC | Tổng TC | Pass | Fail |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Product List Display | 3 | 0 | 3 | 3 | 0 |
| Search Keyword | 4 | 7 | 11 | 11 | 0 |
| Empty Search Result | 1 | 0 | 1 | 1 | 0 |
| Search Safety | 3 | 0 | 3 | 2 | 1 |
| **Tổng** | **11** | **7** | **18** | **17** | **1** |

## FR-20 Bug Mapping

| Bug ID | Related Test Cases | Summary | Test-run Severity | Issue Severity / Priority | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `BUG-FR20-X-01` | `FR20-X-TC03` | SQL injection qua từ khóa tìm kiếm làm API trả về toàn bộ danh sách sản phẩm. | High | Critical / P0 | Open |

## Bug Artifact

- `tests/bug/FR-20.md`

### Issue Template Fields Included

- `GitHub issue title`
- `Labels`
- `Found by Test Case`
- `Requirement liên quan`
- `Severity / Priority`
- `Environment`
- `Steps to reproduce`
- `Expected result`
- `Actual result`
- `Technical note`
- `Evidence`

Evidence placeholder was intentionally left as `[Bổ sung evidence sau]` for tester-provided screenshots, videos, logs, or API responses.

## Verification Performed

- Verified `tests/test-cases/mobile_product_list_search/` contains 18 `FR20-*.md` files.
- Verified `tests/test-runs/fr20-mobile-product-list-search-test-run.md` summary is 18 total, 17 Passed, 1 Failed.
- Verified `FR20-X-TC03` is mapped to `BUG-FR20-X-01` in:
  - `tests/test-runs/fr20-mobile-product-list-search-test-run.md`
  - `tests/test-cases/mobile_product_list_search/FR20-X-TC03.md`
  - `tests/bug/FR-20.md`
- Verified FR-20 artifacts do not reference `BUG-FR10-*`.
- Verified FR-20 test case/test-run artifacts no longer contain `Not Run / None`.
- Verified the repo currently has `.github/ISSUE_TEMPLATE/bug_report.md`.

## Notes

- This session created and updated test/report artifacts only; it did not patch application runtime code.
- Existing unrelated dirty workspace files were left unchanged.
- `tests/bug` already existed, so no duplicate bug folder was created.
- Bug evidence is pending tester input.

## AI Audit Extract

```markdown
Name of the AI tool: GPT-5 Codex
Date and time: 2026-06-28 08:16:14 +07
Your prompt: hãy map các test case failed sang BUG defect ở bảng dưới, không dùng lại BUG của FR-10. Ngoài ra, tạo 1 folder bug trong tests, với FR-20 này, hãy dùng template issue để ghi 1 list bug trong đó để t dễ dàng tạo issue trên Github dựa vào file đó, các chỗ evidence t sẽ bổ sung sau. Đường dẫn bắt đầu từ eshop-sut
The AI output: Đã map `FR20-X-TC03` sang bug mới `BUG-FR20-X-01`, cập nhật defect log và summary trong `tests/test-runs/fr20-mobile-product-list-search-test-run.md`, đồng bộ `Status / Related bugs` cho 18 testcase FR-20, và tạo issue-ready bug list tại `tests/bug/FR-20.md` với evidence placeholder.
```

```markdown
Name of the AI tool: GPT-5 Codex
Date and time: 2026-06-28 08:16:14 +07
Your prompt: export session này ra ai_log
The AI output: Đã tạo session log tại `tests/ai_log/2026-06-28-fr20-bug-mapping-session-log.md`.
```
