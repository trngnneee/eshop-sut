const fs = require("fs");
const path = require("path");

const taskRoot = path.resolve(__dirname, "..");
const resultsRoot = path.join(taskRoot, "results");
const csvPath = path.join(resultsRoot, "Task3_Cross_Platform_Results.csv");
const summaryPath = path.join(resultsRoot, "run-summary.json");

const csvText = fs.readFileSync(csvPath, "utf8").trim();
const lines = csvText.split(/\r?\n/);

function parseCsvLine(line) {
  const cells = [];
  let current = "";
  let quoted = false;
  for (let index = 0; index < line.length; index += 1) {
    const character = line[index];
    if (character === '"') {
      if (quoted && line[index + 1] === '"') {
        current += '"';
        index += 1;
      } else {
        quoted = !quoted;
      }
    } else if (character === "," && !quoted) {
      cells.push(current);
      current = "";
    } else {
      current += character;
    }
  }
  cells.push(current);
  return cells;
}

const headers = parseCsvLine(lines[0]);
const rows = lines.slice(1).map((line) => {
  const cells = parseCsvLine(line);
  return Object.fromEntries(headers.map((header, index) => [header, cells[index] || ""]));
});
const runSummary = JSON.parse(fs.readFileSync(summaryPath, "utf8"));

const platforms = runSummary.platforms.map((platform) => platform.platform_id);
const platformLabels = Object.fromEntries(
  runSummary.platforms.map((platform) => [platform.platform_id, platform.platform_label]),
);
const checklistIds = [...new Set(rows.map((row) => row.checklist_id))].sort();

const escapeCell = (value) => String(value).replaceAll("|", "\\|").replaceAll("\n", " ");
const statusToken = (row) => {
  if (!row) return "MISSING";
  return `[${row.status}](${row.evidence_path})`;
};

const matrix = [
  "# Task 3 Cross-Platform Matrix",
  "",
  `**Generated:** ${runSummary.generated_at}`,
  `**Task status:** \`${runSummary.task3_status}\``,
  "",
  "Every status links to the screenshot carrying the student identity, platform/OS/device, localhost URL, checklist IDs, observation and capture time overlay.",
  "",
  `| Checklist ID | ${platforms.map((id) => escapeCell(platformLabels[id])).join(" | ")} |`,
  `|---|${platforms.map(() => "---").join("|")}|`,
];

for (const id of checklistIds) {
  matrix.push(
    `| ${id} | ${platforms
      .map((platformId) => statusToken(rows.find((row) => row.platform_id === platformId && row.checklist_id === id)))
      .join(" | ")} |`,
  );
}
matrix.push("");
fs.writeFileSync(path.join(taskRoot, "Cross_Platform_Matrix.md"), matrix.join("\n"), "utf8");

const evidenceIndex = [
  "# Task 3 Evidence Index",
  "",
  `**Generated:** ${runSummary.generated_at}`,
  `**Evidence files:** ${new Set(rows.map((row) => row.evidence_path)).size}`,
  `**Result rows:** ${rows.length}`,
  "",
  "Screenshots are grouped states: one screenshot may support multiple checklist IDs. All result rows retain a direct evidence link. Supplemental WebKit and Pixel 7 emulation remain labelled non-eligible for the third-platform requirement.",
  "",
];

for (const platformId of platforms) {
  const platform = runSummary.platforms.find((item) => item.platform_id === platformId);
  evidenceIndex.push(`## ${platform.platform_label}`);
  evidenceIndex.push("");
  evidenceIndex.push(`- Eligibility: \`${platform.eligible_for_hw03_required_three ? "ELIGIBLE" : "SUPPLEMENTAL_NOT_ELIGIBLE"}\``);
  evidenceIndex.push(`- Browser version: \`${platform.browser_version}\``);
  evidenceIndex.push(`- OS/device: ${platform.os_host}; ${platform.device}`);
  evidenceIndex.push(`- Note: ${platform.platform_note}`);
  evidenceIndex.push("");
  evidenceIndex.push("| Evidence | Checklist IDs | Statuses | Execution mode | Observation | Captured | ");
  evidenceIndex.push("|---|---|---|---|---|---|");

  const grouped = new Map();
  for (const row of rows.filter((item) => item.platform_id === platformId)) {
    if (!grouped.has(row.evidence_path)) grouped.set(row.evidence_path, []);
    grouped.get(row.evidence_path).push(row);
  }
  for (const [evidencePath, evidenceRows] of grouped) {
    const first = evidenceRows[0];
    evidenceIndex.push(
      `| [${first.evidence_id}](${evidencePath}) | ${evidenceRows.map((row) => row.checklist_id).join(", ")} | ${evidenceRows.map((row) => `${row.checklist_id}=${row.status}`).join("; ")} | ${[...new Set(evidenceRows.map((row) => row.execution_mode))].join(", ")} | ${escapeCell(evidenceRows.map((row) => row.actual_result).join(" "))} | ${first.captured_at} |`,
    );
  }
  evidenceIndex.push("");
}
fs.writeFileSync(path.join(taskRoot, "Evidence_Index.md"), evidenceIndex.join("\n"), "utf8");

const evidenceCsvRows = [];
for (const evidencePath of [...new Set(rows.map((row) => row.evidence_path))].sort()) {
  const evidenceRows = rows.filter((row) => row.evidence_path === evidencePath);
  evidenceCsvRows.push({
    evidence_id: evidenceRows[0].evidence_id,
    platform_id: evidenceRows[0].platform_id,
    evidence_path: evidencePath,
    checklist_ids: evidenceRows.map((row) => row.checklist_id).join(";"),
    statuses: evidenceRows.map((row) => `${row.checklist_id}=${row.status}`).join(";"),
    execution_modes: [...new Set(evidenceRows.map((row) => row.execution_mode))].join(";"),
    captured_at: evidenceRows[0].captured_at,
  });
}

const csvEscape = (value) => {
  const text = String(value ?? "");
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
};
const evidenceHeaders = Object.keys(evidenceCsvRows[0]);
fs.writeFileSync(
  path.join(resultsRoot, "Evidence_Index.csv"),
  [
    evidenceHeaders.join(","),
    ...evidenceCsvRows.map((row) => evidenceHeaders.map((header) => csvEscape(row[header])).join(",")),
  ].join("\n") + "\n",
  "utf8",
);

const consistency = checklistIds.map((id) => {
  const idRows = rows.filter((row) => row.checklist_id === id);
  const statuses = [...new Set(idRows.map((row) => row.status))];
  return { checklist_id: id, consistent: statuses.length === 1, statuses };
});
fs.writeFileSync(
  path.join(resultsRoot, "derived-summary.json"),
  JSON.stringify(
    {
      platform_count: platforms.length,
      eligible_platform_count: runSummary.eligible_successful_platforms,
      checklist_item_count: checklistIds.length,
      result_row_count: rows.length,
      evidence_file_count: evidenceCsvRows.length,
      status_consistent_items: consistency.filter((item) => item.consistent).length,
      status_inconsistent_items: consistency.filter((item) => !item.consistent),
      platform_counts: Object.fromEntries(
        platforms.map((platformId) => {
          const platformRows = rows.filter((row) => row.platform_id === platformId);
          return [
            platformId,
            {
              pass: platformRows.filter((row) => row.status === "Pass").length,
              fail: platformRows.filter((row) => row.status === "Fail").length,
              not_observable: platformRows.filter((row) => row.status === "Not Observable").length,
            },
          ];
        }),
      ),
    },
    null,
    2,
  ),
  "utf8",
);

console.log(`Generated matrix for ${checklistIds.length} IDs and evidence index for ${evidenceCsvRows.length} screenshots.`);
