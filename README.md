![Skill Creator Pro Board 1](docs/images/board-01.svg)

![Skill Creator Pro Board 2](docs/images/board-02.svg)

# skill-creator-pro

**skill-creator-pro** 是一个面向多 Agent 的单包 Skill 自动开发器。它把需求澄清、复用检索、计划生成、开发执行、验证、飞书指南、默认介绍画板，以及 Agent 安装包打包整合进一个技能目录里，目标是让用户只安装这一个技能，就能完成从场景描述到 skill 交付的闭环。

## 这个仓库是什么

这是一个 **skill-only 发布仓库**。

仓库中只保留 skill 本体需要的核心内容：

- `SKILL.md`
- `agents/`
- `assets/`
- `references/`
- `scripts/`
- README 顶部展示用图片

像测试用例、评估过程、验证报告、构建产物这类开发过程文件，不作为公开仓库长期内容保留。

## 适用场景

这个 skill 适合以下场景：

- 想把一个重复流程沉淀成可复用的 skill
- 希望自动完成需求澄清、计划、开发、验证和交付收口
- 需要同时产出飞书指南、介绍画板和安装包
- 不想再依赖多个分散 skill 手动拼接完整交付链路

## 核心能力

- **显式需求澄清**：先输出结构化澄清摘要，而不是直接脑补实现
- **双 Gate 控制**：在 plan 确认和最终验收两个关键节点停下等待确认
- **simple / complex 分流**：根据复杂度自动走轻量或完整链路
- **内置执行骨架**：统一管理 plan / findings / progress / acceptance 状态
- **飞书交付内建**：支持飞书指南、画板、命令计划一体化生成
- **多 Agent 打包**：支持标准 zip 与 Agent 安装包输出

## 仓库结构

```text
.
├── SKILL.md                    # 技能定义与主说明
├── README.md                   # GitHub 首页说明
├── LICENSE                     # MIT License
├── CHANGELOG.md                # 版本与整理记录
├── CONTRIBUTING.md             # 贡献说明
├── agents/                     # Agent interface 配置
├── assets/                     # 模板、样式、图表资源、预览图
├── docs/images/                # README 顶部展示图
├── references/                 # 内置参考技能与规则资料
└── scripts/                    # 澄清、执行、打包、校验、交付脚本
```

## 使用入口

建议先阅读：

- `SKILL.md`
- `references/workflow-playbook.md`
- `references/source-map.md`

## 主要输出产物

这个 skill 在本地运行时可以生成：

- skill 目录
- 飞书使用指南
- 两张介绍画板
- `skill-creator-pro.zip`
- `skill-creator-pro-agent-install.zip`
- `agent-install-manifest.json`

## 注意事项

- 开发前不要跳过澄清与 Gate 1
- 最终交付前不要跳过 Gate 2
- 没有验证证据不要宣称完成
- 本仓库默认不长期跟踪本地生成产物和开发过程文件
