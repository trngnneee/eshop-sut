---
name: api-test-generator
description: AI-driven API test case generator cho SUT EShop trong HW06 – API Testing (level G9.5 – Create). Dùng skill này khi người dùng muốn "generate test case", "sinh test case từ API spec", "tạo bộ test cho API", nhắc tới api_specification.md, EShop, domain partition, state transition, security testing SEC-01–SEC-07, hoặc schema validation cho HW06. Skill điều khiển việc sinh test case qua 4 giai đoạn tách biệt (domain partitions → state transitions → security → schema validation) thay vì 1 prompt chung chung, rồi gộp lại thành bộ test case có ID, có thể mở bằng Excel, sẵn sàng cho bước audit/extend/export mà người dùng tự làm sau đó. Skill cũng ghi AI Audit Log bắt buộc (Name of AI tool / Date-time / Prompt / Output) cho mọi lượt tương tác AI thuộc HW06 — kể cả các việc ngoài sinh test case như viết hoặc sửa main report, viết AI Critique, viết bug report — nên cũng nên dùng skill này khi người dùng nhờ hỗ trợ các phần đó của HW06 và cần được log lại. Luôn dùng skill này thay vì tự generate test case một lần cho toàn bộ API.
---

# API Test Generator (HW06 – G9.5)

## Skill này dùng để làm gì

Đây là phần triển khai (implementation / pseudocode sống) của **"AI-driven API test generator"** mà đề bài HW06 yêu cầu ở mục 7 (Agent Skill, level G9.5 – Create):

> Given the API specification, it produces test cases automatically.

Skill **chỉ phụ trách bước sinh test case tự động**. Các bước sau — audit (VALID/INVALID/INCOMPLETE), extend (≥5 test case AI bỏ sót), execute (Postman/Newman), report bug, export Excel/CI-CD — **do người dùng tự làm**, skill không tự động thực hiện các bước đó trừ khi được yêu cầu rõ ràng.

Yêu cầu về diagram tự vẽ tay (self-drawn) là trách nhiệm của người dùng, **không phải việc của skill này** — skill chỉ là phần code/pseudocode hiện thực hoá thiết kế đó.

## Nguyên tắc cốt lõi: 4 giai đoạn tách biệt, KHÔNG generate hết trong 1 lần

Đề bài cấm kiểu prompt chung chung "generate all the API test cases from the spec and run them". Vì vậy pipeline bên dưới bắt buộc chạy **tuần tự qua 4 giai đoạn độc lập**, mỗi giai đoạn có mục tiêu riêng, input riêng, và ghi ra 1 file riêng trước khi sang giai đoạn kế tiếp:

1. **Stage 1 — Domain Partitions** (phân vùng miền giá trị từng tham số)
2. **Stage 2 — State Transitions** (chuyển trạng thái, đặc biệt FR-10)
3. **Stage 3 — Security** (SEC-01 → SEC-07 + các lỗ hổng API phổ biến)
4. **Stage 4 — Schema Validation** (đối chiếu response với spec)

Sau đó là **Stage 5 — Consolidate**: gộp 4 file lại, đánh số ID thống nhất, kiểm tra đủ ngưỡng ≥ 35 test case/API.

**Không được gộp 4 giai đoạn vào 1 lượt suy nghĩ/1 lần viết duy nhất.** Với mỗi API đang xử lý, hãy hoàn thành xong Stage 1 (viết file `01_domain_partitions.json` ra đĩa) rồi mới đọc lại spec và bắt đầu Stage 2, v.v. Điều này vừa đúng tinh thần "guide the AI through every step", vừa tạo ra dấu vết log tự nhiên (mỗi file = 1 lần "hỏi AI 1 việc cụ thể").

## AI Audit Log — BẮT BUỘC, ghi ngay sau mỗi stage sinh test case

Đề bài (mục 9 — AI Audit Report, mandatory appendix) yêu cầu ghi log **từng lượt tương tác AI dùng để tạo ra kết quả**, đủ 4 field:

> Name of the AI tool / Date and time / Your prompt / The AI output

**Phạm vi log: chỉ Stage 1 → 4** (4 lượt AI thật sự sinh nội dung test case). Các thao tác thuần kỹ thuật/hệ thống — Stage 0 (tạo thư mục, copy spec), Stage 5 (chạy `consolidate.py` để gộp file) — **không phải là 1 lượt "hỏi AI"**, nên **không** đưa vào `ai_audit_log.md`. Đừng log kiểu "AI tool: N/A" cho các bước này, sẽ làm file audit bị loãng và có entry giả không đúng tinh thần mục 9. Những bước đó chỉ cần phản ánh ở `README.md` (tóm tắt tiến độ) là đủ.

Quy tắc bắt buộc cho 4 entry Stage 1–4:

1. Log ghi vào `./API-testing/<api-slug>/ai_audit_log.md`, khởi tạo ở Stage 0 với dòng mở đầu đúng format đề bài yêu cầu: `"I use AI tools for the following tasks:"` (chỉ tạo file + viết dòng mở đầu, chưa có entry nào — entry đầu tiên xuất hiện khi Stage 1 xong).
2. **Ngay sau khi ghi xong file JSON của 1 stage** (không gộp lại chờ đến cuối), append 1 entry mới vào `ai_audit_log.md` theo đúng template ở `assets/ai_audit_log_entry_template.md`, gồm đủ 4 field:
   - **AI tool**: tên + phiên bản model đang chạy skill này (lấy từ system prompt/ngữ cảnh hiện tại nếu biết, ví dụ "Claude Sonnet 5"; nếu không xác định được version chính xác, ghi "Claude (phiên bản không xác định được từ ngữ cảnh)"). Không tự ý ghi tên tool khác nếu không đúng thực tế đang chạy.
   - **Date and time**: lấy thời gian **thật** bằng lệnh `date "+%Y-%m-%d %H:%M:%S %Z"` qua bash tool ngay tại thời điểm chạy stage đó — **không được bịa/ước lượng giờ**.
   - **Your prompt**: chép lại **nguyên văn, đầy đủ** chỉ dẫn cụ thể đã dùng để sinh stage đó — tức là bản tóm tắt cụ thể hoá từ mục "Stage N" tương ứng trong SKILL.md này, áp dụng cho đúng endpoint/tham số/SEC-id đang xử lý (không chỉ ghi "xem SKILL.md" — phải viết ra prompt thực sự đã dùng, đủ để người khác đọc lại và tái tạo được kết quả).
   - **The AI output**: **tóm tắt** những gì đã sinh ra ở stage đó — không dán full JSON. Gồm: số lượng test case sinh ra, liệt kê ngắn gọn `temp_id` + `title` của từng test case (1 dòng/case), và ghi rõ "chi tiết đầy đủ tại `0N_....json`" để người đọc tự mở file khi cần. Không cần copy nguyên khối JSON vào log.
3. Không log dồn 4 stage vào 1 entry chung chung — đúng tinh thần "step by step" nghĩa là audit log cũng phải tách theo từng bước, không phải 1 prompt tổng.
4. Đúng 4 entry cho mỗi API (1 entry/stage sinh test case). Không thêm, không bớt.

File `ai_audit_log.md` này **thay thế** file `generation_log.md` ở bản thiết kế trước — không cần tạo thêm file log riêng nữa.

## General Audit Log — cho các prompt KHÁC ngoài 4 stage sinh test case

`ai_audit_log.md` ở trên chỉ log 4 stage sinh test case của từng API. Nhưng đề bài mục 9 yêu cầu log **mọi** lượt tương tác AI dùng trong cả bài, không riêng phần sinh test case. Vì vậy: bất cứ khi nào người dùng nhờ hỗ trợ AI cho các việc **khác** thuộc HW06 — ví dụ viết/sửa main report, viết đoạn AI Critique (mục 10), viết nội dung bug report, viết/sửa README, viết CI/CD report, sửa lại 1 đoạn báo cáo đã có, v.v. — cũng phải log lại, dù các việc đó không thuộc pipeline 4 stage.

Quy tắc:

1. Log vào file chung `./API-testing/general_audit_log.md` (không phải file theo `<api-slug>`, vì các việc này không gắn với 1 API cụ thể). Tạo file này nếu chưa có, dòng mở đầu cũng là `"I use AI tools for the following tasks:"`.
2. **Mỗi lần người dùng đưa ra 1 yêu cầu mới thuộc dạng này** (kể cả yêu cầu sửa lại/chỉnh sửa 1 việc đã làm trước đó — sửa report tính là 1 entry mới, không gộp vào entry viết report lần đầu) → append 1 entry, dùng đúng format 4-field như template ở `assets/ai_audit_log_entry_template.md` (đổi tiêu đề entry cho phù hợp, không nhất thiết phải là "Stage N", có thể ghi ví dụ `### Viết main report — phần 6. Requirements`, `### Sửa lại đoạn AI Critique theo góp ý`).
3. Cùng nguyên tắc như log stage: **Date and time** lấy thật qua `date`, **Your prompt** chép lại đúng yêu cầu/chỉ dẫn đã dùng (có thể là nguyên văn câu người dùng nhắn, hoặc bản diễn giải cụ thể việc đã làm nếu người dùng chỉ nói ngắn gọn), **The AI output** chỉ **tóm tắt** đã tạo/sửa gì (không dán full nội dung report — ví dụ "Đã viết mục 5 (API Selection) và mục 6 (Requirements pipeline) của main report, khoảng 400 từ" hoặc "Đã sửa lại đoạn AI Critique theo hướng cụ thể hoá ví dụ SEC-03 bị AI bỏ sót").
4. Không log các việc **không liên quan tới AI hỗ trợ** — ví dụ người dùng tự hỏi thông tin, tự trao đổi ý tưởng mà không yêu cầu AI tạo/sửa nội dung nộp bài thì không cần log.
5. Việc log này **không thay thế** việc người dùng tự viết AI Critique/AI Audit Report hoàn chỉnh để nộp — chỉ là nhật ký nguyên liệu để họ tổng hợp lại cho đúng và đủ, tránh quên lượt tương tác nào.

## Cấu trúc thư mục output

Tất cả output nằm trong `./API-testing` ở thư mục làm việc hiện tại của người dùng (KHÔNG nằm trong thư mục skill):

```
API-testing/
├── README.md                          # index tổng: các API đã xử lý + tổng số test case
├── general_audit_log.md               # AI Audit Log cho các việc KHÁC ngoài 4 stage (viết/sửa report, AI critique, bug report...)
├── specs/
│   └── api_specification.md           # copy của spec đã dùng để sinh test (để đối chiếu sau này)
└── <api-slug>/                        # 1 thư mục cho mỗi API được chọn, vd: login, cart, product-admin
    ├── 01_domain_partitions.json
    ├── 02_state_transitions.json
    ├── 03_security.json
    ├── 04_schema_validation.json
    ├── test_cases_master.csv          # bản gộp cuối cùng, mở được bằng Excel
    └── ai_audit_log.md                # AI Audit Log bắt buộc: 1 entry/stage, đủ 4 field theo mục 9 đề bài
```

`<api-slug>` đặt theo endpoint/feature chính, chữ thường, nối gạch ngang, ví dụ: `login`, `shopping-cart`, `product-admin`, `order-admin`.

## Quy trình chi tiết

### Bước 0 — Chuẩn bị

1. Tìm `api_specification.md` của EShop (người dùng cung cấp, hoặc nếu repo `https://github.com/ttbhanh/eshop-sut` đã được clone/tải, đọc từ đó).
2. Nếu chưa rõ **API nào** đang cần sinh test case, hỏi người dùng 1 câu duy nhất (dùng `ask_user_input_v0` nếu đang ở giao diện có hỗ trợ) để xác nhận API/endpoint + method, ví dụ: "Login (POST /api/auth/login)", "Shopping Cart (POST/GET/DELETE /api/cart)", "Product Admin CRUD (POST/PUT/DELETE /api/admin/products)". Đừng đoán bừa nếu spec có nhiều endpoint khớp mô tả.
3. Tạo `./API-testing/specs/api_specification.md` (copy toàn bộ hoặc phần liên quan) và `./API-testing/<api-slug>/`.
4. Đọc kỹ trong spec: các tham số, header bắt buộc, response schema, mã lỗi, và nếu API liên quan checkout/order thì đọc rõ state machine FR-10 (xem `references/state_machine.md` trong skill này để đối chiếu nhanh).
5. Khởi tạo `./API-testing/<api-slug>/ai_audit_log.md` với dòng đầu `"I use AI tools for the following tasks:"` (đúng câu đề bài yêu cầu ở mục 9) và 1 dòng mô tả API đang xử lý (endpoint, method, related FR). Lấy timestamp khởi tạo bằng `date "+%Y-%m-%d %H:%M:%S %Z"` qua bash tool.

### Stage 1 — Domain Partitions

Mục tiêu: với **từng tham số** của endpoint (path param, query param, body field, header), liệt kê các phân vùng: valid điển hình, valid biên (boundary), invalid định dạng, invalid biên, thiếu field bắt buộc, field thừa/không mong đợi, kiểu dữ liệu sai (string thay vì number, v.v.), giá trị rỗng/null/whitespace.

Quy tắc:
- Duyệt **từng tham số một cách có hệ thống**, không bỏ sót tham số nào trong spec.
- Với field có ràng buộc rõ (email format, độ dài mật khẩu, `price > 0`, enum trạng thái...), sinh cả 2 phía: đúng ngay biên và sai ngay biên (ví dụ `price = 0`, `price = 0.01`, `price = -1`).
- Không trộn logic bảo mật (SQLi, IDOR...) vào đây — để dành cho Stage 3.
- Ghi kết quả ra `01_domain_partitions.json`, mỗi phần tử theo schema ở `references/test_case_schema.md`, field `category = "DomainPartition"`.
- Mục tiêu định lượng: khoảng 12–18 test case (tuỳ số tham số của endpoint), đừng ép số nếu API có ít tham số — thà ít mà đúng còn hơn thêm case trùng lặp vô nghĩa.
- **Ngay sau khi ghi xong file trên**: append 1 entry vào `ai_audit_log.md` (xem mục "AI Audit Log" ở trên) — lấy giờ thật, chép lại prompt cụ thể hoá cho đúng endpoint/tham số vừa xử lý, dán JSON vừa sinh làm "AI output".

### Stage 2 — State Transitions

Mục tiêu: test các đường chuyển trạng thái hợp lệ và không hợp lệ.

- Nếu API liên quan **order** (FR-10): dùng máy trạng thái `pending → confirmed → shipping → delivered` cộng quy tắc huỷ (cancel), tham khảo `references/state_machine.md`. Sinh test cho: mọi cạnh hợp lệ, mọi cạnh **không** hợp lệ (vd nhảy cóc `pending → delivered`, hoặc thao tác lên state đã `delivered`/`cancelled`), huỷ đúng lúc được phép và huỷ sai lúc (đã shipping/delivered).
- Nếu API là auth/login (FR-02: account lockout): coi "số lần đăng nhập sai" và "trạng thái khoá tài khoản" như 1 state machine nhỏ (active → locked, unlock sau timeout/reset) và test tương tự.
- Nếu API không có khái niệm trạng thái rõ ràng (vd product listing), vẫn có thể có state ẩn (giỏ hàng rỗng/có hàng, sản phẩm active/inactive, coupon còn hạn/hết hạn) — hãy tìm state ẩn đó trong spec trước khi kết luận "không áp dụng".
- Mỗi test case ghi rõ `from_state`, `to_state` (hoặc `action`), `expected_allowed` (true/false).
- Ghi ra `02_state_transitions.json`, `category = "StateTransition"`.
- Mục tiêu định lượng: 6–10 test case nếu có state machine rõ ràng; nếu thực sự không có, ghi rõ lý do trong entry log của stage này thay vì bịa case.
- **Ngay sau khi ghi xong file trên**: append 1 entry vào `ai_audit_log.md` — cùng quy tắc như Stage 1 (giờ thật, prompt cụ thể đã dùng, output JSON vừa sinh).

### Stage 3 — Security

Mục tiêu: map trực tiếp vào **SEC-01 → SEC-07** (xem đầy đủ ở `references/security_requirements.md`), cộng thêm các lớp tấn công API phổ biến khác nếu phù hợp với endpoint.

Bắt buộc rà qua từng SEC liên quan đến API đang test (không phải SEC nào cũng áp dụng cho mọi API — chỉ chọn cái liên quan, nhưng phải liên quan tới FR-02, FR-03, FR-04, FR-12, FR-18, FR-19 thì gần như luôn cần SEC-02/SEC-03):

- **SEC-01** (không lưu plaintext password): test gián tiếp qua API — ví dụ endpoint đổi mật khẩu/đăng ký không được trả password về trong response; hoặc test không thể áp dụng trực tiếp qua black-box API thì ghi rõ trong `notes` là "cần kiểm tra qua DB/code review, không kiểm được thuần qua API" — vẫn liệt kê case nhưng đánh dấu rõ.
- **SEC-02** (JWT bắt buộc cho API bảo mật): test gọi API không kèm token, token rỗng, token sai định dạng, token hết hạn, token hợp lệ nhưng của resource khác.
- **SEC-03** (Admin API phải check role='admin' trong token, không chỉ check có token): test dùng token hợp lệ của **user thường** gọi API admin (role escalation / privilege escalation) — đây là case hay bị AI generic bỏ sót, bắt buộc phải có.
- **SEC-04** (escape output, không dùng innerHTML trực tiếp): với API có field hiển thị lại ra UI (tên sản phẩm, review, tên user...), test nhập XSS payload (`<script>alert(1)</script>`) vào field đó, kỳ vọng bị lưu dưới dạng escape hoặc bị từ chối — không thực thi được.
- **SEC-05** (parameterized query, chống SQL injection): test SQLi payload (`' OR '1'='1`, `'; DROP TABLE users; --`) vào các field text, đặc biệt field dùng để tìm kiếm/lọc/login.
- **SEC-06** (API update profile không cho đổi `role` từ client): test gửi thêm field `role` (hoặc `is_admin`) trong body update profile của user thường, kỳ vọng bị bỏ qua/từ chối, không được nâng quyền.
- **SEC-07** (OTP reset password đủ entropy ≥6 số, có hạn dùng, vô hiệu sau khi dùng): test OTP sai, OTP hết hạn, dùng lại OTP đã dùng 1 lần, brute-force OTP ngắn.
- Ngoài 7 mục trên, cân nhắc thêm nếu phù hợp: rate limiting/lockout (FR-02), IDOR (đọc/sửa resource của user khác bằng cách đổi ID trong URL/body), mass assignment các field nhạy cảm khác ngoài `role`.

Mỗi test case ghi rõ field `sec_id` (một hoặc nhiều trong SEC-01..SEC-07, hoặc `"OWASP-Other"` nếu không thuộc 7 mục trên).

- Ghi ra `03_security.json`, `category = "Security"`.
- Mục tiêu định lượng: 7–12 test case, ưu tiên bao phủ hết các SEC-xx liên quan hơn là số lượng.
- **Ngay sau khi ghi xong file trên**: append 1 entry vào `ai_audit_log.md` — trong phần "Your prompt" nhớ liệt kê rõ các SEC-id đã được yêu cầu rà (vì đây là phần TA hay soi kỹ nhất).

### Stage 4 — Schema Validation

Mục tiêu: đối chiếu **hình dạng response** với spec, không phải logic nghiệp vụ.

- Response thành công (2xx): đúng field bắt buộc, đúng kiểu dữ liệu từng field, không thiếu/không thừa field so với spec, đúng format field đặc biệt (date, email, currency...).
- Response lỗi (4xx/5xx): có đúng cấu trúc lỗi chuẩn của spec (vd `{ "error": { "code": ..., "message": ... } }`), đúng status code cho từng loại lỗi (400 vs 401 vs 403 vs 404 vs 422).
- Kiểm tra các trường nhạy cảm **không** bị lộ ra response (password hash, token nội bộ...).
- Ghi ra `04_schema_validation.json`, `category = "SchemaValidation"`.
- Mục tiêu định lượng: 5–8 test case.
- **Ngay sau khi ghi xong file trên**: append 1 entry vào `ai_audit_log.md` — cùng quy tắc như các stage trước.

### Stage 5 — Consolidate

1. Chạy script gộp:
   ```bash
   python3 /mnt/skills/.../api-test-generator/scripts/consolidate.py \
     --api-dir ./API-testing/<api-slug>
   ```
   (đường dẫn script thực tế = nơi skill này được cài đặt; nếu không chắc, dùng `find` để định vị `consolidate.py` trong thư mục skill trước khi gọi).
2. Script sẽ:
   - Gộp 4 file JSON thành `test_cases_master.csv`.
   - Đánh lại ID theo format `TC-<API-SLUG>-<CAT>-<NNN>` (CAT = DP/ST/SEC/SV).
   - In ra tổng số test case theo từng category + tổng cộng.
   - Cảnh báo nếu tổng < 35 (ngưỡng đề bài yêu cầu ≥35/API) — nếu thiếu, quay lại đúng stage đang thiếu (không phải sinh bừa thêm ở stage bất kỳ) để bổ sung cho đủ và hợp lý.
3. Consolidate là thao tác kỹ thuật (chạy script), **không** tạo entry trong `ai_audit_log.md` — xem giải thích ở mục "AI Audit Log" phía trên.
4. Cập nhật `./API-testing/README.md`: bảng tổng hợp tất cả API đã xử lý, số test case mỗi category, tổng số, ngày giờ chạy gần nhất, và ghi chú ngắn "đã chạy consolidate lúc ..." (không cần format 4-field).

## Khi xử lý nhiều API (Pool A / B / C)

Lặp lại toàn bộ Stage 0 → 5 **cho từng API riêng biệt**, không trộn 2 API vào cùng 1 file. Mỗi API có thư mục `<api-slug>` riêng dưới `API-testing/`.

## Sau khi hoàn tất

Dừng lại ở việc sinh test case. **Không tự động** làm audit (gắn nhãn VALID/INVALID/INCOMPLETE), không tự thêm 5 test case "AI bỏ sót" (vì bản thân AI vừa sinh ra không thể tự đánh giá cái mình bỏ sót một cách đáng tin — đây đúng là phần người dùng phải tự làm), không tự chạy Postman/Newman, không tự đẩy lên GitHub. Nếu người dùng muốn các bước đó, họ sẽ yêu cầu riêng.

Kết thúc bằng việc báo lại ngắn gọn: đã sinh bao nhiêu test case, phân bổ theo 4 category, đường dẫn file `test_cases_master.csv` để người dùng mở bằng Excel và tự audit/extend.

## Tài liệu tham khảo trong skill

- `references/security_requirements.md` — bảng đầy đủ SEC-01 → SEC-07 kèm gợi ý cách test qua API cho từng mục.
- `references/state_machine.md` — sơ đồ trạng thái đơn hàng FR-10 (pending → confirmed → shipping → delivered + cancel) dùng cho Stage 2.
- `references/test_case_schema.md` — định nghĩa đầy đủ các field của 1 test case (dùng thống nhất ở cả 4 stage).
- `scripts/consolidate.py` — gộp 4 file JSON stage thành 1 CSV master, đánh ID, đếm và cảnh báo ngưỡng ≥35.
- `assets/test_case_template.csv` — header mẫu, dùng nếu cần tạo file CSV tay thay vì qua script.
- `assets/ai_audit_log_entry_template.md` — template 1 entry log đúng 4 field bắt buộc (AI tool / Date-time / Prompt / Output), dùng cho cả 4 stage sinh test case lẫn các entry trong `general_audit_log.md`.