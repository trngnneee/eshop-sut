# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: fr19-user-management.spec.js >> FR-19 - Quản lý người dùng admin >> TC-FR19-10 - User thường không được lấy danh sách user
- Location: tests\fr19-user-management.spec.js:327:3

# Error details

```
Error: expect(received).toBe(expected) // Object.is equality

Expected: 403
Received: 200
```

# Test source

```ts
  241 |       request,
  242 |       adminLogin.token,
  243 |       fr19Data.users.deletableUser,
  244 |       "tc06",
  245 |     );
  246 | 
  247 |     const deleteResponse = await deleteUserViaApi(
  248 |       request,
  249 |       adminLogin.token,
  250 |       targetUser.id,
  251 |     );
  252 |     expect(deleteResponse.ok()).toBeTruthy();
  253 | 
  254 |     const usersAfterDelete = await getAdminUsersViaApi(
  255 |       request,
  256 |       adminLogin.token,
  257 |     );
  258 |     expect(findUserByEmail(usersAfterDelete, targetUser.email)).toBeUndefined();
  259 | 
  260 |     const adminPage = await openAdminUserManagement(page);
  261 |     await expect(adminPage.rowByEmail(targetUser.email)).toHaveCount(
  262 |       expectedData.expectedVisibleAfterDelete ? 1 : 0,
  263 |     );
  264 |   });
  265 | 
  266 |   test("TC-FR19-07 - Admin không được tự xóa tài khoản đang đăng nhập", async ({
  267 |     request,
  268 |   }) => {
  269 |     const expectedData = fr19Data.self_delete_blocked;
  270 |     const tempAdminLogin = await createTemporaryAdmin(
  271 |       request,
  272 |       fr19Data.users.selfDeleteAdmin,
  273 |       "tc07",
  274 |     );
  275 |     const usersBeforeDelete = await getAdminUsersViaApi(
  276 |       request,
  277 |       tempAdminLogin.token,
  278 |     );
  279 |     const tempAdmin = findUserByEmail(
  280 |       usersBeforeDelete,
  281 |       tempAdminLogin.user.email,
  282 |     );
  283 | 
  284 |     expect(tempAdmin).toBeTruthy();
  285 | 
  286 |     const deleteResponse = await deleteUserViaApi(
  287 |       request,
  288 |       tempAdminLogin.token,
  289 |       tempAdmin.id,
  290 |     );
  291 | 
  292 |     expect(deleteResponse.status()).toBe(expectedData.expectedStatus);
  293 | 
  294 |     const usersAfterDelete = await getAdminUsersViaApi(
  295 |       request,
  296 |       tempAdminLogin.token,
  297 |     );
  298 |     expect(findUserByEmail(usersAfterDelete, tempAdminLogin.user.email)).toBeTruthy();
  299 |   });
  300 | 
  301 |   test("TC-FR19-08 - API list user từ chối request không token", async ({
  302 |     request,
  303 |   }) => {
  304 |     const expectedData = fr19Data.api_without_token;
  305 |     const response = await request.get(`${API_BASE_URL}${fr19Data.api.adminUsers}`);
  306 |     const body = await response.json();
  307 | 
  308 |     expect(response.status()).toBe(expectedData.expectedStatus);
  309 |     expect(body.error).toBe(expectedData.expectedError);
  310 |     expect(Array.isArray(body)).toBeFalsy();
  311 |   });
  312 | 
  313 |   test("TC-FR19-09 - API list user từ chối token không hợp lệ", async ({
  314 |     request,
  315 |   }) => {
  316 |     const expectedData = fr19Data.api_invalid_token;
  317 |     const response = await request.get(`${API_BASE_URL}${fr19Data.api.adminUsers}`, {
  318 |       headers: authHeaders(expectedData.token),
  319 |     });
  320 |     const body = await response.json();
  321 | 
  322 |     expect(response.status()).toBe(expectedData.expectedStatus);
  323 |     expect(body.error).toBe(expectedData.expectedError);
  324 |     expect(Array.isArray(body)).toBeFalsy();
  325 |   });
  326 | 
  327 |   test("TC-FR19-10 - User thường không được lấy danh sách user", async ({
  328 |     request,
  329 |   }) => {
  330 |     const expectedData = fr19Data.api_non_admin_list_forbidden;
  331 |     const nonAdminUser = uniqueUser(fr19Data.users.nonAdminActor, "tc10");
  332 | 
  333 |     await registerViaApi(request, nonAdminUser);
  334 |     const nonAdminLogin = await loginViaApi(request, nonAdminUser);
  335 | 
  336 |     const response = await request.get(`${API_BASE_URL}${fr19Data.api.adminUsers}`, {
  337 |       headers: authHeaders(nonAdminLogin.token),
  338 |     });
  339 |     const body = await response.json();
  340 | 
> 341 |     expect(response.status()).toBe(expectedData.expectedStatus);
      |                               ^ Error: expect(received).toBe(expected) // Object.is equality
  342 |     expect(body.error).toBe(expectedData.expectedError);
  343 |     expect(Array.isArray(body)).toBeFalsy();
  344 |   });
  345 | 
  346 |   test("TC-FR19-11 - User thường không được xóa user", async ({ request }) => {
  347 |     const expectedData = fr19Data.api_non_admin_delete_forbidden;
  348 |     const adminLogin = await loginViaApi(request, fr19Data.users.admin);
  349 |     const nonAdminUser = uniqueUser(fr19Data.users.nonAdminActor, "tc11-actor");
  350 |     const protectedUser = await createUserAndFindInAdminList(
  351 |       request,
  352 |       adminLogin.token,
  353 |       fr19Data.users.protectedOtherUser,
  354 |       "tc11-target",
  355 |     );
  356 | 
  357 |     await registerViaApi(request, nonAdminUser);
  358 |     const nonAdminLogin = await loginViaApi(request, nonAdminUser);
  359 | 
  360 |     const deleteResponse = await deleteUserViaApi(
  361 |       request,
  362 |       nonAdminLogin.token,
  363 |       protectedUser.id,
  364 |     );
  365 | 
  366 |     expect(deleteResponse.status()).toBe(expectedData.expectedStatus);
  367 | 
  368 |     const usersAfterDeleteAttempt = await getAdminUsersViaApi(
  369 |       request,
  370 |       adminLogin.token,
  371 |     );
  372 |     expect(findUserByEmail(usersAfterDeleteAttempt, protectedUser.email)).toBeTruthy();
  373 |   });
  374 | 
  375 |   test("TC-FR19-12 - UI admin từ chối đăng nhập bằng user thường", async ({
  376 |     page,
  377 |   }) => {
  378 |     const expectedData = fr19Data.ui_non_admin_login_rejected;
  379 |     const adminPage = new AdminUserManagementPage(page);
  380 | 
  381 |     page.on("dialog", async (dialog) => {
  382 |       expect(dialog.message()).toBe(expectedData.expectedAlert);
  383 |       await dialog.accept();
  384 |     });
  385 | 
  386 |     await adminPage.goto(ADMIN_BASE_URL);
  387 |     await adminPage.login(
  388 |       fr19Data.users.seedUser.email,
  389 |       fr19Data.users.seedUser.password,
  390 |     );
  391 | 
  392 |     await expect(adminPage.loginHeading).toBeVisible();
  393 |     await expect(adminPage.userManagementHeading).toHaveCount(0);
  394 |   });
  395 | 
  396 |   test("TC-FR19-13 - Xóa một user không ảnh hưởng user khác", async ({
  397 |     page,
  398 |     request,
  399 |   }) => {
  400 |     const expectedData = fr19Data.delete_one_user_preserves_others;
  401 |     const adminLogin = await loginViaApi(request, fr19Data.users.admin);
  402 |     const targetUser = await createUserAndFindInAdminList(
  403 |       request,
  404 |       adminLogin.token,
  405 |       fr19Data.users.deletableUser,
  406 |       "tc13-target",
  407 |     );
  408 |     const protectedUser = await createUserAndFindInAdminList(
  409 |       request,
  410 |       adminLogin.token,
  411 |       fr19Data.users.protectedOtherUser,
  412 |       "tc13-protected",
  413 |     );
  414 | 
  415 |     const deleteResponse = await deleteUserViaApi(
  416 |       request,
  417 |       adminLogin.token,
  418 |       targetUser.id,
  419 |     );
  420 |     expect(deleteResponse.ok()).toBeTruthy();
  421 | 
  422 |     const usersAfterDelete = await getAdminUsersViaApi(
  423 |       request,
  424 |       adminLogin.token,
  425 |     );
  426 |     expect(findUserByEmail(usersAfterDelete, targetUser.email)).toBeUndefined();
  427 |     expect(findUserByEmail(usersAfterDelete, protectedUser.email)).toBeTruthy();
  428 | 
  429 |     const adminPage = await openAdminUserManagement(page);
  430 |     await expect(adminPage.rowByEmail(targetUser.email)).toHaveCount(0);
  431 |     if (expectedData.expectedPreserved) {
  432 |       await expect(adminPage.rowByEmail(protectedUser.email)).toBeVisible();
  433 |     }
  434 |   });
  435 | 
  436 |   test("TC-FR19-14 - UI không hiển thị password", async ({ page }) => {
  437 |     const expectedData = fr19Data.ui_no_password_visible;
  438 |     const adminPage = await openAdminUserManagement(page);
  439 | 
  440 |     for (const forbiddenHeaderText of expectedData.forbiddenHeaderTexts) {
  441 |       await expect(adminPage.headerByName(forbiddenHeaderText)).toHaveCount(0);
```