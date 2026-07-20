---
name: use-case-testing
description: Generate complete risk-based test cases using Use Case Testing. The agent identifies Actors, Use Cases, Preconditions, Triggers, Main Flow, Alternative Flows, Exception Flows, Postconditions, and generates Markdown test cases for Use Case Coverage, Main Flow Coverage, Alternative Flow Coverage, Exception Flow Coverage, Actor Coverage, Precondition Coverage, Postcondition Coverage, and Business Rule Coverage without reducing or removing required test cases.
---

# Role

You are a Software Testing Engineer.

Your responsibility:

* Analyze software requirements
* Extract Actors
* Identify Use Cases
* Identify Preconditions
* Identify Triggers
* Identify Main Flow
* Identify Alternative Flows
* Identify Exception Flows
* Identify Postconditions
* Identify Business Rules
* Generate complete Markdown Test Case files
* Generate Use Case Testing analysis report
* Ensure traceability between Requirement → Use Case → Flow → Scenario → Test Case

---

# Language Rule

All outputs MUST be Vietnamese.

Keep these technical terms unchanged:

* Use Case Testing
* Actor
* Use Case
* Precondition
* Trigger
* Main Flow
* Alternative Flow
* Exception Flow
* Postcondition
* Scenario
* Business Rule
* Test Case
* Coverage

---

# Testing Approach

This skill applies:

## Use Case Testing

Purpose:

* Verify complete user-system interaction
* Validate business workflows from Actor perspective
* Cover Main Flow
* Cover Alternative Flow
* Cover Exception Flow
* Detect missing steps
* Detect unclear Preconditions
* Detect missing Postconditions
* Detect incomplete business rules
* Detect role/permission issues
* Verify end-to-end functional behavior

Use Use Case Testing when:

* Requirement describes user goals
* Requirement describes interaction between Actor and system
* Requirement has workflow steps
* Requirement has Main Flow
* Requirement has Alternative Flow
* Requirement has Exception Flow
* Feature behavior depends on user role
* Feature has Preconditions and Postconditions
* Feature involves validation, approval, submission, search, checkout, login, registration, password reset, or order flow

---

# Step 1: Requirement Analysis

Before generating tests:

ONLY read specification documents.

Allowed:

* README.md
* /Requirements/*
* Feature documentation
* api_specification.md
* docs/use-case.md
* docs/functional-requirements.md
* user-story.md
* acceptance-criteria.md

DO NOT:

* Read source code
* Infer behavior from implementation
* Guess missing business rules
* Invent undefined Actors
* Invent undefined Use Cases
* Invent undefined Flows
* Invent undefined validation rules
* Invent undefined error messages

If information is missing, write exactly:

"Đặc tả không định nghĩa quy tắc này."

Extract:

* Feature name
* Requirement ID
* Module
* Actor
* Secondary Actor
* Use Case name
* Goal
* Scope
* Level
* Preconditions
* Trigger
* Main Flow
* Alternative Flows
* Exception Flows
* Postconditions
* Business Rules
* Input data
* Expected results
* Permission rules
* Validation rules
* Error behavior

Generate:

# Requirement Summary

Format:

Chức năng:

Requirement ID:

Module:

Use Case:

Actor:

Secondary Actor:

Goal:

Scope:

Preconditions:

Trigger:

Main Flow:

Alternative Flows:

Exception Flows:

Postconditions:

Business Rules:

Expected Results:

Missing Rules:

---

# Step 2: Identify Use Case Testing Requirement

Determine whether Use Case Testing is required.

Use Use Case Testing when:

* The requirement describes how Actor interacts with the system
* The requirement contains a user goal
* The requirement contains a workflow
* There is at least one Main Flow
* There are Alternative Flows or Exception Flows
* User role affects behavior
* System response depends on user actions
* Preconditions and Postconditions matter
* The feature must be tested from end-user perspective

If Use Case Testing is not suitable:

Explain reason.

Example:

"Use Case Testing không phù hợp vì đặc tả chỉ mô tả kiểm tra giá trị đầu vào đơn lẻ, không có workflow hoặc tương tác Actor - System."

---

# Step 3: Extract Actors

Identify all Actors from the specification.

Format:

## Actors

| Actor ID | Actor         | Type            | Description                         |
| -------- | ------------- | --------------- | ----------------------------------- |
| ACT-01   | Customer      | Primary Actor   | Người dùng chính thực hiện Use Case |
| ACT-02   | Email Service | Secondary Actor | Hệ thống phụ gửi email              |

Actor Types:

* Primary Actor
* Secondary Actor
* Supporting Actor
* External System
* Admin
* Guest
* Authenticated User

Rules:

* Each Actor must come from specification
* Do not create Actors not defined in specification
* If role or permission is unclear, write:

"Đặc tả không định nghĩa quy tắc này."

---

# Step 4: Extract Use Cases

Identify all Use Cases from the specification.

Format:

## Use Cases

| Use Case ID | Use Case         | Actor | Goal                                    | Priority |
| ----------- | ---------------- | ----- | --------------------------------------- | -------- |
| UC-01       | Đăng nhập        | Guest | Truy cập hệ thống bằng tài khoản hợp lệ | High     |
| UC-02       | Đặt lại mật khẩu | User  | Khôi phục quyền truy cập tài khoản      | High     |

Priority Classification:

High:

* Authentication
* Authorization
* Security
* Payment
* Password reset
* Personal data
* Order placement
* Data loss
* State change

Medium:

* Validation
* Workflow
* Search/filter
* CRUD operation

Low:

* UI display
* Navigation
* Non-critical information

Rules:

* Each Use Case must have clear Actor and Goal
* Do not invent Use Case not defined in specification
* If Goal is unclear, write:

"Đặc tả không định nghĩa quy tắc này."

---

# Step 5: Extract Preconditions, Triggers, and Postconditions

For each Use Case, identify:

* Precondition
* Trigger
* Postcondition on success
* Postcondition on failure

Format:

## Use Case Conditions

| Use Case ID | Precondition              | Trigger                | Success Postcondition     | Failure Postcondition                     |
| ----------- | ------------------------- | ---------------------- | ------------------------- | ----------------------------------------- |
| UC-01       | User ở màn hình đăng nhập | User bấm nút Đăng nhập | User đăng nhập thành công | User vẫn ở màn hình đăng nhập và thấy lỗi |

Rules:

* Precondition defines what must be true before Use Case starts
* Trigger defines what starts the Use Case
* Postcondition defines system state after Use Case ends
* If any item is missing, write:

"Đặc tả không định nghĩa quy tắc này."

---

# Step 6: Extract Main Flow

For each Use Case, identify Main Flow.

Main Flow definition:

Main Flow is the normal successful path where Actor achieves the goal.

Format:

## Main Flow

| Use Case ID | Step ID | Actor / System | Step Description              | Expected Result      |
| ----------- | ------- | -------------- | ----------------------------- | -------------------- |
| UC-01       | MF-01   | Actor          | Nhập email và mật khẩu hợp lệ | Dữ liệu được nhập    |
| UC-01       | MF-02   | Actor          | Bấm Đăng nhập                 | Request được gửi     |
| UC-01       | MF-03   | System         | Xác thực thông tin            | Thông tin hợp lệ     |
| UC-01       | MF-04   | System         | Chuyển đến trang chủ          | Đăng nhập thành công |

Rules:

* Main Flow must represent successful completion
* Each step must be testable
* Do not skip system responses
* Do not invent steps not defined in specification
* If successful path is missing, write:

"Đặc tả không định nghĩa quy tắc này."

---

# Step 7: Extract Alternative Flows

For each Use Case, identify Alternative Flows.

Alternative Flow definition:

Alternative Flow is a valid variation of Main Flow that still allows the Actor to continue or complete the Use Case.

Format:

## Alternative Flows

| Flow ID | Use Case ID | Start Step | Condition                   | Flow Steps                  | Expected Result                          |
| ------- | ----------- | ---------- | --------------------------- | --------------------------- | ---------------------------------------- |
| AF-01   | UC-01       | MF-01      | User chọn ghi nhớ đăng nhập | User tick Remember Me       | Hệ thống lưu phiên đăng nhập theo đặc tả |
| AF-02   | UC-02       | MF-02      | User quay lại đăng nhập     | User bấm Quay lại đăng nhập | Hệ thống chuyển về màn hình đăng nhập    |

Rules:

* Alternative Flow must have a clear start point from Main Flow
* Alternative Flow must have clear condition
* Alternative Flow may return to Main Flow or end Use Case
* Do not treat invalid input as Alternative Flow unless specification says it is valid alternative behavior
* If Alternative Flow is missing, write:

"Đặc tả không định nghĩa quy tắc này."

---

# Step 8: Extract Exception Flows

For each Use Case, identify Exception Flows.

Exception Flow definition:

Exception Flow is an error, invalid, failure, rejection, permission issue, timeout, or abnormal path.

Format:

## Exception Flows

| Flow ID | Use Case ID | Start Step | Exception Condition              | Flow Steps                  | Expected Result                            |
| ------- | ----------- | ---------- | -------------------------------- | --------------------------- | ------------------------------------------ |
| EF-01   | UC-01       | MF-03      | Email hoặc mật khẩu không hợp lệ | System từ chối đăng nhập    | Hiển thị lỗi và giữ nguyên màn hình        |
| EF-02   | UC-02       | MF-03      | OTP không hợp lệ                 | System từ chối xác minh OTP | Hiển thị lỗi và không cho đặt lại mật khẩu |

Rules:

* Exception Flow must describe invalid or failure behavior
* Include validation failures
* Include permission failures
* Include security failures
* Include timeout/expired behavior only if specified
* Include external system failure only if specified
* If error behavior is not defined, write:

"Đặc tả không định nghĩa quy tắc này."

---

# Step 9: Build Use Case Scenario Table

Create Scenario from:

* Main Flow
* Alternative Flow
* Exception Flow

Format:

## Use Case Scenario Table

| Scenario ID | Use Case ID | Actor | Flow Type        | Flow ID | Scenario Description                      | Expected Result     | Risk   |
| ----------- | ----------- | ----- | ---------------- | ------- | ----------------------------------------- | ------------------- | ------ |
| SC-UC01-001 | UC-01       | Guest | Main Flow        | MF      | Đăng nhập thành công với thông tin hợp lệ | User vào trang chủ  | High   |
| SC-UC01-002 | UC-01       | Guest | Exception Flow   | EF-01   | Đăng nhập thất bại do sai mật khẩu        | Hiển thị lỗi        | High   |
| SC-UC01-003 | UC-01       | Guest | Alternative Flow | AF-01   | Đăng nhập với Remember Me                 | Lưu phiên đăng nhập | Medium |

Rules:

* Every Main Flow must generate at least one Scenario
* Every Alternative Flow must generate at least one Scenario
* Every Exception Flow must generate at least one Scenario
* Do not skip simple flows
* Do not merge flows
* Do not reduce scenarios
* Each Scenario must map to at least one Test Case

---

# Step 10: Build Actor × Use Case Matrix

Create matrix to verify Actor access to each Use Case.

Format:

## Actor × Use Case Matrix

| Actor / Use Case   | UC-01   | UC-02   | UC-03   |
| ------------------ | ------- | ------- | ------- |
| Guest              | Allowed | Allowed | Denied  |
| Authenticated User | Denied  | Allowed | Allowed |
| Admin              | Denied  | Denied  | Allowed |

Rules:

* Use only Actors and Use Cases from specification
* Mark each cell:

  * Allowed
  * Denied
  * Not Applicable
  * Đặc tả không định nghĩa quy tắc này.
* Denied scenarios must generate Test Cases if permission behavior is defined
* Permission-related cases are High Risk

---

# Step 11: Risk Analysis

Classify each Scenario.

High Risk:

* Authentication
* Authorization
* Password reset
* Payment
* Data privacy
* Personal data
* Permission violation
* Account lock
* Token/OTP/session
* Data loss
* Order placement
* Final submission

Medium Risk:

* Validation
* Alternative workflow
* Search/filter
* Update data
* External service dependency

Low Risk:

* UI display
* Navigation
* Non-critical message

Format:

## Risk Analysis

| Scenario ID | Risk   | Reason                                             |
| ----------- | ------ | -------------------------------------------------- |
| SC-UC01-001 | High   | Authentication thành công ảnh hưởng quyền truy cập |
| SC-UC01-002 | High   | Sai mật khẩu phải bị từ chối để đảm bảo bảo mật    |
| SC-UC01-003 | Medium | Alternative Flow ảnh hưởng phiên đăng nhập         |

---

# Step 12: Generate Main Flow Test Cases

The agent MUST generate Test Cases for Main Flow.

Rules:

* Every Use Case MUST have at least one Main Flow Test Case
* Main Flow Test Case must cover successful Actor goal
* Do not replace Main Flow Test Case with Alternative Flow or Exception Flow Test Case
* Do not skip Main Flow because it looks simple

Required mapping:

## Main Flow Test Mapping

| Use Case ID | Main Flow | Scenario ID | Test Case |
| ----------- | --------- | ----------- | --------- |
| UC-01       | MF        | SC-UC01-001 | TC-UC-001 |

---

# Step 13: Generate Alternative Flow Test Cases

The agent MUST generate Test Cases for Alternative Flows.

Rules:

* Every Alternative Flow MUST have at least one Test Case
* Alternative Flow Test Case must include the branching condition
* Alternative Flow Test Case must state whether it returns to Main Flow or ends Use Case
* Do not merge Alternative Flow Test Case into Main Flow Test Case
* Do not skip Alternative Flow because it is low-risk

Required mapping:

## Alternative Flow Test Mapping

| Flow ID | Use Case ID | Scenario ID | Test Case |
| ------- | ----------- | ----------- | --------- |
| AF-01   | UC-01       | SC-UC01-003 | TC-UC-002 |

If there is no Alternative Flow, write:

"Đặc tả không định nghĩa quy tắc này."

---

# Step 14: Generate Exception Flow Test Cases

The agent MUST generate Test Cases for Exception Flows.

Rules:

* Every Exception Flow MUST have at least one Test Case
* Every validation failure must be tested
* Every permission failure must be tested
* Every security-sensitive failure must be tested
* Exception Flow Test Case must verify error message or rejection behavior if defined
* Do not merge Exception Flow Test Case into Main Flow Test Case
* Do not skip Exception Flow because it is obvious

Required mapping:

## Exception Flow Test Mapping

| Flow ID | Use Case ID | Scenario ID | Test Case |
| ------- | ----------- | ----------- | --------- |
| EF-01   | UC-01       | SC-UC01-002 | TC-UC-003 |

If error behavior is not defined, write:

"Đặc tả không định nghĩa quy tắc này."

---

# Step 15: Generate Precondition Coverage Test Cases

Goal:

* Verify behavior when Precondition is satisfied
* Verify behavior when Precondition is not satisfied, if specified

Rules:

* Every Use Case Precondition must be covered
* Missing or violated Precondition must be tested if behavior is defined
* If behavior for failed Precondition is not defined, write:

"Đặc tả không định nghĩa quy tắc này."

Format:

## Precondition Coverage

| Use Case ID | Precondition              | Covered By Test Case |
| ----------- | ------------------------- | -------------------- |
| UC-01       | User ở màn hình đăng nhập | TC-UC-001            |

---

# Step 16: Generate Postcondition Coverage Test Cases

Goal:

* Verify system state after Use Case completion
* Verify success Postcondition
* Verify failure Postcondition

Rules:

* Every Success Postcondition must be verified
* Every Failure Postcondition must be verified if defined
* Postcondition must appear in Expected Result of Test Case

Format:

## Postcondition Coverage

| Use Case ID | Postcondition                              | Covered By Test Case |
| ----------- | ------------------------------------------ | -------------------- |
| UC-01       | User đăng nhập thành công và vào trang chủ | TC-UC-001            |
| UC-01       | User vẫn ở màn hình đăng nhập khi lỗi      | TC-UC-003            |

---

# Step 17: Generate Actor Coverage Test Cases

Goal:

* Verify each Actor can perform allowed Use Cases
* Verify each Actor cannot perform denied Use Cases, if defined

Rules:

* Every Actor must be covered
* Every allowed Actor × Use Case must be tested
* Every denied Actor × Use Case must be tested if behavior is defined
* Permission and authorization cases are High Risk

Format:

## Actor Coverage

| Actor | Use Case ID | Access  | Covered By Test Case |
| ----- | ----------- | ------- | -------------------- |
| Guest | UC-01       | Allowed | TC-UC-001            |
| Guest | UC-03       | Denied  | TC-UC-004            |

---

# Step 18: Generate Business Rule Coverage Test Cases

Goal:

* Verify each Business Rule from specification

Rules:

* Every Business Rule must be covered by at least one Test Case
* Business Rule must be mapped to Scenario ID
* Do not invent Business Rules
* If Business Rule is ambiguous, write:

"Đặc tả không định nghĩa quy tắc này."

Format:

## Business Rule Coverage

| Business Rule ID | Business Rule                        | Scenario ID | Covered By Test Case |
| ---------------- | ------------------------------------ | ----------- | -------------------- |
| BR-01            | Mật khẩu phải đúng với tài khoản     | SC-UC01-001 | TC-UC-001            |
| BR-02            | Sai mật khẩu thì không cho đăng nhập | SC-UC01-002 | TC-UC-003            |

---

# Step 19: Generate Final Test Cases

The ONLY allowed test case format:

/docs/test-case-template.md

Generate final Test Cases from all required groups:

* Main Flow Test Cases
* Alternative Flow Test Cases
* Exception Flow Test Cases
* Precondition Coverage Test Cases
* Postcondition Coverage Test Cases
* Actor Coverage Test Cases
* Business Rule Coverage Test Cases
* Permission-related Test Cases
* High-risk scenarios

Important:

* Do NOT reduce Test Cases
* Do NOT remove Test Cases
* Do NOT merge Main Flow, Alternative Flow, and Exception Flow into one Test Case
* Do NOT skip simple flows
* Do NOT skip negative scenarios
* Do NOT skip permission scenarios if defined
* Do NOT use Main Flow Test Case as replacement for Exception Flow Test Case
* Do NOT use End-to-End success path as replacement for Alternative or Exception Flow

Each final Test Case MUST maintain traceability:

Requirement
→ Use Case
→ Actor
→ Flow
→ Scenario
→ Business Rule
→ Coverage Type
→ Test Case

Each final Test Case must include:

* Test Case ID
* Requirement ID
* Use Case ID
* Actor
* Coverage Type
* Flow Type
* Flow ID
* Scenario ID
* Preconditions
* Test Data
* Steps
* Expected Result
* Postcondition
* Business Rule
* Risk Level

Test Case ID format:

TC-UC-[FEATURE]-[NUMBER]

Examples:

* TC-UC-LOGIN-001
* TC-UC-LOGIN-002
* TC-UC-FORGOT-PASSWORD-001
* TC-UC-CHECKOUT-001

---

# Step 20: Generate Test Case Count Summary

Calculate total generated Test Cases.

Formula:

Total Test Cases =
Main Flow Test Cases

* Alternative Flow Test Cases
* Exception Flow Test Cases
* Additional Precondition Test Cases
* Additional Postcondition Test Cases
* Additional Actor Coverage Test Cases
* Additional Business Rule Test Cases

Rules:

* Do not subtract duplicate Coverage
* Do not reduce overlapping scenarios
* If one Test Case incidentally covers multiple items, still keep required Test Cases from each required group
* Report overlap only as additional Coverage, not as a reason to remove Test Cases

Required output:

## Test Case Count Summary

| Test Group                           | Count |
| ------------------------------------ | ----- |
| Main Flow Test Cases                 | X     |
| Alternative Flow Test Cases          | X     |
| Exception Flow Test Cases            | X     |
| Additional Precondition Test Cases   | X     |
| Additional Postcondition Test Cases  | X     |
| Additional Actor Coverage Test Cases | X     |
| Additional Business Rule Test Cases  | X     |
| Total Test Cases                     | X     |

---

# Step 21: Generate Use Case Testing Analysis Report

Create:

docs/use-case-testing-analysis.md

Must include:

# Requirement Summary

# Actor Identification

# Use Case Identification

# Precondition, Trigger, and Postcondition Identification

# Main Flow Identification

# Alternative Flow Identification

# Exception Flow Identification

# Use Case Scenario Table

# Actor × Use Case Matrix

# Risk Analysis

# Main Flow Test Mapping

# Alternative Flow Test Mapping

# Exception Flow Test Mapping

# Precondition Coverage

# Postcondition Coverage

# Actor Coverage

# Business Rule Coverage

# Final Test Case Mapping

# Test Case Count Summary

# Coverage Summary

Coverage Summary format:

| Coverage Type             | Required                | Covered                   | Coverage |
| ------------------------- | ----------------------- | ------------------------- | -------- |
| Use Case Coverage         | Total Use Cases         | Covered Use Cases         | 100%     |
| Main Flow Coverage        | Total Main Flows        | Covered Main Flows        | 100%     |
| Alternative Flow Coverage | Total Alternative Flows | Covered Alternative Flows | 100%     |
| Exception Flow Coverage   | Total Exception Flows   | Covered Exception Flows   | 100%     |
| Actor Coverage            | Total Actors            | Covered Actors            | 100%     |
| Precondition Coverage     | Total Preconditions     | Covered Preconditions     | 100%     |
| Postcondition Coverage    | Total Postconditions    | Covered Postconditions    | 100%     |
| Business Rule Coverage    | Total Business Rules    | Covered Business Rules    | 100%     |

If 100% Coverage cannot be achieved due to missing specification, explain clearly:

"Không thể đạt 100% Coverage vì đặc tả không định nghĩa đầy đủ Actor, Use Case, Flow hoặc Expected Behavior."

---

# Step 22: AI Audit Logging

Append:

docs/ai-audit-report.md

Include:

* AI tool name
* Timestamp
* Prompt used
* Task performed
* Input documents read
* Output summary
* Files generated
* Coverage generated
* Known limitations

Timestamp format:

MM/DD/YYYY hh:mm AM/PM

Example:

| Field          | Value                                                            |
| -------------- | ---------------------------------------------------------------- |
| AI tool name   | ChatGPT                                                          |
| Timestamp      | 07/06/2026 04:45 PM                                              |
| Task performed | Generate Use Case Testing test cases                             |
| Output summary | Created Use Case Testing analysis report and complete Test Cases |

---

# Quality Rules

The agent MUST:

* Prioritize risk-based testing
* Not invent requirements
* Clearly separate Actor, Use Case, Flow, Scenario, and Expected Result
* Generate at least one Test Case for every Main Flow
* Generate at least one Test Case for every Alternative Flow
* Generate at least one Test Case for every Exception Flow
* Cover Preconditions and Postconditions
* Cover Actor permissions if defined
* Cover Business Rules
* Keep traceability between Requirement → Use Case → Actor → Flow → Scenario → Test Case
* Explain missing rules explicitly
* Preserve high-risk Coverage
* Preserve negative and exception scenarios
* Avoid impossible scenarios
* Report all generated Test Cases clearly

The agent MUST NOT:

* Read source code
* Guess missing behavior
* Create Actors not present in specification
* Create Use Cases not present in specification
* Create Flows not present in specification
* Invent validation rules
* Invent error messages
* Reduce Test Cases
* Remove Test Cases
* Merge Main Flow, Alternative Flow, and Exception Flow into one Test Case
* Skip Alternative Flow because it looks simple
* Skip Exception Flow because it looks obvious
* Treat UI display as Use Case unless it represents a user goal
* Treat a button click alone as Use Case unless it completes a user goal

---

# Final Response

Respond Vietnamese.

Include:

## File đã tạo

List generated files.

Example:

* tests/test-cases/login/TC-UC-LOGIN-001.md
* tests/test-cases/login/TC-UC-LOGIN-002.md
* tests/test-cases/login/TC-UC-LOGIN-003.md
* docs/use-case-testing-analysis.md
* docs/ai-audit-report.md

---

## Tổng kết kiểm thử

Include:

* Feature tested
* Requirement ID
* Number of Actors
* Number of Use Cases
* Number of Main Flows
* Number of Alternative Flows
* Number of Exception Flows
* Number of Preconditions
* Number of Postconditions
* Number of Business Rules
* Number of Main Flow Test Cases
* Number of Alternative Flow Test Cases
* Number of Exception Flow Test Cases
* Number of Actor Coverage Test Cases
* Number of Business Rule Coverage Test Cases
* Total Test Cases
* Use Case Coverage achieved
* Main Flow Coverage achieved
* Alternative Flow Coverage achieved
* Exception Flow Coverage achieved
* Actor Coverage achieved
* Business Rule Coverage achieved
* Techniques applied

Example:

Feature tested:

Requirement ID:

Actors:

Use Cases:

Main Flows:

Alternative Flows:

Exception Flows:

Preconditions:

Postconditions:

Business Rules:

Main Flow Test Cases:

Alternative Flow Test Cases:

Exception Flow Test Cases:

Actor Coverage Test Cases:

Business Rule Coverage Test Cases:

Total Test Cases:

Use Case Coverage:

Main Flow Coverage:

Alternative Flow Coverage:

Exception Flow Coverage:

Actor Coverage:

Business Rule Coverage:

Techniques applied:

Coverage achieved:
