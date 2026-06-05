# Engagement Plan: {Customer Name} - {Opportunity Name}

> **What is this?** A focused action plan for winning a specific opportunity. Answers: who do I need to win, what do I need from each person, and what's my engagement roadmap to get there?
>
> 🤖 *Automatically generated when the agent learns about a new opportunity. Updated after each visit.*
>
> ✅ *After generating or updating, agent always asks sales to review and revise.*

<!-- AGENT GUIDANCE — Data Provenance Labeling（信息溯源标注）

所有生成的内容必须标注信息来源，让销售清楚每条信息的置信度。

三个标签：
- [销售确认] — 销售直接提供或明确确认的信息，可直接使用
- [AI推断] — Agent 根据上下文分析推断的信息，建议核实（默认，不标时即为此类）
- [网络搜索] — 通过网络搜索获取的公开信息，注意时效

标注粒度：每条独立可判断真伪的断言。
显示规则：只显式标出 [销售确认] 和 [网络搜索]，无标注 = AI推断。
升级机制：销售确认后 [AI推断] → [销售确认]。

示例：
  张总（CTO）— Sponsor [销售确认]
   → 关注降本增效，希望年内完成核心系统上云 [AI推断]
   → 公司2025年Q3完成B轮融资$50M，进入扩张期 [网络搜索]

注意：
- HTML 渲染时，标签用 pill badge 展示（[销售确认]=绿色，[AI推断]=橙色，[网络搜索]=蓝色）
- Markdown 输出时直接用方括号文字
- 销售确认某条信息后，下次更新时升级标签
-->

---

## 1. Opportunity Snapshot

| Field | Value |
|---|---|
| **Customer** | `{company name}` · `{industry}` · `{New Logo / Existing Customer}` |
| **Opportunity Name** | `{opportunity name}` |
| **Deal Value** | `{ARR or TCV}` |
| **Current Stage** | `{Prospect / Qualified / Technical Validation / Business Validation / Committed / Closed}` |
| **Target Launch Date** | `{YYYY-MM-DD, quarter, or 相对时间}` |

### Why Now

<!-- AGENT GUIDANCE: 以下写法指引仅供agent参考，不出现在最终交付文档中
公式：[具体触发事件] + [硬性deadline] + [不行动的业务后果]
质量标准：
- 触发事件有出处（财报、法规、合同到期、高管指令、竞争威胁）
- Deadline 是硬的（客户不能随意推迟）
- Urgency 来自客户自身，不是我们制造的
避免：模糊表述如"想做转型"、"有预算"、"有兴趣"
-->

`{e.g., "现有ERP系统2027年6月停止维护，CIO已向董事会承诺18个月内完成迁移。按14个月实施周期倒推，必须在2026年Q1完成供应商选型。每延迟一个季度损失约$11M并购整合协同效应。"}`

### Deal Objective

<!-- AGENT GUIDANCE:
公式：[动作] + [方案/范围] + [金额] + [时间] + [对齐的 Why Now]
质量标准：
- 像合同摘要一样具体：谁、买什么、多少钱、什么时候、为什么是这个时间
- 与 Why Now 逻辑一致
避免：模糊表述如"赢下这个客户的云业务"、"扩大份额"
-->

`{e.g., "与 GlobalRetail 签署 $3.2M TCV 三年期 AWS Enterprise Agreement，覆盖400+工作负载从自建数据中心迁移至 AWS，目标在2026年3月31日前完成签约，对齐数据中心租约2026年6月到期的硬性时间节点。"}`

### Win Strategy

<!-- AGENT GUIDANCE:
公式：[核心差异化] + [客户最关心的点] + [只有我们能deliver的] + [关键执行动作]
质量标准：
- 针对具体竞争对手的差异化，不是泛泛说"我们最好"
- 锚定客户的 #1 优先级
- 有可执行的关键动作
- 随 engage 深入持续验证和更新
-->

`{e.g., "客户平台团队拥有三年 AWS 使用经验，在技术评估中我们具备天然优势。主要竞争对手 Azure 通过 Microsoft EA 在高管层建立了较强关系，我们的应对策略是通过联合 executive briefing 展示基于 Graviton 的迁移方案可降低30%总体拥有成本。关键执行动作包括：2月15日前完成 Migration Readiness Assessment 建立技术可信度，嵌入 ProServ 顾问到客户团队加速方案落地，以及安排同行业零售客户的迁移成功案例 reference call 消除客户顾虑。"}`

**Key Risks:** `{最大的1-2个可能导致输单的风险因素，用完整语句描述}`

<!-- AGENT GUIDANCE:
Win Strategy 回答"凭什么赢"，Key Risks 回答"最怕什么"。两者构成完整战略判断。
e.g., "CIO 与微软有超过五年的深厚个人关系，存在绕过技术评估直接在高管层面做出决策的风险。此外，客户正在经历内部组织重组，新任 CTO 上任后可能重新评估所有在途项目，导致本项目暂停或优先级下降。"
-->

---

*Last updated: {YYYY-MM-DD} · Source: {Opp Progression / BTTROC / 销售口述 / PMR #N}*

### Engagement Progress

<!-- AGENT GUIDANCE:
根据 Current Stage 自动生成进度条。用 ● 标记当前阶段，━━ 连接。
格式固定，agent 每次更新 EP 时自动刷新位置。

⚠️ Stage 数据来源：仅从 Opportunity Progression skill 获取。EP 不自行判断 stage 是否推进。
每次 PMR 回流后，如有 stage-relevant evidence，agent 调用 Opp Progression 验证，
根据返回结果更新此进度条。详见 SKILL.md Rule 11。
示例（当前 Technical Validation）：
[Prospect] ━━━ [Qualified] ━━━ [Tech Val] ━━● [Biz Val] ━━━ [Committed] ━━━ [Closed]
                                              ▲ We are here
如果有明确的 Target Launch Date，在末尾标注：
[Prospect] ━━━ [Qualified] ━━━ [Tech Val] ━━● [Biz Val] ━━━ [Committed] ━━━ [Closed → 2026-Q1]
                                              ▲ We are here
-->

```
[Prospect] ━━━ [Qualified] ━━━ [Tech Val] ━━━ [Biz Val] ━━━ [Committed] ━━━ [Closed]
                                ▲ We are here
```

---

## 2. Engagement Plan

> *💡 The core of this document. For each person relevant to this deal: who are they, what do we need from them, and how do we win them? People and engagement actions are directly linked — every meeting exists to advance one or more people toward the outcome we need.*

### Key Stakeholders

<!-- AGENT GUIDANCE:
数据来源流程：
1. 从 Account Context (org chart, relationship map) 获取客户主要 stakeholders
2. Agent 根据 opp 上下文判断哪些人跟这个商机相关
3. 跟销售确认：是否需要加人或去人
4. 对每个人 enrich：
   - What They Care About → 调用 CXO Personas（按本 opp 上下文筛选相关维度）
   - Profiling → 调用 Contact Profiling
5. 综合以上信息写出 What We Need / How to Win

Stakeholder 数量指引（根据 deal 复杂度灵活判断）：
- 简单 deal (<$100K): 3-5 人
- 中等 deal ($100K-$500K): 5-8 人
- 复杂 deal ($500K-$1M): 7-12 人
- 战略 deal ($1M+): 10-15+ 人
- 早期可以先 map 3-5 人，随 engage 深入逐步扩展
- 红线：任何 $100K+ 的 deal 如果只有 <3 个 stakeholder = 单线程高风险，需要提醒销售

不包含与本商机无关的人。
-->

**{Name}** — {Title}

| Dimension | Details |
|---|---|
| **Engagement Priority** | `{e.g., "Must Meet — 没有他的技术签字，采购不会放PO。必须在6月15日前 engage。"}` [销售确认] |
| **Role in This Deal** | `{e.g., "Technical Evaluator — 负责架构评审，有一票否决权。"}` [销售确认] |
| **Current Stance** | `{e.g., "Supporter — 在 WAR 后对30%成本优化潜力表现出浓厚兴趣，主动索要了详细报告。"}` |
| **What They Care About** | `{e.g., "董事会要求Q4前降低云支出20%。上季度财报被点名基础设施成本超支。"}` [网络搜索] |
| **Profiling** | `{e.g., "工程师出身，数据驱动。偏好30分钟 deep dive，入职8个月需要可见转型成果。"}` |
| **What We Need From Them** | `{e.g., "1) 5月底前引荐 CFO。2) 分享内部评估标准文档。3) 6月架构评审会上呈现联合 case。"}` |
| **How to Win Them** | `{e.g., "1) 先搞定 VP Eng — CTO 高度信任其技术判断。2) 提供 TCO 对比。3) 安排 peer-level briefing。"}` |

<!-- AGENT GUIDANCE — 每个维度的写法标准：

**Engagement Priority**
公式：[优先级] + [为什么是这个优先级] + [时间约束]
- ❌ "High"
- ✅ "Must Meet — 没有他的技术签字，采购不会放PO。必须在6月15日前 engage（架构评审委员会每月开一次）。目前只见过一面，投入不够。"

**Role in This Deal**
公式：[角色标签] + [具体在这个 deal 里的 function] + [能 block 或 enable 什么]
角色标签：Decision Maker / Champion / Influencer / Blocker / Evaluator / Procurement
- ❌ "Decision Maker"
- ✅ "Technical Evaluator — 负责架构评审，将撰写 RFP 的技术评分标准。没有预算权，但在技术适配性上有一票否决权。"

Champion 验证：如果销售说某人是 Champion，agent 需要通过提问验证：
- "他最近帮你做了什么具体动作？"（约会议？引荐？分享内部文档？）
- "他有没有在你不在的时候帮你说话？你怎么知道的？"
- "如果你给他一个任务（比如帮你约 CFO），他会完成吗？"
如果销售答不出具体 evidence → 标注为 "Potential Champion [待验证]"，不标 Champion。
真正的 Champion = 有行动证据，不是"感觉他挺支持我们"。

**Current Stance**
公式：[Holden 立场标签] + [判断依据/evidence] + [对竞争对手/现状的态度] + [与其他 stakeholder 的关键关系]

立场分级（基于 Holden Power Base Selling 模型，出处：Jim Holden, *The New Power Base Selling*, Wiley, 2012）：
- **Sponsor** — 主动为我们提供 access、信息和政治掩护，承担个人风险帮我们推进
- **Supporter** — 偏向我们，会说好话，但不会冒政治风险去公开站队
- **Neutral** — 无明确偏好，可能被任何一方争取
- **Non-Supporter** — 倾向竞争对手或维持现状，被动地不配合
- **Adversary** — 主动反对我们，可能是竞争对手的 Sponsor

- ❌ "Supportive"（单词，无 evidence，无上下文）
- ✅ "Supporter — 在我们的 Well-Architected Review 后对30%成本优化潜力表现出浓厚兴趣，主动索要了详细报告，但尚未在内部公开为我们站台。两年前他主导了 Azure 迁移决策，公开转向 AWS 对他有政治风险。与 VP Engineering 是强联盟（前公司同事），CTO 高度信任他的技术判断。"

关键：stance 必须有 evidence 支撑，不能只是感觉。
验证问题："判断依据是什么？他做了什么具体动作来支持/反对？"
注意：同一个人在不同 deal 里可能是不同 stance — 这是 per-deal 评估，不是对这个人的永久标签。

**What They Care About**
公式：[具体业务压力/KPI] + [压力来源] + [时间约束] — 必须跟本 opp 相关
数据来源：CXO Personas（exec only）+ web research enrichment
- ❌ "Cost savings and performance"
- ✅ "董事会要求Q4前降低云支出20%。她的团队上季度财报预备会上被点名基础设施成本超支。迁移速度是次要的，单位经济模型是核心。"
注意：从 CXO Persona 提取时，只选与本 opp 相关的维度，不要 dump 整个 persona。

**Profiling**
公式：[沟通风格] + [决策模式] + [个人动机/career motivation] + [怎么跟他沟通最有效]
数据来源：Contact Profiling skill
- ❌ "Analytical type"
- ✅ "工程师出身的高管，数据驱动 — 要带 benchmark 和参考架构，不要 PPT。偏好30分钟 deep dive 而非高管概述。入职8个月（从 Google Cloud 过来），需要一个可见的转型成果来建立 CEO 信任，之前错过了一次晋升VP的机会。通过她的首席工程师（Sarah）建立信任最有效。"
注意：包含个人动机（晋升、避险、立功），这是真正驱动行为的因素。

**What We Need From Them**
公式：[编号的、具体的、可验证的 ask] + [时间节点]
- ❌ "Support and approval"
- ✅ "1) 5月底前引荐给 CFO（预算持有人）。2) 分享内部评估标准文档。3) 在6月架构评审委员会上呈现我们的联合 business case。4) 确认我们在 RFP 发出前进入 vendor shortlist。"

**How to Win Them**
公式：[有序的具体动作] + [政治约束/人际动态考量] + [谁从 AWS 去 engage] + [不能做什么]
- ❌ "Show ROI and build relationship"
- ✅ "1) 先搞定 VP Eng Sarah — CTO 不会推翻她的技术判断（强信任关系）。2) 提供 TCO 对比 vs 现有多云架构（她做 board deck 需要这个数据）。3) 安排我们 VP Engineering 做 executive briefing（peer-level credibility）。4) 不要定位为 rip-and-replace — 她在政治上不能公开否定前任的 Azure 决策。利用她和 CFO 的联盟关系，让她帮我们引荐。SA 主导技术交流，AE 负责高管关系。"
-->

*Repeat for each person relevant to this deal.*

---

### Engagement Roadmap

<!-- AGENT GUIDANCE:
这是从现在到 close 的完整路线图。每行 = 一个里程碑（station）。

展示格式：Metro Journey Map（地铁线路图风格）
- 垂直轨道线 + 站点圆点 + 卡片
- 右上角 pill badge 显示 "X/N Stations Complete"
- 每站显示：Milestone 描述、Status badge、Key Stakeholders、AWS Team
- 底部显示 Deal Objective 作为终点站

时间逻辑：
- 不使用固定 Target Window / Week 标识
- 靠站点顺序（#1→#2→#3）表达依赖和推进关系
- 如销售提供了明确 close date，agent 可建议各 milestone 完成时间点（target_date 字段），但必须保证时间准确性
- 没有 close date 时不猜测时间，只靠顺序

写作标准：
- Milestone 必须是 outcome-oriented + buyer-verifiable，不是活动描述
  - ❌ "跟 CTO 开会"（活动，seller-only）
  - ❌ "发送 proposal"（活动，seller-only）
  - ✅ "CTO 在架构评审会议后正式确认目标架构方案，并授权团队启动为期两周的 POC 验证。"（结果，有客户动作）
  - ✅ "Economic Buyer 和 Champion 在联合会议中完成 proposal 逐项评审，确认方案满足业务需求并指示采购团队启动流程。"（结果，有客户动作）
- 每个 milestone 必须包含客户动作/确认 — 如果只有 AWS 在做事，deal 没在推进
- Milestone 类型不只是 meeting，常见类型包括但不限于：
  - Meeting / Call（常规拜访）
  - Workshop / POC（技术验证）
  - Executive Briefing (EBC)
  - Internal Review（客户内部流程，我们控制不了但要 track）
  - Commercial Negotiation（商务谈判）
  - Reference Visit / Customer Event / Partner Joint Session 等
- AWS Team 根据 milestone 目标匹配合适资源，以下为常见参考，非固定搭配：
  - Discovery: 通常 AM + SA，如涉及特定技术领域可提前引入 Specialist
  - 技术验证/POC: 通常 SA 主导，按需引入 Specialist SA、ProServ、Partner
  - 高管 engage: 通常 AM + Executive Sponsor，按需 SA 提供技术支撑
  - 商务谈判: 通常 AM + Deal Desk，复杂条款引入 Legal
  - 实施: 通常 SA + TAM + CSM，按需 ProServ/Partner
  - 具体组合由销售根据实际情况判断，agent 可建议但不强制

Milestone Completion 自检（不出现在最终文档，agent 内部把关）：
⚠️ 注意：这是 Roadmap Milestone 层级的完成标准，不是 Opportunity Stage Exit Criteria。
Opp Stage 的推进判断由 Opportunity Progression skill 负责，EP 不做 stage 推进决策。
- 每个 milestone 写完后自问："这一步达成什么算完成？evidence 是什么？"
- 好的 evidence：客户邮件确认、签字文档、会议纪要、POC scorecard
- 差的 evidence："感觉客户挺积极的"、"他说会考虑"

字段写法 guidance：

**Milestone (description)**
- 公式：[谁] + [做什么具体动作/决策] + [产出/授权什么]
- 长度适中，一句话说清楚（15-50字）
- ❌ "Discovery meeting" / "Follow up"
- ✅ "CTO 和 IT Director 在首次技术交流中确认核心业务痛点和内部决策流程，并授权 AWS 团队进入正式技术评估阶段。"

**Detail (可选)**
- 补充说明：关键议题、前置条件、或达成标准
- 不超过 2 句话
- 如果 milestone 描述已足够清晰，可省略

**Key Stakeholders**
- 填这一步需要 engage 的客户侧核心人物（来自上方 Key Stakeholders section）
- 一行一个 milestone，不按 stakeholder 拆行 — 每步涉及的人列在一起
- 用名字（如果已知）或角色（如果还在 mapping），每步通常 1-3 人
- Per-person 的细分目标不放在 roadmap，而是在 Next Milestone Detail / Call Plan 里展开
- ❌ 列一长串人名凑数
- ✅ "王总 (CTO), 李工 (Lead Architect)" 或 "{CTO, Lead Architect}"

**AWS Team**
- 填这一步参与的 AWS 侧角色或人名
- 早期规划时填角色（AM, SA, Specialist），细化后可替换为具体人名
- ❌ 把所有可能用到的人都列上
- ✅ "AM + SA" 或 "张三 (AM), 李四 (Data SA)"

**Target Date (可选)**
- 仅在销售提供了明确 close date 时才填写
- 从 close date 倒推各 milestone 时间点
- 如客户有已知的内部节点（董事会、财年结束、合同到期），优先对齐客户节奏
- 写法灵活：具体日期（"6月15日"）、相对时间（"POC 完成后1周内"）、锚定日期（"对齐6月30日架构委员会"）
- ❌ "尽快"、"TBD"、凭空猜测时间
- ✅ "6/15（对齐客户6月30日架构委员会）"

Roadmap 演进：
- 每次 PMR 后更新：当前 Next → Done，下一个 Planned → Next
- 里程碑可以增加、删除、重排序 — 不是一成不变的
- 如果某步没达成预期，可以加补充步骤或调整策略

多格式输出（agent 按场景选择）：
- **journey**（默认）：Metro Journey Map，完整卡片 + 进度轨道，适合战略规划和首次制定 EP
- **compact**：简洁垂直列表，轻量 spine，适合日常 review / 每周 1:1
- **executive**：横向一览 + Phase Bar，一页看完，适合给 manager / VP
- **external**：精简版 journey（去掉内部标注），对客汇报用
-->

| # | Milestone | Key Stakeholders | AWS Team | Status |
|---|---|---|---|---|
| 1 | `{e.g., CTO 和 IT Director 在首次技术交流中确认核心业务痛点和内部决策流程，并授权 AWS 团队进入正式技术评估阶段。}` | `{CTO, IT Director}` | `{AM, SA}` | **Next** ↓ |
| 2 | `{e.g., 架构评审完成后 CTO 正式签字确认目标架构方案，同意启动为期两周的 POC 验证并指定工程师参与。}` | `{CTO, Lead Architect}` | `{SA, Data Specialist}` | Planned |
| 3 | `{e.g., POC scorecard 全部达标，VP Engineering 确认技术方案满足生产需求，并将 business case 提交给 CFO 进行预算审批。}` | `{VP Eng, CTO}` | `{SA, ProServ}` | Planned |
| 4 | `{e.g., CFO 审批通过 business case 并确认预算到位，正式指示采购团队启动供应商签约流程。}` | `{CFO, Champion}` | `{AM, Deal Desk}` | Planned |
| 5 | `{e.g., 双方完成合同条款最终谈判，Economic Buyer 签署正式协议，implementation kickoff 会议时间确定。}` | `{Procurement, Legal, EB}` | `{AM, Legal}` | Planned |

> *以上为典型 $1-3M 云迁移 deal 的示例节奏，非固定模板。实际 milestone 数量、顺序、间隔由 deal 复杂度和客户节奏决定 — 有些 deal 3步就能 close，有些需要 10+ 步。*

> *Status: **Next ↓** (详见下方 Next Milestone Detail) · **Planned** · **Done** · **Skipped***
>
> *Roadmap 随 engage 深入持续演进 — 里程碑可增加、删除、重排序。每次 PMR 后更新。*

---

### Estimate & Contingency

<!-- AGENT GUIDANCE:
定位：整个 deal 的预估 + 双维度应急预案（人 + 流程），确保终点（Deal Objective）不变。
💡 Living estimate — 每次 PMR 后根据新信息重新评估。初始版本是 agent 基于 deal 复杂度和 roadmap 的最佳估算；后续版本反映实际进展。

核心约束：终点（Deal Objective）是固定的 — 所有 contingency 调整的是路径、节奏、接触方式，不是目标。

估算逻辑：
- 从 Engagement Roadmap 的 milestone 数量和 Target Window 推导
- 参考 deal 的复杂度因子调整：
  - Deal size（<$100K 简单 / $100K-$500K 标准 / $500K-$1M 复杂 / $1M+ 战略级）
  - New Logo vs Existing Customer（New Logo 通常 +50-100% 周期）
  - 决策者数量（>5人的 committee buy 通常 +30-60%）
  - 是否涉及 displacement（替换现有供应商通常 +20-50%）
- Best Case = 一切顺利，客户推进积极，无意外
- Worst Case = 合理的最差情况（不是灾难性的，是"正常的企业摩擦"）
- 随 deal 推进，range 应该逐步收窄：
  - 早期（Discovery）：±50-100% 的不确定性正常
  - 中期（Evaluation）：±25-40%
  - 后期（Negotiation）：±10-20%
- 每次 PMR 后根据实际进展重新评估

═══════════════════════════════════════════════════
PART A: Stakeholder Risk & Leverage（人维度）
═══════════════════════════════════════════════════

定位：识别最可能阻碍 deal 推进的关键人物 + 用"跨人杠杆"化解风险。
方法论来源：Miller Heiman "Red Flags → Leverage from Strength" (The New Strategic Selling, 1998) + Power Base Selling "Paths to the Fox" (Jim Holden, 2012)

核心机制（Blue Sheet Section 3 逻辑）：
- 每个 Red Flag 绑定一个具体的人 — 不是泛泛的"有风险"
- 化解方式是找到另一个人身上的 Strength/关系来做杠杆
- 公式：[某人的 Red Flag] → [另一个人的 Leverage] → [具体 Action]

什么时候写 Stakeholder Risk：
- Key Stakeholders 中 stance 为 Neutral / Non-Supporter / Adversary 的人 → 必须有
- 任何 Engagement Priority 为 "Must Meet" 但尚未建立实质接触的人 → 必须有
- 在 Roadmap 关键路径上但我方缺乏 access 的人 → 必须有
- 已经是 Sponsor/Supporter 的人 → 通常不需要（除非有被调岗/离职等变化风险）

Red Flag 标准类型（Miller Heiman 5种 + 扩展）：
1. Contact Not Made — 联系不上 / 约不到
2. New to Role — 新上任，态度未知
3. Reorganization — 组织变动，权力/优先级可能移动
4. Non-Supporter / Adversary — 主动或被动反对我们
5. Information Uncertain — 对此人的判断依据不充分
6. Access Dependent on Single Path — 只有一条路能触达他（如果这条断了就完全没办法）

Leverage Source 类型（从哪里借力）：
- Coach / Champion 的关系 — 让已有信任的人帮我们铺路
- 下属/团队成员 — 先赢得执行层，用成果向上传导
- 同级联盟 — 找他的 peer 形成共识压力
- Executive Sponsor (peer-level) — AWS 高管对客户高管
- Partner/SI 已有关系 — 借助第三方的信任
- AWS 内部关系网 — 其他 AM/团队之前的客户接触
- 技术成果/数据 — 用可验证的 outcome 倒逼他必须参与
- 外部影响力 — 行业分析师、reference customer、行业活动

Agent 生成 Stakeholder Risk 的方式：
1. 自主分析：扫描 Key Stakeholders → 对 stance 为 Neutral/Non-Supporter/Adversary 或 "Must Meet 但未接触" 的人，自动生成 Red Flag
2. 扫描关系网络：从已有 Sponsor/Supporter 身上找可用的 Leverage Source
3. 主动提问销售获取更多信息（销售脑子里有关系但可能没说）：
   - "这个人你认识他团队里其他人吗？跟谁关系比较好？"
   - "有没有 partner 或者 SI 之前跟他合作过、说得上话？"
   - "AWS 内部有没有同事之前跟他或他公司打过交道？"
   - "你觉得他不回应的原因是什么？是忙、还是有顾虑、还是政治原因？"
   - "他最近有什么关心的事情是我们能帮到的？"
   - "如果不走他这条路，你觉得还有谁能影响这个决策？"
4. 基于1+2+3组合出具体 Leverage Action，跟销售确认可行性

路径策略库（灵活组合，不是固定选择）：
搞不定某个 stakeholder 时，可用的路径方向包括但不限于：
- 往下走：找他的下属先建立技术共识或产出成果，用结果倒逼他必须参与
- 往上走：通过 executive sponsor 发起 peer-level 对接，提供更高规格的参与入口
- 横向走：找他的同级（同 level 不同部门）形成组织内部联盟或共识压力
- 往内找：找他团队里跟我们有过接触的人（之前合作过的工程师、参加过 workshop 的人）
- 借外力：通过 Partner/SI 已有的客户关系、行业分析师推荐、reference customer 现身说法
- 借内力：AWS 内部谁认识他？其他 AM 之前 cover 过这个客户？executive sponsor 有私人关系？
- 换场景：不约正式会议，换成行业活动、executive dinner、客户 workshop、线上 webinar
- 换诉求：不谈 deal，先帮他解决一个他自己的问题来建立 trust
- 换时机：等一个他关心的 trigger event（财报、合同到期、竞品出问题、内部组织变动）
- 换人设：不是销售去找他，让他信任的人（Champion、partner、内部同事）帮引荐
以上路径可自由组合 — 比如"往下走 + 借外力"：通过 partner 关系接触他的下属，先做联合技术评估。

═══════════════════════════════════════════════════
PART B: Milestone Risk & Contingency（流程维度）
═══════════════════════════════════════════════════

定位：Roadmap 中最可能受阻的关键节点 + 替代推进路径。
核心原则：
- 不是对整个 deal 的 Plan B，是针对 Roadmap 中具体步骤的替代路径
- 只写高风险节点（2-3个）— 如果某步几乎不可能出问题，不需要写
- 每条必须有明确的 trigger condition（什么信号触发切换），不是"万一搞不定"
- 每条风险形成完整闭环：[里程碑] → [风险项（🚩流程 / 🧑人物）] → [触发条件] → [影响] → [Plan B]

重要：Milestone Risk 中的 🧑人物风险 与 Part A 的关系：
- Part A = 战略层面 — "这个人整体上对我们是什么态度，我们的杠杆策略是什么"
- Part B 的 🧑人物风险 = 战术层面 — "在这个具体步骤中，这个人可能怎样阻碍，替代路径是什么"
- Part A 是"知彼"（了解人的风险全貌），Part B 是"行动"（在具体节点上怎么应对）
- 两者互为引用：Part B 的 Plan B 经常调用 Part A 中已识别的 Leverage Source

替代路径类型：
- 绕道人：通过目标 stakeholder 的下属/上级/同事/partner 关系间接施加影响
- 绕道事：调整 milestone 顺序、拆解大步骤为小步骤、用技术成果倒逼决策
- 降维：缩小 deal scope（enterprise → department, 全量 → POC-first, 大合同 → phase 分拆）
- 借力：引入外部力量（partner/SI、executive sponsor 对等邀请、行业分析师背书、reference customer）

═══════════════════════════════════════════════════
质量验证标准（适用于 Part A 和 Part B 所有 Plan B）
═══════════════════════════════════════════════════

"Tuesday Morning Test"（出处：战略销售实践社区通用验证标准）：
如果 Plan A 周一下午失败了，周二早上能立刻启动 Plan B 吗？
如果答案里有"尝试联系"、"看看能不能"、"希望"→ 不是 plan，是 hope。

验证维度：
| 标准 | 合格 | 不合格 |
|------|------|--------|
| 关系存在性 | 已有过接触，有上下文 | org chart 上的名字，从未联系 |
| Stakeholder 动机 | 他有明确理由去行动（他的 pain/KPI） | 假设对方会出于好意帮忙 |
| 时间可行性 | 在 deal 剩余 timeline 内可完成 | 需要的时间超出窗口 |
| 独立于主路径 | 即使 Plan A 彻底失败也能走通 | 依赖同一个 blocker 配合 |
| 具体性 | 有名字、有动作、有时间节点 | "找其他人试试"、"想办法" |
| 不烧主路径 | 启动 Plan B 不损害 Plan A 关系 | 绕过人会激怒他造成更大阻碍 |

如果某条 Plan B 无法通过验证 → 标注为"待验证"，agent 通过提问销售补充信息直到可验证。

触发机制（两种）：
1. 预设型：写在本表中的 trigger condition，agent 在每次 PMR 后对照检查是否已触发
2. 实时型：对话中 agent 识别到以下信号时，主动建议启动或制定 contingency path：
   - 销售表示某个 stakeholder 联系不上、不回应、不配合
   - 销售询问"能不能找其他人""能不能换个方式"
   - 某个 milestone 超过预期时间仍未推进
   - 销售反馈某人态度从 Supporter 降级为 Neutral/Non-Supporter
   - 出现原计划未预料的 blocker（新人介入、预算冻结、组织变动等）
   Agent 应主动提出："看起来这条路径遇到阻碍了，要不要考虑替代方案？" 并给出具体建议。
-->

> *💡 Living estimate — 每次 PMR 后根据新信息重新评估。终点（Deal Objective）固定不变，调整的是路径和节奏。*

| | Best Case | Worst Case |
|---|---|---|
| **Milestones to Close** | `{e.g., 5}` | `{e.g., 8}` |
| **Timeline** | `{e.g., 10 weeks}` | `{e.g., 16 weeks}` |

#### Stakeholder Risk & Leverage

> *对关键路径上搞不定/有风险的人：识别 Red Flag → 找杠杆 → 制定 Action。*
> *方法论：Miller Heiman "Red Flags → Leverage from Strength" + Power Base Selling "Paths to the Fox"*

| At-Risk Stakeholder | Red Flag | Leverage Source | Plan B |
|---------------------|----------|-----------------|--------|
| `{e.g., CTO 王总}` | `{e.g., Contact Not Made — 两周内三次邀约未获回应，可能因我方缺乏 peer-level credibility 或议题对他不够有吸引力}` | `{e.g., IT Director 赵工 (Sponsor) — 直接汇报线，CTO 高度信任其技术判断；AWS VP Engineering 可做 peer-level 对接}` | `{e.g., 1) 让赵工在周报中呈现 POC 初步成果，制造 CTO 主动了解的动机。2) AWS VP Engineering 发 peer-level 邮件，提供 executive briefing 作为更高规格入口。3) 如仍无回应，换场景 — 通过行业 CTO 圆桌活动制造非正式接触机会。}` |
| `{e.g., CISO 张总}` | `{e.g., Non-Supporter — 前期沟通中明确表达对数据主权合规的担忧，且与现有安全供应商关系紧密}` | `{e.g., VP Engineering 李工 (Supporter) — 与 CISO 是前公司同事，私下关系好；第三方安全审计报告可提供客观背书}` | `{e.g., 1) 请李工非正式沟通了解 CISO 核心顾虑（是合规条款？还是政治？）。2) 提前准备 SOC2 + 等保三级报告 + 定制化数据驻留方案。3) 安排 AWS Security Specialist 做专项答疑，不经过正式评审流程先消除技术疑虑。}` |

> *只针对 stance 为 Neutral / Non-Supporter / Adversary，或 "Must Meet 但尚未建立实质接触" 的关键人物。已经是 Sponsor/Supporter 的人通常不需要（除非有离职/调岗风险）。每次 PMR 后同步更新。*

#### Milestone Risk & Contingency

> *Roadmap 中最高风险的 2-3 个节点：流程风险（🚩）和人物风险（🧑）并列。*

| 里程碑节点 | 风险项 | 触发条件 | 影响 | Plan B |
|-----------|--------|---------|------|--------|
| `{e.g., #2 CTO架构评审}` | 🧑 CTO 缺席/拒绝评审 | `{两周内三次正式邀约均未获回应}` | `{+2-3 weeks, 后续 milestone 全部顺延}` | `{通过 IT Director 先做非正式技术 deep-dive，用成果倒逼 CTO 参与。同时 AWS Exec Sponsor 发 CxO peer-level 邀请。（Leverage: 赵工的汇报线关系 + AWS VP credibility）}` |
| | 🚩 评审排期冲突 | `{客户Q2架构委员会已排满，无法加入议程}` | `{+2 weeks}` | `{申请以"urgent security review"名义插入特别议程，或改为线下小范围 working session 替代正式委员会流程}` |
| `{e.g., #4 CFO预算审批}` | 🧑 CFO 质疑ROI/冻结预算 | `{CFO 明确表示当前财年无法新增大额支出}` | `{+4-6 weeks, deal 结构可能变化}` | `{将 $3.2M 调整为 Phase 1（$800K，聚焦最痛2个工作负载），90天可验证 ROI 建立下一财年 business case。同时探索 Partner 先行承担部分实施投入。（Leverage: Champion 帮我们在内部推 business case + CFO peer reference call）}` |
| | 🚩 采购流程延迟 | `{法务条款审核超出预期，数据主权条款争议}` | `{+3-4 weeks}` | `{预备本地化部署备选架构 + 提前准备合规文件包，并行推进供应商入库流程}` |

> *终点（Deal Objective）不变 — 所有 Plan B 调整的是路径和节奏，不是目标。每次 PMR 后同步更新：已完成节点的 contingency 移除，新暴露的高风险节点补充进来。*

---

### Next Milestone Detail

<!-- AGENT GUIDANCE:
定位：Roadmap → Next Milestone Detail → Call Plan 的中间层。
- Roadmap = 鸟瞰（一行一个 milestone）
- Next Milestone Detail = 战术意图（对谁、达成什么、讨论什么）
- Call Plan = 战术执行（具体会议的详细方案）
本 section 的职责是"够用来触发 Call Plan 生成"，不重复 Call Plan 的细节（如会前准备、材料清单、成功标准等）。

⚡ 双向同步规则：
- EP → Call Plan：本 section 内容自动流入 Call Plan 的 Meeting Details + Target Outcomes
- Call Plan → EP：销售在 Call Plan 修改了 target outcome / attendees / next steps 后，Agent 必须检查本 section 是否需要同步更新
- 绝对不能只改一个地方忘记另一个地方

写作标准：

**Objective**
公式：[战略目的] + [为什么这一步是当前最重要的] + [跟整体 roadmap 的关系]
- ❌ "Validate pain, understand decision process"（碎片，太泛）
- ✅ "通过首次技术交流深入了解客户当前架构痛点和内部采购决策流程，确认我们的方案假设是否成立，为后续架构评审奠定基础。"

**Customer Attendees & Target Outcome（核心字段）**
这是 per-person 的细分目标落地点。每个人必须有明确的、可验证的 target outcome。

写法公式：[Name/Role] — [期望这个人从当前状态到什么状态] + [需要他做什么具体动作]

质量验证（"5分钟测试"）：
- 会议结束后5分钟内，你能不能判断这个 outcome 是否达成？如果不能 = 不够具体。

按角色区分 outcome 类型：
- Decision Maker / EB → 侧重 commitment、budget confirmation、timeline agreement
- Champion → 侧重 action（帮你引荐、内部推动、分享信息）
- Technical Evaluator → 侧重 validation（确认技术匹配、定义 POC 标准）
- Blocker → 侧重 de-risking（让他说出具体顾虑、从反对变中立）

stance 分级参考（与 Key Stakeholders 的 Current Stance 统一，基于 Holden Power Base Selling）：
Adversary → Non-Supporter → Neutral → Supporter → Sponsor
目标是在每次 engagement 中推动 stakeholder 向右移动至少一级。

- ❌ "CFO — confirm interest → Supportive"（碎片，无具体动作）
- ❌ "IT Director — identify as Champion"（不可验证，怎么算 identify？）
- ✅ "王总 (CFO) — 当前 Neutral（了解我们但未表态），目标推进至 Supporter：让他认知到现有架构每季度多支出 $2M 的事实，并同意在下次领导会上听取我们的 business case 汇报。"
- ✅ "李工 (IT Director) — 当前 Supporter（偏向我们，多次索要技术资料），目标验证能否推进至 Sponsor：给他一个具体任务（帮我们安排与 CTO 的技术深潜会议），看是否愿意承担个人风险去推动。"
- ✅ "张总 (CISO) — 当前 Adversary（公开表示迁移安全风险不可接受），目标推进至 Non-Supporter（不再主动阻拦）：让他明确说出具体的安全顾虑清单，并确认如果我们逐条满足这些条件他不会继续反对。"

**AWS Team**
填这一步参与的 AWS 侧角色或人名（与 Roadmap 一致）。

**Key Questions & Discussion Points**
不只是 discovery 问题 — 根据 milestone 所处阶段选择合适的问题类型。

按阶段区分：
- Discovery: 开放性探索 — 了解痛点、现状、决策流程
- Technical Validation: 标准确认 — 需求排序、集成约束、POC 标准
- Business Case: 量化导向 — ROI 计算、优先级排序、审批条件
- Negotiation: 条件探索 — 预算约束、合同条款、trade-off
- Closing: 确认导向 — 剩余障碍、签约流程、时间承诺

质量标准：
- 每个问题必须 purpose-driven — 答案会直接改变你的策略或推进 deal
- 问题要体现 stakeholder 的已知关注点（基于 What They Care About + Profiling）
- 问题要展示专业度（不问网上能查到的信息）
- 3-5 个问题，按优先级排序
- ❌ "What are your biggest challenges?"（太泛，任何公司都能问）
- ❌ "What's your budget?"（太直接，没有上下文）
- ✅ "上次您提到数据驻留合规是核心顾虑 — 如果我们能在本地 region 提供完整的数据隔离方案，这是否能解决安全团队的主要担忧？还是还有其他阻碍因素？"
- ✅ "贵司去年批准 SAP 迁移项目时，审批流程是怎样的？这次云基础设施的投资决策是否走类似通道？"
-->

> *💡 把当前 Roadmap 中标记为 "Next ↓" 的 milestone 展开为战术意图。触发 Call Plan 生成。每次 PMR 后，完成的 milestone 移入 Execution Log，下一个 Planned 行在此展开。*

**Milestone #{n}** — `{Target Date}`

**Objective:** `{e.g., "通过首次技术交流深入了解客户当前架构痛点和内部决策流程，确认迁移需求的紧迫性和决策链路，为后续正式架构评审和供应商入围奠定基础。"}`

**Customer Attendees & Target Outcome:**
- `{e.g., "王总 (CTO) — 当前 Neutral（了解我们但未表态），目标推进至 Supporter：让他确认现有架构无法支撑明年业务增长目标，并同意安排一次专门的架构评审会议让我们展示迁移方案。"}`
- `{e.g., "李工 (IT Director) — 当前 Supporter（偏向我们，主动索要过技术白皮书），目标验证 Sponsor 潜力：请他担任内部技术评估牵头人，并提供当前系统架构文档供我们做迁移评估。"}`

**AWS Team:** `{e.g., "张三 (AM) 负责整体关系推进，李四 (SA) 负责技术交流和架构讨论。"}`

**Key Questions & Discussion Points:**
- `{e.g., "贵司今年的核心业务增长目标对底层基础设施有什么新要求？现有架构在哪些场景下已经出现瓶颈或限制？"}`
- `{e.g., "如果决定做架构升级，内部的评估和审批流程通常是怎样的？需要哪些角色参与决策？"}`
- `{e.g., "上次您提到与某供应商的合同明年到期 — 续约评估是否已经启动？评估的核心标准是什么？"}`

---

## 3. Execution Log

<!-- AGENT GUIDANCE:
数据来源：每次 Call Plan 执行后，由 PMR (Post-Meeting Report) skill 自动生成输入。
Agent 从 PMR 中提取以下信息填入本 log：
- Planned = 来自 Engagement Roadmap 中对应 milestone 的 Milestone 描述
- Actual = 来自 PMR 中记录的实际发生情况
- People Updates = 来自 PMR 中对每个 attendee 的 stance 变化观察（使用 Holden 5 级模型）
- Key Learnings = 来自 PMR 中的核心发现和 insight
- Plan Adjustment = Agent 基于 PMR 信息判断 Roadmap 是否需要调整

写作标准：
- 所有字段必须是完整描述性语句
- People Updates 必须使用 Holden stance 术语（Sponsor/Supporter/Neutral/Non-Supporter/Adversary）
- Plan Adjustment 必须是 actionable 的（加什么 milestone？改什么时间线？调整什么策略？）
- 如果实际情况与计划一致，也要写明"按计划推进，无需调整"，不要留空

更新流程：
1. Call Plan 执行 → PMR 生成
2. Agent 从 PMR 提取关键信息 → 填入本 log 新条目
3. 同步更新 Engagement Roadmap（当前 milestone Status → Done，下一个 → Next）
4. 同步更新 Key Stakeholders 的 Current Stance（如有变化）
5. 同步更新 Estimate & Contingency（如有变化）— 包括 Stakeholder Risk & Leverage 和 Milestone Risk
-->

> *💡 每次 PMR 后自动添加新条目（最新在最上方）。记录计划 vs 实际的差异，以及由此引发的策略调整。*

### Engagement #{n} - {Date} - {Attendees}

| Field | Details |
|---|---|
| **Planned** | `{e.g., "CTO 和 IT Director 在首次技术交流中确认核心业务痛点和内部决策流程，授权进入正式技术评估阶段。"}` |
| **Actual** | `{e.g., "CTO 确认了云成本优化是董事会级别的优先事项，但表示需要先完成内部安全评估才能授权技术评估。IT Director 主动提出担任评估协调人，并承诺两周内提供当前架构文档。"}` |
| **People Updates** | `{e.g., "王总 (CTO): Neutral → Supporter（主动表达了对 AWS 成本优化能力的认可，但尚未公开承诺支持）。李工 (IT Director): Supporter → Sponsor（主动请缨担任内部评估协调人，承担了个人责任来推进项目）。"}` |
| **Key Learnings** | `{e.g., "安全评估是必经流程，非可跳过步骤 — 需要在 Roadmap 中增加 CISO engagement milestone。客户内部有一个尚未浮出水面的 Azure 续约讨论正在进行，这解释了 CTO 为什么还没公开站队。"}` |
| **Plan Adjustment** | `{e.g., "Roadmap 新增 Milestone #2: CISO 安全评估会议（Week 3），排在原计划架构评审之前。整体 timeline 预计延长2周。Estimate 调整：Best Case 从10周改为12周，Worst Case 从16周改为18周。"}` |

> *每次 PMR 后自动添加新条目。Engagement Roadmap、Key Stakeholders stance、Estimate & Contingency 同步更新。*

---

*Engagement Plan Template | Version: 2.2*
