> **Trạng thái bằng chứng:** chỉ **[DOC]**, **[DOC + ASSUMPTION]**, **[ASSUMPTION]** và kế hoạch chưa chạy; ngày chốt 2026-07-14.

### 1. Tổng quan

`wrk` là HTTP benchmarking CLI do Will Glozer (`wg`) duy trì, tối ưu tạo tải trên máy đa lõi bằng epoll/kqueue và mở rộng request/response qua Lua. [Repository/README](https://github.com/wg/wrk), [maintainer](https://github.com/wg) (truy cập 2026-07-14). **[DOC]**

### 2. Cost và licence

Source mở theo **Modified Apache 2.0 License Version 2.0.1 (February 2015)**, không cần tài khoản/trial; cần giữ đúng qualifier license. [LICENSE](https://raw.githubusercontent.com/wg/wrk/master/LICENSE) (truy cập 2026-07-14). **[DOC]**

### 3. Installation và platform support

Hỗ trợ phần lớn hệ kiểu UNIX; build bằng GNU make (`gmake` trên BSD), LuaJIT và OpenSSL, có dependency bundle/system option. INSTALL không tuyên bố native Windows, nên lớp Windows cần WSL/VM/container tự pin. [INSTALL](https://github.com/wg/wrk/blob/master/INSTALL) (truy cập 2026-07-14). **[DOC]**

### 4. Scripting hoặc configuration model

CLI điều khiển workload; file Lua có hooks `setup/init/delay/request/response/done`, dễ version-control. Mỗi thread có một Lua environment; response callback làm giảm khả năng phát tải. [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC]**

### 5. Workload capabilities

`-t` threads, `-c` connections, `-d` duration, timeout, header, latency và Lua delay/request. Mô hình chính là fixed connections trong duration; không có staged arrival/ramp, weighted multi-scenario hay distributed controller trong CLI. State Lua per-thread không tương ứng VU/connection khi một thread quản lý nhiều connections, nên correlation login/cart dễ trộn session. [README options](https://github.com/wg/wrk#command-line-options), [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 6. Assertions và validation

Lua `response(status, headers, body)` cho phép đếm/ghi custom check, nhưng không có assertion DSL/SLA threshold contract native. Business pass/fail và CI exit cần script/wrapper được review. [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 7. Metrics và reporting

Console có latency/Req-Sec average, stdev, max, total, RPS, transfer/sec; `--latency` thêm distribution. Hook `done` đọc percentile tùy ý, histogram value/count và connect/read/write/status/timeout errors; artifact machine-readable chuẩn phải tự xây. [README](https://github.com/wg/wrk), [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC]**

### 8. CI/CD và automation

CLI/Lua hợp pipeline và chạy local/offline; threshold, stable JSON/CSV, exit policy và custom container cần nhóm cung cấp/pin. Trang Releases không công bố package release, nên phải lưu commit/tag/binary provenance. [Releases](https://github.com/wg/wrk/releases), [INSTALL](https://github.com/wg/wrk/blob/master/INSTALL) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 9. EShop suitability

Tốt cho product/catalog API cô lập và header/auth tĩnh. Lua có thể biến đổi request/đọc response nhưng session state per-thread không an toàn để mặc định mô hình login→cart→checkout ở concurrency cao. [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 10. AI-assisted potential

AI có thể sinh Lua, parser, workload matrix và Failure Mode checks; phải audit thread-vs-connection state, callback overhead, secret, HTTP formatting và exit policy. Script AI chưa audit không được coi là đúng. [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 11. Classroom suitability

CLI cơ bản có thể demo trong 25 phút nếu đã build sẵn; build Windows/WSL và Lua state model khiến buổi tự cài+tạo journey khó vừa timebox. [INSTALL](https://github.com/wg/wrk/blob/master/INSTALL), [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 12. Điểm mạnh trong phạm vi seminar

Tạo tải endpoint hiệu quả, latency distribution/histogram API tốt, Lua linh hoạt cho request-level instrumentation. [README](https://github.com/wg/wrk), [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC]**

### 13. Hạn chế trong phạm vi seminar

Không có business-VU/session model, staged rate, SLA gate hoặc report artifact chuẩn; response processing giảm load capacity. Đây là ranh giới endpoint benchmark, không phải nhận xét tuyệt đối về chất lượng. [README](https://github.com/wg/wrk), [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 14. Smoke Test Plan

**[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**

- **Mục tiêu:** phát GET nhỏ, thu latency distribution và quan sát HTTP status bằng reviewed Lua response callback mà client chưa bão hòa.
- **Prerequisites:** `[VERIFIED_BASE_URL]`, `[VERIFIED_PRODUCT_PATH]`, `[EXPECTED_STATUS]`, WSL/Linux/container và monitoring đã xác minh. **[ASSUMPTION]**
- **Installation/setup:** build theo [INSTALL](https://github.com/wg/wrk/blob/master/INSTALL); lưu provenance/version. Version-control `status_check.lua` dùng `response(status, headers, body)` và thread aggregation; human-review trước khi chạy. Callback overhead chỉ chấp nhận ở smoke. ([SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) — truy cập 2026-07-14)
- **Một request:** `GET [VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]`.
- **Command:** `wrk -t2 -c4 -d10s --latency -s status_check.lua "[VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]"` theo [README](https://github.com/wg/wrk) và [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14).
- **Expected result:** duration 10s, RPS/latency distribution, status counters và không socket error; không dự đoán số đo.
- **Evidence:** binary/script hashes, review record, command, stdout/stderr/exit, aggregated status counters, EShop commit, timestamps và client/SUT resources.
- **Possible errors:** build/routing/TLS/file descriptor; CPU saturation; nhầm threads với VU; Lua aggregation sai; callback overhead; wrapper che failure.
- **Success criteria:** duration/connections đúng, `unexpected_status=0`, zero socket error, client headroom và evidence đủ; negative status phải làm reviewed wrapper fail.

### 15. Điểm đánh giá

| Tiêu chí | Trọng số | Điểm | Evidence |
|---|---:|---:|---|
| Cost & access | 8% | 5 | Source/license mở. **[DOC]** |
| Learning curve | 8% | 3 | CLI dễ, build/Lua trung bình. **[DOC]** |
| EShop fit | 15% | 2 | Endpoint tốt, journey yếu. **[DOC + ASSUMPTION]** |
| Multi-step journey | 12% | 2 | Lua nhưng state per-thread. **[DOC + ASSUMPTION]** |
| Workload control | 10% | 3 | Threads/connections/duration/delay. **[DOC]** |
| Assertions/checks | 8% | 2 | Custom Lua, không contract native. **[DOC + ASSUMPTION]** |
| Reporting | 8% | 3 | Console/percentile/histogram API. **[DOC]** |
| CI/CD | 7% | 2 | Wrapper/gate/artifact tự xây. **[DOC + ASSUMPTION]** |
| Reproducibility | 7% | 4 | Lệnh/Lua pin được; pin build. **[DOC]** |
| Local/offline | 5% | 5 | Không SaaS. **[DOC]** |
| AI-assisted potential | 7% | 3 | Lua hữu ích nhưng audit sâu. **[DOC + ASSUMPTION]** |
| Classroom suitability | 5% | 3 | Demo CLI được, setup/Lua tốn thời gian. **[DOC + ASSUMPTION]** |
| Community | 0% | 4 | Repo/issues và docs công khai; không ảnh hưởng tổng. [Repository](https://github.com/wg/wrk) (truy cập 2026-07-14). **[DOC]** |

**Tổng có trọng số: 58.2/100**; Community 0% không tham gia công thức.

### 16. Kết luận sơ bộ

**Supporting benchmark tool.** Dùng đo endpoint khi cần generator hiệu quả/Lua nhỏ, không thay công cụ journey.

### 17. Câu hỏi phản biện

<details>
<summary>Phản biện và trả lời</summary>

1. **Có Lua là đủ login–cart–checkout?** Không: state per-thread, một thread có nhiều connection nên correlation per-user không được bảo đảm. [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
2. **RPS cao hơn chứng minh SUT tốt hơn?** Không nếu callback/client CPU/network bão hòa hoặc workload khác; phải quan sát generator. [README](https://github.com/wg/wrk), [SCRIPTING](https://github.com/wg/wrk/blob/master/SCRIPTING) (truy cập 2026-07-14). **[DOC]**
3. **CI xanh nghĩa là SLA đạt?** Không; CLI không có threshold contract mặc định, cần parser/policy exit. [README options](https://github.com/wg/wrk#command-line-options) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

</details>
