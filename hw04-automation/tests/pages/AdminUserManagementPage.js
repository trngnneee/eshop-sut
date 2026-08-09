class AdminUserManagementPage {
  constructor(page) {
    this.page = page;

    this.loginHeading = page.getByRole("heading", {
      level: 2,
      name: "Admin Login",
    });
    this.loginForm = page.locator("form").filter({ has: this.loginHeading }).first();
    this.emailInput = this.loginForm.getByPlaceholder("Email");
    this.passwordInput = this.loginForm.getByPlaceholder("Password");
    this.loginButton = this.loginForm.getByRole("button", { name: "Login" });

    this.adminHeading = page.getByRole("heading", {
      level: 1,
      name: "EShop Admin",
    });
    this.usersNavItem = page.locator("li").filter({ hasText: "Người dùng" }).first();
    this.logoutNavItem = page.locator("li").filter({ hasText: "Đăng xuất" }).first();

    this.userManagementHeading = page.getByRole("heading", {
      level: 2,
      name: "Quản lý Người dùng",
    });
    this.usersTable = page.locator("table").first();
    this.tableHeaders = this.usersTable.locator("thead th");
    this.userRows = this.usersTable.locator("tbody tr");
  }

  async goto(baseUrl = "/") {
    await this.page.goto(baseUrl);
  }

  async login(email, password) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  async loginAsAdminAndWaitForUsers(email, password) {
    const usersResponse = this.page.waitForResponse(
      (response) =>
        response.url().includes("/api/admin/users") &&
        response.request().method() === "GET",
    );

    await this.login(email, password);
    await usersResponse;
  }

  async openUsersTab() {
    await this.usersNavItem.click();
    await this.userManagementHeading.waitFor();
  }

  headerByName(name) {
    return this.tableHeaders.filter({ hasText: name });
  }

  rowByEmail(email) {
    return this.userRows.filter({
      has: this.page.locator("td").filter({ hasText: email }),
    });
  }

  rowCheckbox(row) {
    return row.locator('td input[type="checkbox"]').first();
  }

  userIdCell(row) {
    return row.locator("td").nth(1);
  }

  userEmailCell(row) {
    return row.locator("td").nth(2);
  }

  userRoleCell(row) {
    return row.locator("td").nth(3);
  }

  userPhoneCell(row) {
    return row.locator("td").nth(4);
  }

  userActionCell(row) {
    return row.locator("td").nth(5);
  }

  deleteButton(row) {
    return this.userActionCell(row).getByRole("button", { name: "Xóa" });
  }

  async rowCount() {
    return this.userRows.count();
  }
}

module.exports = { AdminUserManagementPage };
