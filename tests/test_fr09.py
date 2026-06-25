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
# Tự động xác định đường dẫn DB tuyệt đối dựa trên vị trí của file script hiện tại
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "backend", "database.sqlite"))

def make_request(path, method="POST", data=None, token=None):
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
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

def execute_db_write(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def run_tests():
    print("=" * 60)
    print("KỊCH BẢN KIỂM THỬ FR-09: MÃ GIẢM GIÁ (COUPONS)")
    print("=" * 60)
    
    # -------------------------------------------------------------
    # 0. SETUP: ĐĂNG KÝ VÀ LẤY JWT TOKEN ĐỂ THỬ NGHIỆM
    # -------------------------------------------------------------
    email_user = "fr09_test@eshop.com"
    password = "Test1234!"
    
    print("\n[Setup] Đăng ký và đăng nhập tài khoản thử nghiệm...")
    # Xóa lịch sử sử dụng coupon của user này nếu có từ trước
    execute_db_write("DELETE FROM coupon_usage WHERE user_id IN (SELECT id FROM users WHERE email = ?)", (email_user,))
    execute_db_write("DELETE FROM users WHERE email = ?", (email_user,))
    
    status, res = make_request("/api/register", data={
        "name": "FR09 Coupon Tester",
        "email": email_user,
        "password": password
    })
    print(f"  - Đăng ký user: HTTP {status} | {res.get('message', res.get('error'))}")
    
    status, res = make_request("/api/login", data={
        "email": email_user,
        "password": password
    })
    
    token = res.get("token")
    user_id = res.get("user", {}).get("id")
    print(f"  - Đăng nhập thành công. User ID: {user_id} | Token: {token[:20]}..." if token else "  - Đăng nhập thất bại!")
    
    # -------------------------------------------------------------
    # 1. TC-COUPON-001: Áp dụng mã giảm giá SAVE10 (10%) thành công với giá trị đơn hàng đạt ngưỡng tối thiểu biên dưới (300,000 VND)
    # -------------------------------------------------------------
    print("\n[TC-COUPON-001] Áp dụng SAVE10 tại ngưỡng 300,000 VND (Biên dưới)")
    status, res = make_request("/api/apply-coupon", data={
        "code": "SAVE10",
        "total_amount": 300000,
        "user_id": user_id
    }, token=token)
    
    # KỲ VỌNG: HTTP 200, success: true, discount_amount = 30000, final_amount = 270000
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status == 200 and res.get("success") is True:
        discount = res.get("discount_amount")
        final = res.get("final_amount")
        if discount == 30000 and final == 270000:
            print("  => KẾT QUẢ: PASSED")
        else:
            print(f"  => KẾT QUẢ: FAILED (Sai lệch giá trị: discount={discount}, final={final})")
    else:
        print("  => KẾT QUẢ: FAILED")

    # -------------------------------------------------------------
    # 2. TC-COUPON-002: Áp dụng SAVE10 thất bại do giá trị đơn hàng dưới ngưỡng tối thiểu biên dưới 1 đơn vị (299,999 VND)
    # -------------------------------------------------------------
    print("\n[TC-COUPON-002] Áp dụng SAVE10 tại 299,999 VND (Dưới biên)")
    status, res = make_request("/api/apply-coupon", data={
        "code": "SAVE10",
        "total_amount": 299999,
        "user_id": user_id
    }, token=token)
    
    # KỲ VỌNG: HTTP 400, có lỗi
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status == 400 and "error" in res:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # -------------------------------------------------------------
    # 3. TC-COUPON-003: Áp dụng SAVE10 thành công với giá trị đơn hàng trên ngưỡng tối thiểu biên dưới 1 đơn vị (300,001 VND)
    # -------------------------------------------------------------
    print("\n[TC-COUPON-003] Áp dụng SAVE10 tại 300,001 VND (Trên biên)")
    status, res = make_request("/api/apply-coupon", data={
        "code": "SAVE10",
        "total_amount": 300001,
        "user_id": user_id
    }, token=token)
    
    # KỲ VỌNG: HTTP 200, success: true, discount_amount = 30000 (làm tròn từ 30000.1), final_amount = 270001
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status == 200 and res.get("success") is True:
        discount = res.get("discount_amount")
        final = res.get("final_amount")
        if discount == 30000 and final == 270001:
            print("  => KẾT QUẢ: PASSED")
        else:
            print(f"  => KẾT QUẢ: FAILED (Sai lệch giá trị: discount={discount}, final={final})")
    else:
        print("  => KẾT QUẢ: FAILED")

    # -------------------------------------------------------------
    # 4. TC-COUPON-004: Áp dụng mã giảm giá cố định BIGBUY thành công với giá trị đơn hàng đạt ngưỡng tối thiểu biên dưới (500,000 VND)
    # -------------------------------------------------------------
    print("\n[TC-COUPON-004] Áp dụng BIGBUY tại ngưỡng 500,000 VND (Biên dưới)")
    status, res = make_request("/api/apply-coupon", data={
        "code": "BIGBUY",
        "total_amount": 500000,
        "user_id": user_id
    }, token=token)
    
    # KỲ VỌNG: HTTP 200, success: true, discount_amount = 50000, final_amount = 450000
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status == 200 and res.get("success") is True:
        discount = res.get("discount_amount")
        final = res.get("final_amount")
        if discount == 50000 and final == 450000:
            print("  => KẾT QUẢ: PASSED")
        else:
            print(f"  => KẾT QUẢ: FAILED (Sai lệch giá trị: discount={discount}, final={final})")
    else:
        print("  => KẾT QUẢ: FAILED")

    # -------------------------------------------------------------
    # 5. TC-COUPON-005: Áp dụng BIGBUY thất bại do giá trị đơn hàng dưới ngưỡng tối thiểu biên dưới 1 đơn vị (499,999 VND)
    # -------------------------------------------------------------
    print("\n[TC-COUPON-005] Áp dụng BIGBUY tại 499,999 VND (Dưới biên)")
    status, res = make_request("/api/apply-coupon", data={
        "code": "BIGBUY",
        "total_amount": 499999,
        "user_id": user_id
    }, token=token)
    
    # KỲ VỌNG: HTTP 400, có lỗi
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status == 400 and "error" in res:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # -------------------------------------------------------------
    # 6. TC-COUPON-006: Áp dụng mã giảm giá thất bại do mã đã hết hạn sử dụng (EXPIRED)
    # -------------------------------------------------------------
    print("\n[TC-COUPON-006] Áp dụng EXPIRED (Hết hạn)")
    status, res = make_request("/api/apply-coupon", data={
        "code": "EXPIRED",
        "total_amount": 150000,
        "user_id": user_id
    }, token=token)
    
    # KỲ VỌNG: HTTP 400, có lỗi báo hết hạn
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status == 400 and "error" in res:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # -------------------------------------------------------------
    # 7. TC-COUPON-007: Áp dụng mã giảm giá thất bại do mã không tồn tại trong hệ thống (NONEXIST)
    # -------------------------------------------------------------
    print("\n[TC-COUPON-007] Áp dụng mã giảm giá không tồn tại")
    status, res = make_request("/api/apply-coupon", data={
        "code": "NONEXIST",
        "total_amount": 300000,
        "user_id": user_id
    }, token=token)
    
    # KỲ VỌNG: HTTP 404, báo mã không tồn tại
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status == 404 and "error" in res:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # -------------------------------------------------------------
    # 8. TC-COUPON-008: Áp dụng mã giảm giá thất bại do người dùng chưa đăng nhập (Không truyền token JWT)
    # -------------------------------------------------------------
    print("\n[TC-COUPON-008] Áp dụng mã giảm giá khi chưa đăng nhập (Cần xác thực JWT)")
    status, res = make_request("/api/apply-coupon", data={
        "code": "SAVE10",
        "total_amount": 350000,
        "user_id": None
    })
    
    # KỲ VỌNG: HTTP 401 Unauthorized
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status == 401 and "error" in res:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # -------------------------------------------------------------
    # 9. TC-COUPON-009: Áp dụng mã giảm giá VIP100 thất bại do người dùng đã dùng hết số lần tối đa (2 lần)
    # -------------------------------------------------------------
    print("\n[TC-COUPON-009] Áp dụng VIP100 khi đã dùng 2 lần (Đạt giới hạn)")
    # Giả lập ghi nhận 2 lần sử dụng VIP100 cho user_id này trong DB
    coupon_id = query_db("SELECT id FROM coupons WHERE code = 'VIP100'")[0][0]
    execute_db_write("INSERT INTO coupon_usage (coupon_id, user_id) VALUES (?, ?)", (coupon_id, user_id))
    execute_db_write("INSERT INTO coupon_usage (coupon_id, user_id) VALUES (?, ?)", (coupon_id, user_id))
    
    status, res = make_request("/api/apply-coupon", data={
        "code": "VIP100",
        "total_amount": 350000,
        "user_id": user_id
    }, token=token)
    
    # KỲ VỌNG: HTTP 400, báo đạt giới hạn sử dụng
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status == 400 and "error" in res:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # -------------------------------------------------------------
    # 10. TC-COUPON-010: Áp dụng mã giảm giá VIP100 thành công khi người dùng mới sử dụng 1 lần (dưới hạn mức tối đa 2 lần)
    # -------------------------------------------------------------
    print("\n[TC-COUPON-010] Áp dụng VIP100 khi mới dùng 1 lần (Dưới giới hạn)")
    # Xóa bớt 1 lần sử dụng trong DB
    execute_db_write("DELETE FROM coupon_usage WHERE coupon_id = ? AND user_id = ?", (coupon_id, user_id))
    
    status, res = make_request("/api/apply-coupon", data={
        "code": "VIP100",
        "total_amount": 350000,
        "user_id": user_id
    }, token=token)
    
    # KỲ VỌNG: HTTP 200, success: true, discount_amount = 100000, final_amount = 250000
    print(f"  - Phản hồi: HTTP {status} | {res}")
    if status == 200 and res.get("success") is True:
        discount = res.get("discount_amount")
        final = res.get("final_amount")
        if discount == 100000 and final == 250000:
            print("  => KẾT QUẢ: PASSED")
        else:
            print(f"  => KẾT QUẢ: FAILED (Sai lệch giá trị: discount={discount}, final={final})")
    else:
        print("  => KẾT QUẢ: FAILED")

    # Dọn dẹp DB sau khi test
    execute_db_write("DELETE FROM coupon_usage WHERE user_id = ?", (user_id,))
    execute_db_write("DELETE FROM users WHERE id = ?", (user_id,))

if __name__ == "__main__":
    run_tests()
