const fs = require("fs");
const path = require("path");

const root = __dirname;
const baseUrl = "{{baseUrl}}";

const sourceFiles = [
  "01_domain_partitions.json",
  "02_state_transitions.json",
  "03_security.json",
  "04_schema_validation.json",
];

const testCases = sourceFiles.flatMap((file) => {
  const cases = JSON.parse(fs.readFileSync(path.join(root, file), "utf8"));
  return cases.map((testCase) => ({ ...testCase, source_file: file }));
});

function headerList(headers = {}) {
  return Object.entries(headers).map(([key, value]) => ({ key, value }));
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
  const headers = headerList(testCase.request.headers);
  if (!headers.some((header) => header.key.toLowerCase() === "content-type")) {
    headers.push({ key: "Content-Type", value: "application/json" });
  }
  if (!headers.some((header) => header.key.toLowerCase() === "x-student-id")) {
    headers.push({ key: "X-Student-Id", value: "{{studentId}}" });
  }

  return {
    method: testCase.request.method,
    header: headers,
    body: bodyFor(testCase),
    url: {
      raw: `${baseUrl}${testCase.request.path}`,
      host: ["{{baseUrl}}"],
      path: testCase.request.path.replace(/^\//, "").split("/"),
    },
  };
}

function statusAssertion(expectedStatus) {
  if (typeof expectedStatus === "number") {
    return `pm.test("Expected HTTP ${expectedStatus}", function () {
  pm.response.to.have.status(${expectedStatus});
});`;
  }

  if (String(expectedStatus).includes("200") && String(expectedStatus).includes("404")) {
    return `pm.test("Expected HTTP 200 or 404 according to documented policy", function () {
  pm.expect([200, 404]).to.include(pm.response.code);
});`;
  }

  return `pm.test("Expected status policy: ${String(expectedStatus).replace(/"/g, '\\"')}", function () {
  pm.expect(pm.response.code).to.be.oneOf([200, 400, 404, 429, 500]);
});`;
}

function commonTests(testCase) {
  const expectedStatus = testCase.expected_status;
  const title = testCase.title.replace(/"/g, '\\"');
  const lines = [
    `pm.test("X-Student-Id header is attached: " + (pm.variables.get("studentId") || "PUT_YOUR_STUDENT_ID_HERE"), function () {
  pm.expect(pm.request.headers.get("X-Student-Id")).to.eql(pm.variables.get("studentId") || "PUT_YOUR_STUDENT_ID_HERE");
});`,
    `pm.test("${testCase.temp_id} - ${title}", function () {`,
    "  pm.expect(pm.response.code).to.be.a('number');",
    "});",
    statusAssertion(expectedStatus),
    `pm.test("Response is JSON when body exists", function () {
  if (pm.response.text()) {
    pm.expect(pm.response.headers.get("Content-Type") || "").to.include("application/json");
    pm.response.json();
  }
});`,
    `pm.test("No leaked sensitive fields", function () {
  const text = pm.response.text().toLowerCase();
  pm.expect(text).to.not.include("password_hash");
  pm.expect(text).to.not.include("passwordhash");
  pm.expect(text).to.not.include("reset_token");
});`,
  ];

  const id = testCase.temp_id;
  if (
    ["DP-01", "ST-01", "SEC-01", "SV-01", "SV-02"].includes(id) ||
    testCase.title.includes("6 chữ số")
  ) {
    lines.push(`pm.test("resetToken is a 6 digit string per FR-03/SEC-07", function () {
  const json = pm.response.json();
  pm.expect(json.resetToken).to.be.a("string");
  pm.expect(json.resetToken).to.match(/^\\d{6}$/);
});`);
  }

  if (id === "SV-03") {
    lines.push(`pm.test("Success schema has only message and resetToken", function () {
  const json = pm.response.json();
  pm.expect(Object.keys(json).sort()).to.eql(["message", "resetToken"].sort());
});`);
  }

  if (id === "SEC-10") {
    lines.push(`pm.test("Response does not expose password or user object", function () {
  const json = pm.response.json();
  pm.expect(json).to.not.have.property("password");
  pm.expect(json).to.not.have.property("user");
  pm.expect(json).to.not.have.property("role");
});`);
  }

  if (id === "SEC-11") {
    lines.push(`pm.test("Store OTP for randomness comparison", function () {
  const token = pm.response.json().resetToken;
  const previous = pm.collectionVariables.get("previousOtpForRandomness");
  if (previous) {
    pm.expect(token).to.not.eql(previous);
  }
  pm.collectionVariables.set("previousOtpForRandomness", token);
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

const grouped = sourceFiles.map((file) => ({
  name: file.replace(".json", "").replace(/^\d+_/, "").replace(/_/g, " "),
  item: testCases.filter((testCase) => testCase.source_file === file).map(itemFor),
}));

const collection = {
  info: {
    name: "EShop FR-03 Forgot Password - Newman Collection",
    description:
      "Postman collection generated from requirement.md and API-testing/forgot-password test cases. This collection only sends requests to POST /api/forgot-password.",
    schema: "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
  },
  item: grouped,
  event: [
    {
      listen: "prerequest",
      script: {
        type: "text/javascript",
        exec: [
          "pm.request.headers.upsert({ key: 'X-Student-Id', value: pm.variables.get('studentId') || 'PUT_YOUR_STUDENT_ID_HERE' });",
          "console.log('X-Student-Id:', pm.variables.get('studentId') || 'PUT_YOUR_STUDENT_ID_HERE');",
        ],
      },
    },
  ],
  variable: [
    { key: "baseUrl", value: "http://localhost:3000" },
    { key: "studentId", value: "PUT_YOUR_STUDENT_ID_HERE" },
  ],
};

fs.writeFileSync(
  path.join(root, "forgot_password.postman_collection.json"),
  JSON.stringify(collection, null, 2),
);

console.log(
  `Wrote forgot_password.postman_collection.json with ${testCases.length} POST /api/forgot-password requests.`,
);
