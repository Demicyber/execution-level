---
name: post-meeting-report
description: >
  Post-meeting debrief — structures meeting outcomes, insights, action items, and customer follow-up emails.
  Use whenever sales finishes a meeting or visit and needs to capture what happened,
  "拜访复盘", "会议纪要", "会后总结", "刚见完客户", "开完会了", "今天拜访了",
  or provides a transcript, recording, or notes to structure — even if they just say "刚开完会".  
user_locked: true
---

# Post-Meeting Report Skill

## Execution Discipline

**STOP.** Read this entire file before producing any output.

This skill executes: Input → PMR Generation → EP Update → Referrals → Email Draft. No step may be skipped.

- §3 (PMR Template): **REQUIRED: Load `references/post-meeting-report.md`** before generating any PMR content — it contains the full template structure and agent guidance.

## 1. Input

The agent accepts any of the following:
- **Verbal debrief** — sales rep describes what happened in conversation
- **Written notes** — bullet points, free-form text, or structured notes
- **Meeting transcript** — auto-generated or manual
- **Audio recording** — if transcription is available

The agent structures whatever input it receives into the PMR template. If input is sparse, generate best-effort and ask targeted follow-up questions (max 3).

### Output Sequence

Every PMR run outputs in two stages:

1. **Quick Summary (immediate)** — deliver first, within 30 seconds:
   - Action Items (owner + deadline)
   - Key Findings (bullet list)
   
2. **Full PMR (follows)** — complete 7-section report + EP update + referrals + email draft

Do not wait for the full PMR to finish before delivering the Quick Summary.

---

## 2. Core Rules

### Rule 1: Close the Loop
After generating a PMR:
1. Update the Engagement Plan (incremental updates + timestamps + gap detection)
2. Provide Evidence Summary + Referrals to authoritative skills (see §7)
3. Carry insights to the next Call Plan

### Rule 2: Auto-Pull from Related Document
The PMR auto-reads from the **related document** to generate the Outcome Assessment:
- **Call Plan path:** Target Meeting Outcomes (CP Section 2)
- **Executive Briefing path:** Objectives + Success Definition (EB Section 3)

Sales provides the results; agent structures the assessment.


### Rule 3: Never Hallucinate
Do not fabricate meeting outcomes, stakeholder sentiments, or action items. PMR must reflect what actually happened. Mark unclear information as `[待确认]`.

### Rule 4: Data Provenance Labeling
Every piece of information must carry a provenance label so sales knows the confidence level.

| Label | Meaning | Sales Action |
|-------|---------|--------------| 
| `[Sales Confirmed]` | Information directly provided or explicitly confirmed by sales | Use directly |
| `[AI Inferred]` | Information inferred by the agent based on context analysis | Suggest verification |
| `[Web Search]` | Publicly available information obtained via web search | Check timeliness |

**Labeling granularity:** Each independently verifiable assertion.
**Display rule:** Only explicitly label `[Sales Confirmed]` and `[Web Search]`; unlabeled = `[AI Inferred]` (default).
**Upgrade mechanism:** After sales confirms → upgrade to `[Sales Confirmed]`.

---

## 3. PMR Template

**REQUIRED: Load [references/post-meeting-report.md](references/post-meeting-report.md)** before generating. The template has 4 core sections + 1 handoff:

1. **Outcome Assessment** — Auto-pulled objectives/criteria from related document + result (✅ Achieved / ⚠️ Partial / ❌ Not achieved) + stage progression result
2. **Meeting Insights** — Customer sentiment per attendee + key findings with source and implication + information gap check
3. **What Changed — EP Update** — Incremental changes by dimension (stakeholders, Win Strategy, competitive, risks, stage/timeline) + Agent Recommendation
4. **Next Steps — Planned vs Actual** — Comparison table + Action Items sorted by priority (High first), with owner, ETA, status
5. **Customer Recap Email** — Key points for sales review before sending (see §6)

---

## 4. EP Update Rules

When updating the EP from a PMR, **agent directly edits the EP file** and then asks sales to review:

1. **Key Stakeholders** — update Current Stance; update Profiling if new behavioral observations emerged
2. **Engagement Roadmap** — mark completed milestone as **Done**, promote next Planned to **Next ↓**, expand new Next Milestone Detail
3. **Execution Log** — add new entry at top (most recent first): Planned vs Actual, People Updates, Key Learnings, Plan Adjustment
4. **Estimate & Uncertainty** — re-forecast if timeline, call count, or risk profile changed
5. **Incremental updates only** — modify only changed fields; preserve existing content
6. **Timestamp annotations** — add `[Updated: YYYY-MM-DD]` next to every changed field
7. **Gap detection** — if a topic was discussed but no outcome captured, flag: "⚠️ [Topic] discussed but no outcome captured — please confirm."

After updating, always ask sales to review the EP changes.

---

## 5. Agent Recommendation & Referrals

After each PMR, provide:

**A. Evidence Summary (PMR's own authority):**
- What factual outcomes were achieved vs planned?
- What new information was uncovered?
- What risks or blockers emerged?

**B. Referrals to Authoritative Skills (PMR does NOT make these judgments itself):**

| Signal Detected | Refer To | Phrasing |
|---|---|---|
| Stage-relevant evidence (milestone achieved, key person engaged, technical validation passed) | → `opportunity-progression` | "本次会议获得了阶段相关证据，建议运行 OP 评估 stage 是否需要变化。" |
| New competitive intel surfaced | → `competitive-intelligence` | "发现新的竞争信息，建议刷新 CI 分析。" |
| 客户提到外部市场变化、行业事件、政策/监管信号 | → `market-intelligence` | "会议中提到了外部环境变化信号，建议运行 Market Intelligence 生成预警卡，评估对当前策略的影响。" |
| Strategy seems misaligned with outcomes | → `engagement-plan` (user decides) | "会议结果与当前策略有偏差，是否需要调整 EP？" |
| New person introduced (not yet profiled) | → `contact-profiling` | "新人物出现，建议建立 Contact Profile。" |

**⚠️ PMR MUST NOT:**
- Directly say "opportunity should advance to Stage X" (that's OP's authority)
- Unilaterally change EP Win Strategy (that's EP's authority)
- Score MEDDPICC elements (that's OP's authority)

**PMR CAN:**
- State factual observations ("客户明确表示了预算审批通过")
- Flag evidence ("这可能意味着 Economic Buyer 已确认")
- Recommend invoking another skill for judgment

---

## 6. Customer Recap Email

After completing the PMR, ask: "Would you like me to draft a customer recap email based on this report?"

If yes, the PMR agent drafts a complete email using the following guidelines:

**Content to include:**
- Thanks for the meeting
- Key discussion points and alignment (from Section 2 Key Findings)
- Agreed action items with owners and timelines (from Section 4)
- Proposed next steps

**Content to exclude:**
- Internal strategy or INTERNAL-marked content
- Pricing details (unless explicitly agreed to share)
- Competitive analysis
- MEDDPICC terminology
- Stakeholder sentiment assessments

**Email template:**

```
Subject: Follow-up: [Meeting Topic] — [Customer Name] × AWS [Date]

Hi [Name],

Thank you for taking the time to meet with us today. We appreciated the open conversation about [topic].

Here's a summary of what we discussed and aligned on:
- [Key point 1]
- [Key point 2]
- [Key point 3]

Agreed next steps:
- [Action item 1] — [Owner] by [Date]
- [Action item 2] — [Owner] by [Date]

We'll [proposed next step, e.g., "schedule a follow-up technical session for the week of XX"]. Please let us know if anything needs to be adjusted.

Looking forward to continuing the conversation.

Best regards,
[Your name]
```

Sales reviews and edits before sending same day. Customer-facing content only.

---



## 7. Delivery & Document Output

### 交付流程

每次 PMR 生成后，按以下顺序交付：

```
PMR 生成完毕
    ↓
① Quick Summary（对话中直接发送 — 见 §1 Output Sequence）
    ↓
② 完整文档 PDF（必须每次输出）
    ↓
③ HTML 同时保存（中间产物，也存档）
    ↓
④ Word 按需（销售明确要求时生成）
```

### Quick Summary 格式

```
📋 PMR Ready: {Customer} × {Date}

✅ Action Items:
• {Action1} — {Owner} by {Deadline}
• {Action2} — {Owner} by {Deadline}

💡 Key Findings:
• {Finding1}
• {Finding2}
• {Finding3}

📄 完整文档已生成 → [附件]
```

### File Naming Convention

| Format | Naming |
|--------|--------|
| PDF | `PMR_{Customer}_{Date}_{MilestoneBrief}.pdf` |
| HTML | `PMR_{Customer}_{Date}_{MilestoneBrief}.html` |
| Word | `PMR_{Customer}_{Date}_{MilestoneBrief}.docx` |

Example: `PMR_MinghuaHeavy_2026-05-15_Discovery-CTO.pdf`

MilestoneBrief = Condensed EP Roadmap milestone description (2-4 English words, kebab-case). PMR and its corresponding CP/EB share the same `{Date}_{MilestoneBrief}` suffix for easy pairing (pre-meeting plan ↔ post-meeting report).

### Storage Architecture

**First-time setup:** On first interaction with sales, ask for the local storage path.

**Constraint: Files are stored on the sales rep's local device, NOT in Feishu Docs or other cloud document platforms.**

**Directory structure (Customer → Opportunity as the core):**

```
{sales_local_path}/
├── {Customer}/
│   ├── {Opportunity}/
│   │   ├── EP_{Customer}_{Opportunity}.pdf
│   │   ├── CP_{Customer}_{Date}_{MilestoneBrief}.pdf
│   │   ├── PMR_{Customer}_{Date}_{MilestoneBrief}.pdf  ← PMR
│   │   └── ...
│   └── _account/              ← 客户级共享资料（跨 Opp）
│       ├── org-chart.md
│       └── contacts/
```

**Key rules:**
- PMR is stored in the corresponding Opportunity folder (same level as EP and CP)
- Each meeting produces a new PMR file (not a living document)
- Agent locates the Opp directory via the associated CP/EB file
- After generating, PMR auto-updates the EP in the same directory (Execution Log + Roadmap + Stakeholder stance)
- Multi-Opp resolution: 1 active opp → auto-associate; multiple → ask sales to confirm

See engagement-plan SKILL.md for the full directory structure specification (authoritative source).
