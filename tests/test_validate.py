"""Tests for shared.validate — schema validation and auto-fix."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.parse import parse_markdown
from shared.validate import validate, normalize_badge_value


MINIMAL_CP = """\
---
type: call-plan
customer: Test Corp
opportunity: Test Opp
meeting_title: Test Meeting
date: 2026-06-01
time: "10:00"
format: Online
stage: Qualified
version: "1.0"
---

## 🎯 Target Meeting Outcomes

- Validate pain points

## ✅ Success Criteria

### 🟢 Ideal
- Full commitment

### 🟡 Acceptable
- Verbal agreement

### ⚪ Minimum
- Understanding of needs

## 👥 Customer Attendees

### John Smith
- **Title:** CTO
- **Stance:** champion
- **Role:** decision-maker
- **Focus & Priorities:** Cost reduction
- **Communication Approach:** Direct
- **🎯 Our Goal:** Get technical buy-in

## 🏢 AWS Team

| Role | Name |
|------|------|
| SA | Alice |

## 📋 Information Exchange

### Questions to Ask
- Current infrastructure?

## ⚠️ Potential Objections & Responses

### "Too expensive"
- **Category:** price-value
- **Likely From:** CFO
- **Response:** Show TCO analysis
- **Plan B:** Offer pilot at reduced scope

## 📅 Meeting Agenda

| Time | Topic |
|------|-------|
| 10:00 | Intro |

## 🚀 Potential Next Steps

- Schedule follow-up
"""


def test_validate_valid_cp():
    doc = parse_markdown(MINIMAL_CP)
    result = validate(doc)
    assert result["valid"] is True
    assert len(result["errors"]) == 0


def test_validate_missing_sections_auto_fix():
    md = """\
---
type: call-plan
customer: Test
opportunity: Opp
meeting_title: Meeting
date: 2026-06-01
time: "10:00"
format: Online
stage: Qualified
version: "1.0"
---

## 🎯 Target Meeting Outcomes

- Something
"""
    doc = parse_markdown(md)
    result = validate(doc)
    assert result["valid"] is True
    assert len(result["auto_fixes"]) > 0
    section_titles = [s["title"] for s in result["doc"]["sections"]]
    assert "Success Criteria" in section_titles


def test_validate_missing_type_passes_as_unknown():
    md = """\
---
customer: Test
---

## Some Section

Content here.
"""
    doc = parse_markdown(md)
    result = validate(doc)
    # Unknown doc type has no required sections/fields, so passes
    assert result["valid"] is True
    assert len(result["errors"]) == 0


def test_validate_invalid_stance_warning():
    md = """\
---
type: engagement-plan
customer: Test
opportunity: Opp
stage: Prospect
source: outbound
created: 2026-01-01
version: "1.0"
---

## 📊 Opportunity Snapshot

Some context.

## 👥 Key Stakeholders

### Alice
- **Title:** CEO
- **Stance:** very-positive
- **Role:** decision-maker
- **What They Care About:** Growth

## 📍 Engagement Roadmap

### Milestone 1: Discovery
- **Status:** next
- **👤 Stakeholders:** Alice
- **📅 Timeline:** Week 1

## 🔍 Next Milestone Detail

Details here.

## 💰 Estimate & Contingency

TCV estimate.

## 📝 Execution Log

No entries yet.

## 📋 Change Log

Initial version.
"""
    doc = parse_markdown(md)
    result = validate(doc)
    assert result["valid"] is True
    assert any("Invalid stance" in w for w in result["warnings"])


def test_validate_invalid_milestone_status():
    md = """\
---
type: engagement-plan
customer: Test
opportunity: Opp
stage: Prospect
source: outbound
created: 2026-01-01
version: "1.0"
---

## 📊 Opportunity Snapshot

Context.

## 👥 Key Stakeholders

### Bob
- **Title:** VP
- **Stance:** neutral
- **Role:** influencer
- **What They Care About:** Efficiency

### Carol
- **Title:** Dir
- **Stance:** supporter
- **Role:** technical-evaluator
- **What They Care About:** Innovation

## 📍 Engagement Roadmap

### Milestone 1: Discovery
- **Status:** completed
- **👤 Stakeholders:** Bob

## 🔍 Next Milestone Detail

Details.

## 💰 Estimate & Contingency

Estimate.

## 📝 Execution Log

None.

## 📋 Change Log

Initial.
"""
    doc = parse_markdown(md)
    result = validate(doc)
    assert any("milestone status" in w.lower() for w in result["warnings"])


def test_normalize_badge_value():
    assert normalize_badge_value("champion") == "champion"
    assert normalize_badge_value("Champion") == "champion"
    assert normalize_badge_value("CHAMPION") == "champion"
    assert normalize_badge_value("invalid-thing") == "fallback"
    assert normalize_badge_value("high") == "high"
    assert normalize_badge_value("not-achieved") == "not-achieved"


def test_validate_section_alias_matching():
    md = """\
---
type: call-plan
customer: Test
opportunity: Opp
meeting_title: Meeting
date: 2026-06-01
time: "10:00"
format: Online
stage: Qualified
version: "1.0"
---

## 🎯 Target Meeting Outcomes
- Goal

## ✅ Success Criteria
### Ideal
- Win

## 👥 Attendees
### Someone
- **Title:** CTO
- **Stance:** neutral

## 📋 Questions
- What is your budget?

## ⚠️ Objection Handling
### Price concern
- **Category:** price-value
- **Likely From:** CFO
- **Response:** TCO
- **Plan B:** Pilot

## 📅 Agenda
| Time | Topic |
|------|-------|
| 10:00 | Start |

## 🚀 Next Steps
- Follow up
"""
    doc = parse_markdown(md)
    result = validate(doc)
    # "Attendees" should alias to "Customer Attendees"
    # "Questions" should alias to "Information Exchange"
    # "Objection Handling" should alias to "Potential Objections & Responses"
    # "Agenda" should alias to "Meeting Agenda"
    # "Next Steps" should alias to "Potential Next Steps"
    # Should not auto-insert these as missing
    auto_fix_titles = [af for af in result["auto_fixes"]]
    assert not any("Customer Attendees" in af for af in auto_fix_titles)
    assert not any("Information Exchange" in af for af in auto_fix_titles)
    assert not any("Meeting Agenda" in af for af in auto_fix_titles)


def test_validate_eb_basic():
    """Executive Briefing with all required sections passes."""
    md = """---
type: executive-briefing
customer: Test Corp
opportunity: Cloud Deal
meeting_title: CTO Review
date: 2026-06-01
format: Video
stage: Prove
version: "1.0"
---

## 1. 📋 Meeting Logistics

| Field | Details |
|-------|---------|
| **Date & Time** | 2026-06-01, 10:00 CST |
| **Format** | Video |

### AWS Attendees

| Name | Role |
|------|------|
| Sarah | AM — lead |

## 2. 👤 Customer Attendee Background

### Company Profile

| Dimension | Details |
|-----------|---------|
| **Industry** | Tech |

### John Smith — CEO

| Dimension | Details |
|-----------|---------|
| **Role & Influence** | CEO — decision-maker |
| **Current Stance** | supporter |

## 3. 🎯 Meeting Objectives

### Success Definition

Get commitment to next step.

### Objective 1: Confirm timeline

| Field | Details |
|-------|---------|
| **Context** | Q2 planning |
| **Talking Points** | ROI data |
| **Asks** | Timeline confirmation |

## 4. 📊 AWS Account Background

| Dimension | Details |
|-----------|---------|
| **Geo / Segment** | US / Enterprise |
| **Current Spend** | $1M ARR |

## 5. 📎 Appendix

Previous meeting notes.
"""
    doc = parse_markdown(md)
    result = validate(doc)
    assert result["valid"] is True
    # Should not have errors (warnings are OK)
    assert len(result["errors"]) == 0


def test_validate_eb_missing_section():
    """EB missing a required section triggers auto-fix."""
    md = """---
type: executive-briefing
customer: Test Corp
opportunity: Cloud Deal
meeting_title: CTO Review
date: 2026-06-01
format: Video
stage: Prove
version: "1.0"
---

## 1. 📋 Meeting Logistics

Basic info.

## 3. 🎯 Meeting Objectives

Goals here.
"""
    doc = parse_markdown(md)
    result = validate(doc)
    # Should auto-fix missing sections
    assert len(result["auto_fixes"]) > 0


def test_validate_pmr_basic():
    """Post-Meeting Report with all required sections passes."""
    md = """---
type: post-meeting-report
customer: Test Corp
opportunity: Cloud Deal
meeting_title: Technical Review
date: 2026-06-01
source: call-plan
stage: Prove
version: "1.0"
---

## 1. 📊 Outcome Assessment

| Objective | Target Outcome | Actual Outcome | Result |
|-----------|---------------|----------------|--------|
| Validate architecture | Sign-off | Approved | achieved |

## 2. 🔍 Meeting Insights

### Customer Sentiment

| Attendee | Pre-Meeting Stance | Post-Meeting Stance |
|----------|-------------------|---------------------|
| John | neutral | supporter |

### Key Findings

| # | Finding | Source | Implication |
|---|---------|--------|-------------|
| 1 | Budget approved | CTO [销售确认] | Can proceed |

## 3. ✏️ What Changed — EP Update

| Dimension | Change Type | Before | After | Evidence |
|-----------|-------------|--------|-------|----------|
| Timeline | update | Q3 | Q2 | CTO confirmed |

## 4. 📋 Next Steps — Planned vs Actual

| Planned | Actual | Delta |
|---------|--------|-------|
| SOW in 2 weeks | SOW next week | Ahead |

### Action Items

| # | Action | Owner | ETA | Priority | Status |
|---|--------|-------|-----|----------|--------|
| 1 | Send SOW | Sarah | 2026-06-05 | high | pending |

## 5. ✉️ Customer Recap Email (Handoff)

Thanks for the meeting. Key next steps...
"""
    doc = parse_markdown(md)
    result = validate(doc)
    assert result["valid"] is True
    assert len(result["errors"]) == 0

def test_validate_pmr_invalid_result_badge():
    """PMR with missing recommended frontmatter triggers warning."""
    md = """\
---
type: post-meeting-report
customer: Test Corp
opportunity: Cloud Deal
meeting_title: Review
date: 2026-06-01
source: call-plan
stage: Prove
version: "1.0"
---

## 1. 📊 Outcome Assessment

| Objective | Result |
|-----------|--------|
| Goal 1 | super-achieved |

## 2. 🔍 Meeting Insights

Findings.

## 3. ✏️ What Changed — EP Update

| Dimension | Change Type |
|-----------|-------------|
| Timeline | update |

## 4. 📋 Next Steps — Planned vs Actual

Actions.

## 5. ✉️ Customer Recap Email (Handoff)

Email draft.
"""
    doc = parse_markdown(md)
    result = validate(doc)
    # PMR should warn about missing recommended frontmatter fields
    assert any("recorded_by" in w or "related_document" in w for w in result["warnings"])

