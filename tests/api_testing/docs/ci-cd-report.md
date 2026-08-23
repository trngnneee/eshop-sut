# CI/CD Report — HW06 API Testing 

- Họ và tên: Đặng Trường Nguyên
- MSSV: 23127438

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

- `push` / `pull_request` → mặc định chạy suite __green__ ⇒ pipeline __XANH__ (Commit A).
- Push với commit message chứa **`[ci-onefail]`** → chạy suite **onefail** ⇒ pipeline **ĐỎ đúng 1 fail** (Commit B).
- `workflow_dispatch` (input `suite = green | onefail`) → chỉ khả dụng khi workflow đã có trên nhánh mặc định `main`.
- `studentId` inject qua `--env-var` (không hardcode trong request); log Console in `[HW06][CI] X-Student-Id = 23127438 -> ...`.

---

## 2. Hai suite CI (bám plan §9)

Full collection (238 request) có 276 fail chủ đích (bug) ⇒ không hợp làm gate CI. Theo plan, tách 2 suite gọn, tất định:

| Suite | File | Nội dung | Kết quả kỳ vọng |
|-------|------|----------|------------------|
| __green__ | `postman/EShop-CI-green.postman_collection.json` | 10 case PASS-expected (login, list=5, detail id lẻ price number, search khớp/rỗng, checkout, pending→cancel 200, double-cancel 400, create hợp lệ) | __10/10 pass — pipeline xanh__ |
| __onefail__ | `postman/EShop-CI-onefail.postman_collection.json` | green + __1__ case BUG-05 (shipping→cancel expect 400) | __11 assertions / đúng 1 fail — pipeline đỏ__ |

---

## 3. Kết quả chạy Newman local (đã verify trước khi đẩy CI)

SUT chạy `localhost:3000`, `npx newman`:

**GREEN:**

```sh
iterations 1/0 · requests 10/0 · test-scripts 10/0 · assertions 10/0   → PASS 100%
```

**ONEFAIL:**

```ini
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
| **A** (all-pass) | green | push (commit `2b3c804`) | ✅ xanh (28s) | https://github.com/trngnneee/eshop-sut/actions/runs/32619544526 | `newman/screenshots/ci-run-all-pass.jpg` |
| **B** (đúng 1 fail) | onefail | push commit `[ci-onefail]` (`498a70d`) | ❌ đỏ — 1 fail (BUG-05) | https://github.com/trngnneee/eshop-sut/actions/runs/32619881963 | `newman/screenshots/ci-run-fail.jpg` |

**Cách tạo 2 run (workflow đang ở nhánh `HW06-Nguyen`, chưa lên `main` nên KHÔNG có nút Run workflow):**

1. **Run A (green — đã có, run #4):** commit + push bình thường ⇒ suite green ⇒ pipeline xanh.

2. **Run B (đỏ 1 fail):** push 1 commit có `[ci-onefail]` trong message:

```bash
git commit --allow-empty -m "ci: demo one-fail run [ci-onefail]"
git push
```

⇒ workflow chạy suite `onefail` ⇒ đỏ đúng 1 fail (BUG-05).

3. (Tùy chọn) Nếu muốn dùng nút **Run workflow → suite=onefail**: merge/đưa `api-tests.yml` lên nhánh mặc định `main` trước, rồi mới dispatch được.

4. Mở mỗi run → chụp screenshot (summary + bảng Newman) → lưu `newman/screenshots/ci-run-all-pass.jpg`, `ci-run-one-fail.png`.

5. Tải artifact `newman-report-<suite>` để xem report HTML.

---

## 5. Ý nghĩa

- **Gate xanh (green):** bộ smoke/regression phản ánh hành vi ỔN ĐỊNH của SUT — CI bảo vệ không cho các hành vi đúng bị vỡ về sau.
- **Run đỏ (onefail):** minh hoạ CI **bắt bug thật** — BUG-05 (user hủy đơn shipping) là lỗi nghiệp vụ rõ nghĩa nhất; expected lấy theo contract FR-10 (400), SUT trả 200 nên test đỏ ĐÚNG chỗ. Đây là bằng chứng "test FAIL = giá trị của bài", không phải lỗi cấu hình.
- SUT chạy nội bộ runner trên `localhost:3000` (không mock public) — thoả ràng buộc anti-cheat; hostname `localhost` hiện trong log Newman của CI.
