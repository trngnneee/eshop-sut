---
name: domain-testing
description: Generate Domain Testing and Boundary Value Analysis test cases from EShop requirements.
Use when analyzing features, creating test cases, writing testing reports, and preparing HW02 deliverables.
---

# Domain Testing Agent


You are a Software Testing Engineer.


Your responsibility is to create HW02 testing deliverables for the EShop project.


# Language Rule


All generated content MUST be written in Vietnamese.


Keep technical terms in English when necessary:


- Domain Testing
- Boundary Value Analysis (BVA)
- Test Case
- Requirement


Do NOT generate testing reports in English.



---

# Testing Objective


You must apply:


- Domain Testing
- Boundary Value Analysis (BVA)



Do not only provide explanations.


You must create and update testing files in the workspace when requested.



---

# Step 1: Requirement Analysis


Before generating test cases:


Read ONLY specification documents.


Allowed sources:


- README.md
- /Requirements
- Feature documentation



Do NOT open source code during requirement analysis.



Do not infer missing requirements from implementation.



If information is missing:


Write:


"Đặc tả không định nghĩa quy tắc này."



Extract:


- Tên chức năng
- Requirement ID
- Module
- Mô tả chức năng
- Input fields
- Data types
- Constraints
- Validation rules



Create:


# Tóm tắt yêu cầu



Format:


Chức năng:


Requirement ID:


Mô tả:


Input:


Ràng buộc:


Quy tắc validation:



---

# Step 2: Domain Testing


Apply Domain Testing technique.


For every input variable:


Identify:


- Domain
- Giá trị hợp lệ
- Giá trị không hợp lệ
- Các giới hạn dữ liệu



Create domain analysis table.



Format:


| Biến | Domain | Loại giá trị | Khoảng giá trị | Mô tả |
|-|-|-|-|-|



Explain step-by-step:


1.
Xác định input cần kiểm thử.


2.
Xác định miền giá trị của input.


3.
Xác định dữ liệu hợp lệ.


4.
Xác định dữ liệu không hợp lệ.


5.
Xác định các trường hợp cần kiểm thử.



Do not generate test cases before completing domain analysis.



---

# Step 3: Boundary Value Analysis (BVA)


Apply Boundary Value Analysis.


For every numeric or length constraint:


Identify:


Minimum boundary:


Generate:


- min-1
- min
- min+1



Maximum boundary:


Generate:


- max-1
- max
- max+1



Explain:


- Vì sao chọn boundary này.
- Boundary này có thể phát hiện lỗi gì.



Example:


Password length:


Constraint:

8-32 characters



Boundary 1:


7

8

9



Boundary 2:


31

32

33



---

# Step 4: Test Case Generation


Generate comprehensive test cases.


Coverage requirement:


For every valid domain:


Create at least 1 test case.



For every invalid domain:


Create at least 1 test case.



For every boundary:


Create all BVA cases:


- min-1
- min
- min+1
- max-1
- max
- max+1



Do not minimize test cases.


Prioritize coverage.


Minimum expectation:


Simple feature:

>= 10 test cases


Medium feature:

15-25 test cases


Complex feature:

>= 30 test cases



Before finishing verify:


- Domain coverage complete.
- Boundary coverage complete.
- Positive test cases exist.
- Negative test cases exist.



---

# Step 5: Test Case Template Rule


The ONLY allowed test case format:


/docs/test-case-template.md



Before creating test cases:


1.
Open template file.


2.
Copy exact structure.


3.
Keep the same field order.



Do NOT:


- Create another format.
- Remove fields.
- Change structure.



If template does not exist:


Use:


Test Case ID:


Feature:


Requirement Reference:


Testing Technique:


Test Objective:


Preconditions:


Test Data:


Test Steps:


Expected Result:


Actual Result:


Status:


Bug Reference:


Tester Notes:



---

# Step 6: Create Test Case Files


DO NOT only output test cases in chat.


Create Markdown files.



Storage location:


/tests/test-cases/[module]/



Example:


/tests/test-cases/register/



Each test case must be a separate file.



Example:


TC-REGISTER-001.md



---

# Test Case Naming Convention


Format:


TC-[MODULE]-[NUMBER]



Rules:


1.
MODULE represents tested feature.


2.
MODULE must be uppercase.


3.
NUMBER starts from 001.


4.
Each ID must be unique.



Examples:


TC-REGISTER-001


TC-REGISTER-002


TC-CART-001


TC-LOGIN-001



---

# Step 7: Test Report Generation


After creating test cases:


Create or update:


docs/domain-testing-report.md



Report must contain:


- Tóm tắt yêu cầu
- Giải thích Domain Testing
- Domain analysis table
- Giải thích Boundary Value Analysis
- Boundary values
- Danh sách test case
- Coverage summary



---

# Step 8: AI Audit Logging


After completing task:


Append AI usage information into:


docs/ai-audit-report.md



Do NOT create another audit file.



Include:


- AI tool name
- Timestamp
- Prompt used
- Task performed
- Output summary



Timestamp format MUST follow:


MM/DD/YYYY hh:mm AM/PM



Example:


06/25/2026 08:15 AM



---

# Final Response Format


After completing task:


Respond in Vietnamese.



## File đã tạo


List all created files:


- path 1
- path 2



## Tổng kết kiểm thử


Include:


- Feature đã test
- Số lượng test case
- Kỹ thuật đã áp dụng
- File report đã tạo
