# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import json
import codecs
import sys

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

BASE_URL = "http://localhost:3000"

def make_request(path, data, token=None):
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req_data = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")
    
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

def run_selected_tests():
    print("=" * 80)
    print("CHẠY CÁC API REQUESTS KIỂM THỬ FR-16 (SELECTED TEST CASES)")
    print("=" * 80)
    
    # 0. Login Admin
    status, res = make_request("/api/login", {
        "email": "admin@eshop.com",
        "password": "Admin123!"
    })
    token = res.get("token")
    if not token:
        print("LỖI: Đăng nhập admin thất bại!")
        return
    
    # Selected test cases definitions
    cases = [
        {
            "id": "TC-IMPORT-003",
            "desc": "Tệp CSV thiếu dòng header đầu tiên (Frontend gửi nulls/undefineds)",
            "payload": {
                "products": [
                    {
                        "name": None,
                        "price": None,
                        "description": None,
                        "imageUrl": None,
                        "category_id": None
                    }
                ]
            },
            "bug": "BUG-IMPORT-003 (Thiếu validate header ở Frontend) & BUG-IMPORT-004 (Backend trả về HTTP 200 OK thay vì 400 Bad Request khi có lỗi validation)"
        },
        {
            "id": "TC-IMPORT-004",
            "desc": "Tệp CSV có header sai tên cột bắt buộc (Frontend gửi sai tên cột)",
            "payload": {
                "products": [
                    {
                        "ten_sp": "Imported SP Wrong Header",
                        "gia": 100000,
                        "mo_ta": "Mô tả"
                    }
                ]
            },
            "bug": "BUG-IMPORT-003 (Thiếu validate header ở Frontend) & BUG-IMPORT-004 (Backend trả về HTTP 200 OK thay vì 400 Bad Request)"
        },
        {
            "id": "TC-IMPORT-005",
            "desc": "Dòng sản phẩm có name rỗng (\"\")",
            "payload": {
                "products": [
                    {
                        "name": "",
                        "price": 150000,
                        "description": "Mô tả A",
                        "imageUrl": "",
                        "category_id": 1
                    }
                ]
            },
            "bug": "BUG-IMPORT-004 (Backend trả về HTTP 200 OK thay vì 400 Bad Request)"
        },
        {
            "id": "TC-IMPORT-013",
            "desc": "Dòng sản phẩm có name chỉ chứa khoảng trắng (\"   \")",
            "payload": {
                "products": [
                    {
                        "name": "   ",
                        "price": 100000,
                        "description": "Mô tả",
                        "imageUrl": "",
                        "category_id": 1
                    }
                ]
            },
            "bug": "BUG-IMPORT-007 (Backend trả về HTTP 200 OK và lưu tên trống \"   \" vào CSDL)"
        },
        {
            "id": "TC-IMPORT-018",
            "desc": "Tệp CSV có header viết hoa (NAME, PRICE...)",
            "payload": {
                "products": [
                    {
                        "NAME": "Imported Caps Header",
                        "PRICE": 120000,
                        "DESCRIPTION": "Mô tả",
                        "IMAGEURL": "",
                        "CATEGORY_ID": 1
                    }
                ]
            },
            "bug": "BUG-IMPORT-011 (Backend trả về HTTP 200 OK nhưng chèn dữ liệu trống do không chuẩn hóa trường viết hoa)"
        },
        {
            "id": "TC-IMPORT-022",
            "desc": "Cột category_id để trống hoàn toàn (thiếu trường)",
            "payload": {
                "products": [
                    {
                        "name": "Imported Category Empty",
                        "price": 100000,
                        "description": "Mô tả",
                        "imageUrl": ""
                    }
                ]
            },
            "bug": "BUG-IMPORT-015 (Backend trả về HTTP 200 OK và tự động gán category_id = 1 thay vì báo lỗi thiếu trường)"
        }
    ]

    for case in cases:
        print(f"\n[Chạy {case['id']}] - {case['desc']}")
        print(f"  - Payload gửi lên: {json.dumps(case['payload'])}")
        
        status, response = make_request("/api/admin/import-products", case['payload'], token)
        
        print(f"  - Kết quả API trả về: HTTP {status} | {response}")
        print(f"  - BUG LIÊN QUAN: {case['bug']}")
        
        # Check if test passed or failed (all these should return HTTP 400 if correctly implemented, but currently return HTTP 200)
        if status == 200:
            print("  => ĐÁNH GIÁ THỰC TẾ: FAILED (Hệ thống chấp nhận dữ liệu lỗi - Lỗi bảo mật/nghiệp vụ)")
        elif status == 400:
            print("  => ĐÁNH GIÁ THỰC TẾ: PASSED (Hệ thống từ chối dữ liệu lỗi chính xác)")
        else:
            print(f"  => ĐÁNH GIÁ THỰC TẾ: UNEXPECTED RESPONSE (HTTP {status})")
        print("-" * 80)

if __name__ == "__main__":
    run_selected_tests()
