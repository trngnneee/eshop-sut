---
description: Kỹ năng hỗ trợ thiết kế test case tự động sử dụng kỹ thuật Phân vùng tương đương (Equivalence Partitioning) và Phân tích giá trị biên (Boundary Value Analysis) cho các yêu cầu chức năng (FR) của hệ thống EShop.
name: domain-and-boundary-testing
---

# Kỹ năng Kiểm thử Miền & Giá trị Biên (Domain & Boundary Testing Skill)

Kỹ năng này hướng dẫn Agent cách phân tích một Yêu cầu Chức năng (Functional Requirement - FR), xác định các miền dữ liệu, phân vùng tương đương, các giá trị biên và tự động sinh ra các test case chuẩn hóa dưới định dạng Markdown.

---

## 1. Quy trình Áp dụng Kỹ thuật Kiểm thử

Khi nhận được yêu cầu thiết kế test case cho một FR cụ thể, Agent phải tuân thủ nghiêm ngặt quy trình 4 bước sau:

### Bước 1: Xác định biến Đầu vào & Đầu ra (Identify Input & Output variables)

* Xác định tất cả các trường dữ liệu người dùng nhập (ví dụ: Email, Mật khẩu, Số lượng, Mã giảm giá).
* Xác định các trạng thái hệ thống cần thiết (ví dụ: Người dùng đã đăng nhập/chưa đăng nhập, giỏ hàng trống/có sản phẩm, trạng thái đơn hàng hiện tại).
* Với chức năng dạng state machine, xác định thêm `actor`, `current_state`, `requested_state/action`, endpoint/API, và các final state.

### Bước 2: Phân tích Phân vùng tương đương (Equivalence Partitioning - EP)

* Phân chia mỗi tham số đầu vào hoặc điều kiện thành các phân vùng tương đương:
   * **Phân vùng hợp lệ (Valid Partitions):** Các giá trị được hệ thống chấp nhận và xử lý bình thường.
   * **Phân vùng không hợp lệ (Invalid Partitions):** Các giá trị bị hệ thống từ chối hoặc báo lỗi.

* Lập bảng phân vùng tương đương để tiện theo dõi.
* Với state machine, xem mỗi transition hợp lệ/không hợp lệ là một phân vùng cần được bao phủ riêng.

### Bước 3: Phân tích Giá trị biên (Boundary Value Analysis - BVA)

* Đối với các tham số có tính chất số học, độ dài chuỗi, hoặc giới hạn số lượng, xác định các giá trị biên:
   * **Biên dưới (Min):** Giá trị nhỏ nhất hợp lệ.
   * **Ngay dưới biên dưới (Min - 1):** Giá trị không hợp lệ.
   * **Ngay trên biên dưới (Min + 1):** Giá trị hợp lệ.
   * **Biên trên (Max):** Giá trị lớn nhất hợp lệ.
   * **Ngay dưới biên trên (Max - 1):** Giá trị hợp lệ.
   * **Ngay trên biên trên (Max + 1):** Giá trị không hợp lệ.
   * **Giá trị danh nghĩa (Nominal):** Một giá trị bình thường nằm giữa khoảng Min và Max.

### Bước 4: Thiết kế Test Cases & Ghi nhận

* Ghép các phân vùng và giá trị biên để tạo thành danh sách test case.
* Đảm bảo bao phủ tối thiểu:
   * Tất cả các phân vùng hợp lệ ít nhất một lần.
   * Mỗi phân vùng không hợp lệ được kiểm thử bằng một test case riêng biệt (để tránh lỗi này che lấp lỗi khác).
   * Tất cả các giá trị biên đã xác định.

---

## 2. Quy ước đặt mã và Thư mục Lưu trữ

* **Thư mục lưu trữ:** Lưu các file test case dưới định dạng Markdown (`.md`) vào thư mục `tests/test-cases/[tên-module]/`.
   * Ví dụ: `tests/test-cases/profile_management/FR04-N-TC01.md`

* **Quy ước mã Test Case cho Domain Testing:** `FR[NN]-[FIELD]-TC[NN]`
   * Ví dụ: `FR04-N-TC01`, `FR04-P-TC01`, `FR04-A-TC01`.

* **Quy ước mã Test Case cho Boundary Value Analysis:** `FR[NN]-[FIELD]-BVA-TC[NN]`
   * Ví dụ: `FR04-N-BVA-TC01`, `FR04-P-BVA-TC01`, `FR04-A-BVA-TC01`.

* **Mã field ngắn:** dùng một chữ cái đại diện cho input hoặc nhóm input đang kiểm thử.
   * Ví dụ với FR-04: `N` = Name, `P` = Phone, `A` = Address.
   * Ví dụ với FR-10: `S` = Status transition, `O` = Order ID.

---

## 3. Template File Test Case chuẩn Markdown

Mỗi lần phân tích và tạo test case, Agent phải dùng các bảng Markdown sau làm form chuẩn.

| Class ID | Domain Class | Representative Values | Expected Status | Reason |
| :--- | :--- | :--- | :--- | :--- |
| [Class ID] | [Valid/Invalid domain class] | [Representative values] | [Accepted/Rejected] | [Reason] |


| TC ID | Domain Class | Test Data | Steps | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| [TC ID] | [Class ID / Domain Class] | [Test data] | [Execution steps] | [Expected result] |


| Boundary Type | Value | Test Data | Expected Status | Reason |
| :--- | :--- | :--- | :--- | :--- |
| [Min/Min-1/Min+1/Max-1/Max/Max+1/Nominal] | [Boundary value] | [Test data] | [Accepted/Rejected] | [Reason] |


| TC ID | Boundary Type | Test Data | Steps | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| [TC ID] | [Boundary Type] | [Test data] | [Execution steps] | [Expected result] |

### Template File Test Run

Mỗi lần Agent sinh test case bằng skill này, Agent phải tạo thêm một template test run tại `tests/test-runs/[fr]-[module]-test-run.md` để người dùng có thể chạy test và cập nhật kết quả sau. Template phải có các phần chính giống file test run hiện có:

```markdown
# Test Run - [FR] [Module]

__Ngày thực hiện__: [dd/mm/yyyy]  
__Người thực hiện__: [Tên người test]  
__Môi trường thử nghiệm__: [Môi trường thử nghiệm]  

## Tổng quan kết quả

| Nhóm kiểm thử | Domain TC | BVA TC | Tổng TC | Pass | Fail |
| :--- | ---: | ---: | ---: | ---: | ---: |
| [Nhóm input/chuyển trạng thái] | [Số Domain TC] | [Số BVA TC] | [Tổng TC] | 0 | 0 |

## Test Case Execution Report

| Test Case ID | Module | Tester | Result | Related Bug | Note |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [TC ID](../test-cases/[module]/[TC ID].md) | [Module / nhóm] | [Tên người test] | Not Run | None | [Điền actual result / ghi chú sau khi chạy] |

## Defect Log

| Bug ID | Related TC ID | Tóm tắt | Severity | Status | Evidence / Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [BUG-ID] | [TC ID] | [Tóm tắt lỗi] | [High/Medium/Low] | Open | [Actual result / evidence] |
```

---

## 4. Hướng dẫn Tương tác cho Agent (Prompt Guidelines)

Khi kích hoạt kỹ năng này, Agent sẽ:

1. Hỏi người dùng cung cấp tài liệu đặc tả hoặc mô tả yêu cầu của chức năng cần test (nếu chưa có trong README.md).
2. Tự động liệt kê các phân vùng tương đương và các giá trị biên dưới dạng bảng để người dùng xác nhận.
3. Sau khi người dùng xác nhận, Agent sẽ tạo các file test case tương ứng vào đúng thư mục `tests/test-cases/[module]/` với mã test case theo format `FR[NN]-[FIELD]-TC[NN]` hoặc `FR[NN]-[FIELD]-BVA-TC[NN]`.
4. Tạo hoặc kiểm tra template test run tương ứng trong `tests/test-runs/`. Nếu file test run đã tồn tại và có kết quả thật, không ghi đè mặc định; chỉ ghi đè khi người dùng yêu cầu rõ.
5. Cập nhật ma trận truy vết `tests/test-summary/traceability-matrix.md`.
6. Tự động lưu vết (Auto-Logging): Cuối mỗi câu trả lời, Agent BẮT BUỘC phải tự động tạo một block Markdown chứa thông tin log để người dùng copy vào phụ lục AI Audit Report. Đoạn log phải tuân thủ chính xác định dạng mã code sau:

```markdown
Name of the AI tool: [Tên công cụ, VD: ChatGPT-4o / Claude 3.5]
Date and time: [Thời gian hệ thống hiện tại]
Your prompt: [Tóm tắt lại yêu cầu của người dùng]
The AI output: [Ghi chú: Toàn bộ bảng biểu test case được sinh ra ở trên]
```

---

## 5. Hướng dẫn Sử dụng Công cụ Tự động hóa (Automation Script)

Để tối ưu hóa hiệu suất và đảm bảo tính nhất quán của các file test case, Agent nên ưu tiên sử dụng script Python tự động hóa được tích hợp sẵn.

### Các bước thực hiện:

1. **Xác định mô hình kiểm thử** của chức năng:
   * Dùng `test_model: "input_boundary"` cho form/input có `required`, độ dài chuỗi, hoặc biên số.
   * Dùng `test_model: "state_transition"` cho chức năng dạng state machine như FR-10 Order State Machine.

2. **Tạo một file cấu hình JSON** mô tả chức năng:
   * Với input/form, tham khảo `examples/register_config.json`. File JSON chứa `feature_name`, `module_name`, và mảng `inputs` với `name`, `field_code`, `type`, `required`, `min_length`, `max_length`, `min_value`, `max_value`.
   * Với state machine, tham khảo `examples/fr10_order_state_machine_config.json`. File JSON chứa `states`, `final_states`, `actors`, `valid_transitions`, `invalid_transitions`, `invalid_status_values`, và `boundary_cases`.

3. **Chạy script tự động hóa** bằng lệnh:

```bash
python ".agents/skills/domain_and_boundary_testing/scripts/generate_test_cases.py" --config "[đường-dẫn-đến-file-json-cấu-hình]"
```

   * Script mặc định sẽ sinh cả test case và template test run.
   * Dùng `--skip-test-run` nếu chỉ muốn sinh test case.
   * Dùng `--overwrite-test-run` nếu người dùng yêu cầu tạo lại file test run đã tồn tại.
   * Có thể dùng `--test-run-output-root` hoặc `--test-run-file` để đổi thư mục/tên file test run khi cần.

4. **Hậu xử lý (Post-processing):**
   * Script sẽ tự động tạo test case tại `tests/test-cases/[module_name]/` theo đúng mã `FR[NN]-[FIELD]-TC[NN]` hoặc `FR[NN]-[FIELD]-BVA-TC[NN]`.
   * Script sẽ tự động tạo template test run tại `tests/test-runs/[fr]-[module]-test-run.md` với các dòng `Not Run`, `Related Bug = None`, và cột `Note` để điền actual result sau khi chạy.
   * Nếu test run đã tồn tại, script sẽ bỏ qua để tránh làm mất kết quả chạy test/bug mapping đã có.
   * Agent cần đọc lại output để bổ sung test case nghiệp vụ phức tạp chưa thể mô hình hóa hết trong JSON (ví dụ: quyền truy cập, dữ liệu thuộc user khác, hoặc rule còn mơ hồ trong đặc tả).
   * Chỉ xóa file cấu hình tạm; giữ lại các example tái sử dụng như `register_config.json` và `fr10_order_state_machine_config.json`.
