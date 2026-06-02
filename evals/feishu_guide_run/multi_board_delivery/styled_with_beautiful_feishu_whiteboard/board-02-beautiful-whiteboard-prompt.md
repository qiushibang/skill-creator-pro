请使用 beautiful-feishu-whiteboard skill 制作一张 Feishu/Lark whiteboard。

目标：让读者快速建立从用户输入到最终交付的完整流程心智模型。
推荐风格：Raw Grid（适合流程型、系统型说明图，结构利落，能把主链路和子系统分区做清楚。）
备选风格：Cobalt Glaze（如果希望更稳重、偏正式文档气质，可以用这个。）
受众：第一次接触当前 skill 的读者或使用者
画板标题：skill-creator-pro 的功能与流程
副标题：从一句需求，到飞书指南、画板与 Agent 安装包
布局建议：建议做成横向或纵向流程图，分成用户输入、系统主链路、内置子系统、最终交付物四个泳道或四列。把 Gate 1 和 Gate 2 做成高亮检查点。
风格气质：清晰、系统化、易扫描，优先强调流程而不是装饰。

必须包含的内容：
- 用户侧输入：["描述想沉淀成 skill 的场景", "补充参考资料 / 目标输出 / 特殊约束", "在 Gate 1 确认计划", "在 Gate 2 验收交付物"]
- 系统主链路：["生成 clarification-summary", "检查可复用 skill / source-map", "判断 simple / complex", "初始化 task_plan / findings / progress / execution-state", "进入实现、验证、评审与安全检查", "生成飞书指南、画板与命令计划", "完成 Agent 安装包打包"]
- 内置子系统：["Clarification Engine：显式澄清而不是静默脑补", "Execution Spine：Gate 1 / Gate 2 + verify 流程", "Lark Delivery：飞书文档与请求封装", "Chart Delivery：默认介绍板 + 轻量图表流水线", "Packaging：quick_validate / package_skill / package_agent_install"]
- 最终交付物：["skill 目录", "test / review / security 摘要", "飞书使用指南", "两张介绍画板", "Agent 安装 zip 与 manifest"]
- 关键检查点：["Gate 1：计划确认", "Gate 2：交付验收"]
- 重点高亮：["不是单点功能，而是完整交付流水线", "飞书图文与 Agent 安装包打包默认内建", "复杂能力被统一编排"]

禁止：
- 画成松散海报
- 打乱流程顺序
- 忽略 Gate 1 / Gate 2

交付要求：
- 输出可编辑飞书画板
- 返回文档链接和渲染图
- 这张板将插入到飞书指南“使用步骤”后面
