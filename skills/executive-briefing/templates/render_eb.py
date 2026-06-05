#!/usr/bin/env python3
"""
Executive Briefing HTML/PDF Renderer — fills the Jinja2 template with structured data.

Usage:
    python render_eb.py input.json output.html
    python render_eb.py input.json output.pdf

Input: JSON file with the EB data structure (see sample_data.json).
Output: Rendered HTML or PDF file (determined by extension).

PDF generation:
  Priority 1: headless Chromium (chrome/chromium/google-chrome)
  Priority 2: weasyprint (pip install weasyprint)

The template uses Tailwind CDN for utility classes with screens:{} to disable
responsive breakpoints. Chrome and Firefox both render identically on desktop.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("ERROR: jinja2 not installed. Run: pip install jinja2", file=sys.stderr)
    sys.exit(1)


def render_html(data: dict, template_dir: str = None) -> str:
    """Render Executive Briefing data into HTML string."""
    if template_dir is None:
        template_dir = str(Path(__file__).parent)

    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=True
    )
    template = env.get_template("executive-briefing.html.j2")
    return template.render(**data)


def find_chrome() -> str | None:
    """Find Chrome/Chromium binary."""
    candidates = [
        "google-chrome",
        "google-chrome-stable",
        "chromium",
        "chromium-browser",
        "chrome",  # Windows — shutil.which 能找到 PATH 中的 chrome.exe
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",  # Windows 默认安装路径
    ]
    for candidate in candidates:
        if shutil.which(candidate):
            return candidate
    # Check macOS path directly
    mac_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if os.path.exists(mac_path):
        return mac_path
    return None


def html_to_pdf_chrome(html_path: str, pdf_path: str) -> bool:
    """Convert HTML to PDF using headless Chrome."""
    chrome = find_chrome()
    if not chrome:
        return False

    cmd = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-software-rasterizer",
        "--run-all-compositor-stages-before-draw",
        "--force-color-profile=srgb",
        "--window-size=1280,900",
        f"--print-to-pdf={pdf_path}",
        "--no-pdf-header-footer",
        "--print-to-pdf-no-header",
        f"file://{os.path.abspath(html_path)}"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return os.path.exists(pdf_path)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def html_to_pdf_weasyprint(html_path: str, pdf_path: str) -> bool:
    """Convert HTML to PDF using weasyprint."""
    try:
        from weasyprint import HTML
        HTML(filename=html_path).write_pdf(pdf_path)
        return True
    except ImportError:
        return False
    except Exception as e:
        print(f"weasyprint error: {e}", file=sys.stderr)
        return False


def render_pdf(html_content: str, pdf_path: str) -> bool:
    """Render HTML content to PDF. Returns True on success."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(html_content)
        tmp_html = f.name

    try:
        if html_to_pdf_chrome(tmp_html, pdf_path):
            return True

        if html_to_pdf_weasyprint(tmp_html, pdf_path):
            return True

        print("ERROR: No PDF renderer available.", file=sys.stderr)
        print("  Install one of:", file=sys.stderr)
        print("  - Google Chrome / Chromium (recommended)", file=sys.stderr)
        print("  - pip install weasyprint", file=sys.stderr)
        return False
    finally:
        os.unlink(tmp_html)


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} input.json output.html|pdf", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    html = render_html(data)

    if output_path.lower().endswith('.pdf'):
        success = render_pdf(html, output_path)
        if success:
            print(f"✅ PDF rendered: {output_path}")
        else:
            sys.exit(1)
    else:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ HTML rendered: {output_path}")


if __name__ == "__main__":
    main()
