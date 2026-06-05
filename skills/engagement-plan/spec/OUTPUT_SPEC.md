# Engagement Plan — Structured Markdown Output Spec

> This defines the exact Markdown format the LLM must output for Engagement Plan documents.
> The renderer parses this format deterministically into HTML/PDF/Word.

---

## Frontmatter (YAML, required)

```yaml
---
type: engagement-plan
customer: "GlobalRetail Inc."
opportunity: "Cloud Migration - Data Center Exit"
stage: "Technical Validation"
tcv: "$3.2M"
source: "new-logo"
created: "2026-01-15"
version: "2026-03-20"
---
```

**All fields required** except `tcv` (omit if unknown).

---

## Section Structure (fixed order, fixed headers)

EP has 3 major sections matching the template:
1. Opportunity Snapshot + Win Strategy
2. Engagement Plan (People + Roadmap + Estimate)
3. Execution Log

---

## 📊 Opportunity Snapshot

```markdown
## 📊 Opportunity Snapshot

| Field | Value |
|-------|-------|
| Customer | {customer name} |
| Opportunity | {opportunity name} |
| Stage | {current stage} |
| TCV | {total contract value} |
| Source | {new-logo / existing-customer} |
| Timeline | {target close date or timeframe} |
| Decision Maker | {primary decision maker name + title} |
| Champion | {champion name + title} |
| Competitive | {main competitor(s)} |

### 🎆 Why Now

{1-2 paragraphs explaining urgency drivers — customer-side and time-based}

### 🎯 Deal Objective

{1-2 sentences: what does "winning" look like for this deal}

### ⚔️ Win Strategy

{2-3 sentences: how we win this deal — differentiation, approach, key levers}

### ⚠️ Key Risks

- {Risk 1 + mitigation}
- {Risk 2 + mitigation}
- {Risk 3 + mitigation}
```

**Constraints:**
- Snapshot table: all fields required (mark unknown as `[待确认]`)
- Why Now: must articulate urgency, not just background
- Win Strategy: must be specific to THIS deal, not generic
- Key Risks: 2-4 items, each with mitigation approach

---

## 👥 Key Stakeholders

```markdown
## 👥 Key Stakeholders

### {Person Name}
- **Title:** {title}
- **Stance:** {champion|supporter|neutral|non-supporter|unknown}
- **Priority:** {must-meet|important|nice-to-have}
- **Role:** {decision-maker|technical-evaluator|influencer|end-user|champion|blocker|sponsor|economic-buyer}
- **What They Care About:** {key concerns and motivations, 1-2 sentences} [销售确认]
- **What We Need:** {specific outcomes needed from this person}
- **🎯 How to Win:** {tactical approach for this person}

### {Person Name 2}
...
```

**Constraints:**
- Minimum 2 stakeholders, recommend 3-6
- `Stance`, `Priority`, `Role` are enums
- `How to Win` is always present and specific
- Provenance labels on assertions where applicable
- Order by Priority (must-meet first)

---

## 🗺️ Engagement Roadmap

```markdown
## 🗺️ Engagement Roadmap

**Progress:** {N}/{Total} Milestones Complete

### Milestone 1: {brief description}
- **Status:** {done|next|planned}
- **👤 Stakeholders:** {who is involved}
- **🏢 AWS Resources:** {AM, SA, specialist, etc.}
- **📅 Timeline:** {Week X-Y or date range}
- **Exit Criteria:** {what "done" looks like for this milestone}

### Milestone 2: {brief description}
- **Status:** {done|next|planned}
- **👤 Stakeholders:** {who}
- **🏢 AWS Resources:** {who}
- **📅 Timeline:** {when}
- **Exit Criteria:** {what done looks like}

### Milestone 3: ...
...
```

**Constraints:**
- 3-7 milestones (covers full deal cycle)
- Exactly ONE milestone has `Status: next` (the current focus)
- Milestones before it: `done`; after: `planned`
- Each milestone has all 5 fields
- Timeline uses relative weeks OR absolute dates

---

## 📋 Next Milestone Detail

```markdown
## 📋 Next Milestone Detail

| Field | Value |
|-------|-------|
| Milestone | {milestone description} |
| Objective | {what this milestone achieves} |
| Customer Attendees | {names + titles} |
| AWS Team | {names + roles} |
| Target Date | {date} |
| Format | {online/on-site/hybrid} |
| Success Looks Like | {observable outcome} |

**Triggers Call Plan generation when confirmed by sales.**
```

**Constraints:**
- This section triggers downstream CP/EB generation
- All fields required
- Must align with the `next` milestone in Roadmap

---

## 📐 Estimate & Contingency

```markdown
## 📐 Estimate & Contingency

### Best Case
- **Close Date:** {date}
- **Remaining Meetings:** {N}
- **Confidence:** {high|medium|low}
- **Assumption:** {what must go right}

### Worst Case
- **Close Date:** {date}
- **Remaining Meetings:** {N}
- **Risk Factor:** {what could go wrong}
- **Plan B:** {contingency approach}
```

**Constraints:**
- Both cases always present
- Confidence is an enum
- Plan B must be actionable

---

## 📝 Execution Log

```markdown
## 📝 Execution Log

### Engagement #{N} — {date}
- **Attendees:** {list}
- **Planned:** {what was planned per CP/EB}
- **Actual:** {what actually happened}
- **👥 People Updates:** {stance changes, new info about stakeholders}
- **💡 Key Learnings:** {what we learned}
- **🔄 Plan Adjustment:** {how the plan changes as a result}

### Engagement #{N-1} — {date}
...
```

**Constraints:**
- Most recent engagement first (reverse chronological)
- Each entry maps to a CP+PMR pair
- Empty on initial EP creation (populated after first PMR)
- People Updates references specific stakeholder stance changes

---

## 📜 Change Log

```markdown
## 📜 Change Log

| Date | Source | Change Summary |
|------|--------|---------------|
| {YYYY-MM-DD HH:MM} | {PMR/CP/EB/OP/User} | {one-line description} |
| ... | ... | ... |
```

**Constraints:**
- Newest first
- Every EP modification must add a row
- Source = which skill/action triggered the change

---

## Badge Value Enums

| Field | Allowed Values |
|-------|---------------|
| Stance | `champion`, `supporter`, `neutral`, `non-supporter`, `unknown` |
| Priority | `must-meet`, `important`, `nice-to-have` |
| Role | `decision-maker`, `technical-evaluator`, `influencer`, `end-user`, `champion`, `blocker`, `sponsor`, `economic-buyer` |
| Milestone Status | `done`, `next`, `planned` |
| Confidence | `high`, `medium`, `low` |

---

## Validation Rules

1. Frontmatter: all required fields present
2. All required sections present (8 sections)
3. Badge values match enum lists
4. Exactly 1 milestone with `Status: next`
5. At least 2 stakeholders defined
6. Next Milestone Detail aligns with `next` milestone in Roadmap
7. Change Log present (can be empty on first creation)
8. Execution Log present (can be empty on first creation)
