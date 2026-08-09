const { test, expect } = require("@playwright/test");
const { AdminUserManagementPage } = require("./pages/AdminUserManagementPage");
const fr19Data = require("../data/fr19.json");

const API_BASE_URL = process.env.SUT_API_URL ?? "http://localhost:3000";
const ADMIN_BASE_URL =
  process.env.SUT_ADMIN_BASE_URL ?? "http://localhost:5174";

async function loginViaApi(request, user) {
  const response = await request.post(`${API_BASE_URL}${fr19Data.api.login}`, {
    data: {
      email: user.email,
      password: user.password,
    },
  });

  expect(response.ok()).toBeTruthy();
  return response.json();
}

async function registerViaApi(request, user) {
  const response = await request.post(`${API_BASE_URL}${fr19Data.api.register}`, {
    data: {
      name: user.name,
      email: user.email,
      password: user.password,
    },
  });

  expect(response.ok()).toBeTruthy();
}

function uniqueUser(userTemplate, label) {
  const uniquePart = `${label}-${Date.now()}-${Math.random()
    .toString(36)
    .slice(2, 8)}`;

  return {
    name: `${userTemplate.namePrefix} ${uniquePart}`,
    email: `${userTemplate.emailPrefix}-${uniquePart}@${userTemplate.emailDomain}`,
    password: userTemplate.password,
    role: userTemplate.role,
  };
}

function authHeaders(token) {
  return {
    Authorization: `Bearer ${token}`,
  };
}

function deleteEndpoint(userId) {
  return fr19Data.api.adminDeleteUser.replace("{id}", userId);
}

async function getAdminUsersViaApi(request, adminToken) {
  const response = await request.get(
    `${API_BASE_URL}${fr19Data.api.adminUsers}`,
    {
      headers: authHeaders(adminToken),
    },
  );

  expect(response.ok()).toBeTruthy();
  return response.json();
}

function findUserByEmail(users, email) {
  return users.find((user) => user.email === email);
}

async function createUserAndFindInAdminList(request, adminToken, userTemplate, label) {
  const user = uniqueUser(userTemplate, label);

  await registerViaApi(request, user);

  const users = await getAdminUsersViaApi(request, adminToken);
  const createdUser = findUserByEmail(users, user.email);

  expect(createdUser).toBeTruthy();
  return {
    ...user,
    id: createdUser.id,
  };
}

async function deleteUserViaApi(request, adminToken, userId) {
  return request.delete(`${API_BASE_URL}${deleteEndpoint(userId)}`, {
    headers: authHeaders(adminToken),
  });
}

async function createTemporaryAdmin(request, userTemplate, label) {
  const user = uniqueUser(userTemplate, label);

  await registerViaApi(request, user);

  const firstLogin = await loginViaApi(request, user);
  const profileResponse = await request.put(
    `${API_BASE_URL}${fr19Data.api.userProfile}`,
    {
      data: {
        name: user.name,
        shipping_address: "",
        phone: "",
        role: "admin",
      },
      headers: authHeaders(firstLogin.token),
    },
  );

  expect(profileResponse.ok()).toBeTruthy();

  return loginViaApi(request, user);
}

async function openAdminUserManagement(page, user = fr19Data.users.admin) {
  const adminPage = new AdminUserManagementPage(page);

  await adminPage.goto(ADMIN_BASE_URL);
  await adminPage.loginAsAdminAndWaitForUsers(user.email, user.password);
  await expect(adminPage.adminHeading).toBeVisible();
  await adminPage.openUsersTab();

  return adminPage;
}

function expectUserDoesNotExposeForbiddenFields(user, forbiddenFields) {
  for (const forbiddenField of forbiddenFields) {
    expect(user, `User object should not expose ${forbiddenField}`).not.toHaveProperty(
      forbiddenField,
    );
  }
}

test.describe("FR-19 - Quản lý người dùng admin", () => {
  test("TC-FR19-01 - Admin xem được bảng quản lý người dùng", async ({
    page,
  }) => {
    const expectedData = fr19Data.ui_admin_user_list;
    const adminPage = await openAdminUserManagement(page);

    await expect(adminPage.userManagementHeading).toHaveText(
      expectedData.expectedHeading,
    );
    await expect(adminPage.usersTable).toBeVisible();
    expect(await adminPage.rowCount()).toBeGreaterThanOrEqual(
      expectedData.expectedMinimumRows,
    );
  });

  test("TC-FR19-02 - Bảng user hiển thị các cột quản lý chính", async ({
    page,
  }) => {
    const expectedData = fr19Data.ui_required_columns;
    const adminPage = await openAdminUserManagement(page);

    for (const header of expectedData.expectedHeaders) {
      await expect(adminPage.headerByName(header)).toBeVisible();
    }
  });

  test("TC-FR19-03 - API list user không trả về password", async ({
    request,
  }) => {
    const expectedData = fr19Data.api_list_excludes_password;
    const loginResult = await loginViaApi(request, fr19Data.users.admin);
    const response = await request.get(
      `${API_BASE_URL}${fr19Data.api.adminUsers}`,
      {
        headers: {
          Authorization: `Bearer ${loginResult.token}`,
        },
      },
    );
    const users = await response.json();

    expect(response.status()).toBe(expectedData.expectedStatus);
    expect(Array.isArray(users)).toBeTruthy();
    expect(users.length).toBeGreaterThan(0);

    for (const user of users) {
      for (const requiredField of fr19Data.specification.requiredApiFields) {
        expect(user, `User object should include ${requiredField}`).toHaveProperty(
          requiredField,
        );
      }

      expectUserDoesNotExposeForbiddenFields(
        user,
        expectedData.forbiddenFields,
      );
    }
  });

  test("TC-FR19-04 - UI hiển thị user seed và role tương ứng", async ({
    page,
  }) => {
    const expectedData = fr19Data.ui_seed_users_visible;
    const adminPage = await openAdminUserManagement(page);

    for (const [email, expectedRole] of Object.entries(
      expectedData.expectedRoles,
    )) {
      const row = adminPage.rowByEmail(email);

      await expect(row).toBeVisible();
      await expect(adminPage.userEmailCell(row)).toHaveText(email);
      await expect(adminPage.userRoleCell(row)).toHaveText(expectedRole);
    }
  });

  test("TC-FR19-05 - Admin xóa được user thường", async ({ request }) => {
    const expectedData = fr19Data.delete_regular_user;
    const adminLogin = await loginViaApi(request, fr19Data.users.admin);
    const targetUser = await createUserAndFindInAdminList(
      request,
      adminLogin.token,
      fr19Data.users.deletableUser,
      "tc05",
    );

    const deleteResponse = await deleteUserViaApi(
      request,
      adminLogin.token,
      targetUser.id,
    );
    const body = await deleteResponse.json();

    expect(deleteResponse.status()).toBe(expectedData.expectedDeleteStatus);
    expect(body.message).toBe(expectedData.expectedMessage);
  });

  test("TC-FR19-06 - User đã xóa biến mất khỏi danh sách", async ({
    page,
    request,
  }) => {
    const expectedData = fr19Data.deleted_user_removed_from_list;
    const adminLogin = await loginViaApi(request, fr19Data.users.admin);
    const targetUser = await createUserAndFindInAdminList(
      request,
      adminLogin.token,
      fr19Data.users.deletableUser,
      "tc06",
    );

    const deleteResponse = await deleteUserViaApi(
      request,
      adminLogin.token,
      targetUser.id,
    );
    expect(deleteResponse.ok()).toBeTruthy();

    const usersAfterDelete = await getAdminUsersViaApi(
      request,
      adminLogin.token,
    );
    expect(findUserByEmail(usersAfterDelete, targetUser.email)).toBeUndefined();

    const adminPage = await openAdminUserManagement(page);
    await expect(adminPage.rowByEmail(targetUser.email)).toHaveCount(
      expectedData.expectedVisibleAfterDelete ? 1 : 0,
    );
  });

  test("TC-FR19-07 - Admin không được tự xóa tài khoản đang đăng nhập", async ({
    request,
  }) => {
    const expectedData = fr19Data.self_delete_blocked;
    const tempAdminLogin = await createTemporaryAdmin(
      request,
      fr19Data.users.selfDeleteAdmin,
      "tc07",
    );
    const usersBeforeDelete = await getAdminUsersViaApi(
      request,
      tempAdminLogin.token,
    );
    const tempAdmin = findUserByEmail(
      usersBeforeDelete,
      tempAdminLogin.user.email,
    );

    expect(tempAdmin).toBeTruthy();

    const deleteResponse = await deleteUserViaApi(
      request,
      tempAdminLogin.token,
      tempAdmin.id,
    );

    expect(deleteResponse.status()).toBe(expectedData.expectedStatus);

    const usersAfterDelete = await getAdminUsersViaApi(
      request,
      tempAdminLogin.token,
    );
    expect(findUserByEmail(usersAfterDelete, tempAdminLogin.user.email)).toBeTruthy();
  });

  test("TC-FR19-08 - API list user từ chối request không token", async ({
    request,
  }) => {
    const expectedData = fr19Data.api_without_token;
    const response = await request.get(`${API_BASE_URL}${fr19Data.api.adminUsers}`);
    const body = await response.json();

    expect(response.status()).toBe(expectedData.expectedStatus);
    expect(body.error).toBe(expectedData.expectedError);
    expect(Array.isArray(body)).toBeFalsy();
  });
});
