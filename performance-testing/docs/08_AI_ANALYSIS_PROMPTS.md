# 08 — AI PROMPTS (chuỗi prompt từng bước)

> Đề §2: *"this does not mean issuing a single, generic prompt such as 'run a load test and tell me whether the performance is good.' Instead, you must guide the AI through every step of the technique as it was taught, using the AI as a disciplined assistant rather than a black box."*
>
> File này chứa **prompt mẫu** cho hai giai đoạn:
> - **§2** — sinh test plan (Task 1) → nhật ký ghi vào `deliverables/02_ai-generation-log.md`
> - **§3** — phân tích kết quả (Task 2) → output thô ghi vào `deliverables/06_ai-analysis-critique.md` §1

---

## 1. Nguyên tắc bắt buộc

### 1.1 Dùng prompt của mình, không chép nguyên

Đề §17: *"Copying between students — **including prompts** — results in a grade of 0 for both parties."*

Các prompt dưới đây là **khung**. Phải viết lại bằng lời của mình, thêm ngữ cảnh riêng (tên máy, số liệu thật, thứ tự bước mình chọn). Chép nguyên xi rồi nộp là rủi ro trùng lặp.

### 1.2 Ghi nhật ký ngay, không ghi lại sau

Mỗi lần gọi AI, ghi ngay bốn thứ đề §9 yêu cầu:

| Trường | Ví dụ |
| :--- | :--- |
| Tên công cụ AI | `Claude Opus 5 (Claude Code CLI)` / `ChatGPT GPT-5` / `Gemini 2.5 Pro` |
| Ngày giờ | `2026-08-12 14:07 (+07)` |
| Prompt | **nguyên văn**, kể cả lỗi gõ |
| Output | **nguyên văn**, không rút gọn, không sửa |

Ghi lại sau trí nhớ sẽ ra một nhật ký mượt mà nhưng giả — và người chấm nhìn ra ngay vì không có vòng lặp sai/sửa nào.

### 1.3 Output thô là output thô

Ở `06_ai-analysis-critique.md` §1, dán output AI **y nguyên**, kể cả chỗ nó sai. Chính những chỗ sai đó là nguyên liệu cho §2 (misinterpretation hunt). Sửa output trước khi dán là tự phá hỏng Task 2.

### 1.4 Nên dùng công cụ AI khác cho Task 2

Test plan sinh bằng công cụ A (ví dụ Claude Code, vì nó đọc được repo). Phần **phân tích kết quả** nên chạy trên công cụ B (ChatGPT hoặc Gemini) vì:

- AI Audit Report khai báo được **nhiều công cụ** → thể hiện năng lực G9.4 (Collaborate).
- Công cụ B **không có ngữ cảnh repo**, nên nó buộc phải suy luận từ số liệu thô — đúng tình huống đề muốn tạo ra, và **dễ mắc lỗi diễn giải hơn**, cho Task 2 nhiều nguyên liệu hơn.
- Tránh việc cùng một mô hình vừa tạo test plan vừa tự chấm kết quả của mình.

> *Phương án thay thế nếu không dùng được công cụ ngoài:* chạy §3 trong một **phiên hội thoại mới hoàn toàn**, chỉ cung cấp số liệu, không cung cấp repo. Ghi rõ điều này trong AI Audit Report.

---

## 2. Chuỗi prompt sinh test plan (Task 1)

Bảy bước. **Không gộp.** Sau mỗi bước, đọc output, sửa nếu cần, rồi mới sang bước sau — và ghi cả phần mình sửa vào nhật ký.

### Bước 1 — Phân tích endpoint và chốt workflow

```
Tôi đang làm bài tập kiểm thử hiệu năng trên một hệ thống e-commerce demo tên EShop
(Node.js + Express + SQLite, chạy ở http://localhost:3000).

Đây là đặc tả API: [dán nội dung api_specification.md]

Ràng buộc quan trọng: nhóm tôi có 5 người, mỗi người phải chọn MỘT workflow
end-to-end khác nhau, không được trùng. Workflow của tôi tên là "Browse-to-buy":
người dùng đăng nhập, xem TOÀN BỘ danh sách sản phẩm (KHÔNG dùng chức năng tìm
kiếm — endpoint search đã thuộc về bạn khác trong nhóm), xem chi tiết một sản
phẩm, thêm vào giỏ, rồi thanh toán.

Nhiệm vụ bước này: liệt kê chính xác các HTTP request tạo nên workflow đó, mỗi
request ghi rõ method, path, header, body. Với mỗi request, phân loại nó thuộc
nhóm nào trong ba nhóm mà đề bài yêu cầu: auth-heavy, read-heavy, transactional.

Chưa cần viết file JMeter. Chỉ cần bảng phân tích.
```

**Kiểm tra output:** đúng 5 request? có lẫn `?search=` không? phân loại 3 nhóm có hợp lý không?

### Bước 2 — Đọc mã nguồn để tìm đặc thù

```
Đây là mã nguồn xử lý của các endpoint trên:

[dán backend/server.js — ít nhất các đoạn: 32-66 (login), 141-165 (products),
 284-309 (cart & checkout), 100-110 (authenticateToken)]

Nhiệm vụ: đọc kỹ và chỉ ra những đặc điểm CÀI ĐẶT có thể ảnh hưởng tới thiết kế
test hiệu năng hoặc tới việc đặt assertion. Tôi quan tâm đặc biệt tới:
- cơ chế khóa tài khoản khi đăng nhập sai
- endpoint nào có thể trả HTTP 200 nhưng thực chất không thành công
- nơi lưu trạng thái giỏ hàng
- điểm nào có thể trở thành nút thắt cổ chai khi nhiều luồng chạy đồng thời

Với mỗi phát hiện, trích số dòng cụ thể.
```

**Đây là bước quan trọng nhất.** Nếu bỏ qua, AI sẽ thiết kế theo `README.md` và mắc lỗi mục 1, 3, 5 ở `07_HUMAN_REVIEW_TEMPLATE.md`. Nếu AI **vẫn** bỏ sót dù đã có mã nguồn → đó là **model limitations**, ghi vào human review.

### Bước 3 — Chọn tham số tải cho từng kịch bản

```
Dựa trên workflow đã chốt ở bước 1 và các đặc thù cài đặt ở bước 2, hãy đề xuất
tham số cho ba kịch bản Load, Stress, Spike, và một kịch bản Endurance/soak.

Với mỗi kịch bản, cho tôi: số thread, ramp-up, thời lượng, và think time cho từng
bước trong workflow.

Ràng buộc:
- SUT là tiến trình Node.js đơn luồng, chạy CÙNG MÁY với JMeter (máy cá nhân,
  [ghi CPU và RAM thật của máy bạn]). Tham số phải thực tế với phần cứng này.
- Think time phải mô phỏng người dùng THẬT đang duyệt catalog, không được bằng 0.
- Kịch bản Endurance phải kéo dài 10-15 phút theo yêu cầu đề bài.

Quan trọng: với MỖI con số, giải thích tại sao chọn con số đó. Tôi sẽ không dùng
tham số nào mà không có lý do.
```

### Bước 4 — Thiết kế assertion và correlation

```
Với 5 request của workflow, hãy thiết kế:
(a) các giá trị cần trích xuất từ response để dùng cho request sau (correlation)
(b) các assertion cho từng request

Lưu ý những gì bạn đã phát hiện ở bước 2. Cụ thể, tôi KHÔNG muốn assertion chỉ
kiểm tra response code, vì bạn đã chỉ ra rằng có endpoint trả 200 ngay cả khi
không tìm thấy dữ liệu.

Với mỗi assertion, ghi rõ loại element JMeter tương ứng (Response Assertion /
JSON Assertion / Duration Assertion) và cấu hình cụ thể của nó.
```

### Bước 5 — Thiết kế dữ liệu CSV

```
Workflow này phải data-driven bằng file CSV. Hãy thiết kế schema CSV:
tên cột, kiểu dữ liệu, cột nào dùng ở request nào, và ví dụ 3 dòng.

Ràng buộc:
- Kịch bản Spike cần tới 310 luồng đồng thời.
- Backend khóa tài khoản sau khi đăng nhập sai (xem bước 2), nên nhiều luồng
  KHÔNG được dùng chung một tài khoản.
- Địa chỉ giao hàng có chứa dấu phẩy.

Ngoài schema, hãy chỉ rõ cấu hình CSV Data Set Config trong JMeter cần đặt thế
nào để mỗi luồng nhận một dòng khác nhau, và giải thích chuyện gì xảy ra nếu
đặt sai.
```

### Bước 6 — Sinh file `.jmx`

```
Bây giờ hãy sinh file .jmx hoàn chỉnh cho kịch bản Load, dùng toàn bộ quyết định
đã chốt ở bước 1-5. Yêu cầu:

- JMeter 5.6.3, định dạng XML hợp lệ, mở được bằng JMeter GUI
- Tên file: 23127207_Load_20260812.jmx
- CHỈ dùng element có sẵn trong JMeter core, KHÔNG dùng plugin bên thứ ba
  (file phải mở được trên máy khác mà không cần cài thêm gì)
- Listener: Aggregate Report
- Đường dẫn CSV lấy từ biến ${__P(csvdir)}, không hard-code đường dẫn tuyệt đối
- Label của các sampler đặt là: 01_Login, 02_BrowseProducts, 03_ProductDetail,
  04_AddToCart, 05_Checkout

Nhắc lại ràng buộc: bước 2 là GET /api/products KHÔNG có query string.
```

> Lặp bước 6 cho Stress (Summary Report, 4 Thread Group bậc thang), Spike (View Results Tree chỉ ghi lỗi, 3 Thread Group), Endurance.
>
> Chú ý câu nhắc lại ràng buộc ở dòng cuối — theo `07_HUMAN_REVIEW_TEMPLATE.md` mục 6, ràng buộc âm phải nhắc lại ở **mỗi** bước, vì mô hình có xu hướng trôi về mẫu quen thuộc.

### Bước 7 — Tự rà soát

```
Hãy tự rà soát file .jmx vừa sinh và liệt kê những điểm mà bạn KHÔNG chắc chắn,
hoặc những giả định bạn đã đưa ra mà tôi cần tự kiểm chứng trước khi chạy tải thật.

Với mỗi điểm, ghi rõ hậu quả nếu giả định đó sai.
```

Output bước này thường lộ ra chính những chỗ AI sai → nguyên liệu tốt cho human review.

---

## 3. Chuỗi prompt phân tích kết quả (Task 2)

> Chạy trên **công cụ AI khác** (§1.4), **sau khi** đã có đủ 4 `summary.json`.
> Output thô của cả 3 prompt dán vào `deliverables/06_ai-analysis-critique.md` §1.

### 3.1 Chuẩn bị dữ liệu đầu vào

Cấp cho AI **dữ liệu thô có kiểm soát**, không cấp kết luận của mình:

```powershell
$pt = "C:\My Workspace\HCMUS\Test\Week 3\Hw2\performance-testing"

# Trích 200 dòng đầu của .jtl (giữ nguyên header) để AI thấy dữ liệu thô thật
Get-Content "$pt\results\load\23127207_Load_20260812.jtl" -TotalCount 200 |
  Out-File -Encoding utf8 "$pt\results\load\jtl-sample-200.txt"

# Thống kê đầy đủ
Get-Content "$pt\results\load\summary.json"
```

> **Không** đưa `summary.md` đã có nhận xét của mình vào prompt. Nếu mớm kết luận, AI sẽ lặp lại kết luận đó và Task 2 mất sạch nguyên liệu.

### 3.2 Prompt A — Phân tích metric

```
Tôi vừa chạy kiểm thử hiệu năng bằng Apache JMeter trên một REST API
(Node.js + Express + SQLite) và cần bạn phân tích kết quả.

Workflow gồm 5 bước, mỗi bước là một label:
  01_Login          POST /api/login
  02_BrowseProducts GET  /api/products     (trả về toàn bộ catalog, 505 sản phẩm)
  03_ProductDetail  GET  /api/products/{id}
  04_AddToCart      POST /api/cart
  05_Checkout       POST /api/checkout

Đây là 200 dòng đầu của file .jtl thô:
[dán jtl-sample-200.txt]

Đây là thống kê tổng hợp của toàn bộ run Load (50 luồng, ramp-up 60s, chạy 5 phút):
[dán summary.json của Load]

Và của run Stress (4 bậc: 25 → 50 → 100 → 200 luồng, mỗi bậc 2 phút):
[dán summary.json của Stress]

Nhiệm vụ:
1. Phân tích hiệu năng của từng label. Bước nào là nút thắt cổ chai? Vì sao?
2. Giải thích ý nghĩa của các cột trong file .jtl mà bạn dùng để kết luận.
3. Chỉ ra dấu hiệu bất thường nếu có.

Hãy nêu rõ con số cụ thể để chứng minh mỗi nhận định.
```

### 3.3 Prompt B — Đề xuất ngưỡng

```
Dựa trên số liệu trên, hãy đề xuất bộ ngưỡng hiệu năng (performance thresholds)
cho hệ thống này, dùng để chặn regression trong CI.

Với mỗi ngưỡng: đặt cho metric nào, ở label nào, giá trị bao nhiêu, và cơ sở nào
để chọn giá trị đó.

Cũng cho tôi biết: mức tải tối đa mà hệ thống này còn phục vụ ổn định là bao
nhiêu, và bạn suy ra con số đó từ đâu trong dữ liệu.
```

### 3.4 Prompt C — Đề xuất tối ưu

```
Cuối cùng, hãy đề xuất các biện pháp tối ưu hiệu năng cho backend này.

Bối cảnh kỹ thuật: Node.js + Express, cơ sở dữ liệu là SQLite (file cục bộ, dùng
driver `sqlite3` của npm). Endpoint GET /api/products chạy câu lệnh
`SELECT * FROM products` không có mệnh đề WHERE. Endpoint POST /api/checkout chạy
`INSERT INTO orders`. Giỏ hàng được lưu trong một object JavaScript trong bộ nhớ
tiến trình.

Với mỗi đề xuất: mô tả cách làm, ước lượng mức cải thiện, và mức độ rủi ro.

Xếp hạng các đề xuất theo tỉ lệ hiệu quả trên công sức.
```

**Prompt C là cái bẫy có chủ ý.** Dựa trên bối cảnh mô tả, AI rất có khả năng đề xuất "thêm index cho bảng products" và "dùng connection pool" — hai thứ **không áp dụng được** ở đây. Xem `09_MISINTERPRETATION_HUNT_TEMPLATE.md` §3.

> Bối cảnh trong prompt C là **mô tả trung thực** về hệ thống, không phải cài bẫy bằng thông tin sai. Việc AI vẫn đề xuất sai dù đã có đủ thông tin chính là bằng chứng cho phần "model limitations".

---

## 4. Khung `deliverables/02_ai-generation-log.md`

```markdown
# Nhật ký sinh Test Plan bằng AI

## Công cụ đã dùng
| Công cụ | Phiên bản | Dùng cho | Số lượt tương tác |
|---|---|---|---|
| <<FILL>> | <<FILL>> | Sinh test plan (Task 1) | <<FILL>> |
| <<FILL>> | <<FILL>> | Phân tích kết quả (Task 2) | <<FILL>> |

## Bước 1 — Phân tích endpoint và chốt workflow
**Thời gian:** <<FILL>>
**Prompt:**
> <<nguyên văn>>

**Output của AI:**
> <<nguyên văn, không rút gọn>>

**Đánh giá của tôi:** <<đúng/sai chỗ nào, tôi sửa gì>>

## Bước 2 — Đọc mã nguồn để tìm đặc thù
... (lặp lại cấu trúc trên cho cả 7 bước)

## Tổng kết
- Tổng số lượt tương tác: <<FILL>>
- Số lần phải sửa output của AI: <<FILL>>
- Bước nào AI làm tốt nhất: <<FILL>>
- Bước nào phải can thiệp nhiều nhất: <<FILL>>
```

---

## 5. Checklist

- [ ] Prompt đã **viết lại bằng lời của mình**, không chép nguyên khung này
- [ ] Chuỗi ≥ 7 bước cho Task 1, không gộp thành một prompt lớn
- [ ] Bước 2 (đọc mã nguồn) **đã thực hiện** — đây là bước phân biệt "dùng AI có kỷ luật" với "hỏi bừa"
- [ ] Ràng buộc "không dùng `?search=`" được nhắc lại ở **mỗi** bước sinh `.jmx`
- [ ] Task 2 chạy trên **công cụ AI khác** (hoặc phiên mới hoàn toàn, có ghi rõ)
- [ ] Output thô dán **nguyên văn**, kể cả chỗ sai
- [ ] Mỗi lượt ghi đủ 4 trường: tool / date-time / prompt / output
- [ ] Có ghi lại **cả những lần AI làm sai và mình phải sửa**, không chỉ những lượt thành công
