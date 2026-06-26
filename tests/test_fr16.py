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

def get_product_count():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def run_tests():
    print("=" * 60)
    print("KỊCH BẢN KIỂM THỬ FR-16: IMPORT SẢN PHẨM TỪ CSV")
    print("=" * 60)
    
    # 0. SETUP: Đăng nhập Admin
    print("\n[Setup] Đăng nhập tài khoản admin...")
    status, res = make_request("/api/login", data={
        "email": "admin@eshop.com",
        "password": "Admin123!"
    })
    token = res.get("token")
    if not token:
        print("  => LỖI: Đăng nhập admin thất bại!")
        return
    print(f"  - Đăng nhập thành công. Token: {token[:20]}...")

    # Dọn dẹp sản phẩm import trước khi test
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE name LIKE 'Imported %' OR name LIKE 'Sản phẩm %'")
    conn.commit()
    conn.close()

    # 1. TC-IMPORT-001: Import thành công file CSV hợp lệ
    print("\n[TC-IMPORT-001] Import thành công file CSV hợp lệ gồm nhiều dòng sản phẩm")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported SP Hợp Lệ 1", "price": 150000, "description": "Mô tả A", "imageUrl": "", "category_id": 1},
            {"name": "Imported SP Hợp Lệ 2", "price": 200000, "description": "Mô tả B", "imageUrl": "", "category_id": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    if status == 200 and final_count - initial_count == 2:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Lỗi import)")

    # 2. TC-IMPORT-005: Từ chối import khi có dòng có name rỗng
    print("\n[TC-IMPORT-005] Từ chối import khi có dòng sản phẩm có name rỗng")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "", "price": 150000, "description": "Mô tả A", "imageUrl": "", "category_id": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    # Mong đợi: Từ chối đăng ký (HTTP 400), CSDL không thay đổi
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép bỏ qua hàng lỗi hoặc trả về HTTP 200)")

    # 3. TC-IMPORT-006: Từ chối import khi có dòng có price = 0
    print("\n[TC-IMPORT-006] Từ chối import khi có dòng sản phẩm có price bằng 0")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported SP Giá Không", "price": 0, "description": "Mô tả", "imageUrl": "", "category_id": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép giá bằng 0)")

    # 4. TC-IMPORT-007: Từ chối import khi có dòng có price là số âm
    print("\n[TC-IMPORT-007] Từ chối import khi có dòng sản phẩm có price là số âm")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported SP Giá Âm", "price": -50000, "description": "Mô tả", "imageUrl": "", "category_id": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép lưu giá trị âm)")

    # 5. TC-IMPORT-008: Từ chối import khi có dòng có price không phải số
    print("\n[TC-IMPORT-008] Từ chối import khi có dòng sản phẩm có price chứa ký tự chữ")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported SP Giá Chữ", "price": "abc", "description": "Mô tả", "imageUrl": "", "category_id": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Chấp nhận giá trị không phải số)")

    # 6. TC-IMPORT-009: Kiểm tra tính nguyên tử (Atomicity / Rollback)
    print("\n[TC-IMPORT-009] Rollback toàn bộ import khi có ít nhất một dòng bị lỗi (Atomicity)")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported Atomicity Dòng 1", "price": 100000, "description": "Dòng 1", "imageUrl": "", "category_id": 1},
            {"name": "", "price": 120000, "description": "Dòng 2 bị lỗi", "imageUrl": "", "category_id": 1},
            {"name": "Imported Atomicity Dòng 3", "price": 150000, "description": "Dòng 3", "imageUrl": "", "category_id": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    # Mong đợi: Thất bại toàn bộ, số lượng trước và sau phải bằng nhau (không có dòng nào được lưu).
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Thiếu tính giao dịch nguyên tử - Atomicity, sản phẩm vẫn được ghi dù có lỗi)")

    # Dọn dẹp sau khi kiểm thử
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE name LIKE 'Imported %'")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    run_tests()
