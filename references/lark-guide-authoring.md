# Lark Guide Authoring

本文件用于在最终验收后生成飞书使用指南。

## 文档结构建议
1. 技能简介
2. 适用场景
3. 触发方式
4. 输入 / 输出
5. 使用步骤
6. 示例
7. 限制与注意事项
8. 常见问题

## 写入策略
- 优先创建新文档
- 长文档分段追加
- 需要图表时，先产出本地草稿与图描述，再写入飞书
- 图表失败时，降级为纯文本说明并解释原因

## 参考来源
- `references/copied/lark-doc-create.md`
- `references/copied/lark-doc-update.md`
- `references/copied/lark-doc-fetch.md`


## 推荐生成方式
1. 先整理结构化 spec（技能名、简介、适用场景、触发方式、输入、输出、步骤、限制、FAQ）
2. 运行 `scripts/render_lark_guide.py <spec.json> <out_dir>` 生成：
   - `feishu-guide.md`
   - `feishu-create-payload.json`
   - `guide-spec.normalized.json`
   - `feishu-action-plan.json`
3. 如果希望一次性生成完整图文交付，优先运行 `scripts/build_feishu_delivery_bundle.py <spec.json> <out_dir>`，统一产出：
   - `guide/feishu-guide.md`
   - `guide/guide-spec.normalized.json`
   - `guide/feishu-action-plan.json`
   - `board/skill-overview-board.json`
   - `guide-commands/lark-doc-commands.json`
4. `guide-spec.normalized.json` 作为后续 docs / chart / review 的统一输入，不要重复手写同一份信息
5. 如需真正创建飞书文档，优先读取 `feishu-action-plan.json`：
   - `create`：用于 `docs +create`
   - `update`：用于已存在文档的分段 `docs +update --mode append`
6. 如需把 action plan 转成可直接执行的命令清单，运行 `scripts/render_lark_doc_commands.py <feishu-action-plan.json> <out_dir>`，生成 JSON/Markdown 两种命令计划
7. 文档过长时使用 `update.chunks` 顺序追加，避免一次性写入过长 markdown
8. 当 `embedded_board.enabled` 为 `true` 时，必须额外生成默认介绍画板 spec，并把画板插入到“技能简介”后。
9. 画板插入与填充属于 guide action plan 的一部分，不依赖额外 skill 安装；如果画板失败，必须降级为纯文字指南并记录原因。

## 推荐 spec 字段
- `skill_name`
- `summary`
- `scenarios`
- `triggers`
- `inputs`
- `outputs`
- `steps`
- `limitations`
- `faq`

## Feishu action plan 约定
- `create.title`：文档标题
- `create.markdown`：完整初始正文
- `create.folder_token/wiki_node/wiki_space`：可选投放位置
- `update.doc`：已存在文档的 doc_id 或 URL
- `update.mode`：默认 `append`
- `update.chunks[]`：按顺序执行的分段写入动作，每段带 `section_titles` 和 `markdown`
- `board.enabled`：是否启用默认介绍画板
- `board.placement.after_section`：默认应为 `技能简介`
- `board.insert_markdown` / `board.board_spec_path`：画板占位插入与后续填充所需信息

## 命令计划产物
- `lark-doc-commands.json`：结构化命令数组，可供后续自动执行器消费
- `lark-doc-commands.md`：便于人工审阅和手动执行的命令清单
