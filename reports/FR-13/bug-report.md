# Bug Report – FR-13 Dashboard

No bugs were found for this feature from dynamic test execution since the tests have not been executed on SUT (all test cases are in `Not Executed` status).

However, two critical bugs were discovered through static code audit (static analysis) of the EShop application:

## 1. BUG-FR13-C-01: Giao diện Dashboard hiển thị Tổng doanh thu bị nhân đôi

### Feature
FR-13 – Dashboard

### Found by Test Case
- `TC-DASHBOARD-DT-001`
- `TC-DASHBOARD-BVA-006`

### Severity / Priority
Major / High

### Environment
- OS: Windows
- Browser: Chrome
- App URL: http://localhost:5174 (Web Admin)
- Backend/API URL: http://localhost:3000
- Commit hash: N/A (Local static analysis)

### Preconditions
- Admin logged in and navigating to Dashboard.

### Steps to Reproduce (Static Code Verification)
1. Open file `frontend-admin/src/App.jsx`.
2. Go to line 218:
   ```javascript
   if (o.status === "delivered") return sum + o.total_amount * 2;
   ```
3. Observe that each delivered order's total amount is multiplied by 2 when calculating `totalRevenue`.

### Expected Result
The total revenue should equal the sum of `total_amount` for all orders with `status === "delivered"`. No multiplication by 2 should occur.
```javascript
if (o.status === "delivered") return sum + o.total_amount;
```

### Actual Result
Delivered orders have their total amounts multiplied by 2, causing the dashboard to show double the actual revenue.

### Evidence
- File location: [frontend-admin/src/App.jsx:L218](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/frontend-admin/src/App.jsx#L217-L220)

---

## 2. BUG-FR13-C-02: Backend API `/api/admin/orders` và `/api/admin/users` thiếu kiểm soát phân quyền (role)

### Feature
FR-13 – Dashboard (Security / Access Control)

### Found by Test Case
- `TC-DASHBOARD-DT-004`

### Severity / Priority
Critical / High

### Environment
- OS: Windows
- App URL: http://localhost:5174 (Web Admin)
- Backend/API URL: http://localhost:3000
- Commit hash: N/A (Local static analysis)

### Preconditions
- User has logged in and has a valid JWT token, but user role is customer/user (not admin).

### Steps to Reproduce (Static Code Verification)
1. Open file `backend/server.js`.
2. Inspect the route registration at line 494 and 510:
   ```javascript
   app.get("/api/admin/users", authenticateToken, (req, res) => { ... })
   app.get("/api/admin/orders", authenticateToken, (req, res) => { ... })
   ```
3. Observe that these routes only utilize the `authenticateToken` middleware, which decodes the token and populates `req.user`.
4. Observe that inside the handler, there is no check for `req.user.role === 'admin'`.
5. Any authenticated user (even non-admins) can fetch the list of all users and all orders.

### Expected Result
Backend should enforce that only users with `role === "admin"` can access routes prefixed with `/api/admin/`. Non-admin accounts should receive a `403 Forbidden` response.

### Actual Result
Backend only checks for authentication status. Non-admin users are able to call admin endpoints and retrieve sensitive admin data.

### Evidence
- File location: [backend/server.js:L510-L523](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/backend/server.js#L510-L523)

---

## Execution Evidence
- Test run file: N/A (Not executed)
- Date: 2026-06-28
- Tester: Human Tester & AI Assistant
