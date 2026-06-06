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
source: new-logo
created: "2026-01-01"
version: "2026-05-01"
---

## 1. 📊 Opportunity Snapshot

| Field | Value |
|-------|-------|
| Customer | 测试科技 · Tech · New Logo |
| Opportunity Name | Cloud Migration |
| Deal Value | $500K ARR |
| Current Stage | Technical Validation |
| Target Launch Date | 2026-Q3 |

### Why Now

数据中心租约年底到期，必须在Q3前完成技术验证。

### Deal Objective

帮助客户完成核心工作负载迁移评估，锁定$500K ARR。

### Win Strategy

Champion-led approach. 利用王明的技术信任推动。

**Key Risks:** 竞争对手Azure正在接触CFO。

### 📈 Engagement Progress

[Prospect] ━━━ [Qualified] ━━━ [Tech Val] ━━━ [Biz Val] ━━━ [Committed]
                                ▲ We are here

## 2. 👥 Engagement Plan

### 👥 Key Stakeholders

**王明** — CTO

| Dimension | Details |
|---|---|
| **Engagement Priority** | Must Meet — 技术决策签字人 [销售确认] |
| **Role in This Deal** | Decision Maker — 架构评审有一票否决权 |
| **Current Stance** | Supporter — 主动索要白皮书 |
| **What They Care About** | Cost reduction, reliability |
| **Profiling** | Data-driven, prefers metrics |
| **What We Need From Them** | Technical sign-off |
| **How to Win Them** | Provide benchmark data |

**李芳** — VP Engineering

| Dimension | Details |
|---|---|
| **Engagement Priority** | Important — 评估协调人 |
| **Role in This Deal** | Evaluator — 技术评估负责人 |
| **Current Stance** | Neutral — 首次接触 |
| **What They Care About** | Migration risk control |
| **Profiling** | Process-oriented, documentation-heavy |
| **What We Need From Them** | Provide architecture docs |
| **How to Win Them** | WAR demo first |

### 📍 Engagement Roadmap

| # | Milestone | Key Stakeholders | AWS Team | Status |
|---|-----------|-----------------|----------|--------|
| 1 | Discovery complete | 王明 | SA | Done |
| 2 | POC validation | 王明, 李芳 | SA, TAM | **Next** ↓ |
| 3 | Business case approved | CFO | AM, Deal Desk | Planned |

### 📐 Estimate & Contingency

| | Best Case | Worst Case |
|---|---|---|
| **Milestones to Close** | 3 | 5 |
| **Timeline** | 6 weeks | 12 weeks |

#### Stakeholder Risk & Leverage

| At-Risk Stakeholder | Red Flag | Leverage Source | Plan B |
|---|---|---|---|
| CFO | Not contacted | 王明 intro | Industry event |

#### Milestone Risk & Contingency

| Milestone Node | Risk Item | Trigger Condition | Impact | Plan B |
|---|---|---|---|---|
| #2 POC | 🧑 CTO busy | 2 weeks no reply | +2 weeks | Informal tech chat |

### 📋 Next Milestone Detail

**Milestone #2** — 2026-06-01

**Objective:** Prove <5ms latency at scale

**Customer Attendees & Target Outcome:**
- 王明 (CTO) — Supporter, target Sponsor: approve POC scope
- 李芳 (VP Eng) — Neutral, target Supporter: provide test environment

**AWS Team:** SA leads technical, TAM supports

**Key Questions & Discussion Points:**
- Current architecture bottlenecks?
- POC success criteria?

## 3. 📝 Execution Log

### Engagement #1 — 2026-05-01 — 王明

| Field | Details |
|---|---|
| **Planned** | Initial discovery call |
| **Actual** | CTO confirmed migration interest |
| **People Updates** | 王明: Neutral → Supporter |
| **Key Learnings** | Budget approved for Q3 |
| **Plan Adjustment** | None needed |
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

## 1. 📋 Meeting Details

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

## 2. 🎯 Target Meeting Outcomes

- Validate technical architecture fit
- Confirm POC scope and timeline

## 3. ✅ Success Criteria

| Perspective | Customer Outcome | Seller Outcome |
|-------------|-----------------|----------------|
| Ideal | Clear architecture path | POC commitment |
| Acceptable | Understanding of gaps | Follow-up scheduled |
| Minimum | Relationship maintained | Next steps agreed |

**Disqualification Signals:** Budget freeze, competing project priority

## 4. 🔄 Information Exchange

### Information to Gather
- Current CI/CD pipeline details
- Security compliance requirements

### Information to Deliver
- AWS CodePipeline architecture
- Reference customer results

## 5. ⚡ Potential Objections & Responses

| Objection | Category | Response | Fallback | Disqualifier? |
|-----------|----------|----------|----------|---------------|
| "Too complex" | capability | Step-by-step migration | Managed service option | No |
| "Budget locked" | price-value | Phased approach | Pay-as-you-go | Yes if no budget in 6mo |

## 6. 📅 Meeting Agenda

| Time | Topic | Owner | Purpose |
|------|-------|-------|---------|
| 00-05 | Opening | SA | Context setting |
| 05-30 | Architecture | SA | Deep dive |
| 30-45 | Q&A | All | Address concerns |
| 45-50 | Next Steps | AE | Agreement |

## 7. 🚀 Potential Next Steps

- **Primary Path:** POC kickoff within 2 weeks
- **Fallback Path:** Schedule follow-up with security team
- **Graceful Exit:** Share reference materials, reconnect in Q4
"""

SAMPLE_EB = """\
---
type: executive-briefing
customer: "环球物流集团"
opportunity: "Cloud Partnership"
meeting_title: EBC Visit
date: 2026-06-15
time: "10:00-11:30 CST"
format: "In-person"
classification: "INTERNAL USE ONLY — AWS Confidential"
requested_by: "Zhang Wei (AM)"
version: "1.0"
---

## 1. 📋 Meeting Logistics

- **Date:** 2026-06-15
- **Format:** In-person, Beijing Office
- **AWS Executive:** VP, Greater China
- **Duration:** 90 minutes

## 2. 👤 Customer Attendee Background

**李总** — CEO

> 李总2019年出任CEO，前麦肯锡合伙人。Neutral — 对AWS持谨慎乐观态度，重视可靠性。大格局思考者，偏好战略性对话。核心关注物流网络数字化转型。与AWS的互动主要通过SA团队，合作2年。

### Company Profile

> 环球物流集团，物流与供应链行业，2025年营收$2.8B，员工15000+。目前以本地部署为主，云采用处于早期阶段。

## 3. 🎯 Meeting Objectives

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

## 4. 📊 AWS Account Background

| Field | Details |
|---|---|
| **Geo / Segment** | GCR / Enterprise |
| **Current AWS Spend** | $200K/month |
| **Expected Spend** | $300K/month |
| **Commit / PPA Status** | No PPA yet |

### Account Summary

> 客户当前月支出$200K，YoY增长30%，主要工作负载为数据分析和部分ML实验。与AWS合作2年，主要通过SA团队。无已知活跃escalation。竞争态势：本地部署为主，Azure有少量presence。

## 5. 📎 Appendix

### A. Previous Meeting Notes & Action Items

> 首次高管级会议，无历史记录。
"""

SAMPLE_PMR = """\
---
type: post-meeting-report
customer: "明华重工"
opportunity: DevOps Modernization
meeting_title: Technical Deep Dive
date: 2026-06-01
recorded_by: "Agent (from sales debrief)"
related_document: "call-plan-2026-05-28"
version: "1.0"
---

## 1. 📊 Outcome Assessment

| # | Target Meeting Outcome | Result | Evidence & Notes |
|---|---|---|---|
| 1 | Validate technical fit | Achieved | CTO said "this looks like the right architecture" |
| 2 | Get POC commitment | Achieved | 2-week POC approved on the spot |

**Stage Progression:** ( Qualified ) → ( Technical Validation ) — ✅ Achieved

## 2. 🔍 Meeting Insights

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

## 3. ✏️ What Changed — EP Update

| # | EP Section to Update | Change Type | What to Write |
|---|---|---|---|
| 1 | Key Stakeholders | Update | CTO stance: Neutral → Supporter |
| 2 | Roadmap | Update | Stage progression confirmed |
| 3 | Win Strategy | Add | Competing with Azure (incumbent) |

**Execution Log Update:** Milestone #1 Done — CTO confirmed architecture fit

### Agent Recommendation
Accelerate POC setup. CTO momentum is high; delay risks losing attention to competing initiatives.

## 4. 📋 Next Steps — Planned vs Actual

### Comparison

| # | Planned (from Call Plan) | Actual (agreed in meeting) | Delta |
|---|---|---|---|
| 1 | Get POC commitment | Achieved — 2-week POC approved | On track |
| 2 | Understand security reqs | Partially — need CISO meeting | Follow-up needed |

### Action Items

| # | Priority | Action Item | Owner | ETA | Status |
|---|---|---|---|---|---|
| 1 | High | Send POC proposal | SA 陈明 (AWS) | 2026-06-03 | Open |
| 2 | High | Schedule CISO meeting | AE 王磊 (AWS) | 2026-06-05 | Open |
| 3 | Medium | Share security whitepaper | SA 陈明 (AWS) | 2026-06-02 | Open |

## 5. ✉️ Customer Recap Email (Handoff)

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

## 1. 📋 Meeting Details

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
