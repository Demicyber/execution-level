#!/bin/bash
# One-command setup for execution-level rendering engine
# Usage: curl -sSL <this-url> | bash
#   or:  bash setup.sh

set -euo pipefail

REPO_DIR="$HOME/execution-level"

echo "=== 1/4 Clone repo ==="
if [ -d "$REPO_DIR" ]; then
  cd "$REPO_DIR" && git pull
else
  git clone https://github.com/Demicyber/execution-level.git "$REPO_DIR"
  cd "$REPO_DIR"
fi

echo "=== 2/4 Install Python deps ==="
pip install -q reportlab python-docx pyyaml

echo "=== 3/4 Download fonts ==="
cd shared/fonts && bash download.sh

echo "=== 4/4 Verify ==="
cd "$REPO_DIR"
python -c "from shared import render; print('✅ Rendering engine ready')"

echo ""
echo "============================="
echo "✅ Done! Rendering engine installed at: $REPO_DIR"
echo ""
echo "Usage: cd $REPO_DIR && python -m shared <file.md> -f pdf --strict"
echo "============================="
