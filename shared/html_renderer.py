"""
html_renderer.py — Dict → Self-contained HTML.

Generates a single HTML file with all CSS inlined (no external dependencies).
Handles all 4 document types: EP, CP, EB, PMR.
"""

import html
import os
import re
from pathlib import Path

from parse import extract_provenance, get_doc_type, get_section_by_title


# PDF-safe emoji replacements (WeasyPrint + Noto Sans CJK lack color emoji glyphs)
# These unicode symbols render reliably in all environments.
PDF_SAFE_EMOJI = {
    "🟢": "●",   # Green circle → filled circle (colored via CSS)
    "🟡": "◐",   # Yellow circle → half circle
    "⚪": "○",   # White circle → open circle
    "🔴": "●",   # Red circle → filled circle
}


# Document type display names
DOC_TYPE_LABELS = {
    "engagement-plan": "ENGAGEMENT PLAN",
    "call-plan": "CALL PLAN",
    "executive-briefing": "EXECUTIVE BRIEFING",
    "post-meeting-report": "POST-MEETING REPORT",
}

# Section emoji mapping (canonical)
SECTION_EMOJIS = {
    "opportunity snapshot": "📊",
    "key stakeholders": "👥",
    "engagement roadmap": "📍",
    "next milestone detail": "📋",
    "estimate & contingency": "📐",
    "execution log": "📝",
    "change log": "📜",
    "target meeting outcomes": "🎯",
    "success criteria": "✅",
    "customer attendees": "👥",
    "aws team": "👥",
    "information exchange": "🔄",
    "potential objections & responses": "🛡️",
    "meeting agenda": "📅",
    "potential next steps": "➡️",
    "disqualification signals": "🚫",
    "meeting logistics": "📋",
    "customer attendee background": "👤",
    "company profile": "🏢",
    "meeting objectives": "🎯",
    "aws account background": "📊",
    "appendix": "📎",
    "outcome assessment": "📊",
    "meeting insights": "🔍",
    "what changed": "📝",
    "next steps": "🔄",
    "customer recap email": "✉️",
}


def render_html(doc: dict) -> str:
    """Render a validated document dict to self-contained HTML string."""
    frontmatter = doc.get("frontmatter", {})
    sections = doc.get("sections", [])
    doc_type = get_doc_type(frontmatter)
    
    # Load CSS
    css = _load_css()
    
    # Build HTML parts
    parts = []
    parts.append(_html_head(frontmatter, doc_type, css))
    parts.append('<body>\n<div class="page">\n')
    
    # Document header
    parts.append(_render_header(frontmatter, doc_type))
    
    # EB confidential banner (after header, per DESIGN_PREVIEW L761)
    if doc_type == "executive-briefing":
        classification = frontmatter.get("classification", "")
        if classification:
            parts.append(f'<div class="confidential-banner">🔒 {_esc(classification)}</div>\n')
    
    # Render each section
    for section in sections:
        parts.append(_render_section(section, doc_type, frontmatter))
    
    # Footer
    parts.append(_render_footer(frontmatter, doc_type))
    
    parts.append('</div>\n</body>\n</html>')
    
    return '\n'.join(parts)


def _load_css() -> str:
    """Load theme.css from the shared directory."""
    css_path = Path(__file__).parent / "theme.css"
    if css_path.exists():
        return css_path.read_text(encoding="utf-8")
    return "/* theme.css not found */"


def _esc(text: str) -> str:
    """HTML-escape text and replace problematic emoji with PDF-safe symbols."""
    if not text:
        return ""
    result = str(text)
    for emoji, symbol in PDF_SAFE_EMOJI.items():
        result = result.replace(emoji, symbol)
    return html.escape(result)


def _html_head(frontmatter: dict, doc_type: str, css: str) -> str:
    """Generate HTML head with inline CSS."""
    customer = frontmatter.get("customer", "Document")
    doc_label = DOC_TYPE_LABELS.get(doc_type, "DOCUMENT")
    title = f"{doc_label} — {customer}"
    
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_esc(title)}</title>
<style>
{css}
</style>
</head>'''


def _render_header(frontmatter: dict, doc_type: str) -> str:
    """Render document header."""
    customer = frontmatter.get("customer", "")
    doc_label = DOC_TYPE_LABELS.get(doc_type, "DOCUMENT")
    
    # Build subtitle parts
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
    
    subtitle = " · ".join(subtitle_parts)
    
    # Meta badges
    meta_badges = []
    
    if doc_type == "call-plan":
        stage = frontmatter.get("stage", "")
        stage_target = frontmatter.get("stage_target", "")
        if stage and stage_target:
            meta_badges.append(f'<span class="meta-badge">📈 {_esc(stage)} → {_esc(stage_target)}</span>')
        elif stage:
            meta_badges.append(f'<span class="meta-badge">📈 {_esc(stage)}</span>')
        
        date = frontmatter.get("date", "")
        time_val = frontmatter.get("time", "")
        if date:
            time_str = f"{date} {time_val}" if time_val else date
            meta_badges.append(f'<span class="meta-badge date">📅 {_esc(time_str)}</span>')
        
        location = frontmatter.get("location", "")
        if location:
            meta_badges.append(f'<span class="meta-badge date">📍 {_esc(location)}</span>')
    
    elif doc_type == "engagement-plan":
        stage = frontmatter.get("stage", "")
        if stage:
            meta_badges.append(f'<span class="meta-badge">📈 {_esc(stage)}</span>')
        created = frontmatter.get("created", "")
        if created:
            meta_badges.append(f'<span class="meta-badge date">📅 Created {_esc(created)}</span>')
    
    elif doc_type == "executive-briefing":
        stage = frontmatter.get("stage", "")
        if stage:
            meta_badges.append(f'<span class="meta-badge">📈 {_esc(stage)}</span>')
        date = frontmatter.get("date", "")
        time_val = frontmatter.get("time", "")
        if date:
            time_str = f"{date} {time_val}" if time_val else date
            meta_badges.append(f'<span class="meta-badge date">📅 {_esc(time_str)}</span>')
        location = frontmatter.get("location", "")
        if location:
            meta_badges.append(f'<span class="meta-badge date">📍 {_esc(location)}</span>')
    
    elif doc_type == "post-meeting-report":
        date = frontmatter.get("date", "")
        if date:
            meta_badges.append(f'<span class="meta-badge date">📅 {_esc(date)}</span>')
        recorded_by = frontmatter.get("recorded_by", "")
        if recorded_by:
            meta_badges.append(f'<span class="meta-badge date">📝 Recorded by: {_esc(recorded_by)}</span>')
    
    meta_html = '\n    '.join(meta_badges)
    
    return f'''<div class="doc-header">
  <div class="doc-type-label">{_esc(doc_label)}</div>
  <div class="doc-title">{_esc(customer)}</div>
  <div class="doc-subtitle">{_esc(subtitle)}</div>
  <div class="doc-meta">
    {meta_html}
  </div>
</div>
'''


def _render_section(section: dict, doc_type: str, frontmatter: dict) -> str:
    """Render a section card."""
    emoji = section.get("emoji", "")
    title = section.get("title", "")
    content_blocks = section.get("content", [])
    
    # Determine canonical emoji
    if not emoji:
        emoji = SECTION_EMOJIS.get(title.lower(), "📌")
    
    parts = []
    parts.append('<div class="section-card">')
    parts.append(f'  <div class="section-header"><span class="emoji">{emoji}</span> {_esc(title)}</div>')
    
    # Check if section contains milestones at top level → wrap in roadmap
    has_milestones = any(b.get("type") == "milestone" for b in content_blocks)
    
    if has_milestones:
        # Separate non-milestone blocks (e.g. progress line) from milestones
        pre_blocks = []
        milestone_blocks = []
        for block in content_blocks:
            if block.get("type") == "milestone":
                milestone_blocks.append(block)
            elif not milestone_blocks:
                pre_blocks.append(block)
            else:
                milestone_blocks.append(block)
        
        for block in pre_blocks:
            parts.append(_render_block(block, doc_type))
        
        parts.append('  <div class="roadmap">')
        for block in milestone_blocks:
            parts.append(_render_block(block, doc_type))
        parts.append('  </div>')
    else:
        # Render content blocks normally
        for block in content_blocks:
            parts.append(_render_block(block, doc_type))
    
    parts.append('</div>\n')
    return '\n'.join(parts)


def _render_block(block: dict, doc_type: str) -> str:
    """Render a single content block."""
    block_type = block.get("type", "")
    
    if block_type == "table":
        return _render_table(block)
    elif block_type == "stakeholder_card":
        return _render_stakeholder_card(block, doc_type)
    elif block_type == "milestone":
        return _render_milestone(block)
    elif block_type == "objection":
        return _render_objection_card(block)
    elif block_type == "eb_person":
        return _render_eb_person(block)
    elif block_type == "engagement_entry":
        return _render_engagement_entry(block)
    elif block_type == "subsection":
        return _render_subsection(block, doc_type)
    elif block_type == "subsubsection":
        return _render_subsubsection(block, doc_type)
    elif block_type == "objective":
        return _render_objective(block)
    elif block_type == "concern":
        return _render_concern(block)
    elif block_type == "bullet_list":
        return _render_bullet_list(block)
    elif block_type == "paragraph":
        return _render_paragraph(block)
    elif block_type == "highlight":
        return _render_highlight(block)
    else:
        return f'  <p class="content-paragraph">{_esc(str(block))}</p>'


def _render_table(block: dict) -> str:
    """Render a markdown table as HTML table."""
    headers = block.get("headers", [])
    rows = block.get("rows", [])
    
    parts = ['  <table>']
    
    if headers:
        parts.append('    <thead><tr>')
        for h in headers:
            parts.append(f'      <th>{_render_inline(h)}</th>')
        parts.append('    </tr></thead>')
    
    parts.append('    <tbody>')
    for row in rows:
        parts.append('      <tr>')
        for i, cell in enumerate(row):
            rendered_cell = _render_cell_with_badges(cell)
            parts.append(f'        <td>{rendered_cell}</td>')
        parts.append('      </tr>')
    parts.append('    </tbody>')
    parts.append('  </table>')
    
    return '\n'.join(parts)


def _render_cell_with_badges(cell: str) -> str:
    """Render a table cell, converting badge values to styled spans."""
    # Check for known badge values
    cell_lower = cell.lower().strip()
    
    # Result badges
    if cell_lower in ("achieved", "partial", "not-achieved"):
        prefix = {"achieved": "✓", "partial": "⚠️", "not-achieved": "❌"}.get(cell_lower, "")
        css_class = f"badge-{cell_lower}"
        return f'<span class="badge {css_class}" style="font-size:11px; padding:1px 8px;">{prefix} {_esc(cell.strip().title())}</span>'
    
    # Priority badges
    if cell_lower in ("high", "medium", "low"):
        return f'<span class="badge badge-{cell_lower}" style="font-size:11px; padding:1px 8px;">{_esc(cell.strip().title())}</span>'
    
    # Action status badges
    if cell_lower in ("pending", "in-progress", "done"):
        return f'<span class="badge badge-{cell_lower}" style="font-size:11px; padding:1px 8px;">{_esc(cell.strip().title())}</span>'
    
    # Gap status
    if cell_lower in ("answered", "unanswered"):
        return f'<span class="badge badge-{cell_lower}" style="font-size:11px; padding:1px 8px;">{_esc(cell.strip().title())}</span>'
    
    # Change type
    if cell_lower in ("update", "add", "remove", "no-change"):
        return f'<span class="badge badge-{cell_lower}" style="font-size:11px; padding:1px 8px;">{_esc(cell.strip().title())}</span>'
    
    return _render_inline(cell)


def _render_stakeholder_card(block: dict, doc_type: str) -> str:
    """Render a stakeholder/attendee card."""
    name = block.get("name", "")
    title = block.get("title", "")
    stance = block.get("stance", "unknown").lower().strip()
    role = block.get("role", "").lower().strip()
    
    # Build badge HTML
    badges = []
    if stance and stance != "unknown":
        css_stance = f"badge-{stance}"
        badges.append(f'<span class="badge {css_stance}">{_esc(stance.replace("-", " ").title())}</span>')
    elif stance == "unknown":
        badges.append(f'<span class="badge badge-unknown">Unknown</span>')
    
    if role:
        css_role = f"badge-{role}"
        badges.append(f'<span class="badge {css_role}">{_esc(role.replace("-", " ").title())}</span>')
    
    badges_html = '\n      '.join(badges)
    
    # Fields
    fields_html = []
    
    # Different fields for CP vs EP
    if doc_type == "call-plan":
        focus = block.get("focus", "")
        if focus:
            text, prov = extract_provenance(focus)
            prov_html = _provenance_html(prov)
            fields_html.append(f'    <div class="field"><span class="field-label">Focus:</span> {_render_inline(text)} {prov_html}</div>')
        
        comm = block.get("communication", "")
        if comm:
            fields_html.append(f'    <div class="field"><span class="field-label">Communication:</span> {_render_inline(comm)}</div>')
        
        goal = block.get("our_goal", "") or block.get("how_to_win", "")
        if goal:
            fields_html.append(f'    <div class="how-to-win"><strong>🎯 Our Goal:</strong> {_render_inline(goal)}</div>')
    else:
        # EP style
        care = block.get("what_they_care_about", "")
        if care:
            text, prov = extract_provenance(care)
            prov_html = _provenance_html(prov)
            fields_html.append(f'    <div class="field"><span class="field-label">What They Care About:</span> {_render_inline(text)} {prov_html}</div>')
        
        need = block.get("what_we_need", "")
        if need:
            fields_html.append(f'    <div class="field"><span class="field-label">What We Need:</span> {_render_inline(need)}</div>')
        
        win = block.get("how_to_win", "") or block.get("our_goal", "")
        if win:
            fields_html.append(f'    <div class="how-to-win"><strong>🎯 How to Win:</strong> {_render_inline(win)}</div>')
    
    fields_str = '\n'.join(fields_html)
    
    return f'''  <div class="stakeholder-card">
    <div class="badges">
      {badges_html}
    </div>
    <div class="name">{_esc(name)}</div>
    <div class="title">{_esc(title)}</div>
{fields_str}
  </div>'''


def _render_milestone(block: dict) -> str:
    """Render a milestone in the roadmap timeline."""
    number = block.get("number", 0)
    title = block.get("title", "")
    status = block.get("status", "planned").lower().strip()
    stakeholders = block.get("stakeholders", "")
    aws_resources = block.get("aws_resources", "")
    timeline = block.get("timeline", "")
    
    # Marker content
    marker_content = {"done": "✓", "next": "▶"}.get(status, str(number))
    active_class = " active" if status == "next" else ""
    
    # Status badge
    status_labels = {"done": "✓ Done", "next": "▶ Next", "planned": "Planned"}
    badge_label = status_labels.get(status, status.title())
    
    return f'''  <div class="milestone{active_class}">
    <div class="milestone-marker {status}">{marker_content}</div>
    <div class="milestone-title">{_esc(title)}</div>
    <div class="milestone-meta">
      <span>👤 {_esc(stakeholders)}</span>
      <span>🏢 {_esc(aws_resources)}</span>
      <span>📅 {_esc(timeline)}</span>
      <span class="badge badge-{status}" style="font-size:11px;">{badge_label}</span>
    </div>
  </div>'''


def _render_objection_card(block: dict) -> str:
    """Render an objection card with category-colored left border."""
    title = block.get("title", "")
    category = block.get("category", "").lower().strip()
    likely_from = block.get("likely_from", "")
    response = block.get("response", "")
    plan_b = block.get("plan_b", "")
    
    # Category display name
    category_labels = {
        "risk-trust": "Risk/Trust",
        "capability": "Capability",
        "authority": "Authority/Process",
        "price-value": "Price/Value",
        "status-quo": "Status Quo",
    }
    cat_label = category_labels.get(category, category.replace("-", " ").title())
    cat_class = category if category in category_labels else ""
    
    return f'''  <div class="objection-card {cat_class}">
    <div class="objection-header">
      <span class="objection-title">{_render_inline(title)}</span>
      <span class="category-badge {cat_class}">{_esc(cat_label)}</span>
    </div>
    <div class="field" style="font-size:12px; color:var(--color-text-secondary);">Likely From: {_esc(likely_from)}</div>
    <div class="response"><strong>Response:</strong> {_render_inline(response)}</div>
    <div class="plan-b"><strong>Plan B:</strong> {_render_inline(plan_b)}</div>
  </div>'''


def _render_eb_person(block: dict) -> str:
    """Render an Executive Briefing person background card."""
    name = block.get("name", "")
    title = block.get("title", "")
    stance = block.get("stance", "unknown").lower().strip()
    fields = block.get("fields", {})
    
    # Stance badge
    badge_html = ""
    if stance and stance != "unknown":
        css_stance = f"badge-{stance}"
        badge_html = f'<span class="badge {css_stance}">{_esc(stance.replace("-", " ").title())}</span>'
    
    # Render fields
    field_htmls = []
    for label, value in fields.items():
        text, prov = extract_provenance(value)
        prov_html = _provenance_html(prov)
        field_htmls.append(f'    <div class="field"><span class="field-label">{_esc(label)}:</span> {_render_inline(text)} {prov_html}</div>')
    
    fields_str = '\n'.join(field_htmls)
    
    return f'''  <div class="stakeholder-card">
    <div class="badges">
      {badge_html}
    </div>
    <div class="name">{_esc(name)} — {_esc(title)}</div>
    <div class="title" style="margin-bottom:16px;"></div>
{fields_str}
  </div>'''


def _render_engagement_entry(block: dict) -> str:
    """Render an execution log engagement entry."""
    number = block.get("number", 0)
    date = block.get("date", "")
    
    fields = [
        ("Attendees", block.get("attendees", "")),
        ("Planned", block.get("planned", "")),
        ("Actual", block.get("actual", "")),
        ("👥 People Updates", block.get("people_updates", "")),
        ("💡 Key Learnings", block.get("key_learnings", "")),
        ("🔄 Plan Adjustment", block.get("plan_adjustment", "")),
    ]
    
    field_htmls = []
    for label, value in fields:
        if value:
            field_htmls.append(f'    <div class="field"><span class="field-label">{label}:</span> {_render_inline(value)}</div>')
    
    fields_str = '\n'.join(field_htmls)
    
    return f'''  <div style="border:1px solid var(--color-border); border-radius:10px; padding:16px 20px; margin-bottom:12px;">
    <div style="font-weight:600; font-size:14px; margin-bottom:8px;">Engagement #{number} — {_esc(date)}</div>
{fields_str}
  </div>'''


def _render_subsection(block: dict, doc_type: str) -> str:
    """Render a generic subsection."""
    title = block.get("title", "")
    raw_title = block.get("raw_title", title)
    emoji = block.get("emoji", "")
    content = block.get("content", [])
    
    # Special handling for Success Criteria tiers
    if _is_success_tier(raw_title):
        return _render_success_tier(raw_title, content)
    
    # Special handling for Next Steps paths
    if _is_next_steps_path(raw_title):
        return _render_next_steps_path(raw_title, content)
    
    # Check if this is a roadmap container (contains milestones)
    has_milestones = any(b.get("type") == "milestone" for b in content)
    
    parts = []
    
    if has_milestones:
        # Render as roadmap timeline
        parts.append('  <div class="roadmap">')
        for b in content:
            parts.append(_render_block(b, doc_type))
        parts.append('  </div>')
    else:
        # Generic sub-heading + content
        prefix = f"{emoji} " if emoji else ""
        parts.append(f'  <div class="sub-heading">{_esc(prefix + title)}</div>')
        for b in content:
            parts.append(_render_block(b, doc_type))
    
    return '\n'.join(parts)


def _render_subsubsection(block: dict, doc_type: str) -> str:
    """Render a #### level block."""
    title = block.get("title", "")
    emoji = block.get("emoji", "")
    content = block.get("content", [])
    
    prefix = f"{emoji} " if emoji else ""
    parts = [f'  <div style="font-weight:600; font-size:14px; margin:12px 0 6px;">{_esc(prefix + title)}</div>']
    for b in content:
        parts.append(_render_block(b, doc_type))
    
    return '\n'.join(parts)


def _render_objective(block: dict) -> str:
    """Render an EB meeting objective."""
    title = block.get("title", "")
    context = block.get("context", "")
    talking_points = block.get("talking_points", [])
    ask = block.get("ask", "")
    
    parts = [f'  <div style="border:1px solid var(--color-border); border-radius:8px; padding:14px 18px; margin-bottom:12px;">']
    parts.append(f'    <div style="font-weight:600; font-size:14px; margin-bottom:8px;">{_render_inline(title)}</div>')
    
    if context:
        parts.append(f'    <div class="field"><span class="field-label">Context:</span> {_render_inline(context)}</div>')
    
    if talking_points:
        parts.append('    <div class="field"><span class="field-label">Talking Points:</span></div>')
        parts.append('    <ul class="content-list">')
        if isinstance(talking_points, list):
            for tp in talking_points:
                parts.append(f'      <li>{_render_inline(tp)}</li>')
        else:
            parts.append(f'      <li>{_render_inline(str(talking_points))}</li>')
        parts.append('    </ul>')
    
    if ask:
        parts.append(f'    <div class="how-to-win"><strong>Ask:</strong> {_render_inline(ask)}</div>')
    
    parts.append('  </div>')
    return '\n'.join(parts)


def _render_concern(block: dict) -> str:
    """Render an EB anticipated concern."""
    title = block.get("title", "")
    acknowledge = block.get("acknowledge", "")
    pivot = block.get("pivot", "")
    elevate = block.get("elevate", "")
    landmine = block.get("landmine", "")
    
    parts = [f'  <div style="border:1px solid var(--color-border); border-left:4px solid var(--color-neutral); border-radius:8px; padding:14px 18px; margin-bottom:12px;">']
    parts.append(f'    <div style="font-weight:600; font-size:14px; margin-bottom:8px;">{_render_inline(title)}</div>')
    parts.append(f'    <div class="field"><span class="field-label">Acknowledge:</span> {_render_inline(acknowledge)}</div>')
    parts.append(f'    <div class="field"><span class="field-label">Pivot:</span> {_render_inline(pivot)}</div>')
    parts.append(f'    <div class="field"><span class="field-label">Elevate:</span> {_render_inline(elevate)}</div>')
    if landmine:
        parts.append(f'    <div class="field" style="color:var(--color-not-achieved);"><span class="field-label">💣 Landmine:</span> {_render_inline(landmine)}</div>')
    parts.append('  </div>')
    return '\n'.join(parts)


def _is_success_tier(title: str) -> bool:
    """Check if subsection is a success criteria tier."""
    return bool(re.match(r'^[🟢🟡⚪●◐○]\s', title))


def _render_success_tier(title: str, content: list) -> str:
    """Render a success criteria tier (Ideal/Acceptable/Minimum)."""
    # Determine tier level for icon coloring
    tier_class = "tier-icon-minimum"
    if "●" in title or "🟢" in title or "Ideal" in title:
        tier_class = "tier-icon-ideal"
    elif "◐" in title or "🟡" in title or "Acceptable" in title:
        tier_class = "tier-icon-acceptable"
    
    # Split icon from label text
    escaped_title = _esc(title)
    # Wrap the leading symbol in a colored span
    icon_match = re.match(r'^([●◐○])\s*(.*)$', escaped_title)
    if icon_match:
        icon_html = f'<span class="{tier_class}">{icon_match.group(1)}</span> {icon_match.group(2)}'
    else:
        icon_html = escaped_title
    
    parts = ['  <div class="tier">']
    parts.append(f'    <div class="tier-header">{icon_html}</div>')
    
    for block in content:
        if block.get("type") == "bullet_list":
            parts.append('    <ul>')
            for item in block.get("items", []):
                parts.append(f'      <li>{_render_inline(item)}</li>')
            parts.append('    </ul>')
        else:
            parts.append(_render_block(block, ""))
    
    parts.append('  </div>')
    return '\n'.join(parts)


def _is_next_steps_path(title: str) -> bool:
    """Check if subsection is a next steps path header."""
    return bool(re.match(r'^[✅⏳🚪]\s', title))


def _render_next_steps_path(title: str, content: list) -> str:
    """Render a next steps path (primary/fallback/exit)."""
    # Determine path icon
    icon = title[0] if title else "✅"
    
    parts = [f'  <div class="path-header"><span class="path-icon">{icon}</span> {_esc(title[1:].strip() if len(title) > 1 else title)}</div>']
    
    for block in content:
        parts.append(_render_block(block, ""))
    
    return '\n'.join(parts)


def _render_bullet_list(block: dict) -> str:
    """Render a bullet list."""
    items = block.get("items", [])
    parts = ['  <ul class="content-list">']
    for item in items:
        parts.append(f'    <li>{_render_inline(item)}</li>')
    parts.append('  </ul>')
    return '\n'.join(parts)


def _render_paragraph(block: dict) -> str:
    """Render a paragraph."""
    text = block.get("text", "")
    return f'  <p class="content-paragraph">{_render_inline(text)}</p>'


def _render_highlight(block: dict) -> str:
    """Render a bold highlight line (like **Stage Progression:** ...)."""
    text = block.get("text", "")
    
    # Check for stage progression
    if "Stage Progression" in text or "Fallback Outcome" in text:
        css_class = "highlight-box success" if "Achieved" in text or "achieved" in text else "highlight-box"
        rendered = _render_inline(text)
        return f'  <div class="{css_class}">{rendered}</div>'
    
    return f'  <div class="highlight-box">{_render_inline(text)}</div>'


def _render_inline(text: str) -> str:
    """Render inline markdown (bold, provenance, badges) to HTML."""
    if not text:
        return ""
    
    result = _esc(text)
    
    # Bold: **text**
    result = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', result)
    
    # Provenance labels
    result = result.replace('[销售确认]', '<span class="provenance provenance-sales">[销售确认]</span>')
    result = result.replace('[网络搜索]', '<span class="provenance provenance-web">[网络搜索]</span>')
    result = result.replace('[AI推断]', '<span class="provenance provenance-ai">[AI推断]</span>')
    
    # Inline badge syntax {field:value}
    def _badge_replace(m):
        value = m.group(2)
        css_class = f"badge-{value}"
        return f'<span class="badge {css_class}">{value.replace("-", " ").title()}</span>'
    
    result = re.sub(r'\{(\w+):([\w-]+)\}', _badge_replace, result)
    
    return result


def _provenance_html(prov_type: str | None) -> str:
    """Generate provenance label HTML."""
    if prov_type == "sales":
        return '<span class="provenance provenance-sales">[销售确认]</span>'
    elif prov_type == "web":
        return '<span class="provenance provenance-web">[网络搜索]</span>'
    elif prov_type == "ai":
        return '<span class="provenance provenance-ai">[AI推断]</span>'
    return ""


def _render_footer(frontmatter: dict, doc_type: str) -> str:
    """Render document footer."""
    doc_label = DOC_TYPE_LABELS.get(doc_type, "DOCUMENT")
    customer = str(frontmatter.get("customer", ""))
    date = str(frontmatter.get("date", frontmatter.get("version", "")))
    
    # Build footer line
    footer_parts = [doc_label]
    if customer:
        footer_parts.append(customer)
    
    # Add meeting title for CP/EB/PMR
    meeting_title = str(frontmatter.get("meeting_title", ""))
    if meeting_title:
        footer_parts.append(meeting_title)
    
    if date:
        footer_parts.append(date)
    
    footer_line = " | ".join(footer_parts)
    
    confidential = ""
    if doc_type == "executive-briefing":
        confidential = "<br>INTERNAL USE ONLY — AWS Confidential"
    
    return f'''<div class="doc-footer">
  {_esc(footer_line)}{confidential}<br>
  Generated by Dali · Confidential
</div>'''
