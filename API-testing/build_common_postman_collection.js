const fs = require("fs");
const path = require("path");

const root = __dirname;
const baseUrl = "{{baseUrl}}";

const suites = [
  {
    name: "FR-03 Forgot Password",
    dir: "forgot-password",
    files: [
      "01_domain_partitions.json",
      "02_state_transitions.json",
      "03_security.json",
      "04_schema_validation.json",
    ],
  },
  {
    name: "FR-09 Apply Coupon",
    dir: "apply-coupon",
    files: [
      "01_domain_partitions.json",
      "02_state_transitions.json",
      "03_security.json",
      "04_schema_validation.json",
    ],
  },
  {
    name: "FR-17 Admin Coupons",
    dir: "admin-coupons",
    files: [
      "01_domain_partitions.json",
      "02_state_transitions.json",
      "03_security.json",
      "04_schema_validation.json",
    ],
  },
];

function readCases(suite) {
  return suite.files.flatMap((file) => {
    const filePath = path.join(root, suite.dir, file);
    if (!fs.existsSync(filePath)) return [];
    return JSON.parse(fs.readFileSync(filePath, "utf8")).map((testCase) => ({
      ...testCase,
      suite_name: suite.name,
      source_file: file,
    }));
  });
}

function headerList(headers = {}) {
  const result = Object.entries(headers).map(([key, value]) => ({
    key,
    value: String(value)
      .replace("{admin_token}", "{{adminToken}}")
      .replace("{user_token}", "{{userToken}}")
      .replace("{expired_admin_token}", "{{expiredAdminToken}}")
      .replace("{admin_A_token}", "{{adminToken}}"),
  }));
  if (!result.some((header) => header.key.toLowerCase() === "content-type")) {
    result.push({ key: "Content-Type", value: "application/json" });
  }
  if (!result.some((header) => header.key.toLowerCase() === "x-student-id")) {
    result.push({ key: "X-Student-Id", value: "{{studentId}}" });
  }
  return result;
}

function bodyFor(testCase) {
  const requestBody = testCase.request.body;
  if (requestBody === undefined || requestBody === null) {
    return { mode: "raw", raw: "{}" };
  }

  const contentType = testCase.request.headers["Content-Type"];
  if (contentType === "text/plain" && typeof requestBody === "string") {
    return { mode: "raw", raw: requestBody };
  }

  return {
    mode: "raw",
    raw:
      typeof requestBody === "string"
        ? requestBody
        : JSON.stringify(requestBody, null, 2),
    options: { raw: { language: "json" } },
  };
}

function requestFor(testCase) {
  return {
    method: testCase.request.method,
    header: headerList(testCase.request.headers),
    body: bodyFor(testCase),
    url: {
      raw: `${baseUrl}${testCase.request.path}`,
      host: ["{{baseUrl}}"],
      path: testCase.request.path.replace(/^\//, "").split("/"),
    },
  };
}

function expectedStatusCodes(expectedStatus) {
  if (typeof expectedStatus === "number") return [expectedStatus];
  const matches = String(expectedStatus).match(/\b[1-5]\d{2}\b/g);
  return matches ? [...new Set(matches.map(Number))] : [];
}

function statusAssertion(testCase) {
  const codes = expectedStatusCodes(testCase.expected_status);
  if (codes.length === 1) {
    return `pm.test("Expected HTTP ${codes[0]}", function () {
  pm.response.to.have.status(${codes[0]});
});`;
  }

  if (codes.length > 1) {
    return `pm.test("Expected one of HTTP ${codes.join(", ")}", function () {
  pm.expect(${JSON.stringify(codes)}).to.include(pm.response.code);
});`;
  }

  return `pm.test("Response has an HTTP status code", function () {
  pm.expect(pm.response.code).to.be.a("number");
});`;
}

function safeName(value) {
  return String(value || "").replace(/"/g, '\\"');
}

function loginItem({ name, email, password, variableName }) {
  return {
    name,
    request: {
      method: "POST",
      header: [
        { key: "Content-Type", value: "application/json" },
        { key: "X-Student-Id", value: "{{studentId}}" },
      ],
      body: {
        mode: "raw",
        raw: JSON.stringify({ email, password }, null, 2),
        options: { raw: { language: "json" } },
      },
      url: {
        raw: `${baseUrl}/api/login`,
        host: ["{{baseUrl}}"],
        path: ["api", "login"],
      },
    },
    event: [
      {
        listen: "test",
        script: {
          type: "text/javascript",
          exec: [
            'pm.test("Login returns HTTP 200", function () {',
            "  pm.response.to.have.status(200);",
            "});",
            "",
            `pm.test("Store ${variableName}", function () {`,
            "  const json = pm.response.json();",
            '  pm.expect(json.token, "token").to.be.a("string").and.not.empty;',
            `  pm.collectionVariables.set("${variableName}", json.token);`,
            "});",
          ],
        },
      },
    ],
  };
}

function authItems() {
  return {
    name: "Auth - Get Tokens",
    item: [
      loginItem({
        name: "Login admin and save adminToken",
        email: "admin@eshop.com",
        password: "Admin123!",
        variableName: "adminToken",
      }),
      loginItem({
        name: "Login user and save userToken",
        email: "test@eshop.com",
        password: "Test1234!",
        variableName: "userToken",
      }),
    ],
  };
}

function commonTests(testCase) {
  const id = testCase.temp_id;
  const endpoint = testCase.endpoint || `${testCase.request.method} ${testCase.request.path}`;
  const expectedCodes = expectedStatusCodes(testCase.expected_status);
  const lines = [
    `pm.test("X-Student-Id header is attached: " + pm.variables.get("studentId"), function () {
  pm.expect(pm.request.headers.get("X-Student-Id")).to.eql(pm.variables.get("studentId"));
});`,
    `pm.test("${safeName(id)} - ${safeName(testCase.title)}", function () {
  pm.expect(pm.response.code).to.be.a("number");
});`,
    statusAssertion(testCase),
    `pm.test("Response is JSON when body exists", function () {
  if (pm.response.text()) {
    pm.expect(pm.response.headers.get("Content-Type") || "").to.include("application/json");
    pm.response.json();
  }
});`,
    `pm.test("No obvious sensitive data leak", function () {
  const text = pm.response.text().toLowerCase();
  pm.expect(text).to.not.include("password_hash");
  pm.expect(text).to.not.include("passwordhash");
  pm.expect(text).to.not.include("reset_token");
});`,
  ];

  if (endpoint.includes("/api/forgot-password")) {
    if (
      ["DP-01", "ST-01", "SEC-01", "SV-01", "SV-02"].includes(id) ||
      String(testCase.title).includes("6 chữ số")
    ) {
      lines.push(`pm.test("resetToken is a 6 digit string per FR-03/SEC-07", function () {
  const json = pm.response.json();
  pm.expect(json.resetToken).to.be.a("string");
  pm.expect(json.resetToken).to.match(/^\\d{6}$/);
});`);
    } else if (expectedCodes.includes(200)) {
      lines.push(`pm.test("Forgot-password success response has message/resetToken when HTTP 200", function () {
  if (pm.response.code === 200) {
    const json = pm.response.json();
    pm.expect(json.message).to.be.a("string");
    pm.expect(json.resetToken).to.be.a("string");
  }
});`);
    }
  }

  if (endpoint.includes("/api/apply-coupon") && expectedCodes.includes(200)) {
    lines.push(`pm.test("Apply-coupon success response has amount fields when HTTP 200", function () {
  if (pm.response.code === 200) {
    const json = pm.response.json();
    pm.expect(json.discount_amount).to.be.a("number");
    pm.expect(json.final_amount).to.be.a("number");
  }
});`);
  }

  if (endpoint.includes("/api/admin/coupons") && expectedCodes.some((code) => code >= 200 && code < 300)) {
    lines.push(`pm.test("Admin coupon success response is a JSON object when body exists", function () {
  if (pm.response.text()) {
    pm.expect(pm.response.json()).to.be.an("object");
  }
});`);
  }

  return lines.join("\n\n");
}

function itemFor(testCase) {
  return {
    name: `${testCase.temp_id} - ${testCase.title}`,
    request: requestFor(testCase),
    event: [
      {
        listen: "test",
        script: {
          type: "text/javascript",
          exec: commonTests(testCase).split("\n"),
        },
      },
    ],
  };
}

function stageName(file) {
  return file.replace(".json", "").replace(/^\d+_/, "").replace(/_/g, " ");
}

const collectionItems = suites.map((suite) => {
  const cases = readCases(suite);
  return {
    name: suite.name,
    item: suite.files.map((file) => ({
      name: stageName(file),
      item: cases.filter((testCase) => testCase.source_file === file).map(itemFor),
    })),
  };
});

const allCases = suites.flatMap(readCases);

const collection = {
  info: {
    name: "EShop API Test Suite",
    description:
      "Common Postman collection for all current API test cases under API-testing. Generated from stage JSON files for forgot-password, apply-coupon, and admin-coupons.",
    schema: "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
  },
  item: [authItems(), ...collectionItems],
  variable: [
    { key: "baseUrl", value: "http://localhost:3000" },
    { key: "studentId", value: "PUT_YOUR_STUDENT_ID_HERE" },
    { key: "adminToken", value: "" },
    { key: "userToken", value: "" },
    { key: "expiredAdminToken", value: "expired-or-invalid-token" },
  ],
};

fs.writeFileSync(
  path.join(root, "eshop_api.postman_collection.json"),
  JSON.stringify(collection, null, 2),
);

console.log(`Wrote eshop_api.postman_collection.json with ${allCases.length} requests.`);
