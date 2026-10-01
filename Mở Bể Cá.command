#!/bin/bash
# Bật máy chủ nhỏ trên máy (cổng 8791, chỉ nội bộ) rồi mở bể cá bằng Safari
cd "$(dirname "$0")"
PORT=8791
alive(){ curl -s -f "http://127.0.0.1:$PORT/api/ping" >/dev/null 2>&1; }
if ! alive; then
  # dọn máy chủ bản cũ (python http.server) nếu còn chiếm cổng
  for p in $(lsof -ti tcp:$PORT -sTCP:LISTEN 2>/dev/null); do
    if ps -p "$p" -o command= | grep -q "http.server $PORT"; then kill "$p"; sleep 0.6; fi
  done
  nohup python3 aq_server.py $PORT >/dev/null 2>&1 &
  for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15; do alive && break; sleep 0.3; done
fi
if ! alive; then echo "Không bật được máy chủ ở cổng $PORT (có thể cổng đang bị app khác dùng)."; read -n1 -p "Bấm phím bất kỳ để đóng"; exit 1; fi
open -a Safari "http://localhost:$PORT/be-ca-3d.html?v=$(date +%s)"
