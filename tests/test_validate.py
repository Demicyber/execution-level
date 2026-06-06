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
