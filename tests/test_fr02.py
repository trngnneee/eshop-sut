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

def query_db(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result

def run_tests():
    print("=" * 60)
    print("KỊCH BẢN KIỂM THỬ FR-02: ĐĂNG NHẬP & KHÓA TÀI KHOẢN")
    print("=" * 60)
    
    # -------------------------------------------------------------
    # 0. ĐĂNG KÝ TÀI KHOẢN TRƯỚC (Requirement: Đăng ký trước khi đăng nhập)
    # -------------------------------------------------------------
    email_success = "fr02_success@eshop.com"
    email_fail = "fr02_fail@eshop.com"
    password = "Test1234!"
    
    print("\n[Bước 0] Đăng ký các tài khoản thử nghiệm...")
    
    # Đăng ký tài khoản 1 (dùng cho test login thành công)
    status, res = make_request("/api/register", data={
        "name": "FR02 Success User",
        "email": email_success,
        "password": password
    })
    print(f"  - Đăng ký {email_success}: HTTP {status} | {res.get('message', res.get('error'))}")
    
    # Đăng ký tài khoản 2 (dùng cho test đếm số lần đăng nhập sai và khóa)
    status, res = make_request("/api/register", data={
        "name": "FR02 Fail User",
        "email": email_fail,
        "password": password
    })
    print(f"  - Đăng ký {email_fail}: HTTP {status} | {res.get('message', res.get('error'))}")
    
    # -------------------------------------------------------------
    # 1. TC-LOGIN-001: Đăng nhập thành công với thông tin hợp lệ
    # -------------------------------------------------------------
    print("\n[TC-LOGIN-001] Đăng nhập thành công với thông tin hợp lệ")
    status, res = make_request("/api/login", data={
        "email": email_success,
        "password": password
    })
    
    if status == 200 and "token" in res:
        print("  => KẾT QUẢ: PASSED")
        print(f"  - Token nhận được: {res['token'][:30]}...")
    else:
        print("  => KẾT QUẢ: FAILED")
        print(f"  - Phản hồi: HTTP {status} | {res}")

    # -------------------------------------------------------------
    # 2. TC-LOGIN-002: Kiểm tra tăng bộ đếm đăng nhập sai đúng 1 đơn vị
    # -------------------------------------------------------------
    print("\n[TC-LOGIN-002] Kiểm tra tăng bộ đếm đăng nhập sai")
    
    # Kiểm tra trạng thái ban đầu trong DB
    user_data = query_db("SELECT id, login_attempts, locked_until FROM users WHERE email = ?", (email_fail,))
    if not user_data:
        print("  - Lỗi: Không tìm thấy tài khoản trong Database.")
        return
    user_id, init_attempts, locked_until = user_data[0]
    print(f"  - Trạng thái ban đầu trong DB: login_attempts = {init_attempts}, locked_until = {locked_until}")
    
    # Đăng nhập sai lần 1
    print("  - Tiến hành đăng nhập sai lần 1...")
    status, res = make_request("/api/login", data={
        "email": email_fail,
        "password": "WrongPassword123!"
    })
    
    # Kiểm tra lại DB sau lần 1
    user_data = query_db("SELECT login_attempts, locked_until FROM users WHERE email = ?", (email_fail,))
    attempts_after_1, locked_until_after_1 = user_data[0]
    print(f"  - Sau lần 1 sai: login_attempts trong DB = {attempts_after_1}, locked_until = {locked_until_after_1}")
    
    # Đánh giá kết quả TC-LOGIN-002
    if attempts_after_1 == init_attempts + 1:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")
        print(f"  - BUG PHÁT HIỆN: Bộ đếm tăng thêm {attempts_after_1 - init_attempts} đơn vị thay vì 1 đơn vị!")

    # -------------------------------------------------------------
    # 3. TC-LOGIN-003: Tạm khóa tài khoản trong 30 giây sau khi đăng nhập sai 3 lần liên tiếp
    # -------------------------------------------------------------
    print("\n[TC-LOGIN-003] Kiểm tra tạm khóa tài khoản")
    
    # Vì bộ đếm tăng thêm 2 đơn vị sau lần 1 (do bug), hiện tại attempts = 2.
    # Ta thực hiện đăng nhập sai lần 2 để tăng attempts lên >= 3 và kích hoạt khóa.
    print("  - Tiến hành đăng nhập sai lần 2 (để đạt/vượt ngưỡng khóa)...")
    status, res = make_request("/api/login", data={
        "email": email_fail,
        "password": "WrongPassword123!"
    })
    
    user_data = query_db("SELECT login_attempts, locked_until FROM users WHERE email = ?", (email_fail,))
    attempts_after_2, locked_until_after_2 = user_data[0]
    print(f"  - Sau lần 2 sai: login_attempts = {attempts_after_2}, locked_until = {locked_until_after_2}")
    
    if locked_until_after_2:
        print("  - Xác nhận tài khoản ĐÃ bị khóa trong DB.")
        
        # Thử đăng nhập lại bằng thông tin đúng NGAY LẬP TỨC để xem có bị chặn không
        print("  - Thử đăng nhập bằng mật khẩu ĐÚNG ngay lập tức khi đang khóa...")
        status_correct, res_correct = make_request("/api/login", data={
            "email": email_fail,
            "password": password
        })
        print(f"  - Phản hồi: HTTP {status_correct} | {res_correct}")
        
        # Phân tích thời gian khóa
        # Lấy thời gian khóa từ DB và so sánh với thời điểm hiện tại
        try:
            locked_until_time = time.mktime(time.strptime(locked_until_after_2.split(".")[0], "%Y-%m-%dT%H:%M:%S"))
            # SQLite stores DATETIME in UTC or ISO. Let's calculate duration from locked_until - current_time
            # Note: Server uses Date.now() + 180000 or similar
            current_time = time.time()
            # Server is on local time or UTC. Let's parse locked_until_after_2 manually or check the exact duration.
            # In node: Date.now() + 180000. Let's inspect the diff from DB locked_until and time of lock.
            # Since server just updated it, we can estimate lock duration by subtracting current epoch from locked_until epoch
            # Let's calculate the duration of the lock
            # Date.now() in JS is UTC millisecond.
            # In node: lockedUntil = new Date(Date.now() + 180000).toISOString()
            # Python time.time() is UTC epoch seconds.
            # ISO timestamp: 2026-06-23T06:27:15.123Z (let's strip Z and parse)
            iso_str = locked_until_after_2.replace("Z", "")
            if "." in iso_str:
                iso_str = iso_str.split(".")[0]
            lock_epoch = time.mktime(time.strptime(iso_str, "%Y-%m-%dT%H:%M:%S"))
            # python time.timezone/altzone adjusts to local time.
            # Let's calculate difference by looking at current time in UTC
            utc_now = time.gmtime()
            utc_now_epoch = time.mktime(utc_now)
            duration = lock_epoch - utc_now_epoch
            
            print(f"  - Thời gian khóa tính toán từ DB: khoảng {round(duration)} giây.")
            if 25 <= duration <= 35:
                print("  => KẾT QUẢ THỜI GIAN KHÓA: PASSED (Khóa 30 giây)")
            else:
                print("  => KẾT QUẢ THỜI GIAN KHÓA: FAILED")
                print(f"    - BUG PHÁT HIỆN: Tài khoản bị khóa trong {round(duration)} giây (~{round(duration/60)} phút) thay vì 30 giây!")
        except Exception as e:
            print(f"  - Không thể tính toán chính xác giây khóa tự động ({e}). Trực tiếp kiểm tra giá trị trong DB: {locked_until_after_2}")
            
        if status_correct == 403:
            print("  => KẾT QUẢ CHẶN ĐĂNG NHẬP: PASSED (Bị chặn đăng nhập đúng với mã 403)")
        else:
            print("  => KẾT QUẢ CHẶN ĐĂNG NHẬP: FAILED")
    else:
        print("  => KẾT QUẢ KHÓA TÀI KHOẢN: FAILED (Tài khoản không bị khóa sau khi vượt quá 3 lần sai)")

if __name__ == "__main__":
    run_tests()
