from __future__ import annotations

"""
html_renderer.py — Dict -> Self-contained HTML.

Generates a single HTML file with all CSS inlined (no external dependencies).
Handles all 4 document types: EP, CP, EB, PMR.

Design: MD3 Purple + McKinsey/BCG report style.
- Numbered exhibits with emoji in section headers
- Tight spacing, professional typography
- Exhibit-style tables with top/bottom rules
"""

import html
import re
from pathlib import Path

from .parse import extract_provenance, get_doc_type, get_section_by_title


DOC_TYPE_LABELS = {
    "engagement-plan": "ENGAGEMENT PLAN",
    "call-plan": "CALL PLAN",
    "executive-briefing": "EXECUTIVE BRIEFING",
    "post-meeting-report": "POST-MEETING REPORT",
}


def render_html(doc: dict) -> str:
    """Render a validated document dict to self-contained HTML string."""
    frontmatter = doc.get("frontmatter", {})
    sections = doc.get("sections", [])
    doc_type = get_doc_type(frontmatter)

    css = _load_css()

    parts = []
    parts.append(_html_head(frontmatter, doc_type, css))
    parts.append('<body>\n<div class="page">\n')

    parts.append(_render_header(frontmatter, doc_type))

    if doc_type == "executive-briefing":
        classification = frontmatter.get("classification", "")
        if classification:
            parts.append(f'<div class="confidential-banner">{_esc(classification)}</div>\n')

    for i, section in enumerate(sections, 1):
        parts.append(_render_section(section, doc_type, frontmatter, i))

    parts.append(_render_footer(frontmatter, doc_type))

    parts.append('</div>\n</body>\n</html>')

    return '\n'.join(parts)


def _load_css() -> str:
    css_path = Path(__file__).parent / "theme.css"
    if css_path.exists():
        return css_path.read_text(encoding="utf-8")
    return "/* theme.css not found */"


def _esc(text: str) -> str:
    if not text:
        return ""
    return html.escape(str(text))


def _html_head(frontmatter: dict, doc_type: str, css: str) -> str:
    customer = frontmatter.get("customer", "Document")
    doc_label = DOC_TYPE_LABELS.get(doc_type, "DOCUMENT")
    title = f"{doc_label} | {customer}"

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
    customer = frontmatter.get("customer", "")
    doc_label = DOC_TYPE_LABELS.get(doc_type, "DOCUMENT")

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
            subtitle_parts.append(f"TCV {tcv}")

    subtitle = "  |  ".join(subtitle_parts)

    meta_badges = []

    if doc_type == "call-plan":
        stage = frontmatter.get("stage", "")
        stage_target = frontmatter.get("stage_target", "")
        if stage and stage_target:
            meta_badges.append(f'<span class="meta-badge stage">{_esc(stage)} &rarr; {_esc(stage_target)}</span>')
        elif stage:
            meta_badges.append(f'<span class="meta-badge stage">{_esc(stage)}</span>')

        date = frontmatter.get("date", "")
        time_val = frontmatter.get("time", "")
        if date:
            time_str = f"{date} {time_val}" if time_val else date
            meta_badges.append(f'<span class="meta-badge">{_esc(time_str)}</span>')

        fmt = frontmatter.get("format", "")
        location = frontmatter.get("location", "")
        loc_str = location or fmt
        if loc_str:
            meta_badges.append(f'<span class="meta-badge">{_esc(loc_str)}</span>')

    elif doc_type == "engagement-plan":
        stage = frontmatter.get("stage", "")
        if stage:
            meta_badges.append(f'<span class="meta-badge stage">{_esc(stage)}</span>')
        created = frontmatter.get("created", "")
        if created:
            meta_badges.append(f'<span class="meta-badge">Created {_esc(created)}</span>')

    elif doc_type == "executive-briefing":
        stage = frontmatter.get("stage", "")
        if stage:
            meta_badges.append(f'<span class="meta-badge stage">{_esc(stage)}</span>')
        date = frontmatter.get("date", "")
        time_val = frontmatter.get("time", "")
        if date:
            time_str = f"{date} {time_val}" if time_val else date
            meta_badges.append(f'<span class="meta-badge">{_esc(time_str)}</span>')
        location = frontmatter.get("location", "")
        if location:
            meta_badges.append(f'<span class="meta-badge">{_esc(location)}</span>')

    elif doc_type == "post-meeting-report":
        date = frontmatter.get("date", "")
        if date:
            meta_badges.append(f'<span class="meta-badge">{_esc(date)}</span>')
        recorded_by = frontmatter.get("recorded_by", "")
        if recorded_by:
            meta_badges.append(f'<span class="meta-badge">Recorded by: {_esc(recorded_by)}</span>')

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


def _render_section(section: dict, doc_type: str, frontmatter: dict, section_num: int) -> str:
    title = section.get("title", "")
    content_blocks = section.get("content", [])

    parts = []
    parts.append('<div class="section-card">')
    emoji = section.get("emoji", "")
    emoji_str = f"{_esc(emoji)} " if emoji else ""
    parts.append(f'  <div class="section-header"><span class="section-number">{section_num}.</span> {emoji_str}{_esc(title)}</div>')

    has_milestones = any(b.get("type") == "milestone" for b in content_blocks)

    if has_milestones:
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
        for block in content_blocks:
            parts.append(_render_block(block, doc_type))

    parts.append('</div>\n')
    return '\n'.join(parts)


def _render_block(block: dict, doc_type: str) -> str:
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
        for cell in row:
            rendered_cell = _render_cell_with_badges(cell)
            parts.append(f'        <td>{rendered_cell}</td>')
        parts.append('      </tr>')
    parts.append('    </tbody>')
    parts.append('  </table>')

    return '\n'.join(parts)


def _render_cell_with_badges(cell: str) -> str:
    cell_lower = cell.lower().strip()

    # PMR Outcome Result
    if cell_lower in ("achieved", "partial", "not-achieved"):
        prefix = {"achieved": "✓", "partial": "△", "not-achieved": "✗"}.get(cell_lower, "")
        css_class = f"badge-{cell_lower}"
        return f'<span class="badge {css_class}">{prefix} {_esc(cell.strip().title())}</span>'

    # Priority (action items + stakeholder)
    if cell_lower in ("high", "medium", "low", "must-meet", "important", "nice-to-have") or \
       cell_lower.replace(" ", "-") in ("must-meet", "nice-to-have"):
        css = cell_lower.replace(" ", "-")
        return f'<span class="badge badge-{css}">{_esc(cell.strip().title())}</span>'

    # Action Status
    if cell_lower in ("pending", "in-progress", "in progress", "done", "open"):
        css = cell_lower.replace(" ", "-")
        return f'<span class="badge badge-{css}">{_esc(cell.strip().title())}</span>'

    # Gap Status (PMR Information Gap Check)
    if cell_lower in ("answered", "unanswered", "still a gap"):
        css = cell_lower.replace(" ", "-")
        return f'<span class="badge badge-{css}">{_esc(cell.strip().title())}</span>'

    # Change Type (PMR What Changed)
    if cell_lower in ("update", "add", "remove", "no-change", "confirm", "新增", "更新", "删除", "确认"):
        css = f"badge-{cell_lower}" if cell_lower.isascii() else "badge-add"
        return f'<span class="badge {css}">{_esc(cell.strip())}</span>'

    # Milestone Status (EP Roadmap)
    if cell_lower in ("done", "planned", "skipped") or "next" in cell_lower:
        css = "badge-next" if "next" in cell_lower else f"badge-{cell_lower}"
        display = cell.strip()
        return f'<span class="badge {css}">{_esc(display)}</span>'

    # Stance values in table cells
    if cell_lower in ("sponsor", "supporter", "neutral", "non-supporter", "adversary"):
        return f'<span class="badge badge-{cell_lower}">{_esc(cell.strip().title())}</span>'

    # Objection Category
    if cell_lower in ("status quo", "status-quo", "price/value", "price/competition", "capability", "risk/trust", "authority/process"):
        css = cell_lower.replace("/", "-").replace(" ", "-")
        return f'<span class="badge badge-{css}">{_esc(cell.strip().title())}</span>'

    return _render_inline(cell)


def _render_stakeholder_card(block: dict, doc_type: str) -> str:
    name = block.get("name", "")
    title = block.get("title", "")
    stance = block.get("stance", "unknown").lower().strip()
    role = block.get("role", "").lower().strip()

    badges = []
    if stance and stance != "unknown":
        css_stance = f"badge-{stance}"
        badges.append(f'<span class="badge {css_stance}">{_esc(stance.replace("-", " ").title())}</span>')
    elif stance == "unknown":
        badges.append('<span class="badge badge-unknown">Unknown</span>')

    if role and role != stance:
        css_role = f"badge-{role}"
        badges.append(f'<span class="badge {css_role}">{_esc(role.replace("-", " ").title())}</span>')

    badges_html = '\n      '.join(badges)

    fields_html = []

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
            fields_html.append(f'    <div class="how-to-win"><strong>Our Goal:</strong> {_render_inline(goal)}</div>')
    else:
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
            fields_html.append(f'    <div class="how-to-win"><strong>How to Win:</strong> {_render_inline(win)}</div>')

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
    number = block.get("number", 0)
    title = block.get("title", "")
    status = block.get("status", "planned").lower().strip()
    stakeholders = block.get("stakeholders", "")
    aws_resources = block.get("aws_resources", "")
    timeline = block.get("timeline", "")

    marker_content = {
        "done": "✓",
        "next": "▶",
    }.get(status, str(number))
    active_class = " active" if status == "next" else ""

    meta_parts = []
    if stakeholders:
        meta_parts.append(f'<span>{_esc(stakeholders)}</span>')
    if aws_resources:
        meta_parts.append(f'<span>{_esc(aws_resources)}</span>')
    if timeline:
        meta_parts.append(f'<span>{_esc(timeline)}</span>')
    meta_parts.append(f'<span class="badge badge-{status}">{_esc(status.title())}</span>')

    meta_html = '\n      '.join(meta_parts)

    return f'''  <div class="milestone{active_class}">
    <div class="milestone-marker {status}">{marker_content}</div>
    <div class="milestone-title">{_esc(title)}</div>
    <div class="milestone-meta">
      {meta_html}
    </div>
  </div>'''


def _render_objection_card(block: dict) -> str:
    title = block.get("title", "")
    category = block.get("category", "").lower().strip()
    likely_from = block.get("likely_from", "")
    response = block.get("response", "")
    plan_b = block.get("plan_b", "")

    category_labels = {
        "risk-trust": "RISK/TRUST",
        "capability": "CAPABILITY",
        "authority": "AUTHORITY",
        "price-value": "PRICE/VALUE",
        "status-quo": "STATUS QUO",
    }
    cat_label = category_labels.get(category, category.replace("-", " ").upper())
    cat_class = category if category in category_labels else ""

    return f'''  <div class="objection-card {cat_class}">
    <div class="objection-header">
      <span class="objection-title">{_render_inline(title)}</span>
      <span class="category-badge {cat_class}">{_esc(cat_label)}</span>
    </div>
    <div class="field">Likely from: {_esc(likely_from)}</div>
    <div class="response"><strong>Response:</strong> {_render_inline(response)}</div>
    <div class="plan-b"><strong>Plan B:</strong> {_render_inline(plan_b)}</div>
  </div>'''


def _render_eb_person(block: dict) -> str:
    name = block.get("name", "")
    title = block.get("title", "")
    stance = block.get("stance", "unknown").lower().strip()
    fields = block.get("fields", {})

    badge_html = ""
    if stance and stance != "unknown":
        css_stance = f"badge-{stance}"
        badge_html = f'<span class="badge {css_stance}">{_esc(stance.replace("-", " ").title())}</span>'

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
    <div class="title"></div>
{fields_str}
  </div>'''


def _render_engagement_entry(block: dict) -> str:
    number = block.get("number", 0)
    date = block.get("date", "")

    fields = [
        ("Attendees", block.get("attendees", "")),
        ("Planned", block.get("planned", "")),
        ("Actual", block.get("actual", "")),
        ("People Updates", block.get("people_updates", "")),
        ("Key Learnings", block.get("key_learnings", "")),
        ("Plan Adjustment", block.get("plan_adjustment", "")),
    ]

    field_htmls = []
    for label, value in fields:
        if value:
            field_htmls.append(f'    <div class="field"><span class="field-label">{label}:</span> {_render_inline(value)}</div>')

    fields_str = '\n'.join(field_htmls)

    return f'''  <div style="border:1px solid var(--color-border-light); border-top:3px solid var(--color-primary); padding:10px 14px; margin-bottom:8px;">
    <div style="font-weight:700; font-size:13px; color:var(--color-primary); margin-bottom:6px;">Engagement #{number} — {_esc(date)}</div>
{fields_str}
  </div>'''


def _render_subsection(block: dict, doc_type: str) -> str:
    title = block.get("title", "")
    raw_title = block.get("raw_title", title)
    content = block.get("content", [])

    if _is_success_tier(raw_title):
        return _render_success_tier(raw_title, content)

    if _is_next_steps_path(raw_title):
        return _render_next_steps_path(raw_title, content)

    has_milestones = any(b.get("type") == "milestone" for b in content)

    parts = []

    if has_milestones:
        parts.append('  <div class="roadmap">')
        for b in content:
            parts.append(_render_block(b, doc_type))
        parts.append('  </div>')
    else:
        emoji = block.get("emoji", "")
        emoji_str = f"{_esc(emoji)} " if emoji else ""
        parts.append(f'  <div class="sub-heading">{emoji_str}{_esc(title)}</div>')
        for b in content:
            parts.append(_render_block(b, doc_type))

    return '\n'.join(parts)


def _render_subsubsection(block: dict, doc_type: str) -> str:
    title = block.get("title", "")
    content = block.get("content", [])

    parts = [f'  <div style="font-weight:700; font-size:12px; color:var(--color-primary); margin:8px 0 4px;">{_esc(title)}</div>']
    for b in content:
        parts.append(_render_block(b, doc_type))

    return '\n'.join(parts)


def _render_objective(block: dict) -> str:
    title = block.get("title", "")
    context = block.get("context", "")
    talking_points = block.get("talking_points", [])
    ask = block.get("ask", "")

    parts = ['  <div style="border:1px solid var(--color-border-light); border-top:3px solid var(--color-primary); padding:10px 14px; margin-bottom:10px;">']
    parts.append(f'    <div style="font-weight:700; font-size:13px; color:var(--color-primary); margin-bottom:6px;">{_render_inline(title)}</div>')

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
    title = block.get("title", "")
    acknowledge = block.get("acknowledge", "")
    pivot = block.get("pivot", "")
    elevate = block.get("elevate", "")
    landmine = block.get("landmine", "")

    parts = ['  <div style="border:1px solid var(--color-border-light); border-left:4px solid var(--color-medium); padding:10px 14px; margin-bottom:8px;">']
    parts.append(f'    <div style="font-weight:700; font-size:13px; color:var(--color-primary); margin-bottom:4px;">{_render_inline(title)}</div>')
    parts.append(f'    <div class="field"><span class="field-label">Acknowledge:</span> {_render_inline(acknowledge)}</div>')
    parts.append(f'    <div class="field"><span class="field-label">Pivot:</span> {_render_inline(pivot)}</div>')
    parts.append(f'    <div class="field"><span class="field-label">Elevate:</span> {_render_inline(elevate)}</div>')
    if landmine:
        parts.append(f'    <div class="field" style="color:var(--color-not-achieved);"><span class="field-label">LANDMINE:</span> {_render_inline(landmine)}</div>')
    parts.append('  </div>')
    return '\n'.join(parts)


def _is_success_tier(title: str) -> bool:
    return bool(re.match(r'^[\U0001F7E2\U0001F7E1⚪●◐○]\s', title))


def _render_success_tier(title: str, content: list) -> str:
    tier_class = "tier-icon-minimum"
    if "●" in title or "\U0001F7E2" in title or "Ideal" in title:
        tier_class = "tier-icon-ideal"
    elif "◐" in title or "\U0001F7E1" in title or "Acceptable" in title:
        tier_class = "tier-icon-acceptable"

    clean_title = re.sub(r'^[\U0001F7E2\U0001F7E1⚪●◐○]\s*', '', title)
    icon_map = {"tier-icon-ideal": "●", "tier-icon-acceptable": "◐", "tier-icon-minimum": "○"}
    icon = icon_map.get(tier_class, "○")

    parts = ['  <div class="tier">']
    parts.append(f'    <div class="tier-header"><span class="{tier_class}">{icon}</span> {_esc(clean_title)}</div>')

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
    return bool(re.match(r'^[✅⏳\U0001F6AA]\s', title))


def _render_next_steps_path(title: str, content: list) -> str:
    clean_title = re.sub(r'^[✅⏳\U0001F6AA]\s*', '', title)

    parts = [f'  <div class="path-header">{_esc(clean_title)}</div>']

    for block in content:
        parts.append(_render_block(block, ""))

    return '\n'.join(parts)


def _render_bullet_list(block: dict) -> str:
    items = block.get("items", [])
    parts = ['  <ul class="content-list">']
    for item in items:
        parts.append(f'    <li>{_render_inline(item)}</li>')
    parts.append('  </ul>')
    return '\n'.join(parts)


def _render_paragraph(block: dict) -> str:
    text = block.get("text", "")
    return f'  <p class="content-paragraph">{_render_inline(text)}</p>'


def _render_highlight(block: dict) -> str:
    text = block.get("text", "")

    if "Stage Progression" in text or "Fallback Outcome" in text:
        css_class = "highlight-box success" if ("Achieved" in text or "achieved" in text or "✓" in text) else "highlight-box"
        rendered = _render_inline(text)
        return f'  <div class="{css_class}">{rendered}</div>'

    return f'  <div class="highlight-box">{_render_inline(text)}</div>'


def _render_inline(text: str) -> str:
    if not text:
        return ""

    result = _esc(text)

    # Bold
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
    if prov_type == "sales":
        return '<span class="provenance provenance-sales">[销售确认]</span>'
    elif prov_type == "web":
        return '<span class="provenance provenance-web">[网络搜索]</span>'
    elif prov_type == "ai":
        return '<span class="provenance provenance-ai">[AI推断]</span>'
    return ""


def _render_footer(frontmatter: dict, doc_type: str) -> str:
    doc_label = DOC_TYPE_LABELS.get(doc_type, "DOCUMENT")
    customer = str(frontmatter.get("customer", ""))
    date = str(frontmatter.get("date", frontmatter.get("version", "")))

    footer_parts = [doc_label]
    if customer:
        footer_parts.append(customer)

    meeting_title = str(frontmatter.get("meeting_title", ""))
    if meeting_title:
        footer_parts.append(meeting_title)

    if date:
        footer_parts.append(date)

    footer_line = "  |  ".join(footer_parts)

    confidential = ""
    if doc_type == "executive-briefing":
        confidential = "<br>INTERNAL USE ONLY — AWS Confidential"

    return f'''<div class="doc-footer">
  {_esc(footer_line)}{confidential}
</div>'''
