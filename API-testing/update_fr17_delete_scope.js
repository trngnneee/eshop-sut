const fs = require("fs");
const path = require("path");

const rootDir = __dirname;
const csvPath = path.join(rootDir, "admin-coupons", "test_cases_master.csv");
const dataPath = path.join(rootDir, "data", "admin-coupons.test-data.json");

function parseCsvLine(line) {
  const cells = [];
  let cell = "";
  let inQuotes = false;

  for (let i = 0; i < line.length; i += 1) {
    const char = line[i];
    const next = line[i + 1];

    if (char === "\"" && inQuotes && next === "\"") {
      cell += "\"";
      i += 1;
    } else if (char === "\"") {
      inQuotes = !inQuotes;
    } else if (char === "," && !inQuotes) {
      cells.push(cell);
      cell = "";
    } else {
      cell += char;
    }
  }

  cells.push(cell);
  return cells;
}

function parseCsv(text) {
  const lines = text.replace(/^\uFEFF/, "").split(/\r?\n/).filter(Boolean);
  const headers = parseCsvLine(lines[0]).map((header) => header.replace(/^\uFEFF/, ""));
  const rows = lines.slice(1).map((line) => {
    const values = parseCsvLine(line);
    return headers.reduce((row, header, index) => {
      row[header] = values[index] || "";
      return row;
    }, {});
  });

  return { headers, rows };
}

function escapeCsv(value) {
  const text = String(value ?? "");
  return /[",\r\n]/.test(text) ? `"${text.replace(/"/g, "\"\"")}"` : text;
}

function toCsv(headers, rows) {
  return [
    headers.join(","),
    ...rows.map((row) => headers.map((header) => escapeCsv(row[header])).join(","))
  ].join("\n") + "\n";
}

const acceptedDeleteCases = new Set([
  "TC-ADMIN-COUPONS-ST-003",
  "TC-ADMIN-COUPONS-ST-004",
  "TC-ADMIN-COUPONS-SEC-006",
  "TC-ADMIN-COUPONS-SEC-010",
  "TC-ADMIN-COUPONS-SV-007",
  "TC-ADMIN-COUPONS-SV-008"
]);

const stillOutsideScope = new Set([
  "TC-ADMIN-COUPONS-ST-005",
  "TC-ADMIN-COUPONS-ST-006",
  "TC-ADMIN-COUPONS-ST-007",
  "TC-ADMIN-COUPONS-ST-008"
]);

const { headers, rows } = parseCsv(fs.readFileSync(csvPath, "utf8"));
for (const row of rows) {
  if (acceptedDeleteCases.has(row.id)) {
    row.Status = "";
    row.Audit = "VALID";
    row.Notes = "Đổi scope FR-17: chấp nhận test DELETE /api/admin/coupons/:id.";
  }

  if (row.id === "TC-ADMIN-COUPONS-SEC-006") {
    row.preconditions = "Tài khoản role=user có JWT hợp lệ; collection tạo coupon riêng cho test và lưu id vào biến createdCouponId.";
    row.request_path = "/api/admin/coupons/{{createdCouponId}}";
    row.expected_result = "API từ chối user thường bằng 403; coupon được tạo riêng cho test không bị xóa bởi user không có quyền admin.";
  }

  if (row.id === "TC-ADMIN-COUPONS-SEC-010") {
    row.related_FR = "FR-17, SEC-02, SEC-03";
    row.title = "JWT payload giả role admin nhưng signature sai không được xóa coupon";
    row.preconditions = "Collection tạo coupon riêng cho test bằng admin token; request chính dùng forged JWT có payload role=admin nhưng signature sai.";
    row.request_path = "/api/admin/coupons/{{createdCouponId}}";
    row.expected_status = "401";
    row.expected_result = "API từ chối JWT bị chỉnh payload role=admin nhưng signature sai; coupon fixture không được xóa bởi token giả.";
    row.Notes = "Đổi từ IDOR tenant/store không áp dụng với SUT sang security case DELETE chạy được trong scope FR-17.";
  }

  if (stillOutsideScope.has(row.id)) {
    row.Status = "NOT EXECUTED";
    row.Audit = "INVALID";
    row.Notes = "Ngoài scope chạy hiện tại vì chỉ test POST/DELETE /api/admin/coupons";
  }

}
fs.writeFileSync(csvPath, toCsv(headers, rows), "utf8");

const data = JSON.parse(fs.readFileSync(dataPath, "utf8"));
const byId = Object.fromEntries(data.map((row) => [row.testCaseId, row]));

function setDeleteCase(id, patch) {
  Object.assign(byId[id], {
    contentType: "application/json",
    bodyMode: "json",
    rawBody: "{}",
    skipReason: "",
    ...patch
  });
}

setDeleteCase("TC-ADMIN-COUPONS-ST-003", {
  setupFlow: "createCouponForDelete",
  method: "DELETE",
  path: "/api/admin/coupons/{{createdCouponId}}",
  authorization: "Bearer {{adminToken}}",
  expectedStatus: 200,
  assertions: ["common", "successDeleteSchema"]
});

setDeleteCase("TC-ADMIN-COUPONS-ST-004", {
  setupFlow: "deleteCouponBeforeMain",
  method: "DELETE",
  path: "/api/admin/coupons/{{deletedCouponId}}",
  authorization: "Bearer {{adminToken}}",
  expectedStatus: 404,
  assertions: ["common", "errorOnly"]
});

setDeleteCase("TC-ADMIN-COUPONS-SEC-006", {
  setupFlow: "createCouponForDelete",
  method: "DELETE",
  path: "/api/admin/coupons/{{createdCouponId}}",
  authorization: "Bearer {{userToken}}",
  expectedStatus: 403,
  assertions: ["common", "errorOnly"]
});

setDeleteCase("TC-ADMIN-COUPONS-SEC-010", {
  setupFlow: "createCouponForDelete",
  method: "DELETE",
  path: "/api/admin/coupons/{{createdCouponId}}",
  authorization: "Bearer {{forgedAdminRoleToken}}",
  expectedStatus: 401,
  expectedResult: "API từ chối JWT bị chỉnh payload role=admin nhưng signature sai; coupon fixture không được xóa bởi token giả.",
  secId: "SEC-02, SEC-03",
  attackVector: "Forged JWT role escalation on DELETE admin coupon",
  assertions: ["common", "errorOnly"]
});

setDeleteCase("TC-ADMIN-COUPONS-SV-007", {
  setupFlow: "createCouponForDelete",
  method: "DELETE",
  path: "/api/admin/coupons/{{createdCouponId}}",
  authorization: "Bearer {{adminToken}}",
  expectedStatus: 200,
  assertions: ["common", "successDeleteSchema", "messageString"]
});

setDeleteCase("TC-ADMIN-COUPONS-SV-008", {
  setupFlow: "",
  method: "DELETE",
  path: "/api/admin/coupons/999999",
  authorization: "Bearer {{adminToken}}",
  expectedStatus: 404,
  assertions: ["common", "errorOnly"]
});

for (const id of stillOutsideScope) {
  Object.assign(byId[id], {
    expectedStatus: "N/A",
    authorization: "",
    skipReason: "Ngoài scope chạy hiện tại vì chỉ test POST/DELETE /api/admin/coupons",
    assertions: ["skip"]
  });
}

fs.writeFileSync(dataPath, `${JSON.stringify(data, null, 2)}\n`, "utf8");

console.log("Updated FR-17 DELETE scope in CSV and admin-coupons test data.");
