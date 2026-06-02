## 当前技能实际集成了哪些能力

为了让用户只安装这一个 skill 就能走完整条交付链路，当前版本已经把以下关键能力内聚到同一套流程里：

- **需求澄清 / 设计前置**：吸收 `brainstorming` 的核心思路，先确认目标、约束、验收标准，再进入开发。
- **计划 / 执行 / 验证骨架**：吸收 `superpowers` 与 `planning-with-files` 的方法，维护 `task_plan`、`findings`、`progress`，并保留 Gate 1 / Gate 2。
- **Skill 开发与交付**：吸收 `skill-creator` 与 `find-skills` 的能力，用于结构生成、复用判断、校验与 Agent 安装包打包。
- **飞书文档 / 画板 / 图表落地**：吸收 `lark-doc`、`lark-whiteboard`、`design-lark-chart` 的核心工作流，用于指南生成、画板插入与图表交付。
- **Lark 深水区补位**：吸收 `lark-openapi-explorer` 与 `lark-skill-maker` 的能力，在现成 CLI / skill 不够用时继续向原生 OpenAPI 和新 skill 规格扩展。

这也是当前 skill 与“临时拼装多个 skill”的根本差异：**它不是简单引用外部提示词，而是把高频能力收束进一个面向交付的统一主链路里。**
