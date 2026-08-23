# Human-Extended Test Cases - FR-09 Apply Coupon

File này liệt kê các test case do người kiểm thử bổ sung sau khi audit bộ test do AI sinh. Các case này tập trung vào tính đúng công thức giảm giá, các invariant tiền tệ, security edge cases quanh `user_id`, và state transition giữa việc preview coupon với việc lưu `coupon_usage`.

## Summary

- API chính: `POST /api/apply-coupon`
- API liên quan để kiểm state: `POST /api/coupon-usage`
- Số test case bổ sung: 7
- Lý do bổ sung: bộ AI-generated ban đầu đã kiểm nhiều input và schema chung của apply-coupon, nhưng chưa kiểm đủ giá trị tính toán cụ thể theo dữ liệu seed, chưa tách rõ coupon percent/fixed, chưa kiểm các giá trị falsy như `null`/`0` cho `user_id`, và chưa phân biệt preview coupon với state lưu usage sau checkout.

## Test Cases

| ID | Type | Scenario | Preconditions | Request / Steps | Expected Result |
| --- | --- | --- | --- | --- | --- |
| HT-APPLY-EXT-001 | Schema Validation, Business Logic | Coupon percent `SAVE10` phải tính đúng 10% | Coupon `SAVE10` tồn tại, `type=percent`, `discount_value=10`, `min_order_amount=300000`; `user_id=1` tồn tại | `POST /api/apply-coupon` với `code=SAVE10`, `total_amount=500000`, `user_id=1` | API trả `200`; `discount_amount = 50000`; `final_amount = 450000`; giá trị giảm không âm và không vượt quá tổng tiền. |
| HT-APPLY-EXT-002 | Schema Validation, Business Logic | Coupon fixed `BIGBUY` phải tính đúng số tiền giảm cố định | Coupon `BIGBUY` tồn tại, `type=fixed`, `discount_value=50000`, `min_order_amount=500000`; `user_id=1` tồn tại | `POST /api/apply-coupon` với `code=BIGBUY`, `total_amount=600000`, `user_id=1` | API trả `200`; `discount_amount = 50000`; `final_amount = 550000`. |
| HT-APPLY-EXT-003 | Security, Business Logic | Coupon percent không được tạo `final_amount` âm hoặc tăng tổng tiền | Coupon `SAVE10` tồn tại; `total_amount=500000`; `user_id=1` tồn tại | Gọi `POST /api/apply-coupon` và kiểm các field tiền tệ trong response | `discount_amount >= 0`; `discount_amount <= total_amount`; `final_amount >= 0`; `final_amount <= total_amount`. |
| HT-APPLY-EXT-004 | Security, Domain Partition | `user_id = null` không được bypass giới hạn sử dụng coupon | Coupon `SAVE10` tồn tại, `max_uses_per_user=1`; `total_amount` đủ điều kiện | `POST /api/apply-coupon` với `user_id=null` | API trả `400` hoặc xử lý an toàn tương đương; không được dùng `null` để né quota theo user. |
| HT-APPLY-EXT-005 | Security, Domain Partition | `user_id = 0` không được bypass giới hạn sử dụng coupon | Coupon `SAVE10` tồn tại, `max_uses_per_user=1`; `total_amount` đủ điều kiện | `POST /api/apply-coupon` với `user_id=0` | API trả `400` hoặc xác thực user hợp lệ; không được xem `0` là falsy để bỏ qua kiểm tra quota. |
| HT-APPLY-EXT-006 | State Transition | Preview apply-coupon không được tự tăng `coupon_usage` | Coupon `SAVE10` tồn tại, `max_uses_per_user=1`; `user_id=1` chưa có usage cho coupon này trước test | Gọi `POST /api/apply-coupon` hai lần liên tiếp, không gọi `POST /api/coupon-usage` ở giữa | Cả hai lần vẫn là preview tính toán; nếu lần hai bị chặn quota thì endpoint đã tạo side effect sai chỗ. |
| HT-APPLY-EXT-007 | Domain Partition | Code có khoảng trắng đầu/cuối không được match nhầm coupon hợp lệ | Coupon `SAVE10` tồn tại; `user_id=1` tồn tại; `total_amount` đủ điều kiện | `POST /api/apply-coupon` với `code=" SAVE10 "` hoặc `"SAVE10 "` | API xử lý nhất quán: hoặc trim theo rule rõ ràng, hoặc trả `404`/error; không được áp dụng coupon ngoài ý muốn khi input không đúng mã. |

## Why The AI Missed Them

| Added Test Case | Why AI Missed It |
| --- | --- |
| HT-APPLY-EXT-001 | AI đã kiểm response có `discount_amount` và `final_amount`, nhưng chưa dùng dữ liệu seed để tính expected value cụ thể. Đây là thiếu sót do prompt chưa yêu cầu kiểm công thức tính tiền bằng số liệu cụ thể. |
| HT-APPLY-EXT-002 | AI tập trung vào luồng coupon hợp lệ chung, nhưng chưa ép bao phủ từng loại coupon. Vì vậy AI dễ kiểm `SAVE10` mà bỏ sót nhánh fixed discount của `BIGBUY`. |
| HT-APPLY-EXT-003 | AI thường dừng ở schema/type check, chưa kiểm invariant an toàn của giá tiền. Với API tính tiền, các ràng buộc `>= 0` và `<= total_amount` là quan trọng nhưng dễ bị bỏ sót nếu prompt không nhắc rõ business logic. |
| HT-APPLY-EXT-004 | AI đã có case thiếu `user_id` và sai kiểu `user_id`, nhưng chưa tách `null` thành một partition riêng. Thiếu sót đến từ domain partition chưa đủ sâu cho các giá trị falsy. |
| HT-APPLY-EXT-005 | AI không soi tới chi tiết implementation `if (user_id)`, nên bỏ qua rủi ro `user_id=0` bị coi là falsy và làm bypass logic kiểm usage. Đây là giới hạn khi model chỉ dựa trên spec mà không phân tích code path cụ thể. |
| HT-APPLY-EXT-006 | AI có nhắc quota/coupon usage, nhưng chưa tách rõ hành động preview coupon và hành động persist usage sau checkout. Đây là state-transition gap do API có hidden state nằm ở endpoint liên quan `POST /api/coupon-usage`. |
| HT-APPLY-EXT-007 | AI đã tạo case code toàn khoảng trắng, nhưng bỏ sót khoảng trắng đầu/cuối quanh một mã hợp lệ. Đây là boundary input normalization phổ biến nhưng dễ bị bỏ qua nếu prompt chỉ yêu cầu empty/whitespace chung chung. |

## Notes For Execution

- Các case `HT-APPLY-EXT-001` đến `HT-APPLY-EXT-003` cần assert sâu vào giá trị `discount_amount` và `final_amount`, không chỉ assert HTTP status.
- Các case `HT-APPLY-EXT-004` và `HT-APPLY-EXT-005` nên kiểm thêm response không có `discount_amount/final_amount` thành công nếu API từ chối user_id không hợp lệ.
- Case `HT-APPLY-EXT-006` cần chạy theo sequence và đảm bảo không gọi `POST /api/coupon-usage` giữa hai lần preview.
- Case `HT-APPLY-EXT-007` cần thống nhất policy với backend: nếu hệ thống chủ động trim code thì expected có thể là `200`; nếu lookup exact match thì expected là `404`. Điều quan trọng là behavior phải nhất quán và được ghi rõ.
