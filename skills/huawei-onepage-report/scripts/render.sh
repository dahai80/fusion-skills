#!/usr/bin/env bash
# 用法: render.sh input.html output.pdf [预览图目录]
# HTML -> PDF（Chrome 无头打印），再用 PDFKit 把每页渲染成 PNG 供检查排版
set -e
IN=$(cd "$(dirname "$1")" && pwd)/$(basename "$1"); OUT=$2; PV=${3:-$(dirname "$IN")}
"${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}" --headless=new --disable-gpu \
  --no-pdf-header-footer --print-to-pdf="$OUT" "file://$IN" >/dev/null 2>&1
rm -f "$PV"/p[0-9]*.png
swift "$(dirname "$0")/pdf2png.swift" "$OUT" "$PV"
