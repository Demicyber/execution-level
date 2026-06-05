from __future__ import annotations

"""
render.py — Main entry point for the Execution-Level Document Renderer.

Usage:
    from render import render
    
    # From markdown string
    result = render(markdown_text, format="html", output_path="output.html")
    
    # From file
    result = render_file("input.md", format="pdf", output_path="output.pdf")

Supported formats: "html", "pdf", "docx"

Pipeline:
    Markdown → validate → parse → render (html/pdf/docx)
"""

import logging
import sys
from pathlib import Path

# Add shared directory to path for imports
_shared_dir = Path(__file__).parent
if str(_shared_dir) not in sys.path:
    sys.path.insert(0, str(_shared_dir))

from parse import parse_markdown, get_doc_type
from validate import validate
from html_renderer import render_html
from reportlab_renderer import render_pdf as render_pdf_reportlab
from docx_renderer import render_docx

logger = logging.getLogger(__name__)


def render(
    markdown_text: str,
    format: str = "html",
    output_path: str | None = None,
    strict: bool = False,
) -> dict:
    """Render structured markdown to the specified output format.
    
    Args:
        markdown_text: The structured markdown input (with YAML frontmatter)
        format: Output format — "html", "pdf", or "docx"
        output_path: Path to write the output file. If None, auto-generates.
        strict: If True, raise on validation errors. If False (default), continue with warnings.
        
    Returns:
        {
            "success": bool,
            "output_path": str,           # absolute path to generated file
            "format": str,
            "doc_type": str,              # e.g. "call-plan"
            "validation": {
                "valid": bool,
                "warnings": [str],
                "errors": [str],
                "auto_fixes": [str],
            },
            "html": str | None,           # HTML string (only for format="html")
            "error": str | None,          # error message if failed
        }
    """
    result = {
        "success": False,
        "output_path": None,
        "format": format,
        "doc_type": None,
        "validation": None,
        "html": None,
        "error": None,
    }
    
    try:
        # 1. Parse
        doc = parse_markdown(markdown_text)
        doc_type = get_doc_type(doc.get("frontmatter", {}))
        result["doc_type"] = doc_type
        
        # 2. Validate (+ auto-fix)
        validation = validate(doc)
        result["validation"] = {
            "valid": validation["valid"],
            "warnings": validation["warnings"],
            "errors": validation["errors"],
            "auto_fixes": validation["auto_fixes"],
        }
        
        if not validation["valid"] and strict:
            result["error"] = f"Validation failed: {'; '.join(validation['errors'])}"
            return result
        
        doc = validation["doc"]
        
        # 3. Determine output path
        if not output_path:
            ext = {"html": ".html", "pdf": ".pdf", "docx": ".docx"}.get(format, ".html")
            customer = doc["frontmatter"].get("customer", "document")
            safe_name = _safe_filename(customer)
            output_path = str(Path.cwd() / f"{safe_name}_{doc_type}{ext}")
        
        output_path = str(Path(output_path).resolve())
        
        # 4. Render
        if format == "html":
            html_content = render_html(doc)
            Path(output_path).write_text(html_content, encoding="utf-8")
            result["html"] = html_content
            
        elif format == "pdf":
            render_pdf_reportlab(doc, output_path)
            
        elif format == "docx":
            render_docx(doc, output_path)
            
        else:
            result["error"] = f"Unsupported format: {format}. Use 'html', 'pdf', or 'docx'."
            return result
        
        result["success"] = True
        result["output_path"] = output_path
        
        # Log warnings
        for w in validation.get("warnings", []):
            logger.warning(f"[{doc_type}] {w}")
        for af in validation.get("auto_fixes", []):
            logger.info(f"[{doc_type}] Auto-fix: {af}")
        
    except Exception as e:
        logger.error(f"Render failed: {e}", exc_info=True)
        result["error"] = str(e)
    
    return result


def render_file(
    input_path: str,
    format: str = "html",
    output_path: str | None = None,
    strict: bool = False,
) -> dict:
    """Render a markdown file to the specified format.
    
    Args:
        input_path: Path to the .md input file
        format: Output format — "html", "pdf", or "docx"
        output_path: Path for output. If None, uses input filename with new extension.
        strict: If True, raise on validation errors.
        
    Returns:
        Same as render()
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        return {
            "success": False,
            "output_path": None,
            "format": format,
            "doc_type": None,
            "validation": None,
            "html": None,
            "error": f"Input file not found: {input_path}",
        }
    
    markdown_text = input_path.read_text(encoding="utf-8")
    
    # Auto-generate output path from input
    if not output_path:
        ext = {"html": ".html", "pdf": ".pdf", "docx": ".docx"}.get(format, ".html")
        output_path = str(input_path.with_suffix(ext))
    
    return render(markdown_text, format=format, output_path=output_path, strict=strict)


def _safe_filename(name: str) -> str:
    """Convert a name to a safe filename."""
    import re
    # Replace unsafe chars
    safe = re.sub(r'[^\w\s-]', '', name)
    safe = re.sub(r'\s+', '_', safe).strip('_')
    return safe[:50] if safe else "document"


# ===== CLI Interface =====

def main():
    """CLI entry point for rendering."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Render structured markdown to HTML/PDF/Word",
        prog="python render.py",
    )
    parser.add_argument("input", help="Input markdown file path")
    parser.add_argument(
        "-f", "--format",
        choices=["html", "pdf", "docx"],
        default="html",
        help="Output format (default: html)",
    )
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("--strict", action="store_true", help="Fail on validation errors")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    result = render_file(
        args.input,
        format=args.format,
        output_path=args.output,
        strict=args.strict,
    )
    
    if result["success"]:
        print(f"✅ Generated: {result['output_path']}")
        if result["validation"]["warnings"]:
            print(f"⚠️  Warnings ({len(result['validation']['warnings'])}):")
            for w in result["validation"]["warnings"]:
                print(f"   - {w}")
        if result["validation"]["auto_fixes"]:
            print(f"🔧 Auto-fixes ({len(result['validation']['auto_fixes'])}):")
            for af in result["validation"]["auto_fixes"]:
                print(f"   - {af}")
    else:
        print(f"❌ Failed: {result['error']}")
        if result["validation"] and result["validation"]["errors"]:
            for e in result["validation"]["errors"]:
                print(f"   ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
