# 10 — CONTINUOUS PERFORMANCE TESTING PROPOSAL (Task 3)

> Nguồn cho `deliverables/07_continuous-performance-testing.md`. **10 điểm.** Bloom-AI **G9.6 (Disrupt)**.
> Đề §6 Task 3: *"propose a continuous performance-testing model that watches the SUT's commits, decides whether to run performance tests, and flags p95 regressions. Include a **flow chart** and a discussion of the **trade-offs** (cost, false alarms)."*
>
> Doc này viết gần như hoàn chỉnh. Chỉ cần thay `<<FILL>>` bằng số thật rồi chuyển thành deliverable.

---

## 1. Vấn đề cần giải

Kiểm thử hiệu năng thủ công như HW05 có ba nhược điểm chí mạng:

| Nhược điểm | Hệ quả |
| :--- | :--- |
| **Chỉ chạy một lần** | Kết quả hết hạn ngay khi có commit tiếp theo |
| **Tốn ~40 phút chạy + vài giờ phân tích** | Không ai làm lại thường xuyên |
| **Phát hiện muộn** | Regression hiệu năng bị phát hiện khi đã lên production, lúc chi phí sửa cao nhất |

Mục tiêu của mô hình này: **phát hiện regression p95 trong vòng 15 phút kể từ khi commit**, với chi phí đủ thấp để duy trì lâu dài, và tỉ lệ báo động giả đủ thấp để đội ngũ không học cách phớt lờ cảnh báo.

---

## 2. Ba nguyên tắc thiết kế

| # | Nguyên tắc | Vì sao |
| :---: | :--- | :--- |
| 1 | **Không chạy mọi commit** | Sửa README không thể làm chậm API. Chạy hết là đốt tiền CI và làm chậm vòng phản hồi |
| 2 | **So sánh tương đối, không so ngưỡng tuyệt đối** | Runner CI dùng chung phần cứng, hiệu năng dao động 20–40 % giữa các lần chạy. Ngưỡng tuyệt đối kiểu "p95 < 500 ms" sẽ nhấp nháy xanh-đỏ vô nghĩa. So với baseline đo trên **cùng loại runner** thì loại được phần lớn nhiễu nền |
| 3 | **Chặn merge chỉ khi bằng chứng đủ mạnh** | Một lần chạy chậm bất thường không phải regression. Cần median của nhiều lần chạy và một ngưỡng đủ rộng |

---

## 3. Flow chart

```mermaid
flowchart TD
    A[Commit / Pull Request] --> B{Đường dẫn thay đổi<br/>khớp backend/** ?}
    B -- Không --> Z1[Bỏ qua<br/>Ghi log: perf-skip: path]
    B -- Có --> C{Có nhãn perf-skip<br/>hoặc [skip perf] ?}
    C -- Có --> Z2[Bỏ qua<br/>Ghi log: perf-skip: manual]
    C -- Không --> D{Phân loại thay đổi}

    D -- "Chỉ comment / test / docs" --> Z3[Bỏ qua]
    D -- "Route, truy vấn, middleware, dependency" --> E[Xếp hàng chạy Smoke Perf]

    E --> F[Khởi tạo môi trường<br/>Node + seed dữ liệu cố định<br/>seed 400 user / 505 product]
    F --> G[Chạy JMeter non-GUI<br/>15 VU × 2 phút<br/>workflow Browse-to-buy 5 bước]
    G --> H[analyze_jtl.py<br/>xuất summary.json]

    H --> I{Lần chạy thứ mấy?}
    I -- "< 3" --> G

    I -- "= 3" --> J[Lấy MEDIAN p95 của 3 lần chạy<br/>theo từng label]
    J --> K[Đọc baseline.json<br/>từ nhánh main]

    K --> L{delta_p95 = p95_hiện_tại / p95_baseline − 1}

    L -- "delta ≤ 10%" --> M[✅ PASS<br/>Báo cáo xanh]
    L -- "10% < delta ≤ 20%" --> N[⚠️ WARN<br/>Bình luận vào PR<br/>KHÔNG chặn merge]
    L -- "delta > 20%" --> O[❌ FAIL<br/>Chặn merge<br/>Bình luận kèm bảng so sánh]

    M --> P{Nhánh là main ?}
    P -- Có --> Q[Cập nhật baseline.json<br/>commit tự động]
    P -- Không --> R[Kết thúc]
    N --> R
    O --> R
    Q --> R

    S[Nightly cron 02:00] --> T[Chạy đầy đủ<br/>Load + Stress + Spike + Endurance]
    T --> U[Lưu vào kho lịch sử<br/>vẽ xu hướng 30 ngày]
    U --> V{Xu hướng xấu dần<br/>> 15% trong 7 ngày ?}
    V -- Có --> W[Mở issue tự động<br/>gán cho chủ sở hữu backend]
    V -- Không --> X[Kết thúc]
```

---

## 4. Bốn tầng của mô hình

| Tầng | Kích hoạt | Thời lượng | Tải | Mục đích |
| :--- | :--- | :---: | :--- | :--- |
| **T1 — Cổng lọc** | Mọi commit | < 5 s | — | Quyết định có chạy hay không |
| **T2 — Smoke perf** | PR chạm `backend/**` | ~8 phút | 15 VU × 2 phút × 3 lần | Chặn regression trước khi merge |
| **T3 — Nightly đầy đủ** | Cron 02:00 hằng ngày | ~40 phút | Load + Stress + Spike + Endurance | Theo dõi xu hướng, cập nhật baseline |
| **T4 — Trước release** | Gắn tag | ~90 phút | Toàn bộ + soak 60 phút | Cổng chất lượng cuối |

### 4.1 Chi tiết T1 — logic cổng lọc

```yaml
# Chạy khi:
paths:
  - 'backend/**'
  - 'performance-testing/test-plans/**'
  - '.github/workflows/perf-regression.yml'

# Bỏ qua khi:
#  - PR có nhãn 'perf-skip'
#  - Commit message chứa '[skip perf]'
#  - Diff chỉ chạm file *.md hoặc *.test.js
```

Phân loại mức hai (chạy bằng script, không phải AI): diff có chạm tới định nghĩa route, chuỗi SQL, middleware, hay `package.json` không? Nếu chỉ đổi comment hoặc chuỗi hằng thì bỏ qua.

> **Cân nhắc dùng AI ở tầng này:** có thể để mô hình đọc diff và phán đoán "thay đổi này có khả năng ảnh hưởng hiệu năng không". Nhưng đây là **đánh đổi rủi ro**: một phán đoán sai theo hướng bỏ sót sẽ để lọt regression mà không ai biết. Khuyến nghị: dùng luật tĩnh làm cổng chính, dùng AI chỉ để **gợi ý bổ sung** ("diff này có vẻ ảnh hưởng hiệu năng dù không khớp path filter"), và luôn ghi log lý do bỏ qua để kiểm toán được.

### 4.2 Chi tiết T2 — vì sao 15 VU × 2 phút × 3 lần

| Tham số | Giá trị | Lý do |
| :--- | :--- | :--- |
| Số VU | **15** | Đủ để lộ regression thuật toán (O(n) → O(n²)), đủ nhẹ để chạy trên runner 2 vCPU chia sẻ mà không tự bão hòa |
| Thời lượng | **2 phút** | 30 s đầu bỏ đi (khởi động JIT + cache lạnh), còn 90 s lấy mẫu |
| Số lần lặp | **3** | Lấy **median** để loại một lần chạy bất thường. Đây là biện pháp chống báo động giả rẻ nhất và hiệu quả nhất |
| Tổng thời gian | ~8 phút | Nằm trong ngưỡng chấp nhận được của một bước CI trên PR |

### 4.3 `baseline.json`

Lưu trong repo tại `performance-testing/baseline/baseline.json`:

```json
{
  "updated_at": "2026-08-12T02:14:33Z",
  "commit": "d5eaf839",
  "runner": "ubuntu-latest-2core",
  "jmeter_version": "5.6.3",
  "dataset": { "users": 400, "products": 505 },
  "labels": {
    "01_Login":          { "p95_ms": 42,  "samples": 1350 },
    "02_BrowseProducts": { "p95_ms": 421, "samples": 1350 },
    "03_ProductDetail":  { "p95_ms": 38,  "samples": 1350 },
    "04_AddToCart":      { "p95_ms": 25,  "samples": 1350 },
    "05_Checkout":       { "p95_ms": 156, "samples": 1350 }
  }
}
```

Trường `runner` và `dataset` là bắt buộc: baseline chỉ có nghĩa khi so trên **cùng loại phần cứng và cùng lượng dữ liệu**. Đổi runner mà không đổi baseline là nguồn báo động giả lớn nhất.

Baseline chỉ được cập nhật khi **merge vào `main`** và kết quả `PASS`. Không bao giờ cập nhật từ nhánh feature — nếu không, một regression được merge sẽ tự trở thành chuẩn mới và vĩnh viễn ẩn đi.

---

## 5. Ngưỡng phát hiện regression

| Mức | Điều kiện | Hành động |
| :--- | :--- | :--- |
| ✅ **PASS** | `delta_p95 ≤ +10 %` **trên mọi label** | Không làm gì |
| ⚠️ **WARN** | `+10 % < delta_p95 ≤ +20 %` trên ≥ 1 label | Bình luận vào PR, **không** chặn merge |
| ❌ **FAIL** | `delta_p95 > +20 %` trên ≥ 1 label<br/>**hoặc** `error_rate > 1 %` | Chặn merge, bình luận kèm bảng so sánh |
| 🎉 **IMPROVED** | `delta_p95 < −15 %` | Bình luận chúc mừng + **nhắc cập nhật baseline** |

### 5.1 Vì sao chọn 20 % chứ không phải 5 %

Đo trên chính runner CI: chạy cùng một commit 10 lần liên tiếp, độ lệch p95 giữa các lần là `<<FILL: đo thực tế, thường 10–25 % trên runner chia sẻ>>`.

Nguyên tắc: **ngưỡng phải lớn hơn nhiễu nền, nếu không toàn bộ hệ thống chỉ tạo ra báo động giả.** Nếu đặt 5 % thì mỗi PR đều đỏ, đội ngũ sẽ học cách bấm bỏ qua trong hai tuần, và hệ thống trở thành vô dụng — tệ hơn cả không có gì, vì nó tạo cảm giác an toàn giả.

> Với hạ tầng chạy trên runner **riêng** (self-hosted, không chia sẻ CPU), nhiễu giảm còn dưới 5 % và có thể siết ngưỡng xuống 10 %. Chi phí: phải tự vận hành máy. Đây là đánh đổi tiền lấy độ nhạy.

### 5.2 Vì sao dùng p95 chứ không phải trung bình

| Metric | Vấn đề |
| :--- | :--- |
| Trung bình | Bị khối request nhanh kéo xuống; một regression chỉ ảnh hưởng 5 % người dùng gần như không làm trung bình nhúc nhích |
| p99 | Quá nhiễu ở cỡ mẫu nhỏ của smoke test — với ~1350 mẫu, p99 chỉ dựa trên ~13 điểm dữ liệu |
| **p95** | Cân bằng: đủ nhạy với đuôi phân phối, đủ ổn định ở cỡ mẫu vài nghìn |

---

## 6. Trade-offs — phần đề bài yêu cầu bàn kỹ

### 6.1 Chi phí

| Hạng mục | Ước tính | Ghi chú |
| :--- | :--- | :--- |
| T2 (smoke) | 8 phút/lần × ~15 PR-run/tuần = **~2 giờ CI/tuần** | Trên GitHub Actions runner công cộng, repo public thì miễn phí; repo private tính vào hạn mức |
| T3 (nightly) | 40 phút × 30 ngày = **~20 giờ CI/tháng** | |
| T4 (release) | 90 phút × ~2 lần/tháng = **~3 giờ/tháng** | |
| **Tổng** | **~30 giờ CI/tháng** | |
| Lưu trữ | `.jtl` + HTML report ~50 MB/lần chạy đầy đủ | **Phải có chính sách xóa**, nếu không kho phình vài GB mỗi tháng. Đề xuất: giữ raw 14 ngày, giữ `summary.json` vĩnh viễn |
| Công vận hành | ~2 giờ/tháng | Cập nhật baseline khi đổi runner, điều tra cảnh báo |

**Cách giảm chi phí:**
- Gộp nhiều commit liên tiếp trên cùng PR thành một lần chạy (huỷ job cũ khi có push mới — `concurrency: cancel-in-progress`).
- Chỉ chạy 3 lần lặp khi lần đầu đã vượt ngưỡng WARN; nếu lần đầu xanh rõ ràng thì dừng luôn ⇒ tiết kiệm ~60 % thời gian ở trường hợp phổ biến.
- T3 chạy nightly, không chạy mỗi merge.

### 6.2 Báo động giả

| Nguồn nhiễu | Mức độ | Biện pháp giảm |
| :--- | :--- | :--- |
| **Runner chia sẻ CPU với job khác** | **Cao — nguồn lớn nhất** | Median của 3 lần chạy; ngưỡng 20 %; ghi nhận loại runner vào baseline |
| Cache lạnh / JIT chưa ấm | Trung bình | Bỏ 30 s đầu mỗi lần chạy |
| Dữ liệu seed khác nhau giữa các lần | Trung bình | Seed **cố định, có kiểm soát** (400 user / 505 product), reset DB trước mỗi lần |
| Đổi phiên bản Node hoặc runner image | Trung bình | Ghim phiên bản Node; coi việc nâng cấp runner là sự kiện **cập nhật baseline bắt buộc** |
| Thay đổi trong chính test plan | Thấp | Đưa `test-plans/**` vào path filter để test plan đổi thì baseline cũng phải đo lại |
| Mạng nội bộ CI | Thấp | Chạy SUT và JMeter trong cùng job, qua loopback |

**Chỉ số theo dõi sức khỏe hệ thống:** tỉ lệ **cảnh báo được xác nhận là regression thật** trên tổng số cảnh báo. Nếu tụt dưới **50 %**, hệ thống đang mất uy tín — phải nới ngưỡng hoặc giảm nhiễu, chứ không phải yêu cầu đội ngũ chịu đựng.

### 6.3 Bỏ sót (false negative) — mặt trái ít được nhắc

Ngưỡng rộng để tránh báo động giả đồng nghĩa với việc **regression 15 % sẽ lọt qua**. Và nhiều regression 15 % tích lũy qua sáu tháng thành gấp đôi độ trễ mà không lần nào bị chặn.

Biện pháp: T3 nightly **so với baseline của 30 ngày trước**, không chỉ so với hôm qua. Trôi chậm chỉ lộ ra ở cửa sổ dài.

```
Cảnh báo trôi: p95_hôm_nay / p95_30_ngày_trước − 1 > 25%  ⇒ mở issue tự động
```

### 6.4 Bảng đánh đổi tổng hợp

| Lựa chọn | Được | Mất |
| :--- | :--- | :--- |
| Ngưỡng chặt (10 %) | Bắt được regression nhỏ | Nhiều báo động giả → đội ngũ mất niềm tin |
| Ngưỡng rộng (30 %) | Gần như không báo động giả | Bỏ lọt regression vừa; trôi chậm không bao giờ bị bắt |
| Chạy mọi commit | Phát hiện sớm nhất | Chi phí CI cao, hàng đợi tắc |
| Chỉ chạy nightly | Rẻ | Regression đã merge rồi mới biết, khó truy commit thủ phạm |
| Runner riêng | Nhiễu thấp, ngưỡng siết được | Chi phí hạ tầng + công vận hành |
| Runner chia sẻ | Miễn phí/rẻ | Nhiễu cao, buộc phải nới ngưỡng |
| Lưu raw `.jtl` vĩnh viễn | Điều tra hậu kiểm được | Kho phình vài GB/tháng |

**Khuyến nghị cho dự án quy mô EShop:** runner chia sẻ + median 3 lần + ngưỡng 20 % + nightly đầy đủ + giữ raw 14 ngày. Đây là điểm cân bằng giữa chi phí gần bằng không và độ tin cậy đủ dùng.

---

## 7. Workflow mẫu — `.github/workflows/perf-regression.yml`

> Tạo file này ở dạng **đề xuất**, đặt `workflow_dispatch` là trigger duy nhất được bật, để không tự chạy trên repo của nhóm và làm phiền các thành viên khác. Ghi rõ trong report rằng đây là bản trình bày ý tưởng.

```yaml
name: Performance Regression Gate

on:
  workflow_dispatch:          # BẬT: chạy tay để demo
  # pull_request:             # TẮT: bản đề xuất, chưa bật tự động
  #   paths:
  #     - 'backend/**'
  #     - 'performance-testing/test-plans/**'
  # schedule:
  #   - cron: '0 19 * * *'    # 02:00 giờ VN

concurrency:
  group: perf-${{ github.ref }}
  cancel-in-progress: true

jobs:
  smoke-perf:
    if: "!contains(github.event.pull_request.labels.*.name, 'perf-skip')"
    runs-on: ubuntu-latest
    timeout-minutes: 20

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '17'

      - name: Cache JMeter
        id: cache-jmeter
        uses: actions/cache@v4
        with:
          path: ~/jmeter
          key: jmeter-5.6.3

      - name: Install JMeter
        if: steps.cache-jmeter.outputs.cache-hit != 'true'
        run: |
          curl -sL https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.6.3.tgz \
            | tar xz -C $HOME
          mv $HOME/apache-jmeter-5.6.3 $HOME/jmeter

      - name: Start SUT with fixed dataset
        run: |
          cd backend && npm ci
          node database.js
          node ../performance-testing/scripts/seed_perf_data.js
          node server.js &
          npx wait-on http://localhost:3000/api/products -t 30000

      - name: Run smoke perf 3 times
        run: |
          for i in 1 2 3; do
            $HOME/jmeter/bin/jmeter -n \
              -t performance-testing/test-plans/ci_smoke.jmx \
              -l results/run-$i.jtl \
              -Jcsvdir=performance-testing/data \
              -Jthreads=15 -Jduration=120
          done

      - name: Analyse and compare against baseline
        run: |
          python performance-testing/scripts/analyze_jtl.py \
            --jtl results/run-1.jtl --out-dir results/r1 --scenario CI
          python performance-testing/scripts/analyze_jtl.py \
            --jtl results/run-2.jtl --out-dir results/r2 --scenario CI
          python performance-testing/scripts/analyze_jtl.py \
            --jtl results/run-3.jtl --out-dir results/r3 --scenario CI
          python performance-testing/scripts/compare_baseline.py \
            --runs results/r1 results/r2 results/r3 \
            --baseline performance-testing/baseline/baseline.json \
            --warn-pct 10 --fail-pct 20 \
            --out results/comparison.md

      - name: Comment result on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const body = fs.readFileSync('results/comparison.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body
            });

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: perf-results
          path: results/
          retention-days: 14
```

### 7.1 `ci_smoke.jmx` và `compare_baseline.py`

- **`ci_smoke.jmx`**: bản rút gọn của `23127207_Load_*.jmx`, cùng 5 sampler, nhưng `Threads` và `Duration` đọc từ tham số CLI: `${__P(threads,15)}`, `${__P(duration,120)}`. Listener: Simple Data Writer (nhẹ nhất, phù hợp CI).
- **`compare_baseline.py`**: đọc N thư mục kết quả, lấy median p95 theo label, so với `baseline.json`, sinh bảng Markdown, và `exit 1` khi vượt `--fail-pct`.

Bảng bình luận PR trông như sau:

```markdown
### 📊 Performance Regression Check

| Label | Baseline p95 | Hiện tại (median of 3) | Δ | Kết quả |
|:--|--:|--:|--:|:--|
| 01_Login | 42 ms | 44 ms | +4,8 % | ✅ |
| 02_BrowseProducts | 421 ms | 538 ms | **+27,8 %** | ❌ |
| 03_ProductDetail | 38 ms | 39 ms | +2,6 % | ✅ |
| 04_AddToCart | 25 ms | 26 ms | +4,0 % | ✅ |
| 05_Checkout | 156 ms | 161 ms | +3,2 % | ✅ |

**Kết luận: FAIL** — `02_BrowseProducts` vượt ngưỡng 20 %.
Runner: `ubuntu-latest-2core` · Baseline commit: `d5eaf839` · 3 lần chạy, lấy median.
```

---

## 8. Lộ trình triển khai

| Giai đoạn | Thời gian | Việc làm | Tiêu chí hoàn thành |
| :--- | :--- | :--- | :--- |
| 1 | Tuần 1 | Dựng `ci_smoke.jmx` + `compare_baseline.py`, chạy tay bằng `workflow_dispatch` | Chạy được 3 lần liên tiếp, kết quả nhất quán |
| 2 | Tuần 2 | Đo nhiễu nền: chạy 10 lần trên cùng commit, tính độ lệch p95 | Có con số nhiễu thật để chốt ngưỡng |
| 3 | Tuần 3 | Bật chế độ **chỉ cảnh báo**, chưa chặn merge | Thu thập tỉ lệ báo động giả trong 2 tuần |
| 4 | Tuần 5 | Nếu tỉ lệ cảnh báo đúng > 70 %, bật chặn merge | |
| 5 | Tuần 6 | Bật nightly T3 + cảnh báo trôi 30 ngày | |

Giai đoạn 2 và 3 là phần hay bị bỏ qua nhất, và cũng là phần quyết định hệ thống có được tin dùng hay không. **Bật chặn merge trước khi biết tỉ lệ báo động giả là cách nhanh nhất để cả đội ghét hệ thống này.**

---

## 9. Checklist

- [ ] Có flow chart Mermaid, render được
- [ ] Có bàn **cả hai** loại lỗi: báo động giả **và** bỏ sót
- [ ] Có bảng chi phí với con số ước tính cụ thể
- [ ] Giải thích được vì sao chọn **p95** chứ không phải trung bình/p99
- [ ] Giải thích được vì sao ngưỡng **20 %** chứ không phải 5 %
- [ ] Có file workflow mẫu, để `workflow_dispatch` để không tự chạy
- [ ] Có lộ trình triển khai theo giai đoạn
- [ ] Đã điền `<<FILL>>` ở §5.1 bằng số nhiễu đo thật (hoặc ghi rõ là ước lượng chưa đo)
- [ ] Commit: `docs(perf): add continuous performance testing proposal`
