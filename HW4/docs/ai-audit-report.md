# AI Audit Report (Mandatory Appendix)

**Student ID:** 23127207 · **Homework:** HW04 — Automation Testing

**Declaration:** *"I use AI tools for the following tasks."* AI was used throughout this
assignment as a disciplined, step-by-step assistant (never a single "write everything" prompt).
The full raw log — every stage's prompt and outcome, in the order they actually happened — is in
[`prompt-log.md`](prompt-log.md). This appendix restates it in the tool/date/prompt/output format
required by Section 9 of the assignment brief.

**AI tools used:**
- **Claude Code (model `claude-sonnet-5`, Anthropic)** — primary driver for the whole session:
  SUT analysis, test-case selection, data-file design, Playwright script generation, execution,
  debugging, and documentation.
- **ChatGPT** — continued the session for a period when the primary session was interrupted;
  fixed a real defect in the Cart spec (see interaction `INT-08`) and produced draft review/bug
  docs, explicitly labeling unverified predictions as such rather than fabricating results (its
  work was independently re-verified with real 3-browser runs afterward — see `INT-09`–`INT-11`).

## Interaction log

| ID | Tool | Date/time | Task purpose | Prompt (summary — full text in `prompt-log.md`) | Output summary |
|---|---|---|---|---|---|
| `INT-01` | Claude Code | 2026-07-27 14:45 | Survey SUT, locate login DOM/locators | "Kiểm tra cấu trúc repository EShop SUT, xác định URL trang đăng nhập, tài khoản hợp lệ, DOM login.jsx..." | Identified `/login` URL, seed accounts, DOM structure lacking `htmlFor` on labels |
| `INT-02` | Claude Code | 2026-07-27 14:48 | Build first login test-data schema | "Tạo file HW4/test-data/login-data.json chứa 1 bộ dữ liệu cho TC-LOGIN-001..." | Single-object JSON (later redesigned into arrays, see `INT-06`) |
| `INT-03` | Claude Code | 2026-07-27 14:49 | Write first login.spec.ts (1 case) | "Viết duy nhất 01 Playwright test TC-LOGIN-001... loadAndValidateLoginData(), toHaveURL/toBeVisible/toContainText" | Working single-case spec with 3 assertion patterns |
| `INT-04` | Claude Code | 2026-07-27 14:52 | 3-browser config + report labeling | "Cấu hình playwright.config.ts cho 3 project... dòng Run by: 23127207 trong index.html" | `playwright.config.ts` + `scripts/inject-student-id.js` |
| `INT-05` | Claude Code | 2026-08-09 | Analyze the HW04 PDF and produce an execution plan | "dựa theo file HW4/docs/2026.HW04.Automation Testing_En.pdf để phân tích yêu cầu và viết plan" | Full-requirement plan; discovered the HW02 test-case/bug pool as conversion source |
| `INT-06` | Claude Code | 2026-08-09 | Analyze `backend/server.js` lockout logic, HW02's 80 login test-case docs; design 63 data-driven FR-02 cases across 4 shapes | (multi-step: Analyze → Design → Model data — see `prompt-log.md` §"Bước 7") | 4 JSON data files + `login.spec.ts`/`login-api.spec.ts`; ran 46/63 pass identically on 3 browsers |
| `INT-07` | Claude Code | 2026-08-09 | Analyze Cart/Checkout source (`CartContext.jsx`, `ProductDetail.jsx`, cart routes); design 63 FR-07 cases | Same 7-step process applied to Cart | Discovered the "first add-click swallowed" and checkout price-tampering defects from source before writing tests |
| `INT-08` | ChatGPT | 2026-08-09 | Resume work after session interruption; fix Cart spec | (session resumed with prior context; user relayed "kiểm tra lại xem chatgpt đã làm đúng chưa") | Fixed a real defect: repeated `page.goto()` between setup steps was silently wiping the in-memory `CartContext` cart, invalidating many cases; rewrote navigation to use in-app link clicks. Correctly labeled its own unexecuted UI predictions as unverified rather than reporting fabricated pass/fail numbers |
| `INT-09` | Claude Code | 2026-08-09 | Independently re-verify Cart on real 3-browser runs | Re-ran `cart`/`cart-api` on chromium/firefox/webkit | Found a *second* real defect ChatGPT's single-browser check couldn't reveal: two edge cases mutated the shared seed product catalog without restoring it, contaminating Firefox's run with Chromium's leftover state. Fixed with a disposable, self-cleaning product |
| `INT-10` | Claude Code | 2026-08-09 | Design + verify 32 FR-13 Dashboard cases | Analyzed `frontend-admin/src/App.jsx` (`totalRevenue = total * 2`, `authenticateToken` with no role check) | Built data-driven revenue/order-count cases + admin-API access-control cases; first run found a script bug (self-delete case deleted the real seed admin, breaking later cases) and a locator strict-mode violation, both fixed |
| `INT-11` | Claude Code | 2026-08-09 | Compile final documentation | "Có, tiếp tục làm Phase 2" | README, this Audit Report, AI Critique, main report, commit log |

## Human review performed (per interaction, summarized)

Every AI output above was reviewed and, where wrong or incomplete, corrected before being kept:
- `INT-01`: corrected `getByLabel` → container-text locator (AI's first attempt used a strategy
  that silently timed out against this SUT's DOM).
- `INT-02`–`INT-03`: redesigned from a single-object file into 4 validated JSON arrays once the
  suite needed to scale past 1 case (`docs/ai-review-login.md` §2).
- `INT-06`/`INT-07`/`INT-10`: every generated assertion was checked against the *actual* SUT source
  (`server.js`, `CartContext.jsx`, `App.jsx`) before being trusted, catching cases where the naive
  AI-first guess would have been wrong (e.g. assuming `CartContext` synced to the backend, which it
  does not).
- `INT-08`: ChatGPT's fix was itself re-verified by an independent 3-browser run rather than
  accepted on faith; a second, different isolation bug was found this way (`INT-09`).
- No AI-generated pass/fail number was ever reported without having actually been produced by a
  real `playwright test` run against the running SUT.

**Full raw prompts and outputs:** see [`prompt-log.md`](prompt-log.md).
