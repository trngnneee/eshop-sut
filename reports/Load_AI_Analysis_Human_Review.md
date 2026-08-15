# Review phân tích AI cho Load Test

## 1. Mục đích

Phần này dùng cho Task 2 của HW05: review lại phần AI phân tích kết quả Load Test, chỉ ra các chỗ AI diễn giải sai hoặc dễ gây hiểu nhầm, trích giá trị đúng từ raw JTL, và đánh giá recommendation nào khả thi, chưa đủ bằng chứng hoặc bị loại bỏ.

## 2. Giá trị đúng từ raw JTL

| Metric | Giá trị đúng | Nguồn |
|---|---:|---|
| Tổng số samples | 1.709 | raw JTL |
| Failures | 0 | cột `success` |
| Error rate | 0,0% | `failures / samples` |
| Response code | HTTP 200: 1.709 | cột `responseCode` |
| Duration | 381,346 giây | timestamp đầu-cuối |
| Request throughput | 4,481 req/s | analyzer output |
| Complete workflows xấp xỉ | 282 | số sampler cuối `06 My Orders Verify New Order` |
| Workflow throughput xấp xỉ | 0,739 workflows/s | `282 / 381,346 s` |
| Overall avg latency | 3,002 ms | cột `elapsed` |
| Overall p95 latency | 8,0 ms | cột `elapsed` |
| Overall p99 latency | 10,0 ms | cột `elapsed` |
| Overall max latency | 164,0 ms | cột `elapsed` |
| Sampler chậm nhất theo avg | Checkout, 7,594 ms | per-sampler metrics |
| Checkout p95 / p99 / max | 10,0 ms / 11,0 ms / 164,0 ms | per-sampler metrics |

## 3. Các chỗ AI diễn giải sai hoặc dễ gây hiểu nhầm

| AI claim / recommendation | Giá trị đúng hoặc diễn giải đúng | Human decision | Lý do |
|---|---|---|---|
| AI đưa các mục như giữ baseline, tiếp tục dùng CSV user riêng và capture resource-monitor evidence vào nhóm optimization. | Đây là các ghi chú về baseline, test data và evidence, không phải cải thiện hệ thống/backend. | Corrected | HW05 yêu cầu đánh giá recommendation cải thiện hệ thống, ví dụ database index, connection handling, SQLite WAL hoặc backend query. |
| AI có thể làm người đọc hiểu max latency 164,0 ms là suy giảm hiệu năng nghiêm trọng. | Overall p95 = 8,0 ms, p99 = 10,0 ms; Checkout p95 = 10,0 ms, p99 = 11,0 ms; chỉ có một max outlier 164,0 ms. | Corrected | Một outlier cần theo dõi, nhưng không chứng minh sustained degradation hoặc bottleneck kéo dài. |
| AI nhắc việc tách dữ liệu đăng nhập như một cải thiện repeatability dựa trên kết quả test. | Việc đổi dữ liệu đăng nhập là thật, nhưng được xác minh từ cấu hình test plan và CSV, không phải từ raw JTL. | Corrected | Raw JTL không lưu request body hay username, nên không thể dùng JTL để chứng minh trực tiếp user nào đã đăng nhập. |
| AI đặt HTML report và resource-monitor evidence gần phần optimization. | Đây là thông tin về mức độ đầy đủ của evidence, không phải cải thiện hệ thống. | Corrected | Evidence completeness phải được ghi ở phần phụ lục/bằng chứng của bài nộp, không phải recommendation cải thiện hệ thống trong nội dung phân tích. |
| AI từng nhắc B-tree index cho `products(name)` như một hướng tối ưu product search. | Product List p95 chỉ 2,0 ms; query hiện dùng `LIKE '%term%'` nên không thể giả định B-tree index sẽ giúp. | Hallucinated / rejected | Không giữ đề xuất này nếu chưa đổi query pattern hoặc chưa có query plan chứng minh benefit. |
| AI đề xuất pagination hoặc `LIMIT` cho `/api/orders/my-orders`. | My Orders p95 hiện chỉ 3,0 ms và max 7,0 ms, nên Load run chưa chứng minh bottleneck hiện tại. | Feasible / accepted | Human review chấp nhận đề xuất này như một cải thiện hệ thống hợp lý vì endpoint trả toàn bộ order history của user; tuy nhiên cần trình bày là phòng ngừa khi dữ liệu tăng, không phải lỗi hiệu năng đã được Load Test chứng minh. |
| AI đề xuất index cho My Orders. | My Orders p95 hiện chỉ 3,0 ms và max 7,0 ms. | Plausible but not proven | Có thể hữu ích khi bảng `orders` lớn hơn, nhưng Load run hiện tại chưa chứng minh bottleneck. |
| AI đề xuất SQLite WAL / busy timeout. | Load run có 0 failures và không có SQLite lock error; Checkout có một outlier 164,0 ms. | Plausible but not proven | Chỉ nên áp dụng nếu Stress/Spike/Endurance cho thấy lock contention hoặc checkout tail latency lặp lại. |
| AI đề xuất parameterize product search SQL. | Product List p95 chỉ 2,0 ms, nên đây không phải performance bottleneck từ JTL. Backend source nối trực tiếp search term vào SQL. | Feasible, but not a proven performance fix | Đề xuất này đúng về security/correctness, nhưng không nên trình bày như cải thiện hiệu năng đã được Load Test chứng minh. |

## 4. Recommendation cuối cùng sau human review

| Recommendation | Phân loại | Cơ sở đánh giá | Kết luận |
|---|---|---|---|
| Parameterize SQL của endpoint product search. | Feasible | Backend source nối trực tiếp `search` vào SQL; Product List p95 = 2,0 ms | Nên làm vì security/correctness, không claim là performance improvement đã được chứng minh. |
| Thêm pagination hoặc `LIMIT` cho `/api/orders/my-orders` khi dữ liệu orders tăng. | Feasible / accepted | My Orders p95 = 3,0 ms, max = 7,0 ms trong Load; endpoint hiện trả toàn bộ order history của user | Được chấp nhận như cải thiện hệ thống hợp lý để tránh payload tăng không giới hạn; không trình bày như bottleneck đã được Load run chứng minh. |
| Thêm composite index `orders(user_id, id DESC)` nếu My Orders chậm ở test nặng hơn. | Plausible but not proven | Query My Orders filter theo `user_id` và sort theo `id DESC` | Có khả năng hữu ích khi bảng `orders` lớn, nhưng chưa được Load run chứng minh. |
| Bật SQLite WAL mode và busy timeout nếu có lock contention. | Plausible but not proven | Load có 0 failures; Checkout có một max outlier 164,0 ms | Chỉ áp dụng nếu Stress/Spike/Endurance xuất hiện lock wait, checkout failure hoặc tail latency lặp lại. |
| Điều tra Checkout write path nếu outlier 164,0 ms lặp lại. | Plausible but not proven | Checkout avg = 7,594 ms, p95 = 10,0 ms, p99 = 11,0 ms, max = 164,0 ms | Theo dõi thêm trước khi tối ưu để tránh kết luận quá mức từ một sample. |

## 5. Kết luận human review

Sau khi đối chiếu với raw JTL, các metric chính của AI là đúng: Load Test có 1.709 samples, 0 failures, error rate 0,0%, p95 8,0 ms và throughput 4,481 req/s. Sai sót chính của AI không nằm ở việc đọc số liệu tổng quan, mà nằm ở cách phân loại và diễn giải: AI trộn các việc cải thiện quy trình test/evidence vào mục optimization, và có nguy cơ diễn giải quá mức max latency 164,0 ms.

Kết luận đã chỉnh là: Load Test ổn định ở 10 concurrent users; Checkout là bước chậm nhất và có một outlier cần theo dõi, nhưng chưa đủ bằng chứng về bottleneck kéo dài. Human review chấp nhận pagination hoặc `LIMIT` cho My Orders như một cải thiện hệ thống hợp lý khi dữ liệu orders tăng, đồng thời vẫn ghi rõ rằng Load run hiện tại chưa chứng minh đây là bottleneck. Các recommendation cuối cùng phải tập trung vào SUT/backend, đồng thời ghi rõ recommendation nào đã được chứng minh, recommendation nào chỉ là plausible/feasible và recommendation nào bị loại bỏ.
