"""Render API-3 order-status generation/audit artifacts from an explicit catalogue."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "api-03-admin-order-status"
STATES = ["pending", "confirmed", "shipping", "delivered", "canceled"]
ALLOWED = {
    ("pending", "confirmed"), ("pending", "canceled"),
    ("confirmed", "shipping"), ("confirmed", "canceled"),
    ("shipping", "delivered"), ("shipping", "canceled"),
}


def matrix_case(number, source, target, ai, label="VALID", reason="", action="Giữ nguyên.", run="PASS", bug="—"):
    allowed = (source, target) in ALLOWED
    final = f"200; transition {source} → {target} được chấp nhận" if allowed else f"400; từ chối transition {source} → {target}"
    return {
        "id": f"TC-API-ORDER-STATUS-{number:03d}",
        "number": number,
        "group": "State",
        "title": f"{source} → {target}",
        "pre": f"Admin JWT; order hiện ở trạng thái `{source}`",
        "data": f"PUT /api/admin/orders/:id; status='{target}'",
        "ai": ai,
        "label": label,
        "reason": reason or f"Ô ma trận {source} → {target} được đối chiếu trực tiếp với FR-10.",
        "action": action,
        "final": final,
        "technique": "State-transition",
        "run": run,
        "bug": bug,
        "spec_allowed": allowed,
        "source": source,
        "target": target,
    }


CASES = []
number = 1
for source in STATES:
    for target in STATES:
        if (source, target) == ("shipping", "canceled"):
            CASES.append(matrix_case(number, source, target, "400; invalid transition", "INVALID", "FR-10 cho phép Admin hủy đơn shipping; AI đã mô tả hiện thực lỗi thay vì đặc tả.", "Sửa expected thành 200; cần báo D-ADM-03 khi SUT trả 400.", "FAIL", "D-ADM-03"))
        elif (source, target) == ("canceled", "delivered"):
            CASES.append(matrix_case(number, source, target, "200; cập nhật thành công", "INVALID", "canceled là terminal state; AI đã tin whitelist hiện tại của SUT và cho phép hồi sinh đơn.", "Sửa expected thành 400; không được chuyển terminal canceled sang delivered.", "FAIL", "D-ADM-02"))
        else:
            allowed = (source, target) in ALLOWED
            expected = "200; transition hợp lệ" if allowed else "400; transition không hợp lệ"
            CASES.append(matrix_case(number, source, target, expected))
        number += 1


def extra(number, group, title, pre, data, ai, label, reason, action, final, technique, run="PASS", bug="—"):
    CASES.append({
        "id": f"TC-API-ORDER-STATUS-{number:03d}", "number": number,
        "group": group, "title": title, "pre": pre, "data": data,
        "ai": ai, "label": label, "reason": reason, "action": action,
        "final": final, "technique": technique, "run": run, "bug": bug,
        "spec_allowed": None, "source": "—", "target": "—",
    })


extra(26, "Partition", "Order id không tồn tại", "Admin JWT", "id=999999; status='confirmed'", "200; cập nhật", "VALID", "Defect catalog và API contract yêu cầu order không tồn tại trả 404.", "Giữ nguyên oracle 404.", "404; {error:'Order not found'}", "EP", bug="—")
extra(27, "Partition", "Order id âm", "Admin JWT", "id=-1; status='confirmed'", "400; id không hợp lệ", "INCOMPLETE", "API spec không quy định riêng 400 hay 404 cho id âm; ý tưởng boundary đúng nhưng status chưa có oracle.", "Sửa thành controlled 4xx; không 5xx và ghi actual status khi execute.", "Controlled 4xx; không 5xx", "BVA")
extra(28, "Partition", "Order id là chuỗi không số", "Admin JWT", "id='abc'; status='confirmed'", "200; server cast id", "INVALID", "Không được coi chuỗi tùy ý là order id hợp lệ; expected AI không bám schema path parameter.", "Sửa thành 400/404 controlled error.", "Controlled 4xx; không cập nhật order", "EP/type", "PASS")
extra(29, "Partition", "Thiếu status", "Admin JWT", "Body={}", "200; giữ nguyên trạng thái", "VALID", "Body API yêu cầu status; thiếu field phải bị từ chối.", "Giữ nguyên.", "400; lỗi transition/validation", "EP", bug="—")
extra(30, "Partition", "Status sai enum/hoa", "Admin JWT", "status='DELIVERED'", "200; normalize thành delivered", "INVALID", "API công bố đúng 5 giá trị lowercase; không có yêu cầu normalize.", "Sửa thành 400; không cập nhật.", "400; invalid state transition", "EP/type", "PASS")
extra(31, "Security", "Không có token", "Order tồn tại", "Không gửi Authorization", "401", "VALID", "FR-12/SEC-03 yêu cầu JWT hợp lệ cho /api/admin/*.", "Giữ nguyên.", "401; không cập nhật", "Security", bug="—")
extra(32, "Security", "Token sai chữ ký", "Order tồn tại", "Bearer invalid.token", "403", "VALID", "authenticateToken từ chối token sai chữ ký.", "Giữ nguyên.", "403; không cập nhật", "Security", bug="—")
extra(33, "Security", "User thường gọi endpoint admin", "User JWT; order tồn tại", "Bearer userToken; status='confirmed'", "200; chỉ cần JWT", "INVALID", "FR-12/SEC-03 yêu cầu role=admin, không chỉ token tồn tại.", "Sửa thành 403; tạo bug role escalation nếu SUT cho phép.", "403; không cập nhật", "Security/role", "FAIL", "D-ADM-01")
extra(34, "Security", "User A sửa order của user B", "User JWT; order B tồn tại", "Bearer userToken; id=orderB", "403 vì khác chủ đơn", "INCOMPLETE", "Endpoint admin phải chặn user role trước; ownership rule chưa được API spec mô tả riêng.", "Assert 403 do role; nếu admin thì quyền toàn hệ thống là hợp lệ.", "403 với user token", "Security/IDOR")
extra(35, "Schema", "Response success có message string", "Admin JWT; transition hợp lệ", "status='confirmed'", "200; message là object", "INCOMPLETE", "Spec chỉ nêu endpoint/body, chưa công bố exact response schema; không được tự bịa object.", "Hạ thành tối thiểu message:string nếu response có message.", "200; message:string", "Schema")
extra(36, "Schema", "Response lỗi transition", "Admin JWT; transition invalid", "status='delivered' từ pending", "400; body chỉ có message", "INCOMPLETE", "API spec không quy định exact error fields; chỉ status + controlled JSON là oracle chắc chắn.", "Không assert duy nhất message; kiểm tra JSON và error/message có nội dung.", "400; controlled JSON error", "Schema")
extra(37, "Schema", "Content-Type JSON", "Admin JWT; transition hợp lệ", "status='confirmed'", "text/html cũng chấp nhận", "VALID", "API JSON phải trả application/json.", "Sửa expected thành application/json.", "Content-Type application/json", "Schema")
extra(38, "Schema", "Không lộ secret hoặc credential", "Admin JWT; transition hợp lệ", "status='confirmed'", "Response có thể trả token/password", "INCOMPLETE", "API spec không công bố full response nhưng security boundary cấm lộ credential.", "Giữ negative security assertion, không yêu cầu exact field whitelist.", "Không có password/token/secret nội bộ", "Schema/security")


EXTENDED = [
    ("TC-API-ORDER-STATUS-039", "Role escalation bằng user token", "User thường có JWT; order tồn tại; PUT status=confirmed", "403; không cập nhật order", "D-ADM-01", "AI mặc định endpoint `/admin/` đã kiểm tra role; đây là assumption bias về chức năng."),
    ("TC-API-ORDER-STATUS-040", "Cross-user order mutation", "User A dùng token sửa order của user B", "403; user không có quyền admin", "D-ADM-01", "Case cần hai danh tính và dữ liệu liên kết; prompt generate không yêu cầu kịch bản multi-identity."),
    ("TC-API-ORDER-STATUS-041", "Canceled không hồi sinh và dashboard không tăng doanh thu", "Admin thử canceled→delivered rồi kiểm tra dữ liệu delivered/dashboard", "400; không tăng delivered revenue", "D-ADM-02", "AI thường chỉ assert response endpoint, bỏ qua tác động dây chuyền sang FR-13."),
    ("TC-API-ORDER-STATUS-042", "Admin hủy đơn shipping", "Admin JWT; order shipping; status=canceled", "200; order chuyển canceled", "D-ADM-03", "Đặc tả diễn đạt quyền Admin gián tiếp; AI bám whitelist hiện tại thay vì suy luận từ state rule."),
    ("TC-API-ORDER-STATUS-043", "User không hủy order shipping qua endpoint user", "User JWT; order shipping; PUT /api/orders/:id/cancel", "400; user không được hủy shipping", "D-ADM-08", "Endpoint cancel nằm ngoài prompt về admin status, nên AI không nối hai endpoint cùng state machine."),
    ("TC-API-ORDER-STATUS-044", "Status sai kiểu dữ liệu", "Admin JWT; status=['delivered'] hoặc {value:'delivered'}", "400; phân biệt type invalid với transition invalid", "D-ADM-06", "AI thường chỉ sinh enum sai dạng chuỗi, bỏ qua type confusion của JSON body."),
]


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def render_generated():
    rows = [
        "# API-3 — AI-generated test cases for `PUT /api/admin/orders/:id/status`",
        "",
        "> Output thô trước audit. Ma trận state 5×5 được liệt kê đầy đủ theo thứ tự pending, confirmed, shipping, delivered, canceled.",
        "",
        "## P1 — Phân tích input và state",
        "",
        "| Input/state | Kiểu/vị trí | Oracle/partition |",
        "| :--- | :--- | :--- |",
        "| `Authorization` | Header Bearer JWT | thiếu, sai chữ ký, user role, admin role |",
        "| `:id` | Path parameter | số nguyên tồn tại, không tồn tại, âm, chuỗi |",
        "| `status` | JSON body string enum | 5 lowercase states, thiếu, sai kiểu, sai casing |",
        "| Order state | DB state | 5×5 transitions; delivered/canceled terminal |",
        "",
        "## P2–P5 — Ma trận và case bổ sung",
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
        "| State transition matrix | 25 |",
        "| Domain partition/BVA | 5 |",
        "| Security | 4 |",
        "| Schema | 4 |",
        "| **Tổng** | **38** |",
    ])
    write(OUT / "01-ai-generated.md", "\n".join(rows) + "\n")


def render_audit():
    rows = [
        "# API-3 — Human-review worksheet for AI-generated order-status cases",
        "",
        "> Oracle: FR-10/FR-12/FR-18, API specification, `backend/server.js` và `docs/hw06/02-sut-defect-catalog.md` §3.",
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
        "| VALID | 28 | 73.68% |",
        "| INVALID | 5 | 13.16% |",
        "| INCOMPLETE | 5 | 13.16% |",
        "| **Tổng đã audit** | **38/38** | **100%** |",
        "",
        "## HUMAN checkpoint — bắt buộc trước khi sang Postman",
        "",
        "- [ ] Tôi đã đối chiếu đủ 38 dòng, đặc biệt đủ 25 ô state matrix.",
        "- [ ] Tôi đồng ý hoặc đã chỉnh lại nhãn/lý do cho case INVALID/INCOMPLETE.",
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
        "# API-3 — Test case do người học mở rộng cho `PUT /api/admin/orders/:id/status`",
        "",
        "| TC ID | Test case tự bổ sung | Preconditions / Test data | Expected result theo đặc tả | Bug nhắm tới | Vì sao AI bỏ sót |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]
    rows.extend(f"| {tc} | {title} | {pre} | {expected} | {bug} | {why} |" for tc, title, pre, expected, bug, why in EXTENDED)
    rows.append("\n**Số case mở rộng:** 6; tất cả đều nhắm security hoặc state-transition liên API.")
    write(OUT / "03-extended.md", "\n".join(rows) + "\n")


def render_final():
    rows = [
        "# API-3 — Danh sách test case chốt cho `PUT /api/admin/orders/:id/status`",
        "",
        "> 38 case AI sau audit + 6 case human extension. 25 dòng đầu là đầy đủ ma trận 5×5.",
        "",
        "| TC ID | Requirement | Nhóm | Kỹ thuật | Preconditions | Method + Endpoint / Test data | Expected | Nguồn | Kỳ vọng chạy | Bug ID |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- |",
    ]
    rows.extend(f"| {x['id']} | FR-10/FR-12/FR-18 | {x['group']} | {x['technique']} | {x['pre']} | `{x['data']}` | {x['final']} | AI/audit | {x['run']} | {x['bug']} |" for x in CASES)
    for tc, title, pre, expected, bug, _ in EXTENDED:
        rows.append(f"| {tc} | FR-10/FR-12/FR-18 | Extension | State/security | {pre} | `{title}` | {expected} | Human | FAIL | {bug} |")
    rows.extend([
        "",
        "## Summary",
        "",
        "| Nguồn | Số lượng |",
        "| :--- | ---: |",
        "| AI-generated sau audit | 38 |",
        "| Human extension | 6 |",
        "| **Tổng** | **44** |",
    ])
    write(OUT / "test-cases.md", "\n".join(rows) + "\n")


if __name__ == "__main__":
    render_generated()
    render_audit()
    render_extended()
    render_final()
    print("Rendered API-3 artifacts: 38 AI cases (25 matrix) + 6 extensions")
