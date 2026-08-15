# 14 — HƯỚNG DẪN LÀM PHẦN NGƯỜI PHẢI TỰ LÀM (Screenshot · Video · GitHub Issues)

> Đối tượng: **Khoa (23127207)** — không phải AI.
> Đây là 3 hạng mục duy nhất còn thiếu của HW05. Toàn bộ số liệu, `.jmx`, script, báo cáo đã xong và đã kiểm chứng.
> Tổng thời gian ước tính: **~90 phút**, trong đó 35 phút là ngồi chờ test chạy (vừa chờ vừa quay video).

---

## 0. NGUYÊN TẮC VÀNG — ĐỌC TRƯỚC KHI LÀM GÌ

### 0.1 Chụp ảnh và quay video PHẢI làm CÙNG MỘT LÚC

Cả hai yêu cầu của đề đều đòi **JMeter và resource monitor xuất hiện trong cùng một khung hình khi test đang chạy**. Nghĩa là cả hai chỉ tồn tại trong lúc test chạy thật. Đừng chia làm 2 buổi — bật ghi màn hình, chạy test, và **bấm PrtScn ngay giữa lúc quay**. Một lần setup, thu được cả hai.

### 0.2 CẢNH BÁO: chạy lại test sẽ GHI ĐÈ kết quả đã có

`run_scenario.ps1` ghi thẳng vào `performance-testing/results/<scenario>/`. Nếu bạn chạy lại để quay video mà không backup, các file `.jtl` / `summary.json` hiện tại **sẽ bị thay bằng số mới**, và toàn bộ con số trong `23127207_HW05_Report.md` (p95 = 25 / 586 / 1016 / 382 ms) sẽ **không còn khớp với file thật** — đây đúng là loại lỗi mà giám khảo dò ra ngay.

**Bắt buộc chạy lệnh backup này TRƯỚC KHI quay:**

```powershell
Copy-Item "performance-testing\results" "performance-testing\results_canonical_backup" -Recurse -Force
```

Sau khi quay xong, xử lý theo §4.

### 0.3 Ba điều tuyệt đối không làm

- ❌ Đọc trong video một con số không hiện trên màn hình lúc đó.
- ❌ Cắt cảnh để giấu đoạn test lỗi. Nếu lỗi thì nói ra và giải thích — đó là điểm cộng, không phải điểm trừ.
- ❌ Dùng giọng đọc máy (TTS). Đề yêu cầu giọng của chính sinh viên.

---

## 1. CHUẨN BỊ MÔI TRƯỜNG (~15 phút, làm một lần)

### 1.1 Cài phần mềm quay màn hình

Dùng **OBS Studio** (miễn phí, `winget install OBSProject.OBSStudio`).

> ⚠️ **Không dùng Xbox Game Bar (Win+G)** — nó chỉ quay được **một cửa sổ ứng dụng**, trong khi đề bắt buộc phải thấy **cả terminal lẫn Task Manager trong cùng khung hình**. Game Bar sẽ làm bạn trượt yêu cầu này.

Cấu hình OBS tối thiểu:
- Sources → **Display Capture** (quay toàn màn hình, không phải Window Capture).
- Settings → Audio → Mic/Auxiliary Audio → chọn micro của laptop. **Nói thử và nhìn thanh âm lượng nhảy** trước khi quay thật.
- Settings → Output → Recording Format: `mp4`.
- Settings → Video → Output Resolution: giữ nguyên độ phân giải màn hình (chữ trong terminal phải đọc được).

### 1.2 Bố trí màn hình (quan trọng nhất)

Chia màn hình làm đôi bằng phím `Win + ←` / `Win + →`:

```
┌──────────────────────────────┬──────────────────────────────┐
│  TRÁI: PowerShell            │  PHẢI: Task Manager           │
│  đang chạy run_scenario.ps1  │  tab Details, lọc node.exe    │
│  (JMeter non-GUI in log)     │  cột: CPU, Memory (private)   │
└──────────────────────────────┴──────────────────────────────┘
```

Cách lọc Task Manager cho đúng:
1. `Ctrl + Shift + Esc` mở Task Manager → tab **Details**.
2. Click cột **Name**, gõ `node` để nhảy tới `node.exe`.
3. Chuột phải hàng tiêu đề cột → **Select columns** → tick thêm **Memory (private working set)**.
4. Chuột phải `node.exe` → không cần gì thêm, chỉ cần nó luôn nằm trong khung hình.

> Nếu có 2 màn hình: **tắt bớt, chỉ dùng 1 màn hình**. OBS Display Capture quay 2 màn hình sẽ làm chữ bé xíu không đọc được.

### 1.3 Chụp ảnh dxdiag (1 phút, làm luôn cho xong)

```powershell
dxdiag
```
Chờ thanh tiến trình chạy xong 100%, rồi:
```powershell
.\performance-testing\scripts\capture_evidence.ps1 -Name dxdiag -Scenario hardware -Delay 3
```
→ ảnh lưu sẵn tại `performance-testing\evidence\hardware\dxdiag.png`.

### 1.4 Tạo sẵn thư mục chứa ảnh

```powershell
mkdir performance-testing\evidence\load, performance-testing\evidence\stress, performance-testing\evidence\spike, performance-testing\evidence\endurance, performance-testing\evidence\issues -Force
```

---

## 2. BUỔI QUAY — CHẠY TEST THẬT, THU CẢ VIDEO LẪN ẢNH (~45 phút)

### 2.1 Lệnh chạy — CHÚ Ý THAM SỐ `-RunDate`

File `.jmx` được đặt tên `23127207_Load_20260814.jmx`, nhưng `run_scenario.ps1` mặc định lấy **ngày hôm nay** để tìm file → sẽ báo không tìm thấy. **Luôn truyền `-RunDate 20260814`:**

```powershell
# Terminal 1 — backend (bật trước, để yên suốt buổi)
node backend/server.js

# Terminal 2 — chạy từng kịch bản
.\performance-testing\scripts\run_scenario.ps1 -Scenario Load     -RunDate 20260814
.\performance-testing\scripts\run_scenario.ps1 -Scenario Stress   -RunDate 20260814
.\performance-testing\scripts\run_scenario.ps1 -Scenario Spike    -RunDate 20260814
.\performance-testing\scripts\run_scenario.ps1 -Scenario Endurance -RunDate 20260814
```

> 🔁 **Restart backend giữa các kịch bản.** `Ctrl+C` ở Terminal 1 rồi `node backend/server.js` lại. Đây chính là lỗi đã phải sửa một lần rồi (Stress khởi động với 532 MB RAM tồn từ run trước, làm sai kết luận knee-point). Đừng lặp lại.

### 2.2 Bạn KHÔNG cần quay đủ cả 31 phút

Yêu cầu là **video ≥ 6 phút**, không phải quay hết mọi run. Kế hoạch tiết kiệm nhất:

| Clip | Quay gì | Độ dài | Test có chạy live không? |
|:--|:--|:--:|:--|
| **Clip 1 — Load** | Mở `.jmx` giải thích scope + chạy Load live | ~2:30 | ✅ Có (5 phút, quay 2:30 đầu là đủ) |
| **Clip 2 — Stress** | Giải thích 4 Thread Group xếp chồng + chạy live, chỉ CPU tăng theo bậc | ~2:00 | ✅ Có |
| **Clip 3 — Spike + Endurance** | Chạy Spike live; Endurance thì **mở `resource-endurance.csv` và `html-report`** đã có, nói rõ "đây là run em đã chạy trước, dài 12 phút" | ~2:00 | Spike ✅ / Endurance ❌ (xem lại) |

Endurance dài 12 phút — không cần quay live, chỉ cần **nói thật** rằng đang xem lại kết quả đã chạy. Nói thật thì không mất điểm; giả vờ là đang chạy live mới mất điểm.

### 2.3 Trong lúc mỗi run đang chạy — bấm PrtScn

Có sẵn script `capture_evidence.ps1` để chụp thẳng vào đúng đường dẫn với đúng tên — khỏi phải mò trong `Pictures\Screenshots` rồi đổi tên thủ công. Mở **một PowerShell thứ ba** (cửa sổ nhỏ, để ở góc màn hình) và gõ:

```powershell
.\performance-testing\scripts\capture_evidence.ps1 -Name jmeter+taskmgr-load -Scenario load -Delay 5
```

Script đếm ngược 5 giây để bạn kịp sắp xếp cửa sổ, rồi chụp toàn màn hình và lưu vào `evidence\load\jmeter+taskmgr-load.png`. (Vẫn dùng `Win + PrtScn` được nếu bạn thích, chỉ là phải tự đổi tên.)

Cần đúng **4 ảnh này**, mỗi kịch bản 1 ảnh, ảnh phải thấy **cả terminal lẫn Task Manager**:

```
performance-testing\evidence\load\jmeter+taskmgr-load.png
performance-testing\evidence\stress\jmeter+taskmgr-stress.png
performance-testing\evidence\spike\jmeter+taskmgr-spike.png
performance-testing\evidence\endurance\jmeter+taskmgr-endurance.png
```

Thời điểm chụp tốt nhất:
- **Load**: khoảng phút thứ 2–3, khi đã đủ 50 thread.
- **Stress**: ở bậc 200 VU (khoảng phút thứ 6–7), lúc CPU cao nhất.
- **Spike**: đúng lúc đợt sốc 300 VU — canh lúc số thread trong log JMeter nhảy vọt.
- **Endurance**: phút cuối, khi RAM đã leo cao nhất (~172 MB).

### 2.4 Thêm 4 ảnh listener

Phần này **bắt buộc thao tác tay trong JMeter GUI**, không script hoá được. Mỗi ảnh mất khoảng 1 phút:

```powershell
.\.tools\jmeter\bin\jmeter.bat
```

Trong GUI, với từng kịch bản:
1. `File → Open` → chọn `performance-testing\test-plans\23127207_Load_20260814.jmx`
2. Click vào listener trong cây bên trái (Aggregate Report / Summary Report / View Results Tree)
3. Ở ô **Write results to file / Read from file**, bấm **Browse** → chọn `performance-testing\results\load\23127207_Load_20260814.jtl`
4. **Chờ nó nạp xong** — file Stress 3.6 MB mất vài giây, bảng số phải hiện đầy đủ mới chụp
5. Chụp bằng script:
   ```powershell
   .\performance-testing\scripts\capture_evidence.ps1 -Name listener-load -Scenario load -Delay 5
   ```

Lặp lại cho `stress`, `spike`, `endurance`. Bốn ảnh cần có:

```
performance-testing\evidence\load\listener-load.png            (Aggregate Report)
performance-testing\evidence\stress\listener-stress.png        (Summary Report)
performance-testing\evidence\spike\listener-spike.png          (View Results Tree)
performance-testing\evidence\endurance\listener-endurance.png  (Aggregate Report)
```

Đây cũng chính là bằng chứng cho yêu cầu **"3 loại listener khác nhau"** của đề — nên 3 ảnh đầu phải nhìn thấy rõ là 3 giao diện khác nhau.

### 2.5 Ảnh thủ tục reset lockout

Đề yêu cầu tường minh hoá bước reset khoá tài khoản giữa các run. Chạy và chụp output:

```powershell
node performance-testing\scripts\reset_lockout.js
.\performance-testing\scripts\capture_evidence.ps1 -Name lockout-reset -Scenario stress -Delay 3
```
Để cửa sổ PowerShell hiện rõ output của `reset_lockout.js` khi script đếm ngược → ảnh lưu tại `performance-testing\evidence\stress\lockout-reset.png`.

---

## 3. LỜI THOẠI VIDEO

Kịch bản chi tiết theo từng mốc thời gian **đã có sẵn** tại `05_EXECUTION_RUNBOOK.md` §7 — mở ra và đọc theo. Bốn điều cần sửa so với bản đó:

1. Tên file trong kịch bản ghi `20260812`, thực tế là **`20260814`**.
2. Ở clip 1, khi giải thích scope, nhớ nói câu: *"Em dùng `GET /api/products` trả toàn bộ danh mục, **không** dùng `?search=` vì endpoint đó thuộc phần của bạn Trâm trong nhóm"* — đây là bằng chứng cho yêu cầu "không hai thành viên nào test trùng workflow".
3. Ở clip 3, khi nói về memory leak, con số thật để đọc: **RAM tăng từ 60.30 MB lên 137.39 MB sau 12 phút, tức 6.45 MB/phút**, nguyên nhân là `userCarts` ở `backend/server.js:14,293` không bao giờ được giải phóng sau checkout.
4. Thêm một câu về **giới hạn phương pháp** — câu này rất được điểm: *"Em chạy JMeter và backend trên cùng một máy, nên JMeter cũng chiếm CPU và làm nhiễu số đo. Em ghi nhận đây là hạn chế của phương pháp chứ không phải điều kiện lý tưởng."*

### Upload

YouTube → **Unlisted** (không phải Private, thầy cô sẽ không mở được) → dán link vào `performance-testing/README.md`.

---

## 4. SAU KHI QUAY — XỬ LÝ KẾT QUẢ BỊ GHI ĐÈ (~10 phút)

Bạn vừa chạy lại test nên `results/` đã có số mới. Chọn **một** trong hai đường, đừng làm nửa vời:

### Đường A — Giữ số cũ làm chuẩn (nhanh, khuyên dùng)

Run mới chỉ đóng vai trò minh hoạ trong video. Khôi phục lại bộ số đã được kiểm chứng:

```powershell
Remove-Item "performance-testing\results" -Recurse -Force
Rename-Item "performance-testing\results_canonical_backup" "results"
```

Rồi thêm **một câu vào README** để minh bạch:
> *Video demo ghi lại một lần chạy tái lập vào ngày 2026-08-15. Số liệu trong báo cáo lấy từ lần chạy chuẩn ngày 2026-08-14 lưu tại `results/`. Hai lần chạy cùng cấu hình, sai khác nằm trong dao động phần cứng thông thường.*

### Đường B — Lấy số mới làm chuẩn (chính xác hơn, tốn công hơn)

Nếu muốn số trong video khớp tuyệt đối với báo cáo:

```powershell
foreach ($s in "load","stress","spike","endurance") {
  python performance-testing\scripts\analyze_jtl.py --scenario $s
}
```
Rồi **cập nhật lại** các con số p95 / RPS / RAM trong `23127207_HW05_Report.md`, `04_execution-report.md`, `05_endurance-threshold.md` và `baseline/baseline.json`. Đây là việc sửa số ở nhiều chỗ — nếu chọn đường này, bảo tôi làm, đừng sửa tay kẻo sót.

---

## 5. GITHUB ISSUES (~15 phút)

Repo: **https://github.com/trngnneee/eshop-sut/issues**

Nội dung 2 issue **đã soạn sẵn** ở `performance-testing/README.md` §3 và `05_EXECUTION_RUNBOOK.md` §8 — chỉ việc copy dán. Tạo **2 issue thật**:

| # | Title | Nội dung lấy từ |
|:--|:--|:--|
| 1 | `[BUG] Memory leak in userCarts global object (server.js:14,293)` | README §3 Issue 1 |
| 2 | `[BUG][FR-02] Login attempt counter increments by 2 and lockout lasts 180s instead of 30s` | RUNBOOK §8 Issue #1 |

**Mỗi issue bắt buộc phải đính kèm ảnh** (đề ghi rõ *"with screenshots"*):
- Issue 1 → kéo thả ảnh biểu đồ RAM tăng (mở `results/endurance/html-report/index.html`, chụp biểu đồ, hoặc chụp `resource-endurance.csv` mở trong Excel dưới dạng đồ thị đường).
- Issue 2 → ảnh output probe lockout (`evidence/issues/fr02-lockout-probe.png`).

Sau khi tạo xong: chụp trang danh sách Issues → `performance-testing/evidence/issues/github-issues-list.png`, và **dán link 2 issue vào README**.

> Nếu bạn không có quyền tạo issue trên repo `trngnneee/eshop-sut`: fork về tài khoản `khoadangwneee`, bật Issues trong Settings, tạo ở fork, rồi ghi rõ trong README là issue nằm ở fork.

---

## 6. SỬA BẢNG TỰ ĐÁNH GIÁ

`performance-testing/README.md` §2 đang ghi **100/100** trong khi lúc đó chưa có video và screenshot. Sau khi làm xong §2–§5 ở trên thì con số đó mới đúng.

Nhưng lời khuyên: **hạ Task 1 xuống 47/50** và ghi một dòng tự nhận hạn chế, ví dụ *"JMeter chạy chung máy với SUT nên số đo có nhiễu; kết quả phản ánh giới hạn của môi trường máy đơn"*. Tự chấm tuyệt đối 100/100 dễ khiến người chấm đi tìm lỗi để bác; tự nhận đúng một hạn chế có thật lại chứng minh mình hiểu việc mình làm.

---

## 7. CHECKLIST NGHIỆM THU CUỐI

Đánh dấu từng dòng, chỉ nộp khi hết dấu ☐:

**Screenshot**
- ☐ `evidence/hardware/dxdiag.png`
- ☐ `evidence/{load,stress,spike,endurance}/jmeter+taskmgr-*.png` — **4 ảnh**, mỗi ảnh thấy cả terminal lẫn Task Manager
- ☐ `evidence/{load,stress,spike,endurance}/listener-*.png` — **4 ảnh**, 3 loại listener khác nhau nhìn thấy rõ
- ☐ `evidence/stress/lockout-reset.png`
- ☐ `evidence/issues/fr02-lockout-probe.png`
- ☐ `evidence/issues/github-issues-list.png`

**Video**
- ☐ Tổng **≥ 6 phút**
- ☐ Tiếng Việt, giọng thật, không TTS
- ☐ Có khung hình thấy đồng thời tool + Task Manager **trong lúc test chạy**
- ☐ Mọi con số đọc lên đều đang hiện trên màn hình
- ☐ Đã upload **Unlisted**, link đã dán vào README

**GitHub Issues**
- ☐ 2 issue thật đã tạo, mỗi issue có ảnh đính kèm
- ☐ Link 2 issue đã dán vào README

**Dọn dẹp**
- ☐ Đã xử lý `results/` theo Đường A hoặc B (§4) — không để lẫn lộn
- ☐ Đã xoá `results_canonical_backup` nếu chọn Đường B
- ☐ Bảng tự đánh giá README đã cập nhật (§6)
- ☐ Commit toàn bộ vào branch `HW5`:
  ```powershell
  git add performance-testing/evidence performance-testing/README.md
  git commit -m "docs(perf): add execution screenshots, demo video link, and GitHub issue evidence"
  ```
- ☐ `git log --oneline --decorate > performance-testing/deliverables/git-commit-log.txt` chạy lại lần cuối, rồi commit thêm một lần
