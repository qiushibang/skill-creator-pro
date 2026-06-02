# Agent Compatibility Checklist

打包前必须确认：

- `SKILL.md` 存在且 frontmatter 合法
- `name` 为小写连字符格式，长度不超过 64
- `description` 不超过 1024 字符，且不包含 XML 标签
- 目录至少包含 `SKILL.md`
- 若存在 `agents/openai.yaml`，字段应可被解析
- 打包 zip / skill 文件后，解压结构完整
- 不把运行期临时目录、`__pycache__`、无关产物打进包

## 建议附带产物
- `references/`
- `scripts/`
- `assets/`
- `evals/`（可选）
