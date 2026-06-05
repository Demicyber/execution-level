# Executive Briefing — Structured Markdown Output Spec

> This defines the exact Markdown format the LLM must output for Executive Briefing documents.
> The renderer parses this format deterministically into PDF (ReportLab direct rendering).

---

## Frontmatter (YAML, required)

```yaml
---
type: executive-briefing
customer: "明华重工"
opportunity: "Cloud Migration - Data Center Exit"
meeting_title: "EBC — VP Visit"
date: "2026-06-10"
time: "14:00-16:00"
format: "On-site"
location: "明华重工总部 A栋 VIP 会议室"
requested_by: "{who initiated this meeting and why}"
version: "2026-06-08"
---
```

**All fields required.**

---

## Section Structure (fixed order, fixed headers)

5 sections matching the template:
1. Meeting Logistics (AWS Attendees table + Key Contacts)
2. Customer Attendee Background (person paragraphs + Company Profile)
3. Meeting Objectives (Success Definition, Strategic Alignment, Objectives, Anticipated Concerns, Proposed Next Steps)
4. AWS Account Background
5. Appendix (optional)

### Rules:
1. Section headers MUST use `## N. {Title}` format matching template
2. Sub-sections use `###`
3. Stance badge uses `{stance:value}` inline syntax at end of "Attitude Toward AWS" paragraph
4. Tables use standard Markdown table syntax
5. Each section is REQUIRED except Appendix

---

## 1. Meeting Logistics

```markdown
## 1. Meeting Logistics

| Field | Details |
|-------|---------|
| Date / Time / Format | {YYYY-MM-DD / HH:MM-HH:MM timezone / In-person or VTC / Location} |
| Opportunity Name | {auto from EP} |
| Current Sales Stage | {auto from EP} |
| AWS Attendees | {Executive name (role), Account Manager, others} |

**Who requested this meeting and why?**

> {2-3 sentences: who initiated, why executive needed, position in roadmap, risk of not going}

| Role | Name / Contact | Purpose in This Meeting |
|------|---------------|------------------------|
| Account Manager | {name, alias, phone} | {purpose} |
| Sales Leader / VP | {name, alias, phone} | {purpose} |
| Executive Sponsor | {name, title} | {specific executive-level ask} |
```

**Constraints:**
- "Who requested and why" must cover: initiator, executive justification, roadmap position, consequence of inaction
- Every AWS attendee has a specific Purpose (not "support")

---

## 2. Customer Attendee Background

```markdown
## 2. Customer Attendee Background

### {Person Name} — {Title}

**Position & Tenure:** {role, reporting line, years at company, career trajectory}

**Communication Style:** {specific behavioral guidance from Contact Profiling}

**Decision Role & Business Focus:** {authority level, current priorities, KPIs}

**Attitude Toward AWS:** {stance description, concerns, sensitivities} {stance:supporter}

**Collaboration History:** {past projects, wins, friction points with AWS}

### {Person Name 2} — {Title}
...

### Company Profile

{One paragraph, 150-200 characters: positioning, scale, tech profile, strategic priorities, recent leadership changes}
```

**Constraints:**
- One block per customer attendee
- All 5 dimensions required for each person (Position & Tenure, Communication Style, Decision Role & Business Focus, Attitude Toward AWS, Collaboration History)
- Stance badge at end of "Attitude Toward AWS" paragraph using `{stance:value}` syntax
- Company Profile: subsection under this section, one dense paragraph
- Deeper research expected for EB (vs CP)

---

## 3. Meeting Objectives

```markdown
## 3. Meeting Objectives

### Success Definition

{1-2 sentences: what does a successful meeting look like — must be verifiable customer action}

### Strategic Alignment

{1-2 sentences: how this meeting fits into the broader deal strategy / EP roadmap position}

### Objective 1: {verb-led title}

| Element | Content |
|---------|---------|
| **Objective / Outcome** | {action-oriented outcome} |
| **Context** | {background + risk + competition} |
| **Talking Points** | {natural executive dialogue paragraph} |
| **Asks** | {1-2 executive-level asks that require peer-level authority} |

### Objective 2: {verb-led title}

| Element | Content |
|---------|---------|
| **Objective / Outcome** | {outcome} |
| **Context** | {context} |
| **Talking Points** | {talking points paragraph} |
| **Asks** | {asks} |

### Anticipated Concerns

**1. {concern topic}**
> {Acknowledge → Pivot → Elevate response strategy, one paragraph}

**2. {concern topic}**
> {response strategy}

### ⚠️ Landmines — Do Not Raise
> - {Topic 1}: {why dangerous}
> - {Topic 2}: {why dangerous}

### Proposed Next Steps

| Tier | Next Step | Trigger Condition |
|------|-----------|-------------------|
| **Ideal** | {specific action + owner + timeline} | All objectives achieved |
| **Acceptable** | {action + owner + timeline} | Partial success, positive attitude |
| **Minimum** | {action + owner + timeline} | Limited progress, keep dialogue |
```

**Constraints:**
- 2-3 objectives, each with Objective/Outcome + Context + Talking Points + Asks
- Asks must be executive-level (require peer-level authority)
- Anticipated Concerns: 1-3 items with Acknowledge-Pivot-Elevate framework
- Landmines: optional but recommended
- Proposed Next Steps: always 3 tiers (Ideal/Acceptable/Minimum)

---

## 4. AWS Account Background

```markdown
## 4. AWS Account Background

| Field | Details |
|-------|---------|
| Geo / Segment | {region / enterprise tier} |
| Current AWS Spend | {annual spend} |
| Expected Spend | {next year projection} |
| Commit / PPA Status | {PPA details, renewal timeline} |

### Account Summary

> {One paragraph, ~250 chars: AWS usage + commercial status + recent wins + active issues/risks + competitive landscape}
```

**Constraints:**
- Table fields: mark unknown as `[待确认]`
- Account Summary: must include issues/escalations (executive cannot be surprised)
- Competitive landscape must be honest with threat level (🔴 Active / 🟡 Exploring / 🟢 Awareness)

---

## 5. Appendix (optional)

```markdown
## 5. Appendix

### A. Previous Meeting Notes & Action Items

> {Previous executive meeting summary + action items with status (✅ Done / 🔄 In Progress / ❌ Overdue)}

### B. Relevant Customer Success Stories

> {1-2 cases mirroring customer situation: industry, challenge, solution, quantified outcome, timeline}

### C. Competitive Intelligence

> Per competitor:
> - Products in use
> - Contract status
> - Customer satisfaction
> - Our differentiators
> - Displacement / coexistence strategy
```

---

## Badge Value Enums

| Field | Allowed Values |
|-------|---------------|
| Stance (via {stance:value}) | `sponsor`, `supporter`, `neutral`, `non-supporter`, `adversary` |
| Next Step Tier | `ideal`, `acceptable`, `minimum` |

---

## Validation Rules

1. Frontmatter: all required fields present
2. All required sections present (4 sections; Appendix optional)
3. At least 1 customer attendee with all 5 dimensions
4. At least 1 AWS attendee with Purpose
5. At least 2 meeting objectives with full structure (Objective + Context + Talking Points + Asks)
6. Company Profile present as subsection of Customer Attendee Background
7. Account Background table has at least Geo/Segment and Spend fields
