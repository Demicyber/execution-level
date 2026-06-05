# Post-Meeting Report — Structured Markdown Output Spec

> This defines the exact Markdown format the LLM must output for PMR documents.
> The renderer parses this format deterministically into PDF (ReportLab direct rendering).

## ⚠️ MANDATORY COMPLIANCE

**This spec is the ONLY accepted output format. The agent MUST follow it exactly:**
- All 5 sections MUST appear in exact order: 1. Outcome Assessment → 2. Meeting Insights → 3. What Changed — EP Update → 4. Next Steps — Planned vs Actual → 5. Customer Recap Email
- Section headers MUST use `## N. {Title}` format (numbered)
- Section 5 (Customer Recap Email) is REQUIRED — agent must prompt user "Would you like me to draft a customer recap email?" and include the section either with the draft or with the prompt text
- Meeting Insights MUST contain all three subsections: Customer Sentiment, Key Findings, Information Gap Check
- What Changed MUST contain: EP Update table + Execution Log Update + Agent Recommendation
- Next Steps MUST contain: Comparison table + Action Items table
- Customer Recap Email MUST contain: Subject line, email body, and "Excluded from email" list
- Do NOT skip the email section — it is the final handoff deliverable of every PMR
- Violation of this spec will result in rendering failures. No exceptions.

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

PMR has 5 sections:
1. Outcome Assessment
2. Meeting Insights (Customer Sentiment + Key Findings + Information Gap Check)
3. What Changed — EP Update (EP Update table + Execution Log Entry + Agent Recommendation)
4. Next Steps — Planned vs Actual (Comparison + Action Items)
5. Customer Recap Email (Handoff)

### Rules:
1. Section headers MUST use `## N. {Title}` format matching template
2. Sub-sections use `###`
3. Result/Stance/Status values written directly as field values (renderer maps to badge colors)
4. Tables use standard Markdown table syntax
5. All 5 sections REQUIRED (Section 5 may be a prompt to user)

---

## 1. Outcome Assessment

```markdown
## 1. Outcome Assessment

| # | Target Meeting Outcome | Result | Evidence & Notes |
|---|----------------------|--------|-----------------|
| 1 | {auto-pulled from CP/EB} | ✅ / ⚠️ / ❌ | {specific customer words/actions as evidence} |
| 2 | {outcome 2} | ✅ / ⚠️ / ❌ | {evidence} |

**Fallback Outcome Assessment:** {was fallback needed? what happened?}

**Stage Progression:** ( {current} ) → ( {target} ) — ✅ Achieved / ❌ Not achieved — {reason}
```

**Constraints:**
- Outcomes auto-pulled from related CP (Section 2) or EB (Section 3)
- Result symbols: ✅ Achieved, ⚠️ Partial, ❌ Not achieved
- Evidence must be specific customer actions/words (not "went well")
- Stage Progression: always present, even if "no change"
- Fallback Outcome Assessment: always present

---

## 2. Meeting Insights

```markdown
## 2. Meeting Insights

### Customer Sentiment

| Attendee | Stance Before | Stance After | Evidence |
|----------|--------------|--------------|----------|
| {name} | {stance before} | {stance after} | {specific words/actions showing shift} |
| {name2} | {before} | {after} | {evidence} |

### Key Findings

| # | Finding | Source | Implication for Strategy |
|---|---------|--------|------------------------|
| 1 | {new information discovered} | {who said it / observed behavior} | {what it means + which EP section to update} |
| 2 | {finding} | {source} | {implication} |
| 3 | {finding} | {source} | {implication} |

### Information Gap Check

| # | Question (from Call Plan) | Status | Answer / Notes |
|---|--------------------------|--------|----------------|
| 1 | {auto-pulled from CP Section 4} | ✅ Answered / ❌ Still a gap | {answer or plan to get it} |
| 2 | {question} | ✅ / ❌ | {notes} |
```

**Constraints:**
- Customer Sentiment: one row per attendee present in meeting
- Before/After use Holden stance values (sponsor/supporter/neutral/non-supporter/adversary)
- Key Findings: 2-5 items, only information that changes strategy (not meeting minutes)
- Gap Check: auto-pulled from CP's Information to Gather section
- Status: ✅ Answered or ❌ Still a gap

---

## 3. What Changed — EP Update

```markdown
## 3. What Changed — EP Update

| # | EP Section to Update | Change Type | What to Write |
|---|---------------------|-------------|---------------|
| 1 | {Key Stakeholders / Win Strategy / Roadmap / etc.} | {Update / Add / Remove / Confirm} | {specific change description} |
| 2 | {section} | {type} | {description} |
| 3 | {section} | {type} | {description} |

**Execution Log Update:** {milestone status → Done/Partial/Repeat, reason}

### Agent Recommendation

> {2-4 sentences: assessment + recommended next actions + stage-relevant evidence + referrals to other skills}
>
> ⚠️ If stage-relevant evidence emerged, recommend invoking `opportunity-progression` for evaluation.
```

**Constraints:**
- EP Update table: covers all changed dimensions (Key Stakeholders, Roadmap, Win Strategy, Estimate & Contingency, Competitive)
- Change Type: `Update`, `Add`, `Remove`, `Confirm` (confirm = previously assumed, now verified)
- Execution Log Update: marks current milestone completion status
- Agent Recommendation: must include referrals to other skills when signals detected
- PMR does NOT make stage advancement judgments (flags evidence for Opportunity Progression)

---

## 4. Next Steps — Planned vs Actual

```markdown
## 4. Next Steps — Planned vs Actual

### Comparison

| # | Planned (from Call Plan) | Actual (agreed in meeting) | Delta |
|---|-------------------------|---------------------------|-------|
| 1 | {auto-pulled from CP Section 7} | {what was actually agreed} | {on track / exceeded / fell short — why} |
| 2 | {planned} | {actual} | {delta} |
| NEW | — | {unexpected item not in CP} | {why added} |

### Action Items

| # | Priority | Action Item | Owner | ETA | Status |
|---|----------|------------|-------|-----|--------|
| 1 | High | {specific action} | {name (AWS/Customer)} | {date} | Open |
| 2 | High | {action} | {owner} | {date} | Open |
| 3 | Medium | {action} | {owner} | {date} | Open |
```

**Constraints:**
- Comparison: maps 1:1 to CP Next Steps; add "NEW" rows for unexpected items
- Action Items: sorted by Priority (high first)
- Priority: `High`, `Medium`, `Low`
- Status: `Open`, `In Progress`, `Done`
- Every action needs Owner + ETA (no vague "TBD")
- Recommend 3-7 action items

---

## 5. Customer Recap Email

```markdown
## 5. Customer Recap Email

**Subject:** Follow-up: {meeting topic} — {Customer} × AWS {date}

---

{email body — professional, customer-facing, includes: thanks, key discussion points, agreed action items, proposed next steps}

---

**Excluded from email (internal only):**
- {item 1 — e.g., competitive analysis}
- {item 2 — e.g., stakeholder sentiment}
```

**Constraints:**
- Agent prompts user: "Would you like me to draft a customer recap email?" before generating
- Must NOT contain: internal strategy, pricing analysis, MEDDPICC terms, sentiment assessments
- Must include: thanks, key discussion points, agreed action items, proposed next steps
- "Excluded" section reminds agent what NOT to put in customer-facing email
- If user declines, section contains only the prompt text

---

## Badge Value Enums

| Field | Allowed Values |
|-------|---------------|
| Result | ✅ (achieved), ⚠️ (partial), ❌ (not-achieved) |
| Stance | `sponsor`, `supporter`, `neutral`, `non-supporter`, `adversary` |
| Gap Status | ✅ Answered, ❌ Still a gap |
| Change Type | `Update`, `Add`, `Remove`, `Confirm` |
| Priority | `High`, `Medium`, `Low` |
| Action Status | `Open`, `In Progress`, `Done` |

---

## Validation Rules

1. Frontmatter: all required fields present
2. All 5 sections present
3. Outcome Assessment has at least 1 outcome row
4. Customer Sentiment has at least 1 attendee
5. Key Findings has at least 2 items
6. Action Items has at least 2 items
7. All badge values match enum lists
8. EP Update table has at least 1 change row
