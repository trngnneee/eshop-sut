# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: fr11-order-history.spec.js >> FR-11 - Xem lịch sử đơn hàng >> TC-FR11-04 - Tổng tiền hiển thị theo định dạng tiền tệ dễ đọc
- Location: tests\fr11-order-history.spec.js:149:3

# Error details

```
Error: expect(locator).toHaveText(expected) failed

Locator:  locator('div.w-full.md\\:w-2\\/3.bg-white').filter({ has: getByRole('heading', { name: 'Lịch sử đơn hàng', level: 2 }) }).first().locator('table').first().locator('tbody tr').filter({ has: locator('td').filter({ hasText: '#10' }) }).locator('td').nth(2)
Expected: "125.000 ₫"
Received: "125,000 ₫"
Timeout:  5000ms

Call log:
  - Expect "toHaveText" with timeout 5000ms
  - waiting for locator('div.w-full.md\\:w-2\\/3.bg-white').filter({ has: getByRole('heading', { name: 'Lịch sử đơn hàng', level: 2 }) }).first().locator('table').first().locator('tbody tr').filter({ has: locator('td').filter({ hasText: '#10' }) }).locator('td').nth(2)
    14 × locator resolved to <td class="p-2 text-red-600 font-bold">125,000 ₫</td>
       - unexpected value "125,000 ₫"

```

```yaml
- cell "125,000 ₫"
```

# Test source

```ts
  67  | 
  68  | function expectNonEmptyText(text, label) {
  69  |   expect.soft(text, `${label} should not be empty`).not.toBe("");
  70  | }
  71  | 
  72  | test.describe("FR-11 - Xem lịch sử đơn hàng", () => {
  73  |   test("TC-FR11-01 - User đã đăng nhập xem được bảng lịch sử đơn hàng", async ({
  74  |     page,
  75  |     request,
  76  |   }) => {
  77  |     const expectedData = fr11Data.primary_user_orders;
  78  |     const setup = await createPrimaryOrders(
  79  |       request,
  80  |       expectedData.expectedMinimumRows,
  81  |     );
  82  | 
  83  |     const orderHistoryPage = await openProfileAsUser(page, setup.token);
  84  | 
  85  |     await expect(orderHistoryPage.ordersTable).toBeVisible();
  86  |     expect(await orderHistoryPage.rowCount()).toBeGreaterThanOrEqual(
  87  |       expectedData.expectedMinimumRows,
  88  |     );
  89  | 
  90  |     for (const createdOrder of setup.orders) {
  91  |       await expect(
  92  |         orderHistoryPage.rowByOrderId(createdOrder.id),
  93  |       ).toBeVisible();
  94  |     }
  95  |   });
  96  | 
  97  |   test("TC-FR11-02 - Mỗi dòng đơn hiển thị đủ trường bắt buộc", async ({
  98  |     page,
  99  |     request,
  100 |   }) => {
  101 |     const expectedData = fr11Data.required_columns;
  102 |     const setup = await createPrimaryOrders(request, 3);
  103 |     const orderHistoryPage = await openProfileAsUser(page, setup.token);
  104 | 
  105 |     for (const header of expectedData.expectedHeaders) {
  106 |       await expect(orderHistoryPage.headerByName(header)).toBeVisible();
  107 |     }
  108 | 
  109 |     for (const createdOrder of setup.orders) {
  110 |       const row = orderHistoryPage.rowByOrderId(createdOrder.id);
  111 |       await expect(row).toBeVisible();
  112 | 
  113 |       expectNonEmptyText(
  114 |         (await orderHistoryPage.orderIdCell(row).textContent()).trim(),
  115 |         "Order id",
  116 |       );
  117 |       expectNonEmptyText(
  118 |         (await orderHistoryPage.orderDateCell(row).textContent()).trim(),
  119 |         "Order date",
  120 |       );
  121 |       expectNonEmptyText(
  122 |         (await orderHistoryPage.orderAmountCell(row).textContent()).trim(),
  123 |         "Order amount",
  124 |       );
  125 |       expectNonEmptyText(
  126 |         (await orderHistoryPage.orderStatusCell(row).textContent()).trim(),
  127 |         "Order status",
  128 |       );
  129 |     }
  130 |   });
  131 | 
  132 |   test("TC-FR11-03 - Mã đơn hiển thị theo đúng order id", async ({
  133 |     page,
  134 |     request,
  135 |   }) => {
  136 |     const expectedData = fr11Data.order_id_display;
  137 |     const setup = await createPrimaryOrders(request, 3);
  138 |     const orderHistoryPage = await openProfileAsUser(page, setup.token);
  139 | 
  140 |     for (const createdOrder of setup.orders) {
  141 |       const row = orderHistoryPage.rowByOrderId(createdOrder.id);
  142 | 
  143 |       await expect(orderHistoryPage.orderIdCell(row)).toHaveText(
  144 |         `${expectedData.expectedPrefix}${createdOrder.id}`,
  145 |       );
  146 |     }
  147 |   });
  148 | 
  149 |   test("TC-FR11-04 - Tổng tiền hiển thị theo định dạng tiền tệ dễ đọc", async ({
  150 |     page,
  151 |     request,
  152 |   }) => {
  153 |     const expectedData = fr11Data.amount_format;
  154 |     const setup = await createPrimaryOrders(
  155 |       request,
  156 |       expectedData.checks.length,
  157 |     );
  158 |     const orderHistoryPage = await openProfileAsUser(page, setup.token);
  159 | 
  160 |     for (const amountCheck of expectedData.checks) {
  161 |       const createdOrder = setup.orders.find(
  162 |         (order) => order.key === amountCheck.fixtureRef,
  163 |       );
  164 |       const row = orderHistoryPage.rowByOrderId(createdOrder.id);
  165 |       const amountCell = orderHistoryPage.orderAmountCell(row);
  166 | 
> 167 |       await expect(amountCell).toHaveText(amountCheck.expectedAmountText);
      |                                ^ Error: expect(locator).toHaveText(expected) failed
  168 |       await expect(amountCell).not.toContainText(expectedData.forbiddenUnitText);
  169 |     }
  170 |   });
  171 | });
  172 | 
```