# AI Critique — HW06: API Testing (EShop)

**Sinh viên:** Đặng Trường Nguyên

**MSSV:** 23127438 · **Ngày:** 23/08/2026

**Công cụ AI:** Claude Code (Claude Opus 5, 1M context)

> Bài phản tỉnh theo đề §10: _AI sai/thiên lệch/thiếu ở đâu? Vì sao nó không bắt được lỗi? Nguyên tắc gì em rút ra khi cộng tác với AI?_ Đối chiếu chi tiết verdict ở `ai_declaration/[AI-02] AI Audit Report` §3.

---

## 1. AI làm tốt ở đâu

AI mạnh ở **bề rộng cơ học của thiết kế hộp đen** — thứ tốn công nhưng theo luật:

- __Liệt kê lớp tương đương + giá trị biên__: với mỗi tham số (`:id`, `?search=`, `name/price/category_id`), AI tách bảng partition đầy đủ (valid/invalid/boundary) rồi mới sinh case — đúng quy trình EP/BVA của ISTQB, gần như không sót lớp.
- **State-transition**: dựng đúng bảng 0-switch 5 trạng thái đơn hàng và chuỗi fixture (checkout → admin đẩy state) khi được mô tả sơ đồ FR-10.
- **Schema/contract**: viết JSON Schema draft-07 chuẩn, cấu trúc OpenAPI 3.0.3 hợp lệ (Redocly 0 error), và bộ khung Postman v2.1.0 chạy được ngay.
- **Sinh khối lượng lớn nhất quán**: 219 test case + 238 request Postman + 20 bug report theo template — đồng đều về format, đặt tên, assertion.

⇒ Với phần *enumeration* và *boilerplate*, AI nhanh và đáng tin.

---

## 2. AI sai / thiên lệch / thiếu ở đâu (và VÌ SAO)

Mọi lỗi của AI đều có chung một gốc: **AI suy theo SPEC lý tưởng / REST convention, không suy theo IMPLEMENTATION thật.** Nó không "nhìn" được hành vi ẩn trong code.

| # | AI sai gì | Vì sao AI không bắt được | Ai phát hiện |
|---|-----------|--------------------------|--------------|
| 1 | Giả định endpoint admin (`POST/PUT/DELETE /api/products`) **đã có auth** → bỏ hoàn toàn **BUG-07** (thiếu middleware) | Spec ghi "CRUD dành cho Admin" nên AI *mặc định* đã enforce; không đọc được việc route **quên** `authenticateToken` | Tôi — đọc `server.js` + `curl` không token vẫn `200` |
| 2 | Không tưởng tượng được **`price` bị ép string khi `id` chẵn** (BUG-01) | Logic `if (row.id % 2 === 0)` là quyết định *tùy tiện của code*, không có trong spec — hộp đen không suy ra được | Tôi — so `curl /products/1` vs `/2` |
| 3 | Dự đoán **forged JWT → 403** (token giả bị từ chối) | AI suy theo bảo mật lý tưởng; không nối được "secret hardcode ở `server.js:9`" ⇒ chữ ký hợp lệ ⇒ `jwt.verify` PASS ⇒ `200` (escalation thật, BUG-13) | Tôi — tự sign token bằng secret lộ rồi gọi thật |
| 4 | Chỉ dừng ở SQLi tautology `' OR '1'='1'` để "chứng minh SQLi"; **không đi tới UNION** rút bảng `users` (BUG-20) | UNION cần biết **tên bảng + số cột** — thông tin chỉ có khi đọc `database.js`; prompt ban đầu chưa đưa | Tôi — đọc schema DB, dựng payload UNION 6 cột |
| 5 | Đặt **expected theo REST** (`201 Created`, `404`) không khớp SUT (dùng `200`) | Convention ≠ spec thật của SUT; AI ưu tiên "chuẩn REST" | Tôi — bám `200` theo `POST /api/register` của SUT |
| 6 | Từng đặt nhầm **expected `shipping→cancel` = 200** theo hành vi quan sát | Nếu lấy oracle từ implementation thì bug **tự ẩn**; phải ép về `400` theo FR-10 mới lộ BUG-05 | Tôi — chốt expected theo mô hình trạng thái |
| 7 | Ghi **`?search=%` → 0 kết quả** (coi `%` là literal) | Đúng theo spec, nhưng code nối chuỗi `'%%%'` ⇒ match tất cả (BUG-17); AI không thấy tầng SQL | Tôi — `curl` thấy trả cả 5 |
| 8 | Ban đầu ghi double-cancel song song "cả 2 đều 200" | Suy đoán về race mà không đo; thực đo `200`+`400` (SUT serialize) | Tôi — hạ xuống **observation**, không khẳng định bug |
| 9 | Đánh **số bug lệch** giữa `plan.md` và `openapi.yaml`/testcases | AI trộn 2 hệ đánh số từ 2 nguồn khác nhau | Tôi — yêu cầu **bỏ đánh số**, định danh bằng tiêu đề + TC-ID |

Ngoài ra, ở khâu OpenAPI, `docs/openapi-audit.md` ghi 5 mismatch (M1–M5) tôi tự sửa; rõ nhất là M2 (forged-token verdict).

---

## 3. Bản chất chung của các lỗi

- **Loại lỗi chi phối = [API characteristic]:** bug nằm trong *cách code triển khai* (parity `id%2`, secret hardcode, thiếu FK, thiếu middleware, không kiểm `this.changes`, nối chuỗi SQL). Đây là vùng **mù tuyệt đối** của black-box + spec-only.
- **[Model]:** AI test tuần tự, hiếm thử biến thể lạ (boolean cho trường số, đồng thời/race).
- **[Prompt]:** khi tôi **chưa đưa source** (`server.js`/`database.js`), AI không thể sinh case phụ thuộc implementation (UNION, IDOR endpoint liền kề). Khi tôi đưa source + ép "đừng sửa expected theo code", chất lượng tăng rõ.

---

## 4. Nguyên tắc rút ra khi cộng tác với AI

> **Con người sở hữu ORACLE — AI sở hữu ENUMERATION.**

1. **Để AI sinh không gian đầu vào và contract; TỰ mình quyết mọi expected** từ test basis (FR/OpenAPI/schema DB), không bao giờ từ hành vi quan sát của SUT.
2. **Xác minh mọi "actual" bằng execution thật** (cURL/Postman/Newman trên `localhost`), không tin output AI. Chính bước này lộ 20 bug — đặc biệt 8 bug Critical mà AI không thể suy từ spec.
3. **Đưa source cho AI đọc** và ra lệnh rõ ("đừng hạ expected cho khớp code") — chất lượng phụ thuộc mạnh vào prompt + ngữ cảnh.
4. **Cảnh giác với suy đoán không đo được** (race condition): nếu không tái hiện ổn định thì ghi *observation*, không khẳng định bug.
5. **AI để nhân số lượng, không để phán xét đúng/sai** — nhất là ở security và state-transition, nơi giá trị của bài kiểm thử nằm ở đúng chỗ AI yếu nhất.

---

## 5. Kết luận

AI rút ngắn đáng kể phần cơ học (enumeration, boilerplate, format), nhưng **toàn bộ 20 bug đều do tôi phát hiện/xác nhận bằng cách chạy SUT**, không phải do AI suy ra. Bài học cốt lõi cho các HW sau: dùng AI để **mở rộng độ phủ**, còn **oracle và bằng chứng thực thi phải do con người sở hữu** — đó cũng chính là điều ràng buộc Anti-AI-Cheat của môn học đang bảo vệ.
