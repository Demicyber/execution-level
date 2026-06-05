---
name: engagement-plan
description: >
  People-centric deal strategy — who to engage, how to win, meeting roadmap, and execution tracking.
  Use whenever sales asks how to approach or win a deal, plan an opportunity, map stakeholders,
  "怎么打这个单", "商机推进", "拜访规划", "关键人分析", "见谁", "这个客户怎么打",
  or any hint of deal-level planning — even if they just say "怎么推这个商机".
user_locked: true
---

# Engagement Plan Skill

---

## Execution Discipline

STOP. Read this entire skill file before executing.
This skill has a mandatory reference file that defines field-level execution standards.
Do NOT begin the Pre-Generation Dialogue until you understand all rules and the EP template structure.

---

## 1. Generation Workflow — Pre-Generation Dialogue

EP generation is **NOT** a one-shot output. When the agent learns about a new opportunity, it enters a conversational preparation phase with sales before generating.

**流程：**

```
Sales 提到新商机 / Agent 识别到商机信号
    ↓
Agent 表明意图："我来帮你做一个 Engagement Plan"
    ↓
【Pre-Generation Dialogue 对话确认阶段】
    ├── Agent 主动问关键信息：客户是谁？商机背景？关键人？
    ├── Agent 展示已找到的信息（已有 _account/ 数据、网络搜索结果）
    ├── Sales 可能反问 → Agent 作为信息提供者回应
    │   （行业背景、这个人什么风格、竞争对手情况、类似案例...）
    ├── Sales 补充/修正 → Agent 实时调整理解
    └── 关键输入确认后
    ↓
Agent 正式生成 Engagement Plan
```

**Agent 在对话中的双重角色：**

| 角色 | 说明 | 示例 |
|------|------|------|
| **信息收集者** | 收集生成 EP 所需的关键输入 | "这个商机大概什么规模？谁是 decision maker？" |
| **信息提供者** | 回应销售的问题，提供决策支持信息 | "根据网上信息，这家公司刚完成新一轮融资..." |

**关键原则：**

1. **不要死等所有信息才生成** — 关键人物和商机背景确认后即可生成初版，其余标 `[待确认]`
2. **随时根据销售的问题调整** — 对话中发现新情况，立即纳入 EP 的考量
3. **Agent 的回答本身不是 EP** — 对话中的 research 和建议是帮助销售决策的，最终结构化输出才是 EP 文档
4. **多轮对话是正常的** — 不要急于生成，确保关键共识达成

**必确认项（Agent 不应假设的）：**
- 客户名 + 商机名/背景
- 关键人物（至少 1-2 个 key stakeholders）
- 商机大致阶段 / 来源（new logo vs existing customer）

**可推断项（Agent 可以先填、让 sales 确认的）：**
- Stakeholder 的 stance / what they care about（基于 CXO Persona + 历史）
- Win Strategy（基于竞争态势 + 客户背景）
- Engagement Roadmap 建议（基于 stage + 人物布局）
- Estimate & Contingency

---

## 2. Core Rules

### Rule 1: Auto-Create on Any Opportunity
When the agent learns about a new opportunity (from any request — call plan, meeting prep, deal discussion), automatically generate an EP. Never ask permission to start — but run Pre-Gen Dialogue (§1) to confirm key information before generating.

### Rule 2: Opportunity Snapshot — 数据来源

**原则：**
- 永远跟销售确认，不做假设
- BTTROC 和 Opportunity Progression 可以叠加调用，不互斥
- Agent 根据对话上下文灵活判断，不需要死板流程

**判断逻辑：**
```
├── 销售提供了 scorecard / opp record / 完整 deal 信息？
│   └── YES → 调用 Opportunity Progression
├── 销售只给了客户名 + 模糊需求（无 scorecard）？
│   └── YES → 调用 BTTROC（需确认上游 business-insight + solutions-search 已跑）
└── 不确定？
    └── 问一句："这个商机有没有现成的 scorecard 或 opp record？"
```

**Scorecard 自动填写：** Opportunity Progression 不再要求销售必须手动填写 scorecard 才能调用。Agent 可以根据 Call Plan、PMR、对话中获取的信息自动填写/更新 scorecard，然后交由 Opp Progression 判断是否满足 stage exit criteria。销售只需确认 agent 填写的内容是否准确。

**共通要求：**
- 未确认字段标 `[待确认]`
- 所有字段是 living 的，随 PMR 和 engage 演进持续更新
- New Logo vs Existing Customer 影响后续 engagement 节奏

### Rule 3: People First
The EP is organized around **people**, not process. Start with who's involved, then plan how to engage them. The meeting plan flows from the people strategy, 搞定人来搞定事.

### Rule 4: People-Informed (Contact Profiling + CXO Personas)
For **every stakeholder**, invoke **Contact Profiling** for behavioral profile (the **how** layer — communication style, decision patterns, what motivates/triggers them).

For **executive stakeholders** (C-suite / VP), additionally load the matched **CXO Persona** for role-level priorities (the **what** layer — priorities, pain points, KPIs, common objections).

**Context-aware:** Select and emphasize dimensions most relevant to this specific opportunity. Same persona, different opp = different focus. Depth varies by stage. Supplement with web research (company news, LinkedIn, annual reports) to ground persona assumptions in reality.

### Rule 5: Realistic Planning with Scenarios
Always plan with best and worst case scenarios. Account for uncertainty, additional stakeholders surfacing, and meetings that don't achieve their objectives.

### Rule 6: Living Document
The EP is continuously updated. Every Call Plan, Executive Briefing, and PMR feeds back into it. When a CP or EB is generated with attendees or objectives that differ from EP's Next Milestone Detail, those changes are synced back immediately. The Execution Log (EP document Section 3) grows with each interaction.

EP 是 living document，商机推进中信息必然会变化。遇到变更或冲突时，遵循以下原则而非穷举场景：

1. **发现即更新** — CP/EB/PMR 执行中发现与 EP 矛盾的事实（如决策人变了、新对手出现、组织架构调整），agent 立即提示销售确认，确认后回写 EP 对应 Section
2. **标记而非删除** — 失效信息（如离职 stakeholder、被淘汰的竞争对手）标记为失效并注明原因/时间，不直接删除，保留决策上下文供后续复盘
3. **影响范围评估** — 关键变更发生时，agent 主动检查影响范围：哪些下游内容需要同步调整（如决策链变 → Win Strategy / Roadmap / Next Milestone 可能都要动）
4. **销售确认兜底** — Agent 可以建议更新方案，但涉及判断性变更（如 "这个人还重不重要"、"要不要调整 Win Strategy"）必须销售确认后才写入

**核心精神：** Agent 主动发现变化、评估影响、提出建议；销售确认后执行写入。不遗漏、不擅自判断、不丢失历史。

**Change Log 机制：** EP 文件末尾维护一个 `## Change Log` section。每次自动修改 EP 时，追加一行记录：

```markdown
## Change Log
| 时间 | 来源 | 变更摘要 |
|------|------|---------|
| 2026-06-04 14:30 | PMR | 执行日志追加；张三态度 neutral → supportive |
| 2026-06-03 10:00 | OP | 阶段 Qualify → Validate |
| 2026-06-01 16:45 | CP | 新增 attendee 李四（CTO） |
```

规则：
- 每次写入 EP 必须同时追加 Change Log 条目
- 格式：时间（精确到分钟）| 来源 skill 缩写 | 一句话描述变更内容
- 用户手动修改标记来源为 `User`
- Change Log 只追加不删除，超过 50 条时将最早的归档到 `_account/ep-changelog-archive.md`

### Rule 7: Always Review with Sales
After generating or updating, always ask sales to review and revise.

### Rule 8: Never Hallucinate
Do not fabricate stakeholder information, relationship status, or trust levels. If information is unknown, mark as `[待确认]` and ask sales to provide it.

### Rule 9: Stakeholder Engagement Sequence
When creating an EP, proactively ask sales:
1. **"Are there must-meet stakeholders?"** — Distinguish `Must Meet` / `Important` / `Nice to Have`
2. **"Do you have a preferred engagement sequence?"** — e.g., "I want to win CTO first, then approach CFO"

Then combine sales preference with agent analysis to recommend an engagement sequence in the Roadmap:
- **Sales preference** — always respected as primary input
- **Decision role weight** — Economic Buyer > Champion > Influencer
- **Current stance** — consolidate supporters first, or convert skeptics early?
- **Stage exit criteria** (from Opp Progression) — who's most critical for advancing?
- **Dependencies** — e.g., "Need CTO's technical sign-off before CFO will discuss budget"

If the agent's recommended sequence differs from sales preference, **explain the reasoning and let sales decide**. Never override sales judgment silently.

### Rule 10: Stage Review — Opp Progression as Single Source of Truth

EP does NOT determine whether an opportunity should advance to the next sales stage. Only **Opportunity Progression** has the authority to validate stage transitions against AWS Sales Stage Exit Criteria.

**EP 的职责边界：**
- ✅ 消费 stage 信息（从 Opp Progression 获取当前 stage，显示在 Engagement Progress）
- ✅ 收集 evidence（通过 PMR 回流的客户反馈、承诺、动作）
- ✅ 触发 stage review（识别到可能满足推进条件时，调用 Opp Progression）
- ✅ 根据 stage 变化调整 Roadmap、Stakeholder 策略、Estimate
- ❌ 自行判断 stage 是否应该推进
- ❌ 自行对照 exit criteria 做推进决策

**触发时机：** 每次 PMR 回流 EP 后，agent 评估是否需要 stage review：
1. PMR 中出现 stage-relevant evidence（客户承诺、预算确认、技术方案签字等）
2. Agent 判断累积 evidence 可能满足当前 stage exit criteria
3. Agent 根据 Call Plan + PMR + 对话中的信息自动更新 scorecard（销售确认后）
4. → 调用 Opportunity Progression skill，提交更新后的 scorecard + 新 evidence，请求 stage 验证

**核心原则：** 只要 opp 要推进到下一个 stage，都必须通过 Opp Progression 来判定。Agent 可以帮销售填 scorecard、收集 evidence，但推进决策权始终在 Opp Progression。

**Opp Progression 返回结果后，EP 的响应：**
- **Stage 推进** → 更新 Engagement Progress 进度条 + 调整 Roadmap 后续 milestone 的重心 + 更新 Estimate
- **Stage 不推进 + gap 清单** → 在 Roadmap / Next Milestone 中针对性补 gap，调整 stakeholder 策略

**重要区分：**
- Roadmap Milestone 完成标准 = EP 内部自检（"这步做完了吗？"）
- Opp Stage Exit Criteria = Opp Progression 负责验证（"这个商机能往下走吗？"）
- 两者层级不同，不可混淆

### Rule 11: Data Provenance Labeling

  每条写入 EP 的信息必须携带来源标签，使销售能够判断可信度。

  **三级标签体系：**

  | 标签 | 含义 |
  |------|------|
  | `[销售确认]` | 销售直接提供或明确确认的信息 |
  | `[网络搜索]` | 通过公开渠道获取的信息 |
  | `[AI推断]` | Agent 基于上下文分析推断的信息（默认） |

  **标注规则：**

  *   ✅ 三种标签全部显式标注：`[销售确认]`、`[网络搜索]`、`[AI推断]`
  *   ✅ 从上游 skill 传入的信息继承原始标签（如 account-context 标注为 `[网络搜索]`，写入 EP 时保留）
  *   ✅ 对话中销售口头确认的信息，升级为 `[销售确认]`
  *   ✅ PMR 回流的客户原话标 `[销售确认]`，agent 对客户原话的解读标 `[AI推断]`
  *   ❌ 不得在信息流转过程中丢失或升级标签（`[AI推断]` 不可自动变为 `[销售确认]`）

  **语言规则：** 标签随对话语言切换 — 中文对话用 `[销售确认]`/`[AI推断]`/`[网络搜索]`，英文对话用 `[Sales Confirmed]`/`[AI
  Inferred]`/`[Web Search]`。

  **下游影响：** Call Plan、Executive Briefing、PMR 从 EP 读取信息时，必须能看到来源标签并据此决定是否需要二次验证。
  
---

## 3. EP Template

⚠️ **职责分工：** SKILL.md 定义策略和决策逻辑（什么时候做什么、skill 之间怎么协作、fallback 策略）。Reference file 定义每个字段的执行标准（怎么写、写法公式、质量验证、示例）。Agent 生成任何 EP 内容前必须先读 reference file。

**REQUIRED: Load `references/engagement-plan.md` before generating any EP content.** The template has 3 sections:

1. **Opportunity Snapshot + Win Strategy** — Key opp info pulled from Opportunity Progression Skill, plus deal-level win theme
2. **Engagement Plan (搞定人 + 搞定事)** — Per-person analysis (engagement priority, role, stance, what they care about, profiling, what we need, how to win) followed by Engagement Roadmap (full opportunity roadmap from now to close), Next Milestone Detail card (triggers Call Plan), and Estimate & Contingency (with Plan B scenarios)
3. **Execution Log (回滚)** — Actual results from each visit, auto-updated after PMR. Plan adjustments tracked here.

---

## 4. Relationship with Other Skills

**调用顺序指引（跟随模板 Section 顺序）：**

```
┌─────────────────────────────────────────────────────────┐
│ Pre-Generation 阶段（EP 生成前收集信息）                    │
├─────────────────────────────────────────────────────────┤
│ Step 1: Opp Progression 或 BTTROC（二选一，见 Rule 2）    │
│         → 填 Section 1: Opportunity Snapshot             │
│         → 先搞清楚商机是什么                              │
│                                                         │
│ Step 2: Competitive Intelligence + Market Intelligence  │
│         → 填 Section 1: Win Strategy + Key Risks         │
│         → 竞争定位和外部环境判断                           │
│                                                         │
│ Step 3: Account Context                                 │
│         → 填 Section 2: Key Stakeholders 候选人          │
│         → 知道商机后，从 org chart 筛选相关的人            │
│                                                         │
│ Step 4: CXO Personas + Contact Profiling（可并行）       │
│         → 填 Section 2: enrich 每个人的 what + how 层     │
│         → 确定了人之后再做 enrich                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ Post-Generation 阶段（EP 生成后的 lifecycle）             │
├─────────────────────────────────────────────────────────┤
│ EP 触发下游：Call Plan / Executive Briefing              │
│ 回流更新 EP：Post-Meeting Report                        │
│ Stage review：Opp Progression（PMR 后触发）              │
│ 双向 sync：CP/EB 变更 → 回写 EP                         │
└─────────────────────────────────────────────────────────┘
```

**注意：** Step 1-4 不是死板流程。Agent 根据对话上下文灵活判断 — 如果销售一上来就给了完整 stakeholder 信息，可以跳过 Step 3 直接 enrich。核心原则：信息够用就生成，不够再补。

| Skill | Relationship | How to Access | If Unavailable |
|--------|-------------|---------------|----------------|
| **Account Context** | EP 的 Key Stakeholders 起点数据源。提供客户组织架构（org chart）、关系图谱（relationship map）、客户基本面信息。EP 生成前先从 Account Context 获取该客户主要 stakeholders，再判断哪些人与本 opp 相关。 | Invoke `account-context` skill with customer name. 如已有该客户数据则直接复用；如尚无数据，通过与销售对话 + 网络搜索构建初始版本。 | 直接跟销售确认客户组织架构和关键人物。Mark `[待确认]`。 |
| **CXO Personas** | Role-level insights (**What They Care About**) for executive stakeholders. Context-aware — select dimensions relevant to this opp + stage. | Load from `cxo-personas/personas/` using INDEX.md Title Mapping. | General executive priorities based on role. Mark `[待确认]`. |
| **Contact Profiling** | Person-level behavioral profile (**Profiling**) for every stakeholder. Updated through dialogue with sales and after each PMR. | Load if exists; otherwise build through dialogue with sales. | Use sales rep's input. Mark `[待确认]`. |
| **Competitive Intelligence** | 竞争情报数据源。为 Win Strategy 提供 battlecards、竞品对比分析、竞争定位建议。EP 在制定 Win Strategy 和 Roadmap 中的竞争应对节奏时参考其产出。当竞争态势发生变化时（如竞争对手换人、降价、新产品发布），EP 应 re-evaluate Win Strategy。 | Invoke `competitive-intelligence` skill with competitor name(s). 产出为 battlecard（竞品对比、差异化定位、应对话术）。 | 依赖销售口述竞争情况 + 网络搜索获取公开信息。Mark `[销售确认]` or `[网络搜索]`。 |
| **Opportunity Progression** | **Bi-directional.** EP pulls opp snapshot (stage, competitive, value prop, risk). After each PMR, EP submits new evidence back for stage validation — Opp Progression is the **single source of truth** for stage advancement (see Rule 10). EP adjusts Roadmap based on result. | Load opp record if exists. Re-invoke after PMR when stage-relevant evidence is collected. | Fill from sales rep's input. Mark `[待确认]`. |
| **Call Plan** | EP "Next" milestone triggers Call Plan generation. CP pulls context from EP. **CP may sync changes back** if attendees or objectives differ from Next Milestone Detail. | Agent generates CP when Next Milestone is confirmed. | N/A — CP is always generated from EP. |
| **Executive Briefing** | EP context feeds into EB generation. **EB may sync changes back** if attendees or objectives differ. | Agent generates EB when applicable. | N/A. |
| **BTTROC** | 当销售只有客户名/模糊需求（无 scorecard）时，EP 调用 BTTROC 的产出（identified potential opportunity）作为 Opportunity Snapshot 的数据源。提供客户痛点、CXO 对话角度、和 AWS 方案方向。 | BTTROC 需要上游 `business-insight` + `solutions-search` 的产出。如果已有，invoke BTTROC skill；如果上游未跑，提示销售先运行上游分析。 | 直接跟销售对话确认 opp 情况（客户痛点、决策者、初步方案方向）。Mark `[待确认]`。 |
| **Market Intelligence** | 客户外部环境预警（预警卡）。EP 参考其信号调整 Win Strategy、Roadmap 时间节奏、和风险判断。当预警卡发现重大外部变化时，EP 应 re-evaluate 当前策略是否仍然成立。 | Invoke `market-intelligence` skill with customer name. 产出为六层预警卡。 | 依赖销售口述或网络搜索获取外部环境信息。Mark `[网络搜索]` or `[待确认]`。 |
| **Post-Meeting Report** | PMR results roll back into EP Execution Log (EP document Section 3) and update EP document Section 2 (people stance + roadmap status). | Agent reads PMR after each visit and updates EP. | If no PMR filed, prompt sales for verbal debrief. |

---

## 5. Delivery & Quick Summary

### 交付流程

每次 EP 生成或更新后，按以下顺序交付：

```
EP 生成/更新完毕
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

**首次生成时：**

```
📋 Engagement Plan Ready: {Customer} × {Opportunity}

📊 阶段：{Stage}
👥 关键人：{Stakeholder1 (Role)} + {Stakeholder2 (Role)} + ...共{N}人
🎯 Win Strategy：{一句话}
⏭️ Next Milestone：{Milestone描述} — 目标 {Date}
📅 预估时间线：{Close Date / 总周期}

📄 完整文档已生成 → [附件]
```

**更新时（PMR 回流 / CP-EB sync / 销售手动修改后）：**

```
🔄 EP Updated: {Customer} × {Opportunity}

变更摘要：
• {变更1，如：张三态度 neutral → supportive}
• {变更2，如：Roadmap Milestone 2 标记 Done}
• {变更3，如：新增 stakeholder 李四 (CFO)}
⏭️ Next：{下一步行动}

📄 更新后文档 → [附件]
```

---

## 6. Document Output & Storage

### File Naming Convention

| Format | Naming |
|--------|--------|
| PDF | `EP_{Customer}_{Opportunity}.pdf` |
| HTML | `EP_{Customer}_{Opportunity}.html` |
| Word | `EP_{Customer}_{Opportunity}.docx` |

Example: `EP_MinghuaHeavy_AI-Quality-Inspection.pdf`

### Storage Architecture

**首次配置：** Agent 首次与销售互动时，询问本地存储路径：
> "请告诉我你希望文件存放的本地路径（如 ~/Documents/AWS-Sales/）"

**约束：文件存储在销售本地设备，不存放在 Feishu Doc 或其他云文档平台。**

**目录结构（以 Customer → Opportunity 为核心）：**

```
{sales_local_path}/
├── {Customer}/
│   ├── {Opportunity}/
│   │   ├── EP_{Customer}_{Opportunity}.pdf
│   │   ├── EP_{Customer}_{Opportunity}.html
│   │   ├── CP_{Customer}_{Date}_{MilestoneBrief}.pdf
│   │   ├── PMR_{Customer}_{Date}_{MilestoneBrief}.pdf
│   │   ├── EB_{Customer}_{Date}_{MilestoneBrief}.pdf
│   │   └── ...
│   ├── {Opportunity-2}/
│   │   └── ...
│   └── _account/                  ← 客户级共享资料（跨 Opp）
│       ├── org-chart.md
│       ├── account-info.md
│       └── contacts/
│           ├── {name}-{title}.md  ← Contact Profile
│           └── ...
├── {Customer-2}/
│   └── ...
```

**层级逻辑：**

| 层级 | 组织依据 | 理由 |
|------|---------|------|
| L1: Customer | 客户名 | 比 Sales Rep 更稳定，换 AM 不需要搬文件 |
| L2: Opportunity | 商机名 | EP 为核心，所有衍生文档归属同一 Opp |
| L3: Documents | 类型+日期+描述 | 时间线清晰，CP/PMR 一眼配对 |

**关键规则：**
- `_account/` 存放跨商机共享资料（Contact Profile、Org Chart）— Agent 新建 EP 时先扫这里复用已有信息
- CP 和 PMR 使用相同的 `{Date}_{MilestoneBrief}` 后缀，方便配对（会前计划 ↔ 会后报告）
- MilestoneBrief 取自 EP Roadmap milestone 描述精简版（2-4个英文单词，kebab-case）
- EP 是 living document，原地更新；CP/EB/PMR 每次会议一个新文件
- 商机关闭后文件夹保留（历史参考），EP 标记状态为 Closed

**多 Opp 定位逻辑（Agent 内部）：**
- 该客户只有 1 个 active opp → 自动关联
- 多个 active opp → 问销售确认是哪个商机
- EP Roadmap 中有 milestone 的 target_date 匹配 → 自动匹配该 opp
