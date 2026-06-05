#!/usr/bin/env python3
"""
Call Plan HTML Renderer — fills the Jinja2 template with structured data and outputs rendered HTML.

Usage:
    python render_cp.py input.json output.html

Input: JSON file with the Call Plan data structure (see DATA_SCHEMA below).
Output: Rendered HTML file.

DATA SCHEMA (what the agent produces):
{
    "customer_name": "明华重工",
    "opportunity_name": "Cloud Migration POC Validation",
    "meeting_title": "POC 验证会议",
    "meeting_date": "2026-03-20",
    "meeting_time": "14:00-15:00",
    "meeting_format": "On-site",
    "meeting_location": "明华重工总部 B 栋 3F 会议室",
    "opp_stage": "Technical Validation",
    "target_stage": "Business Validation",
    "fallback_outcome": "...",
    "customer_attendees": [
        {
            "name": "刘总",
            "title": "CTO",
            "stance": "Supporter",
            "role_in_decision": "Decision Maker|Technical Evaluator|Influencer|End User",
            "focus_priorities": "...",
            "communication_approach": "...",
            "our_goal": "..."
        }
    ],
    "aws_attendees": [
        {
            "name": "Sarah Chen",
            "role": "Account Manager",
            "purpose": "Lead conversation, relationship"
        }
    ],
    "target_outcomes": [
        {
            "customer_perspective": "...",
            "our_perspective": "..."
        }
    ],
    "success_criteria": {
        "ideal": {"customer": "...", "us": "..."},
        "acceptable": {"customer": "...", "us": "..."},
        "minimum": {"customer": "...", "us": "..."}
    },
    "disqualification_signals": ["..."],
    "questions_to_ask": [
        {"question": "...", "target_attendee": "CTO", "purpose": "..."}
    ],
    "info_to_deliver": [
        {"what": "...", "format": "...", "purpose": "..."}
    ],
    "objections": [
        {
            "objection": "...",
            "category": "Status Quo|Price/Value|Capability/Fit|Risk/Trust|Authority/Process",
            "response": "...",
            "fallback": "...",
            "is_disqualifier": false
        }
    ],
    "agenda": [
        {"time": "14:00-14:10", "topic": "...", "owner": "...", "purpose": "..."}
    ],
    "next_steps": {
        "primary": [{"step": "...", "owner": "...", "timeline": "...", "purpose": "..."}],
        "fallback": [{"step": "...", "owner": "...", "timeline": "...", "purpose": "..."}],
        "exit": [{"step": "...", "owner": "...", "timeline": "...", "purpose": "..."}]
    },
    "last_updated": "2026-05-14"
}
"""

import json
import sys
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("ERROR: jinja2 not installed. Run: pip install jinja2", file=sys.stderr)
    sys.exit(1)


def render_cp(data: dict, template_dir: str = None) -> str:
    """Render Call Plan data into HTML string."""
    if template_dir is None:
        template_dir = str(Path(__file__).parent)

    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=True
    )
    template = env.get_template("call-plan.html.j2")
    return template.render(**data)


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} input.json output.html|output.pdf", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    html = render_cp(data)

    if output_path.endswith('.pdf'):
        # Write temp HTML, then convert to PDF via headless Chrome
        import subprocess, shutil
        tmp_html = output_path.replace('.pdf', '_tmp.html')
        with open(tmp_html, 'w', encoding='utf-8') as f:
            f.write(html)
        
        chrome = (shutil.which("google-chrome")
                  or shutil.which("chromium-browser")
                  or shutil.which("chromium")
                  or shutil.which("chrome"))  # Windows 兼容
        if chrome:
            pdf_path = str(Path(output_path).resolve())
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
                f"file://{str(Path(tmp_html).resolve())}"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                Path(tmp_html).unlink(missing_ok=True)
                print(f"✅ PDF rendered (Chrome): {output_path}")
                return
            else:
                print(f"WARN: Chrome failed, trying weasyprint... ({result.stderr.strip()})", file=sys.stderr)

        # Fallback: weasyprint
        try:
            from weasyprint import HTML as WeasyHTML
            WeasyHTML(filename=str(Path(tmp_html).resolve())).write_pdf(output_path)
            Path(tmp_html).unlink(missing_ok=True)
            print(f"✅ PDF rendered (weasyprint): {output_path}")
        except ImportError:
            Path(tmp_html).unlink(missing_ok=True)
            print("ERROR: Neither Chrome nor weasyprint available.", file=sys.stderr)
            print("  Install one of: google-chrome | chromium | pip install weasyprint", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            Path(tmp_html).unlink(missing_ok=True)
            print(f"ERROR: weasyprint failed: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ HTML rendered: {output_path}")


if __name__ == "__main__":
    main()
