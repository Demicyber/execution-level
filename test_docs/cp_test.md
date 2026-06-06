---
doc_type: call-plan
customer: Acme Corp
opportunity: Cloud Migration Phase 2
meeting_title: Technical Deep Dive - Security Architecture
date: 2025-03-15
sales_stage: Qualify
---

## 1. 📋 Meeting Details

| Field | Details |
|-------|---------|
| **Date & Time** | 2025-03-15, 14:00-15:30 CST |
| **Format** | In-person (Acme HQ, Building A, Room 301) |
| **Meeting Type** | Technical Deep Dive |
| **Objective Source** | EP Next Milestone #3 |

### Customer Attendees

| Name | Title | Role | Stance | Priority |
|------|-------|------|--------|----------|
| **张伟** | VP Engineering | `decision-maker` | `neutral` | `high` |
| **李明** | Security Architect | `technical-evaluator` | `supporter` | `high` |
| **王芳** | Procurement Lead | `procurement` | `unknown` | `medium` |

### AWS Attendees

| Name | Role in Meeting |
|------|----------------|
| Sarah Chen | Account SA — `lead` |
| Mike Johnson | Security Specialist — `sme` |

## 2. 🎯 Target Meeting Outcomes

| # | Objective | Target Outcome | Priority |
|---|-----------|----------------|----------|
| 1 | Validate security architecture meets compliance | Written sign-off on design [AI推断] | `must-meet` |
| 2 | Address data residency concern | Agreement on region strategy | `must-meet` |
| 3 | Introduce managed SIEM integration | Interest for follow-up demo | `nice-to-have` |

## 3. ✅ Success Criteria

| Tier | Criteria | Disqualifier |
|------|----------|--------------|
| ✅ Ideal | Security sign-off + demo scheduled + procurement timeline [AI推断] | `no` |
| ⚠️ Acceptable | Security sign-off + verbal interest in next step | `no` |
| ❌ Minimum | Clear list of remaining blockers with owners | `no` |
| 🚪 Walk-away | Customer reveals competing POC already in progress | `yes` |

## 4. 🔄 Information Exchange

### A. Discovery Questions

| # | Question | Context | What Good Sounds Like |
|---|----------|---------|----------------------|
| 1 | "What's your current incident response SLA for P1 security events?" | They mentioned compliance audit coming Q2 [销售确认] | Specific SLA numbers → map to our automation value |
| 2 | "How does your security team handle cross-region data access today?" | Data residency concern from last meeting | Manual process = pain point for our solution |

### B. Information to Deliver

| # | Insight | Delivery Trigger | Format |
|---|---------|-----------------|--------|
| 1 | Similar financial services customer achieved 40% faster incident response | After Q1 about current SLA | Case study one-pager |
| 2 | Our region-lock architecture passes GDPR Article 44 | When data residency comes up | Architecture diagram |

## 5. ⚡ Potential Objections & Responses

| Category | Objection | Acknowledge | Pivot | Elevate |
|----------|-----------|-------------|-------|---------|
| `capability` | "Can your encryption handle our custom key rotation policy?" [AI推断] | "Key rotation is critical for your compliance posture." | "Our KMS integration supports custom rotation schedules — let me show the config." | "This actually simplifies your audit trail significantly." |
| `risk/trust` | "What happens during a region failover?" | "Business continuity is non-negotiable." | "Our multi-region failover keeps data in-boundary — here's the DR architecture." | "You'd actually get better RPO than your current setup." |

### ⚠️ Landmines

| Topic | Why Avoid | If Raised |
|-------|-----------|-----------|
| Competitor X's recent breach | Could seem like FUD tactics | Acknowledge factually, pivot to our proactive approach |

## 6. 📅 Meeting Agenda

| Time | Duration | Topic | Owner | Objective Link |
|------|----------|-------|-------|----------------|
| 14:00 | 5min | Opening & context setting | Sarah Chen | — |
| 14:05 | 20min | Security architecture walkthrough | Mike Johnson | Obj #1 |
| 14:25 | 15min | Data residency deep dive | Mike Johnson | Obj #2 |
| 14:40 | 15min | Q&A — compliance concerns | Sarah Chen | Obj #1, #2 |
| 14:55 | 10min | Managed SIEM overview (if time) | Mike Johnson | Obj #3 |
| 15:05 | 10min | Next steps & timeline | Sarah Chen | All |

## 7. 🚀 Potential Next Steps

### Ideal Path
- Security sign-off documented → share with procurement [AI推断]
- Schedule SIEM demo with broader team (Week of Mar 24)
- Procurement kickoff call with 王芳

### Acceptable Path
- Follow-up email with remaining security questions + answers
- Schedule 30-min call to close gaps (within 1 week)

### Minimum Path
- Document all open blockers → assign owners → set review date
- Escalate data residency question to AWS Solutions Architect team
