# Báo cáo kết quả Stress Test

## 1. Mục tiêu và phạm vi kiểm thử

Stress Test được thực hiện cho cùng workflow end-to-end `Buy-then-history` đã dùng ở Load Test:

`Login -> browse product list -> view product detail -> add to cart -> checkout -> read My Orders`

Workflow này bao phủ đủ ba nhóm endpoint backend trong HW05:

| Nhóm endpoint | API được kiểm thử trong workflow |
|---|---|
| Auth-heavy | `POST /api/login` |
| Read-heavy | `GET /api/products?search=...`, `GET /api/products/:id`, `GET /api/orders/my-orders` |
| Transactional | `POST /api/cart`, `POST /api/checkout` |

Mục tiêu của Stress Test là tăng dần số người dùng đồng thời từ 10 lên 20, 35 và 50 users để quan sát hệ thống có xuất hiện lỗi, tăng latency kéo dài, hoặc dấu hiệu breakpoint trong môi trường local hay không.

## 2. Cấu hình kiểm thử

| Thành phần | Giá trị |
|---|---|
| Student ID | `23127158` |
| Backend base URL | `http://localhost:3000` |
| Thread model | Ultimate Thread Group |
| Stress profile | Continuous stepped profile 10 -> 20 -> 35 -> 50 users |
| Think time | Uniform Random Timer 500-1500 ms |
| Dữ liệu đăng nhập | 50 tài khoản riêng cho mức peak 50 VU |
| Dữ liệu sản phẩm | Search term, product ID, product name, price, quantity |
| Dữ liệu checkout | Shipping address và total amount |
| Listener/report view | Aggregate Report |

Lần chạy này sử dụng test plan Stress đã được sửa sau human review. Điểm sửa quan trọng là các row của Ultimate Thread Group được cấu hình theo dạng tăng thêm và chồng lấn, để tải đi theo profile liên tục `10 -> 20 -> 35 -> 50` thay vì rơi gần về 0 giữa các mức.

Thời gian chạy được suy ra từ timestamp trong JTL: từ `2026-08-16 04:26:09 +07:00` đến `2026-08-16 04:38:20 +07:00`.

## 3. Kết quả tổng quan từ raw JTL

Các số liệu dưới đây được tính trực tiếp từ raw JTL của lần chạy Stress Test mới.

| Metric | Giá trị | Nguồn |
|---|---:|---|
| Tổng số samples | 21.830 | raw JTL |
| Failures | 0 | cột `success` |
| Error rate | 0,0% | `failures / samples` |
| Response code | HTTP 200: 21.830 | cột `responseCode` |
| Duration | 730,957 giây | timestamp đầu-cuối |
| Request throughput | 29,865 req/s | `samples / duration` |
| Complete workflows xấp xỉ | 3.618 | số sampler cuối `06 My Orders Verify New Order` |
| Workflow throughput xấp xỉ | 4,950 workflows/s, 297,0 workflows/phút | `3618 / 730,957 s` |
| Avg latency | 2,792 ms | cột `elapsed` |
| p95 latency | 6,0 ms | JMeter HTML dashboard, tính từ raw JTL |
| p99 latency | 9,0 ms | cột `elapsed` |
| Max latency | 188,0 ms | cột `elapsed` |

## 4. Kết quả theo từng sampler

| Sampler / endpoint | Samples | Error % | Avg ms | p95 ms | p99 ms | Max ms | Throughput req/s |
|---|---:|---:|---:|---:|---:|---:|---:|
| 01 Login / `POST /api/login` | 3.660 | 0,0 | 3,023 | 5,0 | 9,0 | 129,0 | 5,013 |
| 02 Browse Product List / `GET /api/products?search=...` | 3.652 | 0,0 | 1,656 | 3,0 | 6,0 | 179,0 | 5,000 |
| 03 View Product Detail / `GET /api/products/:id` | 3.643 | 0,0 | 1,564 | 3,0 | 7,0 | 49,0 | 4,994 |
| 04 Add To Cart / `POST /api/cart` | 3.632 | 0,0 | 1,623 | 2,0 | 3,0 | 6,0 | 4,988 |
| 05 Checkout / `POST /api/checkout` | 3.625 | 0,0 | 6,025 | 9,0 | 11,0 | 188,0 | 4,991 |
| 06 My Orders Verify New Order / `GET /api/orders/my-orders` | 3.618 | 0,0 | 2,878 | 5,0 | 8,0 | 174,0 | 4,985 |

Checkout là sampler chậm nhất theo latency trung bình, với avg 6,025 ms, p95 9,0 ms và p99 11,0 ms. My Orders không còn là sampler chậm nhất như lần chạy Stress cũ; p95 của My Orders trong run mới chỉ 5,0 ms.

## 5. Kết quả theo stress level

| Cửa sổ tải | Samples | Failures | Avg ms | p95 ms | p99 ms | Max ms | Throughput xấp xỉ |
|---|---:|---:|---:|---:|---:|---:|---:|
| 10 users | 1.376 | 0 | 2,776 | 8,0 | 9,0 | 26,0 | 9,173 req/s |
| 20 users | 2.873 | 0 | 2,783 | 8,0 | 9,0 | 28,0 | 19,153 req/s |
| 35 users | 5.450 | 0 | 2,394 | 6,0 | 8,0 | 19,0 | 33,030 req/s |
| 50 users | 11.522 | 0 | 2,982 | 7,0 | 10,0 | 188,0 | 48,008 req/s |
| Shutdown | 609 | 0 | 2,833 | 7,0 | 9,0 | 11,0 | 20,300 req/s |

Theo từng level, hệ thống không xuất hiện lỗi khi tải tăng đến 50 users. Throughput tăng rõ theo từng mức tải, từ khoảng 9,173 req/s ở cửa sổ 10 users lên khoảng 48,008 req/s ở cửa sổ 50 users. p95 vẫn nằm trong khoảng 6,0-8,0 ms, nên chưa có dấu hiệu latency tăng kéo dài theo bậc tải.

## 6. Nhận xét kết quả

Stress Test mới chạy thành công về mặt chức năng: toàn bộ 21.830 samples đều thành công, error rate bằng 0,0% và tất cả response code là HTTP 200. Kết quả này cho thấy workflow `Buy-then-history` vẫn ổn định trong profile tăng tải liên tục đến 50 users trên môi trường local.

Điểm đáng chú ý nhất là throughput tăng theo tải trong khi p95 tổng vẫn thấp. Theo JMeter HTML dashboard, overall 95th percentile là 6,0 ms và 99th percentile là 9,0 ms, không vượt ngưỡng degradation đã dự kiến cho Stress. Vì vậy, lần chạy này chưa tìm thấy breakpoint hiệu năng rõ ràng của hệ thống.

Có một số max outlier riêng lẻ: Checkout max 188,0 ms, Product List max 179,0 ms, My Orders max 174,0 ms và Login max 129,0 ms. Tuy nhiên p95/p99 của các sampler này vẫn thấp và không có failure, nên không nên diễn giải các max outlier này thành bottleneck kéo dài. Chúng nên được theo dõi lại ở Spike hoặc Endurance để xem có lặp lại không.

So với lần Stress cũ đã bị invalidated, run mới đáng tin cậy hơn vì profile Ultimate Thread Group đã được sửa thành dạng stepped liên tục và dữ liệu đăng nhập Stress có đủ tài khoản cho mức peak 50 VU.

## 7. Ngưỡng hiệu năng đề xuất

| Ngưỡng | Giá trị đề xuất | Lý do | Metric dùng làm cơ sở |
|---|---:|---|---|
| Stress overall p95 warning | > 25 ms | Baseline Stress mới có 95th percentile 6,0 ms theo JMeter HTML dashboard; 25 ms đủ rộng cho dao động local nhưng vẫn bắt được regression đáng kể. | Overall 95th pct = 6,0 ms |
| Stress overall p95 fail / breakpoint | > 100 ms | Nếu p95 vượt 100 ms trong cùng profile 50 users thì có thể xem là dấu hiệu suy giảm rõ ràng so với run hiện tại. | Overall 95th pct = 6,0 ms |
| Checkout p95 warning | > 50 ms | Checkout là bước ghi dữ liệu và có max outlier 188,0 ms, nhưng p95 hiện chỉ 9,0 ms. | Checkout p95 = 9,0 ms |
| My Orders p95 warning | > 40 ms | My Orders hiện p95 chỉ 5,0 ms; ngưỡng này giúp phát hiện order-history read bắt đầu tăng khi dữ liệu orders lớn hơn. | My Orders p95 = 5,0 ms |
| Error-rate warning | > 0,5% | Run hiện tại không có lỗi; lỗi lặp lại với credential hợp lệ cần được điều tra. | Error rate = 0,0% |
| Error-rate fail | >= 1,0% | Mức lỗi 1% trong Stress Test cho thấy workflow không còn ổn định dưới profile đang kiểm thử. | Error rate = 0,0% |
| Request throughput floor | < 25 req/s | Run hiện tại đạt 29,865 req/s; thấp hơn 25 req/s trong cùng profile có thể là regression. | Throughput = 29,865 req/s |
| Complete workflow throughput floor | < 4,2 workflows/s | Run hiện tại đạt khoảng 4,950 workflows/s; ngưỡng 4,2 workflows/s giúp phát hiện giảm throughput đáng kể. | Workflow throughput = 4,950 workflows/s |

## 8. Đề xuất cải thiện hệ thống

Các recommendation dưới đây chỉ tập trung vào SUT/backend. Những việc như chuẩn bị thêm screenshot, đổi CSV hoặc sinh lại HTML report không được tính là system optimization.

| Recommendation | Phân loại | Metric / quan sát dùng làm cơ sở | Tác động kỳ vọng |
|---|---|---|---|
| Thêm pagination hoặc `LIMIT` cho `/api/orders/my-orders` khi dữ liệu orders tăng. | Feasible / accepted, but not proven by this run | My Orders p95 hiện chỉ 5,0 ms, nhưng endpoint trả toàn bộ order history của user theo `id DESC` | Giới hạn payload và chi phí đọc khi lịch sử đơn hàng của user tăng dài hạn. |
| Cân nhắc composite index `orders(user_id, id DESC)` nếu My Orders p95 tăng ở Spike/Endurance hoặc khi seed orders lớn hơn. | Plausible but not proven | Query My Orders filter theo `user_id` và sort theo `id DESC`; run hiện tại chưa chứng minh bottleneck vì p95 chỉ 5,0 ms | Có thể giảm chi phí lookup/sort khi bảng `orders` lớn hơn. |
| Chỉ bật SQLite WAL mode hoặc busy timeout nếu test nặng hơn xuất hiện lock wait, checkout failure hoặc tail latency lặp lại. | Plausible but not proven | Stress run có 0 failures và không có response/message thể hiện SQLite lock | Có thể cải thiện concurrent read/write dưới tải cao hơn, nhưng run hiện tại chưa chứng minh nhu cầu này. |

Các mục như "giữ implementation hiện tại" hoặc "theo dõi outlier" được xem là kết luận/ghi chú kiểm thử, không phải recommendation cải thiện hệ thống nên không đưa vào bảng optimization.

## 9. Human review đối với phân tích AI

| AI claim / recommendation | Giá trị đúng hoặc diễn giải đúng | Human decision | Lý do |
|---|---|---|---|
| AI ghi overall p95 là 7,0 ms mà chưa nói rõ khác biệt với JMeter HTML dashboard. | JMeter HTML dashboard ghi overall 95th pct = 6,0 ms; custom analyzer tính từ raw JTL theo cách nội suy/làm tròn khác nên ra 7,0 ms. | Corrected | Hai giá trị đều rất thấp và không đổi kết luận, nhưng main report nên dùng số JMeter dashboard khi trình bày cùng HTML report để tránh lệch evidence. |
| AI kết luận Stress Test mới chưa tìm thấy breakpoint. | 21.830 samples, 0 failures, 0,0% error rate, toàn bộ HTTP 200; throughput đạt 29,865 req/s và peak 50 users đạt khoảng 48,008 req/s. | Correct | Không có lỗi chức năng hoặc latency p95/p99 tăng kéo dài theo stress level. |
| AI diễn giải các max outlier 129-188 ms là điểm cần theo dõi, không phải bottleneck kéo dài. | Checkout max 188,0 ms, Product List max 179,0 ms, My Orders max 174,0 ms, Login max 129,0 ms; nhưng p95/p99 vẫn thấp và error rate bằng 0,0%. | Correct | Max đơn lẻ không đủ để kết luận sustained degradation nếu percentile cao và lỗi đều ổn. |
| AI đưa "giữ implementation hiện tại" vào bảng optimization. | Đây là kết luận vận hành sau test, không phải một recommendation cải thiện hệ thống. | Corrected | Theo yêu cầu review trước đó, recommendation nên tập trung vào cải thiện SUT/backend. |
| AI đưa "theo dõi outlier" vào bảng optimization. | Theo dõi outlier là ghi chú kiểm thử/phân tích tiếp, không phải thay đổi cải thiện hệ thống. | Corrected | Nội dung này được chuyển thành nhận xét, không giữ trong bảng optimization. |
| AI giữ pagination hoặc `LIMIT` cho My Orders như cải thiện dài hạn. | My Orders p95 hiện chỉ 5,0 ms, nhưng endpoint trả toàn bộ order history của user theo `id DESC`. | Feasible / accepted | Đề xuất hợp lý về thiết kế hệ thống khi dữ liệu orders tăng, nhưng không được trình bày như bottleneck đã được Stress run chứng minh. |
| AI đề xuất composite index cho My Orders nếu dữ liệu lớn hơn hoặc test nặng hơn cho thấy latency tăng. | Query filter theo `user_id` và sort theo `id DESC`, nhưng p95 hiện chỉ 5,0 ms. | Plausible but not proven | Có cơ sở từ query shape, nhưng chưa có bằng chứng raw JTL đủ mạnh để tối ưu ngay. |
| AI đề xuất SQLite WAL / busy timeout theo điều kiện. | Run hiện tại có 0 failures và không có dấu hiệu SQLite lock trong response. | Plausible but not proven | Chỉ nên áp dụng nếu Spike/Endurance xuất hiện lock contention hoặc checkout tail latency lặp lại. |

Sau human review, kết luận cuối cùng là Stress Test mới ổn định đến 50 users trong môi trường local, chưa đạt breakpoint hiệu năng rõ ràng. Các recommendation được giữ lại chỉ gồm các cải thiện hệ thống có thể áp dụng theo điều kiện: pagination/LIMIT cho My Orders khi dữ liệu tăng, composite index cho order-history read nếu latency tăng ở test nặng hơn, và SQLite WAL/busy timeout nếu có bằng chứng lock contention.

Trạng thái: Đã human review và chỉnh lại diễn giải.
