#!/bin/bash
# DON'T BE MESSY — 一键本地预览
# pop-shutter 需要摄像头权限，必须通过 localhost 打开
cd "$(dirname "$0")"
PORT=8461
URL="http://localhost:$PORT/"
echo "▶ DON'T BE MESSY  →  $URL"
( sleep 1; open "$URL" ) &
python3 -m http.server $PORT
