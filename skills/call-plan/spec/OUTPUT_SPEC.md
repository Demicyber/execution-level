# Call Plan — Structured Markdown Output Spec

> This defines the exact Markdown format the LLM must output for Call Plan documents.
> The renderer parses this format deterministically into PDF (ReportLab direct rendering).

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

### Rules:
1. Section headers MUST match exactly (emoji + text)
2. Sub-sections use `###`
3. Stance/Role/Category values written directly as bullet field values (renderer maps to badge colors)
4. Provenance labels use `[销售确认]` or `[网络搜索]` inline — no label = AI推断
5. Tables use standard Markdown table syntax
6. Each section is REQUIRED unless marked (optional)

---

## 📋 Meeting Details

> Already captured in frontmatter. Renderer auto-generates this section from YAML.
> LLM does NOT write this section in the body.

---

## 🎯 Target Meeting Outcomes

```markdown
## 🎯 Target Meeting Outcomes

| # | Customer Perspective | Our Perspective |
|---|---------------------|-----------------|
| 1 | {customer's goal from their POV} | {our goal - what we want to achieve} |
| 2 | {customer's goal 2} | {our goal 2} |

**📈 Stage Progression Target:** {stage_target description, 1 sentence}

**Fallback Outcome:** {minimum acceptable outcome if primary goals not fully met}
```

**Constraints:**
- 1-4 rows (match meeting complexity)
- Each row: customer vs. our perspective, one sentence each
- Stage Progression Target: required if `stage_target` in frontmatter
- Fallback Outcome: always required

---

## ✅ Success Criteria

```markdown
## ✅ Success Criteria

### 🟢 Ideal
- {Observable criterion 1}
- {Observable criterion 2}

### 🟡 Acceptable
- {Minimum viable criterion 1}
- {Minimum viable criterion 2}

### ⚪ Minimum
- {Walk-away criterion — below this, meeting failed}
```

**Constraints:**
- Three tiers always present (Ideal / Acceptable / Minimum)
- Each criterion must be **observable and binary** (can assess yes/no after meeting)
- 1-3 items per tier

---

## 👥 Customer Attendees

```markdown
## 👥 Customer Attendees

### {Person Name}
- **Title:** {title}
- **Stance:** {champion|supporter|neutral|non-supporter|unknown}
- **Role:** {decision-maker|technical-evaluator|influencer|end-user|champion|blocker}
- **Focus:** {what they care about, 1-2 sentences} [销售确认]
- **Communication:** {how to communicate with them, 1-2 sentences}
- **🎯 Our Goal:** {what we need from this person in THIS meeting}

### {Person Name 2}
- **Title:** ...
...
```

**Constraints:**
- One `###` block per attendee
- `Stance` and `Role` values are enums (renderer maps to badge colors)
- `Our Goal` is the most actionable field — always present
- Provenance labels on individual assertions where applicable

---

## 👥 AWS Team

```markdown
## 👥 AWS Team

| Name | Role | Purpose |
|------|------|---------|
| {name} | {role title} | {why they're in this meeting} |
| {name2} | {role2} | {purpose2} |
```

---

## 🔄 Information Exchange

```markdown
## 🔄 Information Exchange

### ❓ Questions to Ask

| Question | Target Attendee | Purpose |
|----------|----------------|---------|
| {question text} | {person name + title} | {why we're asking this} |
| ... | ... | ... |

### 📊 Information to Deliver

| What | Format | Purpose |
|------|--------|---------|
| {deliverable name} | {format: PPT/demo/doc/verbal} | {what it achieves} |
| ... | ... | ... |
```

**Constraints:**
- Questions: 2-6 rows, prioritized (most important first)
- Information: 2-5 rows
- Every question must have a clear `Purpose` tied to Target Outcomes

---

## 🛡️ Potential Objections & Responses

```markdown
## 🛡️ Potential Objections & Responses

### {Objection title}
- **Category:** {risk-trust|capability|authority|price-value|status-quo}
- **Likely From:** {person name}
- **Response:** {1-3 sentences, specific response strategy}
- **Plan B:** {fallback if primary response doesn't land}

### {Objection 2}
...
```

**Constraints:**
- 2-5 objections (match meeting complexity)
- Category is an enum (renderer maps to left-border color)
- Response must be specific (not generic)
- Plan B always present

---

## 📅 Meeting Agenda

```markdown
## 📅 Meeting Agenda

| Time | Topic | Owner | Purpose |
|------|-------|-------|---------|
| {HH:MM-HH:MM} | {topic name} | {person} | {what this slot achieves} |
| ... | ... | ... | ... |
```

**Constraints:**
- Time slots must be consecutive and cover the full meeting duration
- Every slot has an Owner
- Purpose ties back to Target Outcomes

---

## ➡️ Potential Next Steps

```markdown
## ➡️ Potential Next Steps

### ✅ If meeting goes well (primary path)

| # | Proposed Next Step | Timeline | Owner | Purpose |
|---|-------------------|----------|-------|---------|
| 1 | {concrete action} | {when} | {who} | {why} |
| 2 | ... | ... | ... | ... |

### ⏳ If customer needs more time (fallback path)

| # | Proposed Next Step | Timeline | Owner | Purpose |
|---|-------------------|----------|-------|---------|
| 1 | {action} | {when} | {who} | {why} |
| 2 | ... | ... | ... | ... |

### 🚪 If not a fit / timing wrong (graceful exit)

| # | Proposed Next Step | Timeline | Owner | Purpose |
|---|-------------------|----------|-------|---------|
| 1 | {action} | {when} | {who} | {why} |
```

**Constraints:**
- Three paths always present
- Primary: 2-4 items
- Fallback: 1-3 items
- Graceful exit: 1-2 items
- All items must have Timeline + Owner (no vague "TBD")

---

## 🚫 Disqualification Signals (optional)

```markdown
## 🚫 Disqualification Signals

- ❌ {signal 1 — if this happens, deal may be dead}
- ❌ {signal 2}
- ❌ {signal 3}
```

**Constraints:**
- Optional section (include for complex deals)
- 2-4 signals max
- Each must be observable in this meeting

---

## Badge Value Enums

| Field | Allowed Values |
|-------|---------------|
| Stance | `champion`, `supporter`, `neutral`, `non-supporter`, `unknown` |
| Role | `decision-maker`, `technical-evaluator`, `influencer`, `end-user`, `champion`, `blocker`, `sponsor` |
| Objection Category | `risk-trust`, `capability`, `authority`, `price-value`, `status-quo` |
| Priority | `high`, `medium`, `low` |
| Status | `achieved`, `partial`, `not-achieved` |

---

## Validation Rules

1. Frontmatter: all required fields present and non-empty
2. All required sections present (7 sections + AWS Team)
3. Badge values match enum lists above
4. Tables have correct column count
5. At least 1 Customer Attendee defined
6. At least 1 AWS Team member defined
7. Meeting Agenda time slots are consecutive
