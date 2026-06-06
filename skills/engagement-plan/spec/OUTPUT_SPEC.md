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

EP has 3 top-level `##` sections matching the reference template:
1. `## 1. 📊 Opportunity Snapshot` — deal context + progress
2. `## 2. 👥 Engagement Plan` — stakeholders, roadmap, estimate, next milestone (all as `###`)
3. `## 3. 📝 Execution Log` — reverse-chronological engagement history

### Rules:
1. Section headers use format: `## {N}. {emoji} {Title}` for top-level, `### {emoji} {Title}` for subsections
2. Subsection headers use `###` (Key Stakeholders, Engagement Roadmap, Estimate & Contingency, Next Milestone Detail are ALL under `## 2.`)
3. Stance/Role/Priority values written directly as field values (renderer maps to badge colors)
4. Tables use standard Markdown table syntax
5. Each section is REQUIRED unless marked (optional)

---

## 1. 📊 Opportunity Snapshot

```markdown
## 1. 📊 Opportunity Snapshot

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

## 2. 👥 Engagement Plan

```markdown
## 2. 👥 Engagement Plan
```

This is the core section containing 4 subsections (all `###` level):

### 👥 Key Stakeholders

```markdown
### 👥 Key Stakeholders

**{Person Name}** — {Title}

| Dimension | Details |
|---|---|
| **Engagement Priority** | `{e.g., "Must Meet — 没有他的技术签字，采购不会放PO。必须在6月15日前 engage。"}` [销售确认] |
| **Role in This Deal** | `{e.g., "Technical Evaluator — 负责架构评审，有一票否决权。"}` [销售确认] |
| **Current Stance** | `{e.g., "Supporter — 在 WAR 后对30%成本优化潜力表现出浓厚兴趣，主动索要了详细报告。"}` |
| **What They Care About** | `{e.g., "董事会要求Q4前降低云支出20%。上季度财报被点名基础设施成本超支。"}` [网络搜索] |
| **Profiling** | `{e.g., "工程师出身，数据驱动。偏好30分钟 deep dive，入职8个月需要可见转型成果。"}` |
| **What We Need From Them** | `{e.g., "1) 5月底前引荐 CFO。2) 分享内部评估标准文档。3) 6月架构评审会上呈现联合 case。"}` |
| **How to Win Them** | `{e.g., "1) 先搞定 VP Eng — CTO 高度信任其技术判断。2) 提供 TCO 对比。3) 安排 peer-level briefing。"}` |
```

**Constraints:**
- Minimum 2 stakeholders, recommend 3-6
- Each person uses table format with `| Dimension | Details |` header
- `Engagement Priority`, `Role in This Deal`, `Current Stance` use enum values followed by detailed explanation
- Each field must be actionable — not single-word labels
- Order by Priority (must-meet first)

### 📍 Engagement Roadmap

```markdown
### 📍 Engagement Roadmap

| # | Milestone | Key Stakeholders | AWS Team | Status |
|---|-----------|-----------------|----------|--------|
| 1 | {outcome-oriented milestone description with customer action} | {names or roles} | {AM, SA, etc.} | Done |
| 2 | {milestone description} | {names} | {team} | **Next** ↓ |
| 3 | {milestone description} | {names} | {team} | Planned |
| 4 | {milestone description} | {names} | {team} | Planned |
| 5 | {milestone description} | {names} | {team} | Planned |
```

**Constraints:**
- 3-7 milestones (covers full deal cycle)
- Exactly ONE milestone has Status: `**Next** ↓` (the current focus, expanded in Next Milestone Detail)
- Milestones before it: `Done`; after: `Planned`
- Each milestone must be outcome-oriented with customer action (not activity-based)
- Status values: `Done`, `**Next** ↓`, `Planned`, `Skipped`

### 📐 Estimate & Contingency

```markdown
### 📐 Estimate & Contingency

| | Best Case | Worst Case |
|---|-----------|-----------| 
| **Milestones to Close** | {N} | {N} |
| **Timeline** | {N weeks} | {N weeks} |

#### Stakeholder Risk & Leverage

| At-Risk Stakeholder | Red Flag | Leverage Source | Plan B |
|---------------------|----------|-----------------|--------|
| {name} | {red flag type + detail} | {leverage person + relationship} | {ordered actions} |

#### Milestone Risk & Contingency

| 里程碑节点 | 风险项 | 触发条件 | 影响 | Plan B |
|---------------|-----------|-------------------|--------|--------|
| {#N milestone} | 🧑 {person risk} or 🚩 {process risk} | {specific trigger} | {time/scope impact} | {alternative path} |
```

**Constraints:**
- Best/Worst Case always present
- Stakeholder Risk: only for Neutral/Non-Supporter/Adversary or Must-Meet-but-not-contacted
- Milestone Risk: 2-3 highest risk nodes from Roadmap
- All Plan B must pass "Tuesday Morning Test" (actionable immediately if Plan A fails)
- Risk items tagged 🧑 (person) or 🚩 (process)

### 📋 Next Milestone Detail

```markdown
### 📋 Next Milestone Detail

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

## 3. 📝 Execution Log

```markdown
## 3. 📝 Execution Log

### Engagement #{n} - {Date} - {Attendees}

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
| Milestone Status | `Done`, `**Next** ↓`, `Planned`, `Skipped` |
| Confidence | `high`, `medium`, `low` |

---

## Validation Rules

1. Frontmatter: all required fields present
2. All 3 top-level sections present (Opportunity Snapshot, Engagement Plan, Execution Log)
3. Badge values match enum lists
4. Exactly 1 milestone with Status: `**Next** ↓`
5. At least 2 stakeholders defined
6. Next Milestone Detail aligns with `Next ↓` milestone in Roadmap
7. Execution Log present (can be empty on first creation)
8. Engagement Progress stage matches frontmatter `stage` field
