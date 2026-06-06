"""Tests for shared.parse — markdown parsing into structured dicts."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.parse import (
    parse_markdown,
    extract_badges,
    extract_provenance,
    get_doc_type,
    get_section_by_title,
)


SAMPLE_CP = """\
---
type: call-plan
customer: Acme Corp
opportunity: Cloud Migration
meeting_title: Technical Deep Dive
date: 2026-05-20
time: "14:00"
format: Online
stage: Technical Validation
version: "1.0"
---

## 🎯 Target Meeting Outcomes

- Validate technical architecture fit
- Confirm POC scope and timeline

## ✅ Success Criteria

### 🟢 Ideal Outcome
- Customer commits to 2-week POC
- Technical decision-maker expresses strong support

### 🟡 Acceptable Outcome
- Customer agrees to review POC proposal internally

### ⚪ Minimum Outcome
- Clear understanding of decision criteria

## 👥 Customer Attendees

### Zhang Wei
- **Title:** CTO
- **Stance:** supporter
- **Role:** decision-maker
- **Focus & Priorities:** Cloud-native architecture, cost optimization [销售确认]
- **Communication Approach:** Data-driven, prefers concise presentations
- **🎯 Our Goal:** Secure commitment to POC timeline

### Li Ming
- **Title:** VP Engineering
- **Stance:** neutral
- **Role:** technical-evaluator
- **Focus & Priorities:** Migration risk, team readiness [AI推断]
- **Communication Approach:** Detail-oriented, wants to see proof points
- **🎯 Our Goal:** Address migration concerns with reference architecture

## 🏢 AWS Team

| Role | Name | Focus |
|------|------|-------|
| SA | Wang Lei | Technical architecture |
| AM | Sarah Chen | Relationship management |

## 📋 Information Exchange

### Questions to Ask
- What is your current deployment frequency?
- Have you evaluated other cloud providers?

### Information to Deliver
- Migration reference architecture for similar companies
- TCO comparison framework

## ⚠️ Potential Objections & Responses

### "We're concerned about migration downtime"
- **Category:** risk-trust
- **Likely From:** Li Ming (VP Engineering)
- **Response:** Present zero-downtime migration pattern with case study
- **Plan B:** Offer phased migration approach starting with non-critical workloads

### "Our team lacks cloud expertise"
- **Category:** capability
- **Likely From:** Zhang Wei (CTO)
- **Response:** AWS Training & Certification program + dedicated TAM support
- **Plan B:** Propose managed services to reduce operational burden

## 📅 Meeting Agenda

| Time | Topic | Purpose | Owner |
|------|-------|---------|-------|
| 14:00 | Opening & Context | Set objectives | SA |
| 14:15 | Architecture Deep Dive | Technical validation | SA |
| 14:45 | Q&A + Concerns | Address objections | All |
| 15:00 | Next Steps | Confirm POC path | AM |

## 🚀 Potential Next Steps

### ✅ If Yes (customer ready)
- Schedule POC kickoff within 2 weeks
- Share POC success criteria document

### ⏳ If Maybe (needs more time)
- Send follow-up reference architecture
- Arrange call with AWS reference customer

### 🚪 If Not Ready
- Identify specific blockers
- Propose smaller proof-of-value exercise
"""


def test_parse_frontmatter():
    doc = parse_markdown(SAMPLE_CP)
    fm = doc["frontmatter"]
    assert fm["type"] == "call-plan"
    assert fm["customer"] == "Acme Corp"
    assert fm["stage"] == "Technical Validation"
    assert str(fm["date"]) == "2026-05-20"


def test_parse_sections_count():
    doc = parse_markdown(SAMPLE_CP)
    titles = [s["title"] for s in doc["sections"]]
    assert "Target Meeting Outcomes" in titles
    assert "Success Criteria" in titles
    assert "Customer Attendees" in titles
    assert "AWS Team" in titles
    assert "Information Exchange" in titles
    assert "Potential Objections & Responses" in titles
    assert "Meeting Agenda" in titles
    assert "Potential Next Steps" in titles


def test_parse_emoji_extraction():
    doc = parse_markdown(SAMPLE_CP)
    target_section = get_section_by_title(doc["sections"], "Target Meeting Outcomes")
    assert target_section is not None
    assert target_section["emoji"] == "🎯"
    assert target_section["title"] == "Target Meeting Outcomes"


def test_parse_stakeholder_card():
    doc = parse_markdown(SAMPLE_CP)
    attendees = get_section_by_title(doc["sections"], "Customer Attendees")
    cards = [b for b in attendees["content"] if b.get("type") == "stakeholder_card"]
    assert len(cards) == 2

    zhang = cards[0]
    assert zhang["name"] == "Zhang Wei"
    assert zhang["stance"] == "supporter"
    assert zhang["role"] == "decision-maker"
    assert "Cloud-native" in zhang["focus"]

    li = cards[1]
    assert li["name"] == "Li Ming"
    assert li["stance"] == "neutral"
    assert li["role"] == "technical-evaluator"


def test_parse_table():
    doc = parse_markdown(SAMPLE_CP)
    aws_team = get_section_by_title(doc["sections"], "AWS Team")
    tables = [b for b in aws_team["content"] if b.get("type") == "table"]
    assert len(tables) == 1
    assert tables[0]["headers"] == ["Role", "Name", "Focus"]
    assert len(tables[0]["rows"]) == 2
    assert tables[0]["rows"][0][1] == "Wang Lei"


def test_parse_objection_card():
    doc = parse_markdown(SAMPLE_CP)
    objections = get_section_by_title(doc["sections"], "Potential Objections")
    cards = [b for b in objections["content"] if b.get("type") == "objection"]
    assert len(cards) == 2
    assert cards[0]["category"] == "risk-trust"
    assert "Li Ming" in cards[0]["likely_from"]
    assert cards[1]["category"] == "capability"


def test_parse_bullet_list():
    doc = parse_markdown(SAMPLE_CP)
    target = get_section_by_title(doc["sections"], "Target Meeting Outcomes")
    bullets = [b for b in target["content"] if b.get("type") == "bullet_list"]
    assert len(bullets) == 1
    assert len(bullets[0]["items"]) == 2


def test_parse_success_tiers():
    doc = parse_markdown(SAMPLE_CP)
    criteria = get_section_by_title(doc["sections"], "Success Criteria")
    subsections = [b for b in criteria["content"] if b.get("type") == "subsection"]
    assert len(subsections) == 3


def test_extract_badges():
    badges = extract_badges("The stance is {stance:champion} and role is {role:decision-maker}")
    assert len(badges) == 2
    assert badges[0] == {"field": "stance", "value": "champion"}
    assert badges[1] == {"field": "role", "value": "decision-maker"}


def test_extract_provenance():
    text, prov = extract_provenance("Cloud expertise required [销售确认]")
    assert text == "Cloud expertise required"
    assert prov == "sales"

    text2, prov2 = extract_provenance("Market growing at 15% [网络搜索]")
    assert text2 == "Market growing at 15%"
    assert prov2 == "web"

    text3, prov3 = extract_provenance("Likely interested in cost savings [AI推断]")
    assert text3 == "Likely interested in cost savings"
    assert prov3 == "ai"

    text4, prov4 = extract_provenance("No provenance label here")
    assert text4 == "No provenance label here"
    assert prov4 is None


def test_get_doc_type():
    assert get_doc_type({"type": "call-plan"}) == "call-plan"
    assert get_doc_type({"type": "engagement-plan"}) == "engagement-plan"
    assert get_doc_type({}) == "unknown"


def test_get_section_by_title_partial_match():
    doc = parse_markdown(SAMPLE_CP)
    section = get_section_by_title(doc["sections"], "Objection")
    assert section is not None
    assert "Objections" in section["title"]


# ---- EP Parse Tests ----

SAMPLE_EP = """---
type: engagement-plan
customer: Acme Corp
opportunity: Cloud Migration Phase 2
stage: Qualify
source: inbound
created: 2026-01-15
version: "1.0"
---

## 1. 📊 Opportunity Snapshot

### Why Now

Customer's current contract expires Q3.

### Deal Objective

$2M TCV cloud migration.

### Win Strategy

AWS-primary positioning with open standards.

## 2. 👥 Engagement Plan

### Key Stakeholders

### Zhang Wei
- **Title:** CTO
- **Stance:** champion
- **Role:** decision-maker
- **What They Care About:** Innovation, cost savings

### Engagement Roadmap

### Milestone 1: Executive Alignment
- **Status:** done
- **👤 Stakeholders:** Zhang Wei
- **📅 Timeline:** Week 1-2

### Milestone 2: Technical Validation
- **Status:** next
- **👤 Stakeholders:** Li Ming
- **📅 Timeline:** Week 3-4

### Estimate & Contingency

TCV: $2M over 3 years. Plan B: Start with $500K Phase 1.

### Next Milestone Detail

Focus on technical deep dive with VP Engineering.

## 3. 📝 Execution Log

### Engagement #1 - 2026-01-20 - Zhang Wei, Li Ming

| Field | Details |
|-------|---------|
| **Planned** | Intro meeting, establish rapport |
| **Actual** | Strong alignment, CTO offered to champion |
| **Key Learnings** | Budget already approved at board level |
"""


def test_parse_ep_sections():
    doc = parse_markdown(SAMPLE_EP)
    titles = [s["title"] for s in doc["sections"]]
    assert "Opportunity Snapshot" in titles
    assert "Engagement Plan" in titles
    assert "Execution Log" in titles


def test_parse_ep_emoji():
    doc = parse_markdown(SAMPLE_EP)
    opp = get_section_by_title(doc["sections"], "Opportunity Snapshot")
    assert opp["emoji"] == "📊"
    eng = get_section_by_title(doc["sections"], "Engagement Plan")
    assert eng["emoji"] == "👥"


def test_parse_ep_subsections():
    doc = parse_markdown(SAMPLE_EP)
    opp = get_section_by_title(doc["sections"], "Opportunity Snapshot")
    subsections = [b for b in opp["content"] if b.get("type") == "subsection"]
    sub_titles = [s["title"] for s in subsections]
    assert "Why Now" in sub_titles
    assert "Deal Objective" in sub_titles
    assert "Win Strategy" in sub_titles


# ---- EB Parse Tests ----

SAMPLE_EB = """---
type: executive-briefing
customer: Acme Corp
opportunity: Cloud Migration Phase 2
meeting_title: CTO Quarterly Review
date: 2026-03-20
format: Video
stage: Prove
version: "1.0"
---

## 1. 📋 Meeting Logistics

| Field | Details |
|-------|---------|
| **Date & Time** | 2026-03-20, 10:00 CST |
| **Format** | Video (Chime) |
| **Requested By** | Customer (CTO office) |

## 2. 👤 Customer Attendee Background

### Company Profile

| Dimension | Details |
|-----------|---------|
| **Industry** | Financial Services |
| **Strategic Priorities** | Digital transformation |

### Liu Jian — CTO

| Dimension | Details |
|-----------|---------|
| **Role & Influence** | CTO — decision-maker |
| **Current Stance** | supporter |
| **Communication Style** | Data-driven |

## 3. 🎯 Meeting Objectives

### Objective 1: Confirm Phase 2 scope

| Field | Details |
|-------|---------|
| **Context** | Phase 1 delivered early |
| **Talking Points** | ROI data, timeline options |
| **Asks** | Q2 start confirmation |

## 4. 📊 AWS Account Background

| Dimension | Details |
|-----------|---------|
| **Geo / Segment** | China / Enterprise |
| **Current Spend** | $2.4M ARR |

## 5. 📎 Appendix

Previous meeting notes from Feb QBR.
"""


def test_parse_eb_sections():
    doc = parse_markdown(SAMPLE_EB)
    titles = [s["title"] for s in doc["sections"]]
    assert "Meeting Logistics" in titles
    assert "Customer Attendee Background" in titles
    assert "Meeting Objectives" in titles
    assert "AWS Account Background" in titles
    assert "Appendix" in titles


def test_parse_eb_emoji():
    doc = parse_markdown(SAMPLE_EB)
    logistics = get_section_by_title(doc["sections"], "Meeting Logistics")
    assert logistics["emoji"] == "📋"
    objectives = get_section_by_title(doc["sections"], "Meeting Objectives")
    assert objectives["emoji"] == "🎯"


def test_parse_eb_table():
    doc = parse_markdown(SAMPLE_EB)
    account = get_section_by_title(doc["sections"], "AWS Account Background")
    tables = [b for b in account["content"] if b.get("type") == "table"]
    assert len(tables) == 1
    assert "Dimension" in tables[0]["headers"]


# ---- PMR Parse Tests ----

SAMPLE_PMR = """---
type: post-meeting-report
customer: Acme Corp
opportunity: Cloud Migration Phase 2
meeting_title: CTO Quarterly Review
date: 2026-03-20
source: call-plan
stage: Prove
version: "1.0"
---

## 1. 📊 Outcome Assessment

| Objective | Target Outcome | Actual Outcome | Result |
|-----------|---------------|----------------|--------|
| Confirm Phase 2 scope | Verbal commitment | CTO confirmed Q2 start | achieved |
| Address governance concern | Framework agreement | Accepted AWS-primary | achieved |

## 2. 🔍 Meeting Insights

### Customer Sentiment

| Attendee | Pre-Meeting Stance | Post-Meeting Stance |
|----------|-------------------|---------------------|
| Liu Jian | supporter | champion |

### Key Findings

| # | Finding | Source | Implication |
|---|---------|--------|-------------|
| 1 | Budget increased 15% | CTO [销售确认] | Not a blocker |

## 3. ✏️ What Changed — EP Update

| Dimension | Change Type | Before | After | Evidence |
|-----------|-------------|--------|-------|----------|
| Stakeholder: Liu Jian | update | supporter | champion | Offered to sponsor |
| Timeline | update | Q2 tentative | Q2 confirmed | Verbal commitment |

## 4. 📋 Next Steps — Planned vs Actual

| Planned | Actual | Delta |
|---------|--------|-------|
| SOW in 2 weeks | Next week | Ahead |

### Action Items

| # | Action | Owner | ETA | Priority | Status |
|---|--------|-------|-----|----------|--------|
| 1 | Send SOW draft | Sarah Chen | 2026-03-22 | high | pending |
| 2 | Schedule deep-dive | David Park | 2026-03-25 | high | pending |

## 5. ✉️ Customer Recap Email (Handoff)

Thanks for the productive meeting. Key takeaways and next steps...
"""


def test_parse_pmr_sections():
    doc = parse_markdown(SAMPLE_PMR)
    titles = [s["title"] for s in doc["sections"]]
    assert "Outcome Assessment" in titles
    assert "Meeting Insights" in titles
    assert "What Changed" in titles or any("What Changed" in t for t in titles)
    assert any("Next Steps" in t for t in titles)
    assert any("Customer Recap" in t for t in titles)


def test_parse_pmr_emoji():
    doc = parse_markdown(SAMPLE_PMR)
    outcome = get_section_by_title(doc["sections"], "Outcome Assessment")
    assert outcome["emoji"] == "📊"
    insights = get_section_by_title(doc["sections"], "Meeting Insights")
    assert insights["emoji"] == "🔍"
    changed = get_section_by_title(doc["sections"], "What Changed")
    assert changed["emoji"] == "✏️"


def test_parse_pmr_table():
    doc = parse_markdown(SAMPLE_PMR)
    outcome = get_section_by_title(doc["sections"], "Outcome Assessment")
    tables = [b for b in outcome["content"] if b.get("type") == "table"]
    assert len(tables) == 1
    assert "Result" in tables[0]["headers"]
    assert len(tables[0]["rows"]) == 2


def test_parse_pmr_provenance_in_findings():
    doc = parse_markdown(SAMPLE_PMR)
    insights = get_section_by_title(doc["sections"], "Meeting Insights")
    # Find tables in subsections
    content_str = str(insights)
    assert "销售确认" in content_str

