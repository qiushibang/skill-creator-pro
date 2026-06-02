# Review Gates

## 必要摘要
- `reports/test-summary.md`
- `reports/review-summary.md`
- `reports/security-summary.md`

## 通过条件
- 至少执行一次结构校验
- 至少执行一次打包验证
- 复杂 skill 必须给出 review 结论
- 复杂 skill 或涉及外部集成时必须给出 security 结论
- 未生成摘要不得进入最终验收

## 安全审查关注点
- 是否复制了现成脚本且说明来源
- 是否引入了不必要的危险命令
- 是否把密钥、令牌、内部链接硬编码到 skill 中
- 飞书文档操作是否区分只读/写入步骤
