# Call Plan — Structured Markdown Output Spec

> This defines the exact Markdown format the LLM must output for Call Plan documents.
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
type: call-plan
customer: "GlobalRetail Inc."
opportunity: "Cloud Migration - Data Center Exit"
meeting_title: "Technical Discovery - CTO + IT Director"
date: "2026-04-10"
time: "14:00-15:00 CST"
format: "Virtual"
stage: "Qualified"
version: "2026-04-08"
---
```

**All fields required.**

---

## Section Structure (fixed order, fixed headers)

CP has 7 top-level `##` sections matching the reference template:
1. `## 1. 📋 Meeting Details` — logistics, attendees, insights
2. `## 2. 🎯 Target Meeting Outcomes` — dual-perspective goals
3. `## 3. ✅ Success Criteria` — tri-level evidence-based criteria
4. `## 4. 💡 Information Exchange` — questions to ask + insights to share
5. `## 5. ⚡ Potential Objections & Responses` — anticipated pushback + handling
6. `## 6. 📅 Meeting Agenda` — time-boxed, purpose-driven agenda
7. `## 7. 🚀 Potential Next Steps` — multi-path next actions

### Rules:
1. Section headers use format: `## {N}. {emoji} {Title}`
2. Sub-sections use `###` (Customer Attendees, AWS Attendees, etc.)
3. Provenance labels use `[销售确认]` or `[网络搜索]` inline — no label = AI推断
4. Tables use standard Markdown table syntax
5. Each section is REQUIRED

---

## 1. 📋 Meeting Details

```markdown
## 1. 📋 Meeting Details

| Field | Value |
|---|---|
| **Date & Time** | {date} {time} {timezone} |
| **Duration** | {duration} |
| **Format** | {In-person / Virtual / Hybrid} |
| **Location / Link** | {location or meeting link} |
| **Opportunity Name** | {auto from Engagement Plan} |
| **Current Sales Stage** | {Prospect / Qualified / Technical Validation / Business Validation / Committed} |

### Customer Attendees

| Name | Title | Role in Decision |
|---|---|---|
| {name} | {title} | {EB / Champion / Decision Maker / Influencer / Evaluator / End User} |

### Attendee Insights

**{Name}** — {Title}
- **Focus & Priorities:** {specific pain/KPI relevant to this meeting}
- **Communication Approach:** {behavioral guidance — how to communicate effectively}
- **Current Stance:** {Holden 5-level + evidence}
- **Our Goal:** {what we need from them in this specific meeting}

*Repeat for each customer attendee.*

### AWS Attendees

| Name | Title | Role in Meeting |
|---|---|---|
| {name} | {title} | {Lead / Support / SME / Executive Sponsor} |
```

**Constraints:**
- Meeting Details table: all fields required (mark unconfirmed as `[待确认]`)
- Customer Attendees: at least 1 attendee
- Attendee Insights: one card per customer attendee with all 4 fields
- AWS Attendees: each person must have a clear Role in Meeting purpose

---

## 2. 🎯 Target Meeting Outcomes

```markdown
## 2. 🎯 Target Meeting Outcomes

| # | Customer Perspective | Our Perspective |
|---|---|---|
| 1 | {what customer gains from this meeting} | {what we gain — specific commitment/info/access} |
| 2 | {customer value} | {our advance} |

**Target Stage Progression:** ( {current stage} ) → ( {target stage or "remain, close gap X"} )

**Fallback Outcome:** {minimum acceptable advance if primary goals not fully met}
```

**Constraints:**
- Dual-perspective format (Customer + Our)
- 1-2 outcomes (primary + optional secondary)
- Each outcome must include a customer action (not just seller activity)
- Target Stage Progression references stage-mapping.md exit criteria
- Fallback Outcome always present

---

## 3. ✅ Success Criteria

```markdown
## 3. ✅ Success Criteria

| Level | Customer Would Consider Successful If… | We Would Consider Successful If… |
|---|---|---|
| **Ideal** | {home run scenario for customer} | {best case for us — full commitment} |
| **Acceptable** | {core value delivered to customer} | {deal advancing — key info + next step secured} |
| **Minimum** | {worth their time, door stays open} | {enough info to qualify + conversation continues} |

**Disqualification Signals:** {conditions that indicate this opp should be de-prioritized}
```

**Constraints:**
- 3-tier structure (Ideal / Acceptable / Minimum)
- Dual perspective per tier
- Each criterion must be observable and binary (yes/no assessable)
- Disqualification Signals always present

---

## 4. 💡 Information Exchange

```markdown
## 4. 💡 Information Exchange

### Information to Gather

| # | Question | Target Attendee | Purpose |
|---|---|---|---|
| 1 | {tailored research-gap question} | {name/role} | {what we'll do with the answer} |
| 2 | {hypothesis-led question} | {name/role} | {purpose} |
| 3 | {question tied to stage exit criteria} | {name/role} | {purpose} |

### Information to Deliver

| # | What to Share | Format | Purpose |
|---|---|---|---|
| 1 | {teaching moment / proof point / market context} | {format} | {value to customer + how it advances our goal} |
| 2 | {insight or data} | {format} | {purpose} |
```

**Constraints:**
- Information to Gather: 3-5 questions, each with Target Attendee and Purpose
- Information to Deliver: 2-3 items, each with clear value to customer
- All items must serve Target Meeting Outcomes (Section 2)
- Questions must be research-gap based (not generic)

---

## 5. ⚡ Potential Objections & Responses

```markdown
## 5. ⚡ Potential Objections & Responses

| # | Anticipated Objection | Category | Response | Fallback | Disqualifier? |
|---|---|---|---|---|---|
| 1 | {specific objection in customer's voice} | {Status Quo / Price-Value / Capability / Risk-Trust / Authority-Process} | {Acknowledge-Reframe-Advance response} | {what to do if reframe doesn't work} | {Yes/No} |
| 2 | {objection} | {category} | {response} | {fallback} | {Yes/No} |
```

**Constraints:**
- 2-4 objections (only those that could block THIS meeting's outcomes)
- Category uses the 5 standard types: Status Quo, Price/Value, Capability, Risk/Trust, Authority/Process
- Response follows Acknowledge-Reframe-Advance pattern
- Each response ends with a question back (dialogue, not monologue)
- Fallback always present

---

## 6. 📅 Meeting Agenda

```markdown
## 6. 📅 Meeting Agenda

| Time | Topic | Owner | Purpose |
|---|---|---|---|
| {00:00–00:05} | {opening + alignment} | {AM} | {set expectations} |
| {00:05–00:20} | {discovery / discussion} | {SA / Customer} | {surface pain, validate} |
| {00:20–00:35} | {insight sharing / solution discussion} | {SA} | {teaching moment} |
| {00:35–00:50} | {co-creation / mutual planning} | {Joint} | {customer participates in designing next steps} |
| {00:50–00:55} | {summary + next steps} | {AM} | {secure concrete commitment} |
| {00:55–01:00} | Close | {AM} | — |
```

**Constraints:**
- Time format: clock time if known, relative time if not
- Every agenda item has Owner and Purpose
- Discovery/dialogue should get the most time (early stage)
- Last 5-10 minutes always reserved for next steps commitment
- Customer-centric topic naming (not "Our demo" but "Exploring solutions to X")

---

## 7. 🚀 Potential Next Steps

```markdown
## 7. 🚀 Potential Next Steps

**If meeting goes well (primary path):**

| # | Proposed Next Step | Timeline | Owner | Purpose |
|---|---|---|---|---|
| 1 | {concrete action advancing the deal} | {specific timeframe} | {who does what} | {connects to stage exit criteria} |
| 2 | {supporting action} | {timeframe} | {owner} | {purpose} |

**If customer needs more time (fallback path):**

| # | Proposed Next Step | Timeline | Owner | Purpose |
|---|---|---|---|---|
| 1 | {lower-pressure value-add} | {timeframe} | {owner} | {maintain momentum} |
| 2 | {check-in plan} | {timeframe} | {owner} | {keep door open} |

**If not a fit / timing wrong (graceful exit):**

| # | Proposed Next Step | Timeline | Owner | Purpose |
|---|---|---|---|---|
| 1 | {parting value} | {timeframe} | {owner} | {preserve relationship} |
| 2 | {future trigger} | {timeframe / trigger-based} | {owner} | {plant seed} |
```

**Constraints:**
- 3 paths: primary, fallback, graceful exit
- Each next step is SMART: Who + What + When + Why + How
- Primary path aligns with Section 2 Target Outcomes achieved
- Fallback path aligns with Section 2 Fallback Outcome
- Graceful exit aligns with Section 3 Disqualification Signals

---

## Badge Value Enums

| Field | Allowed Values |
|-------|---------------|
| Current Stance | `sponsor`, `supporter`, `neutral`, `non-supporter`, `adversary` |
| Role in Decision | `eb`, `champion`, `decision-maker`, `influencer`, `evaluator`, `end-user`, `procurement` |
| Role in Meeting | `lead`, `support`, `sme`, `executive-sponsor` |
| Objection Category | `status-quo`, `price/value`, `capability`, `risk/trust`, `authority/process` |
| Success Level | `ideal`, `acceptable`, `minimum` |
| Disqualifier | `yes`, `no` |

---

## Validation Rules

1. Frontmatter: all required fields present
2. All 7 sections present in correct order
3. Badge values match enum lists
4. At least 1 customer attendee defined
5. Attendee Insights present for each customer attendee
6. Target Meeting Outcomes has dual perspective (Customer + Our)
7. Success Criteria has all 3 tiers
8. Next Steps has all 3 paths (primary, fallback, exit)
