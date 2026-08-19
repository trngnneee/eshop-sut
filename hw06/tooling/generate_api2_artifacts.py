"""Render the API-2 generation, audit, extension and final-case artifacts.

The case catalogue is intentionally explicit so every generated row can be
reviewed against the HW06 oracle.  It is a renderer, not an oracle: the
expected result is kept separate from the observed SUT result.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "api-02-checkout"


def c(
    number, group, title, pre, data, ai_expected, label, reason, action,
    final_expected, technique, run, bug="—",
):
    return {
        "id": f"TC-API-CHECKOUT-{number:03d}",
        "group": group,
        "title": title,
        "pre": pre,
        "data": data,
        "ai": ai_expected,
        "label": label,
        "reason": reason,
        "action": action,
        "final": final_expected,
        "technique": technique,
        "run": run,
        "bug": bug,
    }


CASES = [
    c(1, "Partition", "Checkout với giỏ có sản phẩm và total hợp lệ", "User có JWT; giỏ có một sản phẩm", "total_amount=200000; shipping_address='123 Le Loi'", "200; orderId và tổng đơn bằng 200000", "INVALID", "AI lấy total_amount từ client làm oracle, trái FR-08 yêu cầu tính lại từ giỏ.", "Sửa expected theo tổng thực của giỏ, không theo body.", "200; orderId là số nguyên; đơn có total theo giỏ; status=pending", "EP", "FAIL", "D-CHK-01"),
    c(2, "Partition", "Không có Authorization", "Giỏ không quan trọng", "Không gửi Authorization", "401; JSON error", "VALID", "FR-08 yêu cầu chỉ user đã đăng nhập mới checkout.", "Giữ nguyên.", "401; không tạo đơn", "EP", "PASS"),
    c(3, "Partition", "Authorization không có Bearer", "Không gửi request trước", "Authorization='abc'", "403; token malformed", "VALID", "Token có header nhưng không theo dạng Bearer được middleware coi là token không hợp lệ.", "Giữ nguyên.", "403; không tạo đơn", "EP", "PASS"),
    c(4, "Partition", "Token sai chữ ký", "Có token giả", "Authorization='Bearer invalid.signature.token'", "403", "VALID", "Theo middleware của SUT, token sai chữ ký trả 403; đây là nhánh invalid-token riêng với thiếu header.", "Giữ nguyên.", "403; không tạo đơn", "EP", "PASS"),
    c(5, "Partition", "total_amount bằng 0", "User có JWT; giỏ có sản phẩm", "total_amount=0; shipping_address='A'", "400; tổng phải dương", "VALID", "FR-08 không chấp nhận total do client; dữ liệu 0 phải bị từ chối theo invariant tổng đơn dương.", "Giữ nguyên.", "400; không tạo đơn", "BVA", "FAIL", "D-CHK-02"),
    c(6, "Partition", "total_amount âm", "User có JWT; giỏ có sản phẩm", "total_amount=-500000; shipping_address='A'", "400; tổng phải dương", "VALID", "Giá trị âm là phân vùng invalid rõ ràng của total tiền.", "Giữ nguyên.", "400; không tạo đơn", "BVA", "FAIL", "D-CHK-02"),
    c(7, "Partition", "total_amount là chuỗi số", "User có JWT; giỏ có sản phẩm", "total_amount='200000'", "400; sai kiểu dữ liệu", "VALID", "Schema request mô tả số; chuỗi không được coi là số tiền.", "Giữ nguyên.", "400; không tạo đơn", "EP/type", "PASS"),
    c(8, "Partition", "total_amount là null", "User có JWT; giỏ có sản phẩm", "total_amount=null", "400; thiếu giá trị", "VALID", "Null không phải số tiền hợp lệ.", "Giữ nguyên.", "400; không tạo đơn", "EP/type", "PASS"),
    c(9, "Partition", "Thiếu shipping_address", "User có JWT; giỏ có sản phẩm", "Chỉ gửi total_amount=200000", "400; shipping_address bắt buộc", "INCOMPLETE", "API spec không tuyên bố status khi thiếu shipping_address; ý tưởng đúng nhưng oracle chưa chốt.", "Ghi controlled 4xx/không 5xx; không khẳng định 400 nếu chưa chốt contract.", "Controlled client error nếu contract yêu cầu; không 5xx", "EP", "PASS"),
    c(10, "Partition", "shipping_address rỗng", "User có JWT; giỏ có sản phẩm", "shipping_address=''", "400; địa chỉ không được rỗng", "INCOMPLETE", "FR-08 không nêu độ dài tối thiểu địa chỉ và API spec không định status.", "Sửa expected thành robustness: không 5xx, không phản chiếu nguy hiểm.", "Controlled client error hoặc contract được chốt; không 5xx", "EP/BVA", "PASS"),
    c(11, "Partition", "shipping_address rất dài", "User có JWT; giỏ có sản phẩm", "Chuỗi 1001 ký tự", "400; vượt giới hạn 1000", "INCOMPLETE", "Không có giới hạn 1000 trong đặc tả; AI tự bịa boundary.", "Bỏ con số 1000; kiểm tra server không 5xx và lưu/đọc an toàn theo contract.", "Không 5xx; status cụ thể cần contract", "BVA", "PASS"),
    c(12, "Partition", "Địa chỉ chứa XSS", "User có JWT; giỏ có sản phẩm", "<img src=x onerror=alert(1)>", "400 hoặc escape payload; không lưu raw", "VALID", "SEC-04/FR-18 yêu cầu dữ liệu địa chỉ không gây XSS khi hiển thị.", "Giữ nguyên security expectation.", "Request bị từ chối hoặc dữ liệu được escape khi đọc lại", "Security", "FAIL", "D-CHK-05"),
    c(13, "Partition", "Địa chỉ chứa SQLi", "User có JWT; giỏ có sản phẩm", "' OR 1=1 --", "400; không lỗi SQL và không phản chiếu", "VALID", "Địa chỉ là dữ liệu; query phải parameterized và lỗi không được lộ.", "Giữ nguyên.", "Không bypass; không 5xx; không phản chiếu payload", "Security", "PASS"),
    c(14, "Partition", "Địa chỉ Unicode tiếng Việt", "User có JWT; giỏ có sản phẩm", "12 Lê Lợi, Quận 1, TP.HCM", "200; giữ nguyên Unicode", "VALID", "Unicode là input hợp lệ và cần bảo toàn khi lưu/đọc.", "Giữ nguyên.", "Controlled result; nếu tạo đơn thì status=pending và địa chỉ không hỏng mã hóa", "EP", "PASS"),
    c(15, "Partition", "total_amount là số thực", "User có JWT; giỏ có sản phẩm", "total_amount=200000.5", "400; tiền phải là số nguyên", "VALID", "Tiền đơn hàng được đặc tả là giá trị tiền nguyên; số thực là type/boundary partition.", "Giữ nguyên.", "400; không tạo đơn", "BVA/type", "PASS"),
    c(16, "Partition", "total_amount rất lớn", "User có JWT; giỏ có sản phẩm", "total_amount=9000000000000000000", "400; overflow", "VALID", "Giá trị vượt miền an toàn phải bị từ chối, không làm sai số hoặc crash.", "Giữ nguyên.", "400 hoặc controlled client error; không 5xx", "BVA", "PASS"),
    c(17, "Partition", "Body có field thừa", "User có JWT; giỏ có sản phẩm", "extra role='admin' cùng body hợp lệ", "200; bỏ qua field thừa", "INCOMPLETE", "Spec không nói strict/loose schema đối với field thừa; cần nêu assumption.", "Cho phép field vô hại nhưng kiểm tra không đổi user_id/role; không assert exact body.", "Nếu tạo đơn, user_id lấy từ JWT; field thừa không nâng quyền", "Schema", "PASS"),
    c(18, "Partition", "total_amount dùng ký hiệu khoa học", "User có JWT; giỏ có sản phẩm", "total_amount=2e5", "200; chấp nhận vì vẫn là number", "VALID", "JSON number hợp lệ; server không nên lỗi chỉ vì notation.", "Giữ nguyên nhưng không dùng làm oracle tính tổng.", "Không 5xx; nếu tạo đơn thì tổng phải theo giỏ", "EP", "PASS"),
    c(19, "State", "Checkout tạo đơn pending", "User có JWT; giỏ có sản phẩm", "Body hợp lệ; gọi POST /api/checkout", "200; order mới có status=pending", "VALID", "FR-10 quy định đơn mới luôn pending.", "Giữ nguyên.", "200; orderId số nguyên; status=pending khi đọc lại đơn", "State-transition", "PASS"),
    c(20, "State", "Giỏ bị xóa sau checkout", "User có JWT; giỏ có sản phẩm", "Checkout rồi GET /api/cart", "GET cart trả []", "VALID", "Đây là post-condition bắt buộc của FR-08.", "Giữ nguyên.", "Giỏ rỗng sau checkout thành công", "State/post-condition", "FAIL", "D-CHK-03"),
    c(21, "State", "Gửi lại cùng request checkout", "User có JWT; giỏ có sản phẩm", "Gửi cùng body hai lần", "Request thứ hai trả order cũ, không tạo trùng", "INCOMPLETE", "Idempotency không được nêu rõ trong FR-08/API spec.", "Ghi nhận quan sát nhưng không dùng làm strict assertion nếu contract chưa bổ sung.", "Không đặt strict oracle; ghi số đơn thực tế để audit", "State", "PASS"),
    c(22, "State", "Checkout khi giỏ rỗng", "User có JWT; không thêm sản phẩm", "Body total_amount=1", "400; không tạo đơn", "VALID", "Thanh toán không có hàng là trạng thái invalid theo nghiệp vụ.", "Giữ nguyên.", "400; không tạo đơn", "State-transition", "FAIL", "D-CHK-04"),
    c(23, "State", "Chuỗi cart → checkout → my-orders", "User có JWT", "POST cart rồi POST checkout rồi GET my-orders", "Order xuất hiện trong my-orders với pending", "VALID", "Đây là luồng end-to-end mà execution plan yêu cầu.", "Giữ nguyên.", "Order của đúng user xuất hiện với status=pending", "State/flow", "PASS"),
    c(24, "State", "orderId được trả về", "User có JWT; giỏ có sản phẩm", "Checkout thành công", "orderId là integer dương", "VALID", "Response schema tối thiểu cần định danh đơn để chain request.", "Giữ nguyên.", "orderId là integer dương", "Schema/state", "PASS"),
    c(25, "State", "user_id lấy từ token", "User A có JWT; body cố gửi user_id của B", "user_id=999 trong body", "Đơn dùng user_id từ body", "INVALID", "AI expected hành vi không an toàn; FR-08 yêu cầu identity lấy từ token.", "Sửa expected: user_id phải bằng req.user.id, bỏ qua body.", "Đơn thuộc user trong JWT, không thể giả mạo chủ đơn", "Security/state", "PASS"),
    c(26, "State", "Checkout sau khi login lại", "User đăng nhập; giỏ có sản phẩm", "Login → add cart → checkout", "200; pending", "VALID", "Kiểm tra state auth được nối giữa các request.", "Giữ nguyên.", "200; pending; order thuộc user vừa login", "State-transition", "PASS"),
    c(27, "Security", "Không có token", "Giỏ có thể có hoặc không", "POST checkout không Authorization", "401", "VALID", "SEC-02: endpoint bảo vệ phải yêu cầu JWT.", "Giữ nguyên.", "401; không tạo đơn", "Security", "PASS"),
    c(28, "Security", "Token sai chữ ký", "Có token giả", "Bearer token bị sửa payload", "403", "VALID", "JWT sai chữ ký thuộc nhánh invalid token; middleware trả 403 và không cho tạo đơn.", "Giữ nguyên.", "403; không tạo đơn", "Security", "PASS"),
    c(29, "Security", "Token hết hạn", "Có JWT exp trong quá khứ", "Bearer expired JWT", "403", "VALID", "JWT hết hạn bị jsonwebtoken verify từ chối với 403 trong middleware.", "Giữ nguyên.", "403; không tạo đơn", "Security", "PASS"),
    c(30, "Security", "Token của user khác", "User A có cart; User B có JWT", "B checkout với body cố trỏ tới cart/order của A", "Đơn của A được tạo", "VALID", "Identity phải lấy từ token và không được truy cập cart của user khác.", "Giữ nguyên security expectation.", "Đơn chỉ thuộc user B; không đọc/ghi cart của A", "Security/IDOR", "PASS"),
    c(31, "Security", "Đọc order bằng GET /api/orders/:id không token", "Có orderId của user khác", "GET /api/orders/{id} không Authorization", "401/403", "VALID", "SEC-02 áp dụng cho order data; endpoint kề bên là IDOR cần kiểm tra.", "Giữ nguyên.", "401/403; không lộ order", "Security/IDOR", "FAIL", "D-CHK-07"),
    c(32, "Security", "XSS không phản chiếu ở response", "User có JWT; giỏ có sản phẩm", "shipping_address='<script>alert(1)</script>'", "Không phản chiếu raw payload", "VALID", "Response và endpoint đọc lại không được trả dữ liệu nguy hiểm chưa escape.", "Giữ nguyên.", "Payload bị từ chối hoặc được escape khi đọc lại", "Security", "FAIL", "D-CHK-05"),
    c(33, "Schema", "Schema response checkout thành công", "User có JWT; giỏ có sản phẩm", "Body hợp lệ", "200; object có message:string và orderId:string", "INVALID", "Plan/API chain cần orderId số nguyên; AI tự chọn string trái schema dữ liệu.", "Sửa orderId thành integer dương.", "200; message:string; orderId:integer", "Schema", "PASS"),
    c(34, "Schema", "Content-Type response", "User có JWT; giỏ có sản phẩm", "Checkout hợp lệ", "application/json", "VALID", "Endpoint JSON phải trả JSON content type.", "Giữ nguyên.", "Content-Type application/json", "Schema", "PASS"),
    c(35, "Schema", "orderId là số nguyên", "User có JWT; giỏ có sản phẩm", "Checkout thành công", "orderId integer; không phải float/string/null", "VALID", "ID SQLite là integer và được dùng để chain GET order.", "Giữ nguyên.", "orderId là integer dương", "Schema", "PASS"),
    c(36, "Schema", "Không lộ field nhạy cảm", "User có JWT; giỏ có sản phẩm", "Checkout thành công rồi đọc order", "Response chỉ có message/orderId; không password/token nội bộ", "VALID", "Không response nào được lộ credential hoặc secret nội bộ.", "Giữ nguyên; không cấm metadata vô hại ngoài field nhạy cảm.", "Không có password/reset_token/login_attempts/locked_until", "Schema/security", "PASS"),
]


EXTENDED = [
    ("TC-API-CHECKOUT-037", "Dùng tổng giả trong body", "Có giỏ chứa sản phẩm 30 triệu; gửi total_amount=1", "Đơn phải có tổng tính từ giỏ, không phải 1", "D-CHK-01", "AI test request độc lập và không đặt bất biến giữa POST /api/cart và POST /api/checkout; nguyên nhân là giới hạn phạm vi prompt."),
    ("TC-API-CHECKOUT-038", "Biên total_amount âm", "Có JWT và giỏ có sản phẩm; gửi total_amount=-500000", "400; không tạo đơn", "D-CHK-02", "Prompt bám schema API nhưng không nối invariant nghiệp vụ FR-08 rằng tiền phải dương; cần suy luận từ requirement."),
    ("TC-API-CHECKOUT-039", "Hậu điều kiện xóa giỏ", "Checkout thành công rồi GET /api/cart", "Response là []; không còn item cũ", "D-CHK-03", "AI thường chỉ assert response của endpoint đang được hỏi, bỏ qua post-condition ở endpoint khác."),
    ("TC-API-CHECKOUT-040", "Giỏ rỗng không thể thanh toán", "Không thêm item; gọi checkout", "400; không tạo order", "D-CHK-04", "Spec API không mô tả rõ empty-cart oracle nên AI không tự suy luận trạng thái nghiệp vụ này."),
    ("TC-API-CHECKOUT-041", "IDOR khi đọc order", "User A tạo order; request không token hoặc user B GET /api/orders/:id", "401/403; không lộ order A", "D-CHK-07", "Đây là endpoint liền kề ngoài endpoint checkout; AI bị giới hạn ngữ cảnh theo một endpoint."),
    ("TC-API-CHECKOUT-042", "XSS trong shipping_address", "Địa chỉ là <img src=x onerror=alert(1)>; đọc lại order", "Payload bị reject hoặc escape, không lưu raw", "D-CHK-05", "AI dễ đẩy XSS về frontend và không dựng assertion persistence/read-back ở API."),
]


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def render_generated():
    rows = [
        "# API-2 — AI-generated test cases for `POST /api/checkout`",
        "",
        "> Output thô trước audit. Các expected chưa được chỉnh để khớp SUT; mọi sửa đổi được ghi ở `02-audit.md`.",
        "",
        "## P1 — Phân tích tham số và trạng thái",
        "",
        "| Tham số/trạng thái | Vị trí/điều kiện | Phân vùng nhận diện |",
        "| :--- | :--- | :--- |",
        "| `Authorization` | Header | thiếu, Bearer hợp lệ, token sai chữ ký, token hết hạn, token user khác |",
        "| `total_amount` | JSON body | số dương, 0, âm, chuỗi, null, thiếu, số thực, rất lớn, khoa học |",
        "| `shipping_address` | JSON body | hợp lệ, rỗng, thiếu, Unicode, XSS, SQLi, rất dài |",
        "| Giỏ hàng | Server state | có item, rỗng, thuộc user khác, hậu điều kiện sau checkout |",
        "| Đơn hàng | DB state | chưa có, pending sau checkout, truy vấn lại bằng orderId |",
        "",
        "## P2–P5 — Danh sách test case AI sinh",
        "",
        "| TC ID | Nhóm | Tiêu đề | Preconditions | Test data | Expected result theo output AI |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]
    rows.extend(f"| {x['id']} | {x['group']} | {x['title']} | {x['pre']} | `{x['data']}` | {x['ai']} |" for x in CASES)
    rows.extend([
        "",
        "## Thống kê output AI",
        "",
        "| Nhóm | Số lượng |",
        "| :--- | ---: |",
        "| Domain partition / BVA | 18 |",
        "| State transition / flow | 8 |",
        "| Security | 6 |",
        "| Schema validation | 4 |",
        "| **Tổng** | **36** |",
    ])
    write(OUT / "01-ai-generated.md", "\n".join(rows) + "\n")


def render_audit():
    rows = [
        "# API-2 — Human-review worksheet for AI-generated checkout cases",
        "",
        "> Oracle: FR-08/FR-10, `api_specification.md`, `backend/server.js` và `docs/hw06/02-sut-defect-catalog.md` §2.",
        "",
        "## Bảng audit 100% test case AI sinh",
        "",
        "| TC ID | Nhãn | Lý do review | Hành động sửa |",
        "| :--- | :--- | :--- | :--- |",
    ]
    rows.extend(f"| {x['id']} | {x['label']} | {x['reason']} | {x['action']} |" for x in CASES)
    rows.extend([
        "",
        "## Phiên bản expected sau audit cho case cần sửa",
        "",
        "| TC ID | Expected đã chốt |",
        "| :--- | :--- |",
    ])
    rows.extend(f"| {x['id']} | {x['final']} |" for x in CASES if x["label"] != "VALID")
    rows.extend([
        "",
        "## Thống kê audit",
        "",
        "| Nhãn | Số case | Tỷ lệ |",
        "| :--- | ---: | ---: |",
        "| VALID | 28 | 77.78% |",
        "| INVALID | 3 | 8.33% |",
        "| INCOMPLETE | 5 | 13.89% |",
        "| **Tổng đã audit** | **36/36** | **100%** |",
        "",
        "## HUMAN checkpoint — bắt buộc trước khi sang API-3",
        "",
        "- [ ] Tôi đã đối chiếu đủ 36 dòng với FR-08/FR-10, API spec và mã nguồn.",
        "- [ ] Tôi đồng ý hoặc đã chỉnh lại nhãn/lý do cho các case INVALID/INCOMPLETE.",
        "- [ ] Tôi hiểu vì sao expected phải theo đặc tả, không sửa để khớp bug của SUT.",
        "",
        "**Reviewed by:** <!-- HUMAN điền họ tên -->  ",
        "**Student ID:** `23127207`  ",
        "**Reviewed at:** <!-- HUMAN điền ngày giờ thật -->  ",
        "**Signature / confirmation:** <!-- HUMAN gõ `Đã duyệt` sau khi tự review -->",
    ])
    write(OUT / "02-audit.md", "\n".join(rows) + "\n")


def render_extended():
    rows = [
        "# API-2 — Test case do người học mở rộng cho `POST /api/checkout`",
        "",
        "| TC ID | Test case tự bổ sung | Preconditions / Test data | Expected result theo đặc tả | Bug nhắm tới | Vì sao AI bỏ sót |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]
    rows.extend(f"| {tc} | {title} | {pre} | {expected} | {bug} | {why} |" for tc, title, pre, expected, bug, why in EXTENDED)
    rows.extend(["", "**Số case mở rộng:** 6. Mỗi lý do được phân loại theo chất lượng prompt, giới hạn model hoặc đặc thù API."])
    write(OUT / "03-extended.md", "\n".join(rows) + "\n")


def render_final():
    rows = [
        "# API-2 — Danh sách test case chốt cho `POST /api/checkout`",
        "",
        "> 36 case AI sau audit + 6 case human extension. `Kỳ vọng chạy` phản ánh SUT hiện tại, còn `Expected` luôn theo đặc tả.",
        "",
        "| TC ID | Requirement | Nhóm | Kỹ thuật | Preconditions | Method + Endpoint / Test data | Expected | Nguồn | Kỳ vọng chạy | Bug ID |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- |",
    ]
    rows.extend(
        f"| {x['id']} | FR-08/FR-10 | {x['group']} | {x['technique']} | {x['pre']} | `POST /api/checkout`; {x['data']} | {x['final']} | AI/audit | {x['run']} | {x['bug']} |"
        for x in CASES
    )
    for tc, title, pre, expected, bug, _ in EXTENDED:
        rows.append(f"| {tc} | FR-08/FR-10/SEC-02/SEC-04 | Extension | Flow/security | {pre} | `POST /api/checkout` + chained endpoint; {title} | {expected} | Human | FAIL | {bug} |")
    rows.extend([
        "",
        "## Summary",
        "",
        "| Nguồn | Số lượng |",
        "| :--- | ---: |",
        "| AI-generated sau audit | 36 |",
        "| Human extension | 6 |",
        "| **Tổng** | **42** |",
        "| Expected fail do defect catalog | 12 strict/extension observations |",
    ])
    write(OUT / "test-cases.md", "\n".join(rows) + "\n")


if __name__ == "__main__":
    render_generated()
    render_audit()
    render_extended()
    render_final()
    print("Rendered API-2 artifacts: 36 AI cases + 6 extensions + audit + final matrix")
