# Báo cáo kết quả Load Test

## 1. Mục tiêu và phạm vi kiểm thử

Load Test được thực hiện cho workflow end-to-end `Buy-then-history` của hệ thống EShop:

`Login -> browse product list -> view product detail -> add to cart -> checkout -> read My Orders`

Workflow này bao phủ ba nhóm endpoint backend được yêu cầu trong HW05:

| Nhóm endpoint | API được kiểm thử trong workflow |
|---|---|
| Auth-heavy | `POST /api/login` |
| Read-heavy | `GET /api/products?search=...`, `GET /api/products/:id`, `GET /api/orders/my-orders` |
| Transactional | `POST /api/cart`, `POST /api/checkout` |

Mục tiêu của Load Test là kiểm tra hệ thống dưới mức tải ổn định 10 người dùng đồng thời, dùng làm baseline trước khi thực hiện Stress/Spike/Endurance.

## 2. Cấu hình kiểm thử

| Thành phần | Giá trị |
|---|---|
| Student ID | `23127158` |
| Backend base URL | `http://localhost:3000` |
| Thread model | Ultimate Thread Group |
| Số người dùng đồng thời | 10 users |
| Ramp-up | 60 giây |
| Hold load | 300 giây |
| Shutdown | 30 giây |
| Think time | Uniform Random Timer 1000-3000 ms |
| Dữ liệu đăng nhập | 10 tài khoản riêng cho 10 VU |
| Dữ liệu sản phẩm | Search term, product ID, product name, price, quantity |
| Dữ liệu checkout | Shipping address và total amount |
| Listener/report view | Summary Report |

Bộ dữ liệu đăng nhập chứa 10 tài khoản riêng cho 10 VU, tránh việc toàn bộ thread dùng chung một user. Điều này giúp giảm nhiễu do shared cart/order history trong các lần chạy lại.

Thời gian chạy được suy ra từ timestamp trong JTL: từ `2026-08-16 03:04:57 +07:00` đến `2026-08-16 03:11:18 +07:00`.

## 3. Kết quả tổng quan từ raw JTL

Các số liệu dưới đây được tính từ raw JTL của lần chạy Load Test.

| Metric | Giá trị | Nguồn |
|---|---:|---|
| Tổng số samples | 1.709 | raw JTL |
| Failures | 0 | cột `success` |
| Error rate | 0,0% | `failures / samples` |
| Response code | HTTP 200: 1.709 | cột `responseCode` |
| Duration | 381,346 giây | timestamp đầu-cuối |
| Request throughput | 4,481 req/s | `samples / duration` |
| Complete workflows xấp xỉ | 282 | số sampler cuối `06 My Orders Verify New Order` |
| Workflow throughput xấp xỉ | 0,739 workflows/s, 44,37 workflows/phút | `282 / 381,346 s` |
| Avg latency | 3,002 ms | cột `elapsed` |
| p95 latency | 8,0 ms | cột `elapsed` |
| p99 latency | 10,0 ms | cột `elapsed` |
| Max latency | 164,0 ms | cột `elapsed` |

## 4. Kết quả theo từng sampler

| Sampler / endpoint | Samples | Error % | Avg ms | p95 ms | p99 ms | Max ms | Throughput req/s |
|---|---:|---:|---:|---:|---:|---:|---:|
| 01 Login / `POST /api/login` | 288 | 0,0 | 3,097 | 4,0 | 8,13 | 25,0 | 0,778 |
| 02 Browse Product List / `GET /api/products?search=...` | 288 | 0,0 | 1,587 | 2,0 | 3,0 | 3,0 | 0,778 |
| 03 View Product Detail / `GET /api/products/:id` | 285 | 0,0 | 1,540 | 2,0 | 3,0 | 4,0 | 0,770 |
| 04 Add To Cart / `POST /api/cart` | 283 | 0,0 | 1,972 | 3,0 | 3,18 | 4,0 | 0,761 |
| 05 Checkout / `POST /api/checkout` | 283 | 0,0 | 7,594 | 10,0 | 11,0 | 164,0 | 0,760 |
| 06 My Orders Verify New Order / `GET /api/orders/my-orders` | 282 | 0,0 | 2,255 | 3,0 | 4,0 | 7,0 | 0,757 |

## 5. Nhận xét kết quả

Load Test chạy thành công ở mức 10 concurrent users. Tất cả 1.709 samples đều trả về HTTP 200, không có failure và error rate là 0,0%. Điều này cho thấy workflow `Buy-then-history` hoạt động ổn định trong điều kiện tải cơ bản của môi trường local.

Latency tổng thể thấp: p95 là 8,0 ms và p99 là 10,0 ms. Đây là kết quả tốt cho Load baseline. Request throughput đạt 4,481 req/s, tương ứng khoảng 282 workflow hoàn chỉnh trong 381,346 giây, hay khoảng 44,37 workflow/phút.

Checkout là bước chậm nhất trong workflow với avg 7,594 ms, p95 10,0 ms và p99 11,0 ms. Điều này hợp lý vì checkout là bước ghi dữ liệu vào bảng `orders`, trong khi product list/detail và My Orders chủ yếu là thao tác đọc. Có một outlier tại Checkout với max latency 164,0 ms. Tuy nhiên p95/p99 vẫn thấp và không có lỗi, nên không đủ bằng chứng để kết luận hệ thống bị suy giảm hiệu năng kéo dài. Outlier này nên được theo dõi lại ở Stress/Spike/Endurance.

Số lượng sampler không hoàn toàn bằng nhau: 288 login nhưng chỉ có 282 bước My Orders hoàn tất. Vì vậy, khi báo cáo số workflow hoàn chỉnh, giá trị an toàn là 282 chứ không phải 288. Nguyên nhân có khả năng là một số iteration bị dừng ở giai đoạn ramp-down của Ultimate Thread Group, nhưng raw JTL không đủ thông tin để kết luận chắc chắn.

Báo cáo này chỉ kết luận dựa trên số liệu response-time, throughput, error rate và response code trong raw JTL. Do không phân tích trực tiếp số liệu CPU, RAM hoặc disk I/O trong phần này, báo cáo không đưa ra kết luận về giới hạn phần cứng.

## 6. Ngưỡng hiệu năng đề xuất

| Ngưỡng | Giá trị đề xuất | Lý do | Metric dùng làm cơ sở |
|---|---:|---|---|
| Overall p95 warning | > 50 ms | Cao hơn baseline p95 8,0 ms hơn 6 lần, đủ nhạy để phát hiện regression nhưng vẫn chừa khoảng dao động local. | Overall p95 = 8,0 ms |
| Overall p95 fail | > 100 ms | Cao hơn baseline hơn 12 lần; nếu vượt mức này trong cùng profile thì cần xem là lỗi hiệu năng trừ khi có lý do môi trường rõ ràng. | Overall p95 = 8,0 ms |
| Checkout p95 warning | > 75 ms | Checkout là bước business-critical và chậm nhất, nhưng p95 hiện chỉ 10,0 ms. | Checkout p95 = 10,0 ms |
| Error-rate warning | > 0,5% | Baseline hiện tại không có lỗi; lỗi lặp lại với credential hợp lệ cần được điều tra. | Error rate = 0,0% |
| Error-rate fail | >= 1,0% | Mức lỗi 1% trong Load Test local là dấu hiệu không ổn định. | Error rate = 0,0% |
| Request throughput floor | < 4,0 req/s | Baseline đạt 4,481 req/s; thấp hơn 4,0 req/s trong cùng profile có thể là regression. | Throughput = 4,481 req/s |
| Complete workflow throughput floor | < 0,65 workflows/s | Baseline đạt 0,739 workflows/s; ngưỡng này giúp phát hiện giảm throughput đáng kể. | Workflow throughput = 0,739 workflows/s |

## 7. Đề xuất cải thiện hệ thống

Các recommendation dưới đây chỉ tập trung vào cải thiện SUT/backend. Những việc như chuẩn bị bằng chứng thực thi hoặc điều chỉnh dữ liệu kiểm thử không được tính là system optimization.

| Recommendation | Phân loại | Metric / quan sát dùng làm cơ sở | Tác động kỳ vọng |
|---|---|---|---|
| Thêm pagination hoặc `LIMIT` cho `/api/orders/my-orders` khi dữ liệu orders tăng. | Được chấp nhận / có lý nhưng chưa được Load run chứng minh | My Orders p95 là 3,0 ms và max 7,0 ms trong Load, nhưng endpoint hiện trả toàn bộ orders của user theo `id DESC` | Tránh payload order history tăng không giới hạn khi số đơn hàng lớn. |
| Cân nhắc composite index `orders(user_id, id DESC)` nếu test nặng hơn cho thấy My Orders latency tăng. | Có lý nhưng chưa được chứng minh | Query My Orders filter theo `user_id` và sort theo `id DESC`; Load hiện chưa chứng minh bottleneck vì p95 chỉ 3,0 ms | Có thể giảm chi phí lookup/sort khi bảng `orders` lớn hơn. |
| Cân nhắc bật SQLite WAL mode và cấu hình busy timeout nếu Stress/Spike/Endurance xuất hiện lock wait, checkout failure hoặc checkout tail latency lặp lại. | Có lý nhưng chưa được chứng minh | Load có 0 failures; Checkout có avg 7,594 ms, p95 10,0 ms, p99 11,0 ms và một max outlier 164,0 ms | Có thể cải thiện concurrent read/write trong SQLite dưới tải cao hơn. |
| Kiểm tra backend logic của Checkout nếu outlier 164,0 ms lặp lại ở các lần chạy sau. | Có lý nhưng chưa được chứng minh | Một sample Checkout đạt 164,0 ms trong khi p95/p99 vẫn thấp | Giúp phân biệt local noise, SQLite write contention hoặc logic backend cần tối ưu. |

## 8. Human review đối với phân tích AI

Theo yêu cầu Task 2 của HW05, phần phân tích do AI tạo ra phải được review lại và chỉ ra những chỗ AI đọc sai, diễn giải sai hoặc đề xuất chưa phù hợp.

| AI claim / recommendation | Giá trị đúng hoặc diễn giải đúng | Human decision | Lý do |
|---|---|---|---|
| Max latency 164,0 ms có thể bị diễn giải quá mức thành vấn đề hiệu năng nghiêm trọng. | Overall p95 = 8,0 ms, p99 = 10,0 ms; Checkout p95 = 10,0 ms, p99 = 11,0 ms; chỉ có một max outlier 164,0 ms. | Corrected | Một outlier cần theo dõi nhưng không chứng minh sustained degradation. |
| Đề xuất B-tree index cho `products(name)` với query `LIKE '%term%'`. | Product List p95 chỉ 2,0 ms; query có leading wildcard nên không thể giả định B-tree index sẽ giúp. | Hallucinated / rejected | Không giữ đề xuất này nếu chưa đổi query pattern hoặc chưa có query plan chứng minh. |
| Đề xuất pagination hoặc `LIMIT` cho My Orders. | My Orders p95 hiện chỉ 3,0 ms và max 7,0 ms, nhưng endpoint trả toàn bộ order history của user. | Feasible / accepted | Human review chấp nhận đây là cải thiện hệ thống hợp lý để tránh payload tăng không giới hạn; tuy nhiên không xem đây là bottleneck đã được Load run chứng minh. |
| Đề xuất index cho My Orders. | My Orders p95 hiện chỉ 3,0 ms và max 7,0 ms. | Plausible but not proven | Có thể hữu ích khi dữ liệu orders lớn hơn, nhưng Load run hiện tại chưa chứng minh bottleneck. |
| Đề xuất SQLite WAL / busy timeout. | Load run có 0 failures và không có lock error; Checkout có một outlier 164,0 ms. | Plausible but not proven | Chỉ nên áp dụng nếu test nặng hơn cho thấy lock contention hoặc tail latency lặp lại. |

## 9. Kết luận Load Test

Load Test với 10 concurrent users đạt kết quả ổn định: 0 failures, 0,0% error rate, p95 8,0 ms và throughput 4,481 req/s. Checkout là sampler chậm nhất và có một outlier 164,0 ms, nhưng chưa có bằng chứng về suy giảm kéo dài vì p95/p99 vẫn thấp.
