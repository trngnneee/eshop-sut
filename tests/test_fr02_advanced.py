import urllib.request
import urllib.error
import json
import sqlite3
import time
import os
import sys
import codecs

if sys.stdout.encoding != 'utf-8':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

BASE_URL = "http://localhost:3000"
DB_PATH = os.path.join("backend", "database.sqlite")

def make_request(path, method="POST", data=None, token=None, headers_override=None):
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if headers_override:
        headers.update(headers_override)
        
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

def query_db(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result

def execute_db(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def run_advanced_tests():
    print("=" * 70)
    print("KỊCH BẢN KIỂM THỬ NÂNG CAO FR-02 (TC-LOGIN-013 -> TC-LOGIN-022)")
    print("=" * 70)
    
    email = "adv_test@eshop.com"
    password = "ValidPassword1!"
    
    # Dọn dẹp tài khoản cũ
    try:
        execute_db("DELETE FROM users WHERE email = ?", (email,))
    except Exception as e:
        print(f"Lỗi dọn dẹp DB: {e}")
        
    # Đăng ký tài khoản thử nghiệm
    make_request("/api/register", data={"name": "Adv User", "email": email, "password": password})

    # 1. TC-LOGIN-013: Reset attempts counter on successful login
    print("\n[TC-LOGIN-013] Kiểm tra reset bộ đếm khi đăng nhập đúng")
    # Đăng nhập sai 1 lần để tăng attempts
    make_request("/api/login", data={"email": email, "password": "WrongPassword"})
    # Đăng nhập đúng ngay lập tức
    status, res = make_request("/api/login", data={"email": email, "password": password})
    
    # Kiểm tra DB ngay lập tức
    user_data = query_db("SELECT login_attempts FROM users WHERE email = ?", (email,))
    attempts = user_data[0][0] if user_data else -1
    print(f"  - Kết quả trả về: HTTP {status} | login_attempts trong DB = {attempts}")
    if status == 200 and attempts == 0:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Ghi DB bất đồng bộ không callback gây race condition khiến attempts chưa được reset về 0)")

    # 2. TC-LOGIN-014: Automatic unlock after 30s lockout duration
    print("\n[TC-LOGIN-014] Kiểm tra tự động mở khóa sau 30 giây")
    # Đăng nhập sai liên tiếp để kích hoạt khóa
    make_request("/api/login", data={"email": email, "password": "WrongPassword"})
    make_request("/api/login", data={"email": email, "password": "WrongPassword"})
    make_request("/api/login", data={"email": email, "password": "WrongPassword"})
    
    user_data = query_db("SELECT locked_until FROM users WHERE email = ?", (email,))
    locked_until = user_data[0][0] if user_data else None
    print(f"  - Trạng thái khóa trong DB: locked_until = {locked_until}")
    
    # Thử đăng nhập lại sau khi chờ (mô phỏng hoặc thực tế). Vì thời gian chạy nhanh, ta kiểm tra giá trị thời gian khóa từ DB.
    if locked_until:
        try:
            iso_str = locked_until.replace("Z", "").split(".")[0]
            lock_epoch = time.mktime(time.strptime(iso_str, "%Y-%m-%dT%H:%M:%S"))
            duration = lock_epoch - time.mktime(time.gmtime())
            print(f"  - Thời gian khóa tính toán: {round(duration)} giây.")
            if 25 <= duration <= 35:
                print("  => KẾT QUẢ: PASSED")
            else:
                print(f"  => KẾT QUẢ: FAILED (Tài khoản bị khóa trong {round(duration)} giây thay vì 30 giây)")
        except Exception as e:
            print(f"  - Không thể parse thời gian khóa: {e}")
            print("  => KẾT QUẢ: FAILED")
    else:
        print("  => KẾT QUẢ: FAILED (Tài khoản chưa bị khóa)")

    # 3. TC-LOGIN-015: Invalid email format validation at API level
    print("\n[TC-LOGIN-015] Kiểm tra validate email không hợp lệ ở Backend")
    status, res = make_request("/api/login", data={"email": "invalidemailform", "password": password})
    print(f"  - Phản hồi Backend: HTTP {status} | {res}")
    if status == 400:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Backend không tự kiểm tra định dạng email và trả về HTTP 401 thay vì 400 Bad Request)")

    # 4. TC-LOGIN-016: XSS injection check
    print("\n[TC-LOGIN-016] Kiểm tra chống tấn công XSS trên trường Đăng nhập")
    status, res = make_request("/api/login", data={"email": "<script>alert('XSS')</script>", "password": "password"})
    print(f"  - Phản hồi: HTTP {status} | {res}")
    # Trả về 401 thông thường mà không crash server
    if status == 401:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # 5. TC-LOGIN-018: URL parameters authentication check
    print("\n[TC-LOGIN-018] Kiểm tra chặn truyền thông tin đăng nhập qua URL GET parameters")
    status, res = make_request(f"/api/login?email={email}&password={password}", method="GET")
    print(f"  - Phản hồi GET: HTTP {status} | {res}")
    if status in [404, 405]:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # 6. TC-LOGIN-019: None Algorithm JWT bypass check
    print("\n[TC-LOGIN-019] Kiểm tra chặn JWT Token thuật toán none")
    # Header: {"alg":"none","typ":"JWT"}, Payload: {"id":1,"role":"admin"}
    # Base64 encoded: eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJpZCI6MSwicm9sZSI6ImFkbWluIn0.
    fake_token = "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJpZCI6MSwicm9sZSI6ImFkbWluIn0."
    status, res = make_request("/api/users/me", method="GET", token=fake_token)
    print(f"  - Phản hồi khi dùng token none: HTTP {status} | {res}")
    if status in [401, 403]:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Chấp nhận token thuật toán none)")

    # 7. TC-LOGIN-020: Keyboard navigation & Tab Order static check
    print("\n[TC-LOGIN-020] Kiểm tra thứ tự di chuyển tiêu điểm (Tab Order) tĩnh")
    login_jsx_path = os.path.join("frontend-web", "src", "pages", "Login.jsx")
    tab_bug = False
    if os.path.exists(login_jsx_path):
        with open(login_jsx_path, "r", encoding="utf-8") as f:
            content = f.read()
            if 'tabIndex={1}' in content or 'tabIndex="1"' in content:
                print("  - Phát hiện lỗi: Nút Submit có thuộc tính tabIndex={1} phá vỡ Tab Order tự nhiên.")
                tab_bug = True
    if not tab_bug:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # 8. TC-LOGIN-021: Autofill compatibility static check
    print("\n[TC-LOGIN-021] Kiểm tra thuộc tính name & autocomplete tương thích Autofill")
    has_autofill_attrs = False
    if os.path.exists(login_jsx_path):
        with open(login_jsx_path, "r", encoding="utf-8") as f:
            content = f.read()
            if 'name="email"' in content and 'autocomplete="username"' in content:
                has_autofill_attrs = True
    if has_autofill_attrs:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Thiếu thuộc tính name và autocomplete trên các thẻ input)")

    # 9. TC-LOGIN-022: Large payload body size limit check (150kb payload)
    print("\n[TC-LOGIN-022] Kiểm tra giới hạn kích thước gói tin gửi lên API (150KB)")
    large_password = "A" * 150000 # 150KB
    status, res = make_request("/api/login", data={"email": email, "password": large_password})
    print(f"  - Phản hồi khi gửi payload lớn: HTTP {status} | {res.get('error', res)}")
    if status == 413 or (status == 500 and "too large" in str(res)):
        print("  => KẾT QUẢ: PASSED")
    else:
        # Nếu server cho phép đi qua và xử lý (trả về 401 thay vì chặn ngay lập tức bằng 413) thì coi như không cấu hình giới hạn chặt chẽ
        # Note: Express body-parser mặc định là 100kb, nên sẽ trả về 413 Payload Too Large!
        if status == 413:
            print("  => KẾT QUẢ: PASSED")
        else:
            print("  => KẾT QUẢ: FAILED (Cho phép truyền tải dữ liệu kích thước lớn vượt giới hạn an toàn)")

    # 10. TC-LOGIN-023: Lower boundary of failed attempts
    print("\n[TC-LOGIN-023] Kiểm tra biên dưới của số lần đăng nhập sai (2 lần liên tiếp không khóa)")
    email24 = "test_tc24@eshop.com"
    pwd24 = "ValidPassword1!"
    execute_db("DELETE FROM users WHERE email = ?", (email24,))
    make_request("/api/register", data={"name": "TC24 User", "email": email24, "password": pwd24})
    
    make_request("/api/login", data={"email": email24, "password": "WrongPassword"})
    make_request("/api/login", data={"email": email24, "password": "WrongPassword"})
    
    user_data = query_db("SELECT login_attempts, locked_until FROM users WHERE email = ?", (email24,))
    attempts24 = user_data[0][0] if user_data else -1
    locked24 = user_data[0][1] if user_data else None
    print(f"  - DB sau 2 lần đăng nhập sai: attempts = {attempts24}, locked_until = {locked24}")
    
    status, res = make_request("/api/login", data={"email": email24, "password": pwd24})
    print(f"  - Đăng nhập lần 3 bằng mật khẩu đúng: HTTP {status} | {res.get('message', res)}")
    if status == 200 and not locked24:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Tài khoản bị khóa hoặc đăng nhập thất bại sau 2 lần sai)")

    # 11. TC-LOGIN-024: Reset attempts on success when interleaved
    print("\n[TC-LOGIN-024] Kiểm tra đặt lại bộ đếm đăng nhập sai khi đăng nhập đúng xen kẽ")
    email25 = "test_tc25@eshop.com"
    pwd25 = "ValidPassword1!"
    execute_db("DELETE FROM users WHERE email = ?", (email25,))
    make_request("/api/register", data={"name": "TC25 User", "email": email25, "password": pwd25})
    
    make_request("/api/login", data={"email": email25, "password": "WrongPassword"})
    make_request("/api/login", data={"email": email25, "password": "WrongPassword"})
    status, res = make_request("/api/login", data={"email": email25, "password": pwd25})
    
    user_data = query_db("SELECT login_attempts FROM users WHERE email = ?", (email25,))
    attempts25_post_success = user_data[0][0] if user_data else -1
    print(f"  - login_attempts sau khi đăng nhập đúng: {attempts25_post_success}")
    
    make_request("/api/login", data={"email": email25, "password": "WrongPassword"})
    make_request("/api/login", data={"email": email25, "password": "WrongPassword"})
    
    user_data = query_db("SELECT locked_until FROM users WHERE email = ?", (email25,))
    locked25 = user_data[0][0] if user_data else None
    print(f"  - locked_until sau 2 lần sai tiếp theo: {locked25}")
    if attempts25_post_success == 0 and not locked25:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # 12. TC-LOGIN-025: Lockout duration boundary
    print("\n[TC-LOGIN-025] Kiểm tra biên thời gian khóa (không mở khóa tự động ở giây thứ 29)")
    email26 = "test_tc26@eshop.com"
    pwd26 = "ValidPassword1!"
    execute_db("DELETE FROM users WHERE email = ?", (email26,))
    make_request("/api/register", data={"name": "TC26 User", "email": email26, "password": pwd26})
    
    make_request("/api/login", data={"email": email26, "password": "WrongPassword"})
    make_request("/api/login", data={"email": email26, "password": "WrongPassword"})
    make_request("/api/login", data={"email": email26, "password": "WrongPassword"})
    
    user_data = query_db("SELECT locked_until FROM users WHERE email = ?", (email26,))
    locked_until26 = user_data[0][0] if user_data else None
    if locked_until26:
        try:
            iso_str = locked_until26.replace("Z", "").split(".")[0]
            lock_epoch = time.mktime(time.strptime(iso_str, "%Y-%m-%dT%H:%M:%S"))
            duration = lock_epoch - time.mktime(time.gmtime())
            print(f"  - Thời gian khóa tính từ DB: {round(duration)} giây.")
            status, res = make_request("/api/login", data={"email": email26, "password": pwd26})
            print(f"  - Thử đăng nhập đúng ngay lập tức (giây thứ 1-29): HTTP {status} | {res}")
            if status == 403 and 25 <= duration <= 35:
                print("  => KẾT QUẢ: PASSED")
            else:
                if status == 403:
                    print("  => KẾT QUẢ: FAILED (Tài khoản vẫn bị khóa ở 29s nhưng tổng thời gian khóa sai - 180s thay vì 30s)")
                else:
                    print("  => KẾT QUẢ: FAILED (Không bị khóa hoặc trả về sai mã lỗi)")
        except Exception as e:
            print(f"  - Lỗi phân tích: {e}")
            print("  => KẾT QUẢ: FAILED")
    else:
        print("  => KẾT QUẢ: FAILED (Tài khoản chưa bị khóa)")

    # 13. TC-LOGIN-026: Block JWT token creation in locked state
    print("\n[TC-LOGIN-026] Chặn tạo mới token JWT khi đang đăng nhập đúng trong thời gian khóa")
    email27 = "test_tc27@eshop.com"
    pwd27 = "ValidPassword1!"
    execute_db("DELETE FROM users WHERE email = ?", (email27,))
    make_request("/api/register", data={"name": "TC27 User", "email": email27, "password": pwd27})
    
    make_request("/api/login", data={"email": email27, "password": "WrongPassword"})
    make_request("/api/login", data={"email": email27, "password": "WrongPassword"})
    make_request("/api/login", data={"email": email27, "password": "WrongPassword"})
    
    status, res = make_request("/api/login", data={"email": email27, "password": pwd27})
    print(f"  - Phản hồi login đúng khi khóa: HTTP {status} | {res}")
    if status == 403 and "token" not in res:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Trả về token hoặc sai mã HTTP)")

    # 14. TC-LOGIN-027: Multi-client lockout synchronization
    print("\n[TC-LOGIN-027] Đồng bộ trạng thái khóa tài khoản khi có nhiều thiết bị/phiên truy cập đồng thời")
    email28 = "test_tc28@eshop.com"
    pwd28 = "ValidPassword1!"
    execute_db("DELETE FROM users WHERE email = ?", (email28,))
    make_request("/api/register", data={"name": "TC28 User", "email": email28, "password": pwd28})
    
    make_request("/api/login", data={"email": email28, "password": "WrongPassword"})
    make_request("/api/login", data={"email": email28, "password": "WrongPassword"})
    make_request("/api/login", data={"email": email28, "password": "WrongPassword"})
    
    status, res = make_request("/api/login", data={"email": email28, "password": pwd28}, headers_override={"User-Agent": "Different Client B"})
    print(f"  - Client B đăng nhập đúng: HTTP {status} | {res}")
    if status == 403:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # 15. TC-LOGIN-028: Mixed casing email login and lockout check
    print("\n[TC-LOGIN-028] Kiểm tra đăng nhập với email viết hoa/thường xen kẽ")
    email29 = "test_tc29@eshop.com"
    mixed_email29 = "TeSt_tC29@eShOp.CoM"
    pwd29 = "ValidPassword1!"
    execute_db("DELETE FROM users WHERE email = ?", (email29,))
    make_request("/api/register", data={"name": "TC29 User", "email": email29, "password": pwd29})
    
    status, res = make_request("/api/login", data={"email": mixed_email29, "password": pwd29})
    print(f"  - Đăng nhập đúng với email mixed case: HTTP {status} | {res.get('message', res)}")
    
    make_request("/api/login", data={"email": mixed_email29, "password": "WrongPassword"})
    make_request("/api/login", data={"email": mixed_email29, "password": "WrongPassword"})
    make_request("/api/login", data={"email": mixed_email29, "password": "WrongPassword"})
    
    status_lock, res_lock = make_request("/api/login", data={"email": email29, "password": pwd29})
    print(f"  - Thử đăng nhập email gốc sau 3 lần sai bằng mixed case: HTTP {status_lock} | {res_lock}")
    
    if status == 200 and status_lock == 403:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Không hỗ trợ case-insensitive email đăng nhập hoặc cơ chế khóa tương ứng)")

    # 16. TC-LOGIN-029: Failed attempts counter does not increase on success
    print("\n[TC-LOGIN-029] Kiểm tra bộ đếm đăng nhập sai không tăng khi đăng nhập thành công")
    email30 = "test_tc30@eshop.com"
    pwd30 = "ValidPassword1!"
    execute_db("DELETE FROM users WHERE email = ?", (email30,))
    make_request("/api/register", data={"name": "TC30 User", "email": email30, "password": pwd30})
    
    status, res = make_request("/api/login", data={"email": email30, "password": pwd30})
    user_data = query_db("SELECT login_attempts FROM users WHERE email = ?", (email30,))
    attempts30 = user_data[0][0] if user_data else -1
    print(f"  - Đăng nhập: HTTP {status} | login_attempts = {attempts30}")
    if status == 200 and attempts30 == 0:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # 17. TC-LOGIN-030: Password reset clears attempts and lockout
    print("\n[TC-LOGIN-030] Đặt lại mật khẩu thành công phải giải phóng trạng thái khóa tài khoản và reset bộ đếm")
    email31 = "test_tc31@eshop.com"
    pwd31 = "ValidPassword1!"
    new_pwd31 = "NewPassword123!"
    execute_db("DELETE FROM users WHERE email = ?", (email31,))
    make_request("/api/register", data={"name": "TC31 User", "email": email31, "password": pwd31})
    
    make_request("/api/login", data={"email": email31, "password": "WrongPassword"})
    make_request("/api/login", data={"email": email31, "password": "WrongPassword"})
    make_request("/api/login", data={"email": email31, "password": "WrongPassword"})
    
    status_forgot, res_forgot = make_request("/api/forgot-password", data={"email": email31})
    token31 = res_forgot.get("resetToken")
    print(f"  - Yêu cầu đặt lại: HTTP {status_forgot} | Reset Token = {token31}")
    
    status_reset, res_reset = make_request("/api/reset-password", data={"email": email31, "resetToken": token31, "newPassword": new_pwd31})
    print(f"  - Cập nhật mật khẩu mới: HTTP {status_reset} | {res_reset}")
    
    status_login, res_login = make_request("/api/login", data={"email": email31, "password": new_pwd31})
    
    user_data = query_db("SELECT login_attempts, locked_until FROM users WHERE email = ?", (email31,))
    attempts31 = user_data[0][0] if user_data else -1
    locked31 = user_data[0][1] if user_data else None
    print(f"  - Đăng nhập bằng mật khẩu mới ngay lập tức: HTTP {status_login} | attempts = {attempts31}, locked_until = {locked31}")
    
    if status_login == 200 and attempts31 == 0 and not locked31:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Đặt lại mật khẩu thành công nhưng tài khoản vẫn bị khóa)")

if __name__ == "__main__":
    run_advanced_tests()
