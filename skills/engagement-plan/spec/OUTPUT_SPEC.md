# Engagement Plan — Structured Markdown Output Spec

> This defines the exact Markdown format the LLM must output for Engagement Plan documents.
> The renderer parses this format deterministically into PDF (ReportLab direct rendering).

## ⚠️ MANDATORY COMPLIANCE

**This spec is the ONLY accepted output format. The agent MUST follow it exactly:**
- Every section listed below MUST appear in the output, in the exact order specified
- Section headers MUST match character-for-character (including emoji and numbering)
- Field names within stakeholder cards, milestone tables, etc. MUST use the exact names shown
- Do NOT invent new sections, skip sections, reorder sections, or rename fields
- Do NOT use alternative field names or legacy formats — only what is documented here
- The Engagement Progress bar MUST appear inside the Opportunity Snapshot section (after Win Strategy)
- The Engagement Roadmap MUST use TABLE format (not bullet-field milestones)
- Stakeholder fields MUST use the 7 exact field names specified (Engagement Priority, Role in This Deal, Current Stance, What They Care About, Profiling, What We Need From Them, How to Win Them)
- Violation of this spec will result in rendering failures. No exceptions.

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
1. Opportunity Snapshot (including Engagement Progress)
2. Engagement Plan (Key Stakeholders + Engagement Roadmap + Estimate & Contingency + Next Milestone Detail)
3. Execution Log

### Rules:
1. Section headers MUST match exactly (emoji + text)
2. Sub-sections use `###`
3. Stance/Role/Priority values written directly as field values (renderer maps to badge colors)
4. Provenance labels use `[销售确认]` or `[网络搜索]` inline — no label = AI推断
5. Tables use standard Markdown table syntax
6. Each section is REQUIRED unless marked (optional)

---

## 📊 Opportunity Snapshot

```markdown
## 📊 Opportunity Snapshot

| Field | Value |
|-------|-------|
| Customer | {company name} · {industry} · {New Logo / Existing Customer} |
| Opportunity Name | {opportunity name} |
| Deal Value | {ARR or TCV} |
| Current Stage | {Prospect / Qualified / Technical Validation / Business Validation / Committed / Closed} |
| Target Launch Date | {YYYY-MM-DD, quarter, or relative time} |

### Why Now

{1-2 paragraphs: [specific trigger event] + [hard deadline] + [cost of inaction]}

### Deal Objective

{1-2 sentences: [action] + [scope] + [value] + [timeline] + [aligned to Why Now]}

### Win Strategy

{2-3 sentences: [core differentiation] + [customer's #1 priority] + [key execution actions]}

**Key Risks:** {1-2 risk factors that could lose the deal, with full sentences}

### 📈 Engagement Progress

[Prospect] ━━━ [Qualified] ━━━ [Tech Val] ━━━ [Biz Val] ━━━ [Committed] ━━━ [Closed]
                                ▲ We are here
```

**Constraints:**
- Snapshot table: all fields required (mark unknown as `[待确认]`)
- Why Now: must articulate urgency with trigger event + hard deadline
- Win Strategy: must be specific to THIS deal, not generic
- Key Risks: 1-2 items as complete sentences (inline under Win Strategy, not separate section)
- Engagement Progress: auto-generated from Current Stage, marks current position on track

---

## 👥 Key Stakeholders

```markdown
## 👥 Key Stakeholders

### {Person Name}
- **Engagement Priority:** {must-meet|important|nice-to-have} — {reason + time constraint}
- **Role in This Deal:** {decision-maker|champion|influencer|blocker|evaluator|procurement} — {function + what they can block/enable}
- **Current Stance:** {sponsor|supporter|neutral|non-supporter|adversary} — {evidence + attitude toward competition}
- **What They Care About:** {specific business pressure/KPI + pressure source + time constraint}
- **Profiling:** {communication style + decision mode + personal motivation + how to communicate}
- **What We Need From Them:** {numbered, specific, verifiable asks + time}
- **How to Win Them:** {ordered specific actions + political constraints + who from AWS engages}

### {Person Name 2}
...
```

**Constraints:**
- Minimum 2 stakeholders, recommend 3-6
- `Engagement Priority`, `Role in This Deal`, `Current Stance` use enum values followed by detailed explanation
- Each field must be actionable — not single-word labels
- Provenance labels on assertions where applicable
- Order by Priority (must-meet first)

---

## 📍 Engagement Roadmap

```markdown
## 📍 Engagement Roadmap

| # | Milestone | Key Stakeholders | AWS Team | Status |
|---|-----------|-----------------|----------|--------|
| 1 | {outcome-oriented milestone description with customer action} | {names or roles} | {AM, SA, etc.} | Done |
| 2 | {milestone description} | {names} | {team} | **Next ↓** |
| 3 | {milestone description} | {names} | {team} | Planned |
| 4 | {milestone description} | {names} | {team} | Planned |
| 5 | {milestone description} | {names} | {team} | Planned |
```

**Constraints:**
- 3-7 milestones (covers full deal cycle)
- Exactly ONE milestone has Status: `**Next ↓**` (the current focus, expanded in Next Milestone Detail)
- Milestones before it: `Done`; after: `Planned`
- Each milestone must be outcome-oriented with customer action (not activity-based)
- Milestone description: 15-50 characters, [who] + [what action/decision] + [what output/authorization]

---

## 📐 Estimate & Contingency

```markdown
## 📐 Estimate & Contingency

| | Best Case | Worst Case |
|---|-----------|-----------|
| **Milestones to Close** | {N} | {N} |
| **Timeline** | {N weeks} | {N weeks} |

#### Stakeholder Risk & Leverage

| At-Risk Stakeholder | Red Flag | Leverage Source | Plan B |
|---------------------|----------|-----------------|--------|
| {name} | {red flag type + detail} | {leverage person + relationship} | {ordered actions} |
| {name2} | {red flag} | {leverage} | {plan b} |

#### Milestone Risk & Contingency

| Milestone Node | Risk Item | Trigger Condition | Impact | Plan B |
|---------------|-----------|-------------------|--------|--------|
| {#N milestone} | 🧑 {person risk} or 🚩 {process risk} | {specific trigger} | {time/scope impact} | {alternative path} |
| {same or other} | 🚩 {risk} | {trigger} | {impact} | {plan b} |
```

**Constraints:**
- Best/Worst Case always present
- Stakeholder Risk: only for Neutral/Non-Supporter/Adversary or Must-Meet-but-not-contacted
- Milestone Risk: 2-3 highest risk nodes from Roadmap
- All Plan B must pass "Tuesday Morning Test" (actionable immediately if Plan A fails)
- Risk items tagged 🧑 (person) or 🚩 (process)

---

## 📋 Next Milestone Detail

```markdown
## 📋 Next Milestone Detail

**Milestone #{n}** — {Target Date}

**Objective:** {strategic purpose + why this step is most important now + relation to overall roadmap}

**Customer Attendees & Target Outcome:**
- {Name (Title)} — {current stance}, target {next stance}: {specific verifiable action needed from them}
- {Name2 (Title)} — {current stance}, target {next stance}: {specific action}

**AWS Team:** {names + roles + responsibilities}

**Key Questions & Discussion Points:**
- {research-gap based question targeting specific attendee}
- {hypothesis-led question}
- {question tied to stage exit criteria}
```

**Constraints:**
- Must align with the `Next ↓` milestone in Roadmap
- Each Customer Attendee has per-person target outcome (stance movement + specific action)
- Key Questions: 3-5, purpose-driven, tailored to attendees' known concerns
- Triggers Call Plan generation when confirmed by sales

---

## 📝 Execution Log

```markdown
## 📝 Execution Log

### Engagement #{n} — {Date} — {Attendees}

| Field | Details |
|-------|---------|
| **Planned** | {what was planned per milestone description} |
| **Actual** | {what actually happened — specific customer actions and responses} |
| **People Updates** | {stance changes using Holden 5-level: Name: Old → New (evidence)} |
| **Key Learnings** | {new information that changes strategy + which EP section to update} |
| **Plan Adjustment** | {what changes to Roadmap/Timeline/Strategy as a result} |

### Engagement #{n-1} — {Date} — {Attendees}
...
```

**Constraints:**
- Most recent engagement first (reverse chronological)
- Each entry maps to a CP+PMR pair
- Empty on initial EP creation (populated after first PMR)
- People Updates must use Holden stance terminology
- Plan Adjustment must be actionable (add milestone? change timeline? adjust strategy?)

---

## Badge Value Enums

| Field | Allowed Values |
|-------|---------------|
| Current Stance | `sponsor`, `supporter`, `neutral`, `non-supporter`, `adversary` |
| Engagement Priority | `must-meet`, `important`, `nice-to-have` |
| Role in This Deal | `decision-maker`, `champion`, `influencer`, `blocker`, `evaluator`, `procurement` |
| Milestone Status | `Done`, `**Next ↓**`, `Planned`, `Skipped` |
| Confidence | `high`, `medium`, `low` |

---

## Validation Rules

1. Frontmatter: all required fields present
2. All required sections present (6 sections)
3. Badge values match enum lists
4. Exactly 1 milestone with Status: `**Next ↓**`
5. At least 2 stakeholders defined
6. Next Milestone Detail aligns with `Next ↓` milestone in Roadmap
7. Execution Log present (can be empty on first creation)
8. Engagement Progress stage matches frontmatter `stage` field
