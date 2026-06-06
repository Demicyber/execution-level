from __future__ import annotations

"""
pdf_renderer.py — DEPRECATED. Kept for reference only.

This module used WeasyPrint (HTML → PDF) but has been replaced by
reportlab_renderer.py (direct dict → PDF) which is faster, more reliable
for CJK, and avoids WeasyPrint's CSS Grid/shadow limitations.

DO NOT USE in production. Use `from .reportlab_renderer import render_pdf` instead.
If you need to remove this file entirely, ensure no imports reference it.
"""

import warnings

warnings.warn(
    "pdf_renderer.py is deprecated. Use reportlab_renderer.render_pdf() instead.",
    DeprecationWarning,
    stacklevel=2,
)

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def render_pdf(html_content: str, output_path: str, frontmatter: dict | None = None) -> str:
    """DEPRECATED: Render HTML string to PDF file using WeasyPrint.

    This function is kept for backward compatibility only.
    Use reportlab_renderer.render_pdf(doc, output_path) instead.
    """
    warnings.warn(
        "pdf_renderer.render_pdf() is deprecated. Use reportlab_renderer.render_pdf() instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    try:
        from weasyprint import HTML, CSS
    except ImportError:
        raise RuntimeError(
            "WeasyPrint is not installed. This renderer is deprecated — "
            "use reportlab_renderer.render_pdf() instead.\n"
            "If you still need WeasyPrint: pip install weasyprint"
        )

    output_path = str(Path(output_path).resolve())

    margin_css = _build_margin_css(frontmatter)

    if margin_css:
        html_content = html_content.replace('</style>', f'\n{margin_css}\n</style>', 1)

    # Inject PDF-specific overrides
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
}
"""
    html_content = html_content.replace('</style>', f'\n{pdf_overrides}\n</style>', 1)

    html_obj = HTML(string=html_content)
    html_obj.write_pdf(output_path)

    logger.info(f"[DEPRECATED WeasyPrint] PDF generated: {output_path}")
    return output_path


def _build_margin_css(frontmatter: dict | None) -> str:
    """Build @page margin CSS with header/footer content."""
    if not frontmatter:
        return ""

    doc_type = frontmatter.get("type", "").replace("-", " ").upper()
    customer = frontmatter.get("customer", "")
    date = frontmatter.get("date", "")

    header_left = f"{doc_type}" if doc_type else ""
    header_center = f"{customer}" if customer else ""
    header_right = f"{date}" if date else ""

    css = f"""
@page {{
  size: A4;
  margin: 20mm 15mm 20mm 15mm;
  @top-left {{
    content: "{header_left}";
    font-size: 8pt;
    color: #6B7280;
  }}
  @top-center {{
    content: "{header_center}";
    font-size: 8pt;
    color: #6B7280;
  }}
  @top-right {{
    content: "{header_right}";
    font-size: 8pt;
    color: #6B7280;
  }}
  @bottom-right {{
    content: "Page " counter(page) " / " counter(pages);
    font-size: 8pt;
    color: #9CA3AF;
  }}
}}
"""
    return css
