#!/usr/bin/env bash
set -u
MODE="${1:-full}"
BASE_URL="${BASE_URL:-http://127.0.0.1:3001}"
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
COL="$ROOT/postman/EShop-HW06-23127207.postman_collection.json"
ENV="$ROOT/postman/EShop-HW06-local.postman_environment.json"
OUT="$HERE/reports"
mkdir -p "$OUT"
: "${HW06_USER_PASSWORD:?Set HW06_USER_PASSWORD; fixture passwords are not committed}"
: "${HW06_ADMIN_PASSWORD:?Set HW06_ADMIN_PASSWORD; fixture passwords are not committed}"

node "$ROOT/node_modules/newman/bin/newman.js" run "$COL" -e "$ENV" \
  --env-var "base_url=$BASE_URL" --env-var "spec_strict=$MODE" \
  --env-var "user_password=$HW06_USER_PASSWORD" \
  --env-var "admin_password=$HW06_ADMIN_PASSWORD" \
  -r cli,htmlextra,json \
  --reporter-htmlextra-export "$OUT/00-full-suite.html" \
  --reporter-json-export "$OUT/00-full-suite.json"

python3 "$ROOT/tooling/sanitize_public_artifacts.py" \
  "$OUT/00-full-suite.html" "$OUT/00-full-suite.json"
