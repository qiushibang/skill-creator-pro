---
name: skill-creator-pro
description: 适配多 Agent 的单包 Skill 自动开发器。当用户想把一个重复场景沉淀成 skill、想自动完成需求澄清、计划、开发、测试、评审、Agent 安装包打包、以及飞书图文指南生成时，必须使用本技能。本技能内置澄清、执行、飞书文档、默认画板与打包能力，不依赖额外安装 brainstorming、superpowers、lark 或 design-lark-chart 等技能。
---

# Skill Creator Pro

这是一个**单包、自足、复制优先**的 Skill 自动开发器。它把需求澄清、已有 skill 检索、计划生成、开发执行、TDD/verify、评审、飞书文档、默认画板、图表产出、Agent 安装包打包整合进一个技能目录里，目标是让用户只安装这一个技能就能完成从场景描述到 skill 交付的闭环。

## 内置模块

本技能不是在运行时“借用外部 skill 名称”，而是直接把必要核心能力内置到当前目录：

1. **Clarification Engine（内置澄清引擎）**
   - 负责在 plan 之前输出显式的需求澄清摘要
   - 使用 `scripts/render_clarification_summary.py`
   - 配套模板：`assets/templates/clarification-summary.md`
2. **Execution Spine（内置执行骨架）**
   - 负责 plan → gate 1 → develop/verify → gate 2 → deliver 的主链路
   - 主要规则见 `references/workflow-playbook.md`
   - 本地脚本：`scripts/init_execution_state.py`、`scripts/advance_execution_gate.py`、`scripts/build_acceptance_packet.py`
3. **Lark Delivery（内置飞书交付子系统）**
   - 负责生成飞书指南、action plan、command plan
   - 使用 `scripts/render_lark_guide.py`、`scripts/render_lark_doc_commands.py`
   - 本地包装：`scripts/lark_vendor/build_doc_request.py`、`scripts/lark_vendor/build_whiteboard_requests.py`
   - OpenAPI 探索包装：`scripts/lark_vendor/explore_openapi_contract.py`
   - Lark Skill 规格包装：`scripts/lark_vendor/build_lark_skill_spec.py`
4. **Chart Delivery（内置图表/画板子系统）**
   - 负责轻量文档图表与默认介绍画板
   - 使用 `scripts/render_doc_chart.py`、`scripts/render_skill_overview_board.py`
   - 本地图表流水线：`scripts/chart_pipeline/run_chart_pipeline.py`、`scripts/chart_pipeline/build_quality_gate_report.py`
5. **Feishu Delivery Bundle（内置最终图文交付编排）**
   - 一次性产出 guide + board + commands
   - 使用 `scripts/build_feishu_delivery_bundle.py`

## 核心原则

1. **复制优先**：先看 `references/source-map.md` 里记录的来源，再决定沿用、改写还是拼装；不要凭空编造主流程。
2. **两个确认闸门**：必须在 `plan` 完成后等待第一次确认；必须在测试/评审摘要完成后等待第二次验收。
3. **simple / complex 分流**：目标单一、资源少、无外部集成 → simple；多资源、多规则、Lark/OpenAPI、图表/文档重交付 → complex。
4. **未验证不得宣称完成**：没有新鲜验证证据，不能声称“开发完成”“测试通过”“文档已生成”。
5. **Agent 收口**：最终必须输出合规 skill 目录与 zip 包，不直接上传。

## 工作流总览

```text
用户描述场景
→ 运行内置澄清引擎
→ 检索已有 skill/模式
→ 判断 simple / complex
→ 生成 plan / findings / progress
→ 闸门 1：请用户确认 plan
→ 按内置执行骨架自动开发 skill
→ 跑测试 / verify / review / security summary
→ 闸门 2：请用户验收结果
→ 生成飞书文档、默认介绍画板与必要图表
→ 打包 Agent 兼容安装包
```

## 执行步骤

### 1. 需求澄清
- 必须先运行 `scripts/render_clarification_summary.py <spec.json> <out_dir>` 生成显式澄清摘要。
- 摘要中至少要包含：目标、目标用户、输入、输出、依赖、验收标准、约束、当前假设、待确认项。
- 即使用户已经给了较清楚的信息，也不能静默跳过澄清步骤；最多只是在摘要里把 `待确认项` 标为 `暂无`。
- 如仍缺关键决策，再补 1~3 个高价值问题；否则再进入 `task_plan.md` 初稿。

### 2. 检索与复用
- 先检查是否已有现成 skill 或近似工作流可直接改造。
- 优先复用现有目录、脚本、模板、references、assets。
- 若发现适合的来源，记录到 `references/source-map.md`，说明是直接复制、局部改写还是拼装整合。

### 3. simple / complex 分流
- **simple skill**：单一用途、脚本和 references 少、无需复杂外部集成。可走轻量计划与轻量测试。
- **complex skill**：多阶段、多资源、Lark/OpenAPI、文档/图表型交付、或要求高质量审查。必须走完整链路。
- 无法判断时，按 complex 处理更安全。

### 4. 计划文件
创建并维护：
- `execution-state.json`
- `gate_1-summary.md` / `gate_2-summary.md`
- `task_plan.md`
- `findings.md`
- `progress.md`

默认使用 `assets/templates/` 里的模板，结合当前任务填充。

### 5. 闸门 1：plan 确认
输出 plan 后必须停下，明确告诉用户：
- 计划已生成
- 主要阶段与交付物
- 等待用户确认或修改
- 优先用 `scripts/advance_execution_gate.py <workspace> gate_1 ...` 生成本地闸门摘要

未获得确认前，不进入正式开发。

### 6. 开发与验证
确认后再进入开发：
- 使用 test-first 思路写最小可验证案例
- 开发过程中持续更新 findings/progress
- 跑结构校验、脚本校验、示例验证、打包验证
- 对复杂 skill 补充 review summary 和 security summary
- 所有执行链路默认走本技能内置脚本与模板，不要求再额外安装 brainstorming、superpowers、lark-doc、design-lark-chart 等技能。

### 7. 闸门 2：最终验收
把以下结果汇总给用户确认：
- skill 目录
- 关键文件说明
- test summary
- review / security summary
- zip 包路径
- 优先用 `scripts/build_acceptance_packet.py <workspace>` 生成验收包，再用 `scripts/advance_execution_gate.py <workspace> gate_2 ...` 输出闸门摘要

只有用户确认无异议，才进入最终文档阶段。

### 8. 飞书图文指南
验收通过后：
- 优先使用 `scripts/render_lark_guide.py` 基于结构化 spec 生成飞书指南 Markdown、create payload、规范化 spec、以及 Feishu action plan。
- 默认根据 `guide-spec.normalized.json` 自动生成一张 `skill-overview-board`，用于帮助最终使用者快速理解技能的触发方式、推进流程与最终交付物。
- 默认将这张介绍画板插入到飞书文档“技能简介”后面，不需要额外安装 `design-lark-chart` 等外部 skill。
- 如果要一次性生成完整图文交付，优先运行 `scripts/build_feishu_delivery_bundle.py <spec.json> <out_dir>`，它会统一产出 guide / board / command plan。
- 如需二次增量写入或分段更新，优先执行 `feishu-action-plan.json` 中的 `update.chunks`，并遵循 `references/lark-guide-authoring.md` 里的 create/update 策略。
- 如需进一步进入“真实落地前一跳”，使用 `scripts/render_lark_doc_commands.py` 把 action plan 转成可执行的 `lark-cli docs +create / +update` 命令计划。
- 若要本地化描述 Lark 执行请求，使用 `scripts/lark_vendor/build_doc_request.py` 与 `scripts/lark_vendor/build_whiteboard_requests.py` 生成 create/update/whiteboard 的请求载荷。
- 若当前需求超出已封装命令范围，使用 `scripts/lark_vendor/explore_openapi_contract.py <spec.json> <out_dir>` 生成 OpenAPI exploration contract 与 `lark-cli api` 调用计划，不再只停留在参考文档级集成。
- 若目标是直接沉淀新的 Lark 自动化 skill，使用 `scripts/lark_vendor/build_lark_skill_spec.py <spec.json> <out_dir>` 生成本地 `SKILL.md`、命令计划和规格化 JSON，不再只停留在 `lark-skill-maker` 文档引用。
- 如果说明更适合可视化，先用 `scripts/render_doc_chart.py` 生成轻量 Mermaid 流程图/结构图，再按 `references/doc-chart-pipeline.md` 决定是否同步到飞书。
- 默认介绍画板面向最终使用者，重点展示：怎么触发、怎么推进、最终交付物。
- 图表或画板未过质量门时，降级为纯文字文档，但必须说明降级原因；不得把空白板视为成功。
- 如果进入更完整的本地 pipeline，使用 `scripts/chart_pipeline/run_chart_pipeline.py <spec.json> <out_dir>` 产出 Normalize → Select → Plan → Layout → Render → StaticCheck → VQA → Deliver 的阶段文件，再用 `scripts/chart_pipeline/build_quality_gate_report.py` 汇总质量门。

### 9. Agent 安装包打包
- 使用 `scripts/package_skill.py` 打包
- 必须先通过 `scripts/quick_validate.py`
- 打包结果输出到 `dist/`

## 必需产物

默认至少输出：
- skill 目录
- `clarification-summary.md`
- `execution-state.json`
- `task_plan.md` / `findings.md` / `progress.md`
- `reports/test-summary.md`
- `reports/review-summary.md`
- `reports/security-summary.md`
- 飞书指南链接或本地草稿
- `dist/<skill-name>.zip`

## 参考文件何时读取

- `references/source-map.md`：每次修改主流程前必读
- `references/workflow-playbook.md`：每次执行完整自动开发链路时必读
- `assets/templates/clarification-summary.md`：需求澄清摘要模板
- `references/agent-compatibility.md`：打包前必读
- `references/lark-guide-authoring.md`：生成飞书指南前必读
- `references/doc-chart-pipeline.md`：需要图文化说明时必读
- `assets/templates/guide/feishu-guide-template.md`：飞书指南正文模板
- `assets/templates/chart/flowchart.mmd.tpl`：轻量流程图模板
- `references/review-gates.md`：生成 review / security summary 前必读

## 禁止事项

- 禁止不看来源就重写现有流程
- 禁止跳过两个确认闸门
- 禁止没验证就声称完成
- 禁止把图表预览当作飞书落地产物的替代证据
- 禁止输出不合规 frontmatter 或损坏 zip
