![Skill Creator Pro Board 1](docs/images/board-01.svg)

![Skill Creator Pro Board 2](docs/images/board-02.svg)

# skill-creator-pro

**skill-creator-pro** 是一个面向多 Agent 的单包 Skill 自动开发器。它把需求澄清、复用检索、计划生成、开发执行、测试验证、评审、安全检查、飞书指南、默认介绍画板，以及 Agent 安装包打包整合进一个技能目录里，目标是让用户只安装这一个技能，就能完成从场景描述到 skill 交付的闭环。

## 适用场景

这个项目适合以下场景：

- 想把一个重复流程沉淀成可复用的 skill
- 希望自动完成需求澄清、计划、开发、验证和交付收口
- 需要同时产出飞书指南、介绍画板和安装包
- 不想再依赖多个分散 skill 手动拼接完整交付链路

## 核心能力

- **显式需求澄清**：先输出结构化澄清摘要，而不是直接脑补实现
- **双 Gate 控制**：在 plan 确认和最终验收两个关键节点停下等待确认
- **simple / complex 分流**：根据复杂度自动走轻量或完整链路
- **内置执行骨架**：统一管理 `task_plan`、`findings`、`progress`、`execution-state`
- **飞书交付内建**：支持飞书指南、画板、命令计划一体化生成
- **多 Agent 打包**：支持标准 zip 与 Agent 安装包输出
- **可验证交付**：内置测试、review、安全摘要与 bundle 校验

## 快速开始

### 1. 浏览技能说明

核心说明在：

- `SKILL.md`
- `references/workflow-playbook.md`
- `references/source-map.md`

### 2. 本地验证

```bash
python3 -m pytest -q
python3 scripts/verify_bundle.py .
```

### 3. 生成产物

常见输出包括：

- `dist/skill-creator-pro.zip`
- `dist/skill-creator-pro-agent-install.zip`
- `dist/agent-install-manifest.json`

## 仓库结构

```text
.
├── SKILL.md                    # 技能定义与主说明
├── README.md                   # GitHub 首页说明
├── agents/                     # OpenAI / agent interface 配置
├── assets/                     # 模板、样式、图表资源、预览图
├── docs/                       # GitHub 文档与图片
├── evals/                      # 示例与评估输入输出
├── references/                 # 内置参考技能与规则资料
├── scripts/                    # 澄清、执行、打包、校验、交付脚本
└── tests/                      # 自动化测试
```

## 关键模块

- **Clarification Engine**：显式需求澄清
- **Execution Spine**：Gate 1 / Gate 2 + verify 主链路
- **Lark Delivery**：飞书文档与请求封装
- **Chart Delivery**：默认介绍板 + 轻量图表流水线
- **Packaging**：`quick_validate` / `package_skill` / `package_agent_install`

## 公开仓库说明

这个 GitHub 仓库以**源码和说明**为主，不长期提交本地生成产物，例如：

- `dist/`
- `reports/`
- `.pytest_cache/`
- `.DS_Store`

如果你在本地运行打包或验证，这些目录会被重新生成，但不会作为公开源码仓库的主要内容持续跟踪。

## 主要输出产物

项目最终可生成的交付物包括：

- skill 目录
- 飞书使用指南
- 两张介绍画板
- test / review / security 摘要
- `skill-creator-pro.zip`
- `skill-creator-pro-agent-install.zip`
- `agent-install-manifest.json`

## 注意事项

- 开发前不要跳过澄清与 Gate 1
- 最终交付前不要跳过 Gate 2
- 没有验证证据不要宣称完成
- 公开仓库建议只保留源码、文档、测试和必要示例
