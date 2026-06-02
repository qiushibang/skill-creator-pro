请使用 beautiful-feishu-whiteboard skill 制作一张 Feishu/Lark whiteboard。

目标：让读者一眼看懂：原来能力散落在多个技能中，导致真实使用时流程割裂；当前 skill 把这些能力收口成单包闭环。
推荐风格：Riso Brut（适合“能力整合 + 痛点 + 解决方案”这类信息密度较高的策略说明板，风格稳且有设计感。）
备选风格：Neo-Grid Bold（更偏编辑感和结构化，适合把多技能能力分组做得更清晰。）
受众：准备安装或使用 skill-creator-pro 的最终用户
画板标题：为什么要把多个技能整合进 skill-creator-pro
副标题：从分散能力、割裂流程，到单包闭环交付
布局建议：建议做成三段式信息图：左侧是被整合能力分组，中间是割裂痛点，右侧是当前 skill 的收口价值；中间用箭头或对比关系衔接。
风格气质：专业、结构清楚、略带产品设计感，不要太花。

必须包含的内容：
- 被整合进来的核心能力：[{"theme": "需求澄清 / 设计前置", "skills": [{"name": "brainstorming", "role": "先澄清目标、约束、验收标准，避免一上来直接实现"}]}, {"theme": "计划 / 执行 / 验证骨架", "skills": [{"name": "superpowers", "role": "提供 writing-plans、executing-plans、TDD、verify、review 等执行骨架"}, {"name": "planning-with-files", "role": "维护 task_plan / findings / progress 等文件化状态"}]}, {"theme": "Skill 开发与交付", "skills": [{"name": "skill-creator", "role": "生成 skill 结构、校验、打包、多 Agent 兼容输出"}, {"name": "find-skills", "role": "开发前检查是否已有现成 skill 可复用"}]}, {"theme": "飞书文档 / 画板 / 图表", "skills": [{"name": "lark-doc", "role": "创建和更新飞书文档，生成文档 action plan"}, {"name": "lark-whiteboard", "role": "插入和更新画板，连接文档与画板落地"}, {"name": "design-lark-chart", "role": "生成高质量图表/画板的样式、流水线和质量门"}]}, {"theme": "Lark 深水区补位", "skills": [{"name": "lark-openapi-explorer", "role": "当现有 CLI/skill 覆盖不到时，探索原生 OpenAPI"}, {"name": "lark-skill-maker", "role": "把飞书自动化需求沉淀成新的 Lark skill 规格"}]}]
- 原来分散使用时的割裂点：["用户需要记住多个 skill 的触发方式与边界", "澄清、计划、开发、验证、飞书交付与打包分散在不同链路里", "每一步都可能重新解释上下文，效率低且容易漏步骤", "图表、文档和 Agent 安装包打包缺少统一收口，临门一脚最容易断"]
- 当前 skill 的解决方式：["把需求澄清 → 计划 → 开发 → 验证 → 飞书图文 → Agent 安装包打包串成主链路", "把常用外部能力内置为本地模块，不再依赖单独安装多个 skill", "保留 Gate 1 / Gate 2，让流程既自动化又可控", "把飞书文档、画板、命令计划和 zip 包统一产出"]
- 重点高亮：["多技能能力被单包收口", "解决真实使用中的上下文割裂", "从能力集合升级为端到端工作流"]

禁止：
- 把制作说明、来源说明、prompt 写到白板上
- 过多小字
- 无结构堆砌 skill 名称

交付要求：
- 输出可编辑飞书画板
- 返回文档链接和渲染图
- 这张板将插入到飞书指南“技能简介”后面
