> **Trạng thái bằng chứng:** chỉ **[DOC]**, **[DOC + ASSUMPTION]**, **[ASSUMPTION]** và kế hoạch chưa chạy; ngày chốt 2026-07-14.

### 1. Tổng quan

ApacheBench (`ab`) là CLI benchmark một HTTP endpoint, đi cùng Apache HTTP Server do Apache Software Foundation/PMC duy trì. Mục tiêu chính thức là cho biết số request/giây một HTTP server có thể phục vụ; đây là endpoint benchmark, không phải engine mô phỏng business journey. [Manual `ab`](https://httpd.apache.org/docs/current/en/programs/ab.html), [About HTTP Server](https://httpd.apache.org/ABOUT_APACHE.html) (truy cập 2026-07-14). **[DOC]**

### 2. Cost và licence

Source mở theo Apache License 2.0, không cần tài khoản/trial và sinh viên có thể truy cập tự do. [LICENSE](https://github.com/apache/httpd/blob/trunk/LICENSE), [download](https://httpd.apache.org/download.cgi) (truy cập 2026-07-14). **[DOC]**

### 3. Installation và platform support

`ab` thuộc bộ chương trình HTTP Server. ASF phát source; trang tải nói binary Windows do bên thứ ba cung cấp. Build source có APR/APR-util, PCRE và toolchain tùy cấu hình, nên phải ghi provenance/version của package hoặc binary. [Programs](https://httpd.apache.org/docs/2.4/en/programs/), [Install](https://httpd.apache.org/docs/2.4/install.html), [download](https://httpd.apache.org/download.cgi) (truy cập 2026-07-14). **[DOC]**

### 4. Scripting hoặc configuration model

Cấu hình qua command line và file body POST/PUT; header, cookie và auth có option tĩnh. Lệnh/file dễ version-control nhưng không có module/scenario DSL. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC]**

### 5. Workload capabilities

`-n` tổng request, `-c` concurrency, `-t` duration, `-k` keep-alive, `-s` timeout; một invocation nhắm một URL. Không có arrival-rate phase, scenario mix, VU session, response extractor/correlation hay distributed controller được tài liệu hóa. Shell-chaining nhiều lệnh không tạo journey/session native. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 6. Assertions và validation

Báo failed requests và non-2xx nhưng không có response-body/business assertion hoặc SLA threshold. HTTP 200 không tự chứng minh dữ liệu sản phẩm/checkout đúng. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 7. Metrics và reporting

Console có complete/failed, RPS, time/request, transfer rate và lỗi connect/read/length/exception; `-e` xuất percentile CSV, `-g` TSV measurement, `-w` bảng HTML. Tài liệu cảnh báo `ab` có thể thành bottleneck và không triển khai đầy đủ HTTP/1.x. [Manual/Bugs](https://httpd.apache.org/docs/current/en/programs/ab.html#bugs) (truy cập 2026-07-14). **[DOC]**

### 8. CI/CD và automation

CLI dễ gọi trong pipeline và chạy local/offline, nhưng performance gate/exit policy cần wrapper parse output; không có container release first-party dành riêng cho `ab` trong kênh phát hành chương trình. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html), [download](https://httpd.apache.org/download.cgi) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 9. EShop suitability

Phù hợp GET product/catalog hoặc một API cô lập. Login/session, cart/checkout, data động và multi-step correlation vượt ranh giới native; chỉ có thể replay header/cookie/body tĩnh. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 10. AI-assisted potential

AI có thể soạn lệnh, ma trận `n/c`, parser CSV và checklist Failure Modes; phải audit URL/secret, hai biến thể time/request, sample size và generator saturation. AI không bổ sung session/assertion native. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 11. Classroom suitability

Mental model nhỏ, chạy offline và có thể demo trong 25 phút nếu binary/endpoint đã chuẩn bị; Windows cần package provenance rõ. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html), [download](https://httpd.apache.org/download.cgi) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 12. Điểm mạnh trong phạm vi seminar

Time-to-first-baseline rất ngắn; command/artifact gọn; minh họa rõ concurrency, throughput, latency và client bottleneck. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 13. Hạn chế trong phạm vi seminar

Không phù hợp làm công cụ chính cho journey EShop; thiếu business check/SLA gate; protocol/client bottleneck đe dọa validity. Đây là ranh giới công cụ endpoint benchmark, không phải kết luận công cụ “kém”. [Bugs](https://httpd.apache.org/docs/current/en/programs/ab.html#bugs) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 14. Smoke Test Plan

**[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**

- **Mục tiêu:** xác nhận một GET EShop nhỏ và percentile artifact.
- **Prerequisites:** `[VERIFIED_BASE_URL]`, `[VERIFIED_PRODUCT_PATH]`, `[EXPECTED_STATUS]`, TLS/proxy và resource monitoring đã xác minh. **[ASSUMPTION]**
- **Installation/setup:** cài/build theo [hướng dẫn chính thức](https://httpd.apache.org/docs/2.4/install.html) (truy cập 2026-07-14); lưu `ab -V`, source/package/checksum.
- **Một request:** `GET [VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]`.
- **Command:** `ab -n 20 -c 2 -e ab-percentiles.csv "[VERIFIED_BASE_URL][VERIFIED_PRODUCT_PATH]"` theo [manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14).
- **Expected result:** 20 complete, status theo contract, không connect/read/exception, CSV parse được; chưa dự đoán latency/RPS.
- **Evidence:** version/provenance, command redacted, stdout/stderr, exit code, CSV/hash, EShop commit, timestamp/timezone, CPU/RAM/network client và SUT.
- **Possible errors:** DNS/TLS/refused; response-length biến đổi; file descriptor; Windows provenance; secret leak; client saturation.
- **Success criteria:** count/status đúng, transport error bằng 0 ở smoke load, generator còn headroom, artifacts đủ để rerun; chỉ thêm SLA sau baseline được duyệt.

### 15. Điểm đánh giá

| Tiêu chí | Trọng số | Điểm | Evidence |
|---|---:|---:|---|
| Cost & access | 8% | 5 | Apache-2.0/source mở. **[DOC]** |
| Learning curve | 8% | 5 | CLI nhỏ. **[DOC]** |
| EShop fit | 15% | 2 | Endpoint đơn. **[DOC + ASSUMPTION]** |
| Multi-step journey | 12% | 1 | Không session/extractor. **[DOC + ASSUMPTION]** |
| Workload control | 10% | 2 | Count/concurrency/duration, không phase. **[DOC]** |
| Assertions/checks | 8% | 1 | Protocol failure, không business check. **[DOC + ASSUMPTION]** |
| Reporting | 8% | 3 | Console + percentile CSV/TSV. **[DOC]** |
| CI/CD | 7% | 2 | Cần wrapper/gate. **[DOC + ASSUMPTION]** |
| Reproducibility | 7% | 4 | Lệnh pin được; client bottleneck. **[DOC]** |
| Local/offline | 5% | 5 | Không SaaS. **[DOC]** |
| AI-assisted potential | 7% | 2 | Hữu ích quanh CLI, không đổi semantics. **[DOC + ASSUMPTION]** |
| Classroom suitability | 5% | 5 | Demo nhanh. **[DOC + ASSUMPTION]** |
| Community | 0% | 5 | ASF docs/support/mailing list; không ảnh hưởng tổng. [Support](https://httpd.apache.org/userslist.html) (truy cập 2026-07-14). **[DOC]** |

**Tổng có trọng số: 56.0/100**; Community 0% không tham gia công thức.

### 16. Kết luận sơ bộ

**Supporting benchmark tool.** Dùng làm endpoint baseline phụ, không dùng để tuyên bố hành trình EShop thành công.

### 17. Câu hỏi phản biện

<details>
<summary>Phản biện và trả lời</summary>

1. **Không có journey thì còn giá trị gì?** Cô lập route để có baseline latency/RPS nhanh; claim dừng ở endpoint. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
2. **Có `-e` là p95 đã đáng tin?** Có percentile artifact, nhưng sample size, warm-up và client bottleneck vẫn quyết định validity. [Manual/Bugs](https://httpd.apache.org/docs/current/en/programs/ab.html#bugs) (truy cập 2026-07-14). **[DOC]**
3. **HTTP 200 chứng minh business đúng?** Không; `ab` không có body/business assertion native. [Manual](https://httpd.apache.org/docs/current/en/programs/ab.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

</details>
