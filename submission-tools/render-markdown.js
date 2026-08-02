const fs = require("fs");
const path = require("path");

const [inputPath, outputPath] = process.argv.slice(2);
if (!inputPath || !outputPath) {
  console.error("Usage: node render-markdown.js <input.md> <output.html>");
  process.exit(2);
}

const escapeHtml = (value) =>
  value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");

const inline = (raw) => {
  const code = [];
  let value = raw.replace(/`([^`]+)`/g, (_, content) => {
    const token = `\u0000CODE${code.length}\u0000`;
    code.push(`<code>${escapeHtml(content)}</code>`);
    return token;
  });
  value = escapeHtml(value);
  value = value.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
  value = value.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  value = value.replace(/(?<!\*)\*([^*]+)\*(?!\*)/g, "<em>$1</em>");
  value = value.replace(/\u0000CODE(\d+)\u0000/g, (_, index) => code[Number(index)]);
  return value;
};

const splitCells = (line) =>
  line
    .trim()
    .replace(/^\|/, "")
    .replace(/\|$/, "")
    .split("|")
    .map((cell) => cell.trim());

const lines = fs
  .readFileSync(inputPath, "utf8")
  .replace(/^\uFEFF/, "")
  .split(/\r?\n/);
const body = [];
let index = 0;
let inCode = false;
let codeLines = [];
let listType = null;

const closeList = () => {
  if (listType) {
    body.push(`</${listType}>`);
    listType = null;
  }
};

while (index < lines.length) {
  const line = lines[index];

  if (/^```/.test(line)) {
    closeList();
    if (!inCode) {
      inCode = true;
      codeLines = [];
    } else {
      body.push(`<pre><code>${escapeHtml(codeLines.join("\n"))}</code></pre>`);
      inCode = false;
    }
    index += 1;
    continue;
  }

  if (inCode) {
    codeLines.push(line);
    index += 1;
    continue;
  }

  if (
    line.trim().startsWith("|") &&
    index + 1 < lines.length &&
    /^\s*\|?[\s:|-]+\|?\s*$/.test(lines[index + 1]) &&
    lines[index + 1].includes("-")
  ) {
    closeList();
    const headers = splitCells(line);
    body.push("<table><thead><tr>");
    headers.forEach((cell) => body.push(`<th>${inline(cell)}</th>`));
    body.push("</tr></thead><tbody>");
    index += 2;
    while (index < lines.length && lines[index].trim().startsWith("|")) {
      const cells = splitCells(lines[index]);
      body.push("<tr>");
      headers.forEach((_, cellIndex) =>
        body.push(`<td>${inline(cells[cellIndex] || "")}</td>`)
      );
      body.push("</tr>");
      index += 1;
    }
    body.push("</tbody></table>");
    continue;
  }

  const heading = line.match(/^(#{1,4})\s+(.+)$/);
  if (heading) {
    closeList();
    const level = heading[1].length;
    body.push(`<h${level}>${inline(heading[2])}</h${level}>`);
    index += 1;
    continue;
  }

  const unordered = line.match(/^\s*[-*]\s+(.+)$/);
  const ordered = line.match(/^\s*\d+\.\s+(.+)$/);
  if (unordered || ordered) {
    const wanted = unordered ? "ul" : "ol";
    if (listType !== wanted) {
      closeList();
      listType = wanted;
      body.push(`<${wanted}>`);
    }
    let item = (unordered || ordered)[1];
    item = item.replace(/^\[x\]\s+/i, "☑ ").replace(/^\[\s\]\s+/, "☐ ");
    body.push(`<li>${inline(item)}</li>`);
    index += 1;
    continue;
  }

  if (/^\s*>\s?/.test(line)) {
    closeList();
    body.push(`<blockquote>${inline(line.replace(/^\s*>\s?/, ""))}</blockquote>`);
    index += 1;
    continue;
  }

  if (/^\s*---+\s*$/.test(line)) {
    closeList();
    body.push("<hr>");
    index += 1;
    continue;
  }

  if (!line.trim()) {
    closeList();
    index += 1;
    continue;
  }

  closeList();
  const paragraph = [line.trim()];
  index += 1;
  while (
    index < lines.length &&
    lines[index].trim() &&
    !/^(#{1,4})\s+/.test(lines[index]) &&
    !/^```/.test(lines[index]) &&
    !/^\s*[-*]\s+/.test(lines[index]) &&
    !/^\s*\d+\.\s+/.test(lines[index]) &&
    !lines[index].trim().startsWith("|") &&
    !/^\s*>\s?/.test(lines[index])
  ) {
    paragraph.push(lines[index].trim());
    index += 1;
  }
  body.push(`<p>${inline(paragraph.join(" "))}</p>`);
}

closeList();
if (inCode) {
  body.push(`<pre><code>${escapeHtml(codeLines.join("\n"))}</code></pre>`);
}

const titleLine = lines.find((line) => /^#\s+/.test(line));
const title = titleLine ? titleLine.replace(/^#\s+/, "") : path.basename(inputPath);
const html = `<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${escapeHtml(title)}</title>
<style>
  @page { size: A4; margin: 16mm 14mm 17mm; }
  * { box-sizing: border-box; }
  html { font-family: "Segoe UI", Arial, sans-serif; color: #172033; font-size: 9.7pt; }
  body { margin: 0 auto; max-width: 190mm; line-height: 1.46; }
  h1 { color: #0b3d91; font-size: 21pt; margin: 0 0 14pt; border-bottom: 3px solid #2a72d4; padding-bottom: 7pt; }
  h2 { color: #12366b; font-size: 15pt; margin: 18pt 0 8pt; border-bottom: 1px solid #c8d6ea; padding-bottom: 3pt; break-after: avoid; }
  h3 { color: #204b83; font-size: 11.5pt; margin: 13pt 0 6pt; break-after: avoid; }
  h4 { font-size: 10.3pt; margin: 10pt 0 5pt; break-after: avoid; }
  p { margin: 5pt 0 8pt; orphans: 3; widows: 3; }
  ul, ol { margin: 5pt 0 9pt 18pt; padding: 0; }
  li { margin: 2pt 0; }
  table { width: 100%; border-collapse: collapse; margin: 8pt 0 12pt; font-size: 7.7pt; break-inside: auto; }
  tr { break-inside: avoid; break-after: auto; }
  th { background: #dce9f8; color: #12366b; font-weight: 650; text-align: left; }
  th, td { border: 1px solid #aebdd1; padding: 4pt 4.5pt; vertical-align: top; overflow-wrap: anywhere; }
  code { font-family: Consolas, monospace; font-size: 0.92em; background: #edf2f7; padding: 1px 3px; border-radius: 2px; }
  pre { white-space: pre-wrap; background: #111827; color: #f3f4f6; padding: 9pt; border-radius: 4px; break-inside: avoid; }
  pre code { color: inherit; background: none; padding: 0; }
  blockquote { margin: 8pt 0; padding: 7pt 10pt; border-left: 4px solid #2a72d4; background: #f3f7fc; }
  a { color: #0b5cab; text-decoration: none; }
  hr { border: 0; border-top: 1px solid #b9c6d8; margin: 14pt 0; }
</style>
</head>
<body>
${body.join("\n")}
</body>
</html>`;

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, html, "utf8");
console.log(`Rendered ${inputPath} -> ${outputPath}`);
