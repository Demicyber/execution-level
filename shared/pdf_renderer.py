"""
pdf_renderer.py — HTML → PDF via WeasyPrint.

Features:
- Page header: [Doc Type] | [Customer] | [Date]    Page X/Y
- Page footer: CONFIDENTIAL for EB
- Smart pagination (handled via CSS break rules)
- A4 page size with proper margins
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
    
    # Generate page margin CSS with header/footer content
    margin_css = _build_margin_css(frontmatter)
    
    # Inject margin CSS into the HTML
    if margin_css:
        html_content = html_content.replace('</style>', f'\n{margin_css}\n</style>', 1)
    
    # Render
    try:
        html_doc = HTML(string=html_content)
        html_doc.write_pdf(output_path)
        logger.info(f"PDF generated: {output_path}")
    except Exception as e:
        logger.error(f"PDF generation failed: {e}")
        # Fallback: try without custom margins
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
    customer = frontmatter.get("customer", "")
    date = frontmatter.get("date", frontmatter.get("version", ""))
    
    # Document type labels
    type_labels = {
        "engagement-plan": "ENGAGEMENT PLAN",
        "call-plan": "CALL PLAN",
        "executive-briefing": "EXECUTIVE BRIEFING",
        "post-meeting-report": "POST-MEETING REPORT",
    }
    doc_label = type_labels.get(doc_type, "DOCUMENT")
    
    # Build header content
    header_left = f"{doc_label} | {customer}"
    if date:
        header_left += f" | {date}"
    
    # Build footer for EB
    footer_content = ""
    if doc_type == "executive-briefing":
        footer_content = "CONFIDENTIAL — For Internal Use Only"
    
    css = f'''
@page {{
  size: A4;
  margin: 20mm 18mm 20mm 18mm;
  
  @top-left {{
    content: "{header_left}";
    font-size: 9px;
    color: #6B7280;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }}
  
  @top-right {{
    content: "Page " counter(page) "/" counter(pages);
    font-size: 9px;
    color: #6B7280;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }}
  
  @bottom-center {{
    content: "{footer_content}";
    font-size: 9px;
    color: #DC2626;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }}
}}
'''
    return css
