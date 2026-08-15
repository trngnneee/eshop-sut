#!/bin/bash
# Ghi log CPU/RAM cua backend node + system load moi 5s
# Usage: ./monitor.sh <output.csv> <duration_seconds>
OUT="$1"; DUR="$2"
PID=$(pgrep -f "node server.js" | head -1)
echo "timestamp,node_pid,node_cpu_percent,node_rss_mb,sys_load_1m" > "$OUT"
END=$((SECONDS + DUR))
while [ $SECONDS -lt $END ]; do
  LINE=$(ps -p "$PID" -o %cpu=,rss= 2>/dev/null)
  if [ -z "$LINE" ]; then
    echo "$(date +%H:%M:%S),$PID,DEAD,DEAD,$(sysctl -n vm.loadavg | awk '{print $2}')" >> "$OUT"
  else
    CPU=$(echo "$LINE" | awk '{print $1}')
    RSS=$(echo "$LINE" | awk '{printf "%.1f", $2/1024}')
    LOAD=$(sysctl -n vm.loadavg | awk '{print $2}')
    echo "$(date +%H:%M:%S),$PID,$CPU,$RSS,$LOAD" >> "$OUT"
  fi
  sleep 5
done
