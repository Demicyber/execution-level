# Call Plan — Template

<!-- TOC (Agent Navigation) -->
<!-- 1. Meeting Details — line 56 -->
<!-- 2. Target Meeting Outcomes — line 148 -->
<!-- 3. Success Criteria — line 208 -->
<!-- 4. Information Exchange — line 273 -->
<!-- 5. Potential Objections & Responses — line 372 -->
<!-- 6. Meeting Agenda — line 446 -->
<!-- 7. Potential Next Steps — line 510 -->
<!-- GLOBAL AGENT LOGIC — line 32 -->
<!-- END TOC -->

> **Purpose:** Prepares AWS sales team members before external customer meetings. AI agent generates the Call Plan based on sales input, Engagement Plan context, and the current sales stage.
>
> ✅ *After generating, agent always asks sales to review and revise as needed.*

<!-- AGENT GUIDANCE — Data Provenance Labeling（信息溯源标注）

所有生成的内容必须标注信息来源，让销售清楚每条信息的置信度。

三个标签：
- [销售确认] — 销售直接提供或明确确认的信息，可直接使用
- [AI推断] — Agent 根据上下文分析推断的信息，建议核实（默认，不标时即为此类）
- [网络搜索] — 通过网络搜索获取的公开信息，注意时效

标注粒度：每条独立可判断真伪的断言。
显示规则：只显式标出 [销售确认] 和 [网络搜索]，无标注 = AI推断。
升级机制：销售确认后 [AI推断] → [销售确认]。
-->

<!-- GLOBAL AGENT LOGIC:

## 双向同步字段映射（Rule 6 详细版）

| Call Plan 变更 | 检查 EP 哪里 |
|---|---|
| 修改了 attendee stance/info | → EP Key Stakeholders |
| 加了新 objection | → EP Win Strategy / Stakeholder Risk |
| 改了 target outcome | → EP Next Milestone Detail |
| 改了 next steps | → EP Roadmap / Timeline |
| 发现新 stakeholder | → EP Key Stakeholders（新增） |
| 改了 success criteria | → EP Next Milestone exit criteria |

Agent 行为：变更检测后，向销售提示 "EP 这几个地方也需要同步更新，确认吗？" — 销售确认后执行更新。

## PMR 接口
以下字段会被 PMR 拉取做会后对比评估：
- Target Meeting Outcomes → PMR 对比实际 outcome
- Information to Gather → PMR 标注哪些搞清楚了、哪些还是 gap
- Next Steps → PMR 对比实际约定的 next steps
-->

---

## 1. Meeting Details

<!-- AGENT GUIDANCE:
数据来源：
- Path A（从 EP 触发）：自动从 EP Next Milestone Detail 拉取大部分信息
- Path B（销售直接请求）：向销售收集，确认后填入

📥 数据源标注：
- Opportunity Name / Current Stage → EP 自动拉取
- Date / Time / Location / Duration / Format → 销售提供（可能 [待确认]）
- Customer Attendees → EP Key Stakeholders 自动拉取，销售确认/补充
- Attendee Insights → Agent 从 EP Key Stakeholders + CXO Personas + Contact Profiling 生成，销售确认
- AWS Attendees → 销售提供

Date/Time/Location 如果未确认 → 标注 [待确认]，不要编造
Decision Role 如果第一次见面不清楚 → 标注 [待确认]，同时在 Section 4 加一个 discovery question 去搞清楚

Attendee Insights 写法标准：
从 EP Key Stakeholders 浓缩为"会议可执行版本"— 30秒内扫完就知道怎么跟这个人说话。

公式：每人一张"Stakeholder Card"，包含：
- Focus & Priorities → 最相关的1-2个 pain/KPI（不是 dump 整个 CXO Persona）
- Communication Approach → 沟通风格 + 决策模式 + 怎么跟他交流最有效
- Current Stance → Holden 5级（与 EP 一致）+ 简短 evidence
- Our Goal → 这次会议我们需要他做什么具体动作

质量标准（来自 Jeb Blount, Sales EQ）：
- 每个维度都要 actionable — 看完就知道"怎么办"
- Focus 只挑跟本次会议目标相关的点，不是全面综述
- Communication Approach 要具体到行为指导："先给数据再讲故事"而不是"analytical type"
- Our Goal 必须是可验证的动作（跟 Section 2 Target Meeting Outcomes 一致）
- 如果某人是新面孔/信息不足 → 标注 [待确认]，Section 4 加 discovery question

Current Stance 术语（统一用 Holden Power Base Selling 5级）：
Sponsor → Supporter → Neutral → Non-Supporter → Adversary

- ❌ "Supportive"（单词，无上下文）
- ❌ "Analytical type, needs data"（标签式，不够 actionable）
- ✅ "工程师出身，数据驱动 — 带 benchmark 和参考架构开场，不要从 PPT 开始。偏好30分钟 deep dive。入职8个月需要可见成果建立信任。通过他的首席工程师 Sarah 切入最有效。"
-->

> *💡 Sales provides: date, customer, attendees. Agent pulls opportunity context from Engagement Plan and fills the rest. Date/time/location may not be confirmed yet — mark as `[待确认]` if unknown.*

| Field | Value |
|---|---|
| **Date & Time** | `{date}` `{time}` `{timezone}` |
| **Duration** | `{duration}` |
| **Format** | `{In-person / Virtual / Hybrid}` |
| **Location / Link** | `{location or meeting link}` |
| **Opportunity Name** | `{auto from Engagement Plan}` |
| **Current Sales Stage** | `{Prospect / Qualified / Technical Validation / Business Validation / Committed}` |

### Customer Attendees

| Name | Title | Role in Decision |
|---|---|---|
| `{name}` | `{title}` | `{EB / Champion / Decision Maker / Influencer / Evaluator / End User}` |

### Attendee Insights

**{Name}** — {Title}
- **Focus & Priorities:** `{e.g., "董事会要求Q4前降低云支出20%，她的团队上季度被点名成本超支。单位经济模型是核心关注，迁移速度是次要。"}`
- **Communication Approach:** `{e.g., "工程师出身的高管，数据驱动 — 带 benchmark 和参考架构开场，不要 PPT。偏好30分钟 deep dive 而非高管概述。通过首席工程师 Sarah 建立信任最有效。"}`
- **Current Stance:** `{e.g., "Supporter — 在 Well-Architected Review 后对30%成本优化潜力表现出浓厚兴趣，主动索要了详细报告，但尚未在内部公开为我们站台。"}` 
- **Our Goal:** `{e.g., "让他确认现有架构无法支撑明年增长目标，并同意安排一次专门的架构评审会议。"}`

*Repeat for each customer attendee.*

### AWS Attendees

<!-- AGENT GUIDANCE (AWS Team):
📥 数据源：销售提供，Agent 可从 EP AWS Team 字段建议

角色分配逻辑：
- Lead：主导会议节奏，做开场/收尾，管理时间。通常是 AM (Account Manager)
- Support：辅助 Lead，负责记录关键信息，观察客户反应。通常是 co-sell partner 或 junior AM
- SME (Subject Matter Expert)：回答技术深度问题，做 demo/architecture 讨论。通常是 SA (Solutions Architect)
- Executive Sponsor：高管背书，只在关键会议出现（EB 对 EB）。通常是 Sales Director/VP

分工原则：
- 不要超过 3 人参加客户会议（除非客户方也多人）— 人多显得 pushy
- 每个人必须有明确 purpose，不能"来听听"
- 会前内部对齐：谁问什么问题、谁回答什么类型的问题、谁负责 close next step
- Lead 负责最终 confirm next step — 不要多人同时试图 close
-->

| Name | Title | Role in Meeting |
|---|---|---|
| `{name}` | `{title}` | `{Lead / Support / SME / Executive Sponsor}` |

---

## 2. Target Meeting Outcomes

<!-- AGENT GUIDANCE:
定位：这是整个 Call Plan 的"锚点" — 所有后续 section（成功标准、问题设计、议程安排）都围绕这个目标展开。

📥 数据源：Agent 从 EP Next Milestone Detail 的 Target Outcome 自动生成初稿 → 销售确认/修改
（注意：Call Plan 的 outcome 要比 EP 更具体 — EP 是方向，这里是本次会议的可验证动作）

写法公式 — "Mutual Advance" Formula（出处：Force Management, Command of the Message）：
"By the end of this meeting, [customer action] + [seller action] that moves toward [shared business objective]"

Sandler's PONT Test（出处：Sandler Training）— 每个 outcome 必须通过：
- P (Purpose): 为什么见面？（双方都有理由）
- O (Outcome): 结束时会发生什么？（决策或具体下一步）
- N (Next step): 什么是"advance"？（不只是"继续聊"）
- T (Time): 什么时候？（有时间约束的承诺）

双视角写法（出处：Gartner Buyer Enablement Research, 2019-2023）：
- Customer 视角回答："这次会帮我推进采购决策吗？"
- Seller 视角回答："这次会产生一个可验证的 advance 吗？"

公式：
Customer: "[客户] 将获得 [具体 insight/clarity/validation]，帮助他们 [做出决策/建立内部共识/降低风险]"
Seller: "[我们] 将获得 [具体承诺/信息/access]，推进 [deal milestone]"

质量标准：
- 主目标1个 + 备选目标1个（Sandler：如果主目标达不到，最低可接受的 advance 是什么？）
- Outcome 应该可以在会议开始时大声念给客户听（Sandler's verbal confirmability test）
- 必须包含客户的具体动作，不只是我们做什么

- ❌ "Present our solution"（seller-centric，activity-based）
- ❌ "Learn about their needs"（vague，no commitment）
- ❌ "Build rapport"（unmeasurable）
- ❌ "Demo the product"（activity, not outcome）
- ✅ "客户确认3个优先用例并授权我们访问他们的 sandbox 环境进行初步技术评估"
- ✅ "客户分享当前工作流瓶颈的具体数据，并同意下周二与技术团队做一次 deep-dive"
- ✅ "客户验证我们的方案解决了他们 top 2 痛点，并识别出参与 business case review 的内部 stakeholders"

Target Stage Progression：
- 基于当前 stage 的 exit criteria（参考 stage-mapping.md）判断
- 不是每次会议都能推进 stage — 如果距离 exit criteria 还远，可以写"保持当前 stage，推进以下关键 gap"
- Agent 主动对照 exit criteria 建议：这次会议如果达到 outcome，是否满足推进条件？

Challenger 视角（出处：Challenger Sale, CEB/Gartner）：
最好的 outcome 包含一个"reframe moment" — 客户应该带着一个改变了的认知离开，不只是信息交换。
-->

> *💡 Agent drafts based on current sales stage and EP roadmap. Sales reviews and adjusts. The user's stated meeting objective takes priority.*

| # | Customer Perspective | Our Perspective |
|---|---|---|
| 1 | `{e.g., "获得对当前架构瓶颈的专业评估和量化数据，帮助内部建立升级的紧迫性共识。"}` | `{e.g., "确认 CTO 认可现有架构无法支撑增长目标，并获得安排架构评审会议的明确承诺。"}` |
| 2 | `{e.g., "了解同行业企业的迁移实践和可预期的 ROI 范围，为内部 business case 提供参考。"}` | `{e.g., "识别出内部 business case 的审批流程和关键决策人，确定下次会议的参与者名单。"}` |

**Target Stage Progression:** ( `{current stage}` ) → ( `{target stage or "remain, close gap X"}` )

**Fallback Outcome:** `{e.g., "如果客户未准备好承诺架构评审，最低可接受的 advance 是：确认2-3个具体痛点 + 同意再安排一次30分钟的 follow-up 讨论。"}`

---

## 3. Success Criteria

<!-- AGENT GUIDANCE:
定位：怎么判断会议是否成功？这些标准是 Section 2 Target Meeting Outcomes 的验证工具，帮助销售在会中实时判断目标是否达成。

📥 数据源：Agent 基于 Target Outcomes + EP stage exit criteria (stage-mapping.md) 自动生成 → 销售确认

⚡ 对齐 Section 2：Success Criteria 是 Target Meeting Outcomes 的验证标准 — 每条 criteria 必须能直接追溯到 Section 2 的某个 outcome。如果一条 criteria 跟 Section 2 目标无关 → 删除。

写法公式 — "Evidence-Based Criteria"（出处：Force Management, Command of the Message）：
"I will know this meeting succeeded when I [see/hear/receive] [specific observable evidence]"

三种可观察 evidence 类型：
1. 语言信号（Verbal）：
   - 客户用回你介绍的术语/框架
   - 客户主动说"我们需要..."（而不是你说他们需要）
   - 客户主动提到应该让其他人参与
   - 客户问"这个对我们怎么 work？"（future-pacing）

2. 行为信号（Behavioral）：
   - 客户同意具体的下一步 + 给出时间
   - 客户分享内部文档/数据/access
   - 客户当场介绍你给其他 stakeholder（或安排引荐）
   - 客户在会中就把下次会议时间定了

3. 信息信号（Information）：
   - 你搞清楚了决策流程和时间线
   - 你识别出了真正的 EB（不只是 champion）
   - 客户确认了预算范围或资金渠道
   - 客户透露了在评估的其他方案

分层标准（最佳实践）：
- IDEAL（Home Run）：全部主目标达成 + 意外收获
- ACCEPTABLE（Base Hit）：核心目标达成，deal 在推进
- MINIMUM（Walk）：拿到足够信息判断 opp 是否 qualified + 保持了对话窗口
- DISQUALIFICATION SIGNAL：什么情况下说明这个 opp 不值得继续？（这也是重要信息！）

质量验证 — "Would a Manager Accept This?" Test：
- Specific：不是"went well"而是"客户确认了Q3预算存在"
- Binary：是/否可判断，不是主观感受
- Progressive：每个标准都把你推向 deal milestone 更近一步
- Customer-evidenced：基于客户做了什么，不是你觉得他怎么想

常见错误：
- ❌ "They seemed excited"（feeling-based，不可验证）
- ❌ "I asked all my questions"（input-focused，不是 output-focused）
- ❌ 没有定义什么叫"失败"（no disqualification criteria）
- ❌ 会后回头重写标准来匹配实际结果（retrospective rationalization）
- ✅ "客户确认 Q3 有专项预算，金额在 $X-Y 范围，审批需要 VP 签字"
- ✅ "客户同意在两周内安排 CTO 参加技术 deep-dive，并当场确认了日期"
- ✅ "客户分享了内部评估标准文档（或口头描述了3个以上评估维度）"
-->

> *💡 Agent drafts dual-perspective criteria. These are verification standards for Section 2 outcomes — they help sales assess in real-time whether objectives are being met. Criteria must be observable and assessable.*

| Level | Customer Would Consider Successful If… | We Would Consider Successful If… |
|---|---|---|
| **Ideal** | `{e.g., "获得了清晰的迁移路线图和可信的 ROI 预估，足以向 CFO 提交 business case。"}` | `{e.g., "CTO 当场确认架构方案并授权 POC，同时介绍我们给 CFO 安排预算讨论。"}` |
| **Acceptable** | `{e.g., "对 AWS 方案的技术适配性建立了信心，明确了下一步评估路径。"}` | `{e.g., "确认2-3个核心痛点与我们方案匹配，获得 follow-up 技术 deep-dive 的承诺和时间。"}` |
| **Minimum** | `{e.g., "理解了 AWS 在这个领域的能力范围，值得继续对话。"}` | `{e.g., "拿到足够信息判断 opp 是否 qualified（预算、时间线、竞争态势），保持对话窗口。"}` |

**Disqualification Signals:** `{e.g., "如果客户明确表示已选定其他供应商且合同已签署，或项目已被高管层无限期搁置，则标记为 disqualified。"}`

---

## 4. Information Exchange

<!-- AGENT GUIDANCE:
定位：会议中的"给与取" — 不只是提问题（gather），还要准备输出什么给客户（deliver）。

📥 数据源：
- Questions → Agent 基于 EP 当前信息 gaps + stage exit criteria + Stakeholder Risk 自动生成，销售补充
- Deliver items → Agent 从 EP Win Strategy + Solutions Search + 行业知识生成，销售确认

⚡ 对齐 Section 2：所有问题和分享内容都必须服务于 Target Meeting Outcomes — 问这个问题是为了推进哪个 outcome？分享这个信息是为了帮客户达成哪个目标？如果关联不上 → 删除或降优先级。

核心原则（出处：Corporate Visions Research）：
Buyers rate meetings as valuable when they LEARN something new, not when they're interrogated.
比例建议：60% 给 insight / 40% 收集信息 — 不要变成审讯。

### A. Discovery Questions — 超越通用框架式提问

SPIN Selling 语境层叠法（出处：Neil Rackham, SPIN Selling, 1988）：
关键 insight：提问的顺序比单个问题重要。

Layer 1 — SITUATION（确认外部研究无法获得的事实）：
  公式："I noticed [research finding]. Help me understand [specific gap]..."
Layer 2 — PROBLEM（让不满浮出水面）：
  公式："How does [situation fact] affect [their likely goal]?"
Layer 3 — IMPLICATION（放大痛点影响）：
  公式："When [problem] happens, what's the impact on [broader business metric]?"
Layer 4 — NEED-PAYOFF（让客户自己说出价值）：
  公式："If you could [solve problem], what would that mean for [their KPI]?"

Tailored vs Generic Questions — "Research-Gap" Method：
公式："Based on [specific thing I know about their situation], I'm curious about [specific thing I don't know that matters]"

- ❌ "What are your biggest challenges?"（太泛，任何公司都能问）
- ❌ "Who makes the final decision?"（太直接，显得没做功课）
- ❌ "What's your timeline?"（generic，没有上下文）
- ✅ "我看到贵司上季度扩展了3个新区域 — 你们现有的 onboarding 流程在这个规模下撑得住吗？"
- ✅ "你们上次实施 SAP 时，审批流程是怎么走的？这次这类投资是否走类似通道？"
- ✅ "你们 Q3 财报提到了数字化转型目标 — 这个项目是那个 initiative 的一部分，还是走独立预算？"

Hypothesis-Led Discovery（出处：Challenger Sale, CEB/Gartner）：
不是漫无目的的开放问题，而是带着假设去验证：
公式："Many [industry] companies we work with find that [specific insight]. Does that resonate, or is your situation different?"
- 更尊重买方时间
- 展示专业度
- 自然引导到你的差异化

每个问题必须标注：Target Attendee（问谁）+ Purpose（为什么问 + 答案怎么用）

### B. Information to DELIVER — "Give-to-Get" Strategy

四种类型的价值输出（不能只问不给）：

1. TEACHING MOMENT（Challenger methodology）：
   "什么反直觉的 insight 可以改变他们的认知？"
   - 必须跟他们的情况相关
   - 应该制造"constructive tension"
   - 自然引向你的差异化

2. PROOF POINT（relevant social proof）：
   "什么类似客户的故事可以证明 [specific outcome]？"
   - 同行业/同规模/同挑战
   - 量化结果
   - 60秒版本准备好

3. MARKET CONTEXT（Gartner Buyer Enablement）：
   "关于他们的市场/竞品，我知道什么是他们可能不知道的？"
   - 行业 benchmark
   - 趋势数据
   - 即将来临的法规/合规变化

4. PROCESS INSIGHT（降低采购复杂度）：
   "关于怎么成功购买/实施这类方案，我能分享什么？"
   - 其他客户踩过的坑
   - 常见决策标准框架
   - Implementation best practices

Gartner Buyer Enablement Data：提升成交概率的 #1 因素是帮助客户 do their buying job — 建立内部共识、justify 投资、降低感知风险。
-->

> *💡 Agent auto-selects discovery questions based on current sales stage and known information gaps. Questions and delivery items must be tailored to this specific meeting — not generic.*

### Information to Gather

| # | Question | Target Attendee | Purpose |
|---|---|---|---|
| 1 | `{e.g., "贵司去年批准 SAP 迁移项目时，审批流程是怎样的？这次云基础设施的投资决策是否走类似通道？"}` | `{CFO}` | `{搞清楚 paper process，确定还需要 engage 哪些人}` |
| 2 | `{e.g., "您提到数据驻留合规是核心顾虑 — 如果我们能在本地 region 提供完整数据隔离，这是否解决安全团队的主要担忧？还是还有其他因素？"}` | `{CISO}` | `{验证是否是真 blocker 还是可解决的顾虑}` |
| 3 | `{e.g., "你们目前在评估哪些其他方案？评估标准里排在前三的是什么？"}` | `{IT Director}` | `{了解竞争态势和 decision criteria}` |

### Information to Deliver

| # | What to Share | Format | Purpose |
|---|---|---|---|
| 1 | `{e.g., "同行业零售企业迁移后实现的30% TCO 下降数据（匿名化）"}` | `{Data point + 1-page summary}` | `{Teaching moment：改变他对迁移 ROI 的认知}` |
| 2 | `{e.g., "某零售客户400+工作负载迁移的时间线和关键决策节点"}` | `{Case study (60-sec verbal version ready)}` | `{降低'迁移太复杂'的风险感知，提供可参考的路径}` |
| 3 | `{e.g., "Gartner 关于零售行业云采购的最新报告摘要"}` | `{Market insight}` | `{帮助他在内部建立 urgency，支持他 justify 投资}` |

---

## 5. Potential Objections & Responses

<!-- AGENT GUIDANCE:
定位：提前准备异议处理 — 不是等客户提出再想，而是提前 rehearse。

📥 数据源：Agent 基于 Call Plan 前序 section 的完整上下文（参会人、会议目标、要讨论的内容、已知信息）+ EP 相关分析正常生成异议 → 销售补充已知的具体顾虑

⚡ 对齐 Section 2：只准备会阻碍 Target Meeting Outcomes 达成的异议 — 如果一个 objection 跟本次会议目标无关（可能是未来阶段的问题），不放在这里。

⚡ CXO Personas 校验（生成后 double check）：
- 产出完成后，读取每位 attendee 对应的 CXO Persona Section 8 (Buying Dynamics)
- 检查是否遗漏了该角色的核心 objection 类型（如 CEO 的 4 大 objections：Peer Proof / CFO-Board Narrative / Risk-Governance / Why Now Why You）
- 如果有遗漏 → 补充；如果已覆盖 → 确认 Response 是否回答了 "What they're really asking"
- 用 archetype weighting 校验优先级排序是否合理

异议分类框架（综合 Sandler, Challenger, Corporate Visions）：

5 大异议类型：
1. STATUS QUO / INERTIA："我们现在的流程挺好的"/"不是当前优先级"
   → 根因：no compelling event / pain 未被充分 articulate
2. PRICE / VALUE："太贵了"/"ROI 说不清楚"/"竞品更便宜"
   → 根因：未连接到 business outcome / 在跟错层级的人谈
3. CAPABILITY / FIT："你们能做 X 吗？"/"我们需要 Y（你们没有的）"
   → 根因：可能是真 gap，也可能是竞争对手"教"出来的 criteria
4. RISK / TRUST："我们以前被坑过"/"你们太小/太新"
   → 根因：需要 social proof + risk mitigation
5. AUTHORITY / PROCESS："我需要跟老板确认"/"我们有正式采购流程"
   → 根因：可能会议里不是对的人

Response 写法标准 — "Acknowledge-Reframe-Advance"（出处：Challenger Sale + Sandler）：

```
ACKNOWLEDGE: "这个顾虑很合理，让我解释一下为什么值得再看看…"（1句，不要 dismiss）
CLARIFY: [一个问题去理解 objection 背后的真正关切]
REFRAME: [一个 insight 或数据改变他的认知]
EVIDENCE: [Proof point — 客户故事、数据、demo]
ADVANCE: [具体的下一步动作来测试 objection 是否被化解]
FALLBACK: [如果 reframe 不 work，Plan B 是什么？]
```

Proactive Defusing — "Trap-Setting"（出处：Force Management）：
不是等客户提出，主动先提然后化解：
"在您这个位置的客户通常会关心 [objection]. 我们的经验是… [化解]. 这也是您的顾虑吗？"
→ 展示自信，防止 objection 变成 gotcha

Status Quo Disruption — 最危险的异议是"不做"（出处：Corporate Visions）：
1. Unconsidered Need："大部分企业没意识到 [不行动的隐性成本]"
2. Contrast："如果什么都不做会发生什么 vs 如果行动"
3. Safety："以及我们怎么降低转变过程中的风险"

写法质量标准：
- Response 必须是 2-3 句 + 一个反问（不是独白）
- 标注：Is this a disqualifier?（Yes/No）— 有些 objection 如果确认为真就该 walk away
- 每个 response 都要 end with a question back（dialogue, not monologue）
- Sandler 原则："The person who cares least wins" — 不要争论

- ❌ 准备长篇独白来"说服"客户
- ❌ 把所有 objection 都当真（很多是反射性的，先探查再解决）
- ❌ 用更多 feature 回应关切（应该用 business impact 回应）
- ❌ 没准备应对"让我想想再说"（最常见也最致命的 non-objection）
- ✅ 2-3 句 response + 一个验证问题
- ✅ 标注根因类型 + 是否可能是 disqualifier
- ✅ 包含 fallback plan（如果初始 reframe 无效）
-->

> *💡 Agent drafts based on Call Plan context (attendees, meeting objectives, discussion topics) and EP analysis. Then double-checks against CXO Persona Section 8 (Buying Dynamics) for completeness. Sales reviews and adds.*

| # | Anticipated Objection | Category | Response | Fallback | Disqualifier? |
|---|---|---|---|---|---|
| 1 | `{e.g., "我们现在的多云架构运行得还可以，没有迫切需求改变。"}` | `{Status Quo}` | `{e.g., "完全理解 — 如果现在能 work 当然没必要为了变而变。不过我好奇，您提到的 Q4 降本20% 目标，在不调整架构的情况下有什么方案在考虑？（Pause）我们看到同等规模的零售企业在优化前，通常在多云管理层面有15-25%的隐性成本是 dashboard 上看不到的。如果我给您做一个快速 assessment 来验证这个数字，对您有帮助吗？"}` | `{如果客户坚持不需要：ask "什么条件下您会重新评估？" — 确认 trigger event，planted seed}` | `{No — status quo inertia, not a hard blocker}` |
| 2 | `{e.g., "Azure 给我们的 EA 价格非常有竞争力，你们怎么比？"}` | `{Price/Competition}` | `{e.g., "价格肯定是重要考量。不过我想先确认一件事 — 您比较的是单纯的单位价格，还是包含了运维人力和迁移风险的 total cost？（Pause）我问这个是因为我们某个零售客户当初也觉得 Azure EA 更便宜，后来算上 Graviton 实例的性能优势和管理开销缩减，实际 TCO 低了30%。如果我把这个对比模型分享给您参考，有价值吗？"}` | `{如果客户说已经做过 TCO 对比：ask 能否分享他们用的假设，我们提供第二视角帮他验证}` | `{No — unless contract already signed with competitor}` |

---

## 6. Meeting Agenda

<!-- AGENT GUIDANCE:
定位：有目的性的时间分配 — 不是形式主义，而是确保会议节奏服务于 Target Outcomes。

📥 数据源：Agent 根据 current stage + Target Outcomes + attendee 数量自动生成议程 → 销售调整

⚡ 对齐 Section 2：议程的时间分配必须服务于 Target Meeting Outcomes — 最多时间分给直接推进 outcome 的环节。如果某个 agenda item 不能说清"它怎么帮我达成 Section 2 目标" → 砍掉或压缩。

时间分配原则（出处：RAIN Group "Connect, Convince, Collaborate" + Mike Weinberg）：

按 stage 调整比例：
- Early stage (Prospect/Qualified): 60-70% discovery, 20% insight sharing, 10% next steps
- Mid stage (Technical Validation): 30% discovery (deeper), 40% solution discussion, 20% co-creation, 10% next steps
- Late stage (Business Validation): 20% validation, 30% proposal review, 40% negotiation/discussion, 10% commitment

Mike Weinberg 原则："The person asking questions controls the conversation."
- 发现阶段：客户说话时间应占 60-70%
- Seller 的 "sales story" 压缩到 2-3 分钟 compelling narrative，不是 20 分钟独白

Customer-Centric Agenda Design（出处：Jeb Blount, Sales EQ + Gartner）：
| Seller-Centric（避免） | Customer-Centric（最佳实践） |
|---|---|
| "Company overview" | "Your current situation & priorities" |
| "Product demo" | "Exploring potential solutions to [specific challenge]" |
| "Pricing discussion" | "Understanding investment criteria & decision process" |
| "Our differentiators" | "What matters most in your evaluation" |

让 Agenda 感觉"双方共有"的技巧：
1. 用客户的语言 — mirror 他们之前用过的术语
2. 包含他们说过的目标 — "You mentioned [X] was a priority..."
3. 有明确的"your input"环节 — 用问题而不是陈述
4. 灵活信号 — "We can adjust as we go based on what's most valuable to you"
5. 命名他们的 outcomes — 开场就说这次会对他们有什么价值

Co-ownership 实践：
- 如果可能，会前 24-48 小时发 draft agenda 给客户："Here's what I was thinking — what would you add or change?"
- Gartner research：买家觉得销售过程"有助于推进采购决策"时，高质量成交的可能性提升 2.8x

时间格式：
- 如果销售给了具体开始时间 → 用 clock time（14:00-14:05）
- 如果没有 → 用相对时间（00:00-00:05）或 duration（5 min）

- ❌ 塞满 presentation slides，没给客户说话的空间
- ❌ "Q&A" 只给5分钟放在最后（说明前面都在讲）
- ❌ Welcome + Company Overview 占20%以上时间
- ✅ Discovery/Dialogue 环节是时间最长的
- ✅ 每个 agenda item 有明确 purpose + owner
- ✅ 最后5-10分钟固定是 next steps commitment（不要跳过或压缩）
-->

> *💡 Agent drafts agenda to achieve Target Outcomes. Time allocation reflects current stage: early = more discovery, late = more negotiation. If possible, send draft to customer beforehand for co-ownership.*

| Time | Topic | Owner | Purpose |
|---|---|---|---|
| `{00:00–00:05}` | `{e.g., "开场对齐：确认今天的目标 + 客户希望讨论什么"}` | `{AM}` | `{Set expectations, signal respect for their time}` |
| `{00:05–00:20}` | `{e.g., "了解贵司当前架构现状和业务增长对基础设施的新要求"}` | `{SA (facilitates) / Customer (speaks)}` | `{Discovery: surface pain and validate hypothesis}` |
| `{00:20–00:35}` | `{e.g., "分享同行业迁移实践 + 初步架构方向讨论"}` | `{SA}` | `{Teaching moment + validate technical fit}` |
| `{00:35–00:50}` | `{e.g., "共同探讨：评估路径和内部推进方式"}` | `{Joint}` | `{Co-creation: 客户参与设计 next steps，不是我们单方面提}` |
| `{00:50–00:55}` | `{e.g., "总结今天的共识 + 确认下一步行动和时间"}` | `{AM}` | `{Secure concrete next step with date}` |
| `{00:55–01:00}` | Close | `{AM}` | — |

---

## 7. Potential Next Steps

<!-- AGENT GUIDANCE:
定位：会议结束时提议的具体下一步 — 对齐 Target Outcomes 和当前 stage exit criteria。

📥 数据源：Agent 从 EP Roadmap + stage exit criteria + Target Outcomes 自动生成 → 销售确认
（注意：会议实际约定的 next steps 由 PMR 记录，可能跟这里的预案不同。PMR 会对比 planned vs actual。）

⚡ 与 Section 2 Target Meeting Outcomes 的对齐（关键！）：
- Next Steps 必须是 Target Outcomes 达成后的自然延伸 — 不能跑偏到跟本次会议目标无关的动作
- Primary path → 对应 Section 2 主目标达成的情况
- Fallback path → 对应 Section 2 Fallback Outcome 的情况
- Not a fit path → 对应 Section 3 Disqualification Signals 被触发的情况
- Agent 生成后自检：每个 next step 能否直接追溯到 Section 2 的某个 outcome？如果不能 → 删除或重写

⚡ 与 Section 2 Fallback Outcome 的关系：
- Section 2 Fallback Outcome = 目标层面的退而求其次（"如果主目标达不到，最低可接受的 advance 是什么"）
- Section 7 Fallback Path = 动作层面的退而求其次（"基于 fallback outcome，具体提议什么动作"）
- 两者必须一致：Section 7 的 fallback next steps 应该是 Section 2 Fallback Outcome 的具体执行方案

写法标准 — SMART Next Step（出处：Jeb Blount, Fanatical Prospecting）：
每个 next step 必须包含：
- WHO：具体负责人
- WHAT：具体的 deliverable 或 action
- WHEN：明确的时间/日期
- WHY：连接到 buyer 说过的目标
- HOW：通过什么机制（会议、邮件、shared doc）

"Micro-Commitment" 原则（Jeb Blount）：
- 每次会议必须以一个具体的、有时间约束的下一步动作结束
- Commitment 要跟当前关系阶段成比例 — 不能太大（吓到人）也不能太小（没推进）
- "Advancing" vs "Continuing"：下一步必须把 deal 往前推，不是"有空再聊"

不 pushy 的提议方式（出处：RAIN Group "Offer, Don't Push" + Mike Weinberg）：
- Lead with value："To help you [objective], I can prepare [deliverable]"
- 给对方 agency："Would it be helpful if...?" 而不是 "We need to..."
- 连接到他们的 timeline："You mentioned needing this resolved by Q3 — to stay on track..."

多路径 Next Steps — 准备三种情况：
- IF YES（strong interest）：大步推进，引入更多 stakeholders
- IF MAYBE（interested but not ready）：提供中间价值，保持节奏
- IF NOT READY（timing/fit concerns）：优雅退出但留门

Jeb Blount 的 "Fallback Position"：
始终准备一个退而求其次的 ask。如果主要 next step 被拒绝，pivot 到一个更小的 commitment 来保持 deal alive。

- ❌ "Let's reconnect soon"（模糊，没有 commitment）
- ❌ "I'll follow up"（seller-only action，客户没有 commitment）
- ❌ "Think it over and let me know"（deal 杀手 — 给了客户消失的许可）
- ✅ "我周四前把 ROI 分析发您，我们下周二2点一起 review 这个数据？"
- ✅ "您内部讨论完后，我们安排一个20分钟的 call 听听 [stakeholder] 的反馈？"
- ✅ "如果 technical deep-dive 对您有价值，我来牵头安排，您帮忙协调 CTO 的时间？"
-->

> *💡 Agent drafts 2-3 concrete next steps aligned with Target Outcomes and stage exit criteria. Prepare multi-path options: if yes, if maybe, if not ready.*

**If meeting goes well (primary path):**

| # | Proposed Next Step | Timeline | Owner | Purpose |
|---|---|---|---|---|
| 1 | `{e.g., "安排 CTO + Lead Architect 参加的技术 deep-dive，展示 Graviton 迁移方案和 POC scope 讨论"}` | `{Within 2 weeks}` | `{Joint: AWS SA 牵头，客户 IT Director 协调内部时间}` | `{Advance to Technical Validation — validate architecture fit}` |
| 2 | `{e.g., "发送定制化 TCO 对比分析（current state vs AWS）供客户做内部 business case"}` | `{Within 1 week}` | `{AWS SA}` | `{Support customer's internal selling + justify investment}` |

**If customer needs more time (fallback path):**

| # | Proposed Next Step | Timeline | Owner | Purpose |
|---|---|---|---|---|
| 1 | `{e.g., "发送一份同行业迁移 reference case + 初步 assessment 报告，给客户消化时间"}` | `{Within 3 days}` | `{AWS}` | `{Provide value without pressure, keep door open}` |
| 2 | `{e.g., "两周后安排一个30分钟 check-in，听听内部讨论后的反馈"}` | `{2 weeks}` | `{AM follow up}` | `{Maintain momentum without being pushy}` |

**If not a fit / timing wrong (graceful exit):**

| # | Proposed Next Step | Timeline | Owner | Purpose |
|---|---|---|---|---|
| 1 | `{e.g., "发送一份行业趋势报告作为 parting gift，不附带任何 ask"}` | `{Within 1 week}` | `{AM}` | `{Leave positive impression, preserve long-term relationship}` |
| 2 | `{e.g., "约定6个月后 check-in（标注 trigger event：如果 X 发生请随时联系）"}` | `{6 months / trigger-based}` | `{AM}` | `{Plant seed for future, don't burn bridge}` |

---

*Call Plan Template | Version: 3.4*
