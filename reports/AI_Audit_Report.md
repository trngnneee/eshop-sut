# AI Audit Report - HW05 Performance Testing

Tôi sử dụng công cụ AI để hỗ trợ các công việc trong quá trình thực hiện HW05 Performance Testing.

## Nhật ký tương tác

<!-- AUDIT_ENTRY:interaction-001-load-design:START -->
### [1] Load Test - Thiết kế kịch bản kiểm thử

- **Công cụ:** Codex (GPT-5)
- **Thời gian:** 2026-08-15 23:14
- **Prompt:**
  > [$hw05-performance-testing](E:\Testing_23CLC\HW5\eshop-sut\.codex\skills\hw05-performance-testing\SKILL.md)
  > Start the Load Test for my selected E2E workflow:
  >
  > Buy-then-history
  > Login -> browse product list -> view product detail -> add to cart -> checkout -> read My Orders to verify the newly created order.
  >
  > My student ID is 23127158. Proceed to phase 2
- **Output:**
  AI đã đề xuất thiết kế Load Test cho workflow `Buy-then-history` với mô hình closed-model trên JMeter. Profile ban đầu gồm 10 concurrent users, ramp-up 60 giây, giữ tải 300 giây và shutdown 30 giây. Workflow bao phủ nhóm endpoint auth-heavy, read-heavy và transactional thông qua các bước `POST /api/login`, đọc danh sách sản phẩm, xem chi tiết sản phẩm, thêm vào giỏ hàng, checkout và đọc My Orders. AI cũng đề xuất sử dụng các file CSV `data/load_auth_users.csv`, `data/product_inputs.csv`, `data/checkout_inputs.csv`, correlation cho JWT `${token}` và `${orderId}`, cùng các assertion HTTP/JSON cần thiết.
- **Kết quả sau review:** Người dùng cung cấp StudentID `23127158`, cho phép chuyển sang bước sinh test plan, và thiết kế Load Test được giữ làm cơ sở cho interaction tiếp theo. Sau review bổ sung về test data, file credential của Load được tách thành `data/load_auth_users.csv` với 10 tài khoản riêng phù hợp 10 VU.
<!-- AUDIT_ENTRY:interaction-001-load-design:END -->

<!-- AUDIT_ENTRY:interaction-002-load-generation:START -->
### [2] Load Test - Sinh JMeter test plan

- **Công cụ:** Codex (GPT-5)
- **Thời gian:** 2026-08-15 23:20
- **Prompt:**
  > My student ID is 23127158. Proceed to phase 2
- **Output:**
  AI đã sinh JMeter test plan `test-plans/23127158_Load_20260815.jmx` và các file dữ liệu CSV gồm `data/load_auth_users.csv`, `data/product_inputs.csv`, `data/checkout_inputs.csv`. Test plan giữ workflow `Buy-then-history`, backend target `http://localhost:3000`, correlation JWT và checkout orderId, 12 response assertions, Summary Report listener và output path `results/load/23127158_Load_20260815.jtl`. Sau human review, AI đã sửa test plan từ standard Thread Group sang `Ultimate Thread Group` với 10 users, ramp-up 60 giây, giữ tải 300 giây và shutdown 30 giây. XML được validate lại, plugin `jmeter-plugins-casutg-3.1.1.jar` được xác nhận tồn tại, endpoint sequence, CSV, correlation, assertions và listener được giữ nguyên.
- **Kết quả sau review:** Human review ban đầu yêu cầu thay standard Thread Group bằng `Ultimate Thread Group` để profile tải phản ánh đúng thiết kế. Sau khi test plan được sửa, người dùng đã thực thi test và cho phép chuyển sang phân tích kết quả Load Test. Sau review bổ sung về dữ liệu đăng nhập, Load plan được cập nhật để dùng `data/load_auth_users.csv` thay cho file auth dùng chung.
<!-- AUDIT_ENTRY:interaction-002-load-generation:END -->

<!-- AUDIT_ENTRY:interaction-003-load-analysis:START -->
### [3] Load Test - Phân tích kết quả

- **Công cụ:** Codex (GPT-5)
- **Thời gian:** 2026-08-15 23:48
- **Prompt:**
  > I have already excuted the test plan. Now your mission is doing the phase 4.
- **Output:**
  AI đã phân tích lại `results/load/result.jtl` bằng script `.codex/skills/hw05-performance-testing/scripts/analyze_jtl.py` sau khi Load Test được chạy lại. Kết quả mới có 1.709 samples, 0 failures, error rate 0,0%, toàn bộ response code là HTTP 200, duration 381,346 giây, request throughput 4,481 req/s và khoảng 282 complete workflows. Overall latency có avg 3,002 ms, p95 8 ms, p99 10 ms và max 164 ms. Checkout là bước chậm nhất trong workflow với avg 7,594 ms, p95 10 ms, p99 11 ms và max 164 ms; đây là tail-latency outlier chứ chưa phải suy giảm kéo dài vì p95/p99 vẫn thấp và không có lỗi. HTML report `reports/html/load/` đã tồn tại, nhưng workspace vẫn chưa có resource-monitor screenshot nên chưa thể kết luận về CPU/memory/disk hoặc hardware saturation. AI cũng cập nhật threshold theo số liệu mới và lọc lại optimization để chỉ giữ các đề xuất cải thiện hệ thống/backend: parameterize product-search SQL, cân nhắc pagination/LIMIT và composite index cho My Orders nếu test nặng hơn chứng minh latency tăng, cân nhắc SQLite WAL/busy timeout nếu có lock contention, và kiểm tra Checkout write path nếu outlier 164 ms lặp lại.
- **Kết quả sau review:** Đã cập nhật lại theo kết quả Load Test mới nhất. Các số liệu cũ của lần phân tích Load trước được supersede bởi run `results/load/result.jtl` lúc 2026-08-16 03:04:57 đến 03:11:18 +07:00. Human review phát hiện AI đã trộn lẫn system optimization với test-process/evidence notes như giữ baseline, dùng CSV user riêng và capture resource-monitor evidence; các mục đó không còn được xem là recommendation cải thiện hệ thống. Human review cũng chỉnh cách diễn giải max latency 164 ms: đây chỉ là một Checkout tail-latency outlier vì p95/p99 vẫn thấp và error rate bằng 0, không được overclaim thành sustained degradation. Sau review bổ sung, phần báo cáo Load và review AI đã được viết lại bằng tiếng Việt theo dạng nội dung có thể đưa vào main report, bỏ section bằng chứng/file-location trong workspace và chỉ giữ bối cảnh kiểm thử, metric từ raw JTL, threshold, system-only recommendations, misinterpretation hunt và kết luận human review.
<!-- AUDIT_ENTRY:interaction-003-load-analysis:END -->

<!-- AUDIT_ENTRY:interaction-004-stress-design:START -->
### [4] Stress Test - Thiết kế kịch bản kiểm thử

- **Công cụ:** Codex (GPT-5)
- **Thời gian:** 2026-08-16 00:19
- **Prompt:**
  > Approved Load Phase 4. Start Stress Phase 1.
- **Output:**
  AI đã thiết kế Stress Test cho cùng workflow `Buy-then-history`, tiếp tục sử dụng JMeter và `Ultimate Thread Group`. Thiết kế ban đầu đề xuất profile tăng tải theo các mức 10, 20, 35 và 50 users, think time 500-1500 ms, giữ nguyên request sequence, CSV, JWT correlation, `${orderId}` correlation và assertions như Load Test. AI đề xuất dùng Aggregate Report để khác với Summary Report của Load Test. Thiết kế cũng nêu rõ các tiêu chí quan sát Stress như p95, error rate, throughput, resource usage và yêu cầu evidence thật ở bước chạy test.
- **Kết quả sau review:** Người dùng chấp nhận thiết kế Stress Test và yêu cầu sinh JMeter test plan. Thiết kế được dùng làm cơ sở cho interaction Stress Test plan generation.
<!-- AUDIT_ENTRY:interaction-004-stress-design:END -->

<!-- AUDIT_ENTRY:interaction-005-stress-generation:START -->
### [5] Stress Test - Sinh và chỉnh sửa JMeter test plan

- **Công cụ:** Codex (GPT-5)
- **Thời gian:** 2026-08-16 00:24
- **Prompt:**
  > I accept phase 1. Now you can proceed to phase 2 and generate test plan
- **Output:**
  AI đã sinh Stress JMeter test plan `test-plans/23127158_Stress_20260816.jmx`, reuse các CSV `data/stress_auth_users.csv`, `data/product_inputs.csv`, `data/checkout_inputs.csv`, giữ workflow `Buy-then-history`, correlation JWT `${token}`, checkout `${orderId}`, 12 assertions, think time 500-1500 ms, Aggregate Report listener và output path `results/stress/23127158_Stress_20260816.jtl`. Test plan ban đầu dùng `Ultimate Thread Group` với các mức 10, 20, 35 và 50 users nhưng các row được cấu hình như target độc lập, dẫn đến workload có thể giảm gần về 0 giữa các stress level. Sau khi người dùng reopen interaction, AI chỉ sửa schedule của `Ultimate Thread Group` sang các incremental overlapping thread rows: 10 threads delay 0 startup 30 hold 675 shutdown 30; 10 threads delay 150 startup 30 hold 525 shutdown 30; 15 threads delay 300 startup 45 hold 360 shutdown 30; 15 threads delay 465 startup 60 hold 180 shutdown 30. XML được validate lại, xác nhận có 1 Ultimate Thread Group, 0 standard ThreadGroup, request sequence, CSV, correlation, assertions, think time, listener và JTL output path không đổi.
- **Kết quả sau review:** Người dùng đã chạy test plan Stress đã sửa, nên bản continuous stepped profile 10 -> 20 -> 35 -> 50 users được xem là đã chấp nhận với corrections. Có thể chuyển sang phân tích kết quả Stress mới.

<!-- AUDIT_ENTRY:interaction-005-stress-generation:END -->

<!-- AUDIT_ENTRY:interaction-006-stress-analysis:START -->
### [6] Stress Test - Phân tích kết quả

- **Công cụ:** Codex (GPT-5)
- **Thời gian:** 2026-08-16 00:44
- **Prompt:**
  > Read the file at results/stress/result.jtl and proceed to phase 4
- **Output:**
  AI đã phân tích `results/stress/result.jtl` bằng script `.codex/skills/hw05-performance-testing/scripts/analyze_jtl.py`. Kết quả lần chạy cũ có 20.531 samples, 0 failures, error rate 0,0%, toàn bộ response code là HTTP 200, duration 780,832 giây, request throughput 26,294 req/s và khoảng 3.375 complete workflows. Overall latency có avg 4,948 ms, p95 15 ms, p99 31 ms và max 82 ms. My Orders là sampler chậm nhất với avg 12,260 ms, p95 31 ms và p99 38 ms. AI đã đề xuất threshold cho Stress p95, error rate, workflow throughput và request throughput; đồng thời đề xuất optimization như index cho order-history read, pagination/LIMIT cho `/api/orders/my-orders`, bổ sung HTML Report/resource-monitor screenshot, dùng test accounts tách biệt hơn, và chỉ cân nhắc SQLite WAL/busy timeout nếu các lần test sau có lock error hoặc checkout tail latency tăng.
  Cập nhật sau review:
  AI đã phân tích lại `results/stress/result.jtl` của run mới lúc 2026-08-16 04:26:09 đến 04:38:20 +07:00. Kết quả mới có 21.830 samples, 0 failures, error rate 0,0%, toàn bộ response code HTTP 200, duration 730,957 giây, request throughput 29,865 req/s và khoảng 3.618 complete workflows. Overall latency có avg 2,792 ms, p95 7 ms, p99 9 ms và max 188 ms. Theo từng sampler, Checkout có avg cao nhất 6,025 ms, p95 9 ms, p99 11 ms, max 188 ms; My Orders p95 chỉ 5 ms nên không còn là sampler chậm nhất như run cũ. Theo stress level, throughput tăng từ khoảng 9,173 req/s ở 10 users lên 48,008 req/s ở 50 users, p95 vẫn trong khoảng 6-8 ms và không có lỗi. Báo cáo Stress Phase 4 đã được viết lại bằng tiếng Việt, chỉ giữ recommendation cải thiện hệ thống/backend và phân loại các đề xuất như giữ implementation hiện tại, pagination My Orders dài hạn, composite index khi dữ liệu lớn hơn, theo dõi outlier, và SQLite WAL/busy timeout nếu test nặng hơn có lock contention.
  Cập nhật sau review:
  Sau human review, báo cáo Stress Phase 4 đã được chỉnh để dùng overall 95th percentile = 6,0 ms theo JMeter HTML dashboard, ghi rõ khác biệt với custom analyzer 7,0 ms, và bổ sung bảng human review ngay trong report. Bảng optimization được lọc lại để chỉ còn các cải thiện SUT/backend: pagination/LIMIT cho My Orders khi dữ liệu tăng, composite index cho order-history read nếu My Orders latency tăng ở Spike/Endurance hoặc dữ liệu lớn hơn, và SQLite WAL/busy timeout nếu có bằng chứng lock contention. Các nội dung như giữ implementation hiện tại và theo dõi outlier được chuyển thành nhận xét, không còn là recommendation cải thiện hệ thống. File review riêng `reports/Stress_AI_Analysis_Human_Review.md` được tạo để đưa vào main report.
- **Kết quả sau review:** Human review dựa trên file `reports/Stress_AI_Analysis_Human_Review.md` đã chấp nhận phần lớn diễn giải của AI: Stress Test mới ổn định đến 50 users, 21.830 samples, 0 failures, 0,0% error rate và chưa tìm thấy breakpoint rõ ràng. Review đã sửa cách trình bày percentile tổng: JMeter HTML dashboard ghi overall 95th pct = 6,0 ms, còn custom analyzer ra 7,0 ms do khác cách tính/làm tròn; main report dùng số JMeter HTML để nhất quán evidence. Review cũng loại các mục không phải system optimization như giữ implementation hiện tại hoặc theo dõi outlier khỏi bảng recommendation. Recommendation cuối cùng chỉ giữ pagination/LIMIT cho My Orders như Feasible / accepted nhưng chưa chứng minh bottleneck hiện tại, composite index `orders(user_id, id DESC)` là Plausible but not proven, và SQLite WAL/busy timeout là Plausible but not proven nếu test nặng hơn có lock contention.

<!-- AUDIT_ENTRY:interaction-006-stress-analysis:END -->

<!-- AUDIT_ENTRY:interaction-007-spike-design:START -->
### [7] Spike Test - Thiết kế kịch bản kiểm thử

- **Công cụ:** Codex (GPT-5)
- **Thời gian:** 2026-08-16 05:11
- **Prompt:**
  > [$hw05-performance-testing](E:\Testing_23CLC\HW5\eshop-sut\.codex\skills\hw05-performance-testing\SKILL.md) 
  >
  > Start the Spike Test for my selected E2E workflow:  
  >
  > Buy-then-history
  > Login → browse product list → view product detail → add to cart → checkout → read My Orders to verify the newly created order.
- **Output:**
  AI đã bắt đầu Spike Test Phase 1 cho workflow E2E `Buy-then-history`, giữ cùng request sequence đã dùng ở Load và Stress: `POST /api/login`, `GET /api/products`, `GET /api/products/:id`, `POST /api/cart`, `POST /api/checkout`, và `GET /api/orders/my-orders`. Thiết kế đề xuất dùng JMeter với `Ultimate Thread Group`, workload spike gồm baseline ngắn, tăng đột ngột từ 10 users lên 75 users, giữ spike ngắn để quan sát khả năng hấp thụ tải, sau đó giảm về baseline để quan sát phục hồi. Test vẫn data-driven bằng CSV riêng cho auth của Spike cùng các CSV product và checkout hiện có; tiếp tục correlation JWT `${token}` và checkout `${orderId}`, assertion HTTP/JSON cho từng bước, think time ngắn hơn Stress để tạo cú sốc tải rõ ràng. Listener/view được đề xuất là `View Results Tree - Spike` để khác với Summary Report của Load và Aggregate Report của Stress. File dự kiến sau khi được duyệt là `test-plans/23127158_Spike_20260816.jmx`, JTL dự kiến `results/spike/23127158_Spike_20260816.jtl`, HTML report dự kiến `reports/html/spike/`. Chưa sinh file `.jmx`; đang chờ human review/approval của thiết kế Spike trước khi chuyển sang phase sinh test plan.
  Cập nhật sau review:
  Thiết kế Spike Phase 1 được điều chỉnh tăng tải: baseline giữ ở 20 users để có nền ổn định, sau đó spike đột ngột lên 150 users trong 30 giây, giữ mức spike 120 giây, rồi giảm về 20 users trong 60 giây và giữ thêm 120 giây để quan sát phục hồi. Think time vẫn ngắn, khoảng 250-750 ms, nhằm tạo cú sốc tải rõ hơn so với Stress Test. Thiết kế cần CSV auth riêng cho Spike với ít nhất 150 tài khoản hợp lệ để tránh contention hoặc lockout do dùng chung user; workflow, endpoint sequence, JWT/orderId correlation, assertions và listener `View Results Tree - Spike` được giữ nguyên. Thiết kế sửa đổi vẫn đang chờ human review, chưa sinh `.jmx` và chưa chạy test.
  Cập nhật sau review:
  Thiết kế Spike Phase 1 được điều chỉnh lần hai thành workload lớn hơn để tìm breakpoint: baseline 50 users, spike ramp rất nhanh từ 50 lên 1000 users trong 60 giây, giữ peak 1000 users trong 120 giây, sau đó giảm về 50 users trong 120 giây và giữ baseline phục hồi 180 giây. Think time đề xuất 250-750 ms để vẫn tạo áp lực lớn nhưng tránh vòng lặp request hoàn toàn không thực tế. Vì peak 1000 users có thể vượt khả năng máy local/JMeter/SUT, test plan cần ghi rõ đây là aggressive spike/breakpoint attempt; khi chạy cần quan sát CPU, memory, event-loop/SQLite contention, error rate, p95/p99 và khả năng phục hồi sau spike. CSV auth riêng cho Spike cần ít nhất 1000 tài khoản hợp lệ hoặc một chiến lược đăng nhập hợp lệ không gây lockout/credential contention. Workflow, endpoint sequence, JWT/orderId correlation, assertions và listener `View Results Tree - Spike` vẫn giữ nguyên. Thiết kế sửa đổi vẫn đang chờ human review, chưa sinh `.jmx` và chưa chạy test.
- **Kết quả sau review:** Thiết kế Spike Phase 1 đã được approve với profile baseline 50 users, spike lên 1000 users, giữ peak 120 giây, giảm về baseline và quan sát phục hồi. Được phép chuyển sang interaction Spike Test plan generation.

<!-- AUDIT_ENTRY:interaction-007-spike-design:END -->

<!-- AUDIT_ENTRY:interaction-008-spike-generation:START -->
### [8] Spike Test - Sinh JMeter test plan

- **Công cụ:** Codex (GPT-5)
- **Thời gian:** 2026-08-16 05:30
- **Prompt:**
  > <No separate initial prompt; started after prior approval/review.>
- **Output:**
  AI đã sinh Spike JMeter test plan `test-plans/23127158_Spike_20260816.jmx` cho StudentID `23127158`, giữ nguyên workflow `Buy-then-history` đã dùng trong Load và Stress: login, browse product list, view product detail, add to cart, checkout, và read My Orders để verify order mới. Test plan dùng `Ultimate Thread Group` với hai dòng schedule: baseline 50 users startup 30 giây, giữ xuyên suốt test; thêm 950 users sau 210 giây, ramp 60 giây để đạt peak 1000 users, giữ peak 120 giây, shutdown nhóm spike trong 120 giây, sau đó quan sát recovery baseline 180 giây và shutdown 60 giây. AI cũng sinh `data/spike_auth_users.csv` gồm 1000 user credentials `spike_user_0001` đến `spike_user_1000`, và cập nhật `backend/database.js` để seed 1000 Spike users khi database được khởi tạo lại. Listener/view của Spike là `View Results Tree - Spike`, khác với Summary Report của Load và Aggregate Report của Stress; JTL path được cấu hình là `results/spike/23127158_Spike_20260816.jtl`. Validation đã xác nhận XML hợp lệ bằng `xmllint`, `backend/database.js` pass `node --check`, JMX có 1 Ultimate Thread Group, 0 standard ThreadGroup, 6 HTTP samplers đúng thứ tự, 3 CSV datasets, 2 JSON extractors, 12 response assertions, JWT/orderId correlation và đúng output path. Chưa chạy test; đang chờ human review test plan.
- **Kết quả sau review:** Đang chờ người dùng review Spike Phase 2 test plan. Chưa chạy Spike Test và chưa tạo `.jtl` thực thi.
<!-- AUDIT_ENTRY:interaction-008-spike-generation:END -->

## Tổng hợp công cụ sử dụng

| Công cụ | Mục đích sử dụng | Số lượt tương tác |
|---|---|---:|
| Codex (GPT-5) | Thiết kế Load Test, Stress Test và Spike Test, sinh JMeter test plan, chỉnh sửa Ultimate Thread Group theo human review, phân tích JTL, đề xuất threshold/optimization, phân loại evidence và cập nhật AI Audit Report | 8 |
