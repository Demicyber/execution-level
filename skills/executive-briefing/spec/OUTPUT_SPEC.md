# Executive Briefing — Structured Markdown Output Spec

> This defines the exact Markdown format the LLM must output for Executive Briefing documents.
> The renderer parses this format deterministically into PDF (ReportLab direct rendering).

## ⚠️ MANDATORY COMPLIANCE

**This spec is the ONLY accepted output format. The agent MUST follow it exactly:**
- Every section listed below MUST appear in the output, in the exact order specified
- Section headers MUST match character-for-character (including emoji and numbering)
- Field names within tables MUST use the exact names shown
- Do NOT invent new sections, skip sections, reorder sections, or rename fields
- Do NOT use alternative field names or legacy formats — only what is documented here
- Attendee Background must use paragraph format (not bullet-point labels)
- Violation of this spec will result in rendering failures. No exceptions.

---

## Frontmatter (YAML, required)

```yaml
---
type: executive-briefing
customer: "GlobalRetail Inc."
opportunity: "Cloud Migration - Data Center Exit"
meeting_title: "CEO Executive Briefing - Strategic Cloud Partnership"
date: "2026-04-15"
time: "10:00-11:00 CST"
format: "In-person"
classification: "INTERNAL USE ONLY — AWS Confidential"
requested_by: "Zhang Wei (AM)"
version: "2026-04-12"
---
```

**All fields required.**

---

## Section Structure (fixed order, fixed headers)

EB has 5 top-level `##` sections matching the reference template:
1. `## 1. 📋 Meeting Logistics` — when, where, who, why
2. `## 2. 👤 Customer Attendee Background` — person paragraphs + company profile
3. `## 3. 🎯 Meeting Objectives` — success definition, objectives, concerns, next steps
4. `## 4. 📊 AWS Account Background` — commercial summary + account narrative
5. `## 5. 📎 Appendix` — previous notes, case studies, competitive intel (optional)

### Rules:
1. Section headers use format: `## {N}. {emoji} {Title}`
2. Sub-sections use `###`
3. Attendee Background uses paragraph format (one flowing paragraph per person, NOT bullet-point dimensions)
4. Tables use standard Markdown table syntax
5. All sections required except Appendix (optional)
7. All content in Chinese, professional executive tone

---

## 1. 📋 Meeting Logistics

```markdown
## 1. 📋 Meeting Logistics

| Field | Details |
|---|---|
| **Date / Time / Format** | {YYYY-MM-DD / HH:MM-HH:MM timezone / In-person or VTC / Location} |
| **Opportunity Name** | {auto from EP} |
| **Current Sales Stage** | {auto from EP} |
| **AWS Attendees** | {Executive name (role), Account Manager, others} |

**Who requested this meeting and why?**

> {2-3 sentences: who initiated + why executive involvement needed + position in roadmap + risk of not attending}

| Role | Name / Contact | Purpose in This Meeting |
|---|---|---|
| **Account Manager** | {name, @alias, phone} | {specific purpose} |
| **Sales Leader / VP** | {name, @alias, phone} | {specific purpose} |
| **Executive Sponsor** | {name, title} | {specific ask leveraging peer relationship} |
```

**Constraints:**
- All logistics fields required (mark unconfirmed as "TBC — 待销售确认")
- "Who requested and why" must cover: initiator, why exec needed, roadmap position, consequence of not going
- AWS Team table: each person has specific Purpose (not "支持")

---

## 2. 👤 Customer Attendee Background

```markdown
## 2. 👤 Customer Attendee Background

**{Attendee Name}** — {Title}

> {One flowing paragraph, 180-220 characters in Chinese. Covers: Position & Tenure. Stance (Holden 5级) + evidence. What they care about (relevant to this meeting's objectives). Communication approach. Relationship history with AWS.}

*Repeat for each customer attendee.*

### Company Profile

> {One flowing paragraph, ≤200 characters in Chinese. Covers: industry position, scale (revenue/employees/market share), recent strategic moves, digital transformation status, key business priorities relevant to this engagement.}
```

**Constraints:**
- Each attendee: ONE paragraph (180-220 chars), NOT bullet-point format
- Must include Holden stance + evidence within the paragraph
- Communication style must be behavioral guidance (not labels)
- Company Profile: one paragraph, ≤200 chars, fact-dense with specific data
- No empty labels — avoid "致力于创新" style platitudes

---

## 3. 🎯 Meeting Objectives

```markdown
## 3. 🎯 Meeting Objectives

### Success Definition

> {一句话：what counts as success for this meeting — must be a verifiable customer action}

### Strategic Alignment

> {Position in EP roadmap + why this meeting matters now + what happens if we don't do this}

### Objective 1: {动词开头的简述}

| Element | Content |
|---|---|
| **Objective / Outcome** | {action-oriented goal — sales input verbatim} |
| **Context** | {background + risk + competition — sales input verbatim} |
| **Talking Points** | {one flowing paragraph in executive conversation style — Agent generated} |
| **Asks** | {1-2 executive-level requests that require peer relationship to make} |

### Objective 2: {动词开头的简述}

| Element | Content |
|---|---|
| **Objective / Outcome** | {goal} |
| **Context** | {background} |
| **Talking Points** | {paragraph} |
| **Asks** | {requests} |

### Anticipated Concerns

**1. {顾虑主题}**
> {一整段：顾虑描述 + 回应策略（Acknowledge → Pivot → Elevate），≤100字}

**2. {顾虑主题}**
> {一整段}

### ⚠️ Landmines — 不要主动提

> - {Topic 1}：{为什么不能提}
> - {Topic 2}：{为什么不能提}

### Proposed Next Steps

| 层级 | Next Step | 触发条件 |
|---|---|---|
| **Ideal** | {具体动作 + owner + timeline} | 会议顺利，所有 objectives 达成 |
| **Acceptable** | {具体动作 + owner + timeline} | 部分达成，态度积极但需内部协调 |
| **Minimum** | {具体动作 + owner + timeline} | 态度保留，保住继续对话机会 |
```

**Constraints:**
- 2-3 objectives maximum (60-min executive meeting)
- Objective/Outcome and Context: sales input verbatim, no language optimization
- Talking Points: one flowing paragraph, executive conversation style, Agent generated
- Asks: must require executive-level authority/relationship (not AM/SA work)
- Anticipated Concerns: 2-3 max, each with Acknowledge→Pivot→Elevate response
- Landmines: topics to NEVER raise proactively
- Proposed Next Steps: 3-tier (Ideal/Acceptable/Minimum), executive-level commitments

---

## 4. 📊 AWS Account Background

```markdown
## 4. 📊 AWS Account Background

| Field | Details |
|---|---|
| **Geo / Segment** | {e.g., GCR / Enterprise} |
| **Current AWS Spend** | {e.g., $20M (FY2025)} |
| **Expected Spend** | {e.g., $25M (FY2026)} |
| **Commit / PPA Status** | {e.g., Exceeded $25M PPA 12 months early; renewal in progress} |

### Account Summary

> {One flowing paragraph, ≤250 chars. Covers: AWS usage (key workloads/services), commercial status, recent wins/momentum, active issues/risks (MUST mention if any), competitive landscape. If no active issues, explicitly state "无已知活跃 escalation".}
```

**Constraints:**
- Table: all commercial fields required
- Account Summary: one paragraph, high information density
- Active issues/escalations MUST be mentioned (executive getting surprised = trust collapse)
- Competitive landscape: honest assessment with threat level (🔴 Active / 🟡 Exploring / 🟢 Awareness)

---

## 5. 📎 Appendix

```markdown
## 5. 📎 Appendix

### A. Previous Meeting Notes & Action Items

> {上次高管级会议要点 + action items 状态（✅ Done / 🔄 In Progress / ❌ Overdue）}

### B. Relevant Customer Success Stories

> {1-2 case studies mirroring customer's situation. Each: industry, challenge, solution, quantified outcome, timeline.}

### C. Competitive Intelligence

> *Per competitor:*
> - **Products in use** — what they provide today
> - **Contract status** — terms, renewal timeline
> - **Customer satisfaction** — known sentiment
> - **Our differentiators** — specific (not generic)
> - **Displacement / coexistence strategy**
```

**Constraints:**
- Appendix is optional (include if relevant data available)
- Previous Meeting Notes: highlight ❌ Overdue items (exec may be asked about them)
- Case Studies: must have quantified results (not "效果很好")
- Competitive Intel: per competitor, structured, with source confidence level

---

## Badge Value Enums

| Field | Allowed Values |
|-------|---------------|
| Current Stance | `sponsor`, `supporter`, `neutral`, `non-supporter`, `adversary` |
| Competitive Threat Level | `active` (🔴), `exploring` (🟡), `awareness` (🟢) |
| Action Item Status | `done` (✅), `in-progress` (🔄), `overdue` (❌) |
| Next Step Tier | `ideal`, `acceptable`, `minimum` |

---

## Validation Rules

1. Frontmatter: all required fields present
2. Classification must be "INTERNAL USE ONLY — AWS Confidential"
3. All 5 sections present (Appendix can be empty but header must exist)
4. At least 1 customer attendee background present
5. Attendee Background uses paragraph format (not bullet points)
6. At least 2 meeting objectives defined
7. Anticipated Concerns present with response strategy
8. Proposed Next Steps has 3 tiers
