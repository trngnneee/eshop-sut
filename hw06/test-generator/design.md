# AI API test-generator — design và pseudocode

## Mục tiêu

Generator nhận một endpoint JSON nhỏ, tạo test-case IR có mã ổn định và render ra Markdown/Postman skeleton. Nó không quyết định oracle cuối cùng: mọi expected result phải đi qua audit đối chiếu đặc tả và SUT.

## Input / output

- Input: `method`, `path`, `name`, `parameters`, `states`, `requirements`, `response_schema`.
- Intermediate representation: `{id, group, technique, title, precondition, data, expected, requirement, source}`.
- Output: bảng Markdown, Postman collection item tối thiểu và audit hook (đếm duplicate/missing expected).

## Pseudocode

```text
parse(endpoint_json)
model = ParameterModel(parameters, states, requirements)
cases = []
for parameter in model.parameters:
    cases += partition_cases(parameter)       # valid/invalid EP + boundaries
for transition in model.transitions:
    cases += transition_cases(transition)     # allowed, forbidden, terminal
for control in applicable_security_controls(model):
    cases += security_cases(control)          # auth, IDOR, injection, leakage
for field in model.response_schema:
    cases += schema_cases(field)              # type, required, content type
cases = stable_ids(dedupe(cases), prefix_for(endpoint))
audit = audit_hook(cases)                     # missing expected, duplicate id, unsafe oracle
render_markdown(cases, audit)
render_postman_skeleton(cases)
append_ai_audit_entry(tool, prompt, output_paths)
```

## Quyết định thiết kế

Stable IDs dùng endpoint prefix + số thứ tự để dễ traceability. Các generator groups được giữ riêng để reviewer thấy coverage; state model được truyền explicit thay vì suy ra ngầm. Security cases dùng negative assertions (không bypass/không lộ secret), còn schema cases không tự cấm field ngoài contract nếu spec chưa nói rõ.

## Giới hạn đã biết

Generator không thể tự biết dữ liệu seed, timing lockout, ownership hay precondition stateful của backend. Với API-3, ma trận 5×5 vẫn cần harness chuẩn bị `from_status` cho từng ô. Human review là bắt buộc trước khi biến output thành expected oracle hoặc tạo issue.

## Sơ đồ

`diagram.png` là artifact **HUMAN-ONLY** theo R-16 và hiện **chưa có**. Người học tự ra quyết định bố cục, tự vẽ và tự lưu ảnh; Codex không tạo, render hoặc chỉnh sửa ảnh này.

[`DRAWING-BRIEF.md`](DRAWING-BRIEF.md) chỉ liệt kê các khối/quan hệ tối thiểu để người học tự vẽ. File [`_reference/diagram-notes.mmd`](_reference/diagram-notes.mmd) là ghi chú do AI sinh được lưu riêng nhằm minh bạch provenance; nó **không phải sơ đồ nộp bài** và không được export thành `diagram.png`.
