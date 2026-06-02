from pathlib import Path

src = Path("/Users/bytedance/Desktop/skill-creator-pro/skill-creator-pro/evals/feishu_guide_run/final_publish/feishu-guide-final-live.md")
text = src.read_text()
first = text.find("## 技能简介")
second = text.find("## 技能简介", first + 1)
if second == -1:
    raise SystemExit("no duplicate second heading found")
tail = text[second:]
out = src.with_name("duplicate-tail-to-delete.md")
out.write_text(tail)
print(out)
