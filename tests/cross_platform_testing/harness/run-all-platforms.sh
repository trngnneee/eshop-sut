#!/bin/bash
# Authoritative Task 3 run: re-seed the SQLite fixture before EACH platform so
# every platform starts from the identical SUT state (backend/database.js drops +
# re-seeds on every start), then execute all 66 checklist items on that platform.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
BACKEND="$HERE/../../../backend"
LOG="${1:-/tmp/xp-run.log}"

# Only the 3 required desktop platforms are part of the deliverable. The two
# emulated mobile platforms stay defined in lib/platforms.js (runnable with
# `run-audit.js --platforms all`) but are deliberately NOT part of the evidence
# set: device emulation is not a real device, so it cannot satisfy §6 anyway.
for P in P1-chromium-macos P2-firefox-macos P3-webkit-macos; do
  echo "=================== reseeding SUT database before $P ==================="
  pkill -f "node server.js" 2>/dev/null
  sleep 1
  (cd "$BACKEND" && nohup node server.js > /tmp/xp-backend.log 2>&1 &)
  for i in $(seq 1 30); do
    code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/products || true)
    [ "$code" = "200" ] && break
    sleep 1
  done
  echo "backend up (HTTP $code), products=$(curl -s http://localhost:3000/api/products | tr ',' '\n' | grep -c '"id"')"
  node "$HERE/run-audit.js" --platforms "$P"
done
