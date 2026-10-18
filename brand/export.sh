#!/bin/sh
# Render a flyer template to a square social post (PNG) and an A4 flyer (PDF + PNG preview).
#
#   ./export.sh <template> <name> ['extra=url&params=here']
#
#   ./export.sh ritme samen-spelen
#   ./export.sh gebroken-woord improviseren
#   ./export.sh gebroken-woord samenspel 'w=Sa-men-spel&side=luisteren|en|reageren'
#
# Output lands in brand/exports/.
set -e
cd "$(dirname "$0")"
TEMPLATE="$1"; NAME="$2"; EXTRA="${3:-}"
[ -f "templates/$TEMPLATE.html" ] || { echo "usage: $0 <ritme|gebroken-woord> <name> ['params']"; exit 1; }
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
URL="file://$(pwd)/templates/$TEMPLATE.html"
mkdir -p exports
run() { "$CHROME" --headless=new --disable-gpu --hide-scrollbars --virtual-time-budget=4000 --force-device-scale-factor=1 "$@" 2>/dev/null; }

run --window-size=1080,1080 --screenshot="exports/$NAME-post.png" "$URL?format=square&export=1&$EXTRA"
run --window-size=1240,1754 --screenshot="exports/$NAME-a4.png"   "$URL?format=a4&export=1&$EXTRA"
run --no-pdf-header-footer --print-to-pdf="exports/$NAME-a4.pdf"  "$URL?format=a4&export=1&$EXTRA"
echo "exports/$NAME-post.png  exports/$NAME-a4.png  exports/$NAME-a4.pdf"
