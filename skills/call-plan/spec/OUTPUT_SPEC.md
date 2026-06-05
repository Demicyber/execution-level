# Call Plan — Structured Markdown Output Spec

> This defines the exact Markdown format the LLM must output for Call Plan documents.
> The renderer parses this format deterministically into PDF (ReportLab direct rendering).

## ⚠️ MANDATORY COMPLIANCE

**This spec is the ONLY accepted output format. The agent MUST follow it exactly:**
- All 7 sections MUST appear in exact order: 1. Meeting Details → 2. Target Meeting Outcomes → 3. Success Criteria → 4. Information Exchange → 5. Potential Objections & Responses → 6. Meeting Agenda → 7. Potential Next Steps
- Section headers MUST use `## N. {Title}` format (numbered)
- Attendee Insights MUST be a subsection under Meeting Details with `**Name** — Title` format per person
- Success Criteria MUST use dual-perspective table (Customer + Seller columns) with Disqualification Signals inline
- Information Exchange MUST have both "Information to Gather" and "Information to Deliver" subsections
- Objections table MUST include Fallback and Disqualifier? columns
- Next Steps MUST have all three paths (primary, fallback, graceful exit)
- Do NOT skip sections, reorder them, or use alternative formats
- Violation of this spec will result in rendering failures. No exceptions.

---

## Frontmatter (YAML, required)

```yaml
---
type: call-plan
customer: "明华重工"
opportunity: "Cloud Migration - Data Center Exit"
meeting_title: "POC 验证方案评审会"
date: "2026-03-20"
time: "14:00-15:00"
format: "On-site"
location: "明华重工总部 B栋 3F-08 会议室"
stage: "Technical Validation"
stage_target: "Business Validation"
version: "2026-03-19"
---
```

**All fields required** except `stage_target` (omit if no progression expected).

---

## Section Structure (fixed order, fixed headers)

7 sections matching the template:
1. Meeting Details (includes Customer Attendees, Attendee Insights, AWS Attendees)
2. Target Meeting Outcomes
3. Success Criteria (includes Disqualification Signals)
4. Information Exchange (Information to Gather + Information to Deliver)
5. Potential Objections & Responses
6. Meeting Agenda
7. Potential Next Steps

### Rules:
1. Section headers MUST use `## N. {Title}` format matching template
2. Sub-sections use `###`
3. Stance/Role/Category values written directly as field values (renderer maps to badge colors)
4. Provenance labels use `[销售确认]` or `[网络搜索]` inline — no label = AI推断
5. Tables use standard Markdown table syntax
6. Each section is REQUIRED

---

## 1. Meeting Details

```markdown
## 1. Meeting Details

| Field | Value |
|-------|-------|
| Date & Time | {date} {time} {timezone} |
| Duration | {duration} |
| Format | {In-person / Virtual / Hybrid} |
| Location / Link | {location or meeting link} |
| Opportunity Name | {auto from EP} |
| Current Sales Stage | {stage} |

### Customer Attendees

| Name | Title | Role in Decision |
|------|-------|-----------------|
| {name} | {title} | {EB / Champion / Decision Maker / Influencer / Evaluator / End User} |

### Attendee Insights

**{Name}** — {Title}
- **Focus & Priorities:** {most relevant 1-2 pain/KPI for this meeting}
- **Communication Approach:** {specific behavioral guidance — how to communicate effectively}
- **Current Stance:** {Holden 5-level + brief evidence}
- **Our Goal:** {specific verifiable action needed from this person in THIS meeting}

### AWS Attendees

| Name | Title | Role in Meeting |
|------|-------|-----------------|
| {name} | {title} | {Lead / Support / SME / Executive Sponsor} |
```

**Constraints:**
- At least 1 Customer Attendee
- Each Customer Attendee has an Attendee Insights card
- Our Goal must be verifiable (can assess yes/no after meeting)
- At least 1 AWS Attendee with clear role

---

## 2. Target Meeting Outcomes

```markdown
## 2. Target Meeting Outcomes

| # | Customer Perspective | Our Perspective |
|---|---------------------|-----------------|
| 1 | {what customer gains from this meeting} | {what we gain — verifiable advance} |
| 2 | {customer perspective 2} | {our perspective 2} |

**Target Stage Progression:** ( {current stage} ) → ( {target stage or "remain, close gap X"} )

**Fallback Outcome:** {minimum acceptable advance if primary goals not fully met}
```

**Constraints:**
- 1-4 rows (match meeting complexity)
- Each row: customer vs. our perspective, one sentence each
- Target Stage Progression: always present
- Fallback Outcome: always required — specific minimum viable next step

---

## 3. Success Criteria

```markdown
## 3. Success Criteria

| Level | Customer Would Consider Successful If… | We Would Consider Successful If… |
|-------|----------------------------------------|----------------------------------|
| **Ideal** | {customer ideal outcome} | {our ideal — all objectives + unexpected gain} |
| **Acceptable** | {customer acceptable} | {our acceptable — core objectives achieved} |
| **Minimum** | {customer minimum} | {our minimum — enough info to judge + keep dialogue} |

**Disqualification Signals:** {what signals this opp should be abandoned}
```

**Constraints:**
- Three tiers always present (Ideal / Acceptable / Minimum)
- Dual perspective: Customer AND Seller for each tier
- Each criterion must be observable and binary (based on customer actions, not feelings)
- Disqualification Signals: required, inline at end of section

---

## 4. Information Exchange

```markdown
## 4. Information Exchange

### Information to Gather

| # | Question | Target Attendee | Purpose |
|---|----------|----------------|---------|
| 1 | {tailored question based on research-gap method} | {person name} | {why asking + how answer will be used} |
| 2 | {question} | {person} | {purpose} |
| 3 | {question} | {person} | {purpose} |

### Information to Deliver

| # | What to Share | Format | Purpose |
|---|--------------|--------|---------|
| 1 | {teaching moment / proof point / market context} | {format} | {what it achieves for customer} |
| 2 | {deliverable} | {format} | {purpose} |
```

**Constraints:**
- Information to Gather: 3-5 questions, prioritized (most important first)
- Information to Deliver: 2-4 items
- Every question must have clear Purpose tied to Target Outcomes
- Questions must be tailored (research-gap method), not generic
- Deliver items provide value (teaching moments, proof points, market context)

---

## 5. Potential Objections & Responses

```markdown
## 5. Potential Objections & Responses

| # | Anticipated Objection | Category | Response | Fallback | Disqualifier? |
|---|----------------------|----------|----------|----------|---------------|
| 1 | {specific objection} | {Status Quo|Price/Competition|Capability|Risk/Trust|Authority} | {2-3 sentences + question back} | {if reframe doesn't work} | {Yes/No} |
| 2 | {objection} | {category} | {response} | {fallback} | {Yes/No} |
```

**Constraints:**
- 2-5 objections (match meeting complexity)
- Category is enum: `Status Quo`, `Price/Competition`, `Capability`, `Risk/Trust`, `Authority`
- Response: Acknowledge-Reframe-Advance pattern, ends with question back
- Fallback always present
- Disqualifier flag: marks whether confirmed objection means walk away

---

## 6. Meeting Agenda

```markdown
## 6. Meeting Agenda

| Time | Topic | Owner | Purpose |
|------|-------|-------|---------|
| {00:00-00:05} | {topic} | {person} | {what this achieves} |
| {00:05-00:20} | {topic} | {person} | {purpose} |
| {00:20-00:35} | {topic} | {person} | {purpose} |
| {00:35-00:50} | {topic} | {person} | {purpose} |
| {00:50-00:55} | {topic} | {person} | {purpose} |
| {00:55-01:00} | Close | {AM} | — |
```

**Constraints:**
- Time slots must be consecutive and cover the full meeting duration
- Every slot has an Owner
- Purpose ties back to Target Outcomes
- Discovery/Dialogue should be longest block (not presentations)
- Last 5-10 min always reserved for next steps commitment

---

## 7. Potential Next Steps

```markdown
## 7. Potential Next Steps

**If meeting goes well (primary path):**

| # | Proposed Next Step | Timeline | Owner | Purpose |
|---|-------------------|----------|-------|---------|
| 1 | {concrete action with customer commitment} | {when} | {Joint: who does what} | {advance toward what} |
| 2 | {action} | {when} | {who} | {purpose} |

**If customer needs more time (fallback path):**

| # | Proposed Next Step | Timeline | Owner | Purpose |
|---|-------------------|----------|-------|---------|
| 1 | {value-add without pressure} | {when} | {who} | {purpose} |
| 2 | {maintain momentum} | {when} | {who} | {purpose} |

**If not a fit / timing wrong (graceful exit):**

| # | Proposed Next Step | Timeline | Owner | Purpose |
|---|-------------------|----------|-------|---------|
| 1 | {graceful exit preserving relationship} | {when} | {who} | {purpose} |
| 2 | {future trigger-based reconnect} | {when} | {who} | {purpose} |
```

**Constraints:**
- Three paths always present
- Primary: 2-4 items
- Fallback: 1-3 items
- Graceful exit: 1-2 items
- All items must have Timeline + Owner (SMART: who, what, when, why)
- Every next step includes customer commitment (not just seller actions)

---

## Badge Value Enums

| Field | Allowed Values |
|-------|---------------|
| Stance | `sponsor`, `supporter`, `neutral`, `non-supporter`, `adversary` |
| Role in Decision | `EB`, `champion`, `decision-maker`, `influencer`, `evaluator`, `end-user` |
| Objection Category | `Status Quo`, `Price/Competition`, `Capability`, `Risk/Trust`, `Authority` |
| Role in Meeting | `Lead`, `Support`, `SME`, `Executive Sponsor` |

---

## Validation Rules

1. Frontmatter: all required fields present and non-empty
2. All 7 sections present
3. Badge values match enum lists above
4. Tables have correct column count
5. At least 1 Customer Attendee defined
6. At least 1 AWS Attendee defined
7. Meeting Agenda time slots are consecutive
8. Each Attendee has matching Attendee Insights card
