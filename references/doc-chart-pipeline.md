# Doc Chart Pipeline

这是从 `design-lark-chart` 改写来的**轻量文档图表流水线**，只用于技能功能说明与使用流程图，不作为通用画图引擎。

## 目标图型
- 使用流程图
- 功能结构图
- 触发条件示意图

## 新增专用图型：skill-overview-board
- 面向最终使用者
- 默认三段式：触发 / 推进 / 交付物
- 默认位置：技能简介后
- 默认高亮：确认 plan / 最终验收
- 用于飞书指南中的默认介绍画板，不把空白板或未填充板视为成功

## 轻量流程
Normalize → Select → Plan → Layout → Render → StaticCheck → VQA → Deliver

## 约束
- 图表只能表达文档里已有的技能信息，不能补造业务内容
- 优先使用 `references/examples/` 里的安全样例做参考
- 必须保留文字版内容，图表只是增强，不是唯一交付
- 图表不过质量门时降级为纯文档

## 质量门
- 结构清楚
- 与文字说明一致
- 没有虚构模块
- 若同步到飞书，需有实际写入结果或明确失败说明


## 推荐生成方式
1. 准备 chart spec（title、chart_type、nodes、edges）
2. 运行 `scripts/render_doc_chart.py <spec.json> <out_dir>`
3. 默认输出：
   - `diagram.mmd`
   - `chart-manifest.json`
4. 当前版本先支持 `flowchart`，用于技能使用流程图与功能结构图
5. 当 `embedded_board.enabled` 为 `true` 时，额外生成 `skill-overview-board` spec，作为插入飞书文档“技能简介”后的默认介绍画板
6. 如果后续要同步飞书，再结合 Lark 文档/白板流程执行；失败时降级为纯文字指南
7. 如果是最终交付阶段，优先让 `scripts/build_feishu_delivery_bundle.py` 统一编排 guide / board / commands，避免分散执行
