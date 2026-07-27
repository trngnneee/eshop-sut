> **Trạng thái bằng chứng:** chỉ **[DOC]**, **[DOC + ASSUMPTION]**, **[ASSUMPTION]** và kế hoạch chưa chạy; ngày chốt 2026-07-14.

### 1. Tổng quan

Tsung là framework load test distributed/multi-protocol, repository chính thức thuộc ProcessOne; tài liệu ghi tác giả ban đầu Nicolas Niclausse. Source `develop` khai báo 1.8.0, trong khi hosted manual mang nhãn 1.7.0, nên phải pin tag/DTD và ghi version skew. [Repository](https://github.com/processone/tsung), [`vsn.mk`](https://github.com/processone/tsung/blob/develop/vsn.mk), [manual](https://tsung.readthedocs.io/en/latest/) (truy cập 2026-07-14). **[DOC]**

### 2. Cost và licence

Source mở GPL v2, không cần tài khoản/trial. [Introduction](https://tsung.readthedocs.io/en/latest/introduction.html), [COPYING](https://github.com/processone/tsung/blob/develop/COPYING) (truy cập 2026-07-14). **[DOC]**

### 3. Installation và platform support

Manual nêu Linux/FreeBSD/Solaris và MacPorts, về nguyên tắc trên hệ Erlang hỗ trợ. Dependency gồm Erlang/OTP, build tools; report có thể cần gnuplot, Perl/Template Toolkit hoặc Python/matplotlib. Build `./configure; make; make install`; distributed cần host resolution/Erlang nodes và passwordless SSH. Các minimum-version trong manual 1.7.0 không được tự coi là recommendation năm 2026. [Installation](https://tsung.readthedocs.io/en/latest/installation.html) (truy cập 2026-07-14). **[DOC]**

### 4. Scripting hoặc configuration model

XML/DTD định nghĩa clients, servers, load, sessions, request/transaction/think time; CSV data và config dễ version-control/modularize ở mức file. Local có `use_controller_vm='true'`; cấu hình nâng cao dùng dynvars/loops/conditions. [Client/server](https://tsung.readthedocs.io/en/latest/conf-client-server.html), [Sessions](https://tsung.readthedocs.io/en/latest/conf-sessions.html), [Advanced](https://tsung.readthedocs.io/en/latest/conf-advanced-features.html) (truy cập 2026-07-14). **[DOC]**

### 5. Workload capabilities

Nhiều arrival phases có duration, interarrival/arrival rate/max users; weighted/probabilistic sessions, think time và distributed client hosts/maxusers/weights. Automatic cookies, CSV sequential/random, regex/XPath/limited JSONPath extraction, substitution, random/unique data, loop/if/foreach hỗ trợ session/correlation thật. [Load](https://tsung.readthedocs.io/en/latest/conf-load.html), [Features](https://tsung.readthedocs.io/en/latest/features.html), [Advanced](https://tsung.readthedocs.io/en/latest/conf-advanced-features.html) (truy cập 2026-07-14). **[DOC]**

README hiện hành liệt kê HTTP, WebDAV, SOAP, PostgreSQL, MySQL, LDAP, MQTT, AMQP và Jabber/XMPP. Manual 1.7.0 mô tả thêm WebSocket RFC6455, AMQP 0.9.1, MQTT v3.1 là experimental; phải xác minh tag 1.8.0 trước khi claim production support. [README](https://github.com/processone/tsung), [Features](https://tsung.readthedocs.io/en/latest/features.html) (truy cập 2026-07-14). **[DOC]**

### 6. Assertions và validation

`match` kiểm tra response và có action continue/log/abort session/abort test/restart/loop/dump cùng counters match/nomatch. Đây là content/business validation mạnh; aggregate SLA p95/error-budget vẫn cần policy ngoài. [Response checks](https://tsung.readthedocs.io/en/latest/conf-advanced-features.html#checking-the-server-s-response) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 7. Metrics và reporting

Statistics log hoặc JSON backend theo dõi request/page/connect/session/users/status/traffic; live web dashboard và `tsung_stats.pl` tạo HTML/graphs. Engine chuẩn tính mean/stdev theo interval thay vì mặc định giữ mọi sample, nên raw per-request/p50/p95/p99 phải xác minh theo backend/fullstats của đúng version. [Reports](https://tsung.readthedocs.io/en/latest/reports.html) (truy cập 2026-07-14). **[DOC]**

### 8. CI/CD và automation

CLI `tsung -f config.xml start`, XML/data Git-friendly và local/offline; CI phải pin DTD/version, quản lý node/SUT lifecycle, collect log/report và áp SLA gate. `abort_test` theo match không thay aggregate performance gate. Repository không trình bày first-party container image như kênh phát hành cốt lõi. [Installation/Running](https://tsung.readthedocs.io/en/latest/installation.html#running), [Reports](https://tsung.readthedocs.io/en/latest/reports.html), [Repository](https://github.com/processone/tsung) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 9. EShop suitability

HTTP cookies, dynamic data, correlation, transactions, think time và match có thể biểu diễn login→product→cart→checkout tốt nếu endpoint contract được xác minh. Local single-node phù hợp hơn cluster cho smoke EShop nhỏ. [Features](https://tsung.readthedocs.io/en/latest/features.html), [Advanced](https://tsung.readthedocs.io/en/latest/conf-advanced-features.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 10. AI-assisted potential

AI có thể scaffold XML/CSV/extractor/match/phases và phân tích report; phải audit DTD/version, XML escaping, regex/JSONPath giới hạn, secret, correlation, arrival semantics và Failure Modes. Config AI chưa smoke không được coi là đúng. [Advanced](https://tsung.readthedocs.io/en/latest/conf-advanced-features.html), [Load](https://tsung.readthedocs.io/en/latest/conf-load.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 11. Classroom suitability

Năng lực minh họa cao nhưng Erlang/XML/DTD/report/distributed concepts khó vừa 25 phút nếu chưa chuẩn bị lab. Single-node prebuilt có thể demo offline; tự cài cluster trong lớp là over-scope. [Installation](https://tsung.readthedocs.io/en/latest/installation.html), [Client/server](https://tsung.readthedocs.io/en/latest/conf-client-server.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 12. Điểm mạnh trong phạm vi seminar

Session/correlation/assertion, workload phases/mix, protocol breadth, scale-out thật và HTML/dashboard. [Features](https://tsung.readthedocs.io/en/latest/features.html), [Load](https://tsung.readthedocs.io/en/latest/conf-load.html), [Reports](https://tsung.readthedocs.io/en/latest/reports.html) (truy cập 2026-07-14). **[DOC]**

### 13. Hạn chế trong phạm vi seminar

Learning/setup cao; hosted docs lệch source version; raw percentile/gate cần xác minh thêm. Distributed chỉ cần khi một generator bão hòa CPU/memory/network/socket hoặc mục tiêu yêu cầu scale/geography; với local EShop nó thêm SSH, Erlang naming/cookies, clock/network và biến nhiễu. [Client/server](https://tsung.readthedocs.io/en/latest/conf-client-server.html), [Installation](https://tsung.readthedocs.io/en/latest/installation.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

### 14. Smoke Test Plan

**[KẾ HOẠCH – CHƯA THỰC NGHIỆM]**

- **Mục tiêu:** single-node đọc XML, gửi một GET và sinh log/report; không bật cluster.
- **Prerequisites:** `[VERIFIED_HOST]`, `[VERIFIED_PORT]`, `[VERIFIED_PRODUCT_PATH]`, protocol/TLS và pinned tag/DTD/dependencies. **[ASSUMPTION]**
- **Installation/setup:** theo [Installation](https://tsung.readthedocs.io/en/latest/installation.html) (truy cập 2026-07-14); lưu Tsung/Erlang versions, source commit và dependency versions.
- **Một request:** GET path đã xác minh. Base skeleton cố ý chưa có body `match`; chỉ thêm match đã review sau khi pin binary/DTD và stable marker.
- **Config/command:** validate skeleton dưới bằng DTD của binary; chạy `tsung -f smoke.xml -l ./tsung-logs start`, rồi `tsung_stats.pl` trong `[GENERATED_LOG_DIR]`. [Client/server](https://tsung.readthedocs.io/en/latest/conf-client-server.html), [Load](https://tsung.readthedocs.io/en/latest/conf-load.html), [Reports](https://tsung.readthedocs.io/en/latest/reports.html) (truy cập 2026-07-14).

```xml
<?xml version='1.0'?>
<!DOCTYPE tsung SYSTEM '/path/to/pinned/tsung-1.0.dtd'>
<tsung loglevel='notice' version='1.0'>
 <clients><client host='localhost' use_controller_vm='true'/></clients>
 <servers><server host='[VERIFIED_HOST]' port='[VERIFIED_PORT]' type='tcp'/></servers>
 <load><arrivalphase phase='1' duration='10' unit='second'><users interarrival='1' unit='second'/></arrivalphase></load>
 <sessions><session name='smoke' probability='100' type='ts_http'><request><http url='[VERIFIED_PRODUCT_PATH]' method='GET' version='1.1'/></request></session></sessions>
</tsung>
```

- **Expected result:** XML/DTD hợp lệ, local node start/stop sạch, request/transport đúng contract, log/report sinh được; base smoke chưa claim body check.
- **Evidence:** XML/DTD/hash, Tsung/Erlang/source versions, command, stdout/stderr/exit, log/JSON/HTML, EShop commit, time/timezone, resources, redaction.
- **Possible errors:** DTD mismatch; Erlang hostname/node/cookie; port/TLS; report dependency; placeholder; match/escaping; clock; vô tình remote client/SSH; secret trong log.
- **Success criteria:** single-node hoàn tất, request/transport đúng, artifacts đủ; chỉ claim match khi XML thật có match, pinned validation và negative control. Chưa bật distributed/SLA gate.

### 15. Điểm đánh giá

| Tiêu chí | Trọng số | Điểm | Evidence |
|---|---:|---:|---|
| Cost & access | 8% | 5 | GPLv2/source mở. **[DOC]** |
| Learning curve | 8% | 2 | XML/Erlang/distributed/report. **[DOC + ASSUMPTION]** |
| EShop fit | 15% | 5 | Session/correlation/check. **[DOC]** |
| Multi-step journey | 12% | 5 | Transactions/dynvars/loops. **[DOC]** |
| Workload control | 10% | 5 | Phases/rates/session mix/clients. **[DOC]** |
| Assertions/checks | 8% | 4 | `match` mạnh; SLA ngoài. **[DOC + ASSUMPTION]** |
| Reporting | 8% | 4 | Stats/JSON/live/HTML; raw cần xác minh. **[DOC]** |
| CI/CD | 7% | 3 | CLI/XML tốt, lifecycle/gate phức tạp. **[DOC + ASSUMPTION]** |
| Reproducibility | 7% | 4 | XML pin được; version/node/randomness. **[DOC + ASSUMPTION]** |
| Local/offline | 5% | 4 | Single-node được; dependencies nặng. **[DOC]** |
| AI-assisted potential | 7% | 3 | Scaffold tốt, audit DTD/correlation. **[DOC + ASSUMPTION]** |
| Classroom suitability | 5% | 2 | Khó trong timebox ngắn. **[DOC + ASSUMPTION]** |
| Community | 0% | 3 | Repo/manual/issues có, nhưng docs skew; không ảnh hưởng tổng. [Repository](https://github.com/processone/tsung), [manual](https://tsung.readthedocs.io/en/latest/) (truy cập 2026-07-14). **[DOC]** |

**Tổng có trọng số: 81.0/100**; Community 0% không tham gia công thức.

### 16. Kết luận sơ bộ

**Survey-only** cho seminar EShop local/timebox hiện tại; cân nhắc shortlist trong dự án dài ngày cần journey + distributed scale.

### 17. Câu hỏi phản biện

<details>
<summary>Phản biện và trả lời</summary>

1. **Điểm cao nhất sao chỉ Survey-only?** Điểm đo năng lực; XML/Erlang/version skew và distributed operations làm risk/timebox không phù hợp demo ngắn. [Installation](https://tsung.readthedocs.io/en/latest/installation.html), [manual](https://tsung.readthedocs.io/en/latest/) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
2. **Khi nào distributed thực sự cần?** Khi generator đơn không đạt load/bão hòa tài nguyên hoặc nghiên cứu scale/geography; smoke local có controller VM. [Client/server](https://tsung.readthedocs.io/en/latest/conf-client-server.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**
3. **Vì sao không gắn tiền tố của ASF?** Repo/docs thuộc dự án Tsung/ProcessOne, không có bằng chứng liên hệ ASF; tên đúng là **Tsung**. [Repository](https://github.com/processone/tsung), [Introduction](https://tsung.readthedocs.io/en/latest/introduction.html) (truy cập 2026-07-14). **[DOC]**
4. **XML làm giảm tái lập?** Không tự thân; XML/data pin tốt. Rủi ro là DTD/version, randomness, node/network và dependency chưa khóa. [`vsn.mk`](https://github.com/processone/tsung/blob/develop/vsn.mk), [Configuration](https://tsung.readthedocs.io/en/latest/configuration.html) (truy cập 2026-07-14). **[DOC + ASSUMPTION]**

</details>
