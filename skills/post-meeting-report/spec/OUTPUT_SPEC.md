# Post-Meeting Report — Structured Markdown Output Spec

> This defines the exact Markdown format the LLM must output for PMR documents.
> The renderer parses this format deterministically into HTML/PDF/Word.

---

## Frontmatter (YAML, required)

```yaml
---
type: post-meeting-report
customer: "明华重工"
opportunity: "Cloud Migration - Data Center Exit"
meeting_title: "POC 验证方案评审会"
date: "2026-03-20"
recorded_by: "Sarah Chen (AM)"
related_document: "Call Plan"
related_date: "2026-03-20"
version: "2026-03-20"
---
```

**All fields required.** `related_document` = "Call Plan" or "Executive Briefing".

---

## Section Structure (fixed order, fixed headers)

PMR has 4 core sections + 1 handoff (Email):

---

## 📊 Outcome Assessment

```markdown
## 📊 Outcome Assessment

| # | Target Meeting Outcome | Result | Evidence & Notes |
|---|----------------------|--------|-----------------|
| 1 | {outcome from CP/EB} | {achieved|partial|not-achieved} | {what happened, specifics} |
| 2 | {outcome 2} | {achieved|partial|not-achieved} | {evidence} |

**Fallback Outcome:** {was fallback needed? what happened}

**📈 Stage Progression:** {Previous Stage} → {New Stage} {achieved|partial|not-achieved}
```

**Constraints:**
- Outcomes auto-pulled from related CP (Section 2) or EB (Section 3)
- Result is an enum: `achieved`, `partial`, `not-achieved`
- Evidence must be specific (not "went well")
- Stage Progression: always present, even if "no change"

---

## 🔍 Meeting Insights

```markdown
## 🔍 Meeting Insights

### 👥 Customer Sentiment Changes

| Attendee | Before | → | After | Evidence |
|----------|--------|---|-------|----------|
| {name} ({title}) | {stance before} | → | {stance after} | {what caused the change} |
| {name2} | {before} | → | {after} | {evidence} |

### 💡 Key Findings

| # | Finding | Source | Implication |
|---|---------|--------|-------------|
| 1 | {what we learned} | {who said it / observed behavior} | {what it means for the deal} |
| 2 | {finding 2} | {source} | {implication} |
| 3 | {finding 3} | {source} | {implication} |

### ❓ Information Gap Check

| Question (from Call Plan) | Status | Answer / Notes |
|--------------------------|--------|----------------|
| {question we planned to ask} | {answered|unanswered} | {what we got, or why unanswered} |
| {question 2} | {answered|unanswered} | {notes} |
```

**Constraints:**
- Sentiment Changes: one row per attendee present in meeting
- Before/After use stance enum values
- Key Findings: 2-5 items, each with source and implication
- Gap Check: pulled from CP's Questions to Ask section
- Status is enum: `answered`, `unanswered`

---

## 📝 What Changed — EP Update

```markdown
## 📝 What Changed — EP Update

| EP Section | Change Type | What to Write |
|-----------|-------------|---------------|
| Key Stakeholders | {update|add|remove} | {specific change description} |
| Engagement Roadmap | {update|add} | {milestone status change, new milestone} |
| Win Strategy | {update|no-change} | {what changed and why} |
| Estimate & Contingency | {update|add|no-change} | {timeline/risk changes} |
| Competitive | {update|no-change} | {new competitive intel} |

### 📋 Execution Log Entry

**Engagement #{N} — {date}**
- **Attendees:** {list}
- **Planned:** {from CP}
- **Actual:** {what happened}
- **👥 People Updates:** {stance changes}
- **💡 Key Learnings:** {insights}
- **🔄 Plan Adjustment:** {what changes}

### 🤖 Agent Recommendation

{2-4 sentences: agent's assessment + recommended next actions + referrals to other skills}

**Referrals:**
- {signal} → `{skill-name}`: "{recommendation sentence}"
- {signal 2} → `{skill-name}`: "{sentence}"
```

**Constraints:**
- EP Update table: all 5 rows present (use `no-change` if nothing changed)
- Change Type enum: `update`, `add`, `remove`, `no-change`
- Execution Log Entry: follows EP Execution Log format exactly
- Agent Recommendation: must include referrals to other skills when signals detected
- PMR does NOT make stage advancement judgments (only flags evidence for OP)

---

## 🔄 Next Steps — Planned vs Actual

```markdown
## 🔄 Next Steps — Planned vs Actual

| # | Planned (from CP) | Actual Agreed | Delta |
|---|-------------------|---------------|-------|
| 1 | {what CP said} | {what actually was agreed} | {difference, if any} |
| 2 | {planned} | {actual} | {delta} |
| NEW | — | {new item not in original CP} | {why added} |

### ✅ Action Items

| Priority | Action | Owner | ETA | Status |
|----------|--------|-------|-----|--------|
| {high|medium|low} | {specific action} | {person name} | {date} | {pending|in-progress|done} |
| {priority} | {action 2} | {owner} | {date} | {status} |
```

**Constraints:**
- Planned vs Actual: maps 1:1 to CP Next Steps; add "NEW" rows for unexpected items
- Action Items: sorted by Priority (high first)
- Priority enum: `high`, `medium`, `low`
- Status enum: `pending`, `in-progress`, `done`
- Every action needs Owner + ETA (no vague "TBD")
- Recommend 3-7 action items

---

## ✉️ Customer Recap Email (optional)

```markdown
## ✉️ Customer Recap Email

**Subject:** Follow-up: {meeting topic} — {Customer} × AWS {date}

---

{email body — professional, customer-facing, no internal content}

---

**Excluded from email (internal only):**
- {item 1 — e.g., competitive analysis}
- {item 2 — e.g., stakeholder sentiment}
```

**Constraints:**
- Only generated if sales confirms
- Must NOT contain: internal strategy, pricing analysis, MEDDPICC terms, sentiment assessments
- Must include: thanks, key discussion points, agreed action items, proposed next steps
- "Excluded" section reminds agent what NOT to put in

---

## Badge Value Enums

| Field | Allowed Values |
|-------|---------------|
| Result | `achieved`, `partial`, `not-achieved` |
| Stance | `champion`, `supporter`, `neutral`, `non-supporter`, `unknown` |
| Gap Status | `answered`, `unanswered` |
| Change Type | `update`, `add`, `remove`, `no-change` |
| Priority | `high`, `medium`, `low` |
| Action Status | `pending`, `in-progress`, `done` |

---

## Validation Rules

1. Frontmatter: all required fields present
2. All 4 core sections present (Email is optional)
3. Outcome Assessment has at least 1 outcome row
4. Sentiment Changes has at least 1 attendee
5. Key Findings has at least 2 items
6. Action Items has at least 2 items
7. All badge values match enum lists
8. EP Update table has all 5 EP section rows
