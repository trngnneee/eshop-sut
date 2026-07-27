# EShop — Báo cáo Đánh giá Usability (Task 2)

Đánh giá usability dạng moderated, mẫu nhỏ (7 người tham gia, think-aloud), trên một flow end-to-end của frontend-web (`localhost:5173`).

**Flow được chọn (U-01):** Đăng ký tài khoản mới → tìm sản phẩm → xem chi tiết → thêm vào giỏ (tổng ≥ 300.000₫) → thanh toán áp mã `SAVE10` → xác nhận đơn trong Lịch sử đơn hàng.
FR phủ: FR-01, FR-05, FR-06, FR-07, FR-08, FR-09, FR-11.

---

## 1. Mục tiêu nghiên cứu

### 1.1. Cách xây dựng

Dùng AI đề xuất 6 mục tiêu ứng viên, với input là flow U-01 và các bug Task 1 đã tìm thấy trên chính các màn thuộc flow (BUG-11, 12, 16, 17, 20, 33, 34, 35, 36, 38, 42, 44, 46, 47 — xem `../bug-report.md`). Sau đó em tự chọn 3 mục tiêu chính thức và tự viết lý do chọn/loại dưới đây.

### 1.2. Sáu mục tiêu ứng viên (tóm tắt)

| ID | Câu hỏi nghiên cứu (rút gọn) | Bằng chứng ở bước | Gốc từ Task 1 | Chọn? |
|---|---|---|---|---|
| O1 | Người dùng có tự hiểu và tự sửa được lỗi validation của form Đăng ký không, hay phải thử mò/bỏ cuộc? | Đăng ký | BUG-11, 12, 33, 34, 46 | ✅ |
| O2 | Người dùng có nhận ra thao tác thêm giỏ đã thành công chưa? Họ tự xác nhận bằng cách nào (bấm lặp → trùng hàng, hay mở giỏ kiểm tra)? | Chi tiết sản phẩm → Giỏ | BUG-16, 17, 47 | ✅ |
| O3 | Người dùng có tự tìm ra chỗ nhập mã SAVE10 và xác định được giảm giá đã trừ vào tổng chưa? | Checkout | BUG-44 | ❌ |
| O4 | Sau thanh toán, người dùng có tin đơn đã ghi nhận không, dựa vào dấu hiệu nào? | Sau checkout → Lịch sử đơn | BUG-20 | ❌ |
| O5 | Người dùng có bị lạc khi di chuyển giữa các màn của flow không? | Toàn flow (điểm chuyển màn) | BUG-35, 36, 38 | ❌ |
| O6 | Người dùng có dùng tìm kiếm để đạt mục tiêu mua hàng (giỏ ≥ 300k) không, và phản ứng thế nào khi tìm kiếm trả 0 kết quả không có empty state? | Tìm kiếm / Danh sách | BUG-42, 28 | ✅ |

### 1.3. Mục tiêu chính thức: O1, O2, O6 — lý do chọn

**Chọn O1 — vì Đăng ký là cổng vào bắt buộc của flow và là nơi Task 1 tìm thấy cụm lỗi dày nhất có khả năng chặn người dùng thật.** Regex số điện thoại từ chối số VN hợp lệ bắt đầu bằng 0 (BUG-11) và quy tắc mật khẩu mâu thuẫn với hint (BUG-12) nghĩa là gần như mọi participant sẽ va vào validation ít nhất một lần — session nào cũng chắc chắn sinh dữ liệu cho mục tiêu này. Quan trọng hơn, câu hỏi "họ có tự phục hồi được không" trả lời trực tiếp trục **error recovery** mà đề bắt buộc probe questions phải phủ, nên dữ liệu quan sát và dữ liệu phỏng vấn sẽ đối chiếu được với nhau.

**Chọn O2 — vì đây là vấn đề chỉ usability testing mới đo được, checklist Task 1 không đo nổi.** Task 1 xác nhận *hệ thống* không có feedback khi thêm giỏ (BUG-16) và nuốt click đầu tiên (BUG-17), nhưng không trả lời được *người dùng thật* phản ứng ra sao: có bấm lặp dẫn tới trùng hàng (BUG-47) không, có mất niềm tin không, có tự mở giỏ kiểm tra không. Hành vi này quan sát được trực tiếp và đếm được (số lần bấm, hành động xác minh) trong khuôn khổ 15–25 phút, rất hợp cỡ mẫu n=7 — tín hiệu định tính rõ mà không cần thống kê.

**Chọn O6 — vì tìm kiếm là bước duy nhất trong flow mà hành vi người dùng hoàn toàn tự do, nên cho dữ liệu tự nhiên nhất.** Scenario goal-oriented (không chỉ dẫn từng bước) khiến mỗi participant tự chọn từ khoá, tự quyết duyệt hay tìm — cách họ xoay xở khi kết quả trống trơn không một dòng giải thích (BUG-42) là phép thử trực tiếp cho trục **clarity**. Ngoài ra O6 bao luôn cơ chế ngân sách của scenario (gom giỏ đủ 300k để mã SAVE10 hợp lệ), giúp phát hiện sớm nếu scenario thiết kế ngưỡng tiền chưa hợp lý — điều cần biết ngay từ pilot.

**Tính phủ:** O6 (vào flow) → O1 (cổng đăng ký) → O2 (giữa flow) — ba mục tiêu nằm ở ba đoạn khác nhau, không dồn vào một màn, mỗi session đều đi qua cả ba nên không mục tiêu nào bị đói dữ liệu.

### 1.4. Lý do loại O3, O4, O5

- **O4 (niềm tin đơn đã ghi nhận):** bản chất trùng với trục **trust** mà probe questions bắt buộc phải hỏi — nghĩa là dữ liệu cho O4 *vẫn được thu* ở phần phỏng vấn cuối session mà không cần dành suất mục tiêu chính. Chọn O4 làm mục tiêu riêng sẽ đo trùng hai lần cùng một thứ.
- **O3 (coupon):** cùng họ "hệ thống có xác nhận hành động không" với O2 — giữ cả hai thì hai mục tiêu chồng lấn. Bước nhập SAVE10 vẫn nằm trong template ghi chú quan sát (cột riêng cho bước Checkout), nên friction ở coupon vẫn được ghi nhận như dữ liệu thứ cấp và vẫn có thể thành finding/bug ở GĐ8.
- **O5 (wayfinding):** hiện tượng phân tán khắp flow, khó quy bằng chứng về một bước cụ thể trong session 15–25 phút; với n=7, tín hiệu dễ bị nhiễu bởi khác biệt kinh nghiệm web giữa từng người. Các biểu hiện lạc đường nếu xảy ra vẫn lọt vào cột "Lỗi & do dự quan sát được" của template ghi chú.

---

## 2. Task scenario

Kịch bản goal-oriented (mua quà sinh nhật là tai nghe chống ồn, ngân sách 6–7 triệu, có mã `SAVE10` "nhận qua email", tự xác nhận đơn đã ghi nhận trước khi rời đi) — toàn văn + bảng mapping scenario → 6 bước flow trong `task-scenario-draft.md`. Ba quyết định thiết kế chính:

- **Không chứa bất kỳ chỉ dẫn giao diện nào** (đã kiểm tra danh sách từ cấm: nút, menu, trang, click...) — participant chỉ nhận goal và động cơ.
- **Ngân sách neo vào dữ liệu thật:** catalog seed chỉ có 5 sản phẩm, rẻ nhất 4.000.000₫, nên kiểu ngân sách "dưới 500k" như ví dụ trong đề là bất khả thi; 6–7 triệu trỏ tự nhiên tới AirPods Pro 2 (6.000.000₫), đồng thời ngưỡng 300k của `SAVE10` luôn tự thoả.
- **"Hoàn thành" định nghĩa theo góc nhìn người dùng** (yên tâm đơn đã được ghi nhận), không theo bước kỹ thuật — để quan sát họ tự tìm bằng chứng ở đâu.

## 3. Công cụ đo (instruments)

- **Thang đo: SUS** (bản dịch tiếng Việt trong `template/sus-form-vi.md`, kèm bảng đối chiếu Anh–Việt để kiểm chứng độ trung thành và tính phân cực câu lẻ/chẵn). Em chọn SUS thay vì UEQ-S vì: 10 câu đủ ngắn cho session 15–25 phút, có quy trình chấm chuẩn tái lập được (0–100) và benchmark tham chiếu rộng rãi (68 = trung bình), phù hợp để báo cáo một con số tổng quát với n nhỏ.
- **Probe questions:** 7 câu mở trong `template/probe-questions.md`, phủ đủ 4 trục đề yêu cầu (clarity / error recovery / speed / trust) và bám O1/O2/O6; mỗi câu có bản gốc trung lập + câu đào sâu chỉ dùng khi chính em đã quan sát thấy tình huống trong session.
- **Session kit:** `template/session-kit.md` — kịch bản mở đầu đọc nguyên văn (test sản phẩm không test bạn, demo think-aloud, xin consent ghi màn hình + âm thanh), template ghi chú A4 theo 6 bước flow, cheat-sheet 5 câu trả lời trung lập và quy tắc can thiệp duy nhất (kẹt hẳn > 2 phút, gợi ý nhỏ nhất có thể, ghi lại nguyên văn).

## 4. Người tham gia

**Target user profile:** người 18–30 từng mua sắm online, không làm trong ngành kiểm thử phần mềm và không học lớp HW03 này.

7 người tham gia thật (bảng đầy đủ kèm liên hệ đã che 4 số giữa: `participants.md`), tuyển thủ công không qua AI theo đúng §11 của đề; tất cả đã được báo trước rằng TA có thể gọi điện xác minh. Mỗi người dùng tài khoản tự đăng ký trong chính session (bước đầu của flow), bảo đảm điều kiện `max_uses_per_user` của mã giảm giá không bị vướng giữa các session.

## 5. Chuẩn bị & pilot

Trước session đầu, em tự đi hết flow (dry-run) để xác nhận flow không gãy, ước thời lượng session và soát kịch bản/bảng mapping; DB được reset về seed trước mỗi session và toàn bộ 7 session dùng cùng một bộ tài liệu.

**Hạn chế cần khai rõ: nghiên cứu này không có pilot session với một người tham gia riêng** như đề khuyến nghị. Vai trò của pilot được bù một phần bằng dry-run nói trên và bằng việc rà lại quy trình sau session P1 trước khi tiếp tục — thực tế không session nào ghi nhận participant hiểu sai hoặc phải hỏi lại kịch bản, và bộ tài liệu giữ nguyên xuyên suốt nên 7 session so sánh được với nhau. Rủi ro tồn dư của việc thiếu pilot (nếu scenario có lỗi hệ thống thì lỗi đó lan cả 7 session) được ghi nhận ở mục 10.

## 6. Tiến hành 7 session

7 session diễn ra 21–24/07/2026, mỗi session 15–25 phút, theo đúng trình tự kit: đọc script mở đầu → consent → giao kịch bản → quan sát trung lập (think-aloud) → phiếu SUS → probe questions. Ghi chú được gõ lại trong vòng 15 phút sau mỗi session.

- Bằng chứng: ghi chú quan sát `result/session-P1..P7.md`, phiếu SUS `result/sus-P1..P7.md`, tổng hợp `result/README.md`.
- **Can thiệp:** đúng 2 lần, đều theo quy tắc kẹt-hẳn->2-phút và đều ở bước Đăng ký (P3, P6 — gợi ý tối thiểu "thử bỏ số 0 ở đầu số điện thoại", ghi nguyên văn trong note). Ngoài ra chỉ dùng câu trung lập trong cheat-sheet.
- 7/7 hoàn thành flow (5/7 hoàn toàn độc lập).

## 7. Kết quả SUS

Chấm bằng script tái lập được (`result/sus_score.py` trên `result/sus_responses.csv` — công thức chuẩn: câu lẻ điểm−1, câu chẵn 5−điểm, tổng ×2.5), kết quả khớp 7/7 với bản chấm tay trên phiếu:

| P1 | P2 | P3 | P4 | P5 | P6 | P7 | **Mean** | Median | Min–Max |
|---|---|---|---|---|---|---|---|---|---|
| 67.5 | 57.5 | 30.0 | 52.5 | 55.0 | 35.0 | 75.0 | **53.2** | 55.0 | 30.0–75.0 |

Mean 53.2 nằm dưới benchmark trung bình 68, band "OK" theo thang tính từ Bangor et al. Với n=7 đây là tín hiệu định tính, không phải kết luận thống kê; điểm đáng chú ý là 2 điểm thấp nhất (P3: 30, P6: 35) chính là 2 ca cần can thiệp ở bước Đăng ký — thang đo và quan sát hành vi kể cùng một câu chuyện.

## 8. Findings & mức độ nghiêm trọng

Phân tích đầy đủ (9 theme UF-01→09 + 3 phát hiện hệ thống SYS-01→03, kèm căn cứ từng dòng và tần suất x/7) trong `findings.md`. Tóm tắt xếp theo severity:

| ID | Finding | x/7 | Severity | Bug/Design |
|---|---|---|---|---|
| UF-01 | Validation SĐT từ chối số VN hợp lệ — 2 ca kẹt hẳn phải trợ giúp | 7/7 | **Blocker** | Bug (#204) |
| UF-02 | Thêm giỏ không feedback + click đầu bị nuốt | 7/7 | Major | Bug (#209, #210) |
| UF-03 | Bấm lặp tạo dòng trùng → P6 suýt thanh toán gấp đôi (10,8 triệu) | 2/7 | Major | Bug (#240) |
| UF-04 | Quy tắc mật khẩu mâu thuẫn hint | 7/7 | Major | Bug (#205) |
| UF-05 | Tìm kiếm 0 kết quả = trang trống không giải thích | 4/7 | Major | Bug (#235) |
| UF-06 | Giỏ không reset sau checkout → nghi ngờ giao dịch | 7/7 | Major | Bug (#213) |
| UF-07 | Thông báo lỗi form không actionable | 4/7 | Major | Design |
| UF-08 | Feedback bằng `alert()`, xác nhận giảm giá mờ nhạt | 2/7 | Minor | Design |
| UF-09 | Ô nhập coupon khó thấy | 1/7 | Cosmetic | Design |

**Trả lời mục tiêu nghiên cứu (chi tiết trong `findings.md` §3):** O1 — người dùng tự phục hồi được nhưng bằng thử-sai và kinh nghiệm nền, hệ thống gần như không đóng góp (chỉ P1 rút được hướng sửa từ thông báo lỗi; 2/7 cần trợ giúp). O2 — 0/7 nhận biết "đã thêm giỏ" qua hệ thống; hành vi bù đắp là tự mở giỏ (6/7); người không tự xác minh (P6) chính là người suýt mất tiền. O6 — tìm kiếm chỉ "hoạt động" với người biết luật ngầm từ-khoá-ngắn; 4/7 gõ tự nhiên rơi vào trang trống và không ai hiểu đúng là "0 kết quả".

## 9. Báo cáo bug

Cả 7 bug đều trùng gốc với issue đã mở ở Task 1, nên thay vì mở issue trùng, em bổ sung bằng chứng usability (tần suất x/7, trích think-aloud, hậu quả) thành comment vào từng issue và gắn label `usability`: [#204](https://github.com/trngnneee/eshop-sut/issues/204), [#205](https://github.com/trngnneee/eshop-sut/issues/205), [#209](https://github.com/trngnneee/eshop-sut/issues/209), [#210](https://github.com/trngnneee/eshop-sut/issues/210), [#213](https://github.com/trngnneee/eshop-sut/issues/213), [#235](https://github.com/trngnneee/eshop-sut/issues/235), [#240](https://github.com/trngnneee/eshop-sut/issues/240).

Dựa trên dữ liệu người dùng thật, 2 issue được nâng severity (giữ nguyên đánh giá gốc Task 1 trong body để truy vết): **#204 Major → Blocker** (chặn hoàn thành task với 2/7 người) và **#240 Minor → Major** (rủi ro thanh toán gấp đôi). Comment công khai chỉ dùng mã P1–P7, không chứa thông tin cá nhân.

## 10. Hạn chế

1. **Không có pilot session riêng** (mục 5) — rủi ro lỗi hệ thống của scenario lan cả 7 session; giảm nhẹ bằng dry-run + checkpoint sau P1, nhưng vẫn là thiếu sót so với quy trình chuẩn của đề.
2. **n=7, mẫu đồng nhất** (đều là sinh viên) — kết quả là tín hiệu định tính; các con số x/7 không suy rộng được cho tập người dùng chung.
3. **Catalog chỉ 5 sản phẩm** — làm hành vi "duyệt thay vì tìm" trở nên hợp lý (P4), nên kết luận O6 về tìm kiếm sẽ cần kiểm chứng lại với catalog lớn.
4. Kết quả SUS chịu ảnh hưởng mạnh của cụm lỗi Đăng ký nằm ngay đầu session (hiệu ứng ấn tượng đầu).

## 11. AI Critique (200–300 từ)

Em dùng AI ở hai đầu của nghiên cứu - thiết kế công cụ trước session và tổng hợp sau session - và không dùng trong lúc thu dữ liệu: tuyển người, điều phối, ghi chú quan sát và phiếu SUS đều làm thủ công theo đúng ranh giới của đề. Nhìn lại 9 artifact đã audit (Appendix A - AI Audit Report), chỉ 1 được chấp nhận nguyên trạng, 8 phải sửa mới dùng được: "AI làm ra được" không đồng nghĩa "dùng được ngay".

AI mạnh nhất ở hai chỗ. Một là dựng công cụ có ràng buộc kiểm chứng được: scenario không chứa từ chỉ dẫn giao diện, bản dịch SUS giữ đúng phân cực câu lẻ/chẵn, session kit chuẩn hoá cả 7 session - nhưng em vẫn phải soát từng ràng buộc (đối chiếu từng câu SUS với bản gốc Brooke, rà từ cấm) chứ không tin theo lời AI tự nhận. Hai là code tất định: script chấm SUS khớp 7/7 với bản chấm tay.

Điểm yếu đáng học nhất nằm ở bước tổng hợp: 3 con số thống kê trong bản nháp findings lệch khỏi ghi chú gốc, và cả 3 đều lệch về hướng làm câu chuyện gọn hơn - kể cả khẳng định "không ai rút được cách sửa từ thông báo lỗi" trong khi chính dữ liệu đó có P1 là ngoại lệ. Đây không phải lỗi ngẫu nhiên mà là thiên kiến kể-chuyện-mạch-lạc, và chỉ bị bắt nhờ đếm lại từng dòng theo `session-P*.md`. Em cũng không nghe theo AI ở một quyết định triage: giữ #235 ở Minor thay vì nâng Major như AI đề xuất, vì cả 4/7 người gặp đều tự thoát được bằng đổi từ khoá.

Quy tắc em rút ra: để AI nháp cấu trúc và văn bản, nhưng mọi con số phải truy vết được về dữ liệu thô và phải tự suy ra lại trước khi chấp nhận; các quyết định đánh giá (severity, khai hạn chế thiếu pilot) luôn thuộc về người làm nghiên cứu.
