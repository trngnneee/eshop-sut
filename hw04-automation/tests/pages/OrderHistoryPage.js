class OrderHistoryPage {
  constructor(page) {
    this.page = page;

    this.profileRoot = page.locator("main").first();
    this.unauthenticatedMessage = page.getByText("Vui lòng đăng nhập", {
      exact: false,
    });

    this.profileHeading = page.getByRole("heading", {
      level: 2,
      name: "Hồ sơ của bạn",
    });
    this.orderHistoryHeading = page.getByRole("heading", {
      level: 2,
      name: "Lịch sử đơn hàng",
    });

    this.orderHistorySection = page
      .locator("div.w-full.md\\:w-2\\/3.bg-white")
      .filter({ has: this.orderHistoryHeading })
      .first();
    this.emptyStateMessage = page.getByText("Bạn chưa có đơn hàng nào.", {
      exact: true,
    });

    this.ordersTable = this.orderHistorySection.locator("table").first();
    this.tableHeaders = this.ordersTable.locator("thead th");
    this.orderRows = this.ordersTable.locator("tbody tr");

    this.orderIdCells = this.orderRows.locator("td:nth-child(1)");
    this.orderDateCells = this.orderRows.locator("td:nth-child(2)");
    this.orderAmountCells = this.orderRows.locator("td:nth-child(3)");
    this.orderStatusCells = this.orderRows.locator("td:nth-child(4)");
    this.orderActionCells = this.orderRows.locator("td:nth-child(5)");
  }

  async goto() {
    await this.page.goto("/profile");
  }

  async gotoAndWaitForOrders() {
    const ordersResponse = this.page.waitForResponse(
      (response) =>
        response.url().includes("/api/orders/my-orders") &&
        response.request().method() === "GET",
    );

    await this.goto();
    await ordersResponse;
  }

  headerByName(name) {
    return this.tableHeaders.filter({ hasText: name });
  }

  rowByOrderId(orderId) {
    return this.orderRows.filter({
      has: this.page.locator("td").filter({ hasText: `#${orderId}` }),
    });
  }

  rowByAmountText(amountText) {
    return this.orderRows.filter({
      has: this.page.locator("td").filter({ hasText: amountText }),
    });
  }

  rowByStatusLabel(statusLabel) {
    return this.orderRows.filter({
      has: this.page.locator("span").filter({ hasText: statusLabel }),
    });
  }

  orderIdCell(row) {
    return row.locator("td").nth(0);
  }

  orderDateCell(row) {
    return row.locator("td").nth(1);
  }

  orderAmountCell(row) {
    return row.locator("td").nth(2);
  }

  orderStatusCell(row) {
    return row.locator("td").nth(3);
  }

  orderStatusBadge(row) {
    return this.orderStatusCell(row).locator("span").first();
  }

  orderActionCell(row) {
    return row.locator("td").nth(4);
  }

  cancelButton(row) {
    return this.orderActionCell(row).getByRole("button", {
      name: "Hủy đơn",
    });
  }

  async rowCount() {
    return this.orderRows.count();
  }
}

module.exports = { OrderHistoryPage };
