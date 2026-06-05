---
name: call-plan
description: >
  Generates structured Call Plan for AWS sales before customer meetings.
  Use whenever sales mentions meeting prep, call plan, customer visit,
  "拜访准备", "客户拜访", "明天见客户聊什么", "怎么跟CTO聊", "帮我想想怎么开场",
  or any hint of upcoming customer interaction — even without saying "call plan".
user_locked: true
---

# Call Plan Skill


---

## Execution Discipline

STOP. Read this entire skill file before executing.
This skill has mandatory references that must be loaded at specific stages — do NOT skip them.
Do NOT begin the Pre-Generation Dialogue until you understand all 10 sections.

---

## 1. Core Rules

### Rule 1: Always Build the Bigger Picture
After generating a Call Plan, check if an Engagement Plan exists for this customer. If not, auto-create one — every opportunity deserves a strategic wrapper. Never ask permission to create an EP.

### Rule 2: Load EP Context First
At the **start of every conversation** about a customer, load the EP for latest context (stakeholder stance, roadmap status, Execution Log). This ensures the Call Plan reflects all previous visit outcomes.

### Rule 3: People-Informed (Contact Profiling + CXO Personas)
For **every attendee**, invoke **Contact Profiling** for behavioral profile (the **how** layer — communication style, decision patterns, what motivates/triggers them).

For **executive attendees** (C-suite / VP), additionally load the matched **CXO Persona** for role-level priorities (the **what** layer — priorities, pain points, KPIs, common objections).

**Context-aware:** Select and emphasize dimensions most relevant to this meeting's objective and the current opportunity. Same persona, different opp = different focus. Supplement with web research (company news, LinkedIn, industry reports) to ground persona assumptions in reality.

If attendee roles are unknown, ask the rep before proceeding.

### Rule 4: Stage-Aware
Tag every Call Plan with the current AWS Sales Stage (sourced from EP / Opp Progression). Use the stage to determine focus areas and target outcomes. Warn when activities don't match the stage. Suggest advancement when evidence supports it — but stage advancement decisions are validated by Opp Progression, not Call Plan.

### Rule 5: Bidirectional Sync with EP
**CP → EP (post-generation):** After generating a Call Plan, compare attendees and objectives with EP's Next Milestone Detail. If there are differences:
1. **New attendees** → Add to EP Key Stakeholders; mark unknown fields as `[TBC]`
2. **Attendee changes** → Update EP Next Milestone Detail
3. **Objective changes** → Update the corresponding row in EP Engagement Roadmap
4. Add `[Updated: YYYY-MM-DD]` timestamp next to every changed field
5. Notify sales: "EP has been updated to reflect the Call Plan changes — please review."

**EP → CP (post-sales-review):** When sales reviews the CP and makes changes (e.g., adjusting attendees, objectives, or agenda), the agent proactively checks whether corresponding EP fields need sync updates. See references/call-plan.md AGENT GUIDANCE for field mapping. Principle: if CP changes → EP follows, maintaining consistency.

**EP 回写权限边界：**
- 事实性变更（新增 attendee、更新会议日期/地点）→ 直接写入 EP，Change Log 标注来源为 CP
- 判断性变更（调整 Win Strategy、修改 stakeholder 重要性、改变 engagement 顺序）→ 提示销售确认后再写入

### Rule 6: Data Provenance Labeling
Every piece of information must carry a provenance label so sales knows the confidence level.

| Label | Meaning | Sales Action |
|-------|---------|--------------|
| `[销售确认]` | Information directly provided or explicitly confirmed by sales | Use directly |
| `[AI推断]` | Information inferred by agent from context analysis | Recommend verification |
| `[网络搜索]` | Publicly available information obtained via web search | Check timeliness |

**Labeling granularity:** Each independently verifiable assertion.
**Display rules:** Only explicitly label `[销售确认]` and `[网络搜索]`; no label = `[AI推断]` (default).
**Upgrade mechanism:** After sales confirms → upgrade to `[销售确认]`.
**Language rule:** Labels follow the conversation language — use Chinese labels when conversing in Chinese, English labels (`[Sales Confirmed]`/`[AI Inferred]`/`[Web Search]`) when conversing in English.

### Rule 7: Never Hallucinate
Do not fabricate meeting objectives, attendee roles, customer stance, or expected outcomes. If information is unknown, mark as `[TBC]` and ask sales to provide it.

---

## 2. Input

Call Plan accepts input from two paths:

### Path A: Auto-triggered from Engagement Plan (preferred)
When EP's Next Milestone is confirmed, auto-pull:
- **Objective, Customer Attendees, Target Outcome, AWS Team** from Next Milestone Detail
- **Opportunity context** from EP Section 1 (Opportunity Snapshot + Win Strategy)
- **Stakeholder stance and priorities** from EP Key Stakeholders
- **Sales Stage** from EP (originally sourced from Opp Progression)

Agent enriches with CXO Personas + Contact Profiling + web research, then generates.

### Path B: Direct request from sales rep
When no EP exists or sales requests directly, collect minimum required inputs:

| # | Required Input | Why |
|---|---|---|
| 1 | **Customer name** | Identify account, check for existing EP |
| 2 | **Who are you meeting?** (names + titles) | Persona matching, stakeholder mapping |
| 3 | **Meeting objective** | Shape document focus |
| 4 | **Optional:** Opportunity / customer need context | What's the deal about? |

Then:
1. Confirm the **current sales stage** through interactive dialogue
2. Invoke **Account Context**, **Market Intelligence**, and **Competitive Intelligence** directly (Path B fallback — see Section 8)
3. Infer what you can from context, research publicly available information
4. Generate the Call Plan, marking gaps as `[待确认]`

> After generating via Path B, always check if an EP exists. If not, auto-create one (Rule 1).

---

## 3. Generation Workflow — Pre-Generation Dialogue

Call Plan generation is **NOT** a one-shot output. It follows a conversational preparation phase where agent and sales collaborate to confirm inputs, clarify unknowns, and answer each other's questions.

**Flow:**

```
EP Next Milestone confirmed / Sales requests CP
    ↓
Agent surfaces known context (from EP) + identifies gaps
    ↓
【Pre-Generation Dialogue】
    ├── Agent presents what's known: attendees, objectives, stage context
    ├── Agent raises items to confirm: date? final attendees? progress on previous follow-ups?
    ├── Sales may ask questions → Agent responds as information provider
    │   (competitive intel, communication style advice, similar cases, industry trends...)
    ├── Sales supplements/corrects → Agent adjusts understanding in real-time
    └── Key inputs confirmed
    ↓
Agent generates Call Plan
```

**Agent's dual role during dialogue:**

| Role | Description | Example |
|------|-------------|---------|
| **Information Collector** | Confirm key inputs needed to generate the CP | "When exactly is this meeting? Who's the final attendee list from customer side?" |
| **Information Provider** | Answer sales questions, provide decision-support information | "Based on CXO Persona, this CTO prefers data-driven discussions..." |

**Key principles:**

1. **Don't wait for all information before generating** — If key inputs (attendees, objectives) are confirmed, remaining gaps can be marked `[TBC]` in the initial draft
2. **Adjust based on sales questions at any time** — If new information surfaces during dialogue (competitor moves, internal customer changes), incorporate into CP considerations immediately
3. **Agent's answers are not the CP** — Research, advice, and analysis provided during dialogue help sales make decisions; the final structured output is the CP document
4. **Multiple dialogue rounds are normal** — Don't rush to generate; ensure key consensus is reached
5. **Dialogue convergence criteria** — Enter generation when any of:
   - All must-confirm items (list below) are confirmed
   - Sales explicitly says "enough / give me a first draft / good to go"
   - Agent asks one round with no substantive new info from sales
   - Agent has asked 2 rounds (max 3 questions each) with gaps remaining → generate initial draft, mark gaps as `[TBC]`

**Must-confirm items (Agent should not assume):**
- Meeting date / time / format (online / in-person)
- Final attendee list (customer side + AWS side)
- Core meeting objective (what sales wants to achieve)

**Can-infer items (Agent fills first, sales confirms):**
- Meeting objectives from customer perspective (based on EP context)
- Communication strategy (based on Contact Profiling + CXO Persona)
- Potential objections (based on stage + competitive landscape + history)
- Suggested agenda allocation

---

## 4. Stage-Aware Framework

Six stages: **Prospect → Qualified → Technical Validation → Business Validation → Committed → Closed/Launched**

Full stage definitions and exit criteria: [references/stage-mapping.md](references/stage-mapping.md)

**How stage shapes each Call Plan:**

| Stage | Focus Areas | Tone & Approach |
|---|---|---|
| **Prospect** | Implicit pain, Economic impact, Champion identification | Conversational. 70/30 rule (customer talks 70%). Earn a second meeting, not close anything. |
| **Qualified** | Pain validation, Metrics, Decision process, Champion engagement | Deep discovery. Fill info gaps aggressively. Listen more than present. |
| **Technical Validation** | Decision criteria, Paper process, Technical fit proof | Prove technical fit with evidence. Co-define POC success criteria. |
| **Business Validation** | Economic justification, Paper process, Decision timeline | Financial language. Quantify everything. Map full procurement process. |
| **Committed / Closed** | Metrics delivery, Success validation, Expansion signals | Shift to customer success. Address concerns before discussing expansion. |

**Use this mapping to:**
- Focus discovery questions on info gaps most critical for the current stage
- Align Target Outcomes with stage exit criteria
- Identify gaps blocking stage progression
- Suggest stage advancement when enough evidence is confirmed (final validation by Opp Progression, not Call Plan)

For every Call Plan, prepare **industry-relevant use cases** and **customer references** matched to the customer's industry.

---

## 5. Call Plan Template

⚠️ **Responsibility boundary between SKILL.md and references/call-plan.md:**
- **SKILL.md** (this file) = rules, workflows, dependencies, invocation logic — behavioral instructions for the agent
- **references/call-plan.md** = template structure, writing standards, methodology guidance — format and quality standards for generated content. The `<!-- AGENT GUIDANCE -->` comment blocks provide supplementary generation guidance for each template section.

Agent reads SKILL.md first for workflow and rules, then reads references for template structure and writing guidance. The two files do not duplicate the same definitions.

**REQUIRED: Load `references/call-plan.md` before generating any Call Plan.** This file defines the template structure and writing standards for all 7 sections. The `<!-- AGENT GUIDANCE -->` comment blocks provide supplementary generation guidance for each template section.

1. **Meeting Details** — Attendees, roles, logistics, opportunity context from EP
2. **Target Meeting Outcomes** — Dual-perspective (customer vs. ours) + stage progression target
3. **Success Criteria** — Observable, assessable criteria (verification standard for Section 2 outcomes)
4. **Information Exchange** — Questions to ask (stage-driven, gap-focused) + information to deliver
5. **Potential Objections & Responses** — Based on CXO Persona, Contact Profiling, and competitive context
6. **Meeting Agenda** — Time-allocated, purpose-driven, aligned to outcomes
7. **Potential Next Steps** — 2-3 concrete next steps, multi-path (if yes / if maybe / if not ready), aligned to stage exit criteria

---

## 6. Relationship with Other Skills

| Skill | Relationship | How to Access | If Unavailable |
|--------|-------------|---------------|----------------|
| **Engagement Plan** | Primary context source. CP pulls from EP's Next Milestone Detail + Opp Snapshot + Stakeholder stance. After generating, sync any attendee/objective changes back to EP (Rule 6). | Load `EP_{Customer}_{Opportunity}.html` from workspace. | Use sales rep's direct input (Path B). |
| **CXO Personas** | For exec attendees: role-level priorities, pain points, KPIs, objections (the **what** layer). Context-aware — select dimensions relevant to this meeting + stage. | Load from `cxo-personas/personas/` using INDEX.md Title Mapping. | General executive priorities based on role. Mark `[待确认]`. |
| **Contact Profiling** | For every attendee: behavioral profile — communication style, decision patterns, motivators (the **how** layer). | Load if exists; otherwise build through dialogue with sales. | Use sales rep's input. Mark `[待确认]`. |
| **Opportunity Progression** | Single source of truth for sales stage + exit criteria. Informs sections 2, 4, 5, 7. CP can suggest advancement but does NOT validate it. | Load opp record if it exists. | Confirm stage interactively with sales rep. |
| **Account Context** | Customer background, org chart, strategic priorities. Path A: obtained via EP Opp Snapshot. Path B (no EP): invoke directly for customer context to inform Section 1 (Attendee Insights) and Section 4 (tailored questions). | EP优先; Path B fallback → invoke account-context skill directly. | Web research + sales input. Mark `[待确认]`. |
| **Market Intelligence** | Industry trends, customer news, regulatory changes. Path A: obtained via EP context. Path B (no EP): invoke directly to populate Section 4 Information to Deliver (Market Context type). | EP优先; Path B fallback → invoke market-intelligence skill directly. | Web research for public info. Mark `[网络搜索]`. |
| **Competitive Intelligence** | Battlecard data, competitor positioning. Path A: obtained via EP Win Strategy. Path B (no EP): invoke directly to inform Section 5 (Price/Competition objections) and Section 4 (competitive context questions). | EP优先; Path B fallback → invoke competitive-intelligence skill directly. | General competitive awareness from web research. Mark `[待确认]`. |
| **Post-Meeting Report** | CP's Target Meeting Outcomes (Section 2) are auto-pulled into PMR's Outcome Assessment. CP's Next Steps are compared with actual outcomes in PMR. | N/A — PMR reads from CP. | N/A. |
| **Executive Briefing** | If meeting is an EBC or internal executive briefing, generate EB instead of Call Plan. | Check meeting type with sales rep. | N/A. |

---

## 7. Document Quality Standards

Before delivering, validate:
- [ ] All attendees identified with roles + relevant persona/profiling loaded
- [ ] Dual-perspective outcomes aligned to stage exit criteria
- [ ] Success criteria are observable and binary (not feeling-based)
- [ ] Questions serve Target Outcomes (not generic discovery)
- [ ] Objections sourced from persona + competitive context (not generic)
- [ ] Agenda time allocation reflects outcome priority
- [ ] Next steps are SMART (who, what, when, why, how) with multi-path options

---

## 8. Information Insufficient Fallback

1. **Never block.** Generate best-effort version with available information.
2. **Never hallucinate.** Mark gaps as `[TBC]` with actionable context — explain **why** it matters and **how** it would improve the document.
   - ❌ `[TBC] — please provide competitor info`
   - ✅ `[TBC] — Missing competitor info. If you can share the current vendor and contract expiry, I can produce a competitive analysis and differentiation strategy.`
3. **Max 3 questions at once.** Prioritize top 3; note the rest can be filled later.
4. **Guide with examples.** Provide ❌/✅ contrast when sales input is too vague.

---

## 9. Language & Tone

- **Professional but approachable** — not stiff, not casual
- **Action-oriented** — active voice, lead with verbs
- **Specific and quantified** — "Increase deployment frequency by 40%" not "Improve deployments"

**Bilingual:** Chinese input → Chinese output; English → English; mixed → match primary language. Section titles follow output language; table headers and AWS product names always in English.

**Avoid:** Filler phrases, vague recommendations, generic templates with unfilled placeholders.

---

## 10. Delivery & Quick Summary

### 交付流程

每次 Call Plan 生成后，按以下顺序交付：

```
Call Plan 生成完毕
    ↓
① Quick Summary（对话中直接发送，3-5 行）
    ↓
② 完整文档 PDF（必须每次输出）
    ↓
③ HTML 同时保存（中间产物，也存档）
    ↓
④ Word 按需（销售明确要求时生成）
```

### Quick Summary 格式

```
📋 Call Plan Ready: {Customer} × {Date}

👤 对象：{Attendee1 (Role)} + {Attendee2 (Role)}
🎯 目标：{核心会议目标，一句话}
⚠️ 关键风险：{最需要注意的 1 个 objection 或 risk}
💡 建议开场：{开场策略，一句话}

📄 完整文档已生成 → [附件]
```

---

## 11. Document Output & Storage

### File Naming Convention

| Format | Naming |
|--------|--------|
| PDF | `CP_{Customer}_{Date}_{MilestoneBrief}.pdf` |
| HTML | `CP_{Customer}_{Date}_{MilestoneBrief}.html` |
| Word | `CP_{Customer}_{Date}_{MilestoneBrief}.docx` |

Example: `CP_MinghuaHeavy_2026-05-15_Discovery-CTO.pdf`

MilestoneBrief = condensed version of the EP Roadmap milestone description (2-4 English words, kebab-case). CP and its corresponding PMR use the same `{Date}_{MilestoneBrief}` suffix for easy pairing.

### Storage Architecture

**First-time setup:** On first interaction with a sales rep, ask for local storage path:
> "Please tell me your preferred local file path (e.g., ~/Documents/AWS-Sales/)"

**Constraint: Files are stored on the sales rep's local device, NOT on Feishu Doc or other cloud document platforms.**

**Directory structure (organized by Customer → Opportunity):**

```
{sales_local_path}/
├── {Customer}/
│   ├── {Opportunity}/
│   │   ├── EP_{Customer}_{Opportunity}.pdf
│   │   ├── CP_{Customer}_{Date}_{MilestoneBrief}.pdf   ← Call Plan
│   │   ├── PMR_{Customer}_{Date}_{MilestoneBrief}.pdf
│   │   └── ...
│   └── _account/              ← Account-level shared materials (cross-Opp)
│       ├── org-chart.md
│       └── contacts/
```

**Key rules:**
- Call Plan is stored in the corresponding Opportunity folder (same level as EP)
- Each meeting produces a new CP file (not a living document)
- Agent locates current Opp via EP → Roadmap → Next Milestone
- Multi-Opp routing: 1 active opp → auto-associate; multiple → ask sales to confirm

See engagement-plan SKILL.md for the canonical directory structure specification.

---

*Call Plan Skill | Version: 3.5*
