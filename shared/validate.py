"""
validate.py — Schema validation + auto-fix for structured markdown documents.

Key behaviors:
- Checks required sections per document type
- Validates badge values against enums
- Auto-inserts missing sections with [待补充] placeholder
- Flags invalid badge values (renders as gray fallback)
- Returns validation report with warnings
"""

import re
from typing import Any

from .parse import get_doc_type, get_section_by_title


# ===== Enum Definitions =====

STANCE_VALUES = {"champion", "sponsor", "supporter", "neutral", "non-supporter", "adversary", "unknown"}
ROLE_VALUES = {
    "decision-maker", "technical-evaluator", "evaluator", "influencer", "end-user",
    "champion", "blocker", "sponsor", "economic-buyer", "procurement", "eb"
}
PRIORITY_VALUES = {"high", "medium", "low", "must-meet", "important", "nice-to-have"}
MILESTONE_STATUS_VALUES = {"done", "next", "planned", "skipped"}
CONFIDENCE_VALUES = {"high", "medium", "low"}
OBJECTION_CATEGORY_VALUES = {"risk-trust", "risk/trust", "capability", "authority", "authority/process", "price-value", "price/value", "price/competition", "status-quo", "status quo"}
RESULT_VALUES = {"achieved", "partial", "not-achieved"}
GAP_STATUS_VALUES = {"answered", "unanswered", "still a gap"}
CHANGE_TYPE_VALUES = {"update", "add", "remove", "no-change", "confirm", "新增", "更新", "删除", "确认"}
ACTION_STATUS_VALUES = {"pending", "open", "in-progress", "in progress", "done", "overdue"}
ACTION_PRIORITY_VALUES = {"high", "medium", "low"}
NEXT_STEP_TIER_VALUES = {"ideal", "acceptable", "minimum"}

ALL_BADGE_VALUES = (
    STANCE_VALUES | ROLE_VALUES | PRIORITY_VALUES | MILESTONE_STATUS_VALUES |
    CONFIDENCE_VALUES | OBJECTION_CATEGORY_VALUES | RESULT_VALUES |
    GAP_STATUS_VALUES | CHANGE_TYPE_VALUES | ACTION_STATUS_VALUES |
    ACTION_PRIORITY_VALUES | NEXT_STEP_TIER_VALUES
)

# ===== Required Sections Per Document Type =====

REQUIRED_SECTIONS = {
    # EP reference: ## 1. Opportunity Snapshot, ## 2. Engagement Plan, ## 3. Execution Log
    # Key Stakeholders, Roadmap, Estimate, Next Milestone are ### under ## 2
    "engagement-plan": [
        "Opportunity Snapshot",
        "Engagement Plan",
        "Execution Log",
    ],
    # CP reference: ## 1-7 (Meeting Details through Potential Next Steps)
    "call-plan": [
        "Meeting Details",
        "Target Meeting Outcomes",
        "Success Criteria",
        "Information Exchange",
        "Potential Objections & Responses",
        "Meeting Agenda",
        "Potential Next Steps",
    ],
    # EB reference: ## 1-5 + subsections under ## 3 (Anticipated Concerns, Proposed Next Steps)
    "executive-briefing": [
        "Meeting Logistics",
        "Customer Attendee Background",
        "Meeting Objectives",
        "AWS Account Background",
        "Appendix",
    ],
    # PMR reference: ## 1-5
    "post-meeting-report": [
        "Outcome Assessment",
        "Meeting Insights",
        "What Changed",
        "Next Steps",
        "Customer Recap Email",
    ],
}

# Aliases: common LLM variations → canonical required section name(s)
# If an existing section title matches an alias, it counts as the required section(s).
# Values can be a string (single target) or list (multiple targets satisfied by one section).
SECTION_ALIASES = {
    # EP — subsections of "Engagement Plan"
    "key stakeholders": ["Engagement Plan"],
    "stakeholders": ["Engagement Plan"],
    "engagement roadmap": ["Engagement Plan"],
    "roadmap": ["Engagement Plan"],
    "estimate & contingency": ["Engagement Plan"],
    "estimate": ["Engagement Plan"],
    "next milestone detail": ["Engagement Plan"],
    "next milestone": ["Engagement Plan"],
    # CP
    "agenda": ["Meeting Agenda"],
    "information gaps": ["Information Exchange"],
    "questions": ["Information Exchange"],
    "objection handling": ["Potential Objections & Responses"],
    "objections": ["Potential Objections & Responses"],
    "next steps": ["Potential Next Steps"],
    "conversation strategy": ["Meeting Agenda"],
    # EB
    "account background": ["AWS Account Background"],
    "attendee background": ["Customer Attendee Background"],
    "objectives": ["Meeting Objectives"],
    "anticipated concerns": ["Meeting Objectives"],
    "proposed next steps": ["Meeting Objectives"],
    "landmines": ["Meeting Objectives"],
    "company profile": ["Customer Attendee Background"],
    # PMR
    "action items": ["Next Steps"],
    "follow-up email draft": ["Customer Recap Email"],
    "follow-up email": ["Customer Recap Email"],
    "customer recap": ["Customer Recap Email"],
    "recap email": ["Customer Recap Email"],
    "customer recap email (handoff)": ["Customer Recap Email"],
    "ep update": ["What Changed"],
    "changes": ["What Changed"],
    "ep changes": ["What Changed"],
    "stakeholder updates": ["What Changed"],
    "what changed — ep update": ["What Changed"],
    "next steps — planned vs actual": ["Next Steps"],
    "planned vs actual": ["Next Steps"],
}

# Required frontmatter fields per type
REQUIRED_FRONTMATTER = {
    "engagement-plan": ["type", "customer", "opportunity", "stage", "source", "created", "version"],
    "call-plan": ["type", "customer", "opportunity", "meeting_title", "date", "time", "format", "stage", "version"],
    "executive-briefing": ["type", "customer", "opportunity", "meeting_title", "date", "time", "format", "classification", "requested_by", "version"],
    "post-meeting-report": ["type", "customer", "opportunity", "meeting_title", "date", "recorded_by", "related_document", "version"],
}


def validate(doc: dict) -> dict:
    """Validate a parsed document and auto-fix minor issues.
    
    Args:
        doc: Parsed document dict from parse.py
        
    Returns:
        {
            "valid": bool,
            "warnings": [str],
            "errors": [str],
            "auto_fixes": [str],   # descriptions of auto-fixes applied
            "doc": dict,           # the (possibly modified) document
        }
    """
    warnings = []
    errors = []
    auto_fixes = []
    
    frontmatter = doc.get("frontmatter", {})
    sections = doc.get("sections", [])
    doc_type = get_doc_type(frontmatter)
    
    # 1. Validate frontmatter
    _validate_frontmatter(frontmatter, doc_type, warnings, errors)
    
    # 2. Check required sections and auto-fix missing ones
    sections = _check_required_sections(sections, doc_type, warnings, auto_fixes)
    doc["sections"] = sections
    
    # 3. Validate badge values
    _validate_badges(sections, warnings)
    
    # 4. Type-specific validations
    if doc_type == "engagement-plan":
        _validate_ep(sections, warnings, errors)
    elif doc_type == "call-plan":
        _validate_cp(sections, warnings, errors)
    elif doc_type == "executive-briefing":
        _validate_eb(sections, frontmatter, warnings, errors)
    elif doc_type == "post-meeting-report":
        _validate_pmr(sections, warnings, errors)
    
    valid = len(errors) == 0
    
    return {
        "valid": valid,
        "warnings": warnings,
        "errors": errors,
        "auto_fixes": auto_fixes,
        "doc": doc,
    }


def _validate_frontmatter(frontmatter: dict, doc_type: str, warnings: list, errors: list):
    """Check required frontmatter fields."""
    required = REQUIRED_FRONTMATTER.get(doc_type, [])
    for field in required:
        if field not in frontmatter or not frontmatter[field]:
            if field == "type":
                errors.append(f"Missing required frontmatter field: {field}")
            else:
                warnings.append(f"Missing frontmatter field: {field}")


def _check_required_sections(sections: list, doc_type: str, warnings: list, auto_fixes: list) -> list:
    """Check for required sections, auto-insert missing ones with placeholder.
    
    Matching logic (in order):
    1. Substring match: req_title is a substring of existing title (or vice-versa)
    2. Alias match: existing title matches a known alias for the required section
    """
    required = REQUIRED_SECTIONS.get(doc_type, [])
    
    existing_titles = set()
    for s in sections:
        existing_titles.add(s["title"].lower())
        existing_titles.add(s["raw_title"].lower())
    
    # Build reverse alias lookup: which required sections are satisfied by existing titles?
    alias_satisfied = set()
    for existing in existing_titles:
        # Check if this existing title is an alias for a required section
        for alias_key, canonicals in SECTION_ALIASES.items():
            if alias_key in existing or existing in alias_key:
                for c in canonicals:
                    alias_satisfied.add(c.lower())
    
    for req_title in required:
        found = False
        req_lower = req_title.lower()
        
        # Strategy 1: substring match (bidirectional)
        for existing in existing_titles:
            if req_lower in existing or existing in req_lower:
                found = True
                break
        
        # Strategy 2: alias match
        if not found and req_lower in alias_satisfied:
            found = True
        
        if not found:
            # Auto-insert placeholder section
            placeholder = {
                "emoji": "📌",
                "title": req_title,
                "raw_title": f"📌 {req_title}",
                "content": [{"type": "paragraph", "text": "[待补充]"}],
            }
            sections.append(placeholder)
            auto_fixes.append(f"Auto-inserted missing section: {req_title}")
            warnings.append(f"Section '{req_title}' was missing — placeholder added")
    
    return sections


def _validate_badges(sections: list, warnings: list):
    """Walk through all content blocks and validate badge-like values."""
    for section in sections:
        for block in section.get("content", []):
            _validate_block_badges(block, warnings)


def _extract_badge_value(raw: str) -> str:
    """Extract just the badge/enum value from 'Value — explanation' pattern.
    
    Reference templates use format like:
    - "Supporter — evidence explaining why"
    - "Must Meet — reason for priority"
    - "Technical Evaluator — specific function"
    
    Returns the lowercase first segment before ' — ', ' - ', or ' – '.
    """
    if not raw:
        return ""
    v = raw.strip()
    # Split on em-dash, en-dash, or hyphen-with-spaces
    for sep in [' — ', ' – ', ' - ']:
        if sep in v:
            v = v.split(sep)[0]
            break
    return v.lower().strip()


def _validate_block_badges(block: dict, warnings: list):
    """Validate badge values in a single content block."""
    block_type = block.get("type", "")
    
    if block_type == "stakeholder_card":
        # Extract badge value from "Value — explanation" pattern
        stance = _extract_badge_value(block.get("stance", ""))
        if stance and stance not in STANCE_VALUES:
            warnings.append(f"Invalid stance value '{stance}' for {block.get('name', '?')}")
        
        role = _extract_badge_value(block.get("role", ""))
        if role and role not in ROLE_VALUES:
            warnings.append(f"Invalid role value '{role}' for {block.get('name', '?')}")
        
        priority = _extract_badge_value(block.get("priority", ""))
        if priority and priority not in PRIORITY_VALUES:
            warnings.append(f"Invalid priority value '{priority}' for {block.get('name', '?')}")
    
    elif block_type == "milestone":
        status = block.get("status", "").lower().strip()
        if status and status not in MILESTONE_STATUS_VALUES:
            warnings.append(f"Invalid milestone status '{status}' for milestone {block.get('number', '?')}")
    
    elif block_type == "objection":
        category = block.get("category", "").lower().strip()
        if category and category not in OBJECTION_CATEGORY_VALUES:
            warnings.append(f"Invalid objection category '{category}' for '{block.get('title', '?')}'")
    
    elif block_type == "subsection":
        for sub_block in block.get("content", []):
            _validate_block_badges(sub_block, warnings)


def _validate_ep(sections: list, warnings: list, errors: list):
    """Engagement Plan specific validations."""
    # EP structure: Key Stakeholders and Roadmap are subsections under "Engagement Plan"
    # Need to search within the Engagement Plan section's content blocks
    engagement_plan = get_section_by_title(sections, "Engagement Plan")
    
    # Check for at least 2 stakeholders
    stakeholders_sub = _get_subsection(engagement_plan, "Key Stakeholders") if engagement_plan else None
    # Also try top-level for backward compatibility
    if not stakeholders_sub:
        stakeholders_sub = get_section_by_title(sections, "Key Stakeholders")
    if stakeholders_sub:
        cards = [b for b in stakeholders_sub.get("content", []) if b.get("type") == "stakeholder_card"]
        # Also count table-format stakeholders (reference format: **Name** paragraph + table pairs)
        tables = [b for b in stakeholders_sub.get("content", []) if b.get("type") == "table"]
        stakeholder_count = len(cards) if cards else len(tables)
        if stakeholder_count < 2:
            warnings.append(f"EP should have at least 2 stakeholders (found {stakeholder_count})")
    
    # Check for exactly 1 "next" milestone
    roadmap_sub = _get_subsection(engagement_plan, "Engagement Roadmap") if engagement_plan else None
    if not roadmap_sub:
        roadmap_sub = get_section_by_title(sections, "Engagement Roadmap")
    if roadmap_sub:
        milestones = [b for b in roadmap_sub.get("content", []) if b.get("type") == "milestone"]
        if milestones:
            next_count = sum(1 for m in milestones if m.get("status", "").lower() == "next")
            if next_count != 1:
                warnings.append(f"EP Roadmap should have exactly 1 'next' milestone (found {next_count})")
        else:
            # Table-format roadmap: check Status column for "Next" 
            tables = [b for b in roadmap_sub.get("content", []) if b.get("type") == "table"]
            for table in tables:
                headers = [h.lower() for h in table.get("headers", [])]
                if "status" in headers:
                    status_idx = headers.index("status")
                    next_count = sum(1 for row in table.get("rows", []) if "next" in row[status_idx].lower())
                    if next_count != 1:
                        warnings.append(f"EP Roadmap should have exactly 1 'next' milestone (found {next_count})")


def _get_subsection(section: dict | None, title_fragment: str) -> dict | None:
    """Find a subsection block within a section by partial title match."""
    if not section:
        return None
    title_lower = title_fragment.lower()
    for block in section.get("content", []):
        if block.get("type") == "subsection":
            block_title = block.get("title", "").lower()
            if title_lower in block_title or block_title in title_lower:
                return block
    return None


def _validate_cp(sections: list, warnings: list, errors: list):
    """Call Plan specific validations."""
    # Check for at least 1 attendee
    attendees_section = get_section_by_title(sections, "Customer Attendees")
    if attendees_section:
        cards = [b for b in attendees_section["content"] if b.get("type") == "stakeholder_card"]
        if len(cards) < 1:
            warnings.append("CP should have at least 1 customer attendee")
    
    # Check success criteria has 3 tiers (either as subsections or as table rows)
    criteria_section = get_section_by_title(sections, "Success Criteria")
    if criteria_section:
        tiers = [b for b in criteria_section["content"] if b.get("type") == "subsection"]
        tables = [b for b in criteria_section["content"] if b.get("type") == "table"]
        # Accept either 3 subsections OR a table with 3+ rows
        if len(tiers) < 3 and not any(len(t.get("rows", [])) >= 3 for t in tables):
            warnings.append(f"CP Success Criteria should have 3 tiers (found {len(tiers)} subsections, {sum(len(t.get('rows',[])) for t in tables)} table rows)")


def _validate_eb(sections: list, frontmatter: dict, warnings: list, errors: list):
    """Executive Briefing specific validations."""
    # Check classification field
    if frontmatter.get("classification") != "INTERNAL USE ONLY — AWS Confidential":
        warnings.append("EB classification should be 'INTERNAL USE ONLY — AWS Confidential'")
    
    # Check for at least 1 customer attendee
    attendees_section = get_section_by_title(sections, "Customer Attendee Background")
    if attendees_section:
        persons = [b for b in attendees_section["content"] if b.get("type") == "eb_person"]
        if len(persons) < 1:
            warnings.append("EB should have at least 1 customer attendee background")


def _validate_pmr(sections: list, warnings: list, errors: list):
    """Post-Meeting Report specific validations."""
    # Check outcome assessment has at least 1 row
    outcome_section = get_section_by_title(sections, "Outcome Assessment")
    if outcome_section:
        tables = [b for b in outcome_section["content"] if b.get("type") == "table"]
        if not tables:
            warnings.append("PMR Outcome Assessment should have at least 1 outcome row")
        elif tables and len(tables[0].get("rows", [])) < 1:
            warnings.append("PMR Outcome Assessment table has no data rows")


def normalize_badge_value(value: str) -> str:
    """Normalize a badge value for CSS class generation.
    
    Returns the CSS-safe class suffix or 'fallback' if unrecognized.
    """
    v = value.lower().strip()
    if v in ALL_BADGE_VALUES:
        return v
    return "fallback"
