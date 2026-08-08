# Boundary Value Analysis Report: FR-13 – Dashboard

## 1. Boundary Variables Identification
We focus on numerical, capacity, and delay thresholds:
- **Total Orders Count:** Lower boundary `0`. Upper boundary represents high capacity load (e.g., `100,000` orders).
- **Total Revenue (₫):** Lower boundary `0`. Upper boundary represents massive amount rendering (e.g., `999,999,999,999 ₫` or larger value testing layout).
- **API Response Time (ms):** Timeout limit is configured at `5000ms`.
- **Recent Orders List Count:** Lower boundary `0`. Upper boundary represents maximum display limit configured on UI (e.g., `displayLimit`).
- **Responsive Screen Width Breakpoint:** Tablet breakpoint is `768px`.
- **Other Numeric Cards (Users, Products):** Lower boundary and decimal representation limits.

---

## 2. Boundary Values Definition

### Variable 1: Total Orders Count
- Boundary Point: `Min = 0`
  - **Min - 1 (Invalid):** `-1`
  - **Min (Valid):** `0`
  - **Min + 1 (Valid):** `1`
- Boundary Point: `Max = 100,000`
  - **Max (Valid):** `100,000`

### Variable 2: Total Revenue (₫)
- Boundary Point: `Min = 0`
  - **Min - 1 (Invalid):** `-1`
  - **Min (Valid):** `0`
  - **Min + 1 (Valid):** `1`
- Boundary Point: `Max = 999,999,999,999`
  - **Max (Valid):** `999,999,999,999`
  - **Extreme/Precision Bounds:** `999,999,999,999,999` and value `> Number.MAX_SAFE_INTEGER`

### Variable 3: API Response Time (ms)
- Boundary Point: `Timeout = 5000ms`
  - **Cận dưới (Valid):** `4900ms`
  - **Đúng biên (Edge):** `5000ms`
  - **Cận trên (Invalid/Trigger Timeout):** `5100ms`

### Variable 4: Recent Orders List Count
- Boundary Point: `Min = 0`
  - **Min (Valid):** `0`
  - **Min + 1 (Valid):** `1`
- Boundary Point: `Max = displayLimit` (e.g., 5 or 10 orders)
  - **Max (Valid):** `displayLimit`
  - **Max + 1 (Invalid/Truncated):** `displayLimit + 1`

### Variable 5: Screen Width Breakpoint (px)
- Boundary Point: `Breakpoint = 768px` (Tablet)
  - **Min - 1 (Mobile):** `767px`
  - **Min (Tablet Boundary):** `768px`
  - **Min + 1 (Tablet/Desktop):** `769px`

### Variable 6: Other Numeric Cards
- Boundary Point: `totalUsers = 0`
  - **Min - 1 (Invalid):** `-1` users
- Boundary Point: `totalProducts = Integer`
  - **Decimal Point (Invalid):** `10.5` products

---

## 3. BVA Test Cases List
All BVA test cases are detailed in separate files in [tests/test-cases/dashboard/](../../tests/test-cases/dashboard):

- [TC-DASHBOARD-BVA-001: Kiểm tra biên dưới của Tổng số đơn hàng bằng 0 (Min)](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-001.md)
- [TC-DASHBOARD-BVA-002: Kiểm tra biên dưới + 1 của Tổng số đơn hàng bằng 1 (Min + 1)](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-002.md)
- [TC-DASHBOARD-BVA-003: Kiểm tra biên dưới - 1 của Tổng số đơn hàng bằng -1 (Min - 1)](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-003.md)
- [TC-DASHBOARD-BVA-004: Kiểm tra biên trên của Tổng số đơn hàng với số lượng lớn (100,000 đơn hàng)](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-004.md)
- [TC-DASHBOARD-BVA-005: Kiểm tra biên dưới của Tổng doanh thu bằng 0 ₫ (Min)](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-005.md)
- [TC-DASHBOARD-BVA-006: Kiểm tra biên dưới + 1 của Tổng doanh thu bằng 1 ₫ (Min + 1)](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-006.md)
- [TC-DASHBOARD-BVA-007: Kiểm tra biên dưới - 1 của Tổng doanh thu bằng -1 ₫ (Min - 1)](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-007.md)
- [TC-DASHBOARD-BVA-008: Kiểm tra biên trên của Tổng doanh thu với số cực lớn (999,999,999,999 ₫)](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-008.md)
- [TC-DASHBOARD-BVA-009: Kiểm tra biên dưới của API Response Time (4900ms - Cận dưới timeout)](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-009.md)
- [TC-DASHBOARD-BVA-010: Kiểm tra biên trên của API Response Time (5100ms - Quá biên timeout)](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-010.md)
- [TC-DASHBOARD-BVA-011: Kiểm tra recent orders list ở biên 0 item](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-011.md)
- [TC-DASHBOARD-BVA-012: Kiểm tra recent orders list ở biên 1 item](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-012.md)
- [TC-DASHBOARD-BVA-013: Kiểm tra recent orders list đúng giới hạn hiển thị tối đa](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-013.md)
- [TC-DASHBOARD-BVA-014: Kiểm tra recent orders list vượt giới hạn hiển thị 1 item](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-014.md)
- [TC-DASHBOARD-BVA-015: Kiểm tra total revenue với giá trị rất lớn không làm vỡ layout](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-015.md)
- [TC-DASHBOARD-BVA-016: Kiểm tra total revenue khi vượt giới hạn Number an toàn](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-016.md)
- [TC-DASHBOARD-BVA-017: Kiểm tra API response đúng ngưỡng timeout](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-017.md)
- [TC-DASHBOARD-BVA-018: Kiểm tra total users bằng giá trị âm](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-018.md)
- [TC-DASHBOARD-BVA-019: Kiểm tra total products bằng decimal](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-019.md)
- [TC-DASHBOARD-BVA-020: Kiểm tra responsive tại đúng breakpoint tablet](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-020.md)
- [TC-DASHBOARD-BVA-021: Kiểm tra responsive dưới breakpoint tablet 1px](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-021.md)
- [TC-DASHBOARD-BVA-022: Kiểm tra responsive trên breakpoint tablet 1px](../../tests/test-cases/dashboard/TC-DASHBOARD-BVA-022.md)
