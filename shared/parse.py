from __future__ import annotations

"""
parse.py — Structured Markdown → Python dict parser.

Handles:
- YAML frontmatter extraction
- Section detection (## emoji Title)
- Table parsing (Markdown tables → list of dicts)
- Stakeholder/Attendee card parsing (### Name + bullet fields)
- Milestone parsing (### Milestone N: desc + bullets)
- Objection card parsing (### title + bullets)
- Badge value extraction from inline text
- Provenance label extraction [销售确认] [网络搜索]
- Bullet list extraction
- Paragraph text extraction
"""

import re
import yaml
from typing import Any


def parse_markdown(md_text: str) -> dict:
    """Parse structured markdown into a document dict.
    
    Returns:
        {
            "frontmatter": {...},
            "sections": [
                {
                    "emoji": "📊",
                    "title": "Opportunity Snapshot",
                    "raw_title": "📊 Opportunity Snapshot",
                    "content": [...],  # list of content blocks
                }
            ]
        }
    """
    # Extract frontmatter
    frontmatter = {}
    body = md_text.strip()
    
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', body, re.DOTALL)
    if fm_match:
        try:
            frontmatter = yaml.safe_load(fm_match.group(1)) or {}
        except yaml.YAMLError:
            frontmatter = {}
        body = body[fm_match.end():]
    
    # Split into sections by ## headers
    sections = _split_sections(body)
    
    return {
        "frontmatter": frontmatter,
        "sections": sections,
    }


def _split_sections(body: str) -> list[dict]:
    """Split body into sections by ## headers."""
    # Match ## with optional emoji
    section_pattern = re.compile(r'^##\s+(.+)$', re.MULTILINE)
    
    matches = list(section_pattern.finditer(body))
    if not matches:
        return []
    
    sections = []
    for i, match in enumerate(matches):
        title_raw = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        content_text = body[start:end].strip()
        
        # Extract emoji from title
        emoji, title_clean = _extract_emoji(title_raw)
        
        # Parse content blocks
        content_blocks = _parse_section_content(content_text)
        
        sections.append({
            "emoji": emoji,
            "title": title_clean,
            "raw_title": title_raw,
            "content": content_blocks,
        })
    
    return sections


def _extract_emoji(title: str) -> tuple[str, str]:
    """Extract leading emoji from title string.
    
    Handles two formats:
    - Direct emoji: "📊 Opportunity Snapshot" → ("📊", "Opportunity Snapshot")
    - Numbered+emoji: "1. 📊 Opportunity Snapshot" → ("📊", "Opportunity Snapshot")
    
    The number prefix (N.) is stripped during extraction so renderers can
    apply their own numbering consistently.
    """
    # First: strip leading number prefix "N. " if present
    number_prefix_pattern = re.compile(r'^\d+\.\s*')
    stripped = number_prefix_pattern.sub('', title)
    
    # Match common emoji patterns (single emoji at start)
    emoji_pattern = re.compile(
        r'^([\U0001F300-\U0001FAF0\u2600-\u27BF\u2B50\u2705\u274C\u26A0\u2139'
        r'\u2934\u2935\u25B6\u25CB\u23F3\u2709\U0001F170-\U0001F19A'
        r'\U0001F1E0-\U0001F1FF\u200D\uFE0F]+)\s*'
    )
    m = emoji_pattern.match(stripped)
    if m:
        emoji = m.group(1).strip()
        rest = stripped[m.end():].strip()
        return emoji, rest
    
    # Fallback: check for emoji-like characters NOT in CJK/punctuation ranges
    # CJK Unified Ideographs: U+4E00–U+9FFF, U+3400–U+4DBF, U+F900–U+FAFF
    # CJK punctuation: U+3000–U+303F
    # Fullwidth forms: U+FF00–U+FFEF
    # We only match if the character is clearly emoji (Miscellaneous Symbols, Dingbats, etc.)
    if stripped:
        ch = stripped[0]
        cp = ord(ch)
        # Exclude CJK ideographs, CJK punctuation, fullwidth forms, and general punctuation
        is_cjk = (0x3000 <= cp <= 0x9FFF) or (0xF900 <= cp <= 0xFAFF) or (0xFF00 <= cp <= 0xFFEF)
        is_emoji_range = cp > 0x2000 and not is_cjk
        if is_emoji_range:
            idx = 0
            while idx < len(stripped):
                c = ord(stripped[idx])
                c_is_cjk = (0x3000 <= c <= 0x9FFF) or (0xF900 <= c <= 0xFAFF) or (0xFF00 <= c <= 0xFFEF)
                if c <= 0x2000 or c_is_cjk:
                    break
                if stripped[idx] not in '\uFE0F\u200D' and c < 0x2100:
                    break
                idx += 1
            if idx > 0:
                return stripped[:idx].strip(), stripped[idx:].strip()
    
    # No emoji found — return stripped title (number prefix already removed)
    return "", stripped


def _parse_section_content(text: str) -> list[dict]:
    """Parse section body into typed content blocks.
    
    Block types:
    - table: {type: "table", headers: [...], rows: [[...]]}
    - subsection: {type: "subsection", title: "...", emoji: "...", content: [...]}
    - stakeholder_card: {type: "stakeholder_card", name: "...", fields: {...}}
    - milestone: {type: "milestone", number: N, title: "...", fields: {...}}
    - objection: {type: "objection", title: "...", fields: {...}}
    - bullet_list: {type: "bullet_list", items: [...]}
    - paragraph: {type: "paragraph", text: "..."}
    - highlight: {type: "highlight", text: "..."}
    """
    if not text:
        return []
    
    blocks = []
    lines = text.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Skip empty lines
        if not line.strip():
            i += 1
            continue
        
        # ### Sub-section header
        if line.strip().startswith('### '):
            subsection_title = line.strip()[4:].strip()
            i += 1
            # Collect subsection content until next ### or end
            sub_lines = []
            while i < len(lines) and not lines[i].strip().startswith('### '):
                sub_lines.append(lines[i])
                i += 1
            sub_text = '\n'.join(sub_lines).strip()
            
            # Detect if it's a stakeholder/milestone/objection card
            block = _classify_subsection(subsection_title, sub_text)
            if isinstance(block, list):
                blocks.extend(block)
            else:
                blocks.append(block)
            continue
        
        # #### Sub-sub-section (EB objectives)
        if line.strip().startswith('#### '):
            subsection_title = line.strip()[5:].strip()
            i += 1
            sub_lines = []
            while i < len(lines) and not lines[i].strip().startswith('#### ') and not lines[i].strip().startswith('### '):
                sub_lines.append(lines[i])
                i += 1
            sub_text = '\n'.join(sub_lines).strip()
            block = _parse_subsubsection(subsection_title, sub_text)
            blocks.append(block)
            continue
        
        # Table detection
        if '|' in line and i + 1 < len(lines) and re.match(r'\s*\|[-\s|:]+\|', lines[i + 1]):
            table_lines = []
            while i < len(lines) and '|' in lines[i]:
                table_lines.append(lines[i])
                i += 1
            table = _parse_table(table_lines)
            if table:
                blocks.append(table)
            continue
        
        # Bold highlight lines (**text:** content)
        if line.strip().startswith('**') and ':**' in line:
            text_content = line.strip()
            # Check for multi-line (next lines indented)
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('**') and not lines[i].strip().startswith('|') and not lines[i].strip().startswith('#') and not lines[i].strip().startswith('- '):
                text_content += ' ' + lines[i].strip()
                i += 1
            blocks.append({"type": "highlight", "text": text_content})
            continue
        
        # Bold name lines (**Name** — Title) — common in stakeholder/attendee sections
        if line.strip().startswith('**') and ':**' not in line:
            blocks.append({"type": "paragraph", "text": line.strip()})
            i += 1
            continue
        
        # Bullet list
        if line.strip().startswith('- '):
            items = []
            while i < len(lines) and lines[i].strip().startswith('- '):
                item_text = lines[i].strip()[2:]
                # Check for continuation (indented sub-items)
                i += 1
                while i < len(lines) and lines[i].startswith('  ') and not lines[i].strip().startswith('- '):
                    item_text += '\n' + lines[i].strip()
                    i += 1
                items.append(item_text)
            blocks.append({"type": "bullet_list", "items": items})
            continue
        
        # Plain paragraph
        para_lines = []
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('#') and not lines[i].strip().startswith('|') and not lines[i].strip().startswith('- ') and not lines[i].strip().startswith('**'):
            para_lines.append(lines[i].strip())
            i += 1
        if para_lines:
            blocks.append({"type": "paragraph", "text": ' '.join(para_lines)})
            continue
        
        i += 1
    
    return blocks


def _classify_subsection(title: str, content: str) -> dict | list:
    """Classify a ### subsection as stakeholder card, milestone, objection, or generic subsection.

    May return a list of blocks when a subsection contains multiple person entries
    (e.g., "### Attendee Insights" with multiple **Name** — Title blocks).
    """

    # Attendee Insights / multi-person container: split into individual cards
    if title.lower().strip() in ("attendee insights",) and content:
        cards = _split_multi_person_bullets(content)
        if cards:
            return cards

    # Milestone pattern: "Milestone N: description"
    milestone_match = re.match(r'Milestone\s+(\d+):\s*(.+)', title)
    if milestone_match:
        return _parse_milestone(int(milestone_match.group(1)), milestone_match.group(2), content)

    # Stakeholder/attendee pattern: has bullet fields like "- **Title:**", "- **Stance:**", "- **Engagement Priority:**"
    if content and re.search(r'^-\s+\*\*(?:Title|Stance|Role|Focus|Priority|Position|Engagement Priority|Role in This Deal|Current Stance|What They Care About|Profiling|What We Need|How to Win|Communication Approach|Our Goal|Focus & Priorities)', content, re.MULTILINE):
        return _parse_stakeholder_card(title, content)
    
    # Objection pattern: has "- **Category:**" field
    if content and re.search(r'^-\s+\*\*Category:\*\*', content, re.MULTILINE):
        return _parse_objection_card(title, content)
    
    # EB Person pattern: has paragraphs starting with **Position & Tenure:**
    if content and re.search(r'^\*\*(?:Position & Tenure|Communication Style|Decision Role)', content, re.MULTILINE):
        return _parse_eb_person(title, content)
    
    # Engagement log entry pattern: "Engagement #N — date"
    engagement_match = re.match(r'Engagement\s+#(\d+)\s*[—–-]\s*(.+)', title)
    if engagement_match:
        return _parse_engagement_entry(int(engagement_match.group(1)), engagement_match.group(2), content)
    
    # Generic subsection
    emoji, clean_title = _extract_emoji(title)
    sub_content = _parse_section_content(content)
    return {
        "type": "subsection",
        "title": clean_title,
        "raw_title": title,
        "emoji": emoji,
        "content": sub_content,
    }


def _split_multi_person_bullets(content: str) -> list | None:
    """Split a multi-person block (e.g., Attendee Insights) into individual stakeholder cards.

    Format: **Name** — Title followed by bullet fields, repeated for each person.
    Returns None if pattern not detected.
    """
    # Detect **Name** — Title pattern
    person_pattern = re.compile(r'^\*\*(.+?)\*\*\s*[—–-]\s*(.+)$', re.MULTILINE)
    matches = list(person_pattern.finditer(content))
    if len(matches) < 1:
        return None

    cards = []
    for idx, match in enumerate(matches):
        name = match.group(1).strip()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
        person_content = content[start:end].strip()
        if re.search(r'^-\s+\*\*', person_content, re.MULTILINE):
            card = _parse_stakeholder_card(name, person_content)
            cards.append(card)
    return cards if cards else None


def _parse_stakeholder_card(name: str, content: str) -> dict:
    """Parse a stakeholder / attendee card.

    Handles multiple field naming conventions:
    - EP template: Engagement Priority, Role in This Deal, Current Stance, What They Care About,
                   Profiling, What We Need From Them, How to Win Them
    - CP template: Focus & Priorities, Communication Approach, Current Stance, Our Goal
    - Legacy: Title, Stance, Role, Focus, Priority, What We Need, How to Win, Communication
    """
    fields = _parse_bullet_fields(content)
    return {
        "type": "stakeholder_card",
        "name": name,
        "title": fields.get("Title", ""),
        "stance": (fields.get("Current Stance", "") or fields.get("Stance", "unknown")),
        "role": (fields.get("Role in This Deal", "") or fields.get("Role", "")),
        "priority": (fields.get("Engagement Priority", "") or fields.get("Priority", "")),
        "focus": (fields.get("Focus & Priorities", "") or fields.get("Focus", "")),
        "what_they_care_about": fields.get("What They Care About", ""),
        "profiling": fields.get("Profiling", ""),
        "what_we_need": (fields.get("What We Need From Them", "") or fields.get("What We Need", "")),
        "how_to_win": (fields.get("How to Win Them", "") or
                       fields.get("🎯 How to Win", "") or fields.get("🎯 Our Goal", "")),
        "our_goal": (fields.get("Our Goal", "") or
                     fields.get("🎯 Our Goal", "") or fields.get("🎯 How to Win", "")),
        "communication": (fields.get("Communication Approach", "") or fields.get("Communication", "")),
        "fields": fields,
    }


def _parse_milestone(number: int, title: str, content: str) -> dict:
    """Parse a milestone entry."""
    fields = _parse_bullet_fields(content)
    return {
        "type": "milestone",
        "number": number,
        "title": title,
        "status": fields.get("Status", "planned"),
        "stakeholders": fields.get("👤 Stakeholders", ""),
        "aws_resources": fields.get("🏢 AWS Resources", ""),
        "timeline": fields.get("📅 Timeline", ""),
        "exit_criteria": fields.get("Exit Criteria", ""),
        "fields": fields,
    }


def _parse_objection_card(title: str, content: str) -> dict:
    """Parse an objection card."""
    fields = _parse_bullet_fields(content)
    return {
        "type": "objection",
        "title": title,
        "category": fields.get("Category", ""),
        "likely_from": fields.get("Likely From", ""),
        "response": fields.get("Response", ""),
        "plan_b": fields.get("Plan B", ""),
        "fields": fields,
    }


def _parse_eb_person(title: str, content: str) -> dict:
    """Parse an Executive Briefing person background block."""
    # Title format: "Person Name — Title"
    parts = re.split(r'\s*[—–-]\s*', title, maxsplit=1)
    name = parts[0].strip()
    person_title = parts[1].strip() if len(parts) > 1 else ""
    
    # Parse **Label:** value paragraphs
    fields = {}
    current_label = None
    current_value = []
    
    for line in content.split('\n'):
        bold_match = re.match(r'^\*\*(.+?):\*\*\s*(.*)$', line.strip())
        if bold_match:
            if current_label:
                fields[current_label] = ' '.join(current_value).strip()
            current_label = bold_match.group(1)
            current_value = [bold_match.group(2)]
        elif current_label and line.strip():
            current_value.append(line.strip())
    
    if current_label:
        fields[current_label] = ' '.join(current_value).strip()
    
    # Extract stance badge from "Attitude Toward AWS" field
    stance = "unknown"
    attitude = fields.get("Attitude Toward AWS", "")
    stance_match = re.search(r'\{stance:(\w[\w-]*)\}', attitude)
    if stance_match:
        stance = stance_match.group(1)
        fields["Attitude Toward AWS"] = re.sub(r'\s*\{stance:\w[\w-]*\}', '', attitude).strip()
    
    return {
        "type": "eb_person",
        "name": name,
        "title": person_title,
        "stance": stance,
        "fields": fields,
    }


def _parse_engagement_entry(number: int, date: str, content: str) -> dict:
    """Parse an execution log engagement entry."""
    fields = _parse_bullet_fields(content)
    return {
        "type": "engagement_entry",
        "number": number,
        "date": date,
        "attendees": fields.get("Attendees", ""),
        "planned": fields.get("Planned", ""),
        "actual": fields.get("Actual", ""),
        "people_updates": fields.get("👥 People Updates", ""),
        "key_learnings": fields.get("💡 Key Learnings", ""),
        "plan_adjustment": fields.get("🔄 Plan Adjustment", ""),
        "fields": fields,
    }


def _parse_subsubsection(title: str, content: str) -> dict:
    """Parse a #### level subsection (used in EB objectives)."""
    emoji, clean_title = _extract_emoji(title)
    
    # Check for concern (Acknowledge-Pivot-Elevate pattern)
    if re.search(r'^-\s+\*\*Acknowledge:\*\*', content, re.MULTILINE):
        fields = _parse_bullet_fields(content)
        return {
            "type": "concern",
            "title": clean_title,
            "raw_title": title,
            "acknowledge": fields.get("Acknowledge", ""),
            "pivot": fields.get("Pivot", ""),
            "elevate": fields.get("Elevate", ""),
            "landmine": fields.get("💣 Landmine", ""),
            "fields": fields,
        }
    
    # Check for objective (Context + Talking Points + Ask)
    if re.search(r'^-\s+\*\*Context:\*\*', content, re.MULTILINE):
        fields = _parse_bullet_fields(content)
        # Extract talking points (indented sub-items)
        talking_points = []
        in_tp = False
        for line in content.split('\n'):
            if '**Talking Points:**' in line:
                in_tp = True
                continue
            if in_tp:
                if line.strip().startswith('- ') and not line.startswith('  '):
                    in_tp = False
                elif line.strip().startswith('- '):
                    talking_points.append(line.strip()[2:])
        
        return {
            "type": "objective",
            "title": clean_title,
            "raw_title": title,
            "context": fields.get("Context", ""),
            "talking_points": talking_points or fields.get("Talking Points", ""),
            "ask": fields.get("Ask", ""),
            "fields": fields,
        }
    
    # Generic subsubsection
    sub_content = _parse_section_content(content)
    return {
        "type": "subsubsection",
        "title": clean_title,
        "raw_title": title,
        "emoji": emoji,
        "content": sub_content,
    }


def _parse_bullet_fields(content: str) -> dict:
    """Parse bullet list with **Label:** value format into a dict."""
    fields = {}
    current_key = None
    current_value = []
    
    for line in content.split('\n'):
        stripped = line.strip()
        # Match "- **Label:** value" pattern
        field_match = re.match(r'^-\s+\*\*(.+?):\*\*\s*(.*)$', stripped)
        if field_match:
            # Save previous field
            if current_key:
                fields[current_key] = '\n'.join(current_value).strip()
            current_key = field_match.group(1)
            current_value = [field_match.group(2)]
        elif current_key and stripped and stripped.startswith('- '):
            # Sub-item under current field
            current_value.append(stripped[2:])
        elif current_key and stripped and not stripped.startswith('#'):
            # Continuation line
            current_value.append(stripped)
    
    if current_key:
        fields[current_key] = '\n'.join(current_value).strip()
    
    return fields


def _parse_table(lines: list[str]) -> dict | None:
    """Parse markdown table lines into structured dict."""
    if len(lines) < 2:
        return None
    
    # Parse header
    header_line = lines[0].strip()
    headers = [cell.strip() for cell in header_line.split('|') if cell.strip()]
    
    # Skip separator line (line 1)
    # Parse data rows
    rows = []
    for line in lines[2:]:
        stripped = line.strip()
        if not stripped or not '|' in stripped:
            continue
        cells = [cell.strip() for cell in stripped.split('|') if cell.strip() or stripped.count('|') > len(headers)]
        # Handle empty cells properly
        raw_cells = stripped.split('|')
        if raw_cells and not raw_cells[0].strip():
            raw_cells = raw_cells[1:]
        if raw_cells and not raw_cells[-1].strip():
            raw_cells = raw_cells[:-1]
        cells = [c.strip() for c in raw_cells]
        
        if cells:
            rows.append(cells)
    
    return {
        "type": "table",
        "headers": headers,
        "rows": rows,
    }


def extract_badges(text: str) -> list[dict]:
    """Extract badge values from text like {badge:value} or inline enum values."""
    badges = []
    # Explicit badge syntax
    for match in re.finditer(r'\{(\w+):(\w[\w-]*)\}', text):
        badges.append({"field": match.group(1), "value": match.group(2)})
    return badges


def extract_provenance(text: str) -> tuple[str, str | None]:
    """Extract provenance label and return (clean_text, provenance_type).
    
    provenance_type: "sales", "web", or None (AI inferred / no label)
    """
    if '[销售确认]' in text:
        return text.replace('[销售确认]', '').strip(), "sales"
    if '[网络搜索]' in text:
        return text.replace('[网络搜索]', '').strip(), "web"
    if '[AI推断]' in text:
        return text.replace('[AI推断]', '').strip(), "ai"
    return text, None


def get_doc_type(frontmatter: dict) -> str:
    """Get normalized document type from frontmatter."""
    return frontmatter.get("type", "unknown")


def get_section_by_title(sections: list[dict], title_fragment: str) -> dict | None:
    """Find a section by partial title match (case-insensitive)."""
    title_lower = title_fragment.lower()
    for section in sections:
        if title_lower in section["title"].lower() or title_lower in section["raw_title"].lower():
            return section
    return None
