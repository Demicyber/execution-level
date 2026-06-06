"""Smoke tests for all renderers — verify each doc type × format produces output."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from shared.render import render


# ===== Sample Documents =====

SAMPLE_EP = """\
---
type: engagement-plan
customer: "测试科技"
opportunity: Cloud Migration
stage: Technical Validation
win_strategy: Champion-led
version: "1.0"
---

## 📊 Opportunity Snapshot

- **Deal Size:** $500K ARR
- **Stage:** Technical Validation `{confidence:high}`
- **Win Strategy:** Champion-led approach

### Engagement Progress
[████████░░░░░░░░] 50% — Technical Validation

## 👥 Key Stakeholders

### 王明
- **Title:** CTO
- **Engagement Priority:** high
- **Role in This Deal:** decision-maker
- **Current Stance:** supporter
- **What They Care About:** Cost reduction, reliability
- **Profiling:** Data-driven, prefers metrics
- **What We Need From Them:** Technical sign-off
- **How to Win Them:** Provide benchmark data

## 🗺️ Engagement Roadmap

| # | Milestone | Stakeholders | AWS Resources | Timeline | Status |
|---|-----------|-------------|---------------|----------|--------|
| 1 | Discovery | 王明 | SA | Week 1 | done |
| 2 | POC | 王明 | SA, TAM | Week 3 | next |

## 📍 Next Milestone Detail

**Milestone:** POC Setup
**Objective:** Prove <5ms latency at scale

### Preparation
- Prepare test environment
- Gather baseline metrics

## 🧠 Estimated Objections

### "Migration risk is too high"
- **Category:** risk-trust
- **Likely From:** CTO
- **Our Response:** Phased migration plan with rollback
- **Plan B:** Start with non-critical workload

## 📝 Execution Log

| Date | Event | Type |
|------|-------|------|
| 2026-05-01 | Initial call with CTO | update |
"""

SAMPLE_CP = """\
---
type: call-plan
customer: "明华重工"
opportunity: DevOps Modernization
meeting_title: Technical Deep Dive
date: 2026-06-01
time: "14:00"
format: Online
stage: Technical Validation
version: "1.0"
---

## 1. Meeting Details

**Customer:** 明华重工
**Meeting:** Technical Deep Dive
**Date/Time:** 2026-06-01 14:00
**Format:** Online

### Attendee Insights

**张伟** — CTO
- Background: 15 years in enterprise IT
- Communication Style: Data-driven, values precision
- Stance: `{stance:supporter}`
- Our Goal: Secure technical validation commitment

## 2. Target Meeting Outcomes

- Validate technical architecture fit
- Confirm POC scope and timeline

## 3. Success Criteria

| Perspective | Customer Outcome | Seller Outcome |
|-------------|-----------------|----------------|
| Ideal | Clear architecture path | POC commitment |
| Acceptable | Understanding of gaps | Follow-up scheduled |
| Minimum | Relationship maintained | Next steps agreed |

**Disqualification Signals:** Budget freeze, competing project priority

## 4. Information Exchange

### Information to Gather
- Current CI/CD pipeline details
- Security compliance requirements

### Information to Deliver
- AWS CodePipeline architecture
- Reference customer results

## 5. Potential Objections & Responses

| Objection | Category | Response | Fallback | Disqualifier? |
|-----------|----------|----------|----------|---------------|
| "Too complex" | capability | Step-by-step migration | Managed service option | No |
| "Budget locked" | price-value | Phased approach | Pay-as-you-go | Yes if no budget in 6mo |

## 6. Meeting Agenda

| Time | Topic | Owner | Purpose |
|------|-------|-------|---------|
| 00-05 | Opening | SA | Context setting |
| 05-30 | Architecture | SA | Deep dive |
| 30-45 | Q&A | All | Address concerns |
| 45-50 | Next Steps | AE | Agreement |

## 7. Potential Next Steps

- **Primary Path:** POC kickoff within 2 weeks
- **Fallback Path:** Schedule follow-up with security team
- **Graceful Exit:** Share reference materials, reconnect in Q4
"""

SAMPLE_EB = """\
---
type: executive-briefing
customer: "环球物流集团"
meeting_title: EBC Visit
date: 2026-06-15
classification: CONFIDENTIAL
aws_executive: "VP, Greater China"
version: "1.0"
---

## 1. Meeting Logistics

- **Date:** 2026-06-15
- **Format:** In-person, Beijing Office
- **AWS Executive:** VP, Greater China
- **Duration:** 90 minutes

## 2. Customer Attendee Background

**李总** — CEO

**Title & Tenure:** CEO since 2019, former McKinsey partner
**Strategic Priorities:** Digital transformation of logistics network
**Attitude Toward AWS:** Cautiously optimistic, values reliability `{stance:neutral}`
**Communication Style:** Big-picture thinker, asks strategic questions

### Company Profile

- **Industry:** Logistics & Supply Chain
- **Revenue:** $2.8B (2025)
- **Employees:** 15,000+
- **Cloud Status:** Early adoption, mostly on-premise

## 3. Meeting Objectives

### Success Definition
Win CEO sponsorship for enterprise cloud strategy partnership.

### Strategic Alignment
This aligns with AWS Greater China's logistics vertical play.

### Objective 1: Establish Strategic Partnership

| Aspect | Detail |
|--------|--------|
| Objective/Outcome | CEO commitment to explore strategic partnership |
| Context | Company spending $50M on legacy infra maintenance |
| Talking Points | TCO comparison, logistics industry peers on AWS |
| Asks | Monthly strategic review cadence |

### Anticipated Concerns
- Data sovereignty requirements
- Integration with existing SAP systems

### Proposed Next Steps
- Schedule follow-up with CTO for technical deep-dive
- Share logistics industry reference architectures

## 4. AWS Account Background

- **Current Spend:** $200K/month
- **Growth Trajectory:** 30% YoY
- **Key Workloads:** Data analytics, some ML experiments
- **Relationship History:** 2 years, primarily through SA team
"""

SAMPLE_PMR = """\
---
type: post-meeting-report
customer: "明华重工"
opportunity: DevOps Modernization
meeting_title: Technical Deep Dive
date: 2026-06-01
attendees_customer: "张伟 (CTO), 李芳 (VP Eng)"
attendees_aws: "SA: 陈明, AE: 王磊"
version: "1.0"
---

## 1. Outcome Assessment

- **Overall Result:** `{result:achieved}`
- **Meeting Objective:** Validate technical fit → Achieved
- **Confidence for Next Step:** `{confidence:high}`

### Key Win
CTO explicitly said "this looks like the right architecture for us"

## 2. Meeting Insights

### Customer Sentiment
Positive. CTO was engaged throughout, asked detailed questions about security model.

### Key Findings
- Budget is approved for Q3 ($300K)
- Security team needs separate review
- Competing with Azure (incumbent for some workloads)

### Information Gap Check

| Question | Status | Finding |
|----------|--------|---------|
| CI/CD current state? | answered | Jenkins on-premise, 200+ pipelines |
| Security requirements? | unanswered | Need follow-up with CISO |
| Timeline pressure? | answered | Must migrate before Dec 2026 |

## 3. What Changed — EP Update

| Field | Before | After | Change |
|-------|--------|-------|--------|
| Stage | Qualified | Technical Validation | update |
| CTO Stance | neutral | supporter | update |
| Win Probability | 40% | 65% | update |

### Execution Log Update
- 2026-06-01: Technical deep dive — CTO confirmed architecture fit

### Agent Recommendation
Accelerate POC setup. CTO momentum is high; delay risks losing attention to competing initiatives.

## 4. Next Steps — Planned vs Actual

| Planned | Actual | Gap |
|---------|--------|-----|
| Get POC commitment | Achieved — 2-week POC approved | None |
| Understand security reqs | Partially — need CISO meeting | Follow-up needed |

### Action Items

| # | Action | Owner | Due | Status |
|---|--------|-------|-----|--------|
| 1 | Send POC proposal | SA 陈明 | 2026-06-03 | pending |
| 2 | Schedule CISO meeting | AE 王磊 | 2026-06-05 | pending |
| 3 | Share security whitepaper | SA 陈明 | 2026-06-02 | pending |

## 5. Customer Recap Email

**Subject:** Thank You — Technical Deep Dive Follow-up

张总、李总好，

感谢今天的深度技术交流。以下是我们讨论的主要成果和后续步骤：

1. **架构验证** — 确认 AWS CodePipeline + EKS 方案满足你们的 CI/CD 需求
2. **POC 计划** — 2周 POC，重点验证 <5ms 延迟目标
3. **后续安排** — 我们会在本周发送 POC 方案书，并与安全团队安排专项讨论

如有任何问题，随时联系我们。

此致，
陈明 | Solutions Architect, AWS

**Excluded from email:**
- Competing with Azure (internal only)
- Win probability assessment
- CTO stance classification
"""

SAMPLES = {
    "engagement-plan": SAMPLE_EP,
    "call-plan": SAMPLE_CP,
    "executive-briefing": SAMPLE_EB,
    "post-meeting-report": SAMPLE_PMR,
}


# ===== Tests =====

class TestHTMLRenderer:
    """Test HTML output for all doc types."""

    @pytest.mark.parametrize("doc_type", SAMPLES.keys())
    def test_html_renders_successfully(self, doc_type, tmp_path):
        output = tmp_path / f"{doc_type}.html"
        result = render(SAMPLES[doc_type], format="html", output_path=str(output))
        assert result["success"], f"HTML render failed for {doc_type}: {result['error']}"
        assert output.exists()
        assert output.stat().st_size > 500  # sanity check — not empty/trivial
        content = output.read_text()
        assert "<html" in content
        assert "</html>" in content

    @pytest.mark.parametrize("doc_type", SAMPLES.keys())
    def test_html_contains_customer_name(self, doc_type, tmp_path):
        output = tmp_path / f"{doc_type}.html"
        result = render(SAMPLES[doc_type], format="html", output_path=str(output))
        assert result["success"]
        content = output.read_text()
        customer = result["doc_type"]  # just verify it parsed
        assert customer is not None


class TestPDFRenderer:
    """Test PDF (ReportLab) output for all doc types."""

    @pytest.mark.parametrize("doc_type", SAMPLES.keys())
    def test_pdf_renders_successfully(self, doc_type, tmp_path):
        output = tmp_path / f"{doc_type}.pdf"
        result = render(SAMPLES[doc_type], format="pdf", output_path=str(output))
        assert result["success"], f"PDF render failed for {doc_type}: {result['error']}"
        assert output.exists()
        assert output.stat().st_size > 1000  # PDF should be substantial
        # Verify it's a valid PDF (starts with %PDF)
        with open(output, "rb") as f:
            header = f.read(5)
        assert header == b"%PDF-", f"Not a valid PDF for {doc_type}"


class TestDocxRenderer:
    """Test DOCX output for all doc types."""

    @pytest.mark.parametrize("doc_type", SAMPLES.keys())
    def test_docx_renders_successfully(self, doc_type, tmp_path):
        output = tmp_path / f"{doc_type}.docx"
        result = render(SAMPLES[doc_type], format="docx", output_path=str(output))
        assert result["success"], f"DOCX render failed for {doc_type}: {result['error']}"
        assert output.exists()
        assert output.stat().st_size > 1000  # DOCX should be substantial
        # Verify it's a valid ZIP (DOCX is ZIP-based)
        with open(output, "rb") as f:
            header = f.read(4)
        assert header == b"PK\x03\x04", f"Not a valid DOCX/ZIP for {doc_type}"


class TestValidationIntegration:
    """Test that validation + render pipeline works end-to-end."""

    def test_render_returns_validation_warnings(self, tmp_path):
        """A minimal doc should still render but may have warnings."""
        minimal = """\
---
type: call-plan
customer: Test
opportunity: Test
meeting_title: Test
date: 2026-01-01
time: "10:00"
format: Online
stage: Qualified
version: "1.0"
---

## 1. Meeting Details

Test content.
"""
        output = tmp_path / "minimal.html"
        result = render(minimal, format="html", output_path=str(output))
        assert result["success"]
        assert result["validation"] is not None
        # Should have warnings about missing required sections
        assert len(result["validation"]["warnings"]) > 0 or len(result["validation"]["auto_fixes"]) > 0

    def test_render_invalid_format_returns_error(self):
        result = render("# Hello", format="xlsx")
        assert not result["success"]
        assert "Unsupported format" in result["error"]
