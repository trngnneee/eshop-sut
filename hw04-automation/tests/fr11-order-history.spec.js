const { test, expect } = require("@playwright/test");
const { OrderHistoryPage } = require("./pages/OrderHistoryPage");
const fr11Data = require("../data/fr11.json");

const API_BASE_URL = process.env.SUT_API_URL ?? "http://localhost:3000";

async function loginViaApi(request, user) {
  const response = await request.post(`${API_BASE_URL}${fr11Data.api.login}`, {
    data: {
      email: user.email,
      password: user.password,
    },
  });

  expect(response.ok()).toBeTruthy();
  return response.json();
}

async function createOrderViaApi(request, token, orderFixture) {
  const response = await request.post(`${API_BASE_URL}${fr11Data.api.checkout}`, {
    data: {
      total_amount: orderFixture.total_amount,
      shipping_address: orderFixture.shipping_address,
    },
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  expect(response.ok()).toBeTruthy();
  const body = await response.json();
  return {
    ...orderFixture,
    id: body.orderId,
  };
}

async function createPrimaryOrders(request, count = 3) {
  const loginResult = await loginViaApi(request, fr11Data.users.primary);
  const selectedFixtures = fr11Data.orderFixtures.primary.slice(0, count);
  const createdOrders = [];

  for (const fixture of selectedFixtures) {
    createdOrders.push(
      await createOrderViaApi(request, loginResult.token, fixture),
    );
  }

  return {
    token: loginResult.token,
    user: loginResult.user,
    orders: createdOrders,
  };
}

async function openProfileAsUser(page, token) {
  await page.addInitScript((authToken) => {
    window.localStorage.setItem("token", authToken);
  }, token);

  const orderHistoryPage = new OrderHistoryPage(page);
  await orderHistoryPage.gotoAndWaitForOrders();
  await expect(orderHistoryPage.orderHistoryHeading).toBeVisible();

  return orderHistoryPage;
}

function expectNonEmptyText(text, label) {
  expect.soft(text, `${label} should not be empty`).not.toBe("");
}

test.describe("FR-11 - Xem lịch sử đơn hàng", () => {
  test("TC-FR11-01 - User đã đăng nhập xem được bảng lịch sử đơn hàng", async ({
    page,
    request,
  }) => {
    const expectedData = fr11Data.primary_user_orders;
    const setup = await createPrimaryOrders(
      request,
      expectedData.expectedMinimumRows,
    );

    const orderHistoryPage = await openProfileAsUser(page, setup.token);

    await expect(orderHistoryPage.ordersTable).toBeVisible();
    expect(await orderHistoryPage.rowCount()).toBeGreaterThanOrEqual(
      expectedData.expectedMinimumRows,
    );

    for (const createdOrder of setup.orders) {
      await expect(
        orderHistoryPage.rowByOrderId(createdOrder.id),
      ).toBeVisible();
    }
  });

  test("TC-FR11-02 - Mỗi dòng đơn hiển thị đủ trường bắt buộc", async ({
    page,
    request,
  }) => {
    const expectedData = fr11Data.required_columns;
    const setup = await createPrimaryOrders(request, 3);
    const orderHistoryPage = await openProfileAsUser(page, setup.token);

    for (const header of expectedData.expectedHeaders) {
      await expect(orderHistoryPage.headerByName(header)).toBeVisible();
    }

    for (const createdOrder of setup.orders) {
      const row = orderHistoryPage.rowByOrderId(createdOrder.id);
      await expect(row).toBeVisible();

      expectNonEmptyText(
        (await orderHistoryPage.orderIdCell(row).textContent()).trim(),
        "Order id",
      );
      expectNonEmptyText(
        (await orderHistoryPage.orderDateCell(row).textContent()).trim(),
        "Order date",
      );
      expectNonEmptyText(
        (await orderHistoryPage.orderAmountCell(row).textContent()).trim(),
        "Order amount",
      );
      expectNonEmptyText(
        (await orderHistoryPage.orderStatusCell(row).textContent()).trim(),
        "Order status",
      );
    }
  });

  test("TC-FR11-03 - Mã đơn hiển thị theo đúng order id", async ({
    page,
    request,
  }) => {
    const expectedData = fr11Data.order_id_display;
    const setup = await createPrimaryOrders(request, 3);
    const orderHistoryPage = await openProfileAsUser(page, setup.token);

    for (const createdOrder of setup.orders) {
      const row = orderHistoryPage.rowByOrderId(createdOrder.id);

      await expect(orderHistoryPage.orderIdCell(row)).toHaveText(
        `${expectedData.expectedPrefix}${createdOrder.id}`,
      );
    }
  });

  test("TC-FR11-04 - Tổng tiền hiển thị theo định dạng tiền tệ dễ đọc", async ({
    page,
    request,
  }) => {
    const expectedData = fr11Data.amount_format;
    const setup = await createPrimaryOrders(
      request,
      expectedData.checks.length,
    );
    const orderHistoryPage = await openProfileAsUser(page, setup.token);

    for (const amountCheck of expectedData.checks) {
      const createdOrder = setup.orders.find(
        (order) => order.key === amountCheck.fixtureRef,
      );
      const row = orderHistoryPage.rowByOrderId(createdOrder.id);
      const amountCell = orderHistoryPage.orderAmountCell(row);

      await expect(amountCell).toHaveText(amountCheck.expectedAmountText);
      await expect(amountCell).not.toContainText(expectedData.forbiddenUnitText);
    }
  });
});
