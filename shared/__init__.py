"""
Execution-Level Document Renderer — Shared rendering engine for EP, CP, EB, PMR.

Usage:
    from shared.render import render, render_file
    
    # Render markdown string
    result = render(md_text, format="html")
    
    # Render from file
    result = render_file("input.md", format="pdf", output_path="out.pdf")
"""

from .render import render, render_file
from .parse import parse_markdown
from .validate import validate
