# -*- coding: utf-8 -*-
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

def make_request(path, method="PUT", data=None, token=None):
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
    print("KỊCH BẢN KIỂM THỬ FR-26: QUẢN LÝ HỒ SƠ CÁ NHÂN (PERSONAL PROFILE)")
    print("=" * 60)
    
    # -------------------------------------------------------------
    # 0. SETUP: ĐĂNG KÝ VÀ LẤY JWT TOKEN CỦA USER THỬ NGHIỆM
    # -------------------------------------------------------------
    email_user = "profile_test@eshop.com"
    password = "Test1234!"
    
    print("\n[Setup] Đăng ký và đăng nhập tài khoản thử nghiệm...")
    execute_db_write("DELETE FROM users WHERE email = ?", (email_user,))
    
    status, res = make_request("/api/register", method="POST", data={
        "name": "Profile Tester Original",
        "email": email_user,
        "password": password
    })
    print(f"  - Đăng ký user: HTTP {status} | {res.get('message', res.get('error'))}")
    
    status, res = make_request("/api/login", method="POST", data={
        "email": email_user,
        "password": password
    })
    
    token = res.get("token")
    user_id = res.get("user", {}).get("id")
    print(f"  - Đăng nhập thành công. User ID: {user_id} | Token: {token[:20]}..." if token else "  - Đăng nhập thất bại!")
    
    # Hàm reset thông tin user về trạng thái ban đầu sạch sẽ để chạy từng test case độc lập
    def reset_user():
        execute_db_write("UPDATE users SET name = 'Profile Tester Original', shipping_address = 'Address Original', phone = '0987654321', role = 'user' WHERE id = ?", (user_id,))

    # -------------------------------------------------------------
    # 1. TC-PROFILE-001: Thông tin hợp lệ
    # -------------------------------------------------------------
    print("\n[TC-PROFILE-001] Cập nhật với thông tin hợp lệ")
    reset_user()
    status, res = make_request("/api/users/me", method="PUT", data={
        "name": "Nguyen Van A",
        "shipping_address": "123 Duong Le Loi, Q1, HCM",
        "phone": "0912345678"
    }, token=token)
    
    print(f"  - Phản hồi: HTTP {status} | {res}")
    db_val = query_db("SELECT name, shipping_address, phone FROM users WHERE id = ?", (user_id,))[0]
    print(f"  - Dữ liệu trong CSDL: name='{db_val[0]}', address='{db_val[1]}', phone='{db_val[2]}'")
    if status == 200 and db_val[0] == "Nguyen Van A" and db_val[1] == "123 Duong Le Loi, Q1, HCM" and db_val[2] == "0912345678":
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # -------------------------------------------------------------
    # 2. TC-PROFILE-002: Họ Tên rỗng
    # -------------------------------------------------------------
    print("\n[TC-PROFILE-002] Họ Tên rỗng")
    reset_user()
    status, res = make_request("/api/users/me", method="PUT", data={
        "name": "",
        "shipping_address": "Address Original",
        "phone": "0987654321"
    }, token=token)
    
    print(f"  - Phản hồi: HTTP {status} | {res}")
    db_val = query_db("SELECT name FROM users WHERE id = ?", (user_id,))[0][0]
    print(f"  - CSDL Họ Tên: '{db_val}'")
    if status == 400 and db_val == "Profile Tester Original":
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép Họ Tên rỗng)")

    # -------------------------------------------------------------
    # 3. TC-PROFILE-003: Họ Tên quá ngắn (1 ký tự)
    # -------------------------------------------------------------
    print("\n[TC-PROFILE-003] Họ Tên quá ngắn (1 ký tự)")
    reset_user()
    status, res = make_request("/api/users/me", method="PUT", data={
        "name": "A",
        "shipping_address": "Address Original",
        "phone": "0987654321"
    }, token=token)
    
    print(f"  - Phản hồi: HTTP {status} | {res}")
    db_val = query_db("SELECT name FROM users WHERE id = ?", (user_id,))[0][0]
    print(f"  - CSDL Họ Tên: '{db_val}'")
    if status == 400 and db_val == "Profile Tester Original":
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép Họ Tên chỉ 1 ký tự)")

    # -------------------------------------------------------------
    # 4. TC-PROFILE-004: Họ Tên quá dài (101 ký tự)
    # -------------------------------------------------------------
    print("\n[TC-PROFILE-004] Họ Tên quá dài (101 ký tự)")
    reset_user()
    long_name = "A" * 101
    status, res = make_request("/api/users/me", method="PUT", data={
        "name": long_name,
        "shipping_address": "Address Original",
        "phone": "0987654321"
    }, token=token)
    
    print(f"  - Phản hồi: HTTP {status} | {res}")
    db_val = query_db("SELECT name FROM users WHERE id = ?", (user_id,))[0][0]
    if status == 400 and db_val == "Profile Tester Original":
        print("  => KẾT QUẢ: PASSED")
    else:
        print(f"  => KẾT QUẢ: FAILED (Bug: Cho phép Họ Tên dài 101 ký tự. Đã lưu: {len(db_val)} ký tự)")

    # -------------------------------------------------------------
    # 5. TC-PROFILE-005: Họ Tên chứa số
    # -------------------------------------------------------------
    print("\n[TC-PROFILE-005] Họ Tên chứa chữ số")
    reset_user()
    status, res = make_request("/api/users/me", method="PUT", data={
        "name": "Nguyen Van A 123",
        "shipping_address": "Address Original",
        "phone": "0987654321"
    }, token=token)
    
    print(f"  - Phản hồi: HTTP {status} | {res}")
    db_val = query_db("SELECT name FROM users WHERE id = ?", (user_id,))[0][0]
    print(f"  - CSDL Họ Tên: '{db_val}'")
    if status == 400 and db_val == "Profile Tester Original":
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép Họ Tên chứa số)")

    # -------------------------------------------------------------
    # 6. TC-PROFILE-006: Họ Tên chứa ký tự đặc biệt
    # -------------------------------------------------------------
    print("\n[TC-PROFILE-006] Họ Tên chứa ký tự đặc biệt")
    reset_user()
    status, res = make_request("/api/users/me", method="PUT", data={
        "name": "Nguyen@Van_A",
        "shipping_address": "Address Original",
        "phone": "0987654321"
    }, token=token)
    
    print(f"  - Phản hồi: HTTP {status} | {res}")
    db_val = query_db("SELECT name FROM users WHERE id = ?", (user_id,))[0][0]
    print(f"  - CSDL Họ Tên: '{db_val}'")
    if status == 400 and db_val == "Profile Tester Original":
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép Họ Tên chứa ký tự đặc biệt)")

    # -------------------------------------------------------------
    # 7. TC-PROFILE-007: Stored XSS trong Họ Tên
    # -------------------------------------------------------------
    print("\n[TC-PROFILE-007] Họ Tên chứa mã độc Stored XSS")
    reset_user()
    xss_payload = "<script>alert('XSS')</script>"
    status, res = make_request("/api/users/me", method="PUT", data={
        "name": xss_payload,
        "shipping_address": "Address Original",
        "phone": "0987654321"
    }, token=token)
    
    print(f"  - Phản hồi: HTTP {status} | {res}")
    db_val = query_db("SELECT name FROM users WHERE id = ?", (user_id,))[0][0]
    print(f"  - CSDL Họ Tên: '{db_val}'")
    if status == 400 and db_val == "Profile Tester Original":
        print("  => KẾT QUẢ: PASSED")
    elif xss_payload in db_val:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép lưu trữ trực tiếp thẻ script HTML độc hại vào database)")
    else:
        print("  => KẾT QUẢ: PASSED (Có chuẩn hóa/mã hóa an toàn)")

    # -------------------------------------------------------------
    # 8. TC-PROFILE-008: SQL Injection trong Họ Tên
    # -------------------------------------------------------------
    print("\n[TC-PROFILE-008] Họ Tên chứa payload SQL Injection")
    reset_user()
    sqli_payload = "' OR 1=1 --"
    status, res = make_request("/api/users/me", method="PUT", data={
        "name": sqli_payload,
        "shipping_address": "Address Original",
        "phone": "0987654321"
    }, token=token)
    
    print(f"  - Phản hồi: HTTP {status} | {res}")
    db_val = query_db("SELECT name FROM users WHERE id = ?", (user_id,))[0][0]
    print(f"  - CSDL Họ Tên: '{db_val}'")
    if status == 400 and db_val == "Profile Tester Original":
        print("  => KẾT QUẢ: PASSED")
    elif sqli_payload in db_val:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép lưu trữ payload SQL Injection nguyên bản vào database)")
    else:
        print("  => KẾT QUẢ: PASSED (Có xử lý an toàn)")

    # -------------------------------------------------------------
    # 9. TC-PROFILE-009: Số điện thoại trống
    # -------------------------------------------------------------
    print("\n[TC-PROFILE-009] Số điện thoại trống")
    reset_user()
    status, res = make_request("/api/users/me", method="PUT", data={
        "name": "Nguyen Van A",
        "shipping_address": "Address Original",
        "phone": ""
    }, token=token)
    
    print(f"  - Phản hồi: HTTP {status} | {res}")
    db_val = query_db("SELECT phone FROM users WHERE id = ?", (user_id,))[0][0]
    print(f"  - CSDL Số điện thoại: '{db_val}'")
    if status == 400 and db_val == "0987654321":
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép Số điện thoại trống)")

    # -------------------------------------------------------------
    # 10. TC-PROFILE-010: Số điện thoại không bắt đầu bằng số 0
    # -------------------------------------------------------------
    print("\n[TC-PROFILE-010] Số điện thoại không bắt đầu bằng số 0")
    reset_user()
    status, res = make_request("/api/users/me", method="PUT", data={
        "name": "Nguyen Van A",
        "shipping_address": "Address Original",
        "phone": "1912345678"
    }, token=token)
    
    print(f"  - Phản hồi: HTTP {status} | {res}")
    db_val = query_db("SELECT phone FROM users WHERE id = ?", (user_id,))[0][0]
    print(f"  - CSDL Số điện thoại: '{db_val}'")
    if status == 400 and db_val == "0987654321":
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép Số điện thoại không bắt đầu bằng 0)")

    # -------------------------------------------------------------
    # 11. TC-PROFILE-011: Số điện thoại ngắn hơn 10 chữ số (9 chữ số)
    # -------------------------------------------------------------
    print("\n[TC-PROFILE-011] Số điện thoại ngắn hơn 10 chữ số (9 chữ số)")
    reset_user()
    status, res = make_request("/api/users/me", method="PUT", data={
        "name": "Nguyen Van A",
        "shipping_address": "Address Original",
        "phone": "091234567"
    }, token=token)
    
    print(f"  - Phản hồi: HTTP {status} | {res}")
    db_val = query_db("SELECT phone FROM users WHERE id = ?", (user_id,))[0][0]
    print(f"  - CSDL Số điện thoại: '{db_val}'")
    if status == 400 and db_val == "0987654321":
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép Số điện thoại chỉ có 9 chữ số)")

    # -------------------------------------------------------------
    # 12. TC-PROFILE-012: Số điện thoại dài hơn 11 chữ số (12 chữ số)
    # -------------------------------------------------------------
    print("\n[TC-PROFILE-012] Số điện thoại dài hơn 11 chữ số (12 chữ số)")
    reset_user()
    status, res = make_request("/api/users/me", method="PUT", data={
        "name": "Nguyen Van A",
        "shipping_address": "Address Original",
        "phone": "091234567890"
    }, token=token)
    
    print(f"  - Phản hồi: HTTP {status} | {res}")
    db_val = query_db("SELECT phone FROM users WHERE id = ?", (user_id,))[0][0]
    print(f"  - CSDL Số điện thoại: '{db_val}'")
    if status == 400 and db_val == "0987654321":
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép Số điện thoại dài 12 chữ số)")

    # -------------------------------------------------------------
    # 13. TC-PROFILE-013: Số điện thoại chứa chữ cái
    # -------------------------------------------------------------
    print("\n[TC-PROFILE-013] Số điện thoại chứa chữ cái")
    reset_user()
    status, res = make_request("/api/users/me", method="PUT", data={
        "name": "Nguyen Van A",
        "shipping_address": "Address Original",
        "phone": "091234567a"
    }, token=token)
    
    print(f"  - Phản hồi: HTTP {status} | {res}")
    db_val = query_db("SELECT phone FROM users WHERE id = ?", (user_id,))[0][0]
    print(f"  - CSDL Số điện thoại: '{db_val}'")
    if status == 400 and db_val == "0987654321":
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép Số điện thoại chứa ký tự không phải số)")

    # -------------------------------------------------------------
    # 14. TC-PROFILE-014: Số điện thoại chứa khoảng trắng
    # -------------------------------------------------------------
    print("\n[TC-PROFILE-014] Số điện thoại chứa khoảng trắng")
    reset_user()
    status, res = make_request("/api/users/me", method="PUT", data={
        "name": "Nguyen Van A",
        "shipping_address": "Address Original",
        "phone": "0912 345 678"
    }, token=token)
    
    print(f"  - Phản hồi: HTTP {status} | {res}")
    db_val = query_db("SELECT phone FROM users WHERE id = ?", (user_id,))[0][0]
    print(f"  - CSDL Số điện thoại: '{db_val}'")
    if status == 400 and db_val == "0987654321":
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép Số điện thoại chứa khoảng trắng)")

    # -------------------------------------------------------------
    # 15. TC-PROFILE-015: Địa chỉ giao hàng trống
    # -------------------------------------------------------------
    print("\n[TC-PROFILE-015] Địa chỉ giao hàng trống")
    reset_user()
    status, res = make_request("/api/users/me", method="PUT", data={
        "name": "Nguyen Van A",
        "shipping_address": "",
        "phone": "0987654321"
    }, token=token)
    
    print(f"  - Phản hồi: HTTP {status} | {res}")
    db_val = query_db("SELECT shipping_address FROM users WHERE id = ?", (user_id,))[0][0]
    print(f"  - CSDL Địa chỉ: '{db_val}'")
    if status == 400 and db_val == "Address Original":
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép Địa chỉ giao hàng trống)")

    # -------------------------------------------------------------
    # 16. TC-PROFILE-016: Thay đổi role của bản thân thành admin
    # -------------------------------------------------------------
    print("\n[TC-PROFILE-016] Tự thay đổi thuộc tính role thành admin")
    reset_user()
    status, res = make_request("/api/users/me", method="PUT", data={
        "name": "Nguyen Van A",
        "shipping_address": "Address Original",
        "phone": "0987654321",
        "role": "admin"
    }, token=token)
    
    print(f"  - Phản hồi: HTTP {status} | {res}")
    db_val = query_db("SELECT role FROM users WHERE id = ?", (user_id,))[0][0]
    print(f"  - CSDL Quyền hạn (role): '{db_val}'")
    if db_val == "user":
        print("  => KẾT QUẢ: PASSED (Giữ nguyên role 'user' thành công)")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép người dùng tự thay đổi thuộc tính role)")

    # -------------------------------------------------------------
    # 17. TC-PROFILE-017: Thay đổi email của bản thân
    # -------------------------------------------------------------
    print("\n[TC-PROFILE-017] Thay đổi email của bản thân")
    reset_user()
    status, res = make_request("/api/users/me", method="PUT", data={
        "name": "Nguyen Van A",
        "shipping_address": "Address Original",
        "phone": "0987654321",
        "email": "new_email@eshop.com"
    }, token=token)
    
    print(f"  - Phản hồi: HTTP {status} | {res}")
    db_val = query_db("SELECT email FROM users WHERE id = ?", (user_id,))[0][0]
    print(f"  - CSDL Email: '{db_val}'")
    if db_val == email_user:
        print("  => KẾT QUẢ: PASSED (Không thay đổi email)")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép thay đổi email qua API cập nhật hồ sơ)")

    # -------------------------------------------------------------
    # 18. TC-PROFILE-018: Stored XSS trong Địa chỉ giao hàng
    # -------------------------------------------------------------
    print("\n[TC-PROFILE-018] Địa chỉ giao hàng chứa mã độc Stored XSS")
    reset_user()
    xss_addr = "<script>alert('XSS_addr')</script>"
    status, res = make_request("/api/users/me", method="PUT", data={
        "name": "Nguyen Van A",
        "shipping_address": xss_addr,
        "phone": "0987654321"
    }, token=token)
    
    print(f"  - Phản hồi: HTTP {status} | {res}")
    db_val = query_db("SELECT shipping_address FROM users WHERE id = ?", (user_id,))[0][0]
    print(f"  - CSDL Địa chỉ: '{db_val}'")
    if status == 400 and db_val == "Address Original":
        print("  => KẾT QUẢ: PASSED")
    elif xss_addr in db_val:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép lưu trữ trực tiếp mã độc HTML/XSS trong địa chỉ giao hàng)")
    else:
        print("  => KẾT QUẢ: PASSED")

    # -------------------------------------------------------------
    # 19. TC-PROFILE-019: SQL Injection trong Địa chỉ giao hàng
    # -------------------------------------------------------------
    print("\n[TC-PROFILE-019] Địa chỉ giao hàng chứa payload SQL Injection")
    reset_user()
    sqli_addr = "' OR 1=1 --"
    status, res = make_request("/api/users/me", method="PUT", data={
        "name": "Nguyen Van A",
        "shipping_address": sqli_addr,
        "phone": "0987654321"
    }, token=token)
    
    print(f"  - Phản hồi: HTTP {status} | {res}")
    db_val = query_db("SELECT shipping_address FROM users WHERE id = ?", (user_id,))[0][0]
    print(f"  - CSDL Địa chỉ: '{db_val}'")
    if status == 400 and db_val == "Address Original":
        print("  => KẾT QUẢ: PASSED")
    elif sqli_addr in db_val:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép lưu trữ payload SQL Injection nguyên bản trong địa chỉ giao hàng)")
    else:
        print("  => KẾT QUẢ: PASSED")

    # Dọn dẹp
    execute_db_write("DELETE FROM users WHERE id = ?", (user_id,))

if __name__ == "__main__":
    run_tests()
