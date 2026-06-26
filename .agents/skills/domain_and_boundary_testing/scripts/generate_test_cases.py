import argparse
import codecs
import json
import os
import sys
import unicodedata
from pathlib import Path

# Set console output encoding to UTF-8 to handle Vietnamese characters properly.
if sys.stdout.encoding != "utf-8":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

PROJECT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_OUTPUT_ROOT = "tests/test-cases"
DEFAULT_TEST_RUN_OUTPUT_ROOT = "tests/test-runs"


def format_value(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    return str(value)


def normalize_feature_code(feature_name):
    return str(feature_name).replace("-", "").replace(" ", "").upper()


def field_code_from_name(name, fallback="X"):
    text = str(name).replace("Đ", "D").replace("đ", "d")
    text = unicodedata.normalize("NFKD", text)
    ascii_chars = [ch for ch in text if ch.isascii() and ch.isalnum()]
    return (ascii_chars[0].upper() if ascii_chars else fallback)


def module_display_name(module_name):
    return str(module_name).replace("_", " ").title()


def resolve_output_root(output_root):
    root = Path(output_root or DEFAULT_OUTPUT_ROOT)
    if root.is_absolute():
        return root
    return PROJECT_ROOT / root


def resolve_test_run_output_root(output_root):
    root = Path(output_root or DEFAULT_TEST_RUN_OUTPUT_ROOT)
    if root.is_absolute():
        return root
    return PROJECT_ROOT / root


def slugify(value):
    text = str(value).replace("Đ", "D").replace("đ", "d").replace("_", "-")
    text = unicodedata.normalize("NFKD", text)
    chars = []
    previous_dash = False

    for ch in text:
        if ch.isascii() and ch.isalnum():
            chars.append(ch.lower())
            previous_dash = False
        elif not previous_dash:
            chars.append("-")
            previous_dash = True

    return "".join(chars).strip("-") or "test-run"


def default_test_run_filename(config):
    feature_code = config.get("feature_code") or normalize_feature_code(
        config["feature_name"]
    )
    return f"{slugify(feature_code)}-{slugify(config['module_name'])}-test-run.md"


def test_run_config(config):
    raw = config.get("test_run", {})
    if raw is False:
        return {"enabled": False}
    if raw is True or raw is None:
        return {"enabled": True}
    if not isinstance(raw, dict):
        raise ValueError("test_run must be a boolean or an object")
    return raw


def test_run_setting(config, key, default=None):
    run_config = test_run_config(config)
    if key in run_config:
        return run_config[key]
    legacy_key = f"test_run_{key}"
    return config.get(legacy_key, default)


def relative_markdown_path(from_dir, to_file):
    return os.path.relpath(to_file, start=from_dir).replace(os.sep, "/")


def is_bva_case(test_case):
    return (
        "Boundary Value Analysis" in test_case.get("technique", "")
        or "-BVA-" in test_case["id"]
    )


def field_code_from_tc_id(tc_id):
    parts = str(tc_id).split("-")
    if len(parts) >= 2 and parts[1]:
        return parts[1]
    return "X"


def group_names_from_config(config):
    names = {}

    for inp in config.get("inputs", []):
        field_code = inp.get("field_code") or field_code_from_name(inp.get("name"))
        names[field_code] = inp.get("group_name") or inp.get("name") or field_code

    if config.get("test_model") == "state_transition":
        default_field_code = config.get("field_code", "S")
        names.setdefault(
            default_field_code,
            config.get("field_name") or config.get("group_name") or "Status transition",
        )

    for boundary_case in config.get("boundary_cases", []):
        field_code = boundary_case.get("field_code", "O")
        if boundary_case.get("group_name") or boundary_case.get("field_name"):
            names[field_code] = boundary_case.get("group_name") or boundary_case.get(
                "field_name"
            )
        elif "Order ID" in boundary_case.get("data", {}):
            names.setdefault(field_code, "Order ID")
        else:
            names.setdefault(field_code, field_code)

    names.update(config.get("field_labels", {}))
    return names


def case_group_key(test_case, group_names):
    field_code = test_case.get("field_code") or field_code_from_tc_id(test_case["id"])
    return (
        field_code,
        test_case.get("group_name")
        or group_names.get(field_code)
        or test_case.get("module_name")
        or "General",
    )


def case_run_module(test_case, group_names):
    run_module = test_case.get("run_module")
    if run_module:
        return run_module

    module_name = test_case.get("module_name", "")
    field_code = test_case.get("field_code") or field_code_from_tc_id(test_case["id"])
    group_name = test_case.get("group_name") or group_names.get(field_code)
    if group_name and group_name not in module_name:
        return f"{module_name} - {group_name}"
    return module_name


def next_tc_id(counters, feature_code, field_code, is_bva=False):
    key = (field_code, is_bva)
    counters[key] = counters.get(key, 0) + 1
    if is_bva:
        return f"{feature_code}-{field_code}-BVA-TC{counters[key]:02d}"
    return f"{feature_code}-{field_code}-TC{counters[key]:02d}"


def write_cases(test_cases, module_name, output_root):
    output_dir = resolve_output_root(output_root) / module_name
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Bắt đầu tạo {len(test_cases)} test cases vào thư mục: {output_dir}")

    for tc in test_cases:
        filename = output_dir / f"{tc['id']}.md"

        data_table = "\n".join(
            f"| {key} | {format_value(value)} |" for key, value in tc["data"].items()
        )
        steps_list = "\n".join(
            f"{idx}. {step}" for idx, step in enumerate(tc["steps"], 1)
        )
        expected_list = "\n".join(f"- {exp}" for exp in tc["expected"])
        preconditions_list = "\n".join(f"- {pre}" for pre in tc["preconditions"])

        content = f"""# {tc["id"]}: {tc["title"]}

## Requirement ID
{tc["feature_name"]}

## Module / Test type / Technique
{tc["module_name"]} / Functional / {tc["technique"]}

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
        with filename.open("w", encoding="utf-8") as f:
            f.write(content)
        print(f"-> Đã tạo: {filename}")


def write_test_run_template(test_cases, config, output_root):
    run_config = test_run_config(config)
    if run_config.get("enabled", True) is False:
        return

    output_dir = resolve_test_run_output_root(
        test_run_setting(config, "output_root", DEFAULT_TEST_RUN_OUTPUT_ROOT)
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = output_dir / test_run_setting(
        config, "file_name", default_test_run_filename(config)
    )
    overwrite = bool(test_run_setting(config, "overwrite", False))

    if filename.exists() and not overwrite:
        print(f"-> Bỏ qua test run template vì file đã tồn tại: {filename}")
        return

    module_name = config.get("module_display_name") or module_display_name(
        config["module_name"]
    )
    title = test_run_setting(
        config,
        "title",
        f"Test Run - {config['feature_name']} {module_name}",
    )
    tester = test_run_setting(config, "tester", "[Tên người test]")
    environment = test_run_setting(
        config,
        "environment",
        "[Môi trường thử nghiệm, ví dụ: Local Web/API, database seed, browser]",
    )

    group_names = group_names_from_config(config)
    groups = {}
    for test_case in test_cases:
        key = case_group_key(test_case, group_names)
        if key not in groups:
            groups[key] = {"domain": 0, "bva": 0, "total": 0}
        if is_bva_case(test_case):
            groups[key]["bva"] += 1
        else:
            groups[key]["domain"] += 1
        groups[key]["total"] += 1

    total_domain = sum(item["domain"] for item in groups.values())
    total_bva = sum(item["bva"] for item in groups.values())
    total_cases = len(test_cases)

    summary_rows = []
    for (_, group_name), counts in groups.items():
        summary_rows.append(
            f"| {group_name} | {counts['domain']} | {counts['bva']} | {counts['total']} | 0 | 0 |"
        )
    summary_rows.append(
        f"| **Tổng** | **{total_domain}** | **{total_bva}** | **{total_cases}** | **0** | **0** |"
    )

    test_case_root = resolve_output_root(output_root) / config["module_name"]
    execution_rows = []
    for test_case in test_cases:
        test_case_file = test_case_root / f"{test_case['id']}.md"
        link_path = relative_markdown_path(filename.parent, test_case_file)
        execution_rows.append(
            f"| [{test_case['id']}]({link_path}) | {case_run_module(test_case, group_names)} | {tester} | Not Run | None | [Điền actual result / ghi chú sau khi chạy] |"
        )

    content = f"""# {title}

__Ngày thực hiện__: [dd/mm/yyyy]  
__Người thực hiện__: {tester}  
__Môi trường thử nghiệm__: {environment}  

## Tổng quan kết quả

| Nhóm kiểm thử | Domain TC | BVA TC | Tổng TC | Pass | Fail |
| :--- | ---: | ---: | ---: | ---: | ---: |
{chr(10).join(summary_rows)}

## Test Case Execution Report

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
{chr(10).join(execution_rows)}

## Defect Log

Sau khi chạy test, cập nhật các test case `Fail` vào bảng dưới đây hoặc map sang bug report riêng.

| Bug ID | Related TC ID | Tóm tắt | Severity | Status | Evidence / Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [BUG-ID] | [TC ID] | [Tóm tắt lỗi] | [High/Medium/Low] | Open | [Actual result / evidence] |
"""
    with filename.open("w", encoding="utf-8") as f:
        f.write(content)
    print(f"-> Đã tạo test run template: {filename}")


def generate_input_cases(config):
    feature_name = config["feature_name"]
    module_name = config["module_name"]
    feature_code = config.get("feature_code") or normalize_feature_code(feature_name)
    module_name_display = config.get("module_display_name") or module_display_name(
        module_name
    )
    test_cases = []
    counters = {}

    for inp in config["inputs"]:
        name = inp.get("name")
        inp_type = inp.get("type")
        required = inp.get("required", False)
        field_code = inp.get("field_code") or field_code_from_name(name)

        if required:
            tc_id = next_tc_id(counters, feature_code, field_code)
            test_cases.append(
                {
                    "id": tc_id,
                    "title": f"Kiểm thử {name} để trống",
                    "feature_name": feature_name,
                    "module_name": module_name_display,
                    "technique": "Equivalence Partitioning",
                    "preconditions": [f"Người dùng đang ở form của {feature_name}"],
                    "data": {name: "[Để trống]"},
                    "steps": [
                        f"Mở form {feature_name}.",
                        f"Nhập các trường khác hợp lệ ngoại trừ {name} để trống.",
                        "Bấm nút Submit.",
                    ],
                    "expected": [
                        f"Hệ thống từ chối submit và hiển thị thông báo lỗi bắt buộc nhập cho trường {name}."
                    ],
                }
            )

        if inp_type == "string":
            min_len = inp.get("min_length")
            max_len = inp.get("max_length")

            if min_len is not None:
                tc_id = next_tc_id(counters, feature_code, field_code, is_bva=True)
                test_cases.append(
                    {
                        "id": tc_id,
                        "title": f"Kiểm thử {name} với độ dài dưới tối thiểu ({min_len - 1} ký tự)",
                        "feature_name": feature_name,
                        "module_name": module_name_display,
                        "technique": "Boundary Value Analysis",
                        "preconditions": [f"Người dùng đang ở form của {feature_name}"],
                        "data": {
                            name: "a" * (min_len - 1) if min_len > 1 else "[Để trống]"
                        },
                        "steps": [
                            f"Mở form {feature_name}.",
                            f"Nhập {name} có độ dài {min_len - 1} ký tự.",
                            "Bấm nút Submit.",
                        ],
                        "expected": [
                            f"Hệ thống báo lỗi độ dài {name} tối thiểu là {min_len} ký tự."
                        ],
                    }
                )
                tc_id = next_tc_id(counters, feature_code, field_code, is_bva=True)
                test_cases.append(
                    {
                        "id": tc_id,
                        "title": f"Kiểm thử {name} với độ dài biên tối thiểu ({min_len} ký tự)",
                        "feature_name": feature_name,
                        "module_name": module_name_display,
                        "technique": "Boundary Value Analysis",
                        "preconditions": [f"Người dùng đang ở form của {feature_name}"],
                        "data": {name: "a" * min_len},
                        "steps": [
                            f"Mở form {feature_name}.",
                            f"Nhập {name} có độ dài đúng {min_len} ký tự.",
                            "Bấm nút Submit.",
                        ],
                        "expected": [
                            f"Hệ thống chấp nhận giá trị và không báo lỗi độ dài ở trường {name}."
                        ],
                    }
                )

            if max_len is not None:
                tc_id = next_tc_id(counters, feature_code, field_code, is_bva=True)
                test_cases.append(
                    {
                        "id": tc_id,
                        "title": f"Kiểm thử {name} với độ dài biên tối đa ({max_len} ký tự)",
                        "feature_name": feature_name,
                        "module_name": module_name_display,
                        "technique": "Boundary Value Analysis",
                        "preconditions": [f"Người dùng đang ở form của {feature_name}"],
                        "data": {name: "a" * max_len},
                        "steps": [
                            f"Mở form {feature_name}.",
                            f"Nhập {name} có độ dài đúng {max_len} ký tự.",
                            "Bấm nút Submit.",
                        ],
                        "expected": [
                            f"Hệ thống chấp nhận giá trị và không báo lỗi độ dài ở trường {name}."
                        ],
                    }
                )
                tc_id = next_tc_id(counters, feature_code, field_code, is_bva=True)
                test_cases.append(
                    {
                        "id": tc_id,
                        "title": f"Kiểm thử {name} với độ dài vượt quá tối đa ({max_len + 1} ký tự)",
                        "feature_name": feature_name,
                        "module_name": module_name_display,
                        "technique": "Boundary Value Analysis",
                        "preconditions": [f"Người dùng đang ở form của {feature_name}"],
                        "data": {name: "a" * (max_len + 1)},
                        "steps": [
                            f"Mở form {feature_name}.",
                            f"Nhập {name} có độ dài {max_len + 1} ký tự.",
                            "Bấm nút Submit.",
                        ],
                        "expected": [
                            f"Hệ thống báo lỗi độ dài {name} vượt quá giới hạn tối đa {max_len} ký tự."
                        ],
                    }
                )

        elif inp_type == "numeric":
            min_val = inp.get("min_value")
            max_val = inp.get("max_value")

            if min_val is not None:
                for value, title, expected in [
                    (
                        min_val - 1,
                        f"Kiểm thử {name} nhỏ hơn giá trị tối thiểu ({min_val - 1})",
                        f"Hệ thống báo lỗi giá trị {name} phải lớn hơn hoặc bằng {min_val}.",
                    ),
                    (
                        min_val,
                        f"Kiểm thử {name} đúng giá trị tối thiểu ({min_val})",
                        f"Hệ thống chấp nhận giá trị {min_val} ở trường {name}.",
                    ),
                ]:
                    tc_id = next_tc_id(counters, feature_code, field_code, is_bva=True)
                    test_cases.append(
                        {
                            "id": tc_id,
                            "title": title,
                            "feature_name": feature_name,
                            "module_name": module_name_display,
                            "technique": "Boundary Value Analysis",
                            "preconditions": [
                                f"Người dùng đang ở form của {feature_name}"
                            ],
                            "data": {name: str(value)},
                            "steps": [
                                f"Mở form {feature_name}.",
                                f"Nhập {name} có giá trị {value}.",
                                "Bấm nút Submit.",
                            ],
                            "expected": [expected],
                        }
                    )

            if max_val is not None:
                for value, title, expected in [
                    (
                        max_val,
                        f"Kiểm thử {name} đúng giá trị tối đa ({max_val})",
                        f"Hệ thống chấp nhận giá trị {max_val} ở trường {name}.",
                    ),
                    (
                        max_val + 1,
                        f"Kiểm thử {name} lớn hơn giá trị tối đa ({max_val + 1})",
                        f"Hệ thống báo lỗi giá trị {name} phải nhỏ hơn hoặc bằng {max_val}.",
                    ),
                ]:
                    tc_id = next_tc_id(counters, feature_code, field_code, is_bva=True)
                    test_cases.append(
                        {
                            "id": tc_id,
                            "title": title,
                            "feature_name": feature_name,
                            "module_name": module_name_display,
                            "technique": "Boundary Value Analysis",
                            "preconditions": [
                                f"Người dùng đang ở form của {feature_name}"
                            ],
                            "data": {name: str(value)},
                            "steps": [
                                f"Mở form {feature_name}.",
                                f"Nhập {name} có giá trị {value}.",
                                "Bấm nút Submit.",
                            ],
                            "expected": [expected],
                        }
                    )

    return test_cases


def transition_data(transition, actors):
    actor_name = transition["actor"]
    actor = actors.get(actor_name, {})
    endpoint = transition.get("endpoint") or actor.get("endpoint")
    has_body = "body" in transition
    body = transition.get("body")
    if not has_body and actor_name == "admin" and transition.get("to") is not None:
        body = {"status": transition["to"]}

    return {
        "Actor": actor_name,
        "Current status": transition.get("from"),
        "Requested status": transition.get("to", "[Không gửi]"),
        "Endpoint": endpoint,
        "Body": body if body is not None else "[Không có body]",
        "Order ID": transition.get("order_id", "{existing_order_id}"),
    }


def transition_steps(transition, actors):
    actor_name = transition["actor"]
    actor = actors.get(actor_name, {})
    endpoint = transition.get("endpoint") or actor.get("endpoint")
    has_body = "body" in transition
    body = transition.get("body")
    if not has_body and actor_name == "admin" and transition.get("to") is not None:
        body = {"status": transition["to"]}

    steps = [
        f"Chuẩn bị một đơn hàng đang ở trạng thái `{transition.get('from')}`.",
        f"Đăng nhập bằng tài khoản `{actor_name}` hợp lệ.",
        f"Gửi request `{endpoint}`"
        + (f" với body `{format_value(body)}`." if body is not None else "."),
        "Tải lại thông tin đơn hàng sau khi request hoàn tất.",
    ]
    return steps


def generate_state_transition_cases(config):
    feature_name = config["feature_name"]
    module_name = config["module_name"]
    feature_code = config.get("feature_code") or normalize_feature_code(feature_name)
    field_code = config.get("field_code", "S")
    module_name_display = config.get("module_display_name") or module_display_name(
        module_name
    )
    actors = config.get("actors", {})
    counters = {}
    test_cases = []

    for transition in config.get("valid_transitions", []):
        tc_id = next_tc_id(counters, feature_code, field_code)
        from_status = transition.get("from")
        to_status = transition.get("to")
        actor = transition.get("actor")
        test_cases.append(
            {
                "id": tc_id,
                "title": transition.get("title")
                or f"{actor} chuyển đơn hàng từ {from_status} sang {to_status}",
                "feature_name": feature_name,
                "module_name": module_name_display,
                "technique": "Equivalence Partitioning / State Transition",
                "preconditions": transition.get("preconditions")
                or [
                    f"Có đơn hàng hợp lệ đang ở trạng thái `{from_status}`.",
                    f"Tài khoản `{actor}` đã đăng nhập và có quyền thực hiện thao tác.",
                ],
                "data": transition_data(transition, actors),
                "steps": transition.get("steps") or transition_steps(transition, actors),
                "expected": transition.get("expected")
                or [
                    "Hệ thống trả về HTTP 200.",
                    f"Trạng thái đơn hàng được cập nhật thành `{to_status}`.",
                ],
            }
        )

    for transition in config.get("invalid_transitions", []):
        tc_id = next_tc_id(counters, feature_code, field_code)
        from_status = transition.get("from")
        to_status = transition.get("to")
        actor = transition.get("actor")
        test_cases.append(
            {
                "id": tc_id,
                "title": transition.get("title")
                or f"Từ chối {actor} chuyển đơn hàng từ {from_status} sang {to_status}",
                "feature_name": feature_name,
                "module_name": module_name_display,
                "technique": "Equivalence Partitioning / State Transition",
                "preconditions": transition.get("preconditions")
                or [
                    f"Có đơn hàng hợp lệ đang ở trạng thái `{from_status}`.",
                    f"Tài khoản `{actor}` đã đăng nhập.",
                ],
                "data": transition_data(transition, actors),
                "steps": transition.get("steps") or transition_steps(transition, actors),
                "expected": transition.get("expected")
                or [
                    "Hệ thống trả về HTTP 400 với thông báo lỗi phù hợp.",
                    f"Trạng thái đơn hàng vẫn giữ nguyên là `{from_status}`.",
                ],
            }
        )

    for status_case in config.get("invalid_status_values", []):
        tc_id = next_tc_id(counters, feature_code, field_code)
        transition = {
            "actor": status_case.get("actor", "admin"),
            "from": status_case.get("from", "pending"),
            "to": status_case.get("value"),
            "endpoint": status_case.get("endpoint")
            or actors.get(status_case.get("actor", "admin"), {}).get("endpoint"),
            "body": status_case.get("body", {"status": status_case.get("value")}),
        }
        test_cases.append(
            {
                "id": tc_id,
                "title": status_case.get("title")
                or f"Từ chối giá trị status không hợp lệ `{format_value(status_case.get('value'))}`",
                "feature_name": feature_name,
                "module_name": module_name_display,
                "technique": "Equivalence Partitioning",
                "preconditions": status_case.get("preconditions")
                or [
                    f"Có đơn hàng hợp lệ đang ở trạng thái `{transition['from']}`.",
                    "Admin đã đăng nhập.",
                ],
                "data": transition_data(transition, actors),
                "steps": status_case.get("steps")
                or transition_steps(transition, actors),
                "expected": status_case.get("expected")
                or [
                    "Hệ thống trả về HTTP 400 với thông báo lỗi phù hợp.",
                    f"Trạng thái đơn hàng vẫn giữ nguyên là `{transition['from']}`.",
                ],
            }
        )

    for boundary_case in config.get("boundary_cases", []):
        case_field_code = boundary_case.get("field_code", "O")
        tc_id = next_tc_id(counters, feature_code, case_field_code, is_bva=True)
        test_cases.append(
            {
                "id": tc_id,
                "title": boundary_case["title"],
                "feature_name": feature_name,
                "module_name": module_name_display,
                "technique": "Boundary Value Analysis",
                "preconditions": boundary_case.get("preconditions", []),
                "data": boundary_case.get("data", {}),
                "steps": boundary_case.get("steps", []),
                "expected": boundary_case.get("expected", []),
            }
        )

    return test_cases


def build_cases(config):
    test_model = config.get("test_model", "input_boundary")
    if test_model == "state_transition":
        return generate_state_transition_cases(config)
    if test_model == "input_boundary":
        return generate_input_cases(config)
    raise ValueError(f"Unsupported test_model: {test_model}")


def main():
    parser = argparse.ArgumentParser(description="Tự động sinh test case templates.")
    parser.add_argument("--config", required=True, help="Đường dẫn file JSON cấu hình.")
    parser.add_argument(
        "--output-root",
        help="Ghi đè thư mục output test case trong config.",
    )
    parser.add_argument(
        "--test-run-output-root",
        help="Ghi đè thư mục output test run template trong config.",
    )
    parser.add_argument(
        "--test-run-file",
        help="Ghi đè tên file test run template.",
    )
    parser.add_argument(
        "--skip-test-run",
        action="store_true",
        help="Chỉ sinh test case, không sinh test run template.",
    )
    parser.add_argument(
        "--overwrite-test-run",
        action="store_true",
        help="Ghi đè test run template nếu file đã tồn tại.",
    )
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)

    if args.output_root:
        config["output_root"] = args.output_root

    if (
        args.test_run_output_root
        or args.test_run_file
        or args.skip_test_run
        or args.overwrite_test_run
    ):
        raw_run_config = config.get("test_run", {})
        if not isinstance(raw_run_config, dict):
            raw_run_config = {}
        config["test_run"] = raw_run_config

        if args.test_run_output_root:
            raw_run_config["output_root"] = args.test_run_output_root
        if args.test_run_file:
            raw_run_config["file_name"] = args.test_run_file
        if args.skip_test_run:
            raw_run_config["enabled"] = False
        if args.overwrite_test_run:
            raw_run_config["overwrite"] = True

    test_cases = build_cases(config)
    output_root = config.get("output_root")
    write_cases(
        test_cases,
        module_name=config["module_name"],
        output_root=output_root,
    )
    write_test_run_template(test_cases, config, output_root=output_root)


if __name__ == "__main__":
    main()
