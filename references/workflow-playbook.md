# Workflow Playbook

本手册把多个来源技能的主链路整合为单包自动开发流程。

## 主链路
1. 运行内置澄清引擎并记录关键约束
2. 先检查是否已有现成 skill 或模式可复用
3. 判断 simple / complex
4. 初始化 `task_plan.md`、`findings.md`、`progress.md`
5. 生成实施计划并停在闸门 1
6. 获得确认后进入开发
7. 对关键行为执行 test-first / verify-first
8. 汇总 test / review / security 摘要并停在闸门 2
9. 获得验收后生成飞书图文指南
10. 校验并打包 skill

## 内置引擎要求
- `clarification-summary.md` 必须在 `task_plan.md` 之前生成，不允许静默跳过。
- 若信息充足，澄清摘要中的 `待确认项` 可写 `暂无`，但不能省略该文件。
- `execution-state.json` 必须作为执行状态单一来源，驱动 gate 1 / gate 2 的状态推进。
- 飞书图文交付优先走本地脚本编排：guide → board → commands。
- 如需求超出已内置的 docs / whiteboard 封装，优先运行 `scripts/lark_vendor/explore_openapi_contract.py` 生成 OpenAPI 挖掘合同与调用计划。
- 如目标是沉淀新的 Lark 自动化 skill，优先运行 `scripts/lark_vendor/build_lark_skill_spec.py` 生成本地 `SKILL.md` 脚手架与命令编排。
- 更完整的图表生成优先走本地图表八步流水线，并保留阶段 JSON 证据。
- `scripts/verify_vendored_skills.py` 必须能证明当前技能声明已内嵌的源 skill 文档与关键参考都存在。
- Agent 安装测试前，必须运行 `scripts/package_agent_install.py` 刷新 `_agent_install_staging/`、`agent-install-manifest.json` 与 `*-agent-install.zip`。
- 所有内置模块默认以“本技能目录内脚本”为准，不依赖运行时再安装外部 skill。

## simple skill 建议
- 允许轻量计划
- 至少保留一个最小端到端示例
- 至少保留结构校验 + 打包验证

## complex skill 建议
- 必须完整维护 plan / findings / progress
- 必须保留测试摘要、评审摘要、安全摘要
- 若涉及 Lark/OpenAPI 或图表/文档增强，必须读取对应参考文档
