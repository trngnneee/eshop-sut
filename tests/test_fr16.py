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

    # ============================================================
    # CÁC TEST CASES BỔ SUNG (TC-IMPORT-013 đến TC-IMPORT-026)
    # ============================================================

    # 7. TC-IMPORT-013: Từ chối import khi name chỉ chứa khoảng trắng
    print("\n[TC-IMPORT-013] Từ chối import khi name chỉ chứa khoảng trắng")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "   ", "price": 100000, "description": "Mô tả", "imageUrl": "", "category_id": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Chấp nhận tên chỉ chứa khoảng trắng)")

    # 8. TC-IMPORT-014: Import thành công khi name có độ dài bằng 255 ký tự
    print("\n[TC-IMPORT-014] Import thành công khi name có độ dài bằng 255 ký tự")
    initial_count = get_product_count()
    long_name = "Imported " + "A" * 246
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": long_name, "price": 100000, "description": "Mô tả", "imageUrl": "", "category_id": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    if status == 200 and final_count - initial_count == 1:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # 9. TC-IMPORT-015: Từ chối import khi name có độ dài bằng 256 ký tự
    print("\n[TC-IMPORT-015] Từ chối import khi name có độ dài bằng 256 ký tự")
    initial_count = get_product_count()
    too_long_name = "Imported " + "A" * 247
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": too_long_name, "price": 100000, "description": "Mô tả", "imageUrl": "", "category_id": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép tên vượt quá 255 ký tự)")

    # 10. TC-IMPORT-016: Từ chối hoặc mã hóa an toàn khi name chứa mã độc XSS
    print("\n[TC-IMPORT-016] Từ chối hoặc mã hóa an toàn khi name chứa mã độc XSS")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported <script>alert(1)</script>", "price": 100000, "description": "Mô tả", "imageUrl": "", "category_id": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    # Kiểm tra xem có bị lưu trực tiếp thẻ script không
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM products WHERE name LIKE 'Imported <script>%'")
    row = cursor.fetchone()
    conn.close()
    
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED (Từ chối)")
    elif row is not None:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép lưu trữ mã độc HTML/XSS nguyên bản vào database)")
    else:
        print("  => KẾT QUẢ: PASSED (Mã hóa)")

    # 11. TC-IMPORT-017: Từ chối khi name hoặc price chứa lệnh SQL Injection
    print("\n[TC-IMPORT-017] Từ chối khi name hoặc price chứa lệnh SQL Injection")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported Product", "price": "' OR 1=1 --", "description": "Mô tả", "imageUrl": "", "category_id": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép lưu trữ SQL Injection payload trong trường giá)")

    # 12. TC-IMPORT-018: Hệ thống xử lý hoặc từ chối khi header chứa các trường viết hoa
    print("\n[TC-IMPORT-018] Hệ thống xử lý hoặc từ chối khi header chứa các trường viết hoa")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"NAME": "Imported Caps Header", "PRICE": 120000, "DESCRIPTION": "Mô tả", "IMAGEURL": "", "CATEGORY_ID": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products WHERE name = 'Imported Caps Header'")
    ok_inserted = cursor.fetchone()[0]
    conn.close()
    
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED (Từ chối cấu trúc không hợp lệ)")
    elif status == 200 and ok_inserted == 1:
        print("  => KẾT QUẢ: PASSED (Tự động chuẩn hóa chữ thường)")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Trả về HTTP 200 nhưng tạo sản phẩm rác hoặc lỗi cấu trúc)")

    # 13. TC-IMPORT-019: Từ chối khi description chứa dấu phẩy không bọc nháy kép
    print("\n[TC-IMPORT-019] Từ chối khi description chứa dấu phẩy không bọc nháy kép")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported Comma No Quotes", "price": 100000, "description": "Mô tả, có dấu phẩy", "imageUrl": "imageUrl", "category_id": None}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Chấp nhận dữ liệu lệch cấu trúc cột/category_id rỗng)")

    # 14. TC-IMPORT-020: Từ chối import khi price để trống hoàn toàn
    print("\n[TC-IMPORT-020] Từ chối import khi price để trống hoàn toàn")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported Price Empty", "description": "Mô tả", "imageUrl": "", "category_id": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép import thiếu trường price)")

    # 15. TC-IMPORT-021: Từ chối import khi category_id không tồn tại trong hệ thống
    print("\n[TC-IMPORT-021] Từ chối import khi category_id không tồn tại trong hệ thống")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported Invalid Category", "price": 100000, "description": "Mô tả", "imageUrl": "", "category_id": 9999}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Chấp nhận category_id không tồn tại)")

    # 16. TC-IMPORT-022: Từ chối import khi category_id để trống hoàn toàn
    print("\n[TC-IMPORT-022] Từ chối import khi category_id để trống hoàn toàn")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported Category Empty", "price": 100000, "description": "Mô tả", "imageUrl": ""}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép category_id rỗng và tự động gán mặc định)")

    # 17. TC-IMPORT-023: Từ chối import khi tệp CSV hoàn toàn trống (0 bytes)
    print("\n[TC-IMPORT-023] Từ chối import khi tệp CSV hoàn toàn trống (0 bytes)")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": []
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Chấp nhận danh sách sản phẩm rỗng)")

    # 18. TC-IMPORT-024: Xử lý tệp CSV có chứa dòng trống ở giữa hoặc ở cuối tệp
    print("\n[TC-IMPORT-024] Xử lý tệp CSV có chứa dòng trống ở giữa hoặc ở cuối tệp")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported Dòng Trước Trống", "price": 100000, "description": "Dòng 1", "imageUrl": "", "category_id": 1},
            {},
            {"name": "Imported Dòng Sau Trống", "price": 150000, "description": "Dòng 3", "imageUrl": "", "category_id": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products WHERE name IS NULL OR name = '' OR name = '   '")
    blank_prods = cursor.fetchone()[0]
    conn.close()
    
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED (Từ chối và rollback)")
    elif status == 200 and final_count - initial_count == 2 and blank_prods == 0:
        print("  => KẾT QUẢ: PASSED (Bỏ qua dòng trống)")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Tạo ra dữ liệu rỗng hoặc sai số lượng)")

    # 19. TC-IMPORT-025: Rollback CSDL khi dòng thứ 3 bị price âm (Atomicity)
    print("\n[TC-IMPORT-025] Rollback CSDL khi dòng thứ 3 bị price âm (Atomicity)")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported SP Hợp Lệ 1", "price": 100000, "description": "Mô tả", "imageUrl": "", "category_id": 1},
            {"name": "Imported SP Hợp Lệ 2", "price": 200000, "description": "Mô tả", "imageUrl": "", "category_id": 1},
            {"name": "Imported SP Lỗi Âm", "price": -50000, "description": "Mô tả lỗi", "imageUrl": "", "category_id": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Không rollback toàn bộ giao dịch khi dòng 3 bị lỗi price âm)")

    # 20. TC-IMPORT-026: Import tệp CSV thành công hoàn toàn
    print("\n[TC-IMPORT-026] Import tệp CSV thành công hoàn toàn")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported SP Hợp Lệ 1", "price": 100000, "description": "Mô tả", "imageUrl": "", "category_id": 1},
            {"name": "Imported SP Hợp Lệ 2", "price": 200000, "description": "Mô tả", "imageUrl": "", "category_id": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    if status == 200 and final_count - initial_count == 2 and res.get("inserted") == 2 and len(res.get("errors", [])) == 0:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED")

    # 21. TC-IMPORT-027: Từ chối hoặc mã hóa an toàn khi description chứa mã độc XSS
    print("\n[TC-IMPORT-027] Từ chối hoặc mã hóa an toàn khi description chứa mã độc XSS")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported XSS Desc", "price": 100000, "description": "<script>alert('XSS_desc')</script>", "imageUrl": "", "category_id": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT description FROM products WHERE name = 'Imported XSS Desc'")
    row = cursor.fetchone()
    conn.close()
    
    db_desc = row[0] if row else None
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED (Từ chối)")
    elif db_desc and "<script>" in db_desc:
        print("  => KẾT QUẢ: FAILED (Bug: Lưu trữ mã độc XSS nguyên bản vào database trong trường description)")
    else:
        print("  => KẾT QUẢ: PASSED")

    # 22. TC-IMPORT-028: Từ chối khi description chứa lệnh SQL Injection
    print("\n[TC-IMPORT-028] Từ chối khi description chứa lệnh SQL Injection")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported SQLi Desc", "price": 100000, "description": "' OR 1=1 --", "imageUrl": "", "category_id": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép lưu trữ SQL Injection payload trong trường description)")

    # 23. TC-IMPORT-029: Từ chối hoặc mã hóa an toàn khi imageUrl chứa mã độc XSS
    print("\n[TC-IMPORT-029] Từ chối hoặc mã hóa an toàn khi imageUrl chứa mã độc XSS")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported XSS Image", "price": 100000, "description": "Mô tả", "imageUrl": "javascript:alert(1)", "category_id": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT imageUrl FROM products WHERE name = 'Imported XSS Image'")
    row = cursor.fetchone()
    conn.close()
    
    db_img = row[0] if row else None
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED (Từ chối)")
    elif db_img and "javascript:" in db_img:
        print("  => KẾT QUẢ: FAILED (Bug: Lưu trữ URI nguy hiểm javascript: trong trường imageUrl)")
    else:
        print("  => KẾT QUẢ: PASSED")

    # 24. TC-IMPORT-030: Từ chối khi imageUrl chứa lệnh SQL Injection
    print("\n[TC-IMPORT-030] Từ chối khi imageUrl chứa lệnh SQL Injection")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported SQLi Image", "price": 100000, "description": "Mô tả", "imageUrl": "' OR 1=1 --", "category_id": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép lưu trữ SQL Injection payload trong trường imageUrl)")

    # 25. TC-IMPORT-031: Từ chối khi price chứa mã độc XSS
    print("\n[TC-IMPORT-031] Từ chối khi price chứa mã độc XSS")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported XSS Price", "price": "<script>alert('XSS_price')</script>", "description": "Mô tả", "imageUrl": "", "category_id": 1}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT price FROM products WHERE name = 'Imported XSS Price'")
    row = cursor.fetchone()
    conn.close()
    
    db_price = row[0] if row else None
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED (Từ chối)")
    elif db_price and "<script>" in str(db_price):
        print("  => KẾT QUẢ: FAILED (Bug: Lưu trữ mã độc XSS nguyên bản vào database trong cột price)")
    else:
        print("  => KẾT QUẢ: PASSED")

    # 26. TC-IMPORT-032: Từ chối khi category_id chứa mã độc XSS
    print("\n[TC-IMPORT-032] Từ chối khi category_id chứa mã độc XSS")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported XSS Cat", "price": 100000, "description": "Mô tả", "imageUrl": "", "category_id": "<script>alert('XSS_cat')</script>"}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT category_id FROM products WHERE name = 'Imported XSS Cat'")
    row = cursor.fetchone()
    conn.close()
    
    db_cat = row[0] if row else None
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED (Từ chối)")
    elif db_cat and "<script>" in str(db_cat):
        print("  => KẾT QUẢ: FAILED (Bug: Lưu trữ mã độc XSS nguyên bản vào database trong cột category_id)")
    else:
        print("  => KẾT QUẢ: PASSED")

    # 27. TC-IMPORT-033: Từ chối khi category_id chứa lệnh SQL Injection
    print("\n[TC-IMPORT-033] Từ chối khi category_id chứa lệnh SQL Injection")
    initial_count = get_product_count()
    status, res = make_request("/api/admin/import-products", data={
        "products": [
            {"name": "Imported SQLi Cat", "price": 100000, "description": "Mô tả", "imageUrl": "", "category_id": "' OR 1=1 --"}
        ]
    }, token=token)
    final_count = get_product_count()
    print(f"  - Response: HTTP {status} | {res}")
    print(f"  - Số sản phẩm trước/sau: {initial_count} / {final_count}")
    if status == 400 and final_count == initial_count:
        print("  => KẾT QUẢ: PASSED")
    else:
        print("  => KẾT QUẢ: FAILED (Bug: Cho phép lưu trữ SQL Injection payload trong cột category_id)")

    # Dọn dẹp sau khi kiểm thử
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE name LIKE 'Imported %'")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    run_tests()
