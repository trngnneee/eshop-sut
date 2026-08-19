# AI Audit Report — HW06 API Testing

> **Declaration:** I use AI tools for the following tasks,
> phân tích đặc tả, thiết kế test case theo từng kỹ thuật, rà soát độ bao phủ, tạo skeleton automation và hỗ trợ tổng hợp báo cáo. Mọi output đều phải được người học kiểm tra trước khi nộp.

## Công cụ đã dùng

| Công cụ | Phiên bản / mô hình | Vai trò | Quy tắc human review |
| :--- | :--- | :--- | :--- |
| OpenAI Codex | GPT-5 Codex (API workspace agent) | Phân tích repo, sinh và triển khai artifact HW06 | Đối chiếu `README.md`, `api_specification.md`, mã nguồn SUT và ký xác nhận từng bảng audit |

## Quy ước ghi log

- Mỗi kỹ thuật được thực hiện như một bước riêng, không dùng một prompt tổng để sinh toàn bộ suite.
- Thời gian dùng múi giờ `Asia/Bangkok` (UTC+07:00).
- Phần **Output** là bản tóm tắt có truy vết đến file output đầy đủ; không thay thế artifact gốc.
- Nhãn audit chỉ là đề xuất của AI cho đến khi người học ký dòng `Reviewed by` trong file `02-audit.md` tương ứng.

## Nhật ký tương tác

<!-- Các entry được append ngay sau mỗi bước generate/audit. -->

### INT-000 — Khởi tạo yêu cầu và chia pipeline

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T09:34:00+07:00`
- **Prompt của người học:** `dựa trên docs/hw06 để thực hiện toàn bộ requirements để đmả bảo được 100% số điểm`
- **Output của AI:** Đọc toàn bộ bộ tài liệu `docs/hw06`, xác nhận branch `HW6-Khoa`, lập kế hoạch Phase 0→9 và nhận diện các checkpoint bắt buộc do HUMAN thực hiện. AI không tạo bằng chứng giả và không bỏ qua human review của R-02.

### API-1 / P1 — Phân tích input và state, chưa sinh test case

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T09:54:00+07:00`
- **Prompt:**

  > Đối chiếu `POST /api/login` trong API specification, FR-02, SEC-01/02/05 và mã nguồn SUT. Chưa sinh test case. Chỉ liệt kê toàn bộ input ở body/header, kiểu, tính bắt buộc, partition có ý nghĩa; sau đó mô hình hóa `login_attempts` và `locked_until`, bao gồm đường reset và hết hạn. Phân biệt rõ ràng ràng buộc nghiệp vụ với ràng buộc riêng của HW06.

- **Output:** Nhận diện `email`, `password`, `Content-Type`, `X-Student-Id` và field thừa; tạo bảy trạng thái/transition từ Active-0 → Active-1 → Active-2 → Locked-30s → Lock-expired, cùng hai đường reset. Output đầy đủ ở `api-01-login/01-ai-generated.md` mục P1.

### API-1 / P2 — Domain partition và boundary value

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T09:56:00+07:00`
- **Prompt:**

  > Chỉ dùng mô hình input của P1. Áp dụng Equivalence Partitioning và Boundary Value Analysis cho từng input của `POST /api/login`. Mỗi invalid partition là một case độc lập. Expected phải phát biểu theo đặc tả; nếu phải giả định, vẫn giữ nguyên giả định để bước Human Audit phát hiện. Định dạng: ID, nhóm, tiêu đề, precondition, test data, HTTP status và body mong đợi.

- **Output:** Sinh 16 case `TC-API-LOGIN-001..016`: valid credential, wrong credential, unknown email, missing/empty/null/wrong-type fields, malformed/whitespace email, body array, missing content type và field thừa. AI đã tạo ba giả định cần audit: login password phải mạnh, email được trim, thiếu content type luôn là `415`.

### API-1 / P3 — State-transition coverage

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T09:58:00+07:00`
- **Prompt:**

  > Chỉ sinh test state transition dựa trên state model P1 và FR-02. Phủ threshold 3 lần sai, BVA thời gian 29/31 giây, đăng nhập đúng reset chuỗi sai và lần sai đầu tiên sau reset. Không dùng seed user chung cho case khóa tài khoản; nêu rõ precondition dùng user dùng-một-lần.

- **Output:** Sinh 8 case `TC-API-LOGIN-017..024`, phủ lần sai 1/2/3, request trong lock, 29 s, 31 s, reset sau hai lần sai và một lần sai sau reset. Các expected giữ đúng “+1, khóa 30 s” của FR-02 nên dự kiến phát hiện D-LOGIN-01 và D-LOGIN-02.

### API-1 / P4 — Security coverage

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:00:00+07:00`
- **Prompt:**

  > Chỉ sinh security cases áp dụng được cho login từ SEC-01..SEC-07: SQL injection ở từng credential, XSS/non-reflection, sensitive-field leakage, body role injection, khả năng dùng JWT trên protected endpoint và account-state disclosure. Expected là hành vi an toàn; nếu output lỡ mô tả tấn công thành công, giữ nguyên để Human Audit gắn INVALID.

- **Output:** Sinh 8 case `TC-API-LOGIN-025..032`. Một output sai có chủ đích giữ nguyên lịch sử: case 025 ghi “SQLi bypass thành công”; audit phải sửa thành `401` vì query thực tế parameterized. Cases 028/029 nhắm trực tiếp D-LOGIN-03; case 032 nhắm D-LOGIN-07.

### API-1 / P5 — Schema validation

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:01:00+07:00`
- **Prompt:**

  > Chỉ sinh schema cases cho nhánh success và invalid credential của login. Kiểm tra required fields, JSON content type, kiểu dữ liệu và negative schema cho field nhạy cảm. Không tự bịa cấu trúc `user`; mọi điểm chưa được API spec định nghĩa phải được nêu để audit.

- **Output:** Sinh 4 case `TC-API-LOGIN-033..036`: minimal success schema, JSON content type, error schema và extra-field rule. AI đã diễn đạt quá mạnh ở 033/035/036 vì API spec không công bố exact `user`/error schema; bước audit hạ thành contract tối thiểu + negative sensitive fields.

### API-1 / Audit — Gắn nhãn và sửa output

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:01:04+07:00`
- **Prompt:**

  > Audit từng dòng trong 36 case vừa sinh bằng bốn oracle: FR-02/SEC, API spec, mã nguồn login và defect catalog. Với từng case gắn đúng một nhãn VALID/INVALID/INCOMPLETE, giải thích cụ thể, và viết bản sửa cho mọi INVALID/INCOMPLETE. Không đổi expected theo hành vi lỗi hiện tại. Chừa checkpoint để sinh viên tự review và ký.

- **Output:** Audit đủ `36/36`: `28 VALID`, `3 INVALID`, `5 INCOMPLETE`. Tám bản sửa cụ thể dành cho cases 007, 008, 009, 015, 025, 033, 035, 036. Toàn bộ bảng và worksheet ký xác nhận nằm ở `api-01-login/02-audit.md`.

### API-1 / Human review checkpoint — Xác nhận của người học

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:28:46+07:00`
- **Prompt của người học:** `Đã duyệt API-1`
- **Output:** Ghi nhận worksheet đã được người học tự tick đủ ba checkpoint, điền tên `Đặng Đăng Khoa`, MSSV `23127207`, thời gian review `10:25 19-08-2026` và xác nhận “Đã duyệt”. Quy trình được phép chuyển sang bước Extend.

### API-1 / Extend — Bổ sung case AI bỏ sót

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:31:00+07:00`
- **Prompt:**

  > Sau khi Human Audit hoàn tất, hãy thiết kế tối thiểu 5 test case mới mà output AI ban đầu bỏ sót, ưu tiên security và state transition. Mỗi case phải chỉ rõ precondition, dữ liệu, expected theo đặc tả, bug mục tiêu và một nguyên nhân cụ thể thuộc chất lượng prompt, giới hạn model hoặc đặc thù API.

- **Output:** Bổ sung 6 case `TC-API-LOGIN-037..042`: khóa sớm sau hai lần sai, timeout thực 35 giây, negative sensitive-field schema, JWT expiration, residual state sau hết khóa và JWT forgery từ hard-coded secret. Kết quả đầy đủ ở `api-01-login/03-extended.md` và được hợp nhất vào bảng chốt 42 case ở `api-01-login/test-cases.md`.

### API-2 / P1 — Phân tích input, state và luồng checkout

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:36:04+07:00`
- **Prompt:**

  > Đối chiếu `POST /api/checkout` với FR-08, FR-10, API specification và mã nguồn SUT. Chưa sinh test case. Liệt kê mọi input/header, kiểu dữ liệu, tính bắt buộc, các partition có ý nghĩa; sau đó mô hình hóa state của Authorization, giỏ hàng và đơn hàng. Phân biệt rõ invariant “tổng tiền tính từ giỏ”, “giỏ bị xóa sau checkout”, “đơn mới pending” với assumption chưa được API spec định nghĩa.

- **Output:** Nhận diện `Authorization`, `total_amount`, `shipping_address`, giỏ hàng, đơn hàng và các trạng thái có/không có item; bảng input/state được ghi ở `api-02-checkout/01-ai-generated.md`.

### API-2 / P2 — Domain partition và boundary value

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:36:18+07:00`
- **Prompt:**

  > Dựa trên bảng input P1, áp dụng Equivalence Partitioning và Boundary Value Analysis cho từng tham số của `POST /api/checkout`. Sinh case độc lập cho total bằng 0, âm, chuỗi, null, thiếu, số thực, rất lớn, ký hiệu khoa học; shipping address rỗng, thiếu, Unicode, rất dài, XSS và SQLi. Expected phải bám FR/API spec; nếu spec chưa quy định status thì đánh dấu assumption để Human Audit sửa.

- **Output:** Sinh 18 case `TC-API-CHECKOUT-001..018`, phủ partition/type/BVA của total và shipping address. Các assumption về giới hạn địa chỉ, field thừa và status auth được giữ nguyên để audit.

### API-2 / P3 — State-transition và hậu điều kiện

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:36:32+07:00`
- **Prompt:**

  > Chỉ sinh state/flow cases cho checkout dựa trên FR-08/FR-10: no-token → rejected, cart có item → checkout → order pending, cart phải rỗng sau success, cart rỗng phải bị từ chối, identity lấy từ token, và luồng checkout → my-orders. Ghi rõ mọi endpoint kề bên được gọi để kiểm tra post-condition; không dùng orderId/userId hard-code.

- **Output:** Sinh 8 case `TC-API-CHECKOUT-019..026`, gồm pending, cart cleanup, empty cart, chained my-orders, user identity và double-submit. Case idempotency được đánh dấu assumption vì API spec chưa cam kết.

### API-2 / P4 — Security coverage

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:36:46+07:00`
- **Prompt:**

  > Với `POST /api/checkout`, sinh security cases cho SEC-02/SEC-04: thiếu JWT, JWT sai chữ ký/hết hạn, token user khác, không thể giả mạo user_id, IDOR khi đọc `GET /api/orders/:id`, SQLi/XSS trong shipping_address và không phản chiếu payload. Expected phải là hành vi an toàn theo đặc tả, không mô tả tấn công thành công.

- **Output:** Sinh 6 case `TC-API-CHECKOUT-027..032`. Các case đọc order qua endpoint liền kề được giữ để Human Audit đánh giá phạm vi, vì đây là nguồn D-CHK-07 bị AI dễ bỏ sót.

### API-2 / P5 — Schema validation

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:37:00+07:00`
- **Prompt:**

  > Sinh schema cases cho cả nhánh success và reject của checkout: Content-Type JSON, `message` là string, `orderId` là số nguyên dương, status đơn là pending, không lộ field nhạy cảm và không dùng exact-schema assertion cho field mà API spec chưa công bố. Gắn mỗi case với expected status/body.

- **Output:** Sinh 4 case `TC-API-CHECKOUT-033..036`, trong đó output thô cố tình giữ một expected sai `orderId:string` để Audit phát hiện và sửa thành integer.

### API-2 / Audit — Gắn nhãn và sửa output

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:37:18+07:00`
- **Prompt:**

  > Audit từng dòng trong 36 case checkout bằng FR-08/FR-10, API specification, mã nguồn `server.js` và defect catalog §2. Gắn đúng một nhãn VALID/INVALID/INCOMPLETE, giải thích cụ thể và viết expected sửa cho mọi case INVALID/INCOMPLETE. Không đổi expected theo hành vi lỗi của SUT; chừa checkpoint HUMAN trước khi sang API-3.

- **Output:** Audit đủ 36 case với `28 VALID`, `3 INVALID`, `5 INCOMPLETE`. Các sửa chính gồm: total phải tính từ giỏ, token invalid trả 403 theo middleware, empty/negative total là lỗi theo nghiệp vụ, orderId là integer và các assumption về shipping/idempotency được hạ thành robustness check. Bảng đầy đủ ở `api-02-checkout/02-audit.md`.

### API-2 / Human review checkpoint — Xác nhận của người học

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:41:44+07:00`
- **Prompt của người học:** `Đã duyệt API-2`
- **Output:** Ghi nhận người học đã tick đủ checkpoint, điền `Đặng Đăng Khoa`, MSSV `23127207`, thời gian review `10:40 19-08-2026` và xác nhận `Đã duyệt` trong `api-02-checkout/02-audit.md`. Có thể chuyển sang Extend và API-3.

### API-2 / Extend — Bổ sung case AI bỏ sót

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:42:00+07:00`
- **Prompt:**

  > Sau khi Human Audit API-2 được duyệt, thiết kế tối thiểu 5 case mà AI bỏ sót, ưu tiên bất biến xuyên endpoint, hậu điều kiện giỏ hàng, empty-cart, IDOR endpoint kề bên và XSS persistence. Mỗi case phải có precondition, dữ liệu, expected theo đặc tả, bug mục tiêu và nguyên nhân cụ thể thuộc chất lượng prompt, giới hạn model hoặc đặc thù API.

- **Output:** Bổ sung 6 case `TC-API-CHECKOUT-037..042`, nhắm D-CHK-01/02/03/04/05/07. Bảng và lý do cụ thể nằm ở `api-02-checkout/03-extended.md`, sau đó hợp nhất vào bảng 42 case ở `api-02-checkout/test-cases.md`.

### API-3 / P1 — Phân tích input và state machine đơn hàng

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:44:29+07:00`
- **Prompt:**

  > Đối chiếu `PUT /api/admin/orders/:id/status` với FR-10, FR-12, FR-18, API specification và mã nguồn SUT. Chưa sinh test case. Liệt kê mọi input/header/path parameter, role requirement và dựng state machine đầy đủ với 5 trạng thái pending, confirmed, shipping, delivered, canceled. Bắt buộc ghi 25 ô chuyển đổi 5×5, kể cả self-transition và transition terminal.

- **Output:** Nhận diện `Authorization`, `:id`, `status`, yêu cầu role admin và tạo ma trận 25 ô theo thứ tự 5 trạng thái. Mô hình được ghi ở `api-03-admin-order-status/01-ai-generated.md`.

### API-3 / P2 — Domain partition và boundary value

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:44:43+07:00`
- **Prompt:**

  > Từ input model P1, sinh domain/BVA cases riêng cho `:id` không tồn tại, âm, chuỗi không số, body thiếu status, status sai kiểu và status sai casing. Expected phải theo contract; nếu API spec chưa quy định 400/404 cụ thể thì đánh dấu incomplete thay vì tự bịa.

- **Output:** Sinh `TC-API-ORDER-STATUS-026..030`; giữ boundary `id` và type-confusion của status thành các case độc lập để không che lấp lỗi state transition.

### API-3 / P3 — Ma trận state transition 5×5

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:44:57+07:00`
- **Prompt:**

  > Sinh đúng 25 test case, mỗi ô một case, cho ma trận từ mọi trạng thái [pending, confirmed, shipping, delivered, canceled] đến mọi trạng thái đích. Expected lấy từ FR-10: pending→confirmed/canceled, confirmed→shipping/canceled, shipping→delivered/canceled; delivered và canceled là terminal; mọi ô còn lại trả lỗi. Không được bỏ qua self-transition hoặc terminal transition.

- **Output:** Sinh `TC-API-ORDER-STATUS-001..025`. Hai ô được giữ nguyên chênh lệch hiện thực để audit phát hiện: shipping→canceled bị SUT từ chối (D-ADM-03), canceled→delivered được SUT cho phép (D-ADM-02).

### API-3 / P4 — Security coverage

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:45:11+07:00`
- **Prompt:**

  > Với endpoint admin, sinh security cases cho SEC-02/SEC-03: thiếu JWT, JWT sai chữ ký, user token gọi admin endpoint, user A sửa order của user B và không thể role escalation. Expected phải yêu cầu JWT hợp lệ + role=admin, không mô tả hành vi SUT hiện tại như oracle đúng.

- **Output:** Sinh `TC-API-ORDER-STATUS-031..034`. Case user token được giữ expected AI sai “200” để Human Audit gắn INVALID và nhắm D-ADM-01.

### API-3 / P5 — Schema validation

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:45:25+07:00`
- **Prompt:**

  > Sinh schema cases cho success/error của status endpoint: Content-Type JSON, message/error là dữ liệu an toàn, status code đúng nhánh và không lộ secret. Không ép exact response fields khi API spec chưa công bố; phải phân biệt phần contract chắc chắn với negative security assertion.

- **Output:** Sinh `TC-API-ORDER-STATUS-035..038`; các assumption exact-response được gắn INCOMPLETE, còn Content-Type được giữ thành VALID.

### API-3 / Audit — Gắn nhãn và sửa output

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:45:42+07:00`
- **Prompt:**

  > Audit 38 case API-3 bằng FR-10/FR-12/FR-18, API specification, mã nguồn `server.js` và defect catalog §3. Kiểm tra đủ 25 ô matrix, gắn VALID/INVALID/INCOMPLETE cho từng dòng, sửa mọi expected sai/thiếu và không điều chỉnh expected theo bug SUT. Chừa checkpoint HUMAN trước Postman.

- **Output:** Audit đủ `38/38`: `28 VALID`, `5 INVALID`, `5 INCOMPLETE`. Hai bug matrix là D-ADM-03 (shipping→canceled) và D-ADM-02 (canceled→delivered); D-ADM-01 được phát hiện ở security case user token. Bảng audit nằm ở `api-03-admin-order-status/02-audit.md`.

### API-3 / Agent pre-review — Kiểm tra nhất quán trước automation

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T10:46:00+07:00`
- **Prompt:**

  > Tự rà soát bảng audit API-3 sau khi chưa có Human sign-off: đếm đủ 25 ô matrix và 38 case, kiểm tra mỗi case có đúng một nhãn, mọi INVALID/INCOMPLETE có action sửa, và không chuyển expected sang hành vi lỗi của SUT. Không ký thay Human.

- **Output:** Pre-review đạt các kiểm tra số lượng/nhãn/coverage; giữ nguyên khu vực Human sign-off chưa điền trong `api-03-admin-order-status/02-audit.md`.

### T-10 / Mở rộng độ phủ thực thi và đối soát Newman

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T14:41:48+07:00`
- **Prompt:**

  > Đọc execution plan/checklist, đối chiếu 128 test case với TC ID xuất hiện trong mọi Newman JSON, mở rộng Postman DDT để thực thi tối thiểu 90%, giữ expected theo oracle, phân loại rõ Automated/Manual/Blocked và chỉ cập nhật số liệu báo cáo từ JSON chạy thật. Không tạo hoặc sửa screenshot HUMAN-only.

- **Output:** Viết `tooling/coverage_report.py` làm coverage gate; mở rộng DDT thành 39 login, 41 checkout và 43 order-status assertions. Sau khi cô lập user/state và chạy lại trên backend sạch, Newman JSON chứng minh `123/128 = 96.1%` case đã thực thi, gồm 76 PASS và 47 FAIL theo oracle; cả ba DDT report có 0 request/script failure. Năm case không tự động hóa được được ghi rõ 1 Manual và 4 Blocked cùng lý do trong ba bảng `test-cases.md`.

### T-11 / Chạy CI thật và kiểm chứng off xanh — canary đỏ

- **Tool:** OpenAI Codex (GPT-5 Codex), GitHub CLI và GitHub Actions
- **Date & time:** `2026-08-19T15:07:39+07:00`
- **Prompt:**

  > Push branch `HW6-Khoa`, chạy workflow thật ở `SPEC_STRICT=off` đến khi xanh sạch; sau đó đổi đúng một dòng sang `canary`, yêu cầu run đỏ chỉ vì `TC-API-LOGIN-018`. Lấy SHA/URL bằng `gh run list`/`gh run view`; không dùng lỗi dependency, timeout hoặc port làm bằng chứng đỏ theo thiết kế; không tạo screenshot HUMAN-only.

- **Output:** Hai run đầu `#32230292930` và `#32230485958` bị loại vì Newman chưa chạy do lockfile backend. Sau khi tái sinh lockfile bằng npm 10 và xác nhận `npm ci`, run `off` [#32230928127](https://github.com/trngnneee/eshop-sut/actions/runs/32230928127) tại SHA `4bf4e5f812b02ca4adf2a0cb811b3a4edbad5bb0` xanh với 19 requests, 18 assertions, 0 fail. Đổi duy nhất `SPEC_STRICT` sang `canary` tạo run [#32231020920](https://github.com/trngnneee/eshop-sut/actions/runs/32231020920) tại SHA `03f36993b7766d79d605ee3e334201762bfc5f80`: 19 requests, 19 assertions, đúng 1 fail là `[SPEC] TC-API-LOGIN-018` (expected 200, actual 403). Mọi bước hạ tầng còn lại thành công; hai screenshot CI vẫn được ghi rõ HUMAN-only, chưa có.

### T-12 / Tách ghi chú AI khỏi sơ đồ HUMAN-only

- **Tool:** OpenAI Codex (GPT-5 Codex)
- **Date & time:** `2026-08-19T15:10:00+07:00`
- **Prompt:**

  > Di chuyển Mermaid do AI sinh ra khỏi vị trí sơ đồ nộp bài, ghi rõ provenance và không dùng nó để tạo ảnh. Chỉ chuẩn bị drawing brief về các khối/quan hệ bắt buộc để người học tự quyết định và tự vẽ `diagram.png` theo R-16; không tạo, chỉnh sửa hoặc mô phỏng diagram HUMAN-only.

- **Output:** Chuyển nội dung cũ sang `test-generator/_reference/diagram-notes.mmd` với cảnh báo “Đây là ghi chú tham khảo do AI sinh, KHÔNG phải sơ đồ nộp bài.”; xoá `test-generator/diagram.mmd`; thêm `DRAWING-BRIEF.md` mô tả bảy nhóm khối, quan hệ, vòng audit và gợi ý công cụ. `design.md`, README và main report đều ghi `diagram.png` là HUMAN-only, hiện chưa có.

### T-13 / Chuẩn hoá module label của GitHub Issues

- **Tool:** OpenAI Codex (GPT-5 Codex) và GitHub CLI
- **Date & time:** `2026-08-19T15:14:00+07:00`
- **Prompt:**

  > Đọc label thật của issues #413–#427, bảo đảm mỗi issue có đúng một label `module:` theo Rule H.7; thay `module:checkout` sai định dạng và bỏ `module: api` dư ở issue checkout. Không sửa screenshot và đồng bộ manifest từ trạng thái GitHub sau khi sửa.

- **Output:** Kiểm kê cho thấy #418–#421 có đồng thời `module:checkout` và `module: api`. Tạo label canonical `module: checkout`, thay hai label cũ trên đúng bốn issue này. Xác minh lại cả 15 issue: #413–#417 có đúng `module: api`, #418–#421 có đúng `module: checkout`, #422–#427 có đúng `module: orders`; mọi issue có đúng một module label. `report/github-issues.json` được cập nhật thành mảng label cụ thể thay cho marker `existing`; không tạo hoặc sửa screenshot.
