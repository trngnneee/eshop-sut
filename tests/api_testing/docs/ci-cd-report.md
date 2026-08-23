# CI/CD Report — HW06 API Testing (MSSV 23127438)

**Pipeline:** GitHub Actions · **Workflow:** [`.github/workflows/api-tests.yml`](../../../.github/workflows/api-tests.yml)
**Runner:** `ubuntu-latest` · **SUT:** khởi động ngay trong runner (`node server.js`, `localhost:3000`) — KHÔNG dùng mock public (ràng buộc anti-cheat).
**Tool:** Newman + `newman-reporter-htmlextra`.

---

## 1. Cấu hình pipeline (6 stage)

| # | Stage | Lệnh chính |
|---|-------|-----------|
| 1 | Checkout | `actions/checkout@v4` |
| 2 | Node 20 | `actions/setup-node@v4` |
| 3 | Cài SUT deps | `cd backend && npm install` |
| 4 | Khởi động SUT | `cd backend && node server.js &` + `wait-on tcp:127.0.0.1:3000` (DB tự DROP+reseed mỗi lần start) |
| 5 | Cài + chạy Newman | `newman run EShop-CI-<suite>.postman_collection.json -e EShop-Local... -r cli,htmlextra,json` |
| 6 | Upload report | `actions/upload-artifact@v4` (`if: always()`) — `ci-report-<suite>.html/.json` |

**Trigger:**
- `push` / `pull_request` → chạy suite **green** ⇒ pipeline **XANH** (Commit A).
- `workflow_dispatch` (input `suite = green | onefail`) → chọn chạy suite **onefail** ⇒ pipeline **ĐỎ đúng 1 fail** (Commit B).
- `studentId` inject qua `--env-var` (không hardcode trong request); log Console in `[HW06][CI] X-Student-Id = 23127438 -> ...`.

---

## 2. Hai suite CI (bám plan §9)

Full collection (238 request) có 276 fail chủ đích (bug) ⇒ không hợp làm gate CI. Theo plan, tách 2 suite gọn, tất định:

| Suite | File | Nội dung | Kết quả kỳ vọng |
|-------|------|----------|------------------|
| **green** | `postman/EShop-CI-green.postman_collection.json` | 10 case PASS-expected (login, list=5, detail id lẻ price number, search khớp/rỗng, checkout, pending→cancel 200, double-cancel 400, create hợp lệ) | **10/10 pass — pipeline xanh** |
| **onefail** | `postman/EShop-CI-onefail.postman_collection.json` | green + **1** case BUG-05 (shipping→cancel expect 400) | **11 assertions / đúng 1 fail — pipeline đỏ** |

---

## 3. Kết quả chạy Newman local (đã verify trước khi đẩy CI)

SUT chạy `localhost:3000`, `npx newman`:

**GREEN:**
```
iterations 1/0 · requests 10/0 · test-scripts 10/0 · assertions 10/0   → PASS 100%
```

**ONEFAIL:**
```
iterations 1/0 · requests 14/0 · assertions 11 / FAILED 1
1. AssertionError — BUG-05 · shipping -> cancel phải 400 (SUT trả 200 ⇒ FAIL)
   expected response to have status code 400 but got 200
   inside "CI-FAIL — BUG-05 shipping→cancel (expect 400)"
```

⇒ green xanh tuyệt đối, onefail đỏ đúng **exactly 1 failure** — khớp yêu cầu 2-commit demo.

---

## 4. Hai run demo bắt buộc

| Commit | Suite | Trigger | Trạng thái | Link run | Screenshot |
|--------|-------|---------|-----------|----------|------------|
| **A** (all-pass) | green | push | ✅ xanh | _(dán link Actions run)_ | `newman/screenshots/ci-run-all-pass.png` |
| **B** (đúng 1 fail) | onefail | workflow_dispatch → suite=onefail | ❌ đỏ (1 fail) | _(dán link Actions run)_ | `newman/screenshots/ci-run-one-fail.png` |

**Cách tạo 2 run sau khi push workflow:**
1. **Run A:** `git push` (hoặc vào tab Actions → chọn workflow → Run workflow, suite=green). Pipeline xanh.
2. **Run B:** tab **Actions** → **API Tests (Newman)** → **Run workflow** → chọn `suite = onefail` → Run. Pipeline đỏ với 1 fail (BUG-05).
3. Mở mỗi run → chụp screenshot (summary + bảng Newman) → lưu vào `newman/screenshots/`.
4. Tải artifact `newman-report-<suite>` để xem report HTML.

---

## 5. Ý nghĩa

- **Gate xanh (green):** bộ smoke/regression phản ánh hành vi ỔN ĐỊNH của SUT — CI bảo vệ không cho các hành vi đúng bị vỡ về sau.
- **Run đỏ (onefail):** minh hoạ CI **bắt bug thật** — BUG-05 (user hủy đơn shipping) là lỗi nghiệp vụ rõ nghĩa nhất; expected lấy theo contract FR-10 (400), SUT trả 200 nên test đỏ ĐÚNG chỗ. Đây là bằng chứng "test FAIL = giá trị của bài", không phải lỗi cấu hình.
- SUT chạy nội bộ runner trên `localhost:3000` (không mock public) — thoả ràng buộc anti-cheat; hostname `localhost` hiện trong log Newman của CI.
