---
name: hw6-agent-skill-design
description: >
  Hỗ trợ thiết kế AI-driven API Test Generator cho HW6 (Bloom-AI G9.5 – Create).
  AI tạo pseudocode, chuẩn bị khung tài liệu thiết kế, và hướng dẫn implementation.
  Sơ đồ kiến trúc phải do sinh viên tự vẽ.
---

# Skill: hw6-agent-skill-design

## Mục tiêu

Hỗ trợ sinh viên thiết kế và triển khai **AI-driven API Test Generator** cho EShop SUT (Bloom-AI G9.5 – Create):
1. Mô tả kiến trúc hệ thống test generator
2. Tạo pseudocode chi tiết cho từng module
3. Chuẩn bị khung tài liệu `agent_skill.md`
4. Triển khai prototype Python nếu được yêu cầu

> ⚠️ **Sơ đồ kiến trúc** (diagram) PHẢI do sinh viên tự vẽ – không AI generate.
> AI chỉ mô tả bằng text/pseudocode và tạo Mermaid placeholder để sinh viên thay bằng ảnh tự vẽ.

---

## Thông tin đầu vào

| Mục | Giá trị |
|:----|:--------|
| `AGENT_SKILL_FILE` | `submissions/agent_skill.md` |
| `REPORT_FILE`      | `submissions/MainReport.md` |
| `IMPLEMENT`        | `true` nếu muốn tạo prototype Python script |

---

## Kiến trúc tổng quan của AI Test Generator

Hệ thống gồm 5 module chính:

```
API Spec (Markdown)
    ↓
[1] SpecParser
    ↓
[2] TestStrategyEngine (AI-powered)
    ├── DomainPartitionModule
    ├── StateTransitionModule
    ├── SecurityModule
    └── SchemaValidationModule
    ↓
[3] TestCaseBuilder
    ↓
[4] DeduplicatorFilter
    ↓
[5] PostmanExporter
    ↓
Postman Collection JSON
```

---

## Các bước thực hiện

### Bước 1 — Thiết kế và viết Pseudocode

AI tạo pseudocode chi tiết cho từng module:

**Module 1: SpecParser**
```pseudocode
FUNCTION parse_api_spec(spec_file_path):
    content = read_file(spec_file_path)
    endpoints = []
    
    FOR each section IN content:
        endpoint = {
            method: extract_method(section),
            path: extract_path(section),
            params: extract_parameters(section),
            body_schema: extract_body_schema(section),
            response_schema: extract_response_schema(section),
            auth_required: check_auth_requirement(section),
            feature_tag: extract_feature_tag(section)  # FR-01, FR-10, etc.
        }
        endpoints.append(endpoint)
    
    RETURN endpoints
```

**Module 2: TestStrategyEngine**
```pseudocode
FUNCTION generate_tests_for_endpoint(endpoint, ai_client):
    test_cases = []
    
    # Domain Partition
    dp_prompt = build_domain_partition_prompt(endpoint)
    dp_tests = ai_client.generate(dp_prompt)
    test_cases.extend(parse_tc_table(dp_tests, type="DP"))
    
    # State Transition (chỉ nếu có state machine)
    IF endpoint.feature_tag IN ["FR-10", "FR-08"]:
        st_prompt = build_state_transition_prompt(endpoint)
        st_tests = ai_client.generate(st_prompt)
        test_cases.extend(parse_tc_table(st_tests, type="ST"))
    
    # Security
    sec_prompt = build_security_prompt(endpoint)
    sec_tests = ai_client.generate(sec_prompt)
    test_cases.extend(parse_tc_table(sec_tests, type="SEC"))
    
    # Schema Validation
    sv_prompt = build_schema_validation_prompt(endpoint)
    sv_tests = ai_client.generate(sv_prompt)
    test_cases.extend(parse_tc_table(sv_tests, type="SV"))
    
    RETURN test_cases
```

**Module 3: TestCaseBuilder**
```pseudocode
FUNCTION build_tc(raw_tc, endpoint, pool_prefix):
    tc_id = generate_tc_id(pool_prefix, raw_tc.type, auto_increment())
    RETURN {
        id: tc_id,
        description: raw_tc.description,
        method: endpoint.method,
        url: endpoint.path,
        headers: build_headers(endpoint.auth_required),
        body: raw_tc.input,
        expected_status: raw_tc.expected_status,
        expected_body: raw_tc.expected_body,
        type: raw_tc.type,
        audit: "PENDING"  # sẽ do người review
    }
```

**Module 4: DeduplicatorFilter**
```pseudocode
FUNCTION deduplicate(test_cases):
    seen = set()
    unique_tcs = []
    
    FOR tc IN test_cases:
        key = hash(tc.method + tc.url + str(tc.body))
        IF key NOT IN seen:
            seen.add(key)
            unique_tcs.append(tc)
    
    RETURN unique_tcs
```

**Module 5: PostmanExporter**
```pseudocode
FUNCTION export_to_postman(test_cases, collection_name, student_id):
    collection = {
        "info": { "name": collection_name, "schema": POSTMAN_SCHEMA_URL },
        "variable": [
            { "key": "baseUrl", "value": "http://localhost:3000" },
            { "key": "studentId", "value": student_id }
        ],
        "item": []
    }
    
    FOR tc IN test_cases:
        item = build_postman_item(tc)
        collection["item"].append(item)
    
    write_json(collection, f"postman/{collection_name}.json")
    RETURN collection
```

### Bước 2 — Prototype Python (nếu IMPLEMENT = true)

Tạo file `mini-lab/test_generator/generate_tests.py`:

```python
"""
HW06 – AI-driven API Test Generator
Sinh viên: [Họ tên] – [MSSV]
"""
import json
import re
import sys
from pathlib import Path

# Cấu hình
SPEC_FILE = "api_specification.md"
POOL = sys.argv[1] if len(sys.argv) > 1 else "A"
ENDPOINT_KEYWORD = sys.argv[2] if len(sys.argv) > 2 else "login"

def parse_spec(spec_path: str) -> list[dict]:
    """Đọc và phân tích API specification."""
    content = Path(spec_path).read_text(encoding="utf-8")
    # TODO: sinh viên implement parser theo cấu trúc spec thực tế
    # Trả về list các endpoint dict
    endpoints = []
    return endpoints

def build_domain_prompt(endpoint: dict) -> str:
    return f"""
Áp dụng Domain Partition Testing cho endpoint sau:
Method: {endpoint.get('method')}
Path: {endpoint.get('path')}
Parameters: {json.dumps(endpoint.get('params', {}), ensure_ascii=False)}

Hãy sinh test cases theo bảng:
| TC ID | Mô tả | Input | Expected | Phân vùng |
"""

def build_security_prompt(endpoint: dict) -> str:
    return f"""
Sinh Security test cases cho endpoint {endpoint.get('method')} {endpoint.get('path')}
Bao gồm: SQL Injection, IDOR, Role Escalation, Missing Auth, Expired Token.
Bảng: | TC ID | Loại tấn công | Input | Expected |
"""

def call_ai(prompt: str) -> str:
    """Gọi AI API – sinh viên implement theo tool đang dùng."""
    # Ví dụ: openai, anthropic, google generativeai, v.v.
    # return ai_client.complete(prompt)
    print(f"[AI PROMPT]\n{prompt}\n")
    return "# AI response placeholder – sinh viên implement"

def parse_markdown_table(markdown_text: str) -> list[dict]:
    """Parse markdown table thành list of dicts."""
    # TODO: implement parser
    return []

def export_postman(test_cases: list, output_path: str, student_id: str):
    """Xuất Postman Collection JSON."""
    collection = {
        "info": {
            "name": f"HW06 Auto-Generated – {student_id}",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "variable": [
            {"key": "baseUrl", "value": "http://localhost:3000"},
            {"key": "studentId", "value": student_id}
        ],
        "item": []
    }
    for tc in test_cases:
        item = {
            "name": tc.get("id", "TC"),
            "request": {
                "method": tc.get("method", "GET"),
                "header": [
                    {"key": "X-Student-Id", "value": "{{studentId}}"},
                    {"key": "Content-Type", "value": "application/json"}
                ],
                "url": {"raw": "{{baseUrl}}" + tc.get("url", "/")}
            }
        }
        collection["item"].append(item)
    
    Path(output_path).write_text(json.dumps(collection, indent=2, ensure_ascii=False))
    print(f"[EXPORT] Collection saved to {output_path}")

def main():
    print(f"=== HW06 AI Test Generator ===")
    print(f"Pool: {POOL} | Keyword: {ENDPOINT_KEYWORD}")
    
    # 1. Parse spec
    endpoints = parse_spec(SPEC_FILE)
    target = next((e for e in endpoints if ENDPOINT_KEYWORD in e.get("path", "")), None)
    
    if not target:
        print(f"[WARN] Không tìm thấy endpoint với keyword '{ENDPOINT_KEYWORD}'")
        print("[INFO] Đang dùng placeholder endpoint...")
        target = {"method": "POST", "path": f"/api/{ENDPOINT_KEYWORD}", "params": {}}
    
    # 2. Generate
    test_cases = []
    
    dp_prompt = build_domain_prompt(target)
    dp_output = call_ai(dp_prompt)
    test_cases.extend(parse_markdown_table(dp_output))
    
    sec_prompt = build_security_prompt(target)
    sec_output = call_ai(sec_prompt)
    test_cases.extend(parse_markdown_table(sec_output))
    
    # 3. Export
    output_path = f"postman/hw06_generated_pool{POOL}.json"
    export_postman(test_cases, output_path, student_id="23127486")
    
    print(f"[DONE] Generated {len(test_cases)} test cases")

if __name__ == "__main__":
    main()
```

### Bước 3 — Cập nhật tài liệu

**Cập nhật `agent_skill.md`:**

Agent điền vào các section:
- **Mục 1 – Mô tả**: Giải thích kiến trúc 5 module
- **Mục 2 – Sơ đồ**: Chèn Mermaid flowchart (placeholder, sinh viên thay bằng ảnh tự vẽ)
- **Mục 3 – Pseudocode**: Copy pseudocode từ bước 1
- **Mục 4 – Implementation**: Điền bảng công nghệ
- **Mục 5 – Demo**: Để trống placeholder cho sinh viên điền YouTube link
- **Mục 6 – Nhận xét**: Mô tả điểm mạnh/yếu

**Cập nhật `MainReport.md`:**

Trong section **7. Agent Skill**:
```markdown
## 7. Agent Skill – AI-driven Test Generator

**Bloom-AI Level:** G9.5 (Create)

- **Kiến trúc:** 5 modules (SpecParser → TestStrategyEngine → TestCaseBuilder → Deduplicator → PostmanExporter)
- **Ngôn ngữ:** Python
- **AI Engine:** [tên AI tool]
- **Output:** Postman Collection JSON

> Chi tiết thiết kế: `submissions/agent_skill.md`
> Demo video: *(sinh viên điền YouTube link)*
```

---

## Cập nhật tài liệu (BẮT BUỘC)

Agent phải cập nhật:

1. **`submissions/agent_skill.md`**: Điền đầy đủ pseudocode, bảng implementation, mục nhận xét
2. **`submissions/MainReport.md`**: Cập nhật section 7 với tóm tắt kiến trúc
3. **(Tùy chọn)** `mini-lab/test_generator/generate_tests.py`: Tạo prototype script

---

## Ràng buộc

- Sơ đồ kiến trúc PHẢI do sinh viên tự vẽ (PNG từ draw.io, Excalidraw, v.v.)
- Mermaid trong `agent_skill.md` chỉ là placeholder tham khảo – phải thay bằng ảnh tự vẽ
- Demo video phải quay thực tế agent chạy sinh test cho 1 API
- Python script là skeleton – sinh viên implement logic thực

---

## Checklist hoàn thành

- [ ] `submissions/agent_skill.md` có đầy đủ 5 sections
- [ ] Pseudocode 5 modules đã được viết chi tiết
- [ ] Bảng implementation đã điền công nghệ cụ thể
- [ ] `submissions/MainReport.md` section 7 đã cập nhật
- [ ] Placeholder diagram rõ ràng nhắc sinh viên thay bằng ảnh tự vẽ
- [ ] (Tùy chọn) `mini-lab/test_generator/generate_tests.py` đã tạo
