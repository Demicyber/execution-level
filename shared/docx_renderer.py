"""
docx_renderer.py — Dict → Word document via python-docx.

Generates styled Word documents with:
- Document header (title, subtitle, meta)
- Section cards with headings
- Tables with formatting
- Stakeholder cards
- Badges as colored text
- Proper fonts and spacing for CJK content
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    from docx import Document
    from docx.shared import Inches, Pt, Cm, RGBColor, Emu
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.style import WD_STYLE_TYPE
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False


# Color mapping for badges
BADGE_COLORS = {
    # Stance
    "champion": RGBColor(0x05, 0x96, 0x69) if HAS_DOCX else None,
    "sponsor": RGBColor(0x05, 0x96, 0x69) if HAS_DOCX else None,
    "supporter": RGBColor(0x05, 0x96, 0x69) if HAS_DOCX else None,
    "neutral": RGBColor(0xD9, 0x77, 0x06) if HAS_DOCX else None,
    "non-supporter": RGBColor(0xDC, 0x26, 0x26) if HAS_DOCX else None,
    "adversary": RGBColor(0xDC, 0x26, 0x26) if HAS_DOCX else None,
    "unknown": RGBColor(0x6B, 0x72, 0x80) if HAS_DOCX else None,
    # Role
    "decision-maker": RGBColor(0x4C, 0x1D, 0x95) if HAS_DOCX else None,
    "technical-evaluator": RGBColor(0x6D, 0x28, 0xD9) if HAS_DOCX else None,
    "economic-buyer": RGBColor(0x92, 0x40, 0x0E) if HAS_DOCX else None,
    "influencer": RGBColor(0xD9, 0x77, 0x06) if HAS_DOCX else None,
    "end-user": RGBColor(0x6B, 0x72, 0x80) if HAS_DOCX else None,
    "blocker": RGBColor(0xDC, 0x26, 0x26) if HAS_DOCX else None,
    # Priority
    "high": RGBColor(0xDC, 0x26, 0x26) if HAS_DOCX else None,
    "medium": RGBColor(0xD9, 0x77, 0x06) if HAS_DOCX else None,
    "low": RGBColor(0x05, 0x96, 0x69) if HAS_DOCX else None,
    "must-meet": RGBColor(0xDC, 0x26, 0x26) if HAS_DOCX else None,
    "important": RGBColor(0xD9, 0x77, 0x06) if HAS_DOCX else None,
    "nice-to-have": RGBColor(0x05, 0x96, 0x69) if HAS_DOCX else None,
    # Result / Status
    "achieved": RGBColor(0x05, 0x96, 0x69) if HAS_DOCX else None,
    "partial": RGBColor(0xD9, 0x77, 0x06) if HAS_DOCX else None,
    "not-achieved": RGBColor(0xDC, 0x26, 0x26) if HAS_DOCX else None,
    "done": RGBColor(0x05, 0x96, 0x69) if HAS_DOCX else None,
    "next": RGBColor(0x6D, 0x28, 0xD9) if HAS_DOCX else None,
    "planned": RGBColor(0x9C, 0xA3, 0xAF) if HAS_DOCX else None,
    # Action / Gap
    "pending": RGBColor(0xD9, 0x77, 0x06) if HAS_DOCX else None,
    "in-progress": RGBColor(0x6D, 0x28, 0xD9) if HAS_DOCX else None,
    "answered": RGBColor(0x05, 0x96, 0x69) if HAS_DOCX else None,
    "unanswered": RGBColor(0xD9, 0x77, 0x06) if HAS_DOCX else None,
}

DOC_TYPE_LABELS = {
    "engagement-plan": "ENGAGEMENT PLAN",
    "call-plan": "CALL PLAN",
    "executive-briefing": "EXECUTIVE BRIEFING",
    "post-meeting-report": "POST-MEETING REPORT",
}


def render_docx(doc: dict, output_path: str) -> str:
    """Render parsed document dict to a Word .docx file.
    
    Args:
        doc: Validated document dict from parse.py
        output_path: Path to write the .docx file
        
    Returns:
        Absolute path to the generated .docx file
    """
    if not HAS_DOCX:
        raise RuntimeError(
            "python-docx is not installed. Install with: pip install python-docx"
        )
    
    output_path = str(Path(output_path).resolve())
    frontmatter = doc.get("frontmatter", {})
    sections = doc.get("sections", [])
    doc_type = frontmatter.get("type", "unknown")
    
    # Create document
    document = Document()
    
    # Set default font
    style = document.styles['Normal']
    font = style.font
    font.name = 'Segoe UI'
    font.size = Pt(11)
    
    # Set CJK font
    rPr = style.element.get_or_add_rPr()
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    rPr.append(rFonts)
    
    # EB: Confidential banner
    if doc_type == "executive-briefing":
        _add_confidential_banner(document, frontmatter)
    
    # Document header
    _add_header(document, frontmatter, doc_type)
    
    # Sections
    for section in sections:
        _add_section(document, section, doc_type)
    
    # Footer
    _add_footer(document, frontmatter, doc_type)
    
    # Save
    document.save(output_path)
    logger.info(f"DOCX generated: {output_path}")
    
    return output_path


def _add_confidential_banner(document, frontmatter):
    """Add confidential banner for EB documents."""
    classification = frontmatter.get("classification", "INTERNAL USE ONLY — AWS Confidential")
    para = document.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run(f"🔒 {classification}")
    run.bold = True
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0xDC, 0x26, 0x26)
    _set_paragraph_spacing(para, before=0, after=12)


def _add_header(document, frontmatter, doc_type):
    """Add document header."""
    doc_label = DOC_TYPE_LABELS.get(doc_type, "DOCUMENT")
    customer = frontmatter.get("customer", "")
    
    # Doc type label
    para = document.add_paragraph()
    run = para.add_run(doc_label)
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x6D, 0x28, 0xD9)
    run.bold = True
    _set_paragraph_spacing(para, before=0, after=2)
    
    # Customer title
    para = document.add_paragraph()
    run = para.add_run(customer)
    run.font.size = Pt(22)
    run.bold = True
    _set_paragraph_spacing(para, before=0, after=4)
    
    # Subtitle
    subtitle_parts = []
    if doc_type in ("call-plan", "executive-briefing", "post-meeting-report"):
        meeting_title = frontmatter.get("meeting_title", "")
        opportunity = frontmatter.get("opportunity", "")
        if meeting_title:
            subtitle_parts.append(meeting_title)
        if opportunity:
            subtitle_parts.append(opportunity)
    elif doc_type == "engagement-plan":
        opportunity = frontmatter.get("opportunity", "")
        tcv = frontmatter.get("tcv", "")
        if opportunity:
            subtitle_parts.append(opportunity)
        if tcv:
            subtitle_parts.append(f"{tcv} TCV")
    
    if subtitle_parts:
        para = document.add_paragraph()
        run = para.add_run(" · ".join(subtitle_parts))
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(0x6B, 0x72, 0x80)
        _set_paragraph_spacing(para, before=0, after=6)
    
    # Meta line
    meta_parts = []
    stage = frontmatter.get("stage", "")
    if stage:
        meta_parts.append(f"📈 {stage}")
    date = frontmatter.get("date", frontmatter.get("created", ""))
    if date:
        meta_parts.append(f"📅 {date}")
    
    if meta_parts:
        para = document.add_paragraph()
        run = para.add_run("  |  ".join(meta_parts))
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0x6B, 0x72, 0x80)
        _set_paragraph_spacing(para, before=0, after=12)
    
    # Separator
    document.add_paragraph("─" * 60)


def _add_section(document, section, doc_type):
    """Add a section to the document."""
    emoji = section.get("emoji", "")
    title = section.get("title", "")
    content_blocks = section.get("content", [])
    
    # Section heading
    heading_text = f"{emoji} {title}" if emoji else title
    heading = document.add_heading(heading_text, level=2)
    heading.runs[0].font.size = Pt(14)
    
    # Content blocks
    for block in content_blocks:
        _add_block(document, block, doc_type)


def _add_block(document, block, doc_type):
    """Add a content block to the document."""
    block_type = block.get("type", "")
    
    if block_type == "table":
        _add_table(document, block)
    elif block_type == "stakeholder_card":
        _add_stakeholder_card(document, block, doc_type)
    elif block_type == "milestone":
        _add_milestone(document, block)
    elif block_type == "objection":
        _add_objection(document, block)
    elif block_type == "eb_person":
        _add_eb_person(document, block)
    elif block_type == "subsection":
        _add_subsection(document, block, doc_type)
    elif block_type == "bullet_list":
        _add_bullet_list(document, block)
    elif block_type == "paragraph":
        _add_paragraph(document, block)
    elif block_type == "highlight":
        _add_highlight(document, block)
    elif block_type == "objective":
        _add_objective(document, block)
    elif block_type == "concern":
        _add_concern(document, block)
    elif block_type == "engagement_entry":
        _add_engagement_entry(document, block)


def _add_table(document, block):
    """Add a markdown table to the document."""
    headers = block.get("headers", [])
    rows = block.get("rows", [])
    
    if not headers:
        return
    
    table = document.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Header row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = h
        _style_cell(cell, bold=True, size=9, color=RGBColor(0x6B, 0x72, 0x80))
    
    # Data rows
    for row_idx, row in enumerate(rows):
        for col_idx, cell_text in enumerate(row):
            if col_idx < len(headers):
                cell = table.rows[row_idx + 1].cells[col_idx]
                cell.text = _strip_markdown(cell_text)
                _style_cell(cell, size=10)
    
    document.add_paragraph()  # spacing


def _add_stakeholder_card(document, block, doc_type):
    """Add a stakeholder card."""
    name = block.get("name", "")
    title = block.get("title", "")
    stance = block.get("stance", "")
    role = block.get("role", "")
    
    # Name + badges
    para = document.add_paragraph()
    run = para.add_run(f"{name}")
    run.bold = True
    run.font.size = Pt(12)
    
    if stance:
        run = para.add_run(f"  [{stance.title()}]")
        color = BADGE_COLORS.get(stance.lower())
        if color:
            run.font.color.rgb = color
        run.font.size = Pt(9)
    
    if role:
        run = para.add_run(f"  [{role.replace('-', ' ').title()}]")
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x6B, 0x72, 0x80)
    
    # Title
    if title:
        para = document.add_paragraph()
        run = para.add_run(title)
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0x6B, 0x72, 0x80)
        _set_paragraph_spacing(para, before=0, after=4)
    
    # Fields
    if doc_type == "call-plan":
        _add_field(document, "Focus", block.get("focus", ""))
        _add_field(document, "Communication", block.get("communication", ""))
        goal = block.get("our_goal", "") or block.get("how_to_win", "")
        if goal:
            _add_field(document, "🎯 Our Goal", goal, highlight=True)
    else:
        _add_field(document, "What They Care About", block.get("what_they_care_about", ""))
        _add_field(document, "What We Need", block.get("what_we_need", ""))
        win = block.get("how_to_win", "") or block.get("our_goal", "")
        if win:
            _add_field(document, "🎯 How to Win", win, highlight=True)
    
    document.add_paragraph()  # spacing


def _add_milestone(document, block):
    """Add a milestone entry."""
    number = block.get("number", 0)
    title = block.get("title", "")
    status = block.get("status", "planned")
    timeline = block.get("timeline", "")
    
    status_icons = {"done": "✓", "next": "▶", "planned": "○"}
    icon = status_icons.get(status, "○")
    
    para = document.add_paragraph()
    run = para.add_run(f"{icon} Milestone {number}: {title}")
    run.bold = True
    run.font.size = Pt(11)
    
    color = BADGE_COLORS.get(status)
    if color:
        run.font.color.rgb = color
    
    # Meta
    meta_parts = []
    if block.get("stakeholders"):
        meta_parts.append(f"👤 {block['stakeholders']}")
    if block.get("aws_resources"):
        meta_parts.append(f"🏢 {block['aws_resources']}")
    if timeline:
        meta_parts.append(f"📅 {timeline}")
    
    if meta_parts:
        para = document.add_paragraph()
        run = para.add_run("  |  ".join(meta_parts))
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x6B, 0x72, 0x80)
        _set_paragraph_spacing(para, before=0, after=8)


def _add_objection(document, block):
    """Add an objection card."""
    title = block.get("title", "")
    category = block.get("category", "")
    likely_from = block.get("likely_from", "")
    response = block.get("response", "")
    plan_b = block.get("plan_b", "")
    
    para = document.add_paragraph()
    run = para.add_run(f"⚡ {_strip_markdown(title)}")
    run.bold = True
    run.font.size = Pt(11)
    
    if category:
        run = para.add_run(f"  [{category.replace('-', ' ').title()}]")
        run.font.size = Pt(9)
        color = BADGE_COLORS.get(category.split('-')[0] if '-' in category else category)
        if color:
            run.font.color.rgb = color
    
    if likely_from:
        para = document.add_paragraph()
        run = para.add_run(f"Likely From: {likely_from}")
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(0x6B, 0x72, 0x80)
    
    if response:
        _add_field(document, "Response", response)
    if plan_b:
        _add_field(document, "Plan B", plan_b)
    
    document.add_paragraph()


def _add_eb_person(document, block):
    """Add an EB person background."""
    name = block.get("name", "")
    title = block.get("title", "")
    stance = block.get("stance", "")
    fields = block.get("fields", {})
    
    para = document.add_paragraph()
    run = para.add_run(f"{name} — {title}")
    run.bold = True
    run.font.size = Pt(12)
    
    if stance and stance != "unknown":
        run = para.add_run(f"  [{stance.title()}]")
        color = BADGE_COLORS.get(stance.lower())
        if color:
            run.font.color.rgb = color
        run.font.size = Pt(9)
    
    for label, value in fields.items():
        _add_field(document, label, _strip_provenance(value))
    
    document.add_paragraph()


def _add_subsection(document, block, doc_type):
    """Add a subsection."""
    title = block.get("title", "")
    emoji = block.get("emoji", "")
    content = block.get("content", [])
    
    prefix = f"{emoji} " if emoji else ""
    heading = document.add_heading(f"{prefix}{title}", level=3)
    heading.runs[0].font.size = Pt(12)
    
    for b in content:
        _add_block(document, b, doc_type)


def _add_bullet_list(document, block):
    """Add a bullet list."""
    for item in block.get("items", []):
        para = document.add_paragraph(style='List Bullet')
        run = para.add_run(_strip_markdown(item))
        run.font.size = Pt(10)


def _add_paragraph(document, block):
    """Add a paragraph."""
    text = block.get("text", "")
    if text:
        para = document.add_paragraph()
        run = para.add_run(_strip_markdown(text))
        run.font.size = Pt(10)


def _add_highlight(document, block):
    """Add a highlight/callout box."""
    text = block.get("text", "")
    if text:
        para = document.add_paragraph()
        run = para.add_run(_strip_markdown(text))
        run.font.size = Pt(10)
        run.bold = True


def _add_objective(document, block):
    """Add an EB objective."""
    title = block.get("title", "")
    context = block.get("context", "")
    talking_points = block.get("talking_points", [])
    ask = block.get("ask", "")
    
    para = document.add_paragraph()
    run = para.add_run(title)
    run.bold = True
    run.font.size = Pt(11)
    
    if context:
        _add_field(document, "Context", context)
    
    if talking_points and isinstance(talking_points, list):
        para = document.add_paragraph()
        run = para.add_run("Talking Points:")
        run.bold = True
        run.font.size = Pt(10)
        for tp in talking_points:
            p = document.add_paragraph(style='List Bullet')
            r = p.add_run(_strip_markdown(tp))
            r.font.size = Pt(10)
    
    if ask:
        _add_field(document, "Ask", ask, highlight=True)
    
    document.add_paragraph()


def _add_concern(document, block):
    """Add an EB concern."""
    title = block.get("title", "")
    
    para = document.add_paragraph()
    run = para.add_run(f"⚠️ {_strip_markdown(title)}")
    run.bold = True
    run.font.size = Pt(11)
    
    _add_field(document, "Acknowledge", block.get("acknowledge", ""))
    _add_field(document, "Pivot", block.get("pivot", ""))
    _add_field(document, "Elevate", block.get("elevate", ""))
    if block.get("landmine"):
        _add_field(document, "💣 Landmine", block.get("landmine", ""))
    
    document.add_paragraph()


def _add_engagement_entry(document, block):
    """Add an engagement log entry."""
    number = block.get("number", 0)
    date = block.get("date", "")
    
    para = document.add_paragraph()
    run = para.add_run(f"Engagement #{number} — {date}")
    run.bold = True
    run.font.size = Pt(11)
    
    fields = [
        ("Attendees", block.get("attendees", "")),
        ("Planned", block.get("planned", "")),
        ("Actual", block.get("actual", "")),
        ("People Updates", block.get("people_updates", "")),
        ("Key Learnings", block.get("key_learnings", "")),
        ("Plan Adjustment", block.get("plan_adjustment", "")),
    ]
    
    for label, value in fields:
        if value:
            _add_field(document, label, value)
    
    document.add_paragraph()


def _add_field(document, label, value, highlight=False):
    """Add a labeled field."""
    if not value:
        return
    para = document.add_paragraph()
    run = para.add_run(f"{label}: ")
    run.bold = True
    run.font.size = Pt(10)
    run = para.add_run(_strip_markdown(value))
    run.font.size = Pt(10)
    if highlight:
        run.font.color.rgb = RGBColor(0x6D, 0x28, 0xD9)
    _set_paragraph_spacing(para, before=0, after=2)


def _add_footer(document, frontmatter, doc_type):
    """Add document footer."""
    document.add_paragraph("─" * 60)
    
    doc_label = DOC_TYPE_LABELS.get(doc_type, "DOCUMENT")
    customer = str(frontmatter.get("customer", ""))
    date = str(frontmatter.get("date", frontmatter.get("version", "")))
    
    footer_parts = [doc_label, customer]
    if date:
        footer_parts.append(date)
    
    para = document.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run(" | ".join(footer_parts))
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x9C, 0xA3, 0xAF)
    
    para = document.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = para.add_run("Generated by Dali · Confidential")
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x9C, 0xA3, 0xAF)


def _set_paragraph_spacing(para, before=0, after=6):
    """Set paragraph spacing in points."""
    pf = para.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)


def _style_cell(cell, bold=False, size=10, color=None):
    """Style a table cell."""
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.bold = bold
            run.font.size = Pt(size)
            if color:
                run.font.color.rgb = color


def _strip_markdown(text: str) -> str:
    """Strip markdown formatting from text for Word."""
    import re
    # Remove bold markers
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    # Remove provenance labels (keep text)
    text = text.replace('[销售确认]', '').replace('[网络搜索]', '').replace('[AI推断]', '')
    # Remove badge syntax
    text = re.sub(r'\{(\w+):([\w-]+)\}', r'\2', text)
    return text.strip()


def _strip_provenance(text: str) -> str:
    """Strip provenance labels from text."""
    return text.replace('[销售确认]', '').replace('[网络搜索]', '').replace('[AI推断]', '').strip()
