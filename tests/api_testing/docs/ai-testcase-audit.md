# Bước 3 — Review lại đống test case AI sinh (VALID / INVALID / INCOMPLETE)

**Họ và tên:** Đặng Trường Nguyên

**MSSV:** 23127438

**Ngày:** 22/08/2026

Sau khi AI sinh xong 212 test case ở Bước 2 (API-1: 83, API-2: 57, API-3: 72), em ngồi kiểm tra lại từng cái. Đại khái với mỗi case em tự hỏi 3 thứ: expected có bám **contract** (FR + `openapi.yaml`) hay bị AI lấy theo hành vi thật của SUT; assertion có cụ thể để chạy được không; và precondition/fixture có đủ chưa. Xong thì dán cho mỗi case một nhãn:

- **VALID** — xài được luôn. Kể cả mấy case *đúng nhưng chắc chắn sẽ FAIL* vì SUT làm sai spec — em cố tình giữ, vì đó chính là case bắt bug.
- **INVALID** — expected hoặc assertion sai, hoặc trùng case khác → phải sửa/bỏ.
- **INCOMPLETE** — ý thì đúng nhưng expected còn mơ hồ / thiếu payload / thiếu fixture → phải bồi thêm.

## Mấy lỗi AI hay mắc — em check thử coi bộ này có dính không

Cái này em bám theo checklist trong plan. Kết quả rà:

- **Tự bịa `201 Created` cho POST** — không dính. Mấy case tạo sản phẩm đều để `200` đúng như SUT (cả `POST /api/register` gốc cũng `200`).
- **Thấy `GET /products/99999` trả `200 {}` rồi hạ expected xuống `200` cho đỡ FAIL** — cũng không. TC-P1-007 và TC-P1-065 vẫn để `404` theo spec, chấp nhận nó FAIL (chính là BUG-02). Chỗ này em thấy AI làm đúng tinh thần nhất: expected là của spec, lệch thì ghi bug chứ không chiều theo code.
- **Viết "kiểm tra SQL injection" chung chung không payload** — không dính, nhóm SEC-05 đều có payload thật (`' OR '1'='1`, UNION SELECT...) kèm assertion đếm record + check không lộ HTML.
- **Quên fixture cho state `shipping`/`delivered`** — không, TC-O2-016→024 có nguyên chuỗi `checkout → admin đẩy status` cho từng state.
- **Test token hết hạn bằng token thật** — không, TC-O2-031 tự ký token `exp` quá khứ và có ghi chú là token thật của SUT không có `exp`.
- **Trùng case cho đủ số** — cái này **có dính 2 chỗ**, nói ở dưới.
- **Thiếu header `X-Student-Id`** — API-1 với API-2 có case rồi, riêng **API-3 quên**.

## Con số để đưa vào AI Critique

> **Lưu ý đơn vị đếm — đọc kỹ chỗ này để khỏi tưởng số bị lệch.** Bảng dưới đếm **theo từng test case** (đơn vị = 1 TC-ID, tổng 212). Còn bảng trong AI Audit Report (`ai_declaration/[AI-02]`, mục 3) đếm **theo artifact/prompt** (đơn vị = 1 lần AI sinh ra 1 file/artifact, tổng 16 artifact → 11 VALID / 5 INCOMPLETE). Hai bảng **khác đơn vị nên không so trực tiếp được**: một artifact "INCOMPLETE" ở AI-02 (vd cả file EP+BVA của API-1) bên trong vẫn gồm phần lớn test case VALID cộng vài case phải sửa. Khi viết AI Critique em sẽ nói rõ đang trích con số theo đơn vị nào (per-case ở đây, per-artifact ở AI-02), tránh để người chấm tưởng hai chỗ mâu thuẫn.

| API | Tổng | VALID | INVALID | INCOMPLETE | Trong đó VALID mà sẽ FAIL (lộ bug) |
|-----|------|-------|---------|------------|-------------------------------------|
| API-1 | 83 | 82 | 1 | 0 | ~25 (id strict → 400, BUG-01/02, SQLi thật, trả HTML) |
| API-2 | 57 | 56 | 0 | 1 | 10 (BUG-05, BUG-13 forge, HTML BUG-15) |
| API-3 | 72 | 68 | 1 | 3 | 39 (BUG-07/08/09/10/11/12) |
| **Tổng** | **212** | **206** | **2** | **4** | **~74** |

Tức khoảng **97%** dùng được ngay. Em nghĩ tỷ lệ cao vậy là vì em không bảo AI "sinh hết test case đi" mà dẫn từng kỹ thuật một, lại vừa sinh vừa mở server probe cURL luôn. Phần sai còn lại chủ yếu là expected để mơ hồ ở mấy input mà spec vốn không ràng buộc, với vài case trùng nhau giữa 2 file — không phải sai về tư duy test.

## Mấy case em phải gắn cờ

| TC-ID | Verdict | Sai ở đâu | Em sửa thành |
|-------|---------|-----------|--------------|
| __TC-P1-044__ | __INVALID__ | Expected ghi "array 3 — dùng giá trị đầu `Pro`" là sai bét. `?search=Pro&search=Mac` bị Express gom thành mảng `['Pro','Mac']`, rồi nội suy vô chuỗi thành `%Pro,Mac%` ⇒ ra __0 kết quả__, chứ không phải lấy giá trị đầu. | Expected `200` + `body.length === 0`, không khớp product nào. Đây đúng là __BUG-18__ (search lặp → 0 kết quả im lặng). Bỏ luôn cái "array 3". |
| __TC-P3-048__ | __INVALID (trùng)__ | Y hệt __TC-P3-057__: cùng test mass-assign `id`/`role` trên `POST`, cùng expected `200`, cùng assert `id ≠ 999`. Để 2 cái là đếm gian. | Bỏ TC-P3-048, giữ 057 (057 còn bao thêm `is_admin`). Muốn giữ cả 2 thì phải cho nó test vector khác hẳn. |
| __TC-O2-015__ | __INCOMPLETE (trùng ý)__ | Trùng ý __TC-O2-036__ — cùng nhét `{"status":"delivered"}` vô đơn `pending`, cùng assert `status` cuối là `canceled`. | Gộp lại, lấy TC-O2-036 làm case mass-assign chính. Nếu tiếc thì đổi 015 sang "body thừa field lạ khác ngoài `status`" cho khác biệt. |
| __TC-P3-017__ | __INCOMPLETE__ | Expected để `400/200` (price cực lớn) — mơ hồ. Mà FR-15 với cột `price INTEGER` có đặt trần đâu, nên đòi `400` là không có căn cứ. | Chốt `200`, assert lưu đúng số; ghi observation "spec không giới hạn trên cho price". |
| __TC-P3-027__ | __INCOMPLETE__ | Expected `200/400` (imageUrl sai format) — FR-15 không hề ràng buộc URL. | Chốt `200`, assert lưu nguyên văn, ghi observation. |
| __TC-P3-028__ | __INCOMPLETE__ | Expected `200/400` (imageUrl 5000 ký tự) mà không nói ngưỡng bao nhiêu thì assert kiểu gì. | Muốn khẳng định hành vi thì để `200` + assert lưu đủ; muốn test giới hạn thì phải nêu ngưỡng cụ thể trước. |

Còn mấy case expected cũng có chữ "hoặc" nhưng em **để nguyên VALID**: TC-P1-049/051/052 (`200` hoặc `500`-JSON) và TC-P3-032/034/046. Ở mấy cái này status có dao động thật, nhưng phần assert chính vẫn chặt (không trả HTML / không lộ credential / lưu nguyên văn / dữ liệu không bị đụng), nên "hoặc" ở đây là hợp lý chứ không phải làm ẩu.

## Vài thứ chung chung em nhặt được

- **API-3 thiếu case `thiếu X-Student-Id`.** API-1 (TC-P1-082) với API-2 (TC-O2-056) có rồi mà API-3 sót. Nên thêm 1 case kiểu `TC-P3-073`: `POST /api/products` không gửi `X-Student-Id` vẫn `200`, còn bằng chứng chấm bài thì nằm ở console của pre-request script.
- **Mấy case DELETE là destructive, phải dọn dẹp cho đàng hoàng.** TC-P1-078 xoá product 1, TC-P3-054 xoá product 5, TC-P3-055 xoá product 4 — xoá thật luôn. Em có đánh dấu `PRE-DESTRUCT` nhưng lúc ráp vô Postman Runner phải nhét mấy case này **xuống cuối folder** và re-seed lại, không thì mấy case sau đang tưởng có đủ 5 product sẽ chạy sai.
- **Cặp control `X-Student-Id` hơi thừa.** TC-P1-083 và TC-O2-057 (case "có gửi header") gần như trùng với happy-path gốc, gộp cũng được, không phải lỗi.
- **DEC-01 (id strict) em áp luôn cho API-2.** TC-O2-005/006/007/008 để expected `400` cho id `0/-1/abc/1.5` dù SUT trả `404`. Đây là em cho nhất quán với quyết định strict bên API-1, và ghi rõ nó là validation-gap/observation chứ không phải bug chức năng.

## Chốt lại

Nhìn chung bộ test AI sinh xài được ~97%, tốt hơn em tưởng — nhờ dẫn từng kỹ thuật với probe cURL song song. Em sửa 2 case INVALID (1 cái expected sai theo BUG-18, 1 cái trùng) và 4 case INCOMPLETE (3 cái expected mơ hồ vì spec không ràng buộc + 1 cái trùng ý), thêm mấy ghi chú về header với thứ tự chạy. Điểm em ưng nhất là AI không hạ expected xuống cho khớp SUT, nên ~74 case vẫn FAIL đúng chỗ và lộ trọn bộ bug BUG-01/02/05/07/08/09/10/11/12/13/18.

Việc cần làm để đồng bộ ngược lại vào file test case + `openapi.yaml`:

- [x] TC-P1-044 → expected `200` + array rỗng `[]`, map BUG-18 (đã sửa trong `API-1_TestCases.md`)
- [x] Bỏ TC-P3-048, gộp vào TC-P3-057 (dòng ~~gạch~~ + note trong `API-3_TestCases.md`)
- [x] TC-O2-015 → định vai lại: body field lạ (`user_id`/`total_amount`/`foo`) khác vector `status` của TC-O2-036
- [x] TC-P3-017/027/028 → chốt `200` + ghi **Observation** (spec không ràng buộc trần price / format & độ dài imageUrl)
- [x] Thêm TC-P3-073 (POST thiếu `X-Student-Id` → `200`, đối chứng TC-P1-082/TC-O2-056)
- [x] Thêm callout **Thứ tự chạy (Postman Runner)** cho DELETE destructive ở `API-1_Negative_Contract` & `API-3_Security` (chạy cuối folder + teardown re-seed)

---

> **Đã áp toàn bộ checklist vào file test case ngày 23/08/2026.** Không đổi tổng số case (212): TC-P3-048 gộp vào 057 nhưng bù bằng TC-P3-073. `openapi.yaml` đã có sẵn BUG-18 ở response `400` của `listProducts` nên không cần sửa thêm.
