#!/bin/bash
# Download Noto Sans SC font for ReportLab PDF rendering
# Run this once on a new machine before generating PDFs

FONT_DIR="$(dirname "$0")"
cd "$FONT_DIR"

echo "Downloading Noto Sans SC (Variable Font)..."
curl -sL "https://github.com/google/fonts/raw/main/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf" -o NotoSansSC-Regular.ttf

# ReportLab needs separate files for Regular and Bold
# Variable font contains all weights, just copy it
cp NotoSansSC-Regular.ttf NotoSansSC-Bold.ttf

echo "Done! Fonts installed:"
ls -lh *.ttf
