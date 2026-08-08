const fs = require("fs");
const { spawnSync } = require("child_process");
const patchPath = process.argv[2];
const patch = fs.readFileSync(patchPath, "utf8").replace(/^\uFEFF/, "").trimEnd();
const codex = "C:\\Users\\THIEN DUC\\.vscode\\extensions\\openai.chatgpt-26.727.40816-win32-x64\\bin\\windows-x86_64\\codex.exe";
const result = spawnSync(codex, ["--codex-run-as-apply-patch", patch], { encoding: "utf8" });
if (result.stdout) process.stdout.write(result.stdout);
if (result.stderr) process.stderr.write(result.stderr);
if (result.error) process.stderr.write(String(result.error));
process.exit(result.status ?? 1);
*** Add File: submission-tools/fix-export.patch
*** Begin Patch
*** Update File: submission-tools/export-git-log.ps1
@@
-    $lines.Add($entry -replace '\\|', ' | ')
+    $lines.Add(($entry -replace '\\|', ' | '))
*** Delete File: submission-tools/apply-once.js
*** Delete File: submission-tools/fix-export.patch
*** End Patch
