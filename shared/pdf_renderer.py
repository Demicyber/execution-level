from __future__ import annotations

"""
pdf_renderer.py — HTML -> PDF via WeasyPrint.

Features:
- Page header: [Doc Type] | [Customer] | [Date]    Page X/Y
- Page footer: CONFIDENTIAL for EB
- Tight pagination — no half-empty pages
- A4 page size with compact margins
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def render_pdf(html_content: str, output_path: str, frontmatter: dict | None = None) -> str:
    """Render HTML string to PDF file using WeasyPrint.

    Args:
        html_content: Complete self-contained HTML string
        output_path: Path to write the PDF file
        frontmatter: Optional frontmatter dict for header/footer metadata

    Returns:
        Absolute path to the generated PDF file
    """
    try:
        from weasyprint import HTML, CSS
    except ImportError:
        raise RuntimeError(
            "WeasyPrint is not installed. Install with: pip install weasyprint\n"
            "On Linux, also install system dependencies: "
            "apt-get install libpango1.0-dev libcairo2-dev libgdk-pixbuf2.0-dev"
        )

    output_path = str(Path(output_path).resolve())

    margin_css = _build_margin_css(frontmatter)

    if margin_css:
        html_content = html_content.replace('</style>', f'\n{margin_css}\n</style>', 1)

    # Inject PDF-specific overrides to eliminate excess whitespace
    pdf_overrides = """
/* PDF-specific overrides */
.page {
  padding: 0;
  margin: 0;
  max-width: none;
}
.section-card {
  break-inside: auto;
  page-break-inside: auto;
}
.section-header {
  break-after: avoid;
  page-break-after: avoid;
}
.stakeholder-card, .objection-card, .milestone, .tier {
  break-inside: avoid;
  page-break-inside: avoid;
}
table {
  break-inside: auto;
  page-break-inside: auto;
}
table thead {
  display: table-header-group;
}
tr {
  break-inside: avoid;
  page-break-inside: avoid;
}
"""
    html_content = html_content.replace('</style>', f'\n{pdf_overrides}\n</style>', 1)

    try:
        html_doc = HTML(string=html_content)
        html_doc.write_pdf(output_path)
        logger.info(f"PDF generated: {output_path}")
    except Exception as e:
        logger.error(f"PDF generation failed with margin CSS: {e}")
        try:
            html_doc = HTML(string=html_content)
            html_doc.write_pdf(output_path)
        except Exception as e2:
            raise RuntimeError(f"PDF generation failed: {e2}")

    return output_path


def _build_margin_css(frontmatter: dict | None) -> str:
    """Build @page margin CSS with header/footer."""
    if not frontmatter:
        return ""

    from parse import get_doc_type

    doc_type = get_doc_type(frontmatter)
    customer = str(frontmatter.get("customer", ""))
    date = str(frontmatter.get("date", frontmatter.get("version", "")))

    type_labels = {
        "engagement-plan": "ENGAGEMENT PLAN",
        "call-plan": "CALL PLAN",
        "executive-briefing": "EXECUTIVE BRIEFING",
        "post-meeting-report": "POST-MEETING REPORT",
    }
    doc_label = type_labels.get(doc_type, "DOCUMENT")

    header_left = f"{doc_label}  |  {customer}"
    if date:
        header_left += f"  |  {date}"

    footer_content = ""
    if doc_type == "executive-briefing":
        footer_content = "INTERNAL USE ONLY — AWS Confidential"

    css = f'''
@page {{
  size: A4;
  margin: 16mm 16mm 16mm 16mm;

  @top-left {{
    content: "{header_left}";
    font-size: 8px;
    color: #57606A;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", sans-serif;
    border-bottom: 0.5px solid #D0D7DE;
    padding-bottom: 4px;
  }}

  @top-right {{
    content: "Page " counter(page) "/" counter(pages);
    font-size: 8px;
    color: #57606A;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    border-bottom: 0.5px solid #D0D7DE;
    padding-bottom: 4px;
  }}

  @bottom-center {{
    content: "{footer_content}";
    font-size: 8px;
    color: #CF222E;
    font-weight: 700;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }}
}}
'''
    return css
