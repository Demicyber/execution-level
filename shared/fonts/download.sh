#!/bin/bash
# Download Noto Sans SC fonts for ReportLab PDF rendering
# Run this once on a new machine before generating PDFs
#
# ReportLab needs separate font files for Regular and Bold.
# We download the static (non-variable) builds which have proper weight separation.

FONT_DIR="$(dirname "$0")"
cd "$FONT_DIR"

echo "Downloading Noto Sans SC (Static builds)..."

# Static Regular (weight 400)
curl -sL "https://github.com/google/fonts/raw/main/ofl/notosanssc/static/NotoSansSC-Regular.ttf" -o NotoSansSC-Regular.ttf

# Static Bold (weight 700)
curl -sL "https://github.com/google/fonts/raw/main/ofl/notosanssc/static/NotoSansSC-Bold.ttf" -o NotoSansSC-Bold.ttf

if [ ! -s NotoSansSC-Regular.ttf ] || [ ! -s NotoSansSC-Bold.ttf ]; then
  echo "ERROR: Download failed. Falling back to variable font + fonttools extraction..."
  
  # Fallback: download variable font and extract instances
  curl -sL "https://github.com/google/fonts/raw/main/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf" -o NotoSansSC-Variable.ttf
  
  if command -v fonttools &> /dev/null || pip install fonttools -q 2>/dev/null; then
    echo "Extracting weight instances from variable font..."
    fonttools instancer NotoSansSC-Variable.ttf wght=400 -o NotoSansSC-Regular.ttf 2>/dev/null
    fonttools instancer NotoSansSC-Variable.ttf wght=700 -o NotoSansSC-Bold.ttf 2>/dev/null
  else
    echo "WARNING: fonttools not available. Copying variable font as both Regular and Bold."
    echo "         Bold text will NOT render with proper weight."
    cp NotoSansSC-Variable.ttf NotoSansSC-Regular.ttf
    cp NotoSansSC-Variable.ttf NotoSansSC-Bold.ttf
  fi
  
  rm -f NotoSansSC-Variable.ttf
fi

echo "Done! Fonts installed:"
ls -lh *.ttf 2>/dev/null || echo "No .ttf files found — download may have failed."

# Download Noto Emoji for emoji rendering in PDFs
echo ""
echo "Downloading Noto Emoji (black-and-white emoji for PDF)..."
curl -sL "https://github.com/google/fonts/raw/main/ofl/notoemoji/static/NotoEmoji-Regular.ttf" -o NotoEmoji-Regular.ttf

if [ -s NotoEmoji-Regular.ttf ]; then
  echo "Emoji font installed: $(ls -lh NotoEmoji-Regular.ttf)"
else
  echo "WARNING: Emoji font download failed. PDF emoji will be stripped."
  echo "         Alternatively install system package: sudo yum install google-noto-emoji-fonts"
  rm -f NotoEmoji-Regular.ttf
fi
