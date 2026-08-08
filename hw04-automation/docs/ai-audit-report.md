# AI Audit Report - HW04 Automation Testing

I use AI tools for the following tasks:

## Interaction Log

### [1] FR-05 Product Listing and Search - requirement analysis
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-08 22:50
- **Prompt:**
  > Hãy phân tích FR-05
- **Output:**
  The AI read the HW04 automation-testing skill, checked `feature_pools.md`, `README.md`, `api_specification.md`, `frontend-web/src/pages/Home.jsx`, `backend/server.js`, and `backend/database.js`, then summarized FR-05 scope for product listing and search. The output identified the main user flow, testable requirements, and likely bug candidates: unsafe rendering of the search keyword, empty image `alt`, missing loading state, missing empty state, multiple `<h1>` elements, and SQL injection risk in the search API.
- **Accepted as-is / Modified:** Accepted with later expansion into Markdown test-case artifacts.

### [2] FR-05 Product Listing and Search - Markdown test case files
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-08 22:52
- **Prompt:**
  > Hãy tạo các file md cho các test case
- **Output:**
  The AI created `hw04-automation/docs/test-cases/FR-05-test-cases.md` and individual Markdown files from `TC-FR05-01.md` through `TC-FR05-14.md`. The suite contains 14 test cases covering positive flows, edge cases, negative/security cases, accessibility, semantic HTML, and loading behavior. All cases currently have `Status = Not Run` because automation execution has not started yet.
- **Accepted as-is / Modified:** Accepted. The files should still be human-reviewed before generating Playwright code, especially to confirm exact expected values against the running seeded database.

### [3] FR-05 Product Listing and Search - data file creation
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-08 22:57
- **Prompt:**
  > Tạo data file data/fr05.json từ các test case vừa thiết kế.
- **Output:**
  The AI created `hw04-automation/data/fr05.json` with seeded product data, expected search inputs/results, negative payloads, semantic HTML expectations, and loading-intercept data for TC-FR05-01 through TC-FR05-14. The AI also updated the Markdown test-case references from `data/fr05-product-search.json` to `data/fr05.json` so the traceability table and individual test case files point to the actual data file.
- **Accepted as-is / Modified:** Accepted. JSON parsing was validated with PowerShell `ConvertFrom-Json`; automation scripts have not been generated or executed yet.

## Tool declaration summary

| Tool | Used for | # of interactions |
|---|---|---|
| Codex (GPT-5) | FR-05 requirement analysis, Markdown test case design, and test data creation | 3 |
