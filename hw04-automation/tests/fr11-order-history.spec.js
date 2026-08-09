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

async function registerViaApi(request, user) {
  const response = await request.post(`${API_BASE_URL}${fr11Data.api.register}`, {
    data: {
      name: user.name,
      email: user.email,
      password: user.password,
    },
  });

  expect(response.ok()).toBeTruthy();
}

function uniqueUser(user, suffix) {
  return {
    ...user,
    email: user.email.replace("@", `-${suffix}-${Date.now()}@`),
  };
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

async function updateOrderStatusViaApi(request, adminToken, orderId, status) {
  const endpoint = fr11Data.api.adminOrderStatus.replace("{id}", orderId);
  const response = await request.put(`${API_BASE_URL}${endpoint}`, {
    data: { status },
    headers: {
      Authorization: `Bearer ${adminToken}`,
    },
  });

  expect(response.ok()).toBeTruthy();
}

async function moveOrderToTargetStatus(request, adminToken, orderId, targetStatus) {
  const transitions = {
    pending: [],
    confirmed: ["confirmed"],
    shipping: ["confirmed", "shipping"],
    delivered: ["confirmed", "shipping", "delivered"],
    canceled: ["canceled"],
  };

  for (const status of transitions[targetStatus] ?? []) {
    await updateOrderStatusViaApi(request, adminToken, orderId, status);
  }
}

function primaryFixtureByKey(fixtureKey) {
  return fr11Data.orderFixtures.primary.find(
    (fixture) => fixture.key === fixtureKey,
  );
}

async function createPrimaryOrderForStatus(request, fixtureKey) {
  const primaryLogin = await loginViaApi(request, fr11Data.users.primary);
  const adminLogin = await loginViaApi(request, fr11Data.users.admin);
  const fixture = primaryFixtureByKey(fixtureKey);
  const createdOrder = await createOrderViaApi(
    request,
    primaryLogin.token,
    fixture,
  );

  await moveOrderToTargetStatus(
    request,
    adminLogin.token,
    createdOrder.id,
    fixture.targetStatus,
  );

  return {
    token: primaryLogin.token,
    user: primaryLogin.user,
    order: createdOrder,
  };
}

async function createOrderForNewUser(request, user, orderFixture) {
  await registerViaApi(request, user);
  const loginResult = await loginViaApi(request, user);
  const createdOrder = await createOrderViaApi(
    request,
    loginResult.token,
    orderFixture,
  );

  return {
    token: loginResult.token,
    user: loginResult.user,
    order: createdOrder,
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

async function openProfileWithoutToken(page) {
  await page.addInitScript(() => {
    window.localStorage.removeItem("token");
  });

  const orderHistoryPage = new OrderHistoryPage(page);
  await orderHistoryPage.goto();
  return orderHistoryPage;
}

function expectNonEmptyText(text, label) {
  expect.soft(text, `${label} should not be empty`).not.toBe("");
}

async function expectStatusBadge(orderHistoryPage, orderId, statusExpectation) {
  const row = orderHistoryPage.rowByOrderId(orderId);
  const badge = orderHistoryPage.orderStatusBadge(row);

  await expect(row).toBeVisible();
  await expect(badge).toContainText(statusExpectation.label);

  for (const className of statusExpectation.classContains) {
    await expect(badge).toHaveClass(new RegExp(className));
  }
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

  test("TC-FR11-05 - Trạng thái pending được dịch tiếng Việt và có màu riêng", async ({
    page,
    request,
  }) => {
    const expectedData = fr11Data.status_pending;
    const setup = await createPrimaryOrderForStatus(
      request,
      expectedData.fixtureRef,
    );
    const orderHistoryPage = await openProfileAsUser(page, setup.token);

    await expectStatusBadge(
      orderHistoryPage,
      setup.order.id,
      fr11Data.statusExpectations[expectedData.status],
    );
  });

  test("TC-FR11-06 - Trạng thái confirmed được dịch tiếng Việt và có màu riêng", async ({
    page,
    request,
  }) => {
    const expectedData = fr11Data.status_confirmed;
    const setup = await createPrimaryOrderForStatus(
      request,
      expectedData.fixtureRef,
    );
    const orderHistoryPage = await openProfileAsUser(page, setup.token);

    await expectStatusBadge(
      orderHistoryPage,
      setup.order.id,
      fr11Data.statusExpectations[expectedData.status],
    );
  });

  test("TC-FR11-07 - Trạng thái shipping được dịch tiếng Việt và có màu riêng", async ({
    page,
    request,
  }) => {
    const expectedData = fr11Data.status_shipping;
    const setup = await createPrimaryOrderForStatus(
      request,
      expectedData.fixtureRef,
    );
    const orderHistoryPage = await openProfileAsUser(page, setup.token);

    await expectStatusBadge(
      orderHistoryPage,
      setup.order.id,
      fr11Data.statusExpectations[expectedData.status],
    );
  });

  test("TC-FR11-08 - Trạng thái delivered được dịch tiếng Việt và có màu riêng", async ({
    page,
    request,
  }) => {
    const expectedData = fr11Data.status_delivered;
    const setup = await createPrimaryOrderForStatus(
      request,
      expectedData.fixtureRef,
    );
    const orderHistoryPage = await openProfileAsUser(page, setup.token);

    await expectStatusBadge(
      orderHistoryPage,
      setup.order.id,
      fr11Data.statusExpectations[expectedData.status],
    );
  });

  test("TC-FR11-09 - Trạng thái canceled được dịch tiếng Việt và có màu riêng", async ({
    page,
    request,
  }) => {
    const expectedData = fr11Data.status_canceled;
    const setup = await createPrimaryOrderForStatus(
      request,
      expectedData.fixtureRef,
    );
    const orderHistoryPage = await openProfileAsUser(page, setup.token);

    await expectStatusBadge(
      orderHistoryPage,
      setup.order.id,
      fr11Data.statusExpectations[expectedData.status],
    );
  });

  test("TC-FR11-10 - User không thấy đơn hàng của user khác", async ({
    page,
    request,
  }) => {
    const expectedData = fr11Data.other_user_isolation;
    const otherUser = uniqueUser(fr11Data.users.other, "isolation");
    const otherOrderFixture = fr11Data.orderFixtures.other.find(
      (fixture) => fixture.key === expectedData.otherOrderRef,
    );
    const otherSetup = await createOrderForNewUser(
      request,
      otherUser,
      otherOrderFixture,
    );
    const primarySetup = await createPrimaryOrders(request, 1);
    const orderHistoryPage = await openProfileAsUser(page, primarySetup.token);

    await expect(
      orderHistoryPage.rowByOrderId(primarySetup.orders[0].id),
    ).toBeVisible();
    await expect(orderHistoryPage.rowByOrderId(otherSetup.order.id)).toHaveCount(0);
    await expect(orderHistoryPage.ordersTable).not.toContainText(
      expectedData.forbiddenAmountText,
    );
  });

  test("TC-FR11-11 - Chưa đăng nhập không xem được lịch sử đơn hàng qua UI", async ({
    page,
  }) => {
    const expectedData = fr11Data.unauthenticated_profile;
    const orderHistoryPage = await openProfileWithoutToken(page);

    await expect(orderHistoryPage.unauthenticatedMessage).toContainText(
      expectedData.expectedMessage,
    );
    await expect(orderHistoryPage.orderHistoryHeading).toHaveCount(0);
    await expect(orderHistoryPage.ordersTable).toHaveCount(0);
  });

  test("TC-FR11-12 - API lịch sử đơn hàng từ chối request không có token", async ({
    request,
  }) => {
    const expectedData = fr11Data.api_without_token;
    const response = await request.get(`${API_BASE_URL}${fr11Data.api.myOrders}`);
    const body = await response.json();

    expect(response.status()).toBe(expectedData.expectedStatus);
    expect(body.error).toBe(expectedData.expectedError);
    expect(Array.isArray(body)).toBeFalsy();
  });

  test("TC-FR11-13 - API lịch sử đơn hàng từ chối token không hợp lệ", async ({
    request,
  }) => {
    const expectedData = fr11Data.api_invalid_token;
    const response = await request.get(`${API_BASE_URL}${fr11Data.api.myOrders}`, {
      headers: {
        Authorization: `Bearer ${expectedData.token}`,
      },
    });
    const body = await response.json();

    expect(response.status()).toBe(expectedData.expectedStatus);
    expect(body.error).toBe(expectedData.expectedError);
    expect(Array.isArray(body)).toBeFalsy();
  });

  test("TC-FR11-14 - User chưa có đơn hàng thấy empty state phù hợp", async ({
    page,
    request,
  }) => {
    const expectedData = fr11Data.empty_order_history;
    const emptyUser = uniqueUser(fr11Data.users.emptyHistory, "empty");

    await registerViaApi(request, emptyUser);
    const loginResult = await loginViaApi(request, emptyUser);
    const orderHistoryPage = await openProfileAsUser(page, loginResult.token);

    await expect(orderHistoryPage.emptyStateMessage).toHaveText(
      expectedData.expectedEmptyStateText,
    );
    await expect(orderHistoryPage.ordersTable).toHaveCount(0);
    expect(await orderHistoryPage.rowCount()).toBe(expectedData.expectedOrderCount);
  });
});
