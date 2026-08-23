const fs = require("fs");
const path = require("path");

const reportPath = path.join(__dirname, "admin-coupons-report.html");
const dataPath = path.join(__dirname, "data", "admin-coupons.test-data.json");
const html = fs.readFileSync(reportPath, "utf8");
const data = JSON.parse(fs.readFileSync(dataPath, "utf8"));

function decodeHtml(value) {
  return String(value || "")
    .replace(/&quot;/g, "\"")
    .replace(/&#x27;/g, "'")
    .replace(/&#39;/g, "'")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&amp;/g, "&")
    .replace(/<[^>]+>/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

const failed = new Map();
for (const match of html.matchAll(/Failed Test:<\/strong>\s*((?:TC|HT)-ADMIN-[A-Z-]+-\d{3})\s+-\s*([^<]+)/g)) {
  const id = match[1];
  const assertion = decodeHtml(match[2]);
  if (!failed.has(id)) failed.set(id, []);
  failed.get(id).push(assertion);
}

const statusById = new Map();
for (const match of html.matchAll(/<div id="folder-[^"]+" class="card-deck iteration-(\d+)">([\s\S]*?)(?=<div id="folder-[^"]+" class="card-deck iteration-\d+">|<\/div>\s*<\/div>\s*<\/div>\s*<div class="tab-pane fade" id="pills-skipped"|<script type="text\/javascript">)/g)) {
  const zeroBased = Number(match[1]);
  const row = data[zeroBased];
  if (!row) continue;
  const block = match[2];
  const status = block.match(/Response Code:<\/strong>\s*<span[^>]*>\s*(\d+)/);
  const responseBody = block.match(/<h5[^>]*>Response Body<\/h5>[\s\S]*?<pre><code[^>]*>([\s\S]*?)<\/code><\/pre>/);
  statusById.set(row.testCaseId, {
    iteration: zeroBased + 1,
    status: status ? Number(status[1]) : "?",
    responseBody: responseBody ? decodeHtml(responseBody[1]) : ""
  });
}

for (const [id, assertions] of failed) {
  const status = statusById.get(id);
  const row = data.find((item) => item.testCaseId === id);
  console.log(`${id} | iteration=${status?.iteration || "?"} | expected=${row?.expectedStatus ?? "?"} | actual=${status?.status || "?"} | failed=${assertions.join("; ")} | body=${status?.responseBody || ""}`);
}
