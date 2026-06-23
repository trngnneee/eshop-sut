import os
import json
import argparse
import sys
import codecs

# Set console output encoding to UTF-8 to handle Vietnamese characters properly
if sys.stdout.encoding != 'utf-8':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

def generate_cases(feature_name, module_name, inputs):
    """
    Generates test case templates based on input definitions.
    """
    test_cases = []
    
    for inp in inputs:
        name = inp.get("name")
        inp_type = inp.get("type")
        required = inp.get("required", False)
        
        # 1. Equivalence Partitioning - Required check
        if required:
            test_cases.append({
                "title": f"Kiểm thử {name} để trống",
                "technique": "Equivalence Partitioning",
                "preconditions": [f"Người dùng đang ở form của {feature_name}"],
                "data": {name: "[Để trống]"},
                "steps": [
                    f"Mở form {feature_name}.",
                    f"Nhập các trường khác hợp lệ ngoại trừ {name} để trống.",
                    "Bấm nút Submit."
                ],
                "expected": [f"Hệ thống từ chối submit và hiển thị thông báo lỗi bắt buộc nhập cho trường {name}."]
            })
            
        # 2. Boundary Value Analysis - String Length / Numeric values
        if inp_type == "string":
            min_len = inp.get("min_length")
            max_len = inp.get("max_length")
            
            if min_len is not None:
                # Boundary value check for min length
                test_cases.append({
                    "title": f"Kiểm thử {name} với độ dài dưới tối thiểu ({min_len - 1} ký tự)",
                    "technique": "Boundary Value Analysis",
                    "preconditions": [f"Người dùng đang ở form của {feature_name}"],
                    "data": {name: "a" * (min_len - 1) if min_len > 1 else "[Để trống]"},
                    "steps": [
                        f"Mở form {feature_name}.",
                        f"Nhập {name} có độ dài {min_len - 1} ký tự.",
                        "Bấm nút Submit."
                    ],
                    "expected": [f"Hệ thống báo lỗi độ dài {name} tối thiểu là {min_len} ký tự."]
                })
                test_cases.append({
                    "title": f"Kiểm thử {name} với độ dài biên tối thiểu ({min_len} ký tự)",
                    "technique": "Boundary Value Analysis",
                    "preconditions": [f"Người dùng đang ở form của {feature_name}"],
                    "data": {name: "a" * min_len},
                    "steps": [
                        f"Mở form {feature_name}.",
                        f"Nhập {name} có độ dài đúng {min_len} ký tự.",
                        "Bấm nút Submit."
                    ],
                    "expected": [f"Hệ thống chấp nhận giá trị và không báo lỗi độ dài ở trường {name}."]
                })
                
            if max_len is not None:
                # Boundary value check for max length
                test_cases.append({
                    "title": f"Kiểm thử {name} với độ dài biên tối đa ({max_len} ký tự)",
                    "technique": "Boundary Value Analysis",
                    "preconditions": [f"Người dùng đang ở form của {feature_name}"],
                    "data": {name: "a" * max_len},
                    "steps": [
                        f"Mở form {feature_name}.",
                        f"Nhập {name} có độ dài đúng {max_len} ký tự.",
                        "Bấm nút Submit."
                    ],
                    "expected": [f"Hệ thống chấp nhận giá trị và không báo lỗi độ dài ở trường {name}."]
                })
                test_cases.append({
                    "title": f"Kiểm thử {name} với độ dài vượt quá tối đa ({max_len + 1} ký tự)",
                    "technique": "Boundary Value Analysis",
                    "preconditions": [f"Người dùng đang ở form của {feature_name}"],
                    "data": {name: "a" * (max_len + 1)},
                    "steps": [
                        f"Mở form {feature_name}.",
                        f"Nhập {name} có độ dài {max_len + 1} ký tự.",
                        "Bấm nút Submit."
                    ],
                    "expected": [f"Hệ thống báo lỗi độ dài {name} vượt quá giới hạn tối đa {max_len} ký tự."]
                })

        elif inp_type == "numeric":
            min_val = inp.get("min_value")
            max_val = inp.get("max_value")
            
            if min_val is not None:
                # Min - 1
                test_cases.append({
                    "title": f"Kiểm thử {name} nhỏ hơn giá trị tối thiểu ({min_val - 1})",
                    "technique": "Boundary Value Analysis",
                    "preconditions": [f"Người dùng đang ở form của {feature_name}"],
                    "data": {name: str(min_val - 1)},
                    "steps": [
                        f"Mở form {feature_name}.",
                        f"Nhập {name} có giá trị {min_val - 1}.",
                        "Bấm nút Submit."
                    ],
                    "expected": [f"Hệ thống báo lỗi giá trị {name} phải lớn hơn hoặc bằng {min_val}."]
                })
                # Min
                test_cases.append({
                    "title": f"Kiểm thử {name} đúng giá trị tối thiểu ({min_val})",
                    "technique": "Boundary Value Analysis",
                    "preconditions": [f"Người dùng đang ở form của {feature_name}"],
                    "data": {name: str(min_val)},
                    "steps": [
                        f"Mở form {feature_name}.",
                        f"Nhập {name} có giá trị đúng bằng {min_val}.",
                        "Bấm nút Submit."
                    ],
                    "expected": [f"Hệ thống chấp nhận giá trị {min_val} ở trường {name}."]
                })
                
            if max_val is not None:
                # Max
                test_cases.append({
                    "title": f"Kiểm thử {name} đúng giá trị tối đa ({max_val})",
                    "technique": "Boundary Value Analysis",
                    "preconditions": [f"Người dùng đang ở form của {feature_name}"],
                    "data": {name: str(max_val)},
                    "steps": [
                        f"Mở form {feature_name}.",
                        f"Nhập {name} có giá trị đúng bằng {max_val}.",
                        "Bấm nút Submit."
                    ],
                    "expected": [f"Hệ thống chấp nhận giá trị {max_val} ở trường {name}."]
                })
                # Max + 1
                test_cases.append({
                    "title": f"Kiểm thử {name} lớn hơn giá trị tối đa ({max_val + 1})",
                    "technique": "Boundary Value Analysis",
                    "preconditions": [f"Người dùng đang ở form của {feature_name}"],
                    "data": {name: str(max_val + 1)},
                    "steps": [
                        f"Mở form {feature_name}.",
                        f"Nhập {name} có giá trị {max_val + 1}.",
                        "Bấm nút Submit."
                    ],
                    "expected": [f"Hệ thống báo lỗi giá trị {name} phải nhỏ hơn hoặc bằng {max_val}."]
                })

    # Write files
    output_dir = f"tests/test-cases/{module_name}"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Bắt đầu tạo {len(test_cases)} test cases vào thư mục: {output_dir}")
    
    for i, tc in enumerate(test_cases, 1):
        tc_id = f"TC-{module_name.upper()}-{i:03d}"
        filename = f"{output_dir}/{tc_id}.md"
        
        data_table = "\n".join([f"| {k} | {v} |" for k, v in tc["data"].items()])
        steps_list = "\n".join([f"{idx}. {step}" for idx, step in enumerate(tc["steps"], 1)])
        expected_list = "\n".join([f"- {exp}" for exp in tc["expected"]])
        preconditions_list = "\n".join([f"- {pre}" for pre in tc["preconditions"]])
        
        content = f"""# {tc_id}: {tc["title"]}

## Requirement ID
{feature_name}

## Module / Test type / Technique
{module_name.capitalize()} / Functional / {tc["technique"]}

## Preconditions
{preconditions_list}

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
{data_table}

## Test steps
{steps_list}

## Expected result
{expected_list}

## Status / Related bugs
Not Run / None
"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"-> Đã tạo: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tự động sinh test case templates.")
    parser.add_argument("--config", required=True, help="Đường dẫn file JSON cấu hình.")
    args = parser.parse_args()
    
    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)
        
    generate_cases(
        feature_name=config["feature_name"],
        module_name=config["module_name"],
        inputs=config["inputs"]
    )
