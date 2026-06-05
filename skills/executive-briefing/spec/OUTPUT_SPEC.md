# Executive Briefing — Structured Markdown Output Spec

> This defines the exact Markdown format the LLM must output for Executive Briefing documents.
> The renderer parses this format deterministically into HTML/PDF/Word.

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
classification: "INTERNAL USE ONLY — AWS Confidential"
requested_by: "{who initiated this meeting and why}"
version: "2026-06-08"
---
```

**All fields required.** `classification` is always "INTERNAL USE ONLY — AWS Confidential".

---

## Section Structure (fixed order, fixed headers)

---

## 📋 Meeting Logistics

> Auto-generated from frontmatter by renderer. LLM writes the attendees below.

```markdown
## 📋 Meeting Logistics

### 🏢 AWS Attendees

| Name | Title | Role in Meeting |
|------|-------|-----------------|
| {name} | {title, e.g., VP of APJ} | {why they're here} |
| {name2} | {title} | {role} |

### 📞 Key Contacts

| Name | Role | Phone/Email | Notes |
|------|------|-------------|-------|
| {name} | AM | {contact} | {note} |
| {name2} | SA | {contact} | {note} |
```

---

## 👤 Customer Attendee Background

```markdown
## 👤 Customer Attendee Background

### {Person Name} — {Title}

**Position & Tenure:** {role, reporting line, years at company, career moves}

**Communication Style:** {direct/indirect, preferences, based on Contact Profiling + CXO Persona}

**Decision Role & Business Focus:** {authority level, current priorities, KPIs}

**Attitude Toward AWS:** {stance, concerns, sensitivities, topics to avoid} {stance:supporter}

**Collaboration History:** {past projects, wins, friction points}

### {Person Name 2} — {Title}
...
```

**Constraints:**
- One block per customer attendee
- All 5 dimensions required for each person
- Stance badge at end of "Attitude" line
- Provenance labels where applicable
- Deeper research expected for EB (vs CP) — include LinkedIn, news, annual report findings

---

## 🏢 Company Profile

```markdown
## 🏢 Company Profile

**Positioning & Industry Standing:** {what they do, market position}

**Scale & Impact:** {revenue, users, market share}

**Technology Profile:** {cloud adoption, AI maturity, in-house vs vendor}

**Strategic Priorities & Key Events:** {current focus, major events past/next 12 months}

**Recent Leadership Changes:** {C-suite/board changes in past 6 months}
```

**Constraints:**
- All 5 dimensions required
- Each is 1-2 sentences
- Provenance labels expected (mostly `[网络搜索]`)

---

## 🎯 Meeting Objectives

```markdown
## 🎯 Meeting Objectives

### Success Definition
{1-2 sentences: what does a successful meeting look like from AWS's perspective}

### Strategic Alignment
{1-2 sentences: how this meeting fits into the broader deal strategy / EP}

### Objectives Detail

#### Objective 1: {title}
- **Context:** {why this matters}
- **Talking Points:** 
  - {point 1}
  - {point 2}
  - {point 3}
- **Ask:** {specific request to make}

#### Objective 2: {title}
- **Context:** ...
- **Talking Points:** ...
- **Ask:** ...

### ⚠️ Anticipated Concerns

#### {Concern 1 title}
- **Acknowledge:** {validate their concern}
- **Pivot:** {redirect to our strength}
- **Elevate:** {raise to strategic level}
- **💣 Landmine:** {topic to absolutely avoid, if any}

#### {Concern 2}
...

### ➡️ Proposed Next Steps

| Tier | Proposed Step | Condition |
|------|--------------|-----------|
| 🟢 Ideal | {best outcome next step} | {if everything goes perfectly} |
| 🟡 Acceptable | {good enough next step} | {if partially successful} |
| ⚪ Minimum | {minimum viable next step} | {if limited progress} |
```

**Constraints:**
- 2-4 objectives, each with Context + Talking Points + Ask
- Anticipated Concerns: 1-3 items, each with Acknowledge-Pivot-Elevate
- Landmine is optional but recommended for EB
- Next Steps: always 3 tiers

---

## 📊 AWS Account Background

```markdown
## 📊 AWS Account Background

| Field | Value |
|-------|-------|
| Geo / Segment | {region / enterprise tier} |
| Current AWS Spend | {annual spend or range} [销售确认] |
| PPA Status | {yes/no, details} |
| Contract Expiry | {date if applicable} |

### Account Summary
- **Relationship Tenure:** {how long as customer}
- **Key Workloads on AWS:** {what they run today}
- **Growth Trajectory:** {spending trend}
- **Open Opportunities:** {other active deals}
- **Previous Executive Interactions:** {past EBC/exec meetings, outcomes}
```

**Constraints:**
- Table fields: mark unknown as `[待确认]`
- Account Summary: all 5 items required
- Sensitive financial data must be marked `[销售确认]`

---

## 📎 Appendix (optional)

```markdown
## 📎 Appendix

### Previous Meeting Notes
{Summary of last interaction, key takeaways, open items}

### Relevant Customer Success Stories
- **{Customer A}:** {1-2 sentences, relevance to this deal}
- **{Customer B}:** {1-2 sentences}

### Competitive Intelligence
- **Current Vendor:** {who they use today}
- **Competitor Positioning:** {who else is bidding}
- **Our Differentiation:** {why we win}
```

---

## Badge Value Enums

| Field | Allowed Values |
|-------|---------------|
| Stance | `champion`, `supporter`, `neutral`, `non-supporter`, `unknown` |
| Next Step Tier | `ideal`, `acceptable`, `minimum` |

---

## Validation Rules

1. Frontmatter: all required fields present, `classification` field exists
2. All required sections present (5 sections; Appendix optional)
3. At least 1 customer attendee with all 5 dimensions
4. At least 1 AWS attendee
5. At least 2 meeting objectives with full structure
6. Company Profile has all 5 dimensions
7. Account Background table has at least Geo/Segment and Spend fields
