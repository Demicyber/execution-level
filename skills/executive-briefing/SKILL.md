---
name: executive-briefing
description: >
  Briefing document to prepare AWS executives for customer interactions — covers EBC visits
  and any scenario where AWS VP+ joins a customer meeting.
  Use whenever sales mentions EBC, executive visit, or a VP/SVP/GM joining a meeting,
  "EBC", "高管简报", "高管拜访", "VP要去见客户", "高管要去客户那边需要准备什么",
  or any hint of executive participation — even without saying "executive briefing".
user_locked: true
---

# Executive Briefing Skill

---

## Execution Discipline

STOP. Read this entire skill file before executing.
This skill has a mandatory reference file that defines template structure and writing standards.
Do NOT begin the Pre-Generation Dialogue until you understand all rules and the EB template structure.

---

## 1. Generation Workflow — Pre-Generation Dialogue

EB generation is **NOT** a one-shot output. EBC/高管拜访准备通常涉及多方协调，agent 和 sales 在生成前需要对话确认。

**流程：**

```
Sales 请求 EBC prep / EP Next Milestone 标记为高管拜访
    ↓
Agent 展示已知信息（从 EP pull 的 + 网络搜索）
    ↓
【Pre-Generation Dialogue 对话确认阶段】
    ├── Agent 展示已知：EP 中的参会人、商机背景、竞争态势
    ├── Agent 提出待确认项：具体日期？AWS 方谁来？会议目的？sales 想要什么结果？
    ├── Sales 可能反问 → Agent 作为信息提供者回应
    │   （这位高管什么风格？上次见面聊了什么？有什么 sensitivity？）
    ├── Sales 补充/修正 → Agent 实时调整理解
    └── 关键输入确认后
    ↓
Agent 正式生成 Executive Briefing
```

**Agent 在对话中的双重角色：**

| 角色 | 说明 | 示例 |
|------|------|------|
| **信息收集者** | 确认 EB 所需的关键输入 | "AWS 方最终谁参加？会议核心目标是什么？" |
| **信息提供者** | 回应 sales 的问题，提供高管背景信息 | "根据 LinkedIn，这位 CEO 去年刚从 XX 公司过来..." |

**关键原则：**

1. **不要死等所有信息才生成** — 参会人和会议目标确认后即可生成初版，其余标 `[待确认]`
2. **随时根据销售的问题调整** — 对话中发现新信息立即纳入
3. **EBC 级别的 research 深度更高** — AWS 高管需要准确、当前的信息，agent 应主动做更深入的 web research
4. **多轮对话是正常的** — 不要急于生成，确保关键共识达成
5. **对话收敛判断** — 满足以下任一条件即可进入生成：
   - 必确认项（下方列表）全部确认
   - 销售明确说"可以了/开始生成/够了"
   - 连续 2 轮 agent 提问后销售没有新增信息（说明已掏空）
   - Agent 已问满 3 轮（每轮 max 3 个问题），仍有缺失 → 先生成初版，缺失项标 `[待确认]`

**必确认项（Agent 不应假设的）：**
- 会议日期/时间/形式/地点
- 客户方最终参会人名单
- AWS 方参会高管
- 会议的核心目标（sales 想达成什么）
- 谁发起的这次会议，为什么

**可推断项（Agent 可以先填、让 sales 确认的）：**
- 客户参会人的背景和风格（基于 CXO Persona + Contact Profiling + web research）
- Talking points（基于商机背景 + 会议目标）
- Account background（基于 EP + 公开信息）
- Competitive intelligence

---

## 2. Core Rules

### Rule 1: Always Build the Bigger Picture
After generating an Executive Briefing, check if an EP exists. If not, auto-create one.

**EP 不存在时：** 不阻塞 EB 生成。Agent 基于当前已知信息快速创建 skeleton EP（关键字段标注 `[TBC]`），从中拉取 context 后继续生成 EB。会后通过 PMR 逐步补全 EP。

### Rule 2: People-Informed (Contact Profiling + CXO Personas)
For **every customer attendee**, invoke **Contact Profiling** for behavioral profile (the **how** layer). For **executive attendees** (C-suite / VP), additionally load the matched **CXO Persona** for role-level priorities (the **what** layer).

**Context-aware:** Select dimensions most relevant to this meeting's objectives. EBC-level meetings need deeper persona insights (CEO communication preferences, strategic priorities, known sensitivities). Supplement with web research — AWS executives need current, verified information.

For Manager/IC attendees, use Contact Profiling only (no CXO Persona).

### Rule 3: INTERNAL ONLY
Mark the document clearly as **INTERNAL USE ONLY — AWS Confidential**. Never shared with customers.

### Rule 4: Always Review with Sales
After generating, always ask sales to review and revise.

### Rule 5: Never Hallucinate
Many fields require information the agent cannot independently verify (relationship history, internal politics, customer sentiment, AWS spend details). For unverifiable information:
1. Mark with `[待确认]` and explain what's needed
2. Proactively ask sales to provide or confirm
3. Explain why it matters

### Rule 6: Sync Back to EP
**Only when the EP pre-existed** (not just auto-created by this EB run). After generating, compare attendees and objectives with EP's Next Milestone Detail. If there are differences:
1. **New attendees** → Add to EP Key Stakeholders; mark unknown fields as `[待确认]`
2. **Attendee changes** → Update EP Next Milestone Detail
3. **Objective changes** → Update EP Engagement Roadmap
4. Add `[Updated: YYYY-MM-DD]` timestamp next to every changed field
5. Notify sales: "EP has been updated to reflect the Executive Briefing changes — please review."

**反向：EP 变更后对已生成 EB 的影响**
EB 不是 living document（每次会议一个新文件），但如果 EP 在 EB 生成后、会议发生前出现关键变更（如新增/变更参会人、Win Strategy 调整、竞争态势变化），agent 应：
1. 主动提示销售："{变更内容} 可能影响已生成的 EB，是否需要更新？"
2. 销售确认后，更新 EB 对应 Section 并标注 `[Updated: YYYY-MM-DD]`
3. 如果不更新，至少确保销售 aware of the change（避免高管拿着过时信息去开会）

### Rule 7: Data Provenance Labeling
Every piece of information must carry a provenance label so sales knows the confidence level.

| Label | Meaning | Sales Action |
|-------|---------|--------------|
| `[销售确认]` | 销售直接提供或明确确认的信息 | 可直接使用 |
| `[AI推断]` | Agent 根据上下文分析推断的信息 | 建议核实 |
| `[网络搜索]` | 通过网络搜索获取的公开信息 | 注意时效 |

**标注粒度：** 每条独立可判断真伪的断言。
**显示规则：** 只显式标出 `[销售确认]` 和 `[网络搜索]`，无标注 = AI推断（默认）。
**升级机制：** 销售确认后 → 升级为 `[销售确认]`。

---

## 3. EB Template

⚠️ **SKILL.md vs references/executive-briefing.md 的职责边界：**
- **SKILL.md**（本文件）= 规则、流程、依赖关系、调用逻辑 — agent 的行为指令
- **references/executive-briefing.md** = 模板结构、写作标准、AGENT GUIDANCE — 生成内容时的格式和质量标准

Agent 生成 EB 时先读 SKILL.md 确认流程和规则，再读 references 获取模板结构和写作指导。两者不重复定义同一件事。

**REQUIRED: Load `references/executive-briefing.md` before generating any EB content.** The template has 5 sections:

1. **Meeting Logistics** — Date/time/format, AWS attendees, who requested and why, key contacts
2. **Customer Attendee Background** — Per-attendee detail (5 dimensions) + Company Profile (5 dimensions)
3. **🎯 Meeting Objectives** — Success definition, strategic alignment, per-objective detail (objective, context, talking points, asks), Anticipated Concerns (Acknowledge-Pivot-Elevate + Landmines), Proposed Next Steps (3-tier: ideal / acceptable / minimum)
4. **AWS Account Background** — Geo/segment, spend, PPA status, account summary (5 dimensions)
5. **Appendix** — Previous meeting notes, relevant customer success stories, competitive intelligence detail

---

## 4. Attendee Background Dimensions

For each customer attendee, cover in one focused paragraph:

1. **Position & Tenure** — Current role, reporting line, years at company, relevant career moves
2. **Communication Style** — Direct & pragmatic, or conservative & indirect? Integrate Contact Profiling + CXO Persona (for execs). Sales input takes priority.
3. **Decision Role & Business Focus** — Level of decision authority; current focus areas. For execs, integrate persona's Priorities and KPIs.
4. **Attitude Toward AWS** — Overall stance; known concerns or sensitivities; topics to avoid. For execs, integrate persona's Pain Points and common objections.
5. **Collaboration History** — Highlights (successful projects); past friction points.

---

## 5. Company Profile Dimensions

Cover in one focused paragraph:

1. **Positioning & Industry Standing** — What the company does and where it ranks
2. **Scale & Impact** — Annual revenue, user base, market share
3. **Technology Profile** — AI adoption stage, cloud usage, in-house vs. third-party
4. **Strategic Priorities & Key Events** — Current and upcoming strategic focus; major events in past/next 12 months
5. **Recent Leadership Changes** — C-suite or board changes in past 6 months

---



## 6. Delivery & Quick Summary

### 交付流程

每次 Executive Briefing 生成后，按以下顺序交付：

```
EB 生成完毕
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
📋 Executive Briefing Ready: {Customer} × {Date}

📅 会议：{Date} {Format} {Location}
👤 客户方：{CustomerExec1 (Role)} + {CustomerExec2 (Role)}
🏢 AWS 方：{AWSExec (Role)} + {SA/AM}
🎯 核心 Ask：{最重要的一个 ask，一句话}
⚠️ Landmine：{最需要注意的 sensitivity}

📄 完整文档已生成 → [附件]
```

---

## 7. Document Output & Storage

### File Naming Convention

| Format | Naming |
|--------|--------|
| PDF | `EB_{Customer}_{Date}_{MilestoneBrief}.pdf` |
| HTML | `EB_{Customer}_{Date}_{MilestoneBrief}.html` |
| Word | `EB_{Customer}_{Date}_{MilestoneBrief}.docx` |

Example: `EB_MinghuaHeavy_2026-06-10_EBC-VP-Visit.pdf`

MilestoneBrief = EP Roadmap milestone 描述精简版（2-4个英文单词，kebab-case）。EB 和对应 PMR 使用相同的 `{Date}_{MilestoneBrief}` 后缀，方便配对。

### Storage Architecture

**首次配置：** Agent 首次与销售互动时，询问本地存储路径。

**约束：文件存储在销售本地设备，不存放在 Feishu Doc 或其他云文档平台。**

**目录结构（以 Customer → Opportunity 为核心）：**

```
{sales_local_path}/
├── {Customer}/
│   ├── {Opportunity}/
│   │   ├── EP_{Customer}_{Opportunity}.pdf
│   │   ├── EB_{Customer}_{Date}_{MilestoneBrief}.pdf   ← Executive Briefing
│   │   ├── PMR_{Customer}_{Date}_{MilestoneBrief}.pdf
│   │   └── ...
│   └── _account/              ← 客户级共享资料（跨 Opp）
│       ├── org-chart.md
│       └── contacts/
```

**关键规则：**
- EB 存放在对应 Opportunity 文件夹下（跟 EP 同级）
- 每次 EBC/高管拜访产生一个新 EB 文件（不是 living document）
- Agent 通过 EP → Roadmap → Next Milestone 定位当前 Opp
- 多 Opp 定位：1个 active opp → 自动关联；多个 → 问销售确认

详细目录结构规范见 engagement-plan SKILL.md（主定义文档）。
