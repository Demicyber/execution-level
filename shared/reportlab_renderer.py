from __future__ import annotations

"""
reportlab_renderer.py — Dict -> PDF via ReportLab (direct, no HTML intermediate).

Design: MD3 Purple (#6D28D9) + white background + print-friendly.
Font: Noto Sans SC (with STHeiti fallback for macOS dev).
Badge style: outline (white/light bg + colored border + colored text).
"""

import os
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable,
)
from reportlab.platypus.flowables import Flowable

from parse import extract_provenance, get_doc_type


# ===== Color Palette (MD3 Purple) =====
class C:
    PRIMARY = colors.HexColor("#6D28D9")
    PRIMARY_LIGHT = colors.HexColor("#EDE9FE")
    PRIMARY_DARK = colors.HexColor("#4C1D95")
    WHITE = colors.white
    BG = colors.white
    BG_SUBTLE = colors.HexColor("#F9FAFB")
    BORDER = colors.HexColor("#E5E7EB")
    BORDER_LIGHT = colors.HexColor("#F3F4F6")
    TEXT = colors.HexColor("#111827")
    TEXT_SEC = colors.HexColor("#374151")
    TEXT_MUTED = colors.HexColor("#6B7280")

    CHAMPION = colors.HexColor("#059669")
    SUPPORTER = colors.HexColor("#059669")
    NEUTRAL = colors.HexColor("#D97706")
    NON_SUPPORTER = colors.HexColor("#DC2626")
    UNKNOWN = colors.HexColor("#6B7280")

    ACHIEVED = colors.HexColor("#059669")
    PARTIAL = colors.HexColor("#D97706")
    NOT_ACHIEVED = colors.HexColor("#DC2626")

    HIGH = colors.HexColor("#DC2626")
    MEDIUM = colors.HexColor("#D97706")
    LOW = colors.HexColor("#059669")

    RISK_TRUST = colors.HexColor("#DC2626")
    CAPABILITY = colors.HexColor("#EA580C")
    AUTHORITY = colors.HexColor("#D97706")
    PRICE_VALUE = colors.HexColor("#6D28D9")
    STATUS_QUO = colors.HexColor("#6B7280")


# Badge color mapping
BADGE_COLORS = {
    "sponsor": (C.CHAMPION, colors.HexColor("#ECFDF5")),
    "champion": (C.CHAMPION, colors.HexColor("#ECFDF5")),
    "supporter": (C.SUPPORTER, colors.HexColor("#ECFDF5")),
    "neutral": (C.NEUTRAL, colors.HexColor("#FFFBEB")),
    "non-supporter": (C.NON_SUPPORTER, colors.HexColor("#FEF2F2")),
    "adversary": (C.NON_SUPPORTER, colors.HexColor("#FEF2F2")),
    "unknown": (C.UNKNOWN, C.BG_SUBTLE),
    "decision-maker": (C.PRIMARY_DARK, C.PRIMARY_LIGHT),
    "technical-evaluator": (C.PRIMARY, C.PRIMARY_LIGHT),
    "economic-buyer": (colors.HexColor("#92400E"), colors.HexColor("#FEF3C7")),
    "influencer": (C.NEUTRAL, colors.HexColor("#FFFBEB")),
    "high": (C.HIGH, colors.HexColor("#FEF2F2")),
    "medium": (C.MEDIUM, colors.HexColor("#FFFBEB")),
    "low": (C.LOW, colors.HexColor("#ECFDF5")),
    "must-meet": (C.HIGH, colors.HexColor("#FEF2F2")),
    "important": (C.MEDIUM, colors.HexColor("#FFFBEB")),
    "nice-to-have": (C.LOW, colors.HexColor("#ECFDF5")),
    "achieved": (C.ACHIEVED, colors.HexColor("#ECFDF5")),
    "partial": (C.PARTIAL, colors.HexColor("#FFFBEB")),
    "not-achieved": (C.NOT_ACHIEVED, colors.HexColor("#FEF2F2")),
    "done": (C.ACHIEVED, colors.HexColor("#ECFDF5")),
    "next": (C.PRIMARY, C.PRIMARY_LIGHT),
    "planned": (C.TEXT_SEC, C.BG_SUBTLE),
    "answered": (C.ACHIEVED, colors.HexColor("#ECFDF5")),
    "unanswered": (C.NEUTRAL, colors.HexColor("#FFFBEB")),
    "pending": (C.NEUTRAL, colors.HexColor("#FFFBEB")),
    "in-progress": (C.PRIMARY, C.PRIMARY_LIGHT),
}

CATEGORY_COLORS = {
    "risk-trust": C.RISK_TRUST,
    "risk/trust": C.RISK_TRUST,
    "capability": C.CAPABILITY,
    "authority": C.AUTHORITY,
    "price-value": C.PRICE_VALUE,
    "price/competition": C.PRICE_VALUE,
    "status-quo": C.STATUS_QUO,
    "status quo": C.STATUS_QUO,
}

DOC_TYPE_LABELS = {
    "engagement-plan": "ENGAGEMENT PLAN",
    "call-plan": "CALL PLAN",
    "executive-briefing": "EXECUTIVE BRIEFING",
    "post-meeting-report": "POST-MEETING REPORT",
}


# ===== Font Registration =====
def _register_fonts():
    """Register CJK fonts. Try Noto Sans SC first, fallback to STHeiti."""
    font_dir = Path(__file__).parent / "fonts"

    # Try Noto Sans SC (bundled)
    noto_regular = font_dir / "NotoSansSC-Regular.ttf"
    noto_bold = font_dir / "NotoSansSC-Bold.ttf"

    if noto_regular.exists():
        pdfmetrics.registerFont(TTFont("CJK", str(noto_regular)))
        if noto_bold.exists():
            pdfmetrics.registerFont(TTFont("CJK-Bold", str(noto_bold)))
        else:
            pdfmetrics.registerFont(TTFont("CJK-Bold", str(noto_regular)))
        return

    # Fallback: STHeiti (macOS)
    st_heiti = "/System/Library/Fonts/STHeiti Medium.ttc"
    st_heiti_light = "/System/Library/Fonts/STHeiti Light.ttc"
    if os.path.exists(st_heiti):
        pdfmetrics.registerFont(TTFont("CJK", st_heiti, subfontIndex=0))
        pdfmetrics.registerFont(TTFont("CJK-Bold", st_heiti, subfontIndex=0))
        return

    # Last resort: alias Helvetica (no CJK support but won't crash)
    from reportlab.pdfbase.pdfmetrics import registerFontFamily
    from reportlab.lib.fonts import addMapping
    addMapping("CJK", 0, 0, "Helvetica")
    addMapping("CJK", 1, 0, "Helvetica-Bold")
    addMapping("CJK-Bold", 0, 0, "Helvetica-Bold")
    addMapping("CJK-Bold", 1, 0, "Helvetica-Bold")


_register_fonts()

# ===== Styles =====
FONT = "CJK"
FONT_BOLD = "CJK-Bold"

PAGE_W, PAGE_H = A4
MARGIN_L = 18 * mm
MARGIN_R = 18 * mm
MARGIN_T = 20 * mm
MARGIN_B = 18 * mm
CONTENT_W = PAGE_W - MARGIN_L - MARGIN_R


def _styles():
    """Build paragraph styles."""
    s = {}
    s["title"] = ParagraphStyle("title", fontName=FONT_BOLD, fontSize=18, leading=22, textColor=C.PRIMARY_DARK)
    s["subtitle"] = ParagraphStyle("subtitle", fontName=FONT, fontSize=10, leading=13, textColor=C.TEXT_SEC)
    s["doc_type"] = ParagraphStyle("doc_type", fontName=FONT_BOLD, fontSize=8, leading=10, textColor=C.PRIMARY, spaceAfter=1)
    s["section_header"] = ParagraphStyle("section_header", fontName=FONT_BOLD, fontSize=11, leading=14, textColor=C.PRIMARY_DARK, spaceBefore=8, spaceAfter=2)
    s["sub_heading"] = ParagraphStyle("sub_heading", fontName=FONT_BOLD, fontSize=9.5, leading=13, textColor=C.TEXT, spaceBefore=6, spaceAfter=2)
    s["body"] = ParagraphStyle("body", fontName=FONT, fontSize=9, leading=12, textColor=C.TEXT)
    s["body_small"] = ParagraphStyle("body_small", fontName=FONT, fontSize=8, leading=11, textColor=C.TEXT_SEC)
    s["bullet"] = ParagraphStyle("bullet", fontName=FONT, fontSize=9, leading=12, textColor=C.TEXT, leftIndent=10, bulletIndent=3, bulletFontName=FONT, bulletFontSize=9)
    s["field_label"] = ParagraphStyle("field_label", fontName=FONT_BOLD, fontSize=8, leading=11, textColor=C.TEXT_SEC)
    s["field_value"] = ParagraphStyle("field_value", fontName=FONT, fontSize=9, leading=12, textColor=C.TEXT, leftIndent=0)
    s["footer"] = ParagraphStyle("footer", fontName=FONT, fontSize=7, leading=10, textColor=C.TEXT_MUTED, alignment=TA_CENTER)
    s["highlight"] = ParagraphStyle("highlight", fontName=FONT, fontSize=9, leading=12, textColor=C.PRIMARY_DARK, leftIndent=6)
    s["meta"] = ParagraphStyle("meta", fontName=FONT, fontSize=8, leading=11, textColor=C.TEXT_SEC)
    return s


STYLES = _styles()


# ===== Main Render Function =====
def render_pdf(doc: dict, output_path: str) -> str:
    """Render validated document dict directly to PDF.

    Args:
        doc: Parsed and validated document dict (from parse+validate)
        output_path: Path to write the PDF

    Returns:
        Absolute path to generated PDF
    """
    output_path = str(Path(output_path).resolve())
    frontmatter = doc.get("frontmatter", {})
    sections = doc.get("sections", [])
    doc_type = get_doc_type(frontmatter)

    # Build flowables
    story = []

    # Header
    story.extend(_build_header(frontmatter, doc_type))


    # Collect milestones for EP progress bar (rendered inside Opportunity Snapshot)
    ep_milestones = []
    if doc_type == "engagement-plan":
        for section in sections:
            for block in section.get("content", []):
                if block.get("type") == "milestone":
                    ep_milestones.append(block)
            if not ep_milestones and _is_roadmap_section(section.get("title", "")):
                ep_milestones = _extract_milestones_from_table(section.get("content", []))

    # Sections
    for i, section in enumerate(sections, 1):
        section_flowables = _build_section(section, doc_type, i, ep_milestones=ep_milestones)
        story.extend(section_flowables)

    # Footer spacer
    story.append(Spacer(1, 8 * mm))

    # Build PDF
    pdf_doc = BaseDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN_L,
        rightMargin=MARGIN_R,
        topMargin=MARGIN_T,
        bottomMargin=MARGIN_B,
    )

    frame = Frame(MARGIN_L, MARGIN_B, CONTENT_W, PAGE_H - MARGIN_T - MARGIN_B, id="main")
    template = PageTemplate(id="main", frames=[frame], onPage=lambda c, d: _draw_page_chrome(c, d, frontmatter, doc_type))
    pdf_doc.addPageTemplates([template])

    pdf_doc.build(story)
    return output_path


# ===== Page Chrome (Header/Footer on every page) =====
def _draw_page_chrome(canvas, doc, frontmatter, doc_type):
    """Draw page header and footer on every page."""
    canvas.saveState()

    # Header line
    doc_label = DOC_TYPE_LABELS.get(doc_type, "DOCUMENT")
    customer = frontmatter.get("customer", "")
    date = frontmatter.get("date", frontmatter.get("version", ""))
    header_text = f"{doc_label}  |  {customer}"
    if date:
        header_text += f"  |  {date}"

    canvas.setFont(FONT, 7)
    canvas.setFillColor(C.TEXT_MUTED)
    canvas.drawString(MARGIN_L, PAGE_H - 12 * mm, header_text)

    page_num = f"Page {doc.page}"
    canvas.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 12 * mm, page_num)

    # Header rule
    canvas.setStrokeColor(C.BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN_L, PAGE_H - 14 * mm, PAGE_W - MARGIN_R, PAGE_H - 14 * mm)


    canvas.restoreState()


# ===== Header =====
def _build_header(frontmatter: dict, doc_type: str) -> list:
    """Build document header flowables."""
    elements = []

    doc_label = DOC_TYPE_LABELS.get(doc_type, "DOCUMENT")

    # TCV badge (top-right) for EP
    tcv = frontmatter.get("tcv", "")
    if tcv and doc_type == "engagement-plan":
        label_para = Paragraph(doc_label, STYLES["doc_type"])
        tcv_style = ParagraphStyle("tcv_badge", fontName=FONT_BOLD, fontSize=9, leading=12,
                                   textColor=C.PRIMARY_DARK, alignment=TA_RIGHT)
        tcv_para = Paragraph(f"<b>{_esc(tcv)}</b> TCV", tcv_style)
        badge_row = Table([[label_para, tcv_para]], colWidths=[CONTENT_W * 0.6, CONTENT_W * 0.4])
        badge_row.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ]))
        elements.append(badge_row)
    else:
        elements.append(Paragraph(doc_label, STYLES["doc_type"]))

    customer = frontmatter.get("customer", "")
    elements.append(Paragraph(_esc(customer), STYLES["title"]))

    # Subtitle
    subtitle_parts = []
    if doc_type in ("call-plan", "executive-briefing", "post-meeting-report"):
        mt = frontmatter.get("meeting_title", "")
        opp = frontmatter.get("opportunity", "")
        if mt:
            subtitle_parts.append(mt)
        elif opp:
            subtitle_parts.append(opp)
    elif doc_type == "engagement-plan":
        opp = frontmatter.get("opportunity", "")
        if opp:
            subtitle_parts.append(opp)

    if subtitle_parts:
        elements.append(Paragraph(_esc("  |  ".join(subtitle_parts)), STYLES["subtitle"]))

    # Meta line
    meta_parts = []
    stage = frontmatter.get("stage", "")
    if stage:
        target = frontmatter.get("stage_target", "")
        if target:
            meta_parts.append(f"Stage: {stage} → {target}")
        else:
            meta_parts.append(f"Stage: {stage}")

    date = frontmatter.get("date", "")
    time_val = frontmatter.get("time", "")
    if date:
        meta_parts.append(f"{date} {time_val}".strip())

    location = frontmatter.get("location", frontmatter.get("format", ""))
    if location:
        meta_parts.append(location)

    recorded_by = frontmatter.get("recorded_by", "")
    if recorded_by:
        meta_parts.append(f"Recorded by: {recorded_by}")

    if meta_parts:
        elements.append(Spacer(1, 1.5 * mm))
        elements.append(Paragraph(_esc(" · ".join(meta_parts)), STYLES["meta"]))

    # Header rule
    elements.append(Spacer(1, 2.5 * mm))
    elements.append(HRFlowable(width="100%", thickness=2, color=C.PRIMARY, spaceBefore=0, spaceAfter=3 * mm))

    return elements



# ===== Section Builder =====
def _build_section(section: dict, doc_type: str, num: int, ep_milestones: list = None) -> list:
    """Build flowables for one section."""
    title = section.get("title", "")
    content_blocks = section.get("content", [])

    elements = []

    # Section header with numbered circle (MD3 style)
    num_circle = _section_number_circle(num)
    title_para = Paragraph(f"<b>{_esc(title)}</b>", STYLES["section_header"])
    header_table = Table(
        [[num_circle, title_para]],
        colWidths=[8 * mm, CONTENT_W - 8 * mm],
    )
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    elements.append(Spacer(1, 3 * mm))
    elements.append(header_table)
    elements.append(HRFlowable(width="100%", thickness=1, color=C.PRIMARY, spaceBefore=2, spaceAfter=2.5 * mm))

    # Check if this is the Engagement Roadmap section (contains milestones)
    milestones = [b for b in content_blocks if b.get("type") == "milestone"]
    if not milestones and _is_roadmap_section(title):
        milestones = _extract_milestones_from_table(content_blocks)
    if milestones and _is_roadmap_section(title):
        elements.extend(_build_roadmap_visual(milestones))
        for block in content_blocks:
            if block.get("type") not in ("milestone", "table"):
                elements.extend(_build_block(block, doc_type))
    else:
        for block in content_blocks:
            block_elements = _build_block(block, doc_type)
            elements.extend(block_elements)

    # Engagement Progress bar goes at end of Opportunity Snapshot section
    if ep_milestones and _is_snapshot_section(title):
        elements.append(Spacer(1, 2 * mm))
        elements.append(_ProgressBar(ep_milestones))

    elements.append(Spacer(1, 2 * mm))
    return elements


def _is_roadmap_section(title: str) -> bool:
    """Detect if a section title is the engagement roadmap."""
    t = title.lower()
    return "roadmap" in t or "engagement roadmap" in t


def _is_snapshot_section(title: str) -> bool:
    """Detect if a section title is the Opportunity Snapshot."""
    t = title.lower()
    return "opportunity snapshot" in t or "snapshot" in t


def _extract_milestones_from_table(content_blocks: list) -> list:
    """Convert roadmap table rows into milestone dicts for the visual renderer.

    Table columns: #, Milestone, Key Stakeholders, AWS Team, Status
    """
    milestones = []
    for block in content_blocks:
        if block.get("type") != "table":
            continue
        headers = [h.lower().strip() for h in block.get("headers", [])]
        if not any("milestone" in h for h in headers):
            continue
        for row in block.get("rows", []):
            row_dict = dict(zip(headers, row))
            number_str = row_dict.get("#", "0")
            try:
                number = int(re.sub(r'\D', '', str(number_str)) or "0")
            except ValueError:
                number = 0
            status_raw = row_dict.get("status", "planned").lower().strip()
            status_raw = re.sub(r'[*↓]', '', status_raw).strip()
            milestones.append({
                "type": "milestone",
                "number": number,
                "title": row_dict.get("milestone", ""),
                "status": status_raw,
                "stakeholders": row_dict.get("key stakeholders", ""),
                "aws_resources": row_dict.get("aws team", ""),
                "timeline": "",
                "exit_criteria": "",
                "fields": {},
            })
    return milestones


class _NumberCircle(Flowable):
    """MD3-style numbered circle for section headers."""

    def __init__(self, number, size=6 * mm):
        Flowable.__init__(self)
        self.number = number
        self.size = size
        self.width = size
        self.height = size

    def draw(self):
        self.canv.saveState()
        self.canv.setFillColor(C.PRIMARY)
        r = self.size / 2
        self.canv.circle(r, r, r, fill=1, stroke=0)
        self.canv.setFillColor(C.WHITE)
        self.canv.setFont(FONT_BOLD, 7)
        self.canv.drawCentredString(r, r - 2.5, str(self.number))
        self.canv.restoreState()


def _section_number_circle(num: int) -> _NumberCircle:
    return _NumberCircle(num)


# ===== Engagement Progress Bar =====
class _ProgressBar(Flowable):
    """Horizontal step indicator: green circles (done) → purple (current) → gray (future)."""

    def __init__(self, milestones, width=CONTENT_W, height=20 * mm):
        Flowable.__init__(self)
        self.milestones = milestones
        self.width = width
        self.height = height

    def draw(self):
        c = self.canv
        c.saveState()

        n = len(self.milestones)
        if n == 0:
            c.restoreState()
            return

        circle_r = 3.2 * mm
        label_y = 4 * mm
        circle_y = label_y + 5.5 * mm + circle_r
        line_y = circle_y

        # Compute horizontal positions
        margin = 12 * mm
        usable = self.width - 2 * margin
        step = usable / max(n - 1, 1) if n > 1 else 0
        positions = [margin + i * step for i in range(n)]

        # Find current index
        current_idx = 0
        for i, m in enumerate(self.milestones):
            s = m.get("status", "").lower()
            if s in ("next", "current", "in-progress"):
                current_idx = i
                break
            elif s == "done":
                current_idx = i + 1

        # Draw connecting line (gray base)
        c.setStrokeColor(C.BORDER)
        c.setLineWidth(2)
        c.line(positions[0], line_y, positions[-1], line_y)

        # Draw completed portion (purple)
        if current_idx > 0:
            c.setStrokeColor(C.PRIMARY)
            c.setLineWidth(2.5)
            end_x = positions[min(current_idx, n - 1)]
            if current_idx < n:
                end_x = (positions[current_idx - 1] + positions[current_idx]) / 2
            c.line(positions[0], line_y, end_x, line_y)

        # Draw circles and labels
        for i, m in enumerate(self.milestones):
            x = positions[i]
            s = m.get("status", "").lower()

            if s == "done":
                # Green filled circle with checkmark
                c.setFillColor(colors.HexColor("#386A20"))
                c.circle(x, circle_y, circle_r, fill=1, stroke=0)
                c.setFillColor(C.WHITE)
                c.setFont(FONT_BOLD, 7)
                c.drawCentredString(x, circle_y - 2.5, "✓")
            elif s in ("next", "current", "in-progress"):
                # Purple outlined circle with number
                c.setFillColor(colors.HexColor("#EDE9FE"))
                c.setStrokeColor(C.PRIMARY)
                c.setLineWidth(1.5)
                c.circle(x, circle_y, circle_r, fill=1, stroke=1)
                c.setFillColor(C.PRIMARY)
                c.setFont(FONT_BOLD, 7)
                c.drawCentredString(x, circle_y - 2.5, str(m.get("number", i + 1)))
            else:
                # Gray circle with number
                c.setFillColor(C.BG_SUBTLE)
                c.setStrokeColor(C.TEXT_MUTED)
                c.setLineWidth(0.5)
                c.circle(x, circle_y, circle_r, fill=1, stroke=1)
                c.setFillColor(C.TEXT_MUTED)
                c.setFont(FONT, 6)
                c.drawCentredString(x, circle_y - 2, str(m.get("number", i + 1)))

            # Label below
            label = m.get("title", "")
            max_chars = max(10, int(step / (1.8 * mm))) if step > 0 else 16
            if len(label) > max_chars:
                label = label[:max_chars - 1] + ".."
            c.setFillColor(C.TEXT_SEC if s != "done" else colors.HexColor("#386A20"))
            c.setFont(FONT, 5.5)
            c.drawCentredString(x, label_y, label)

            # "Current" label for active step
            if s in ("next", "current", "in-progress"):
                c.setFillColor(C.PRIMARY)
                c.setFont(FONT_BOLD, 5)
                c.drawCentredString(x, 0.5 * mm, "Current")

        c.restoreState()


# ===== Engagement Roadmap Visual =====
def _build_roadmap_visual(milestones: list) -> list:
    """Build the vertical timeline roadmap."""
    elements = []

    # Counter badge: "X/N Stations Complete"
    done_count = sum(1 for m in milestones if m.get("status", "").lower() == "done")
    total = len(milestones)
    counter_text = f"<b>{done_count}/{total}</b> Stations Complete"
    elements.append(Paragraph(counter_text, ParagraphStyle(
        "counter", fontName=FONT, fontSize=8, leading=10, textColor=C.TEXT_SEC, alignment=TA_RIGHT
    )))
    elements.append(Spacer(1, 2 * mm))

    # Vertical timeline cards
    for m in milestones:
        elements.extend(_build_roadmap_card(m))

    return elements


def _build_roadmap_card(milestone: dict) -> list:
    """Build a single roadmap milestone card with numbered circle + left border."""
    number = milestone.get("number", 0)
    title = milestone.get("title", "")
    status = milestone.get("status", "planned").lower().strip()
    fields = milestone.get("fields", {})

    # Status indicator
    if status == "done":
        indicator_color = colors.HexColor("#386A20")
        indicator_text = "✓ Done"
        indicator_fg = colors.HexColor("#386A20")
        circle_label = "✓"
    elif status in ("next", "current", "in-progress"):
        indicator_color = C.PRIMARY
        indicator_text = "▶ Next"
        indicator_fg = C.PRIMARY
        circle_label = str(number)
    else:
        indicator_color = C.TEXT_MUTED
        indicator_text = "Planned"
        indicator_fg = C.TEXT_MUTED
        circle_label = str(number)

    # Build card content
    parts = []

    # Title + status badge on same row
    title_style = ParagraphStyle("rm_title", fontName=FONT_BOLD, fontSize=9, leading=12, textColor=C.TEXT)
    status_style = ParagraphStyle("rm_status", fontName=FONT_BOLD, fontSize=7, leading=10, textColor=indicator_fg, alignment=TA_RIGHT)
    title_row = Table(
        [[Paragraph(_esc(title), title_style), Paragraph(indicator_text, status_style)]],
        colWidths=[CONTENT_W - 34 * mm, 22 * mm]
    )
    title_row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    parts.append(title_row)

    # Meta tags row (stakeholders, aws team, timeline)
    meta_tags = []
    stakeholders = (milestone.get("stakeholders", "") or
                    fields.get("Stakeholders", "") or fields.get("👤 Stakeholders", ""))
    aws_team = (milestone.get("aws_resources", "") or
                fields.get("AWS Team", "") or fields.get("🏢 AWS Resources", "") or
                fields.get("AWS Resources", ""))
    timeline = (milestone.get("timeline", "") or
                fields.get("Timeline", "") or fields.get("📅 Timeline", ""))

    if stakeholders:
        meta_tags.append(f"👤 {stakeholders}")
    if aws_team:
        meta_tags.append(f"☁ {aws_team}")
    if timeline:
        meta_tags.append(f"📅 {timeline}")

    if meta_tags:
        meta_text = "    ".join(meta_tags)
        parts.append(Paragraph(_esc(meta_text), ParagraphStyle(
            "rm_meta", fontName=FONT, fontSize=7, leading=10, textColor=C.TEXT_SEC
        )))

    # Wrap card content in inner table
    card_inner_data = [[p] for p in parts]
    card_inner = Table(card_inner_data, colWidths=[CONTENT_W - 16 * mm])
    card_inner.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, C.BORDER),
        ("LINEBEFORE", (0, 0), (0, -1), 3, indicator_color),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))

    # Numbered circle on left
    circle = _RoadmapCircle(circle_label, indicator_color)

    # Compose: [circle | card]
    outer = Table([[circle, card_inner]], colWidths=[8 * mm, CONTENT_W - 8 * mm])
    outer.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))

    return [KeepTogether([outer]), Spacer(1, 1.5 * mm)]


class _RoadmapCircle(Flowable):
    """Small numbered circle for roadmap timeline."""

    def __init__(self, label, color, size=5.5 * mm):
        Flowable.__init__(self)
        self.label = label
        self.color = color
        self.size = size
        self.width = size
        self.height = size

    def draw(self):
        c = self.canv
        c.saveState()
        r = self.size / 2
        c.setFillColor(self.color)
        c.circle(r, r, r, fill=1, stroke=0)
        c.setFillColor(C.WHITE)
        c.setFont(FONT_BOLD, 6.5)
        c.drawCentredString(r, r - 2.2, self.label)
        c.restoreState()


# ===== Block Router =====
def _build_block(block: dict, doc_type: str) -> list:
    block_type = block.get("type", "")

    if block_type == "table":
        return _build_table(block)
    elif block_type == "stakeholder_card":
        return _build_stakeholder(block, doc_type)
    elif block_type == "milestone":
        return _build_milestone(block)
    elif block_type == "objection":
        return _build_objection(block)
    elif block_type == "eb_person":
        return _build_eb_person(block)
    elif block_type == "subsection":
        return _build_subsection(block, doc_type)
    elif block_type == "subsubsection":
        return _build_subsubsection(block, doc_type)
    elif block_type == "objective":
        return _build_objective(block)
    elif block_type == "concern":
        return _build_concern(block)
    elif block_type == "engagement_entry":
        return _build_engagement_entry(block)
    elif block_type == "bullet_list":
        return _build_bullets(block)
    elif block_type == "paragraph":
        return [Paragraph(_esc(block.get("text", "")), STYLES["body"]), Spacer(1, 2 * mm)]
    elif block_type == "highlight":
        return _build_highlight(block)
    else:
        return [Paragraph(_esc(str(block)), STYLES["body_small"])]


# ===== Table =====
def _build_table(block: dict) -> list:
    headers = block.get("headers", [])
    rows = block.get("rows", [])

    if not headers and not rows:
        return []

    # Build data
    data = []
    if headers:
        data.append([Paragraph(f"<b>{_esc(h)}</b>", ParagraphStyle("th", fontName=FONT_BOLD, fontSize=8, leading=11, textColor=C.TEXT_SEC)) for h in headers])

    for row in rows:
        data.append([_render_cell(cell) for cell in row])

    if not data:
        return []

    col_count = len(data[0])
    col_widths = _calc_col_widths(headers, rows, col_count)

    t = Table(data, colWidths=col_widths, repeatRows=1 if headers else 0)

    style_cmds = [
        ("FONTNAME", (0, 0), (-1, -1), FONT),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (-1, -1), C.TEXT),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]

    if headers:
        style_cmds.extend([
            ("LINEABOVE", (0, 0), (-1, 0), 1.5, C.PRIMARY),
            ("LINEBELOW", (0, 0), (-1, 0), 0.75, C.BORDER),
            ("TEXTCOLOR", (0, 0), (-1, 0), C.TEXT_SEC),
            ("FONTNAME", (0, 0), (-1, 0), FONT_BOLD),
            ("FONTSIZE", (0, 0), (-1, 0), 8),
        ])

    # Alternating row background
    for i in range(1 if headers else 0, len(data)):
        if i % 2 == 0:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), C.BG_SUBTLE))

    # Bottom rule
    style_cmds.append(("LINEBELOW", (0, -1), (-1, -1), 0.5, C.BORDER))

    t.setStyle(TableStyle(style_cmds))
    return [t, Spacer(1, 2.5 * mm)]


def _calc_col_widths(headers: list, rows: list, col_count: int) -> list:
    """Calculate proportional column widths based on content length."""
    max_lengths = [0] * col_count
    for row in ([headers] if headers else []) + rows:
        for i, cell in enumerate(row[:col_count]):
            max_lengths[i] = max(max_lengths[i], len(str(cell)))

    # Apply min/max constraints and proportional scaling
    min_col = 18 * mm
    total = sum(max_lengths) or 1
    widths = []
    for length in max_lengths:
        w = max(min_col, (length / total) * CONTENT_W)
        widths.append(w)

    # Normalize to fit CONTENT_W exactly
    scale = CONTENT_W / sum(widths)
    return [w * scale for w in widths]


def _render_cell(cell: str) -> Paragraph:
    """Render a table cell, applying badge styling for known values."""
    cell_lower = cell.lower().strip()

    if cell_lower in BADGE_COLORS:
        fg, bg = BADGE_COLORS[cell_lower]
        label = cell.strip().title()
        style = ParagraphStyle("badge_cell", fontName=FONT_BOLD, fontSize=8, leading=10, textColor=fg)
        return Paragraph(f"{_esc(label)}", style)

    return Paragraph(_esc(cell), ParagraphStyle("cell", fontName=FONT, fontSize=9, leading=12, textColor=C.TEXT))


# ===== Stakeholder Card =====
def _build_stakeholder(block: dict, doc_type: str) -> list:
    name = block.get("name", "")
    title = block.get("title", "")
    stance = block.get("stance", "unknown").lower().strip()
    role = block.get("role", "").lower().strip()

    elements = []

    # Determine card border color from stance
    stance_color = BADGE_COLORS.get(stance, (C.PRIMARY, C.PRIMARY_LIGHT))[0]

    # Name + pill badges
    badge_text = ""
    if stance in BADGE_COLORS:
        fg, bg = BADGE_COLORS[stance]
        badge_text += f' <font color="{fg.hexval()}" size="7">[{stance.title()}]</font>'
    if role and role != stance and role in BADGE_COLORS:
        fg, bg = BADGE_COLORS[role]
        badge_text += f' <font color="{fg.hexval()}" size="7">[{role.replace("-", " ").title()}]</font>'

    name_para = Paragraph(f"<b>{_esc(name)}</b> — {_esc(title)}{badge_text}", STYLES["body"])

    # Fields
    field_paras = []
    if doc_type == "call-plan":
        for key, label in [("focus", "Focus"), ("communication", "Communication"), ("our_goal", "Our Goal")]:
            val = block.get(key, "") or (block.get("how_to_win", "") if key == "our_goal" else "")
            if val:
                field_paras.append(Paragraph(f"<b>{label}:</b> {_inline(val)}", STYLES["body_small"]))
    else:
        for key, label in [("what_they_care_about", "What They Care About"), ("what_we_need", "What We Need"), ("how_to_win", "How to Win")]:
            val = block.get(key, "") or (block.get("our_goal", "") if key == "how_to_win" else "")
            if val:
                field_paras.append(Paragraph(f"<b>{label}:</b> {_inline(val)}", STYLES["body_small"]))

    # Left-bordered card (MD3 match-tile style)
    card_content = [[name_para]] + [[p] for p in field_paras]
    card_table = Table(card_content, colWidths=[CONTENT_W - 4 * mm])
    style_cmds = [
        ("BOX", (0, 0), (-1, -1), 0.5, C.BORDER),
        ("LINEBEFORE", (0, 0), (0, -1), 3, stance_color),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 0), (-1, 0), C.BG_SUBTLE),
    ]
    if len(card_content) > 1:
        style_cmds.append(("LINEBELOW", (0, 0), (-1, 0), 0.5, C.BORDER))
    card_table.setStyle(TableStyle(style_cmds))

    elements.append(KeepTogether([card_table]))
    elements.append(Spacer(1, 1.5 * mm))
    return elements


# ===== Milestone =====
def _build_milestone(block: dict) -> list:
    number = block.get("number", 0)
    title = block.get("title", "")
    status = block.get("status", "planned").lower().strip()
    stakeholders = block.get("stakeholders", "")
    timeline = block.get("timeline", "")

    marker = {"done": "✓", "next": "▶"}.get(status, str(number))
    fg, bg = BADGE_COLORS.get(status, (C.TEXT_SEC, C.BG_SUBTLE))

    line = f'<font color="{fg.hexval()}"><b>{marker}</b></font>  <b>{_esc(title)}</b>'
    meta = []
    if stakeholders:
        meta.append(stakeholders)
    if timeline:
        meta.append(timeline)
    if meta:
        line += f'  <font color="{C.TEXT_SEC.hexval()}" size="8">{", ".join(_esc(m) for m in meta)}</font>'

    return [Paragraph(line, STYLES["body"]), Spacer(1, 1.5 * mm)]


# ===== Objection =====
def _build_objection(block: dict) -> list:
    title = block.get("title", "")
    category = block.get("category", "").lower().strip()
    likely_from = block.get("likely_from", "")
    response = block.get("response", "")
    plan_b = block.get("plan_b", "")

    cat_color = CATEGORY_COLORS.get(category, C.TEXT_SEC)
    cat_label = category.replace("-", "/").upper() if category else ""

    parts = []
    header = f'<b>{_esc(title)}</b>'
    if cat_label:
        header += f'  <font color="{cat_color.hexval()}" size="7">[{cat_label}]</font>'
    parts.append(Paragraph(header, STYLES["body"]))

    if likely_from:
        parts.append(Paragraph(f"<i>Likely from: {_esc(likely_from)}</i>", STYLES["body_small"]))
    if response:
        parts.append(Paragraph(f"<b>Response:</b> {_esc(response)}", STYLES["body_small"]))
    if plan_b:
        parts.append(Paragraph(f"<b>Plan B:</b> {_esc(plan_b)}", STYLES["body_small"]))

    # Card with colored left border + header background
    card_data = [[p] for p in parts]
    card = Table(card_data, colWidths=[CONTENT_W - 4 * mm])
    style_cmds = [
        ("BOX", (0, 0), (-1, -1), 0.5, C.BORDER),
        ("LINEBEFORE", (0, 0), (0, -1), 3, cat_color),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 0), (-1, 0), C.BG_SUBTLE),
    ]
    card.setStyle(TableStyle(style_cmds))

    return [KeepTogether([card]), Spacer(1, 1.5 * mm)]


# ===== EB Person =====
def _build_eb_person(block: dict) -> list:
    name = block.get("name", "")
    title = block.get("title", "")
    stance = block.get("stance", "unknown").lower().strip()
    fields = block.get("fields", {})

    stance_color = BADGE_COLORS.get(stance, (C.PRIMARY, C.PRIMARY_LIGHT))[0]
    badge_text = ""
    if stance in BADGE_COLORS:
        fg, _ = BADGE_COLORS[stance]
        badge_text = f' <font color="{fg.hexval()}" size="7">[{stance.title()}]</font>'

    parts = [Paragraph(f"<b>{_esc(name)} — {_esc(title)}</b>{badge_text}", STYLES["body"])]
    for label, value in fields.items():
        text, prov = extract_provenance(value)
        prov_str = f' <font color="{C.TEXT_MUTED.hexval()}" size="7">[{prov}]</font>' if prov else ""
        parts.append(Paragraph(f"<b>{_esc(label)}:</b> {_esc(text)}{prov_str}", STYLES["body_small"]))

    card_data = [[p] for p in parts]
    card = Table(card_data, colWidths=[CONTENT_W - 4 * mm])
    card.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, C.BORDER),
        ("LINEBEFORE", (0, 0), (0, -1), 3, stance_color),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))

    return [KeepTogether([card]), Spacer(1, 1.5 * mm)]


# ===== Objective (EB) =====
def _build_objective(block: dict) -> list:
    title = block.get("title", "")
    context = block.get("context", "")
    talking_points = block.get("talking_points", [])
    ask = block.get("ask", "")

    parts = [Paragraph(f"<b>{_esc(title)}</b>", STYLES["body"])]
    if context:
        parts.append(Paragraph(f"<b>Context:</b> {_esc(context)}", STYLES["body_small"]))
    if talking_points:
        if isinstance(talking_points, list):
            for tp in talking_points:
                parts.append(Paragraph(f"• {_esc(tp)}", STYLES["body_small"]))
        else:
            parts.append(Paragraph(f"• {_esc(str(talking_points))}", STYLES["body_small"]))
    if ask:
        parts.append(Paragraph(f"<b>Ask:</b> {_esc(ask)}", STYLES["body_small"]))

    card_data = [[p] for p in parts]
    card = Table(card_data, colWidths=[CONTENT_W - 4 * mm])
    card.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, C.BORDER),
        ("LINEBEFORE", (0, 0), (0, -1), 3, C.NEUTRAL),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return [KeepTogether([card]), Spacer(1, 1.5 * mm)]


# ===== Concern (EB) =====
def _build_concern(block: dict) -> list:
    title = block.get("title", "")
    acknowledge = block.get("acknowledge", "")
    pivot = block.get("pivot", "")
    elevate = block.get("elevate", "")
    landmine = block.get("landmine", "")

    parts = [Paragraph(f"<b>{_esc(title)}</b>", STYLES["body"])]
    if acknowledge:
        parts.append(Paragraph(f"<b>Acknowledge:</b> {_esc(acknowledge)}", STYLES["body_small"]))
    if pivot:
        parts.append(Paragraph(f"<b>Pivot:</b> {_esc(pivot)}", STYLES["body_small"]))
    if elevate:
        parts.append(Paragraph(f"<b>Elevate:</b> {_esc(elevate)}", STYLES["body_small"]))
    if landmine:
        parts.append(Paragraph(f'<b><font color="{C.NON_SUPPORTER.hexval()}">LANDMINE:</font></b> {_esc(landmine)}', STYLES["body_small"]))

    card_data = [[p] for p in parts]
    card = Table(card_data, colWidths=[CONTENT_W - 4 * mm])
    card.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, C.BORDER),
        ("LINEBEFORE", (0, 0), (0, -1), 3, C.NEUTRAL),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return [KeepTogether([card]), Spacer(1, 1.5 * mm)]


# ===== Engagement Entry =====
def _build_engagement_entry(block: dict) -> list:
    number = block.get("number", 0)
    date = block.get("date", "")

    parts = [Paragraph(f"<b>Engagement #{number} — {_esc(date)}</b>", STYLES["body"])]
    for key, label in [("attendees", "Attendees"), ("planned", "Planned"), ("actual", "Actual"),
                       ("people_updates", "People Updates"), ("key_learnings", "Key Learnings"),
                       ("plan_adjustment", "Plan Adjustment")]:
        val = block.get(key, "")
        if val:
            parts.append(Paragraph(f"<b>{label}:</b> {_esc(val)}", STYLES["body_small"]))

    card_data = [[p] for p in parts]
    card = Table(card_data, colWidths=[CONTENT_W - 4 * mm])
    card.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, C.BORDER),
        ("LINEBEFORE", (0, 0), (0, -1), 3, C.PRIMARY),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return [KeepTogether([card]), Spacer(1, 1.5 * mm)]


# ===== Subsection =====
def _build_subsection(block: dict, doc_type: str) -> list:
    title = block.get("title", "")
    raw_title = block.get("raw_title", title)
    content = block.get("content", [])

    # Success tier detection
    if re.match(r'^[●◐○]\s', raw_title) or re.match(r'^[\U0001F7E2\U0001F7E1⚪]\s', raw_title):
        return _build_success_tier(raw_title, content, doc_type)

    # Path detection
    if re.match(r'^[✅⏳\U0001F6AA]\s', raw_title):
        clean = re.sub(r'^[✅⏳\U0001F6AA]\s*', '', raw_title)
        elements = [Paragraph(f"<b>{_esc(clean)}</b>", STYLES["sub_heading"])]
        for b in content:
            elements.extend(_build_block(b, doc_type))
        return elements

    elements = [Paragraph(f"<b>{_esc(title)}</b>", STYLES["sub_heading"])]
    for b in content:
        elements.extend(_build_block(b, doc_type))
    return elements


def _build_subsubsection(block: dict, doc_type: str) -> list:
    title = block.get("title", "")
    content = block.get("content", [])
    elements = [Paragraph(f"<b>{_esc(title)}</b>", STYLES["body"])]
    for b in content:
        elements.extend(_build_block(b, doc_type))
    return elements


def _build_success_tier(raw_title: str, content: list, doc_type: str) -> list:
    # Determine tier
    clean = re.sub(r'^[●◐○\U0001F7E2\U0001F7E1⚪]\s*', '', raw_title)
    if "●" in raw_title or "\U0001F7E2" in raw_title or "Ideal" in clean:
        icon, color = "●", C.ACHIEVED
    elif "◐" in raw_title or "\U0001F7E1" in raw_title or "Acceptable" in clean:
        icon, color = "◐", C.PARTIAL
    else:
        icon, color = "○", C.TEXT_MUTED

    elements = [Paragraph(f'<font color="{color.hexval()}"><b>{icon}</b></font> <b>{_esc(clean)}</b>', STYLES["body"])]
    for b in content:
        elements.extend(_build_block(b, doc_type))
    return elements


# ===== Bullets =====
def _build_bullets(block: dict) -> list:
    items = block.get("items", [])
    elements = []
    for item in items:
        elements.append(Paragraph(f"•  {_inline(item)}", STYLES["bullet"]))
    elements.append(Spacer(1, 1.5 * mm))
    return elements


# ===== Highlight =====
def _build_highlight(block: dict) -> list:
    text = block.get("text", "")

    is_success = "achieved" in text.lower() or "✓" in text
    border_color = C.ACHIEVED if is_success else C.PRIMARY
    bg_color = colors.HexColor("#ECFDF5") if is_success else C.PRIMARY_LIGHT

    para = Paragraph(f"<b>{_inline(text)}</b>", STYLES["highlight"])
    t = Table([[para]], colWidths=[CONTENT_W - 4 * mm])
    t.setStyle(TableStyle([
        ("LINEBEFORE", (0, 0), (0, -1), 2.5, border_color),
        ("BACKGROUND", (0, 0), (-1, -1), bg_color),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return [t, Spacer(1, 1.5 * mm)]


# ===== Utilities =====
def _esc(text: str) -> str:
    """Escape XML special chars for ReportLab Paragraph."""
    if not text:
        return ""
    text = str(text)
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def _inline(text: str) -> str:
    """Process inline formatting for ReportLab Paragraph markup."""
    if not text:
        return ""
    result = _esc(text)
    # Bold
    result = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', result)
    # Provenance labels
    result = result.replace('[销售确认]', f'<font color="{C.CHAMPION.hexval()}" size="7">[销售确认]</font>')
    result = result.replace('[网络搜索]', f'<font color="{C.PRIMARY.hexval()}" size="7">[网络搜索]</font>')
    result = result.replace('[AI推断]', f'<font color="{C.TEXT_MUTED.hexval()}" size="7">[AI推断]</font>')
    return result
