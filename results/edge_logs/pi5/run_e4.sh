#!/usr/bin/env bash
# E4 measured runs on the Pi (guide sections 6 and 8.2). Logs go to /mnt/agw/pi5_logs.
set -u
export PATH="$HOME/.local/bin:$PATH"
LOG=/mnt/agw/pi5_logs
REPO=/mnt/agw/agentic_gateway

[ "$(findmnt -n -o SOURCE /mnt/agw)" = /dev/mapper/agw ] || { echo "encrypted workspace not mounted"; exit 1; }
cd "$REPO"

snapshot() {  # $1 = label
  {
    echo "=== $1  $(date -Is)  epoch=$(date +%s)"
    cat /proc/device-tree/model; echo
    uname -a; head -4 /etc/os-release
    free -h; df -h / /mnt/agw
    vcgencmd version; vcgencmd measure_clock arm; vcgencmd measure_temp; vcgencmd get_throttled
    echo "governor: $(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor)"
    timedatectl | grep -i synchron
    echo "commit: $(git rev-parse --short HEAD)  dirty: [$(git status --short)]"
    echo "data pkg sha256:"; sha256sum src/agentic_gateway/data/*.py
    echo
  } >> "$LOG/machine.txt" 2>&1
}

# 1. Performance governor
for g in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
  echo performance | sudo -n tee "$g" >/dev/null
done
# 2. Stop services that wake up during the run
STOPPED=""
for s in cron.service bluetooth.service ModemManager.service apt-daily.timer apt-daily-upgrade.timer man-db.timer; do
  if sudo -n systemctl stop "$s" 2>/dev/null; then STOPPED="$STOPPED $s"; fi
done
echo "services stopped:$STOPPED" >> "$LOG/machine.txt"

# 3. Temperature logger (epoch, temp_c, clock_hz, throttle_flags)
[ -f "$LOG/temperature.csv" ] || echo "timestamp,temp_c,clock_hz,throttle_flags" > "$LOG/temperature.csv"
( while true; do
    printf '%s,%s,%s,%s\n' "$(date +%s.%N)" "$(vcgencmd measure_temp | cut -d= -f2 | tr -d "'C")" \
      "$(vcgencmd measure_clock arm | cut -d= -f2)" "$(vcgencmd get_throttled | cut -d= -f2)"
    sleep 5
  done >> "$LOG/temperature.csv" ) &
TEMP_PID=$!
trap 'kill $TEMP_PID 2>/dev/null' EXIT

# 4. Cool down, then record the start state
sleep 120
snapshot "before ICU"

for spec in "icu qwen7b-icu-full-reduced-v1" "ed qwen7b-ed-full-reduced-v1"; do
  set -- $spec
  echo "START $1 $(date +%s)" >> "$LOG/runs.txt"
  uv run python experiments/08_e4_edge.py --setting "$1" --source full --run "$2" --device pi5 \
    > "$LOG/e4_$1.log" 2>&1
  rc=$?
  echo "END $1 $(date +%s) exit=$rc" >> "$LOG/runs.txt"
  snapshot "after $1 (exit $rc)"
  [ $rc -eq 0 ] || { echo "ALL_DONE failed_at=$1" >> "$LOG/runs.txt"; exit $rc; }
  [ "$1" = icu ] && sleep 180   # let the board cool before ED
done
echo "ALL_DONE ok" >> "$LOG/runs.txt"
