# Source Map

本技能采用“复制优先、改写其次、最小新增”的实现策略。下表记录主要模块来源。

| 新模块 | 来源技能 | 来源内容 | 方式 | 改动原因 |
|---|---|---|---|---|
| `SKILL.md` 需求澄清与双闸门流程 | `brainstorming` | `SKILL.md` | 局部改写并内嵌 | 保留“先澄清再实现”和确认闸门，改造成单包 skill 自动开发流程 |
| `SKILL.md` 检索现成 skill 步骤 | `find-skills` | `SKILL.md` | 局部改写 | 把“先搜已有技能”改成自动开发前置复用检查 |
| `scripts/generate_openai_yaml.py` | `.system/skill-creator` | `scripts/generate_openai_yaml.py` | 局部改写 | 保留原生成逻辑，去掉外部 YAML 依赖以适配当前环境 |
| `scripts/quick_validate.py` | `.system/skill-creator` | `scripts/quick_validate.py` | 局部改写 | 保留校验规则，去掉外部 YAML 依赖以适配当前环境 |
| `scripts/package_skill.py` | `skill-creator` | `scripts/package_skill.py` | 局部改写 | 保留打包逻辑，改为本地导入并默认输出 Agent 兼容安装包 |
| `assets/templates/*.md` | `planning-with-files` | `templates/*.md` | 直接复制 | 复用计划/发现/进度模板 |
| `references/copied/openai_yaml.md` | `.system/skill-creator` | `references/openai_yaml.md` | 直接复制 | 保留 metadata 字段规范 |
| `references/copied/schemas.md` | `skill-creator` | `references/schemas.md` | 直接复制 | 复用 eval / metrics / grading 数据结构 |
| `references/workflow-playbook.md` | `writing-plans` + `executing-plans` + `test-driven-development` + `verification-before-completion` | 各自 `SKILL.md` | 拼装整合并内嵌 | 把 plan→execute→TDD→verify 组合成单包执行手册 |
| `references/review-gates.md` | `requesting-code-review` + `verification-before-completion` | `SKILL.md` / `code-reviewer.md` | 拼装整合 | 增加 review 与 security summary 的通过条件 |
| `references/lark-guide-authoring.md` | `lark-doc` + `lark-shared` + `lark-skill-maker` + `lark-openapi-explorer` | `SKILL.md` 与 refs | 拼装整合 | 统一飞书文档与 Lark/OpenAPI skill 文档增强流程 |
| `references/doc-chart-pipeline.md` | `design-lark-chart` | `references/01-pipeline.md`, `06-quality-gates.md`, `02-chart-taxonomy.md` | 局部改写 | 改造成只服务于“技能功能/使用文档”的轻量图表流水线 |
| `assets/style-tokens/*` 与 `references/examples/*` | `design-lark-chart` | style-tokens 与 examples | 直接复制 | 作为图表文档阶段的视觉与示例资源 |
| `references/agent-compatibility.md` | `Agent 安装兼容指南` + `.system/skill-creator` | 文档约束与 validator 规则 | 最小新增 | 统一 Agent 兼容约束，便于打包前核验 |
| `scripts/bootstrap_skill_workspace.py` | 无直接现成脚本 | 最小新增 | 最小新增 | 需要把模板实例化到当前任务工作区 |
| `scripts/create_reports.py` | 无直接现成脚本 | 最小新增 | 最小新增 | 需要统一生成测试/评审/安全摘要 |
| `scripts/render_clarification_summary.py` | `brainstorming` | 澄清结构与硬闸门理念 | 最小新增 + 本地化 | 把 brainstorming 的关键前置能力变成本 skill 的内置澄清引擎 |
| `assets/templates/clarification-summary.md` | `brainstorming` | 需求澄清摘要结构 | 最小新增 + 本地化 | 保证每次都显式输出澄清结果而不是静默跳过 |
| `scripts/init_execution_state.py` / `scripts/advance_execution_gate.py` / `scripts/build_acceptance_packet.py` | `superpowers` + `skill-creator` | gate / verification / acceptance spine | 最小新增 + 本地化 | 把执行骨架和双闸门做成当前 skill 的本地状态机 |
| `references/superpowers/*` | `writing-plans` + `executing-plans` + `test-driven-development` + `verification-before-completion` + `requesting-code-review` + `brainstorming` | `SKILL.md` / reviewer prompts / anti-pattern docs | 直接复制 | 把 superpowers 相关源 skill 文档与关键配套资料并入当前 skill，供本地执行骨架与 reviewer 流程直接读取 |
| `references/system-skill-creator/SKILL.md` | `.system/skill-creator` | `SKILL.md` | 直接复制 | 保留系统 skill-creator 的原始说明，避免只剩局部脚本没有源文档 |

| `scripts/frontmatter_utils.py` | 无直接现成脚本 | 最小新增 | 最小新增 | 为复制来的脚本提供无外部依赖的 frontmatter 解析 |
| `assets/templates/guide/feishu-guide-template.md` | `lark-doc` | create/update 文档结构建议 | 拼装整合 | 固化为可直接渲染的飞书指南模板 |
| `assets/templates/chart/flowchart.mmd.tpl` | `design-lark-chart` | chart pipeline 与 examples | 局部改写 | 固化为轻量文档流程图模板 |
| `scripts/render_lark_guide.py` | `lark-doc` + `lark-skill-maker` | 文档创建/update 规则 | 拼装整合 | 生成飞书指南正文、规范化 spec，以及 docs +create / +update action plan |
| `scripts/render_doc_chart.py` | `design-lark-chart` | pipeline / examples / Mermaid 路由 | 局部改写 | 生成文档型 Mermaid 图表与 manifest |
| `scripts/render_lark_doc_commands.py` | `lark-doc` | `docs +create` / `docs +update` 命令模式 | 拼装整合 | 把 Feishu action plan 转成可执行命令计划，便于真实落地执行 |
| `scripts/render_skill_overview_board.py` | `design-lark-chart` + `lark-doc` | 流水线/样式/文档插入规则 | 拼装整合 | 生成默认介绍画板并并入 guide action plan |
| `embedded_board` action-plan 扩展 | `design-lark-chart` + `lark-doc-update` | 画板插入与文档更新规则 | 局部改写 | 默认插入“技能简介”后面的用户介绍板 |
| `scripts/build_feishu_delivery_bundle.py` | `lark-doc` + `design-lark-chart` | 文档、画板、命令计划组合流程 | 最小新增 + 本地化 | 把最终图文交付编排固化为本地一键脚本 |
| `scripts/lark_vendor/*` | `lark-doc` + `lark-whiteboard` + `lark-shared` | docs/whiteboard 请求结构与安全规则 | 最小新增 + 本地化 | 不再只引用外部 skill 文档，而是在当前 skill 中内置执行包装层 |
| `scripts/lark_vendor/explore_openapi_contract.py` | `lark-openapi-explorer` | OpenAPI 挖掘步骤、llms 文档检索策略、`lark-cli api` 裸调规则 | 最小新增 + 本地化 | 把 explorer 从“参考说明”升级为当前 skill 的本地探索合同与调用计划生成器 |
| `scripts/lark_vendor/build_lark_skill_spec.py` | `lark-skill-maker` | Lark skill 模板、命令优先级、scope 与安全规则 | 最小新增 + 本地化 | 把 skill maker 从“写法参考”升级为当前 skill 的本地 Lark skill 规格与脚手架生成器 |
| `scripts/chart_pipeline/*` | `design-lark-chart` | 八步管道（Normalize → Deliver） | 最小新增 + 本地化 | 把 chart pipeline 的核心阶段落成本地 JSON 产物链 |
| `assets/previews/*` / `assets/raw/*` / `references/design-lark-chart/*` / `references/lark-doc/*` / `references/lark-whiteboard*` / `references/lark-shared/SKILL.md` | `design-lark-chart` + `lark-doc` + `lark-whiteboard` + `lark-shared` | 参考资产与规则 | 直接复制 | 把核心引用资料一并带入当前 skill，避免运行时再去外部目录查找 |
