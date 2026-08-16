---
name: perf-jmeter
description: >-
  Generate JMeter Load/Stress/Spike/Soak test plans for ANY REST endpoint group
  from a single JSON spec, and analyze the resulting raw .jtl into a ground-truth
  metrics + performance-threshold report. Use when the user wants to build JMeter
  test plans for an API workflow, create a data-driven load test, or
  analyze/interpret .jtl logs (p95, throughput, error rate, regression
  thresholds). Running the plans is done by the user.
---

# perf-jmeter — reusable performance-testing & log-analysis workflow

Đóng gói workflow đã dùng trong HW05 (23127438 — Đặng Trường Nguyên) để **tái dùng cho bất kỳ endpoint group nào**: mô tả nhóm endpoint bằng 1 file JSON → sinh 4 test plan → *(người dùng tự chạy)* → phân tích `.jtl` thô ra metric + bảng threshold.

> Skill này **chỉ lo sinh plan và phân tích log**. Bước **chạy** JMeter (và đo tài nguyên, reset state SUT) do người dùng tự thực hiện — xem mục "Giữa 2 bước" bên dưới.

## Khi nào dùng

- Cần sinh test plan JMeter data-driven (CSV) cho một workflow API mà không muốn dựng tay trong GUI.
- Cần phân tích `.jtl` để lấy **ground truth** (percentile tính từ log thô, không tin dashboard) và đề xuất performance threshold.

## Thành phần

```
perf-jmeter/
├── SKILL.md
├── scripts/
│   ├── gen_plan.py   # spec.json  -> 4 plan .jmx (Load/Stress/Spike/Soak)
│   └── analyze.py    # .jtl -> metric per-endpoint + threshold (console + --md)
└── examples/
    ├── category_guided_buy.json   # spec mẫu (workflow HW05)
    └── users.example.csv          # CSV data-driven mẫu
```

## Quy trình 3 bước

### 1. Mô tả endpoint group (spec JSON)
Copy `examples/category_guided_buy.json` và sửa: `base` (host/port), `csv` (file + tên cột), và mảng `steps`. Mỗi step khai: `method`, `path`, `body`/`query`, `auth` (true → tự gắn `Bearer ${token}`), `extract` (JSON post-processor), `assert_code` / `assert_jsonpath` / `assert_contains`, và `think_ms: [delay, range]`. `scenarios` là optional (đã có default hợp lý).

Nguyên tắc thiết kế spec — **học từ HW05, phải giữ**:
- **Assertion phải kiểm nội dung, không chỉ status.** SUT lỗi có thể trả HTTP 200 với body rỗng → luôn thêm `assert_jsonpath`/`assert_contains`.
- **CSV keyword phải khớp dữ liệu thật.** Verify bằng curl trước; keyword không match → assertion fail 100%, làm bẩn error rate.
- **Think-time bám hành vi người thật** (1–3s cho read). Skill tự rút ngắn think-time cho Stress (×0.5) và Spike (×0.3).

### 2. Sinh test plan
```bash
python3 scripts/gen_plan.py <spec.json> <output_dir>
# -> <prefix>_Load_<date>.jmx, _Stress_, _Spike_, _Soak_
```
Đảm bảo file CSV (khai trong `spec.csv.file`) nằm ở thư mục làm việc khi chạy JMeter (đường dẫn CSV là tương đối). 4 plan tự gắn **4 listener khác nhau** (Summary / Aggregate / View Results Tree / Graph) để thoả yêu cầu "nhiều report view".

### Giữa 2 bước — người dùng tự chạy
Bước chạy JMeter **không thuộc skill**, người dùng tự thực hiện. Lưu ý khi chạy:
- Khởi động SUT trước; chạy non-GUI: `jmeter -n -t <plan.jmx> -l <out.jtl> -e -o <html_dir>` (CSV cùng thư mục làm việc).
- Nếu SUT có cơ chế khoá/seed (như EShop: lockout, DROP+reseed khi restart) thì **reset state giữa các run** và **nạp lại data pool** trước mỗi lần chạy.
- Đo tài nguyên process SUT song song (vd `htop -p $(pgrep -f 'server.js')`) — cần cho evidence/demo (JMeter + monitor cùng khung hình).

### 3. Phân tích + đề xuất threshold
```bash
python3 scripts/analyze.py results/load/*.jtl results/stress/*.jtl --md report.md
```
In metric tổng + per-endpoint (percentile tính từ log thô) và sinh `report.md` với **bảng threshold regression-based**: p95 alert ≈ 3× baseline, error < 0.5%, throughput floor = 80% baseline, và chỉ ra **endpoint canary** (mean cao nhất — thường là endpoint ghi đĩa như checkout).

## Bẫy diễn giải cần tránh (từ Task 2)
Khi để AI/dashboard đọc kết quả, đối chiếu lại với `analyze.py`: đừng nhầm **p95 với mean**, đừng đọc **max lẻ 1 sample** thành "suy giảm hệ thống", CPU cao trên **1 core** không phải "bão hòa toàn máy", và **baseline có think-time không phải capacity tối đa**. `analyze.py` là ground truth để bắt các lỗi này.

## Cài như một Claude Code skill (tuỳ chọn)
Copy thư mục `perf-jmeter/` vào `~/.claude/skills/` (hoặc `.claude/skills/` của project) → gọi bằng `/perf-jmeter` hoặc để agent tự kích hoạt khi gặp task perf-testing.
