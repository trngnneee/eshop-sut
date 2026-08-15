# Review phân tích AI cho Stress Test

## 1. Mục đích

Phần này dùng cho Task 2 của HW05: review lại phân tích Stress Test do AI tạo ra, đối chiếu với raw JTL và JMeter HTML dashboard, xác định chỗ AI diễn giải chưa hợp lý, và phân loại các recommendation theo mức độ có cơ sở.

## 2. Giá trị đúng sau khi đối chiếu

| Metric | Giá trị đúng | Ghi chú review |
|---|---:|---|
| Tổng số samples | 21.830 | Khớp giữa raw JTL và JMeter HTML dashboard |
| Failures | 0 | Khớp |
| Error rate | 0,0% | Khớp |
| Response code | HTTP 200: 21.830 | Khớp |
| Duration | 730,957 giây | Tính từ timestamp đầu-cuối trong raw JTL |
| Throughput tổng | 29,865 req/s | Khớp với JMeter HTML dashboard |
| Complete workflows xấp xỉ | 3.618 | Dựa trên số sampler cuối `06 My Orders Verify New Order` |
| Overall avg latency | 2,792 ms | Khớp |
| Overall 95th percentile | 6,0 ms theo JMeter HTML; 7,0 ms theo custom analyzer | Khác biệt do cách tính/làm tròn percentile; kết luận hiệu năng không đổi |
| Overall 99th percentile | 9,0 ms | Khớp |
| Overall max latency | 188,0 ms | Khớp |
| Sampler có avg latency cao nhất | Checkout, 6,025 ms | Checkout chậm nhất theo trung bình |
| My Orders p95 | 5,0 ms | Không còn là sampler chậm nhất trong run mới |

## 3. Review các diễn giải của AI

| AI claim / recommendation | Giá trị đúng hoặc diễn giải đúng | Human decision | Lý do |
|---|---|---|---|
| AI kết luận Stress Test mới chưa tìm thấy breakpoint hiệu năng rõ ràng. | Run có 21.830 samples, 0 failures, 0,0% error rate, toàn bộ HTTP 200; throughput tăng đến khoảng 48,008 req/s ở cửa sổ 50 users. | Correct | Không có dấu hiệu lỗi chức năng, error spike hoặc p95/p99 tăng kéo dài khi tải tăng. |
| AI ghi overall p95 = 7,0 ms như một giá trị duy nhất. | JMeter HTML dashboard ghi overall 95th pct = 6,0 ms; custom analyzer tính ra 7,0 ms. | Corrected | Đây là khác biệt do phương pháp tính percentile. Khi đưa vào main report cùng HTML dashboard, nên dùng số 6,0 ms hoặc ghi rõ nguồn tính. |
| AI cho rằng throughput tăng theo stress level. | Cửa sổ 10 users khoảng 9,173 req/s; 20 users khoảng 19,153 req/s; 35 users khoảng 33,030 req/s; 50 users khoảng 48,008 req/s. | Correct | Số liệu theo cửa sổ thời gian từ raw JTL ủng hộ nhận xét này. |
| AI diễn giải max latency 188,0 ms là outlier cần theo dõi, không phải bottleneck kéo dài. | Checkout max 188,0 ms, Product List max 179,0 ms, My Orders max 174,0 ms, Login max 129,0 ms; nhưng p95/p99 thấp và không có lỗi. | Correct | Max latency đơn lẻ không đủ để kết luận hệ thống suy giảm kéo dài. |
| AI đưa "giữ implementation hiện tại" vào bảng optimization. | Đây là kết luận sau kiểm thử, không phải recommendation cải thiện hệ thống. | Corrected | Bảng recommendation cuối cùng chỉ nên giữ các cải thiện SUT/backend. |
| AI đưa "theo dõi outlier" vào bảng optimization. | Đây là ghi chú phân tích tiếp theo, không phải thay đổi cải thiện hệ thống. | Corrected | Nội dung này nên nằm trong nhận xét/human review, không nằm trong bảng optimization. |
| AI giữ pagination hoặc `LIMIT` cho My Orders như cải thiện dài hạn. | My Orders p95 hiện chỉ 5,0 ms, nhưng endpoint trả toàn bộ order history của user. | Feasible / accepted | Đề xuất hợp lý về thiết kế hệ thống khi dữ liệu orders tăng, nhưng chưa được Stress run hiện tại chứng minh là bottleneck. |
| AI đề xuất composite index `orders(user_id, id DESC)` theo điều kiện. | Query My Orders filter theo `user_id` và sort theo `id DESC`; p95 hiện chỉ 5,0 ms. | Plausible but not proven | Có cơ sở từ query shape, nhưng chưa đủ bằng chứng để xem là tối ưu bắt buộc từ run này. |
| AI đề xuất SQLite WAL / busy timeout theo điều kiện. | Run hiện tại không có failure và không có dấu hiệu SQLite lock. | Plausible but not proven | Chỉ nên áp dụng nếu Spike/Endurance cho thấy lock contention hoặc tail latency lặp lại. |

## 4. Recommendation cuối cùng sau human review

| Recommendation | Phân loại | Cơ sở đánh giá | Kết luận |
|---|---|---|---|
| Thêm pagination hoặc `LIMIT` cho `/api/orders/my-orders` khi dữ liệu orders tăng. | Feasible / accepted | Endpoint trả toàn bộ order history; My Orders p95 hiện chỉ 5,0 ms | Giữ như cải thiện hệ thống dài hạn, không claim là bottleneck hiện tại. |
| Cân nhắc composite index `orders(user_id, id DESC)` nếu My Orders latency tăng ở test nặng hơn. | Plausible but not proven | Query filter theo `user_id` và sort theo `id DESC`; chưa có latency cao ở run này | Chỉ nên triển khai sau khi Spike/Endurance hoặc dữ liệu lớn hơn cho thấy My Orders chậm. |
| Cân nhắc SQLite WAL mode và busy timeout nếu xuất hiện lock contention. | Plausible but not proven | Stress run có 0 failures và không có SQLite lock error | Chưa cần áp dụng từ run này; giữ làm hướng xử lý nếu tải cao hơn làm phát sinh lock/wait. |

## 5. Kết luận human review

Sau khi đối chiếu raw JTL, JMeter HTML dashboard và yêu cầu HW05, phần lớn phân tích AI là hợp lý: Stress Test mới ổn định đến 50 users, không có lỗi, throughput tăng theo tải, và chưa tìm thấy breakpoint hiệu năng rõ ràng. Điểm cần chỉnh chính là cách trình bày percentile tổng: nên dùng overall 95th pct = 6,0 ms từ JMeter HTML dashboard, hoặc ghi rõ custom analyzer cho ra 7,0 ms do khác phương pháp tính.
