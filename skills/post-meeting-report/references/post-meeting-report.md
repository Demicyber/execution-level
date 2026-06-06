# Post-Meeting Report

## Table of Contents
- [Agent Guidance — Data Provenance](#agent-guidance--data-provenance) (in comment)
- [Global Agent Logic](#global-agent-logic) (in comment)
- [1. Outcome Assessment](#1-outcome-assessment)
- [2. Meeting Insights](#2-meeting-insights)
- [3. What Changed — EP Update](#3-what-changed--ep-update)
- [4. Next Steps — Planned vs Actual](#4-next-steps--planned-vs-actual)
- [5. Customer Recap Email](#5-customer-recap-email-handoff)

> **Purpose:** Captures meeting outcomes, extracts insights, and feeds learnings back to the Engagement Plan. AI agent generates the PMR based on sales debrief and Call Plan context.
>
> ✅ *After generating, agent always asks sales to review and confirm before writing back to EP.*



<!-- GLOBAL AGENT LOGIC:

## 定位
PMR 是 EP → Call Plan → 开会 → PMR → EP 闭环的最后一环。

关系链：
- Call Plan = 会前计划（"我们打算怎么聊"）
- PMR = 会后复盘（"实际发生了什么、跟计划有什么差异、EP 需要怎么调整"）

核心职责：
1. 对比：实际 vs 计划（Target Outcomes 达成了吗？）
2. 提取：会议中发现的新信息、变化、信号
3. 回写：把变化同步回 EP（不能只记录不更新）

## 数据源
| 来源 | 说明 |
|---|---|
| Call Plan 自动拉取 | Target Meeting Outcomes (Section 2), Information to Gather (Section 4), Planned Next Steps (Section 7) |
| 销售输入 | 会后口头 debrief、会议录音/笔记、销售观察和判断 |
| Agent 生成 | 基于以上两者对比分析，生成 assessment + 提取 key findings + 推荐 EP 更新 |

## 生成流程
1. 触发：会议结束后，销售提供 debrief（口头描述、笔记、或录音转写）
2. Agent 读取对应的 Call Plan（自动关联）
3. Agent 对比 planned vs actual，生成 PMR 全文初稿
4. 销售 review → confirm 或修改
5. Agent 将确认后的变更回写 EP（见 Section 3 回写规则）

## 回写 EP 规则（关键！）
PMR 不是独立文档 — 它的核心价值是触发 EP 更新。Agent 完成 PMR 后必须：
1. 根据 Section 3 "What Changed" 自动生成 EP 更新建议
2. 向销售展示："以下 EP 字段需要更新，确认吗？"
3. 销售确认后执行 EP 更新
4. 完成的 milestone 移入 EP Execution Log，下一个 Planned milestone 展开为新的 Next Milestone Detail

绝对不能只写 PMR 不更新 EP — 那样信息就断了。

## Call Plan 接口（路径 A：会议由 Call Plan 触发）
从 Call Plan 拉取做对比的字段：
- Section 2 Target Meeting Outcomes → PMR Section 1 逐项评估
- Section 4 Information to Gather → PMR Section 2 标注哪些搞清楚了、哪些还是 gap
- Section 7 Next Steps → PMR Section 4 对比 planned vs actual next steps

## Executive Briefing 接口（路径 B：会议由 EB 触发）
从 Executive Briefing 拉取做对比的字段：
- Section 3 Success Definition → PMR Section 1 逐项评估
- Section 3 Per-objective detail (objectives + talking points + asks) → PMR Section 2 评估每个目标的实际达成
- Section 3 Anticipated Concerns → PMR Section 2 对比预判 vs 实际出现的 concerns
- Section 3 Proposed Next Steps (3-tier: ideal / acceptable / minimum) → PMR Section 4 对比 planned vs actual next steps

路径判断规则：Agent 检查关联文档类型 — 如果是 Executive Briefing 则走路径 B，否则走路径 A。
-->

> **Related Document:** [Call Plan / Executive Briefing — link]  
> **Date:** YYYY-MM-DD  
> **Recorded by:**

---

## 1. Outcome Assessment

<!-- AGENT GUIDANCE:
定位：PMR 的核心 — 对比 Call Plan Section 2 (Target Meeting Outcomes) 的计划 vs 实际。

📥 数据源：Agent 自动从关联的 Call Plan Section 2 拉取 Target Meeting Outcomes → 结合销售 debrief 评估每项达成情况

评估标准：
- ✅ Achieved：客户做了我们期望的具体动作，有明确 evidence
- ⚠️ Partial：方向对但程度不够（如：同意了但没给时间、表示兴趣但没承诺）
- ❌ Not achieved：没有发生，或客户明确拒绝

Notes 必须包含 evidence — 不是主观感受，而是客户说了什么、做了什么。

Stage Progression 评估：
- 对照 Call Plan 的 Target Stage Progression
- 如果没达到 → 说明 gap 是什么，下次需要推进什么

质量标准：
- ❌ "会议很成功，客户很感兴趣"（主观，无 evidence）
- ❌ "Partial — 还需要再跟进"（模糊，不知道差在哪）
- ✅ "⚠️ Partial — CTO 确认了架构痛点存在，但表示需要内部跟 IT Director 对齐后才能承诺评审时间。Evidence: 他说'这个确实是问题，但我得先跟老李聊聊再定'"
-->

> *💡 Agent auto-pulls Target Meeting Outcomes from the related Call Plan and assesses each against actual results. Sales confirms the assessment.*

| # | Target Meeting Outcome | Result | Evidence & Notes |
|---|------|------|------|
| 1 | *{auto-pulled from Call Plan Section 2}* | ✅ / ⚠️ / ❌ | `{客户具体说了什么/做了什么}` |
| 2 | *{auto-pulled}* | ✅ / ⚠️ / ❌ | `{evidence}` |

**Fallback Outcome Assessment:** `{如果主目标未达成，Fallback Outcome 是否达成？}`

**Stage Progression:** ( `{current}` ) → ( `{target}` ) — ✅ Achieved / ❌ Not achieved — `{reason}`

---

## 2. Meeting Insights

<!-- AGENT GUIDANCE:
定位：从会议中提取有战略价值的新信息。不是会议纪要（不记录每句话），而是提取"改变我们认知或策略的信息"。

📥 数据源：销售 debrief + 会议笔记/录音 → Agent 提取并结构化

### Customer Sentiment
对比 Call Plan Section 1 Attendee Insights 中的 Current Stance：
- stance 变了吗？（Neutral → Supporter？Supporter → 退缩？）
- Evidence 必须是客户的具体言行，不是销售感觉

### Key Findings
筛选标准 — 只记录满足以下条件的信息：
1. 改变了我们对这个 opp 的认知（新信息）
2. 影响我们的策略或下一步（actionable）
3. 需要回写到 EP（会改变某个字段）

不记录：
- 已知信息的重复确认（除非之前存疑现在确认了）
- 跟这个 opp 无关的闲聊
- 没有 implication 的琐碎细节

### Information Gap Check
对照 Call Plan Section 4 (Information to Gather)：哪些问题得到了答案？哪些还是 gap？
- 搞清楚了 → 记录答案 + 写入 Key Findings（如果有战略价值）
- 没搞清楚 → 标注为 gap，带入下次 Call Plan

质量标准：
- ❌ 记录会议全程流水账
- ❌ "客户对我们的方案很感兴趣"（无 evidence，无 implication）
- ✅ "CFO 透露预算审批需要 CEO 签字（之前以为 CFO 就能定）→ 需要调整 EP 的 Decision Process，补充 CEO engagement 策略"
-->

> *💡 Agent extracts strategic insights from sales debrief. Focus on what's NEW and what CHANGES our understanding or strategy.*

### Customer Sentiment

| Attendee | Stance Before | Stance After | Evidence |
|----------|--------------|--------------|----------|
| `{name}` | `{from Call Plan: e.g., Neutral}` | `{e.g., Supporter}` | `{what they said/did that shows the shift}` |

### Key Findings

| # | Finding | Source | Implication for Strategy |
|---|---------|--------|------------------------|
| 1 | `{new information discovered}` | `{who said it / how we learned it}` | `{what this means for our strategy + which EP section to update}` |
| 2 | | | |

### Information Gap Check

| # | Question (from Call Plan) | Status | Answer / Notes |
|---|--------------------------|--------|----------------|
| 1 | *{auto-pulled from Call Plan Section 4}* | ✅ Answered / ❌ Still a gap | `{answer if obtained, or plan to get it next time}` |
| 2 | *{auto-pulled}* | ✅ / ❌ | |

---

## 3. What Changed — EP Update

<!-- AGENT GUIDANCE:
定位：这是 PMR 的"动作层" — 不只是记录变化，而是明确告诉 agent 怎么更新 EP。

📥 数据源：Agent 从 Section 1 (Outcome Assessment) + Section 2 (Meeting Insights) 自动提取需要回写 EP 的变更

回写规则：
1. 每条变更必须指向 EP 的具体字段/section
2. 变更类型标注：新增 / 更新 / 删除 / 确认（之前是假设，现在确认了）
3. Agent 生成完后向销售确认："以下 EP 更新确认吗？"
4. 销售确认后 agent 自动执行 EP 更新

常见回写维度：
- Stakeholder stance/relationships → EP Key Stakeholders
- Competitive intelligence → EP Opp Snapshot: Win Strategy
- Risk identified/resolved → EP Estimate & Contingency (Stakeholder Risk & Leverage / Milestone Risk)
- Timeline/urgency change → EP Engagement Roadmap + Estimate & Contingency
- Decision process clarification → EP Key Stakeholders (Role in This Deal) + Engagement Roadmap (审批节点)
- New stakeholder discovered → EP Key Stakeholders (新增)
- Stage progression → EP Opp Snapshot: Current Stage + Execution Log

⚡ 闭环检查：
- PMR 完成后，当前 milestone 移入 EP Execution Log
- 下一个 Planned milestone 自动展开为新的 Next Milestone Detail
- 如果 outcome 未达成 → 评估是否需要重新规划（调整 roadmap、加新 milestone、或重复当前 milestone）

质量标准：
- ❌ "客户态度变好了"（模糊，EP 里改什么？）
- ❌ 只列 dimension 不说具体改什么
- ✅ "Key Stakeholders: 王总 stance 从 Neutral → Supporter（evidence: 主动提出帮我们安排 CTO 会议）— 更新 EP Key Stakeholders 表"
-->

> *💡 Agent auto-extracts EP updates from Sections 1 & 2. Each change must point to a specific EP field. Sales confirms before agent executes the update.*

| # | EP Section to Update | Change Type | What to Write |
|---|---------------------|-------------|---------------|
| 1 | `{e.g., Key Stakeholders}` | `{Update}` | `{e.g., "王总: Neutral → Supporter. Evidence: 主动提出帮安排 CTO 会议"}` |
| 2 | `{e.g., Win Strategy}` | `{新增}` | `{e.g., "客户透露在评估阿里云，但对其 AI 能力不满意"}` |
| 3 | `{e.g., Roadmap}` | `{Update}` | `{e.g., "客户 H2 才有预算 — 原计划 Q2 推进需延后"}` |

**Execution Log Update:** `{当前 milestone 状态 → Done/Partial/Repeat，原因}`

### Agent Recommendation

> *💡 Based on meeting outcomes and EP changes:*
> - *What stage-relevant evidence emerged? (If significant, recommend invoking `opportunity-progression` for stage evaluation.)*
> - *Does the current strategy need adjustment?*
> - *What should the next milestone/interaction focus on?*
>
> *⚠️ If sales asks whether the opportunity should advance, invoke `opportunity-progression` — do NOT answer directly.*

---

## 4. Next Steps — Planned vs Actual

<!-- AGENT GUIDANCE:
定位：对比 Call Plan Section 7 (Planned Next Steps) vs 会议中实际约定的 next steps。

📥 数据源：
- Planned → 自动从 Call Plan Section 7 拉取
- Actual → 从销售 debrief 提取会议中实际约定的动作

为什么要对比：
- 如果 actual = planned → 执行力强，按计划推进
- 如果 actual ≠ planned → 分析为什么偏离，是好事（超预期）还是坏事（没达到）
- 如果客户没有给出任何 commitment → ⚠️ 红旗信号，需要在 Agent Recommendation 里标注

Action Items 提取规则：
- 每条必须有具体 Owner（人名 + AWS/Customer 标注）
- 每条必须有 ETA
- 排序按优先级（High/Medium/Low）
- Agent 主动检查：是否有 action item 没有 owner？是否有 owner 但没有 deadline？→ 标注并提醒销售补充
-->

> *💡 Agent compares planned next steps (from Call Plan) with what was actually agreed in the meeting.*

### Comparison

| # | Planned (from Call Plan) | Actual (agreed in meeting) | Delta |
|---|--------------------------|---------------------------|-------|
| 1 | *{auto-pulled from Call Plan Section 7}* | `{what was actually agreed}` | `{on track / exceeded / fell short — why}` |
| 2 | *{auto-pulled}* | `{actual}` | `{delta}` |

### Action Items

| # | Priority | Action Item | Owner | ETA | Status |
|---|----------|------------|-------|-----|--------|
| 1 | High | `{specific action}` | `{name (AWS/Customer)}` | `{date}` | Open |
| 2 | High | `{specific action}` | `{name (AWS/Customer)}` | `{date}` | Open |
| 3 | Medium | `{specific action}` | `{name (AWS/Customer)}` | `{date}` | Open |

---

## 5. Customer Recap Email (Handoff)

> *💡 After completing the PMR, prompt the user: "Would you like me to draft a customer recap email?" If yes, use key discussion points, agreed action items, and proposed next steps to draft.*

---

*Post-Meeting Report Template | Version: 2.1*
