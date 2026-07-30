#!/usr/bin/env bash
# Usage: init_project.sh <slug> <output_dir>
# Creates <output_dir>/<slug>/{checklist,usability,bugs,audit,screenshots}
# and seeds them with the skill's templates.
set -euo pipefail

SLUG="${1:?Usage: init_project.sh <slug> <output_dir>}"
OUT="${2:?Usage: init_project.sh <slug> <output_dir>}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

PROJECT="$OUT/$SLUG"
mkdir -p "$PROJECT"/{checklist,usability,bugs,audit,screenshots}

cp "$SKILL_DIR/assets/checklist_template.csv" "$PROJECT/checklist/checklist.csv"
cp "$SKILL_DIR/assets/bug_report_template.md" "$PROJECT/bugs/bug_report_template.md"
cp "$SKILL_DIR/assets/usability_session_notes_template.md" "$PROJECT/usability/session_notes_template.md"
cp "$SKILL_DIR/assets/participant_list_template.csv" "$PROJECT/usability/participant_list.csv"
cp "$SKILL_DIR/assets/ai_audit_log_template.md" "$PROJECT/audit/ai_audit_log.md"

echo "Initialized project '$SLUG' at: $PROJECT"
echo "  checklist/checklist.csv"
echo "  bugs/bug_report_template.md"
echo "  usability/session_notes_template.md"
echo "  usability/participant_list.csv"
echo "  audit/ai_audit_log.md   <-- log_ai_interaction.py appends here"
echo "  screenshots/            <-- put Failed-item and bug screenshots here"