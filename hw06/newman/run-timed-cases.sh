#!/usr/bin/env bash
# Chạy TC-API-LOGIN-041 và TC-API-LOGIN-024: prep -> chờ lock 180s hết hạn -> assert.
set -euo pipefail
BASE="${1:-http://localhost:3000}"
SECRET="${HW06_SUT_JWT_SECRET:-super_secret_key_that_should_not_be_here}"
HERE="$(cd "$(dirname "$0")/.." && pwd)"
NEWMAN="$HERE/node_modules/newman/bin/newman.js"
COL="$HERE/postman/EShop-HW06-23127207.postman_collection.json"
ENVF="$HERE/postman/EShop-HW06-local.postman_environment.json"
OUT="$HERE/newman/reports"
TMPENV="$OUT/.timed-env.json"

common=(-e "$ENVF" --env-var "base_url=$BASE" --env-var "spec_strict=full"
        --env-var "user_password=${HW06_USER_PASSWORD:-Test1234!}"
        --env-var "admin_password=${HW06_ADMIN_PASSWORD:-Admin123!}"
        --env-var "sut_jwt_secret=$SECRET")

echo "[1/3] prep: tạo user và làm khóa tài khoản"
node "$NEWMAN" run "$COL" "${common[@]}" --folder "05 - Timed lock prep" \
  --export-environment "$TMPENV" -r cli,json --reporter-json-export "$OUT/05-timed-prep.json"

echo "[2/3] chờ 185 giây cho lock 180s hết hạn"
sleep 185

echo "[3/3] assert: kiểm tra residual state sau khi hết khóa"
node "$NEWMAN" run "$COL" -e "$TMPENV" --env-var "base_url=$BASE" --env-var "spec_strict=full" \
  --folder "05 - Timed lock assert" \
  -r cli,htmlextra,json --reporter-htmlextra-export "$OUT/05-timed-assert.html" \
  --reporter-json-export "$OUT/05-timed-assert.json" || true

rm -f "$TMPENV"
python "$HERE/tooling/sanitize_public_artifacts.py" >/dev/null 2>&1 || true
echo "Xong. Report: newman/reports/05-timed-assert.{html,json}"
