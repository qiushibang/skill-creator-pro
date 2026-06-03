# skill-creator-pro

把一句简单的用户输入，推进成一条完整的 skill 开发与交付链。

**skill-creator-pro** 不是一个只会“生成 skill 骨架”的工具，而是一个面向多 Agent 的单包 Skill 自动开发器。它会把一个场景需求，串成从**交互式需求澄清**、**计划确认**、**TDD / verify 驱动开发**、**Lark / OpenAPI 补位**、**安全与评审收口**，到**飞书指南、介绍画板和安装包输出**的闭环流程。

> 如果你想要的不是“再多一个脚手架”，而是一条真正能从输入走到交付的 skill 生产链，这个项目就是为这个目标设计的。

## 它的特色不只是“能做 skill”

很多 skill 工具解决的是某一个局部问题，例如：

- 只生成目录结构
- 只写一段提示词
- 只做一次性脚本封装
- 只负责打包或只负责文档

**skill-creator-pro** 的不同点在于：它把这些原本分散的环节真正串成了一条主链路。

也就是说，它的特色不是“会其中一步”，而是会把下面这些步骤统一起来：

- 从一个简单用户输入开始理解任务
- 进入结构化、可见的需求澄清
- 判断是否可复用已有 skill 或模式
- 生成计划，并通过 Gate 1 停下来确认
- 用 TDD / verify-first 思路推进开发
- 在需要时接入 Lark API / OpenAPI 查询与补位
- 在需要时使用 lark-skill-creator 能力沉淀 skill 规格
- 生成 review / security 摘要做交付前审查
- 通过 Gate 2 完成最终验收
- 最后输出飞书指南、介绍画板和 Agent 安装包

## 一条完整主链路：从输入到交付

你可以把这个项目理解成一个面向 skill 交付的“端到端编排器”。

典型流程如下：

### 1. 从简单用户输入开始
用户不需要一开始就给出完整规格，往往只需要先描述：

- 想解决什么问题
- 想沉淀什么流程
- 希望最终交付成什么样的 skill

### 2. 进入交互式需求澄清
项目不会直接跳进实现，而是先产出结构化澄清摘要，明确：

- 目标
- 输入 / 输出
- 目标用户
- 依赖
- 验收标准
- 当前假设
- 待确认项

### 3. 检查复用路径
在正式开发前，会先检查：

- 是否已有现成 skill 可复用
- 是否已有近似流程可改造
- 是否应走 simple 还是 complex 路线

### 4. 生成计划，并在 Gate 1 停下
项目不会一上来就“自动做到底”，而是会先生成计划与执行骨架，并在 **Gate 1** 等待确认，确保范围、阶段和交付物都正确。

### 5. 按 TDD / verify-first 推进开发
进入开发后，强调的不是盲目生成，而是：

- test-first / verify-first
- 持续更新执行证据
- 没有验证就不能宣称完成

### 6. 在需要时接入 Lark 能力补位
如果需求涉及飞书/Lark，这个项目不是停留在“文档参考”层面，而是能够继续往下走到：

- Lark 文档交付
- 画板请求封装
- OpenAPI exploration contract
- `lark-cli api` 调用计划
- Lark skill 规格沉淀

### 7. 做 review / security 收口
在最终交付前，项目会把 review 与安全检查纳入主链路，而不是等最后人工想起来再补。

### 8. 在 Gate 2 完成验收
最终不会直接“默认完成”，而是通过 **Gate 2** 等待交付验收，把测试、评审、安全和产物汇总后再收口。

### 9. 输出最终交付物
最终产物不是单一文件，而是一组完整交付物：

- skill 目录
- 飞书使用指南
- 两张介绍画板
- 标准 zip
- Agent 安装包
- manifest

## 支撑这条主链路的内置能力

上面的主链路能成立，是因为这个项目把多个关键能力做成了内置模块，而不是依赖使用者自己临时拼接。

### Clarification Engine
负责把模糊输入转成结构化澄清摘要，避免跳过问题定义阶段直接实现。

### Execution Spine
负责维护 plan → Gate 1 → develop / verify → Gate 2 → deliver 的主骨架。

### TDD / Verify-first workflow
强调开发过程中的验证证据，而不是“生成了代码就算完成”。

### Lark Delivery
负责飞书指南、文档请求、画板请求与命令计划输出。

### OpenAPI / Lark 补位能力
当现有封装不够时，可以继续探索原生 OpenAPI，并生成调用合同与执行计划，而不是在能力边界处直接中断。

### Lark Skill Spec generation
当目标是把需求继续沉淀成新的 Lark skill 时，可以直接生成规格与脚手架，而不只是停留在概念说明。

### Review / Security summaries
把评审与安全摘要纳入最终交付，不让它们成为易被忽略的“后处理步骤”。

### Packaging
支持标准 zip 输出与 Agent 安装包输出，完成真正的交付收口。

## 它适合谁

这个项目特别适合：

- 想把一个完整流程沉淀成 skill，而不是只写一次性脚本的人
- 想把“需求 → 开发 → 验证 → 文档 → 打包”串成闭环的人
- 希望最终把 skill 交付给别人直接使用的人
- 需要飞书 / Lark 集成能力的人
- 需要更强交付纪律，而不是只要一个目录模板的人

## 它不适合谁

如果你只想：

- 临时写一个一次性脚本
- 生成一个最小目录结构就结束
- 不需要交付文档、画板、打包、审查

那这个项目可能会比你的当前需求更完整，也更重一些。

## 如何开始使用

建议按这个顺序开始：

### 1. 看技能主说明
- `SKILL.md`

### 2. 看执行主链路
- `references/workflow-playbook.md`

### 3. 看模块来源与拼装关系
- `references/source-map.md`

## 最短使用路径

如果你只想快速理解怎么开始，可以按这条路径：

1. 阅读 `SKILL.md`
2. 用你的场景描述来触发这个 skill
3. 完成需求澄清与 Gate 1 确认
4. 推进开发、验证、Lark 补位与交付准备
5. 在 Gate 2 验收最终交付
6. 输出 skill、飞书指南、画板与安装包

## 最终你会得到什么

这个 skill 在本地运行时可以生成：

- skill 目录
- 飞书使用指南
- 两张介绍画板
- `skill-creator-pro.zip`
- `skill-creator-pro-agent-install.zip`
- `agent-install-manifest.json`

## 一图看懂

### 为什么它不是“再多一个 skill”

![Skill Creator Pro Board 1](docs/images/board-01.svg)

### 它的功能与推进流程

![Skill Creator Pro Board 2](docs/images/board-02.svg)

## 仓库里包含什么

这是一个 **skill-only 发布仓库**，公开仓库只保留 skill 本体相关内容：

- `SKILL.md`
- `agents/`
- `assets/`
- `references/`
- `scripts/`
- `docs/images/`
- GitHub 展示所需的说明文件

```text
.
├── SKILL.md
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── agents/
├── assets/
├── docs/images/
├── references/
└── scripts/
```

## 这个公开仓库不保留什么

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
