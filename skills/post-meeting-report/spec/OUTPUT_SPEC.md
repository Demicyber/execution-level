# Post-Meeting Report — Structured Markdown Output Spec

> This defines the exact Markdown format the LLM must output for Post-Meeting Report documents.
> The renderer parses this format deterministically into PDF (ReportLab direct rendering).

## ⚠️ MANDATORY COMPLIANCE

**This spec is the ONLY accepted output format. The agent MUST follow it exactly:**
- Every section listed below MUST appear in the output, in the exact order specified
- Section headers MUST match character-for-character (including emoji and numbering)
- Field names within tables MUST use the exact names shown
- Do NOT invent new sections, skip sections, reorder sections, or rename fields
- Do NOT use alternative field names or legacy formats — only what is documented here
- Violation of this spec will result in rendering failures. No exceptions.

---

## Frontmatter (YAML, required)

```yaml
---
type: post-meeting-report
customer: "GlobalRetail Inc."
opportunity: "Cloud Migration - Data Center Exit"
meeting_title: "Technical Discovery - CTO + IT Director"
date: "2026-04-10"
recorded_by: "Agent (from sales debrief)"
related_document: "call-plan-2026-04-08"
version: "2026-04-10"
---
```

**All fields required.**

---

## Section Structure (fixed order, fixed headers)

PMR has 5 top-level `##` sections matching the reference template:
1. `## 1. 📊 Outcome Assessment` — planned vs actual outcomes
2. `## 2. 💡 Meeting Insights` — sentiment shifts, key findings, info gaps
3. `## 3. 🔄 What Changed — EP Update` — specific EP field changes + recommendation
4. `## 4. 📋 Next Steps — Planned vs Actual` — comparison + action items
5. `## 5. ✉️ Customer Recap Email (Handoff)` — draft email for customer

### Rules:
1. Section headers use format: `## {N}. {emoji} {Title}`
2. Sub-sections use `###`
3. Provenance labels use `[销售确认]` or `[网络搜索]` inline — no label = AI推断
4. Tables use standard Markdown table syntax
5. Each section is REQUIRED
6. Data auto-pulled from related Call Plan where marked

---

## 1. 📊 Outcome Assessment

```markdown
## 1. 📊 Outcome Assessment

| # | Target Meeting Outcome | Result | Evidence & Notes |
|---|------|------|------|
| 1 | {auto-pulled from Call Plan Section 2} | ✅ / ⚠️ / ❌ | {客户具体说了什么/做了什么} |
| 2 | {auto-pulled} | ✅ / ⚠️ / ❌ | {evidence} |

**Fallback Outcome Assessment:** {如果主目标未达成，Fallback Outcome 是否达成？}

**Stage Progression:** ( {current} ) → ( {target} ) — ✅ Achieved / ❌ Not achieved — {reason}
```

**Constraints:**
- Auto-pull Target Outcomes from related Call Plan Section 2
- Result uses exactly: ✅ (Achieved), ⚠️ (Partial), ❌ (Not achieved)
- Evidence must be specific customer actions/words (not subjective feelings)
- Fallback Outcome Assessment always present
- Stage Progression compares planned vs actual stage movement

---

## 2. 💡 Meeting Insights

```markdown
## 2. 💡 Meeting Insights

### Customer Sentiment

| Attendee | Stance Before | Stance After | Evidence |
|----------|--------------|--------------|----------|
| {name} | {from Call Plan: e.g., Neutral} | {e.g., Supporter} | {what they said/did showing the shift} |

### Key Findings

| # | Finding | Source | Implication for Strategy |
|---|---------|--------|------------------------|
| 1 | {new information discovered} | {who said it / how we learned it} | {what this means for strategy + which EP section to update} |
| 2 | | | |

### Information Gap Check

| # | Question (from Call Plan) | Status | Answer / Notes |
|---|--------------------------|--------|----------------|
| 1 | {auto-pulled from Call Plan Section 4} | ✅ Answered / ❌ Still a gap | {answer if obtained, or plan for next time} |
| 2 | {auto-pulled} | ✅ / ❌ | |
```

**Constraints:**
- Customer Sentiment: compare stance before/after using Holden 5-level terminology
- Evidence must be specific customer behavior (not "感觉他很积极")
- Key Findings: only items that change strategy or need EP update (not meeting minutes)
- Information Gap Check: auto-pulled from Call Plan Section 4, status binary ✅/❌

---

## 3. 🔄 What Changed — EP Update

```markdown
## 3. 🔄 What Changed — EP Update

| # | EP Section to Update | Change Type | What to Write |
|---|---------------------|-------------|---------------|
| 1 | {e.g., Key Stakeholders} | {Update / Add / Remove / Confirm} | {specific change with evidence} |
| 2 | {e.g., Win Strategy} | {Add} | {new information to incorporate} |
| 3 | {e.g., Roadmap} | {Update} | {timeline/milestone adjustment} |

**Execution Log Update:** {当前 milestone 状态 → Done/Partial/Repeat，原因}

### Agent Recommendation

> - *What stage-relevant evidence emerged?*
> - *Does the current strategy need adjustment?*
> - *What should the next milestone/interaction focus on?*
> - *If significant stage evidence: recommend invoking `opportunity-progression` for evaluation.*
```

**Constraints:**
- Each change must point to a specific EP section/field
- Change Type: `Update`, `Add`, `Remove`, `Confirm` (之前假设 → 现在确认)
- What to Write: specific enough for agent to execute the EP update
- Execution Log Update: always present (milestone Done/Partial/Repeat)
- Agent Recommendation: strategic assessment, NOT stage progression decision (defer to opportunity-progression skill)

---

## 4. 📋 Next Steps — Planned vs Actual

```markdown
## 4. 📋 Next Steps — Planned vs Actual

### Comparison

| # | Planned (from Call Plan) | Actual (agreed in meeting) | Delta |
|---|--------------------------|---------------------------|-------|
| 1 | {auto-pulled from Call Plan Section 7} | {what was actually agreed} | {on track / exceeded / fell short — why} |
| 2 | {auto-pulled} | {actual} | {delta} |

### Action Items

| # | Priority | Action Item | Owner | ETA | Status |
|---|----------|------------|-------|-----|--------|
| 1 | High | {specific action} | {name (AWS/Customer)} | {date} | Open |
| 2 | High | {specific action} | {name (AWS/Customer)} | {date} | Open |
| 3 | Medium | {specific action} | {name (AWS/Customer)} | {date} | Open |
```

**Constraints:**
- Comparison: auto-pull planned from Call Plan Section 7
- Delta: assess whether planned steps were achieved/exceeded/fell short with reason
- Action Items: each must have Owner (name + AWS/Customer), ETA (specific date), Priority, Status
- Priority: `High`, `Medium`, `Low`
- Status: `Open`, `In Progress`, `Done`, `Pending`
- If no customer commitment obtained → flag as ⚠️ red signal in Agent Recommendation

---

## 5. ✉️ Customer Recap Email (Handoff)

```markdown
## 5. ✉️ Customer Recap Email (Handoff)

> *After completing the PMR, prompt the user: "Would you like me to draft a customer recap email?" If yes, use key discussion points, agreed action items, and proposed next steps to draft.*

**Subject:** {e.g., "Re: 技术交流跟进 — 下一步行动确认"}

**To:** {customer attendees}
**CC:** {AWS team}

---

{Email body: professional, concise, customer-facing.
Structure:
1. Thank + meeting recap (2-3 sentences)
2. Key discussion points / agreed outcomes (bullet points)
3. Action items with owners and timelines
4. Proposed next step with specific date
5. Close with availability}

---
```

**Constraints:**
- Email must be customer-facing (no internal jargon, no stance labels)
- Include agreed action items with clear owners and dates
- Propose concrete next step (not "let's stay in touch")
- Professional Chinese (or English if customer is English-speaking)
- Subject line must be specific (not "Meeting Follow-up")

---

## Badge Value Enums

| Field | Allowed Values |
|-------|---------------|
| Current Stance | `sponsor`, `supporter`, `neutral`, `non-supporter`, `adversary` |
| Outcome Result | `achieved` (✅), `partial` (⚠️), `not-achieved` (❌) |
| Change Type | `update`, `add`, `remove`, `confirm` |
| Gap Status | `answered` (✅), `still a gap` (❌) |
| Action Priority | `high`, `medium`, `low` |
| Action Status | `open`, `in progress`, `done`, `pending` |

---

## Validation Rules

1. Frontmatter: all required fields present
2. All 5 sections present in correct order
3. Badge values match enum lists
4. Outcome Assessment has at least 1 outcome row with Result + Evidence
5. Customer Sentiment uses Holden 5-level stance terminology
6. What Changed table has at least 1 EP update row
7. Action Items each have Owner + ETA
8. Stage Progression assessment present
