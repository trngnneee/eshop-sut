import urllib.request
import urllib.error
import json
import sqlite3
import os
import sys
import codecs

if sys.stdout.encoding != 'utf-8':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

BASE_URL = "http://localhost:3000"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "backend", "database.sqlite"))

def make_request(path, method="POST", data=None):
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    req_data = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            return response.status, json.loads(res_body)
    except urllib.error.HTTPError as e:
        res_body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(res_body)
        except Exception:
            return e.code, {"error": res_body}
    except Exception as e:
        return 0, {"error": str(e)}

def execute_db_write(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def run_tests():
    print("=" * 60)
    print("KỊCH BẢN KIỂM THỬ FR-01: ĐĂNG KÝ TÀI KHOẢN (REGISTRATION)")
    print("=" * 60)
    
    # Dọn dẹp các tài khoản test trước khi bắt đầu
    emails_to_clean = [
        "tester_success@eshop.com",
        "tester_reg002@eshop.com",
        "tester_reg005@eshop.com",
        "tester_reg006@eshop.com",
        "tester_reg007@eshop.com",
        "tester_reg008@eshop.com",
        "tester_reg009@eshop.com",
        "tester_reg010@eshop.com",
        "tester_reg011@eshop.com"
    ]
    for email in emails_to_clean:
        execute_db_write("DELETE FROM users WHERE email = ?", (email,))
        
    # Thêm các email mới vào cleanup nâng cao bằng query LIKE
    execute_db_write("DELETE FROM users WHERE email LIKE 'tester_%' OR email LIKE '%@domain.com' OR email = 'userdomain.com' OR email = 'user@domaincom' OR email = '@domain.com' OR email = 'user@' OR email = 'user@com@domain.com' OR email = 'user@domain..com' OR email = 'user @domain.com' OR email = 'user@domain.com@' OR email = '.user@domain.com' OR email = 'user@domain.com.' OR email = 'user@DOMAIN.com' OR email = 'user@d.com' OR email = 'u@d.c' OR email LIKE '%XSS%' OR email LIKE '%OR 1=1%'")

    # 1. TC-REG-001: Đăng ký thành công với thông tin hợp lệ
    print("\n[TC-REG-001] Đăng ký thành công với thông tin hợp lệ")
    status, res = make_request("/api/register", data={
        "name": "Tester Success",
        "email": "tester_success@eshop.com",
        "password": "Secure123!",
        "confirm_password": "Secure123!"
    })
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status == 200 and "id" in res:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # 2. TC-REG-002: Đăng ký thất bại do thiếu Họ Tên
    print("\n[TC-REG-002] Đăng ký thất bại do thiếu Họ Tên")
    status, res = make_request("/api/register", data={
        "name": "",
        "email": "tester_reg002@eshop.com",
        "password": "Secure123!",
        "confirm_password": "Secure123!"
    })
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status == 400 and "error" in res:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # 3. TC-REG-003: Đăng ký thất bại do Email sai định dạng
    print("\n[TC-REG-003] Đăng ký thất bại do Email sai định dạng")
    status, res = make_request("/api/register", data={
        "name": "Tester Email Format",
        "email": "invalid_email",
        "password": "Secure123!",
        "confirm_password": "Secure123!"
    })
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status == 400 and "error" in res:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # 4. TC-REG-004: Đăng ký thất bại do Email đã tồn tại
    print("\n[TC-REG-004] Đăng ký thất bại do Email đã tồn tại")
    status, res = make_request("/api/register", data={
        "name": "Tester Email Exist",
        "email": "test@eshop.com",
        "password": "Secure123!",
        "confirm_password": "Secure123!"
    })
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status in (400, 409) and "error" in res:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # 5. TC-REG-005: Đăng ký thất bại do mật khẩu ngắn hơn 8 ký tự
    print("\n[TC-REG-005] Đăng ký thất bại do mật khẩu ngắn hơn 8 ký tự (7 ký tự)")
    status, res = make_request("/api/register", data={
        "name": "Tester Pwd Length",
        "email": "tester_reg005@eshop.com",
        "password": "P@ss123",
        "confirm_password": "P@ss123"
    })
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status == 400 and "error" in res:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # 6. TC-REG-006: Đăng ký thành công với mật khẩu dài đúng 8 ký tự
    print("\n[TC-REG-006] Đăng ký thành công với mật khẩu dài đúng 8 ký tự")
    status, res = make_request("/api/register", data={
        "name": "Tester Pwd Length 8",
        "email": "tester_reg006@eshop.com",
        "password": "P@ss1234",
        "confirm_password": "P@ss1234"
    })
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status == 200 and "id" in res:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # 7. TC-REG-007: Đăng ký thất bại do mật khẩu thiếu chữ hoa
    print("\n[TC-REG-007] Đăng ký thất bại do mật khẩu thiếu chữ hoa")
    status, res = make_request("/api/register", data={
        "name": "Tester Pwd Upper",
        "email": "tester_reg007@eshop.com",
        "password": "secure123!",
        "confirm_password": "secure123!"
    })
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status == 400 and "error" in res:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # 8. TC-REG-008: Đăng ký thất bại do mật khẩu thiếu chữ thường
    print("\n[TC-REG-008] Đăng ký thất bại do mật khẩu thiếu chữ thường")
    status, res = make_request("/api/register", data={
        "name": "Tester Pwd Lower",
        "email": "tester_reg008@eshop.com",
        "password": "SECURE123!",
        "confirm_password": "SECURE123!"
    })
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status == 400 and "error" in res:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # 9. TC-REG-009: Đăng ký thất bại do mật khẩu thiếu chữ số
    print("\n[TC-REG-009] Đăng ký thất bại do mật khẩu thiếu chữ số")
    status, res = make_request("/api/register", data={
        "name": "Tester Pwd Digit",
        "email": "tester_reg009@eshop.com",
        "password": "Secure!!!",
        "confirm_password": "Secure!!!"
    })
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status == 400 and "error" in res:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # 10. TC-REG-010: Đăng ký thất bại do mật khẩu thiếu ký tự đặc biệt
    print("\n[TC-REG-010] Đăng ký thất bại do mật khẩu thiếu ký tự đặc biệt")
    status, res = make_request("/api/register", data={
        "name": "Tester Pwd Special",
        "email": "tester_reg010@eshop.com",
        "password": "Secure123",
        "confirm_password": "Secure123"
    })
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status == 400 and "error" in res:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # 11. TC-REG-011: Đăng ký thất bại do xác nhận mật khẩu không khớp
    print("\n[TC-REG-011] Đăng ký thất bại do xác nhận mật khẩu không khớp")
    status, res = make_request("/api/register", data={
        "name": "Tester Confirm Pwd",
        "email": "tester_reg011@eshop.com",
        "password": "Secure123!",
        "confirm_password": "Secure123#"
    })
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status == 400 and "error" in res:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # THÊM CÁC TEST CASES 12 ĐẾN 41
    extra_cases = [
        {"id": 12, "title": "Đăng ký với Họ Tên chứa số (Ví dụ: 'Nguyễn Văn A 123')", "name": "Nguyễn Văn A 123", "email": "tester_reg012@eshop.com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 13, "title": "Đăng ký với Họ Tên chứa ký tự đặc biệt (Ví dụ: 'Nguyễn@Văn_A')", "name": "Nguyễn@Văn_A", "email": "tester_reg013@eshop.com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 14, "title": "Đăng ký với Họ Tên chứa mã độc XSS (Ví dụ: <script>alert('XSS')</script>)", "name": "<script>alert('XSS')</script>", "email": "tester_reg014@eshop.com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 15, "title": "Đăng ký với Họ Tên chứa lệnh SQL Injection (Ví dụ: \"' OR 1=1 --\")", "name": "' OR 1=1 --", "email": "tester_reg015@eshop.com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 16, "title": "Đăng ký với Họ Tên chỉ chứa khoảng trắng (Ví dụ: '   ')", "name": "   ", "email": "tester_reg016@eshop.com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 17, "title": "Đăng ký với Họ Tên không viết hoa chữ cái đầu hoặc viết hoa các chữ cái không đứng đầu (Ví dụ: 'phan Quoc tHinh')", "name": "phan Quoc tHinh", "email": "tester_reg017@eshop.com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": False, "check_normalization": True},
        {"id": 18, "title": "Đăng ký với Họ Tên có độ dài bằng 1 ký tự (Biên dưới lỗi)", "name": "A", "email": "tester_reg018@eshop.com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 19, "title": "Đăng ký với Họ Tên có độ dài bằng 101 ký tự (Biên trên lỗi)", "name": "A"*101, "email": "tester_reg019@eshop.com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 20, "title": "Đăng ký với Email thiếu ký tự '@' (Ví dụ: 'userdomain.com')", "name": "Tester Email At", "email": "userdomain.com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 21, "title": "Đăng ký với Email thiếu dấu chấm '.' ở domain-part", "name": "Tester Email Dot", "email": "user@domaincom", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 22, "title": "Đăng ký với Email thiếu phần local-part", "name": "Tester Email Local", "email": "@domain.com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 23, "title": "Đăng ký với Email thiếu phần domain-part", "name": "Tester Email Domain", "email": "user@", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 24, "title": "Đăng ký với Email chứa từ 2 ký tự '@' trở lên (Ví dụ: 'user@com@domain.com')", "name": "Tester Email Multi At", "email": "user@com@domain.com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 25, "title": "Đăng ký với Email chứa 2 dấu chấm liên tiếp ở domain-part (Ví dụ: 'user@domain..com')", "name": "Tester Email Double Dot", "email": "user@domain..com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 26, "title": "Đăng ký với Email chứa khoảng trắng (Ví dụ: 'user @domain.com')", "name": "Tester Email Space", "email": "user @domain.com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 27, "title": "Đăng ký với Email có ký tự '@' nằm ở vị trí đầu tiên", "name": "Tester Email Start At", "email": "@domain.com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 28, "title": "Đăng ký với Email có ký tự '@' nằm ở vị trí cuối cùng", "name": "Tester Email End At", "email": "user@domain.com@", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 29, "title": "Đăng ký với Email có dấu chấm '.' nằm ở vị trí đầu tiên", "name": "Tester Email Start Dot", "email": ".user@domain.com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 30, "title": "Đăng ký với Email có dấu chấm '.' nằm ở vị trí cuối cùng", "name": "Tester Email End Dot", "email": "user@domain.com.", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 31, "title": "Đăng ký với Email có phần domain-part chứa chữ in hoa", "name": "Tester Email Upper Domain", "email": "user@DOMAIN.com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": False, "check_email_normalization": True},
        {"id": 32, "title": "Đăng ký với Email có độ dài phần domain-part bằng 1 ký tự", "name": "Tester Email Domain Len 1", "email": "user@d.com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 33, "title": "Đăng ký với Email có tổng độ dài bằng 5 ký tự (Biên dưới lỗi)", "name": "Tester Email Len 5", "email": "u@d.c", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 34, "title": "Đăng ký với Email có tổng độ dài bằng 255 ký tự (Biên trên lỗi)", "name": "Tester Email Len 255", "email": "u"*243 + "@domain.com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 35, "title": "Đăng ký với Email chứa mã độc XSS", "name": "Tester Email XSS", "email": "<script>alert('XSS')</script>@domain.com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 36, "title": "Đăng ký với Email chứa lệnh SQL Injection (Ví dụ: \"' OR 1=1 --@domain.com\")", "name": "Tester Email SQLi", "email": "' OR 1=1 --@domain.com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": True},
        {"id": 37, "title": "Đăng ký với Mật khẩu chứa mã độc XSS", "name": "Tester Pwd XSS", "email": "tester_pwd_xss@domain.com", "password": "<script>alert('XSS')</script>", "confirm": "<script>alert('XSS')</script>", "expected_fail": True},
        {"id": 38, "title": "Đăng ký với Mật khẩu chứa lệnh SQL Injection (Ví dụ: \"' OR '1'='1\")", "name": "Tester Pwd SQLi", "email": "tester_pwd_sqli@domain.com", "password": "' OR '1'='1", "confirm": "' OR '1'='1", "expected_fail": True},
        {"id": 39, "title": "Đăng ký với Xác nhận mật khẩu chứa mã độc XSS", "name": "Tester Confirm XSS", "email": "tester_conf_xss@domain.com", "password": "Secure123!", "confirm": "<script>alert('XSS')</script>", "expected_fail": True},
        {"id": 40, "title": "Đăng ký với Xác nhận mật khẩu chứa lệnh SQL Injection (Ví dụ: \"' OR '1'='1\")", "name": "Tester Confirm SQLi", "email": "tester_conf_sqli@domain.com", "password": "Secure123!", "confirm": "' OR '1'='1", "expected_fail": True},
        {"id": 41, "title": "Đăng ký thành công nhưng gặp sự cố mạng/mất kết nối ngay lúc chuyển hướng", "name": "Tester Network Lost", "email": "tester_network@domain.com", "password": "Secure123!", "confirm": "Secure123!", "expected_fail": False, "check_db_only": True}
    ]

    for tc in extra_cases:
        tc_id = f"TC-REG-{tc['id']:03d}"
        print(f"\n[{tc_id}] {tc['title']}")
        status, res = make_request("/api/register", data={
            "name": tc["name"],
            "email": tc["email"],
            "password": tc["password"],
            "confirm_password": tc["confirm"]
        })
        print(f"  - Phản hồi: HTTP {status} | {res}")
        
        passed = False
        if tc.get("expected_fail"):
            # Lỗi thì mong đợi HTTP 400
            if status == 400 and "error" in res:
                passed = True
        else:
            # Thành công thì mong đợi HTTP 200
            if status == 200:
                if tc.get("check_normalization"):
                    # Kiểm tra xem Họ Tên đã được chuẩn hóa chưa
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM users WHERE email = ?", (tc["email"],))
                    row = cursor.fetchone()
                    conn.close()
                    if row and row[0] in ("Phan Quốc Thịnh", "Phan Quoc Thinh"):
                        passed = True
                        print(f"  - CSDL check: Họ tên được tự động chuẩn hóa thành '{row[0]}'")
                    else:
                        print(f"  - CSDL check: Họ tên trong CSDL là '{row[0]}' (Không chuẩn hóa!)")
                elif tc.get("check_email_normalization"):
                    # Kiểm tra xem email domain đã được chuẩn hóa thành lowercase chưa
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute("SELECT email FROM users WHERE name = ?", (tc["name"],))
                    row = cursor.fetchone()
                    conn.close()
                    if row and row[0] == "user@domain.com":
                        passed = True
                        print(f"  - CSDL check: Email được chuẩn hóa thành '{row[0]}'")
                    else:
                        print(f"  - CSDL check: Email trong CSDL là '{row[0]}' (Không chuẩn hóa!)")
                elif tc.get("check_db_only"):
                    # Kiểm tra xem có lưu được vào CSDL không
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM users WHERE email = ?", (tc["email"],))
                    row = cursor.fetchone()
                    conn.close()
                    if row:
                        passed = True
                        print("  - CSDL check: Tìm thấy bản ghi đăng ký thành công")
                else:
                    passed = True

        if passed:
            print("  => KẾT QUẢ: PASSED")
        else:
            print("  => KẾT QUẢ: FAILED")

    # Dọn dẹp nâng cao sau khi hoàn tất để trả lại trạng thái ban đầu sạch sẽ
    execute_db_write("DELETE FROM users WHERE email LIKE 'tester_%' OR email LIKE '%@domain.com' OR email = 'userdomain.com' OR email = 'user@domaincom' OR email = '@domain.com' OR email = 'user@' OR email = 'user@com@domain.com' OR email = 'user@domain..com' OR email = 'user @domain.com' OR email = 'user@domain.com@' OR email = '.user@domain.com' OR email = 'user@domain.com.' OR email = 'user@DOMAIN.com' OR email = 'user@d.com' OR email = 'u@d.c' OR email LIKE '%XSS%' OR email LIKE '%OR 1=1%'")
    for email in emails_to_clean:
        execute_db_write("DELETE FROM users WHERE email = ?", (email,))

if __name__ == "__main__":
    run_tests()
