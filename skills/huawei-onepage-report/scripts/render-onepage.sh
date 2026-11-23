#!/bin/bash
# macOS（Chrome 不在默认位置时设 CHROME 环境变量）：把独立 HTML 打印成单页 PDF，并从 PDF 出 2 倍清晰度 PNG，不需要 Swift。
# 页宽固定 A4（210mm）；页高随内容自动取 297～594mm，即 1～2 倍 A4，始终 1 页不分页。
# 高度按打印排版实量：先打一张超长页，在 PDF 里找正文末尾标记，不同机器字体换行不同也能量准。
# 内容超过 2 倍 A4 时报错退出：先删重复信息、压缩图高，不靠缩字号硬塞。
# 用法：bash render-onepage.sh 输入.html 新输出目录   （输出目录必须不存在）
set -eu
in=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
out=$2
test -f "$in" && test ! -e "$out" || { echo '输入不存在或输出目录已存在' >&2; exit 1; }
chrome="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
MIN_MM=297; MAX_MM=594; PROBE_MM=1200
mkdir -p "$out"
out=$(cd "$out" && pwd)
tmp_base="$(dirname "$in")/.render-$$"   # 临时副本放原文件旁边，相对路径的图片、样式照常可用
profile=$(mktemp -d)
trap 'rm -rf -- "$profile" "$tmp_base-measure.html" "$tmp_base-final.html" "$out/measure.pdf"' EXIT

inject() { # 输入 输出 页高mm 模式[measure|final]
  python3 - "$@" <<'PY'
import sys
src, dst, h, mode = sys.argv[1:5]
s = open(src, encoding='utf-8').read()
low = s.lower()
css = f"<style>@page{{size:210mm {h}mm;margin:0}}.page{{height:{h}mm!important;min-height:0!important}}</style>"
if mode == 'measure':
    # 页面高度放开，页脚先隐藏；正文末尾放一个白色标记，打印后在 PDF 里找它的位置
    css = (f"<style>@page{{size:210mm {h}mm;margin:0}}.page{{height:auto!important;min-height:0!important}}"
           ".foot{display:none!important}</style>")
    mark = ("<div id=\"__endmark\" style=\"font:4pt/1 Arial;color:#fff;margin:0;padding:0\">QQEND</div>"
            "<script>(function(){var p=document.querySelector('.page'),m=document.getElementById('__endmark');"
            "var pb=p?parseFloat(getComputedStyle(p).paddingBottom)||0:0;m.textContent='QQEND'+(pb*25.4/96).toFixed(2)+'QQ';})();</script>")
    i = low.find('<div class="foot"')
    if i < 0:
        i = low.rfind('</body>')
    if i < 0: sys.exit('HTML 里找不到 </body>')
    s = s[:i] + mark + s[i:]
    low = s.lower()
i = low.find('</head>')
if i < 0: sys.exit('HTML 里找不到 </head>')
s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
PY
}
url() { python3 -c 'import pathlib,sys;print(pathlib.Path(sys.argv[1]).as_uri(),end="")' "$1"; }
print_pdf() { "$chrome" --user-data-dir="$profile" --headless=new --disable-gpu --disable-extensions --no-pdf-header-footer \
  --virtual-time-budget=3000 --print-to-pdf="$2" "$(url "$1")" >>"$out/chrome.log" 2>&1; }

# 1) 按打印排版量正文高度：先打一张超长页，在 PDF 里找正文末尾标记
inject "$in" "$tmp_base-measure.html" "$PROBE_MM" measure
: >"$out/chrome.log"
print_pdf "$tmp_base-measure.html" "$out/measure.pdf"
need=$(osascript -l JavaScript - "$out/measure.pdf" <<'JXA'
ObjC.import('PDFKit')
function run(argv) {
  var doc = $.PDFDocument.alloc.initWithURL($.NSURL.fileURLWithPath(argv[0]));
  if (doc.pageCount != 1) return 'MULTI';
  var pg = doc.pageAtIndex(0), H = pg.boundsForBox(0).size.height;
  var m = /QQEND([\d.]+)QQ/.exec(ObjC.unwrap(pg.string));
  var sel = doc.findStringWithOptions('QQEND', 0).js;
  if (!m || !sel.length) return '';
  var b = sel[0].boundsForPage(pg);
  var top = (H - (b.origin.y + b.size.height)) * 25.4 / 72;   // 标记顶边距页顶 mm
  return (top + parseFloat(m[1])).toFixed(1);
}
JXA
)
test "$need" != MULTI || { echo "内容超过 ${PROBE_MM}mm，远超 2 倍 A4" >&2; exit 1; }
test -n "$need" || { echo '量不到页面高度：HTML 需要有 class="page" 的主容器' >&2; exit 1; }
h=$(python3 -c 'import math,sys;n=float(sys.argv[1]);print(max(int(sys.argv[2]),math.ceil(n+1)))' "$need" "$MIN_MM")
if [ "$h" -gt "$MAX_MM" ]; then
  echo "内容需要 ${need}mm，超过 2 倍 A4（${MAX_MM}mm）：先删重复信息、压缩图高，字号不低于 7pt" >&2; exit 1
fi

# 2) 按该高度打印单页 PDF
inject "$in" "$tmp_base-final.html" "$h" final
print_pdf "$tmp_base-final.html" "$out/report.pdf"

# 3) 校验 1 页，并直接从 PDF 出 2 倍清晰度（192dpi）预览图，所见即 PDF
res=$(osascript -l JavaScript - "$out/report.pdf" "$out/p1.png" <<'JXA'
ObjC.import('AppKit'); ObjC.import('PDFKit')
function run(argv) {
  var n = $.PDFDocument.alloc.initWithURL($.NSURL.fileURLWithPath(argv[0])).pageCount;
  if (n != 1) return 'PAGES ' + n;
  var img = $.NSImage.alloc.initWithContentsOfFile(argv[0]), sz = img.size, s = 192 / 72;
  var W = Math.round(sz.width * s), H = Math.round(sz.height * s);
  var rep = $.NSBitmapImageRep.alloc.initWithBitmapDataPlanesPixelsWidePixelsHighBitsPerSampleSamplesPerPixelHasAlphaIsPlanarColorSpaceNameBytesPerRowBitsPerPixel(null, W, H, 8, 4, true, false, $.NSDeviceRGBColorSpace, 0, 0);
  var ctx = $.NSGraphicsContext.graphicsContextWithBitmapImageRep(rep);
  $.NSGraphicsContext.saveGraphicsState;
  $.NSGraphicsContext.setCurrentContext(ctx);   // JXA 里用属性赋值不生效，会出空白图
  $.NSColor.whiteColor.setFill;
  $.NSRectFill($.NSMakeRect(0, 0, W, H));
  img.drawInRectFromRectOperationFraction($.NSMakeRect(0, 0, W, H), $.NSZeroRect, $.NSCompositingOperationSourceOver, 1);
  ctx.flushGraphics;
  $.NSGraphicsContext.restoreGraphicsState;
  rep.representationUsingTypeProperties($.NSBitmapImageFileTypePNG, $()).writeToFileAtomically(argv[1], true);
  return 'OK';
}
JXA
)
test "$res" = OK || { echo "实际页数：${res#PAGES }（预期 1）" >&2; exit 1; }
test -s "$out/p1.png"
ratio=$(python3 -c 'import sys;print(f"{int(sys.argv[1])/297:.2f}")' "$h")
echo "已导出 1 页 PDF 和预览图：${out}（页高 ${h}mm，A4 的 ${ratio} 倍；正文实需 ${need}mm）"
