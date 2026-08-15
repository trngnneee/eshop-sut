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
- **Kết quả sau review:** Đã chỉnh sửa, hiện đang chờ review lại. Test plan ban đầu đã được thực thi và tạo `results/stress/result.jtl`, nhưng sau đó interaction bị reopen vì workload schedule không phù hợp: tải giảm gần về 0 giữa các stress level. Người dùng yêu cầu chuyển sang continuous stepped profile 10 -> 20 -> 35 -> 50 users bằng các incremental overlapping thread rows. AI đã sửa lại schedule và validate XML; đồng thời tách credential Stress sang `data/stress_auth_users.csv` với 50 tài khoản riêng phù hợp mức peak 50 VU. Test plan mới chưa được chấp nhận để chạy lại.
<!-- AUDIT_ENTRY:interaction-005-stress-generation:END -->

<!-- AUDIT_ENTRY:interaction-006-stress-analysis:START -->
### [6] Stress Test - Phân tích kết quả lần chạy cũ

- **Công cụ:** Codex (GPT-5)
- **Thời gian:** 2026-08-16 00:44
- **Prompt:**
  > Read the file at results/stress/result.jtl and proceed to phase 4
- **Output:**
  AI đã phân tích `results/stress/result.jtl` bằng script `.codex/skills/hw05-performance-testing/scripts/analyze_jtl.py`. Kết quả lần chạy cũ có 20.531 samples, 0 failures, error rate 0,0%, toàn bộ response code là HTTP 200, duration 780,832 giây, request throughput 26,294 req/s và khoảng 3.375 complete workflows. Overall latency có avg 4,948 ms, p95 15 ms, p99 31 ms và max 82 ms. My Orders là sampler chậm nhất với avg 12,260 ms, p95 31 ms và p99 38 ms. AI đã đề xuất threshold cho Stress p95, error rate, workflow throughput và request throughput; đồng thời đề xuất optimization như index cho order-history read, pagination/LIMIT cho `/api/orders/my-orders`, bổ sung HTML Report/resource-monitor screenshot, dùng test accounts tách biệt hơn, và chỉ cân nhắc SQLite WAL/busy timeout nếu các lần test sau có lock error hoặc checkout tail latency tăng.
- **Kết quả sau review:** Bị từ chối / không còn hiệu lực. Phân tích này sử dụng kết quả từ Stress test plan có workload schedule sau đó được xác định là không phù hợp. Nội dung được giữ lại để phục vụ audit history nhưng không được dùng làm kết quả Stress cuối cùng. Active gate quay lại Interaction [5], nơi Stress Test plan đang chờ review lại sau khi sửa continuous stepped profile.
<!-- AUDIT_ENTRY:interaction-006-stress-analysis:END -->

## Tổng hợp công cụ sử dụng

| Công cụ | Mục đích sử dụng | Số lượt tương tác |
|---|---|---:|
| Codex (GPT-5) | Thiết kế Load Test và Stress Test, sinh JMeter test plan, chỉnh sửa Ultimate Thread Group theo human review, phân tích JTL, đề xuất threshold/optimization, phân loại evidence và cập nhật AI Audit Report | 6 |
