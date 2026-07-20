# Báo Cáo Tổng Hợp Kết Quả Kiểm Thử Nhóm (EShop SUT Summary Report)

Báo cáo này tổng hợp kết quả thiết kế kịch bản, độ bao phủ kịch bản, trạng thái thực thi và danh mục lỗi phát hiện được (Defects/Bugs) của nhóm trên hệ thống **EShop SUT**, bao gồm phần làm của các thành viên: **Đặng Đăng Khoa**, **Đặng Trường Nguyên**, **Phan Quốc Thịnh**, **Võ Ngọc Bích Trâm**, và **Nguyễn Thanh Gia Bảo**.

---

## 1. BẢNG TỔNG HỢP TOÀN NHÓM (GROUP SUMMARY)

| Thành viên | Feature đã test | Tổng số TC | Executed | Passed | Failed | Bug Artifacts |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Đặng Đăng Khoa** | FR02, FR07, FR13, FR21 | 293 | 293 | 190 | 103 | 55 |
| **Đặng Trường Nguyên** | FR04, FR09, FR10, FR18, FR20 | 150 | 150 | 118 | 32 | 20 |
| **Phan Quốc Thịnh** | FR01, FR08, FR09, FR16, FR26 | 145 | 145 | 31 | 114 | 75 |
| **Võ Ngọc Bích Trâm** | FR03, FR07, FR08, FR12, FR15, FR22 | 227 | 188 | 30 | 158 | 36 |
| **Nguyễn Thanh Gia Bảo** | FR03, FR05, FR10, FR11, FR19, FR20 | 118 | 118 | 73 | 45 | 26 |
| **TỔNG CỘNG NHÓM** | **9 Features** | **933** | **894** | **442** | **452** | **212** |

---

## 2. PHẦN CỦA ĐẶNG ĐĂNG KHOA

### 2.1. Tổng Hợp Số Lượng & Độ Bao Phủ Kịch Bản (Test Cases & Coverage)

Tổng cộng có **293** kịch bản kiểm thử đã được thiết kế và thực thi trên 4 chức năng chính (FR) của hệ thống.

#### Thống kê theo kỹ thuật thiết kế & Feature Requirement (Traceability Matrix)

| Kỹ thuật kiểm thử (Test Design Technique) | Thư mục bài làm (Directory) | Feature Requirement | Số lượng Test Cases |
| :--- | :--- | :--- | :---: |
| **Phân vùng tương đương (EP)** &<br>**Phân tích giá trị biên (BVA)** | `assignment/BVA&EP/` | FR02 – Đăng nhập & Khóa tài khoản <br> FR07 – Giỏ hàng <br> FR13 – Dashboard Admin <br> FR21 – Giỏ hàng & Checkout di động | **259** <br>*(80)*<br>*(90)*<br>*(46)*<br>*(43)* |
| **Bảng quyết định (DT)** &<br>**Kiểm thử cặp (Pairwise - PT)** | `assignment/decision-table/` | FR02 – Đăng nhập & Khóa tài khoản | **18** |
| **Chuyển trạng thái (ST)** | `assignment/state-transtition-test/`| FR02 – Đăng nhập & Khóa tài khoản | **9** |
| **Ca sử dụng (Use Case - UC)** | `assignment/use-case-tes/` | FR02 – Đăng nhập & Khóa tài khoản | **7** |
| **TỔNG CỘNG (GRAND TOTAL)** | | | **293** |

#### Trạng Thái Thực Thi Kịch Bản (Execution Status)

| Bài tập / Kỹ thuật kiểm thử | Tổng số TC | Passed | Failed | Tỉ lệ Passed (Pass Rate) |
| :--- | :---: | :---: | :---: | :---: |
| **EP & BVA** | 259 | 168 | 91 | 64.86% |
| **DT & Pairwise (PT)** | 18 | 12 | 6 | 66.67% |
| **State Transition (ST)** | 9 | 5 | 4 | 55.56% |
| **Use Case (UC)** | 7 | 5 | 2 | 71.43% |
| **TỔNG CỘNG** | **293** | **190** | **103** | **64.84%** |

---

### 2.2. Danh Mục Lỗi Phát Hiện & Độ Bao Phủ Lỗi (Bugs Found & Coverage)

Tổng số lỗi duy nhất phát hiện được trong quá trình kiểm thử là **55 lỗi**.

#### Phân bổ lỗi theo Feature Requirement (Bug Coverage by FR)

* **FR02 – Đăng nhập & Khóa tài khoản**: **25 lỗi**
  * *EP & BVA*: 19 lỗi (`BUG-FR02-A-01` đến `BUG-FR02-A-19`)
  * *DT & PT*: 1 lỗi (`BUG-FR02-001`)
  * *ST*: 3 lỗi (`BUG-FR02-ST-01` đến `BUG-FR02-ST-03`)
  * *UC*: 2 lỗi (`BUG-FR02-UC-01` đến `BUG-FR02-UC-02`)
* **FR07 – Giỏ hàng**: **19 lỗi** (`BUG-FR07-B-01` đến `BUG-FR07-B-19`)
* **FR13 – Dashboard Admin**: **5 lỗi** (`BUG-FR13-C-01` đến `BUG-FR13-C-05`)
* **FR21 – Giỏ hàng & Checkout di động**: **6 lỗi** (`BUG-FR21-D-01` đến `BUG-FR21-D-06`)

#### Phân bổ lỗi theo mức độ nghiêm trọng (Bug Coverage by Severity)

| Độ nghiêm trọng (Severity) | Số lượng lỗi | Mã Lỗi (Bug IDs) |
| :--- | :---: | :--- |
| **Critical** <br>*(Nguy cấp, bảo mật)* | **6** | `BUG-FR02-A-07`, `BUG-FR02-A-13`<br>`BUG-FR07-B-13` (Price Tampering)<br>`BUG-FR13-C-02` (Bỏ sót role check admin)<br>`BUG-FR21-D-04`, `BUG-FR21-D-06` |
| **Major** <br>*(Lỗi chức năng nghiêm trọng)* | **29** | - *FR02 (Auth)*: `BUG-FR02-A-01`, `BUG-FR02-A-03`, `BUG-FR02-A-10`, `BUG-FR02-A-15`, `BUG-FR02-A-16`, `BUG-FR02-A-17`, `BUG-FR02-A-18`, `BUG-FR02-A-19`, `BUG-FR02-001`, `BUG-FR02-ST-01`, `BUG-FR02-ST-03`, `BUG-FR02-UC-01`<br>- *FR07 (Cart)*: `BUG-FR07-B-01` đến `BUG-FR07-B-04`, `BUG-FR07-B-09`, `BUG-FR07-B-10`, `BUG-FR07-B-12`, `BUG-FR07-B-14` đến `BUG-FR07-B-19`<br>- *FR13*: `BUG-FR13-C-01`<br>- *FR21*: `BUG-FR21-D-01`, `BUG-FR21-D-02`, `BUG-FR21-D-05` |
| **Medium** <br>*(Lỗi logic)* | **8** | - *FR02 (Auth)*: `BUG-FR02-A-02`, `BUG-FR02-A-09`, `BUG-FR02-A-14`, `BUG-FR02-ST-02`, `BUG-FR02-UC-02`<br>- *FR13*: `BUG-FR13-C-03`, `BUG-FR13-C-04`<br>- *FR21*: `BUG-FR21-D-03` |
| **Minor / Cosmetic** <br>*(Lỗi giao diện, nhãn hiển thị)* | **12** | - *FR02 (Auth)*: `BUG-FR02-A-04`, `BUG-FR02-A-05`, `BUG-FR02-A-06`, `BUG-FR02-A-08`, `BUG-FR02-A-11`, `BUG-FR02-A-12`<br>- *FR07 (Cart)*: `BUG-FR07-B-05` đến `BUG-FR07-B-08`, `BUG-FR07-B-11`<br>- *FR13*: `BUG-FR13-C-05` |

---

## 3. PHẦN CỦA ĐẶNG TRƯỜNG NGUYÊN

### 3.1. Ghi chú phạm vi

- Repo hiện có 4 nhóm artifact chính: `domain_bva_testing`, `decision_table_testing`, `state-transition-testing`, `use-case-testing`.
- `EP` được hiểu là Equivalence Partitioning trong nhóm `domain_bva_testing`.
- `BVA` được hiểu là Boundary Value Analysis trong nhóm `domain_bva_testing`.
- `PT` được hiểu là Pairwise Testing. Repo không có folder PT độc lập; PT đang là subset của các testcase `Decision Table / Pairwise` trong `decision_table_testing`.
- Khi tính tổng testcase unique theo artifact folder, không cộng thêm PT một lần nữa vì PT đã nằm trong DT.

### 3.2. Tổng quan theo nhóm bài tập

| Nhóm bài tập | Artifact source | Feature Requirement coverage | Test design technique coverage | Total TC | Passed | Failed | Bug reports |
| :--- | :--- | :--- | :--- | ---: | ---: | ---: | ---: |
| EP/BVA | `tests/domain_bva_testing/` | FR-04, FR-10, FR-18, FR-20 | EP: 69 TC; BVA: 31 TC | 100 | 79 | 21 | 10 |
| DT/PT | `tests/decision_table_testing/` | FR-09 | DT: 10 TC; PT subset: 4 TC | 10 | 6 | 4 | 3 |
| ST | `tests/state-transition-testing/FR-10/` | FR-10 | State Transition Testing: 20 TC | 20 | 18 | 2 | 2 |
| UC | `tests/use-case-testing/FR-10/` | FR-10 | Use Case Testing: 20 TC | 20 | 15 | 5 | 5 |
| **Tổng unique theo artifact folder** |  | FR-04, FR-09, FR-10, FR-18, FR-20 | EP, BVA, DT, ST, UC; PT là subset của DT | **150** | **118** | **32** | **20** |

*Ghi chú: nếu đếm PT như một dòng technique riêng thì có thêm 4 testcase PT, nhưng 4 testcase này đã nằm trong 10 testcase DT của FR-09.*

### 3.3. Coverage testcase theo feature requirement và technique

| Technique | Feature Requirement coverage | Total TC | Passed | Failed | Ghi chú |
| :--- | :--- | ---: | ---: | ---: | :--- |
| Equivalence Partitioning (EP) | FR-04: 14; FR-10: 20; FR-18: 24; FR-20: 11 | 69 | 54 | 15 | Domain/EP testcase trong `domain_bva_testing`. |
| Boundary Value Analysis (BVA) | FR-04: 18; FR-10: 3; FR-18: 3; FR-20: 7 | 31 | 25 | 6 | Boundary testcase trong `domain_bva_testing`. |
| Decision Table Testing (DT) | FR-09: 10 | 10 | 6 | 4 | Bao gồm 4 testcase có tag Pairwise. |
| Pairwise Testing (PT) | FR-09: 4 | 4 | 1 | 3 | Subset của DT: `FR09-F-TC01`, `FR09-P-TC01`, `FR09-T-TC01`, `FR09-T-TC03`. |
| State Transition Testing (ST) | FR-10: 20 | 20 | 18 | 2 | Artifact riêng trong `state-transition-testing`. |
| Use Case Testing (UC) | FR-10: 20 | 20 | 15 | 5 | Artifact riêng trong `use-case-testing`. |

### 3.4. Coverage testcase theo FR

| Nhóm bài tập | FR | Technique coverage | Total TC | Passed | Failed |
| :--- | :--- | :--- | ---: | ---: | ---: |
| EP/BVA | FR-04 | EP: 14; BVA: 18 | 32 | 20 | 12 |
| EP/BVA | FR-10 | EP: 20; BVA: 3 | 23 | 21 | 2 |
| EP/BVA | FR-18 | EP: 24; BVA: 3 | 27 | 21 | 6 |
| EP/BVA | FR-20 | EP: 11; BVA: 7 | 18 | 17 | 1 |
| DT/PT | FR-09 | DT: 10; PT subset: 4 | 10 | 6 | 4 |
| ST | FR-10 | ST: 20 | 20 | 18 | 2 |
| UC | FR-10 | UC: 20 | 20 | 15 | 5 |

### 3.5. Status testcase

| Scope | Total TC | Passed | Failed | Pass rate | Fail rate |
| :--- | ---: | ---: | ---: | ---: | ---: |
| EP/BVA | 100 | 79 | 21 | 79.00% | 21.00% |
| DT/PT | 10 | 6 | 4 | 60.00% | 40.00% |
| PT subset trong DT | 4 | 1 | 3 | 25.00% | 75.00% |
| ST | 20 | 18 | 2 | 90.00% | 10.00% |
| UC | 20 | 15 | 5 | 75.00% | 25.00% |
| **Tổng unique theo artifact folder** | **150** | **118** | **32** | **78.67%** | **21.33%** |

### 3.6. Tổng quan bug

| Scope | Bug reports | Severity coverage | Ghi chú |
| :--- | ---: | :--- | :--- |
| EP/BVA | 10 | Critical: 3; Major: 6; Minor: 1 | Bug được gom theo root cause từ 21 failed TC. |
| DT/PT | 3 | High: 3 | Bug được gom theo root cause từ 4 failed TC. |
| PT subset trong DT | 2 | High: 2 | `BUG-FR09-P-01`, `BUG-FR09-T-01`; đây là subset của 3 bug DT. |
| ST | 2 | Major: 2 | 2 failed TC, mỗi failed TC map 1 bug. |
| UC | 5 | Major: 5 | 5 failed TC, mỗi failed TC map 1 bug. |
| **Tổng theo artifact folder** | **20** | Critical: 3; High: 3; Major: 13; Minor: 1 | Đếm theo bug report file trong từng nhóm artifact. |

*Ghi chú: nếu deduplicate theo Bug ID trên toàn repo thì còn 18 Bug ID unique, vì `BUG-FR10-S-01` và `BUG-FR10-S-02` xuất hiện ở cả nhóm EP/BVA và ST.*

### 3.7. Coverage bug theo feature requirement và severity

| Nhóm bài tập | Primary FR | Bug reports | Severity coverage | Bug IDs | Related FR ghi trong bug report |
| :--- | :--- | ---: | :--- | :--- | :--- |
| EP/BVA | FR-04 | 4 | Critical: 1; Major: 2; Minor: 1 | `BUG-FR04-A-01`, `BUG-FR04-N-01`, `BUG-FR04-P-01`, `BUG-FR04-R-01` | FR-04 |
| EP/BVA | FR-10 | 2 | Major: 2 | `BUG-FR10-S-01`, `BUG-FR10-S-02` | FR-10 |
| EP/BVA | FR-18 | 3 | Critical: 1; Major: 2 | `BUG-FR18-A-01`, `BUG-FR18-S-01`, `BUG-FR18-X-01` | FR-18; một số bug liên quan rule state machine FR-10 |
| EP/BVA | FR-20 | 1 | Critical: 1 | `BUG-FR20-X-01` | FR-20; bug report có nhắc FR-05 do FR-20 kế thừa hành vi product search |
| DT/PT | FR-09 | 3 | High: 3 | `BUG-FR09-A-01`, `BUG-FR09-P-01`, `BUG-FR09-T-01` | FR-09 |
| PT subset trong DT | FR-09 | 2 | High: 2 | `BUG-FR09-P-01`, `BUG-FR09-T-01` | FR-09 |
| ST | FR-10 | 2 | Major: 2 | `BUG-FR10-S-01`, `BUG-FR10-S-02` | FR-10 |
| UC | FR-10 | 5 | Major: 5 | `BUG-FR10-UC01-TC05`, `BUG-FR10-UC01-TC06`, `BUG-FR10-UC01-TC07`, `BUG-FR10-UC02-TC04`, `BUG-FR10-UC02-TC08` | FR-10 |

### 3.8. Nguồn dữ liệu đã dùng

| Loại dữ liệu | Path |
| :--- | :--- |
| EP/BVA testcase | `tests/domain_bva_testing/test-cases/` |
| EP/BVA test run | `tests/domain_bva_testing/test-runs/` |
| EP/BVA bug reports | `tests/domain_bva_testing/bug/` |
| DT/PT testcase | `tests/decision_table_testing/test-cases/` |
| DT/PT summary | `tests/decision_table_testing/test-summary/fr09-coupon_application-decision-table-summary.md` |
| DT/PT bug reports | `tests/decision_table_testing/bug/FR-09/` |
| ST testcase and summary | `tests/state-transition-testing/FR-10/` |
| UC testcase and summary | `tests/use-case-testing/FR-10/` |

---

## 4. PHẦN CỦA PHAN QUỐC THỊNH (MSSV: 23127486)

### 4.1. Tổng quan

> [!NOTE]
> Báo cáo này tổng hợp số liệu thống kê về Test Cases và Lỗi (Bugs) phát hiện được trên EShop SUT cho toàn bộ các tính năng đã kiểm thử (FR-01, FR-08, FR-09, FR-16, FR-26).

### 4.2. TỔNG HỢP TEST CASES

* **Tổng số Test Cases đã thiết kế & thực thi:** **145**
  * **Đạt (Passed):** 31 (21.4%)
  * **Lỗi (Failed):** 114 (78.6%)

#### A. Độ bao phủ Test Cases theo Tính năng (Feature Requirement Coverage)

| Tính năng (Requirement) | Số lượng Test Cases | Đạt (Passed) | Lỗi (Failed) | Tỷ lệ Đạt | Trạng thái kiểm thử |
| :--- | :---: | :---: | :---: | :---: | :--- |
| FR-01: Đăng ký tài khoản (Account registration) | 42 | 3 | 39 | 7.1% | Hoàn thành |
| FR-08: Thanh toán (Checkout) | 24 | 9 | 15 | 37.5% | Hoàn thành |
| FR-09: Mã giảm giá (Discount coupons) | 27 | 13 | 14 | 48.1% | Hoàn thành |
| FR-16: Import sản phẩm từ CSV | 33 | 5 | 28 | 15.2% | Hoàn thành |
| FR-26: Quản lý hồ sơ cá nhân | 19 | 1 | 18 | 5.3% | Hoàn thành |

#### B. Độ bao phủ Test Cases theo Kỹ thuật Thiết kế (Test Design Technique Coverage)

| Phương pháp/Kỹ thuật kiểm thử | Số lượng Test Cases | Các Requirement áp dụng | Ghi chú |
| :--- | :---: | :--- | :--- |
| Domain Testing (Phân vùng tương đương & Phân tích giá trị biên) | 121 | FR-01, FR-09, FR-16, FR-26 | Kiểm thử hộp đen |
| End-to-End Testing (Kiểm thử tích hợp toàn trình) | 2 | FR-08 | Kiểm thử hộp đen |
| State Transition Testing (Kiểm thử chuyển trạng thái) | 15 | FR-08 | Kiểm thử hộp đen |
| Use Case Testing (Kiểm thử ca sử dụng) | 7 | FR-08 | Kiểm thử hộp đen |

---

### 4.3. TỔNG HỢP BÁO CÁO LỖI (BUG REPORTS)

* **Tổng số lỗi phát hiện được:** **75 lỗi**

#### A. Phân bố lỗi theo Tính năng (Feature Requirement Bug Coverage)

| Tính năng (Requirement) | Số lượng Lỗi (Bugs) | Mã lỗi tương ứng | Tỷ lệ phân bố |
| :--- | :---: | :--- | :---: |
| FR-01: Đăng ký tài khoản (Account registration) | 16 | BUG-REG-001 đến BUG-REG-016 | 21.3% |
| FR-08: Thanh toán (Checkout) | 9 | BUG-CHECKOUT-001 đến BUG-CHECKOUT-009 | 12.0% |
| FR-09: Mã giảm giá (Discount coupons) | 9 | BUG-COUPON-001 đến BUG-COUPON-009 | 12.0% |
| FR-16: Import sản phẩm từ CSV | 23 | BUG-IMPORT-001 đến BUG-IMPORT-023 | 30.7% |
| FR-26: Quản lý hồ sơ cá nhân | 18 | BUG-PROFILE-001 đến BUG-PROFILE-018 | 24.0% |

#### B. Phân bố lỗi theo Mức độ Nghiêm trọng (Severity Bug Coverage)

| Mức độ nghiêm trọng (Severity) | Số lượng Lỗi (Bugs) | Tỷ lệ phân bố | Ghi chú |
| :--- | :---: | :---: | :--- |
| Critical | 21 | 28.0% | Yêu cầu xử lý theo độ ưu tiên |
| High | 3 | 4.0% | Yêu cầu xử lý theo độ ưu tiên |
| Major | 27 | 36.0% | Yêu cầu xử lý theo độ ưu tiên |
| Medium | 15 | 20.0% | Yêu cầu xử lý theo độ ưu tiên |
| Low | 4 | 5.3% | Yêu cầu xử lý theo độ ưu tiên |

---

## 5. PHẦN CỦA VÕ NGỌC BÍCH TRÂM (MSSV: 23127271)

### 5.1. Tổng quan

Báo cáo tổng hợp **6 kỹ thuật thiết kế test** trên các bài tập / module trong khóa:

| Ký hiệu | Kỹ thuật | Nguồn artifact |
|:--:|---|---|
| **EP** | Equivalence Partitioning (Domain Testing) | `HW2/` · `Repo/eshop-sut/tests/test-cases/` |
| **BVA** | Boundary Value Analysis | `HW2/` · `Repo/eshop-sut/tests/test-cases/` |
| **DT** | Decision Table Testing | `DTT/Test Case/FR-12-DTT-test-cases.md` |
| **PT** | Pairwise Testing | `DTT/Test Case/FR-12-Pairwise-test-cases.md` |
| **ST** | State Transition Testing | `Assigment/State Transition/` |
| **UC** | Use-Case Testing | `Assigment/Use Case/` |

> Ghi chú: EP và BVA thuộc **HW02 (Domain Testing)**; DT và PT cùng feature **FR-12**; ST và UC cùng feature **FR-07**.

---

### 5.2. Số lượng test case theo kỹ thuật

#### A. Bảng tổng hợp

| Kỹ thuật | Feature (FR) | TC thiết kế | TC bổ sung (GAP) | **Tổng TC** | Đã thực thi | Pass | Fail | Chưa chạy |
|:--:|---|---:|---:|---:|---:|---:|---:|---:|
| **EP** | FR-03, FR-08, FR-15, FR-03/22 (Mobile) | 75 | — | **75** | —† | —† | —† | —† |
| **BVA** | FR-03, FR-08, FR-15, FR-03/22 (Mobile) | 81 | — | **81** | —† | —† | —† | —† |
| **EP + BVA (gộp)** | FR-03, FR-08, FR-15, Mobile | 156 | 28 | **184** | **145** | **24** | **121** | **39** |
| **DT** | FR-12 | 8 | — | **8** | 8 | 2 | 6 | 0 |
| **PT** | FR-12 | 8 | — | **8** | 8 | 1 | 7 | 0 |
| **ST** | FR-07 | 17‡ | — | **17** | 17 | 3 | 14 | 0 |
| **UC** | FR-07 | 10 | — | **10** | 10 | 0 | 10 | 0 |
| **TỔNG CỘNG** | | **199** | **28** | **227** | **188** | **30** | **158** | **44** |

† HW02 chỉ ghi log thực thi **gộp EP+BVA** (không tách pass/fail riêng từng kỹ thuật).  
‡ Thiết kế manual ghi 16 TC; automation có thêm TC phủ `T-INV-03` → 17 test Playwright.

#### B. Chi tiết EP / BVA theo feature (HW02)

| Feature | EP | BVA | GAP | Tổng module | FR |
|---:|---:|---:|---:|---:|---|
| Quên mật khẩu (Web) | 20 | 24 | 4 | 48 | FR-03 |
| Thanh toán (Checkout) | 24 | 20 | 6 | 50 | FR-08 |
| Quản lý sản phẩm (Admin) | 11 | 13 | 11 | 35 | FR-15 |
| Quên mật khẩu (Mobile) | 20 | 24 | 7 | 51 | FR-03 + FR-22 |
| **Cộng** | **75** | **81** | **28** | **184** | |

---

### 5.3. Coverage test case

#### A. Coverage theo Feature Requirement

| FR | Mô tả ngắn | Kỹ thuật áp dụng | Số TC |
|---|---|---|---:|
| **FR-03** | Quên mật khẩu & đặt lại (Web + Mobile) | EP, BVA, GAP | 99 |
| **FR-07** | Giỏ hàng | ST, UC | 27 |
| **FR-08** | Thanh toán | EP, BVA, GAP | 50 |
| **FR-12** | Phân quyền truy cập API (JWT + admin) | DT, PT | 16 |
| **FR-15** | Quản lý sản phẩm (Admin CRUD) | EP, BVA, GAP | 35 |
| **FR-22** | Quên mật khẩu Mobile (UI/UX) | EP, BVA, GAP (kèm FR-03) | (trong Mobile) |

#### B. Coverage theo kỹ thuật thiết kế

| Kỹ thuật | Đối tượng kiểm thử chính | Tiêu chí coverage |
|---|---|---|
| **EP** | Phân vùng hợp lệ / không hợp lệ từng input (email, OTP, mật khẩu, giá, số lượng…) | Mỗi partition đại diện ≥ 1 TC; on-point valid + invalid classes |
| **BVA** | Biên min, max, min−1, max+1, độ dài, giá trị số | 2–3 giá trị biên / boundary / field |
| **DT** | Quy tắc authorize API (C1–C5 → A1/A2/A3) | 5 rule R1–R5 trong decision table; 8 TC |
| **PT** | Tổ hợp tham số P1–P5 (endpoint, header, token, role) | 8 cặp pairwise + ràng buộc logic |
| **ST** | Trạng thái `EMPTY`, `HAS_ITEMS`, `DELETE_CONFIRM` | 10 transition hợp lệ + 3 invalid; 2 E2E path; final-state |
| **UC** | Luồng MF, AF-01…06, EF-01…03 | Main flow + alternate + exception paths |

#### C. Ma trận FR × Kỹ thuật

| FR | EP | BVA | DT | PT | ST | UC |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| FR-03 / FR-22 | ✓ | ✓ | | | | |
| FR-07 | | | | | ✓ | ✓ |
| FR-08 | ✓ | ✓ | | | | |
| FR-12 | | | ✓ | ✓ | | |
| FR-15 | ✓ | ✓ | | | | |

---

### 5.4. Kết quả thực thi (Pass / Fail)

#### A. Tóm tắt theo kỹ thuật

| Kỹ thuật | Pass | Fail | Tỷ lệ pass |
|:--:|---:|---:|---:|
| EP + BVA (HW02, gộp) | 24 | 121 | 16,6% |
| DT | 2 | 6 | 25% |
| PT | 1 | 7 | 12,5% |
| ST | 3 | 14 | 17,6% |
| UC | 0 | 10 | 0% |
| **Tổng (có log thực thi)** | **30** | **158** | **16,0%** |

#### B. TC Pass theo ST / UC (FR-07)

**ST — Passed (3):**

- `TC-CART-ST-012` — T-10: Tiếp tục mua sắm, giỏ hàng giữ nguyên
- `TC-CART-ST-INV-01` — Không xóa được khi `EMPTY`
- `TC-CART-ST-INV-02` — Không có +/- khi `EMPTY`

**UC — Passed:** 0 / 10

**DT — Passed (ước lượng):** `TC-FR12-DTT-01`, `PW-08` (admin hợp lệ được phép)

**PT — Passed (ước lượng):** `PW-01` (admin_api + token hợp lệ)

#### C. Lệnh thực thi automation

```bash
# FR-12 (DT + PT)
cd Repo/eshop-sut && npm run test:fr12

# FR-07 State Transition
cd Repo/eshop-sut && $env:SKIP_MOBILE_SERVER=1; npm run test:fr07-st

# FR-07 Use Case
cd Repo/eshop-sut && $env:SKIP_MOBILE_SERVER=1; npm run test:fr07

# HW02 EP/BVA — xem test-runs trong Repo/eshop-sut/tests/test-runs/
```

---

### 5.5. Bug đã phát hiện

#### A. Tổng số bug

| Phạm vi | Số bug (báo cáo) | Ghi chú |
|---|---:|---|
| HW02 (EP/BVA) — GitHub #170–#192 | **23** | 4 feature pools |
| FR-12 (DT + PT) | **5** | Cùng root cause, 2 kỹ thuật xác nhận |
| FR-07 (UC + ST) | **8** | 5 bug lõi trùng nhau giữa UC/ST |
| **Tổng unique (không trùng FR)** | **36** | 23 + 5 + 8 |

> UC và ST cùng feature FR-07: báo cáo riêng ghi 8 (UC) và 6 (ST) nhưng **8 defect implementation** là unique; ST-06 là subset của ST-04.

#### B. Bug theo kỹ thuật phát hiện

| Kỹ thuật | Số bug trong báo cáo | Link chi tiết |
|:--:|---:|---|
| EP / BVA | 23 | `HW2/bug-reports/README.md` |
| DT | 5 | `DTT/FR-12-bug-report.md` |
| PT | 5 | (cùng FR-12) |
| ST | 6 | `Assigment/State Transition/FR-07-bug-report.md` |
| UC | 8 | `Assigment/Use Case/FR-07-bug-report.md` |

#### C. Coverage bug — Feature Requirement

| FR | Số bug | Mức độ nghiêm trọng nổi bật |
|---|---:|---|
| **FR-03** (Web) | 7 | High — OTP 4 số, thiếu confirm password, regex mật khẩu |
| **FR-08** | 4 | Critical/High — sửa total_amount, checkout giỏ trống |
| **FR-15** | 5 | Critical — không auth API, thiếu UI admin |
| **FR-03/22** (Mobile) | 7 | High — tương tự web + UX mobile |
| **FR-12** | 5 | **Critical (4)** — API không enforce JWT/admin |
| **FR-07** | 8 | High (4), Medium (3), Low (2) — dialog xóa, +/-, merge, nhãn |

#### D. Coverage bug — Severity

| Severity | Số lượng (unique) | Ví dụ |
|---:|---:|---|
| **Critical** | 8 | FR-12: unauthenticated POST `/api/products`; FR-08: client `total_amount`; FR-15: no auth |
| **High** | 14 | FR-07: no delete dialog, no +/-; FR-03: OTP 4 digits; merge cart |
| **Medium** | 10 | FR-07: wrong label `Tổng tạm tính`, empty illustration; JWT 401 vs 403 |
| **Low** | 4 | FR-07: cột `Giá` vs `Đơn giá`, link `Mua tiếp` |
| **Investigate** | 1 | FR-07: cart persistence (UC-003) |

#### E. Ma trận bug × FR (rút gọn)

| Bug ID (nhóm) | FR | Severity | Kỹ thuật phát hiện |
|---|---|:---:|---|
| #170–#176, #186–#192 | FR-03, FR-22 | High | EP, BVA |
| #177–#180 | FR-08 | Critical–High | EP, BVA |
| #181–#185 | FR-15 | Critical–Medium | EP, BVA |
| BUG-FR12-01 … 05 | FR-12 | Critical (4), Medium (1) | DT, PT |
| BUG-FR07-01 … 08 | FR-07 | High–Low | UC, ST |

---

### 5.6. Nhận xét tổng hợp

1. **Phạm vi TC:** Đã thiết kế **227** test case (199 theo 6 kỹ thuật + 28 GAP); đã thực thi có log **188** TC automation/manual.
2. **Tỷ lệ pass thấp (16%)** phản ánh đúng chất lượng SUT seed — nhiều requirement chưa implement (FR-07 cart UI, FR-12 authorization).
3. **FR-07:** UC (0%) và ST (17,6%) cùng xác nhận thiếu state `DELETE_CONFIRM`, +/- quantity, merge line item.
4. **FR-12:** DT và PT cho kết quả tương đồng — **5 defect bảo mật** trên cùng decision point authorize.
5. **HW02:** 23 bug trên 4 pool; FR-15 chưa chạy đủ do blocker login (#184).

---

### 5.7. Tham chiếu artifact

| Nội dung | Đường dẫn |
|---|---|
| HW02 tổng hợp | `HW2/README.md`, `HW2/hw2.md` |
| FR-12 DT/PT | `DTT/FR-12-bug-report.md` |
| FR-07 ST | `Assigment/State Transition/FR-07-test-run.md`, `FR-07-bug-report.md` |
| FR-07 UC | `Assigment/Use Case/FR-07-test-run.md`, `FR-07-bug-report.md` |
| Automation SUT | `Repo/eshop-sut/tests/e2e/` |
| Test runs HW02 | `Repo/eshop-sut/tests/test-runs/sprint-3-test-run.md`, `sprint-checkout-test-run.md` |

---

## 6. PHẦN CỦA NGUYỄN THANH GIA BẢO (MSSV: 23127158)

## 6.1. Thống kê Test Cases & Trạng thái Thực thi

Dưới đây là bảng tổng hợp số lượng test case và kết quả thực thi chia theo từng nhóm bài tập (Kỹ thuật kiểm thử):

| Bài tập / Kỹ thuật | Chức năng kiểm thử | Requirement | Số Test Case | PASSED | FAILED | Tỷ lệ PASS |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **EP & BVA** (Domain Testing) | - Xem danh sách & Tìm kiếm sản phẩm<br>- Xem lịch sử đơn hàng<br>- Quản lý người dùng (Admin)<br>- Hủy đơn hàng trên Mobile | FR-05<br>FR-11<br>FR-19<br>FR-10, FR-20 | **72** | **51** | **21** | 70.8% |
| **DT & PT** (Decision Table & Pair-wise) | - Quản lý trạng thái đơn hàng (API) | FR-10 | **19** | **15** | **4** | 78.9% |
| **ST** (State Transition Testing) | - Quản lý Quên mật khẩu & Đặt lại mật khẩu (2 bước) | FR-03 | **20** | **5** | **15** | 25.0% |
| **UC** (Use Case Testing) | - Luồng Quên mật khẩu & Đặt lại mật khẩu (2 bước) | FR-03 | **7** | **2** | **5** | 28.6% |
| **TỔNG CỘNG** | | | **118** | **73** | **45** | **61.9%** |

### Chi tiết phân rã nhóm EP & BVA (Domain Testing):
- **Xem danh sách & Tìm kiếm sản phẩm (FR-05):** 14 Test Cases (6 PASSED, 8 FAILED)
- **Xem lịch sử đơn hàng (FR-11):** 14 Test Cases (12 PASSED, 2 FAILED)
- **Quản lý người dùng (FR-19):** 22 Test Cases (13 PASSED, 9 FAILED)
- **Trạng thái đơn hàng trên Mobile (FR-10, FR-20):** 22 Test Cases (20 PASSED, 2 FAILED)

---

## 6.2. Độ phủ Kiểm thử của Test Cases (Test Case Coverage)

### Theo Kỹ thuật Kiểm thử (Test Design Technique):
- **Equivalence Partitioning (EP) & Boundary Value Analysis (BVA):** Phủ 100% các phân vùng tương đương hợp lệ/không hợp lệ và các điểm biên của tham số đầu vào cũng như biên trạng thái (trạng thái hủy đơn trên Mobile).
- **Decision Table Testing (DT):** Bao phủ toàn bộ 28 luật kết hợp điều kiện chuyển đổi trạng thái đơn hàng.
- **Pair-wise Testing (PT):** Áp dụng thuật toán giảm số lượng test case từ 28 luật xuống 19 test case nhưng vẫn đảm bảo bao phủ mọi cặp yếu tố (Current State, Target State, Role).
- **State Transition Testing (ST):** Đạt độ phủ 100% cho:
  - State Coverage (4/4 states)
  - Transition Coverage (9/9 transitions gồm 4 valid và 5 invalid)
  - 1-switch Coverage (4 sequences)
  - n-switch Coverage (n=2, 4 sequences)
  - End-to-End Test (2 paths)
  - Final State Test (1 final state)
- **Use Case Testing (UC):** Đạt độ phủ 100% cho Main Flow (luồng chính), Alternative Flow (luồng thay thế) và Exception Flows (luồng ngoại lệ).

### Theo Yêu cầu Chức năng (Feature Requirement):
- **FR-03 (Quên mật khẩu):** Phủ đầy đủ cả 2 bước (Lấy OTP & Đặt lại mật khẩu), bao gồm kiểm tra tính hợp lệ của email, kiểm tra độ mạnh mật khẩu và logic xác thực mã OTP.
- **FR-05 (Tìm kiếm & Sản phẩm):** Phủ hiển thị dạng lưới, định dạng giá, hiển thị hình ảnh, thanh tìm kiếm và xử lý bảo mật (SQLi, XSS).
- **FR-10 (Order State Machine):** Phủ toàn bộ logic chuyển đổi giữa 5 trạng thái đơn hàng và phân quyền tương ứng cho Admin/User.
- **FR-11 (Lịch sử đơn hàng):** Phủ quyền sở hữu đơn hàng của chính mình, hiển thị tiếng Việt, hiển thị màu sắc và tính năng phân trang.
- **FR-19 (Quản lý người dùng):** Phủ phân quyền truy cập API Admin, tính năng xóa người dùng (bao gồm chặn tự xóa chính mình, kiểm tra tham số hợp lệ, kiểm tra ID không tồn tại và xử lý liên kết dữ liệu).
- **FR-20 (Mobile Order):** Phủ các đặc thù UI trên Mobile như hiển thị/ẩn nút Hủy đơn đỏ, hiển thị dialog xác nhận và cập nhật trạng thái ngay trên ứng dụng Mobile.

---

## 6.3. Báo cáo & Phân loại Lỗi (Bug Report & Severity)

Tổng số lỗi được phát hiện và lập báo cáo chi tiết: **26 lỗi (bugs)**.

### Phân phối Lỗi theo Yêu cầu Chức năng (Feature Requirement):
- **FR-05 (Sản phẩm & Tìm kiếm):** 8 bugs
- **FR-11 (Lịch sử đơn hàng):** 2 bugs
- **FR-19 (Quản lý người dùng):** 7 bugs
- **FR-10 & FR-20 (Đơn hàng & Mobile):** 4 bugs
- **FR-03 (Quên mật khẩu):** 5 bugs

### Phân loại Lỗi theo Mức độ Nghiêm trọng (Severity):

#### A. Critical (Nghiêm trọng / Bảo mật / Leo quyền) — 6 Bugs
1. **[Search]** Chức năng tìm kiếm không sanitize input dẫn đến lỗi bảo mật **Cross-Site Scripting (XSS)**.
2. **[Search]** Chức năng tìm kiếm không xử lý ký tự đặc biệt dẫn đến lỗi **SQL Injection**.
3. **[Order History]** API xem chi tiết đơn hàng không yêu cầu token xác thực, cho phép khách vãng lai xem chi tiết đơn hàng của người khác nếu biết ID đơn.
4. **[User Management]** Tài khoản user thường vẫn gọi được API Admin để lấy danh sách toàn bộ người dùng trong hệ thống.
5. **[User Management]** Tài khoản user thường có thể gọi API Admin để xóa tài khoản của người dùng khác (Leo quyền).
6. **[Order State Machine]** API cập nhật trạng thái đơn hàng của Admin không kiểm tra phân quyền role, cho phép user thường tự chuyển trạng thái đơn sang confirmed, shipping, delivered.

#### B. High (Lỗi Logic / Nghiệp vụ / Sai thông số chính) — 7 Bugs
7. **[User Management]** Admin có thể tự xóa chính tài khoản đang đăng nhập của mình, làm mất quyền quản trị.
8. **[User Management]** Xóa người dùng có đơn hàng liên quan nhưng không cascade xóa hoặc xử lý dữ liệu liên kết, dẫn đến các đơn hàng mồ côi (Orphan Data).
9. **[Order State Machine]** Khách hàng có thể tự hủy đơn hàng khi đơn đã chuyển sang trạng thái `shipping` (Đặc tả cấm tự hủy khi đang giao).
10. **[Forgot Password]** Mã OTP sinh ra ở backend chỉ có 4 chữ số thay vì 6 chữ số theo đặc tả.
11. **[Forgot Password]** Backend chấp nhận đặt lại mật khẩu với mật khẩu cực kỳ yếu (ví dụ: `abc`), bỏ qua quy tắc mật khẩu mạnh.
12. **[Forgot Password]** Biểu thức chính quy (Regex) validator độ mạnh mật khẩu ở frontend viết sai, bắt buộc có khoảng trắng và không cho phép ký tự đặc biệt, chặn toàn bộ mật khẩu mạnh tiêu chuẩn như `NewPass123!`.
13. **[Forgot Password]** Giao diện màn hình đặt lại mật khẩu thiếu hoàn toàn trường nhập "Xác nhận mật khẩu mới".

#### C. Medium (Lỗi hiển thị UI/UX / Phân trang / Thiết kế thiếu) — 10 Bugs
14. **[Product]** Giá sản phẩm không hiển thị đúng định dạng tiền tệ Việt Nam (thiếu ký hiệu `₫` và dấu phân cách hàng nghìn).
15. **[Product]** Trang hiển thị màn hình trắng trơn khi đang tải dữ liệu (không có thông báo Loading).
16. **[Product]** Không hiển thị thông báo Empty State phù hợp khi kết quả tìm kiếm không tìm thấy sản phẩm.
17. **[Order History]** API lịch sử đơn hàng bỏ qua tham số phân trang, luôn trả về toàn bộ dữ liệu.
18. **[User Management]** API xóa người dùng trả về `200 OK` (thành công giả) khi `user_id` không tồn tại.
19. **[User Management]** API xóa người dùng trả về `200 OK` khi `user_id` sai định dạng (ví dụ: `"abc"`).
20. **[User Management]** Trang quản lý người dùng của Admin không hỗ trợ phân trang khi số lượng người dùng lớn.
21. **[Mobile Order]** Các trạng thái đơn hàng hiển thị trên ứng dụng Mobile không có màu sắc phân biệt.
22. **[Mobile Order]** Không hiển thị dialog xác nhận trước khi hủy đơn hàng trên ứng dụng Mobile.
23. **[Forgot Password]** Không hiển thị chỉ báo bước ("Bước 1 / 2") và nút "Quay lại đăng nhập" ở màn hình nhập email.

#### D. Low (Lỗi hiển thị nhỏ / Tiêu chuẩn SEO) — 3 Bugs
24. **[Product]** Khi ảnh sản phẩm bị lỗi không tải được, thẻ ảnh không hiển thị văn bản thay thế `alt` mô tả sản phẩm.
25. **[Product]** Trang chủ chứa nhiều hơn một thẻ `<h1>` (Vi phạm quy tắc cấu trúc HTML).
26. **[Search]** Trang kết quả tìm kiếm sản phẩm chứa nhiều hơn một thẻ `<h1>`.
