<div align="center">

# skill-creator-pro

**把一句简单的用户输入，推进成一条完整的 skill 开发与交付链。**

一个面向多 Agent 的单包 Skill 自动开发器：把场景需求串成从**交互式需求澄清**、**计划确认**、**TDD / verify 驱动开发**、**Lark / OpenAPI 补位**、**安全与评审收口**，到**飞书指南、介绍画板和安装包输出**的闭环流程。

![workflow overview](docs/images/workflow-overview.png)

<p>
  <img alt="Skill" src="https://img.shields.io/badge/Skill-skill--creator--pro-111827?style=for-the-badge">
  <img alt="Workflow" src="https://img.shields.io/badge/Workflow-Clarify%20%E2%86%92%20Plan%20%E2%86%92%20Build%20%E2%86%92%20Verify%20%E2%86%92%20Deliver-2563eb?style=for-the-badge">
  <img alt="Delivery" src="https://img.shields.io/badge/Delivery-Docs%20%2B%20Board%20%2B%20Zip-16a34a?style=for-the-badge">
</p>

</div>

---

## 为什么它不是普通脚手架

很多 skill 工具解决的是某一个局部问题：生成目录、写一段提示词、封装一个脚本，或者最后做一次打包。**skill-creator-pro** 的目标不是再多一个脚手架，而是把需求理解、计划、开发、验证、审查和交付拉成一条真正可控的主链路。

![why skill creator pro](docs/images/why-skill-creator-pro.png)

## 它把哪些环节统一起来

- 从一个简单用户输入开始理解任务
- 进入结构化、可见的需求澄清
- 判断是否可复用已有 skill 或模式
- 生成计划，并通过 Gate 1 停下来确认
- 用 TDD / verify-first 思路推进开发
- 在需要时接入 Lark API / OpenAPI 查询与补位
- 生成 review / security 摘要做交付前审查
- 通过 Gate 2 完成最终验收
- 输出飞书指南、介绍画板和 Agent 安装包

## 一条完整主链路：从输入到交付

```text
用户描述场景
→ 运行内置澄清引擎
→ 检索已有 skill / 模式
→ 判断 simple / complex
→ 生成 task_plan / findings / progress
→ Gate 1：用户确认计划
→ 开发、测试、评审、安全检查
→ Gate 2：用户验收结果
→ 生成飞书文档、介绍画板与图表
→ 打包 Agent 兼容安装包
```

| 阶段 | 它会做什么 | 关键产物 |
| --- | --- | --- |
| Clarification Engine | 把模糊输入转成结构化澄清摘要 | `clarification-summary.md` |
| Execution Spine | 维护 plan → Gate 1 → develop / verify → Gate 2 → deliver 主骨架 | `task_plan.md`、`findings.md`、`progress.md` |
| TDD / Verify-first | 强调验证证据，而不是“生成了代码就算完成” | test / verify summary |
| Lark Delivery | 生成飞书指南、文档请求、画板请求与命令计划 | guide、board、command plan |
| Review / Security | 把评审与安全摘要纳入最终交付 | review / security summary |
| Packaging | 输出标准 zip 与 Agent 安装包 | `dist/<skill-name>.zip` |

## 实战 Demo

### Demo 1：信息完整时快速进入计划确认

当用户已经给出比较完整的场景、目标和约束时，技能会快速生成计划、产物结构与验证摘要，并进入 Gate 1 确认。

![demo rich context plan](docs/images/demo-rich-context-plan.png)

### Demo 2：信息不完整时先澄清，再交付飞书文档与画板

当输入存在缺口时，技能会先补齐关键决策；确认后再继续推进开发、验证、飞书指南和画板交付。

![demo lark doc whiteboard](docs/images/demo-lark-doc-whiteboard.png)

## 图表与画板能力画廊

`skill-creator-pro` 内置轻量图表与画板交付链路，可为最终技能生成介绍画板、流程图、架构图、时序图、里程碑、泳道图等视觉产物。

| 业务架构 | 系统架构 | 流程图 |
| --- | --- | --- |
| ![business architecture](assets/previews/business-architecture.png) | ![system architecture](assets/previews/system-architecture.png) | ![flowchart](assets/previews/flowchart.png) |

| 复杂泳道 | 时序图 | 状态机 |
| --- | --- | --- |
| ![complex swimlane](assets/previews/complex-swimlane.png) | ![sequence](assets/previews/sequence.png) | ![state machine](assets/previews/state-machine.png) |

| 甘特图 | 里程碑 | 组织架构 |
| --- | --- | --- |
| ![gantt](assets/previews/gantt.png) | ![milestone](assets/previews/milestone.png) | ![org chart](assets/previews/org-chart.png) |

| 矩阵象限 | 漏斗 | 链路架构 |
| --- | --- | --- |
| ![matrix quadrant](assets/previews/matrix-quadrant.png) | ![funnel](assets/previews/funnel.png) | ![link architecture](assets/previews/link-architecture.png) |

## 它适合谁

这个项目特别适合：

- 想把一个完整流程沉淀成 skill，而不是只写一次性脚本的人
- 想把“需求 → 开发 → 验证 → 文档 → 打包”串成闭环的人
- 希望最终把 skill 交付给别人直接使用的人
- 需要飞书 / Lark 集成能力的人
- 需要更强交付纪律，而不是只要一个目录模板的人

## 它不适合谁

如果你只想临时写一个一次性脚本、生成一个最小目录结构就结束，或者不需要交付文档、画板、打包和审查，那这个项目可能会比你的当前需求更完整，也更重一些。

## 如何开始使用

建议按这个顺序开始：

1. 阅读 `SKILL.md`
2. 查看 `references/workflow-playbook.md` 理解执行主链路
3. 查看 `references/source-map.md` 理解模块来源与拼装关系
4. 用你的场景描述触发这个 skill
5. 完成需求澄清、Gate 1 计划确认、开发验证和 Gate 2 验收
6. 输出 skill、飞书指南、画板与安装包

## 仓库里包含什么

这是一个 **skill-only 发布仓库**，公开仓库只保留 skill 本体相关内容：

```text
.
├── SKILL.md              # 技能入口：frontmatter + 主工作流
├── README.md             # GitHub 项目页
├── LICENSE               # 开源许可证
├── CHANGELOG.md          # 版本变更记录
├── CONTRIBUTING.md       # 贡献说明
├── agents/               # Agent 兼容配置
├── assets/               # 模板、图表样式、预览图与原始配置
├── docs/images/          # README 项目页图片与 Demo 截图
├── references/           # 工作流、质量门、飞书、图表、兼容性参考
└── scripts/              # 澄清、计划、文档、画板、打包、校验脚本
```

## 快速命令

### 校验技能目录

```bash
python scripts/quick_validate.py .
```

### 生成澄清摘要

```bash
python scripts/render_clarification_summary.py spec.json out/
```

### 生成飞书图文交付包

```bash
python scripts/build_feishu_delivery_bundle.py spec.json out/
```

### 打包 Agent 安装包

```bash
python scripts/package_skill.py .
```

## 公开仓库不长期保留什么

为了让仓库更像“可直接使用的 skill 项目”，而不是“开发现场”，以下内容不作为公开仓库长期保留：

- 测试用例
- eval 过程文件
- 验证报告
- 构建产物
- 本地缓存文件

## 注意事项

- 开发前不要跳过澄清与 Gate 1
- 最终交付前不要跳过 Gate 2
- 没有验证证据不要宣称完成
- 本仓库默认不长期跟踪本地生成产物和开发过程文件
