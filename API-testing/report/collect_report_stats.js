const fs = require("fs");
const path = require("path");

const root = path.join(__dirname, "..");

function parseCsvLine(line) {
  const cells = [];
  let cell = "";
  let inQuotes = false;
  for (let i = 0; i < line.length; i += 1) {
    const c = line[i];
    const n = line[i + 1];
    if (c === "\"" && inQuotes && n === "\"") {
      cell += "\"";
      i += 1;
    } else if (c === "\"") {
      inQuotes = !inQuotes;
    } else if (c === "," && !inQuotes) {
      cells.push(cell);
      cell = "";
    } else {
      cell += c;
    }
  }
  cells.push(cell);
  return cells;
}

function parseCsv(file) {
  const text = fs.readFileSync(file, "utf8").replace(/^\uFEFF/, "");
  const lines = text.split(/\r?\n/).filter(Boolean);
  const headers = parseCsvLine(lines[0]).map((h) => h.replace(/^\uFEFF/, ""));
  return lines.slice(1).map((line) => {
    const values = parseCsvLine(line);
    return Object.fromEntries(headers.map((h, i) => [h, values[i] || ""]));
  });
}

function countBy(rows, field) {
  return rows.reduce((acc, row) => {
    const key = row[field] || "";
    acc[key] = (acc[key] || 0) + 1;
    return acc;
  }, {});
}

function reportStats(slug, reportFile) {
  const rows = parseCsv(path.join(root, slug, "test_cases_master.csv"));
  const category = countBy(rows, "category");
  const audit = countBy(rows, "Audit");
  const status = countBy(rows, "Status");
  const human = rows.filter((r) => r.id.startsWith("HT-"));
  const aiRows = rows.filter((r) => !r.id.startsWith("HT-"));
  const bugs = fs.readdirSync(path.join(root, "Bug"))
    .filter((f) => f.toLowerCase().endsWith(".md"))
    .filter((f) => {
      const upper = f.toUpperCase();
      if (slug === "forgot-password") return upper.startsWith("BUG-FORGOT-");
      if (slug === "apply-coupon") return upper.startsWith("BUG-APPLY-COUPON-");
      if (slug === "admin-coupons") return upper.startsWith("BUG-ADMIN-COUPONS-");
      return false;
    });
  return {
    slug,
    total: rows.length,
    aiTotal: aiRows.length,
    humanTotal: human.length,
    category,
    audit,
    status,
    executed: rows.length - (status["NOT EXECUTED"] || 0),
    passed: status.PASS || 0,
    failed: status.FAIL || 0,
    blocked: status.BLOCKED || status.SKIPPED || 0,
    notExecuted: status["NOT EXECUTED"] || 0,
    bugs: bugs.length,
    humanIds: human.map((r) => ({
      id: r.id,
      title: r.title,
      category: r.category,
      notes: r.Notes || r.notes || ""
    })),
    failedIds: rows.filter((r) => r.Status === "FAIL").map((r) => ({
      id: r.id,
      endpoint: r.endpoint,
      expected: r.expected_status,
      title: r.title
    })),
    bugFiles: bugs
  };
}

const all = [
  reportStats("forgot-password"),
  reportStats("apply-coupon"),
  reportStats("admin-coupons")
];

console.log(JSON.stringify(all, null, 2));
