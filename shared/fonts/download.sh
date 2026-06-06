#!/bin/bash
# Download fonts for PDF rendering (Inter + Noto Sans SC/TC + Noto Emoji)
# Run this once on a new machine before generating PDFs.
#
# Font strategy:
#   PDF  → Inter (Latin) + Noto Sans SC (简体) + Noto Sans TC (繁体) + Noto Emoji
#   HTML → font-family declaration, relies on client system fonts
#   Word → Calibri + Microsoft YaHei, relies on client Office fonts

set -euo pipefail
FONT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$FONT_DIR"

echo "=== Downloading Inter (Latin) ==="
curl -fsSL -o Inter-Regular.ttf \
  "https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Regular.ttf"
curl -fsSL -o Inter-Bold.ttf \
  "https://github.com/rsms/inter/raw/master/docs/font-files/Inter-Bold.ttf"

if [ ! -s Inter-Regular.ttf ] || [ ! -s Inter-Bold.ttf ]; then
  echo "WARNING: Inter download failed. Falling back to Noto Sans SC for Latin."
fi

echo "=== Downloading Noto Sans SC (简体中文) ==="
curl -fsSL -o NotoSansSC-Regular.ttf \
  "https://github.com/google/fonts/raw/main/ofl/notosanssc/static/NotoSansSC-Regular.ttf"
curl -fsSL -o NotoSansSC-Bold.ttf \
  "https://github.com/google/fonts/raw/main/ofl/notosanssc/static/NotoSansSC-Bold.ttf"

if [ ! -s NotoSansSC-Regular.ttf ] || [ ! -s NotoSansSC-Bold.ttf ]; then
  echo "ERROR: Noto Sans SC download failed. Trying variable font fallback..."
  curl -fsSL -o NotoSansSC-Variable.ttf \
    "https://github.com/google/fonts/raw/main/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf"
  if command -v fonttools &> /dev/null || pip install fonttools -q 2>/dev/null; then
    fonttools instancer NotoSansSC-Variable.ttf wght=400 -o NotoSansSC-Regular.ttf 2>/dev/null
    fonttools instancer NotoSansSC-Variable.ttf wght=700 -o NotoSansSC-Bold.ttf 2>/dev/null
  else
    echo "WARNING: fonttools not available. Copying variable font as both weights."
    cp NotoSansSC-Variable.ttf NotoSansSC-Regular.ttf
    cp NotoSansSC-Variable.ttf NotoSansSC-Bold.ttf
  fi
  rm -f NotoSansSC-Variable.ttf
fi

echo "=== Downloading Noto Sans TC (繁體中文) ==="
curl -fsSL -o NotoSansTC-Regular.ttf \
  "https://github.com/google/fonts/raw/main/ofl/notosanstc/static/NotoSansTC-Regular.ttf"
curl -fsSL -o NotoSansTC-Bold.ttf \
  "https://github.com/google/fonts/raw/main/ofl/notosanstc/static/NotoSansTC-Bold.ttf"

if [ ! -s NotoSansTC-Regular.ttf ] || [ ! -s NotoSansTC-Bold.ttf ]; then
  echo "WARNING: Noto Sans TC download failed. Traditional Chinese may show as tofu."
  rm -f NotoSansTC-Regular.ttf NotoSansTC-Bold.ttf
fi

echo "=== Downloading Noto Emoji ==="
curl -fsSL -o NotoEmoji-Regular.ttf \
  "https://github.com/google/fonts/raw/main/ofl/notoemoji/static/NotoEmoji-Regular.ttf"

if [ ! -s NotoEmoji-Regular.ttf ]; then
  echo "WARNING: Emoji font download failed. PDF emoji will be stripped."
  rm -f NotoEmoji-Regular.ttf
fi

echo ""
echo "=== Done! Fonts installed: ==="
ls -lh *.ttf 2>/dev/null || echo "No .ttf files found — downloads may have failed."
