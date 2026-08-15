# Review AI cho Task 1 - Thiết kế và sinh test plan

## 1. Mục đích

Phần này dùng cho Task 1 của HW05, ghi lại những điểm AI đã hiểu sai, bỏ sót hoặc tạo chưa phù hợp trong quá trình thiết kế và sinh test plan. Nội dung được viết dựa trên human review sau khi kiểm tra lại thiết kế, cấu hình JMeter, dữ liệu đăng nhập và cách chạy thực tế.

## 2. Các điểm AI đã sai hoặc bỏ sót

| Giai đoạn | AI đã sai hoặc bỏ sót | Human review | Cách sửa cuối cùng | Nguyên nhân có thể |
|---|---|---|---|---|
| Load Test - sinh test plan | AI ban đầu dùng standard Thread Group, trong khi thiết kế Load đã chọn Ultimate Thread Group để mô tả rõ ramp-up, hold load và shutdown. | Không phù hợp với cấu hình đã thống nhất vì standard Thread Group không thể hiện profile tải đầy đủ như yêu cầu thiết kế. | Chuyển Load plan sang Ultimate Thread Group với 10 users, ramp-up 60 giây, hold 300 giây và shutdown 30 giây. | AI có xu hướng chọn cấu hình JMeter mặc định khi sinh plan nếu prompt không nhấn mạnh rằng plugin Ultimate Thread Group là bắt buộc. |
| Load Test - dữ liệu đăng nhập | AI ban đầu chưa đảm bảo mỗi VU có tài khoản riêng, dễ dẫn đến việc nhiều thread dùng chung một user. | Với workflow có login, cart, checkout và order history, dùng chung một tài khoản có thể gây nhiễu trạng thái giỏ hàng và lịch sử đơn hàng. | Chuẩn bị 10 tài khoản hợp lệ riêng cho Load Test, tương ứng với 10 VU, và seed dữ liệu để tất cả tài khoản đăng nhập được. | AI ưu tiên làm cho request login thành công nhưng chưa xét đủ đặc thù stateful của endpoint cart/orders. |
| Dữ liệu giữa các scenario | AI chưa tách rõ dữ liệu đăng nhập theo từng loại test. Load, Stress và Spike có số VU khác nhau nên không nên dùng một bộ credential chung. | Một bộ data chung làm test khó mở rộng và có thể thiếu tài khoản khi Stress/Spike dùng số VU cao hơn Load. | Tách credential theo scenario: Load dùng số tài khoản phù hợp 10 VU, Stress dùng số tài khoản phù hợp mức peak 50 VU; các plan sau cần dùng bộ credential riêng theo số VU tương ứng. | AI tổng quát hóa việc reuse CSV để giảm lặp, nhưng bỏ sót yêu cầu dữ liệu phải khớp workload của từng scenario. |
| Stress Test - thiết kế lịch tăng tải | AI mô tả các mức 10, 20, 35 và 50 users nhưng chưa làm rõ cách biểu diễn chúng trong Ultimate Thread Group. | Nếu cấu hình mỗi mức như một nhóm độc lập không chồng lấn đúng cách, tải có thể giảm gần về 0 giữa các stress level. | Sửa Stress plan thành continuous stepped profile: 10 -> 20 -> 35 -> 50 users bằng các row tăng thêm và chồng lấn thời gian hold. | AI nhầm giữa “target tổng số user tại một mức” và “số thread được start thêm trong từng row” của Ultimate Thread Group. |
| Stress Test - sinh test plan | AI tạo plan có lịch chạy nhìn giống các mức stress độc lập, nhưng khi review bằng logic schedule thì không giữ được tải liên tục. | Test plan cũ không còn được xem là bản cuối để tiếp tục kết luận Stress vì profile tải không đúng mục tiêu. | Reopen Phase 2, sửa lại schedule và yêu cầu review lại trước khi chạy Stress mới. | AI chỉ kiểm tra XML và cấu trúc sampler, nhưng chưa kiểm tra đầy đủ ý nghĩa runtime của lịch thread. |
| Phân tích sau khi plan bị reopen | AI đã có phân tích dựa trên kết quả Stress cũ, trong khi sau đó Stress Phase 2 bị reopen vì plan chưa phù hợp. | Kết quả từ plan cũ không nên dùng làm kết luận Stress cuối cùng. | Giữ phân tích cũ như lịch sử tham khảo, nhưng không dùng làm kết luận chính cho đến khi plan mới được accept và chạy lại. | AI theo dữ liệu kết quả có sẵn mà chưa gắn chặt với lifecycle của test plan sau human review. |

## 3. Những điểm AI làm đúng sau khi được review

Sau human review, các test plan đã giữ cùng workflow end-to-end `Login -> Product List -> Product Detail -> Add to Cart -> Checkout -> My Orders`, bao phủ đủ auth-heavy, read-heavy và transactional endpoints. Các sampler chính có correlation cho JWT token và order ID, có assertion cho HTTP status và nội dung response quan trọng, đồng thời dùng dữ liệu đầu vào cho credential, sản phẩm và checkout.

Load Test sau khi chỉnh đã phù hợp hơn với mục tiêu baseline: 10 concurrent users, ramp-up 60 giây, hold 300 giây, shutdown 30 giây và dữ liệu đăng nhập tách theo 10 VU. Stress Test sau khi review cũng được chỉnh để tăng tải liên tục 10 -> 20 -> 35 -> 50 users, tránh khoảng rơi tải giữa các level.

## 4. Kết luận human review cho Task 1

AI hỗ trợ tốt trong việc tạo nhanh cấu trúc JMeter, workflow, assertions và dữ liệu kiểm thử ban đầu, nhưng vẫn cần human review để phát hiện các lỗi liên quan đến semantics của công cụ và đặc thù endpoint. Các lỗi quan trọng nhất là dùng sai loại Thread Group cho Load, chưa tách dữ liệu đăng nhập theo số VU/scenario, và hiểu chưa đúng cách Ultimate Thread Group cộng dồn users trong Stress Test.

Sau khi chỉnh, các artifact được giữ theo hướng phù hợp hơn với yêu cầu HW05: cùng một business workflow cho các scenario, workload profile khác nhau theo từng loại test, dữ liệu đăng nhập đủ cho số VU, và không dùng kết quả từ plan đã bị reopen làm kết luận cuối.
