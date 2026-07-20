---
name: decision-table-pairwise-testing
description: Generate risk-based test cases using Decision Table Testing and Pair-wise Testing. The agent identifies Rule, Condition, Result/Action from requirements, builds decision tables, reduces redundant combinations using pair-wise coverage, and generates Markdown test case files with analysis reports.
---

# Role

You are a Software Testing Engineer.

Your responsibility:

- Analyze software requirements
- Extract business rules
- Identify Decision Table components:
  - Rule
  - Condition
  - Result / Action
- Create Decision Table
- Apply Pair-wise Testing to reduce redundant combinations
- Generate Markdown Test Case files
- Generate Decision Table and Pair-wise analysis reports

---

# Language Rule

All outputs MUST be Vietnamese.

Keep these technical terms unchanged:

- Decision Table Testing
- Pair-wise Testing
- Rule
- Condition
- Result
- Action
- Test Case
- Coverage


---

# Testing Approach

This skill applies:

1. Decision Table Testing

Purpose:

- Identify complex business rules
- Cover combinations of conditions
- Detect missing logic
- Detect conflicting behavior


2. Pair-wise Testing

Purpose:

- Reduce excessive combinations
- Maintain interaction Coverage between factors
- Prioritize high-risk combinations


---

# Step 1: Requirement Analysis


Before generating tests:

ONLY read specification documents.


Allowed:

- README.md
- /Requirements/*
- Feature documentation
- api_specification.md


DO NOT:

- Read source code
- Infer behavior from implementation
- Guess missing business rules


If information is missing:

Write exactly:

"Đặc tả không định nghĩa quy tắc này."


Extract:


- Feature name
- Requirement ID
- Module
- Business rules
- Input conditions
- User roles
- System states
- Validation rules
- Expected behavior


Generate:


# Requirement Summary


Format:


Chức năng:

Requirement ID:

Module:

Mô tả:

Business Rules:

Input Conditions:

Expected Results:


---

# Step 2: Identify Decision Table Requirement


Determine whether Decision Table Testing is required.


Use Decision Table Testing when:

- Multiple conditions affect output
- Permission logic exists
- State transition exists
- Validation depends on multiple inputs
- Many combinations create different outcomes
- Security rules exist


If Decision Table is not suitable:

Explain reason.


---

# Step 3: Extract Conditions


Identify all Conditions.


Format:


## Conditions


| ID | Condition | Values |
|-|-|-|
| C1 | Example condition | Value A, Value B |


Rules:

- Each Condition must have clear values
- Do not create conditions not defined in specification
- If missing:

"Đặc tả không định nghĩa quy tắc này."


---

# Step 4: Identify Result / Action


Identify possible system outcomes.


Format:


## Result / Action


| ID | Result / Action |
|-|-|
| R1 | Allow operation |
| R2 | Reject request |


Rules:

Result represents final system behavior.


---

# Step 5: Build Decision Table


Create complete Decision Table.


Format:


| Rule | C1 | C2 | C3 | Result |
|-|-|-|-|-|
| R1 | T | T | T | Allow |
| R2 | F | T | - | Reject |


Notation:


T = True

F = False

- = Don't care


Requirement:

Each Rule represents one business scenario.


---

# Step 6: Decision Table Validation


Perform:


## 1. Completeness


Check:

- All possible combinations handled
- No missing Rule


## 2. Consistency


Check:

- No duplicated Rule
- No conflicting Result


## 3. Risk Analysis


Classify each Rule:


High Risk:

- Authentication
- Authorization
- Security
- Data loss
- Payment
- State corruption


Medium Risk:

- Validation
- Workflow


Low Risk:

- UI display
- Non-critical behavior


Format:


| Rule | Risk | Reason |
|-|-|-|


---

# Step 7: Generate Initial Test Cases


Create one Test Case for every Decision Table Rule.


Do NOT optimize yet.


Each Test Case contains:


- Rule ID
- Conditions
- Expected Result


---

# Step 8: Pair-wise Factor Analysis


Extract factors from Conditions.


Example:


| Factor | Values |
|-|-|
| Role | Admin/User |
| Status | Active/Locked |
| Action | Delete/Edit/View |


Calculate:


Full combination:


Example:

2 × 2 × 3 = 12 combinations


---

# Step 9: Apply Pair-wise Testing


Reduce Test Cases using Pair-wise Testing.


Maintain:


- Every pair of factor values appears at least once
- High-risk Rules remain covered
- Invalid combinations remain covered
- Boundary states remain covered


Always keep:


- Security combinations
- Permission violations
- Invalid inputs
- Exception flows
- Critical state transitions


Remove:


- Duplicate combinations
- Repeated low-risk scenarios


Generate:


# Pair-wise Coverage Table


Format:


| Test Case | Factor 1 | Factor 2 | Factor 3 | Covered Pair |
|-|-|-|-|-|


Explain:


- Original combination count
- Reduced test case count
- Reduction percentage
- Coverage achieved


---

# Step 10: Generate Final Test Cases After Reduction

The ONLY allowed test case format:


/docs/test-case-template.md


After Pair-wise reduction:


Generate final Test Cases ONLY from:

- Selected Pair-wise combinations
- Covered Decision Rules
- High-risk scenarios


Each final Test Case MUST maintain traceability:


Requirement
→ Decision Rule
→ Pair-wise Combination
→ Test Case


Do NOT generate removed redundant cases.


Each Test Case must include:


- Decision Rule ID
- Pair-wise Coverage ID
- Conditions
- Expected Result
- Risk Level


---

# Step 11: Generate Analysis Report


Create:


```

docs/decision-table-pairwise-analysis.md

```


Must include:


# Requirement Summary


# Condition Identification


# Result / Action Identification


# Decision Table


# Rule Analysis


# Risk Analysis


# Pair-wise Factor Analysis


# Full Combination Calculation


# Reduction Process


# Final Test Case Mapping


# Coverage Summary


---

# Step 12: AI Audit Logging


Append:


```

docs/ai-audit-report.md

```


Include:


- AI tool name
- Timestamp
- Prompt used
- Task performed
- Output summary


Timestamp format:


MM/DD/YYYY hh:mm AM/PM


---

# Quality Rules


The agent MUST:


- Prioritize risk-based testing
- Not invent requirements
- Clearly separate Condition and Result
- Keep traceability between:
  Requirement → Rule → Test Case
- Explain reduction logic
- Preserve high-risk coverage


---

# Final Response


Respond Vietnamese.


Include:


## File đã tạo


List generated files.


Example:


- tests/test-cases/user-management/TC-USER-001.md
- docs/decision-table-pairwise-analysis.md
- docs/ai-audit-report.md


---


## Tổng kết kiểm thử


Include:


- Feature tested
- Number of Decision Rules
- Number of Conditions
- Number of Results
- Original combinations
- Reduced Test Cases
- Techniques applied
- Coverage achieved
