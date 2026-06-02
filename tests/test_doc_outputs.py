import json
import subprocess
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TMP = ROOT / "tests" / ".tmp"


def run(*args):
    return subprocess.run(["python3", *map(str, args)], capture_output=True, text=True)


def test_render_clarification_summary_outputs_explicit_clarification_block(tmp_path):
    spec = {
        "request": "帮我做一个会生成飞书指南和画板的 skill",
        "goal": "沉淀一个 Agent 可安装的技能开发器",
        "target_users": ["业务同学", "技能最终使用者"],
        "inputs": ["自然语言需求"],
        "outputs": ["skill 目录", "飞书指南", "Agent 安装包 zip"],
        "dependencies": ["Lark 文档", "默认画板"],
        "acceptance_criteria": ["有双闸门", "能输出指南和画板"],
        "constraints": ["不要依赖额外安装其他 skill"],
    }
    spec_path = tmp_path / "clarify.json"
    spec_path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    out_dir = tmp_path / "clarify-out"

    proc = run(ROOT / "scripts" / "render_clarification_summary.py", spec_path, out_dir)
    assert proc.returncode == 0, proc.stderr

    md = out_dir / "clarification-summary.md"
    normalized = out_dir / "clarification.normalized.json"
    assert md.exists()
    assert normalized.exists()

    text = md.read_text(encoding="utf-8")
    data = json.loads(normalized.read_text(encoding="utf-8"))
    assert "需求澄清摘要" in text
    assert "当前假设" in text
    assert "待确认项" in text
    assert data["recommended_path"] == "complex"
    assert data["needs_visual_delivery"] == "是"


def test_render_lark_guide_creates_markdown_and_payload(tmp_path):
    spec = {
        "skill_name": "demo-skill",
        "summary": "这是一个示例技能。",
        "scenarios": ["整理周报", "输出飞书文档"],
        "triggers": ["帮我做周报技能"],
        "inputs": ["自然语言需求", "可选示例文件"],
        "outputs": ["技能目录", "zip 包", "飞书指南"],
        "steps": ["描述场景", "确认计划", "验收结果"],
        "limitations": ["需要用户在关键节点确认"],
        "faq": [{"q": "要不要每次都写 plan？", "a": "默认需要。"}]
    }
    spec_path = tmp_path / "guide_spec.json"
    spec_path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    out_dir = tmp_path / "out"

    proc = run(ROOT / "scripts" / "render_lark_guide.py", spec_path, out_dir)
    assert proc.returncode == 0, proc.stderr

    md = out_dir / "feishu-guide.md"
    payload = out_dir / "feishu-create-payload.json"
    assert md.exists()
    assert payload.exists()
    text = md.read_text(encoding="utf-8")
    assert "技能简介" in text
    assert "适用场景" in text
    assert "常见问题" in text
    payload_data = json.loads(payload.read_text(encoding="utf-8"))
    assert payload_data["title"] == "demo-skill 使用指南"
    assert "markdown" in payload_data


def test_render_doc_chart_outputs_mermaid_and_manifest(tmp_path):
    spec = {
        "title": "demo-skill 使用流程",
        "chart_type": "flowchart",
        "nodes": [
            {"id": "start", "label": "描述场景"},
            {"id": "plan", "label": "确认计划"},
            {"id": "accept", "label": "最终验收"}
        ],
        "edges": [
            ["start", "plan"],
            ["plan", "accept"]
        ]
    }
    spec_path = tmp_path / "chart_spec.json"
    spec_path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    out_dir = tmp_path / "chart-out"

    proc = run(ROOT / "scripts" / "render_doc_chart.py", spec_path, out_dir)
    assert proc.returncode == 0, proc.stderr

    mmd = out_dir / "diagram.mmd"
    manifest = out_dir / "chart-manifest.json"
    assert mmd.exists()
    assert manifest.exists()
    content = mmd.read_text(encoding="utf-8")
    assert content.startswith("flowchart TD")
    assert "start[描述场景]" in content
    assert "start --> plan" in content
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert data["chart_type"] == "flowchart"
    assert data["deliverable"] == "diagram.mmd"


def test_render_lark_guide_outputs_feishu_action_plan_for_create_and_update(tmp_path):
    spec = {
        "skill_name": "demo-skill",
        "summary": "这是一个示例技能。",
        "scenarios": ["整理周报", "输出飞书文档"],
        "triggers": ["帮我做周报技能"],
        "inputs": ["自然语言需求", "可选示例文件"],
        "outputs": ["技能目录", "zip 包", "飞书指南"],
        "steps": ["描述场景", "确认计划", "验收结果"],
        "limitations": ["需要用户在关键节点确认"],
        "faq": [{"q": "要不要每次都写 plan？", "a": "默认需要。"}],
        "feishu": {
            "title": "demo-skill 飞书指南",
            "folder_token": "fldcnDemo",
            "doc_id": "doxcnDemo",
            "chunk_limit": 120
        }
    }
    spec_path = tmp_path / "guide_spec.json"
    spec_path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    out_dir = tmp_path / "out"

    proc = run(ROOT / "scripts" / "render_lark_guide.py", spec_path, out_dir)
    assert proc.returncode == 0, proc.stderr

    normalized = out_dir / "guide-spec.normalized.json"
    actions = out_dir / "feishu-action-plan.json"
    assert normalized.exists()
    assert actions.exists()

    normalized_data = json.loads(normalized.read_text(encoding="utf-8"))
    assert normalized_data["title"] == "demo-skill 飞书指南"
    assert normalized_data["feishu"]["folder_token"] == "fldcnDemo"

    action_data = json.loads(actions.read_text(encoding="utf-8"))
    assert action_data["create"]["title"] == "demo-skill 飞书指南"
    assert action_data["create"]["folder_token"] == "fldcnDemo"
    assert action_data["update"]["doc"] == "doxcnDemo"
    assert action_data["update"]["mode"] == "append"
    assert len(action_data["update"]["chunks"]) >= 2
    assert action_data["update"]["chunks"][0]["markdown"]


def test_render_lark_guide_outputs_default_embedded_board_metadata(tmp_path):
    spec = {
        "skill_name": "demo-skill",
        "summary": "这是一个示例技能。",
        "scenarios": ["整理周报", "输出飞书文档"],
        "triggers": ["帮我做周报技能"],
        "inputs": ["自然语言需求"],
        "outputs": ["技能目录", "飞书指南", "zip 包"],
        "steps": ["描述场景", "确认计划", "验收结果"],
        "limitations": ["需要用户在关键节点确认"],
        "faq": [{"q": "要不要每次都写 plan？", "a": "默认需要。"}],
        "feishu": {
            "title": "demo-skill 飞书指南",
            "doc_id": "doxcnDemo",
        },
    }
    spec_path = tmp_path / "guide_spec.json"
    spec_path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    out_dir = tmp_path / "out"

    proc = run(ROOT / "scripts" / "render_lark_guide.py", spec_path, out_dir)
    assert proc.returncode == 0, proc.stderr

    normalized = json.loads((out_dir / "guide-spec.normalized.json").read_text(encoding="utf-8"))
    action_plan = json.loads((out_dir / "feishu-action-plan.json").read_text(encoding="utf-8"))

    assert normalized["embedded_board"]["enabled"] is True
    assert normalized["embedded_board"]["placement"]["after_section"] == "技能简介"
    assert normalized["embedded_board"]["audience"] == "end-user"
    assert action_plan["board"]["enabled"] is True
    assert action_plan["board"]["placement"]["after_section"] == "技能简介"


def test_render_skill_overview_board_outputs_three_zone_board_spec(tmp_path):
    normalized = {
        "skill_name": "demo-skill",
        "title": "demo-skill 使用指南",
        "summary": "这是一个示例技能。",
        "scenarios": ["沉淀重复流程", "生成技能交付包"],
        "triggers": ["帮我做一个 skill"],
        "outputs": ["技能目录", "飞书指南", "zip 包"],
        "steps": ["描述场景", "确认计划", "开发验证", "最终验收", "生成指南与打包"],
        "embedded_board": {
            "enabled": True,
            "board_type": "skill-overview-board",
            "audience": "end-user",
            "placement": {"after_section": "技能简介", "mode": "insert_after_section"},
            "focus": ["how_to_trigger", "how_it_progresses", "what_user_gets"],
        },
    }
    spec_path = tmp_path / "guide-spec.normalized.json"
    spec_path.write_text(json.dumps(normalized, ensure_ascii=False), encoding="utf-8")
    out_dir = tmp_path / "board-out"

    proc = run(ROOT / "scripts" / "render_skill_overview_board.py", spec_path, out_dir)
    assert proc.returncode == 0, proc.stderr

    board_spec = json.loads((out_dir / "skill-overview-board.json").read_text(encoding="utf-8"))
    manifest = json.loads((out_dir / "skill-overview-board.manifest.json").read_text(encoding="utf-8"))
    assert board_spec["board_type"] == "skill-overview-board"
    assert board_spec["placement"]["after_section"] == "技能简介"
    assert [zone["title"] for zone in board_spec["zones"]] == [
        "什么时候使用这个技能",
        "它会怎么帮你推进",
        "最终交付物",
    ]
    assert "确认 plan" in "".join(board_spec["zones"][1]["items"])
    assert "最终验收" in "".join(board_spec["zones"][1]["items"])
    assert manifest["board_type"] == "skill-overview-board"
    assert manifest["deliverable"] == "skill-overview-board.json"


def test_render_lark_doc_commands_outputs_create_and_update_commands(tmp_path):
    action_plan = {
        "create": {
            "title": "demo-skill 飞书指南",
            "markdown": "## 技能简介\n\n这是正文",
            "folder_token": "fldcnDemo"
        },
        "update": {
            "doc": "doxcnDemo",
            "mode": "append",
            "chunks": [
                {"index": 1, "section_titles": ["技能简介"], "markdown": "## 技能简介\n\n这是正文"},
                {"index": 2, "section_titles": ["使用步骤"], "markdown": "## 使用步骤\n\n1. 第一步"}
            ]
        }
    }
    plan_path = tmp_path / "feishu-action-plan.json"
    plan_path.write_text(json.dumps(action_plan, ensure_ascii=False), encoding="utf-8")
    out_dir = tmp_path / "commands-out"

    proc = run(ROOT / "scripts" / "render_lark_doc_commands.py", plan_path, out_dir)
    assert proc.returncode == 0, proc.stderr

    cmd_json = out_dir / "lark-doc-commands.json"
    cmd_md = out_dir / "lark-doc-commands.md"
    assert cmd_json.exists()
    assert cmd_md.exists()

    data = json.loads(cmd_json.read_text(encoding="utf-8"))
    assert data["create"]["command"][0] == "lark-cli"
    assert "+create" in data["create"]["command"]
    assert "fldcnDemo" in data["create"]["command"]
    assert len(data["update"]) == 2
    assert all("+update" in item["command"] for item in data["update"])
    assert data["update"][0]["chunk_index"] == 1
    assert data["update"][1]["chunk_index"] == 2

    md = cmd_md.read_text(encoding="utf-8")
    assert "docs +create" in md
    assert "docs +update" in md
    assert "doxcnDemo" in md


def test_render_lark_doc_commands_outputs_embedded_board_commands(tmp_path):
    action_plan = {
        "create": {
            "title": "demo-skill 飞书指南",
            "markdown": "## 技能简介\n\n这是正文"
        },
        "update": {
            "doc": "doxcnDemo",
            "mode": "append",
            "chunks": [{"index": 1, "section_titles": ["技能简介"], "markdown": "## 技能简介\n\n这是正文"}]
        },
        "board": {
            "enabled": True,
            "board_type": "skill-overview-board",
            "placement": {
                "doc": "doxcnDemo",
                "after_section": "技能简介",
                "mode": "insert_after_section"
            },
            "insert_markdown": "<whiteboard type=\"blank\"></whiteboard>",
            "board_spec_path": "board/skill-overview-board.json"
        }
    }
    plan_path = tmp_path / "feishu-action-plan.json"
    plan_path.write_text(json.dumps(action_plan, ensure_ascii=False), encoding="utf-8")
    out_dir = tmp_path / "commands-out"

    proc = run(ROOT / "scripts" / "render_lark_doc_commands.py", plan_path, out_dir)
    assert proc.returncode == 0, proc.stderr

    data = json.loads((out_dir / "lark-doc-commands.json").read_text(encoding="utf-8"))
    assert "board" in data
    assert "+update" in data["board"]["insert"]["command"]
    assert "whiteboard" in data["board"]["insert"]["shell"]
    md = (out_dir / "lark-doc-commands.md").read_text(encoding="utf-8")
    assert "whiteboard" in md
    assert "board/skill-overview-board.json" in md


def test_create_reports_consumes_verification_and_generates_evidence_summaries(tmp_path):
    workspace = tmp_path / "workspace"
    reports = workspace / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    verification = {
        "required": {
            "SKILL.md": True,
            "agents/openai.yaml": True
        },
        "checks": [
            {
                "cmd": ["python3", "quick_validate.py"],
                "returncode": 0,
                "stdout": "Skill is valid!\n",
                "stderr": ""
            },
            {
                "cmd": ["python3", "generate_openai_yaml.py"],
                "returncode": 0,
                "stdout": "[OK] Created agents/openai.yaml\n",
                "stderr": ""
            }
        ]
    }
    (reports / "verification.json").write_text(json.dumps(verification, ensure_ascii=False), encoding="utf-8")

    proc = run(ROOT / "scripts" / "create_reports.py", workspace)
    assert proc.returncode == 0, proc.stderr

    test_summary = (reports / "test-summary.md").read_text(encoding="utf-8")
    review_summary = (reports / "review-summary.md").read_text(encoding="utf-8")
    security_summary = (reports / "security-summary.md").read_text(encoding="utf-8")

    assert "quick_validate.py" in test_summary
    assert "PASS" in test_summary
    assert "source-map" in review_summary or "SKILL.md" in review_summary
    assert "未发现硬编码凭据" in security_summary or "硬编码凭据" in security_summary
    assert "外部写入动作" in security_summary


def test_bootstrap_skill_workspace_also_instantiates_clarification_template(tmp_path):
    workspace = tmp_path / "workspace"
    proc = run(ROOT / "scripts" / "bootstrap_skill_workspace.py", workspace)
    assert proc.returncode == 0, proc.stderr
    assert (workspace / "task_plan.md").exists()
    assert (workspace / "findings.md").exists()
    assert (workspace / "progress.md").exists()
    assert (workspace / "clarification-summary.md").exists()


def test_build_feishu_delivery_bundle_outputs_guide_board_and_command_plan(tmp_path):
    spec = {
        "skill_name": "demo-skill",
        "summary": "这是一个示例技能。",
        "scenarios": ["整理周报", "输出飞书文档"],
        "triggers": ["帮我做周报技能"],
        "inputs": ["自然语言需求", "可选示例文件"],
        "outputs": ["技能目录", "zip 包", "飞书指南"],
        "steps": ["描述场景", "确认计划", "验收结果"],
        "limitations": ["需要用户在关键节点确认"],
        "faq": [{"q": "要不要每次都写 plan？", "a": "默认需要。"}],
        "feishu": {
            "title": "demo-skill 飞书指南",
            "doc_id": "doxcnDemo",
            "folder_token": "fldcnDemo",
        },
    }
    spec_path = tmp_path / "guide_spec.json"
    spec_path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    out_dir = tmp_path / "bundle-out"

    proc = run(ROOT / "scripts" / "build_feishu_delivery_bundle.py", spec_path, out_dir)
    assert proc.returncode == 0, proc.stderr

    manifest = json.loads((out_dir / "delivery-bundle.manifest.json").read_text(encoding="utf-8"))
    assert manifest["modules"]["clarification"] == "built-in"
    assert (out_dir / "guide/feishu-guide.md").exists()
    assert (out_dir / "guide/feishu-action-plan.json").exists()
    assert (out_dir / "board/skill-overview-board.json").exists()
    assert (out_dir / "guide-commands/lark-doc-commands.json").exists()


def test_execution_spine_initializes_and_advances_gate(tmp_path):
    workspace = tmp_path / "workspace"
    proc = run(ROOT / "scripts" / "init_execution_state.py", workspace, "--goal", "交付单包 skill")
    assert proc.returncode == 0, proc.stderr
    state = json.loads((workspace / "execution-state.json").read_text(encoding="utf-8"))
    assert state["current_phase"] == "clarification"

    proc2 = run(
        ROOT / "scripts" / "advance_execution_gate.py",
        workspace,
        "gate_1",
        "--approve",
        "--completed-item",
        "已完成澄清与计划",
        "--approval-item",
        "请确认计划",
        "--next-step",
        "进入 implementation",
    )
    assert proc2.returncode == 0, proc2.stderr
    gate_summary = (workspace / "gate_1-summary.md").read_text(encoding="utf-8")
    state2 = json.loads((workspace / "execution-state.json").read_text(encoding="utf-8"))
    assert "闸门 1" in gate_summary
    assert state2["gates"]["gate_1"]["approved"] is True
    assert state2["current_phase"] == "implementation"


def test_build_acceptance_packet_collects_report_snippets(tmp_path):
    workspace = tmp_path / "workspace"
    reports = workspace / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "test-summary.md").write_text("# Test Summary\nPASS", encoding="utf-8")
    (reports / "review-summary.md").write_text("# Review Summary\npass-with-evidence", encoding="utf-8")
    (reports / "security-summary.md").write_text("# Security Summary\n未发现硬编码凭据", encoding="utf-8")

    proc = run(ROOT / "scripts" / "build_acceptance_packet.py", workspace)
    assert proc.returncode == 0, proc.stderr
    packet = json.loads((workspace / "acceptance-packet.json").read_text(encoding="utf-8"))
    assert "test_summary" in packet["artifacts"]
    assert "PASS" in packet["snippets"]["test_summary"]


def test_lark_vendor_builds_doc_and_whiteboard_requests(tmp_path):
    create_spec = {
        "title": "demo 文档",
        "markdown": "## 技能简介\n\n内容",
        "folder_token": "fldcnDemo",
    }
    create_spec_path = tmp_path / "create.json"
    create_spec_path.write_text(json.dumps(create_spec, ensure_ascii=False), encoding="utf-8")
    create_out = tmp_path / "create-request.json"
    proc = run(ROOT / "scripts" / "lark_vendor" / "build_doc_request.py", create_spec_path, create_out, "--mode", "create")
    assert proc.returncode == 0, proc.stderr
    create_data = json.loads(create_out.read_text(encoding="utf-8"))
    assert create_data["tool"] == "lark-doc-create"
    assert create_data["folder_token"] == "fldcnDemo"

    board_action = {
        "board_type": "skill-overview-board",
        "placement": {"doc": "doxcnDemo", "after_section": "技能简介"},
        "insert_markdown": "<whiteboard type=\"blank\"></whiteboard>",
        "board_spec_path": "board/skill-overview-board.json",
    }
    board_action_path = tmp_path / "board.json"
    board_action_path.write_text(json.dumps(board_action, ensure_ascii=False), encoding="utf-8")
    board_out = tmp_path / "board-out"
    proc2 = run(ROOT / "scripts" / "lark_vendor" / "build_whiteboard_requests.py", board_action_path, board_out)
    assert proc2.returncode == 0, proc2.stderr
    insert_request = json.loads((board_out / "whiteboard-insert-request.json").read_text(encoding="utf-8"))
    fill_request = json.loads((board_out / "whiteboard-fill-request.json").read_text(encoding="utf-8"))
    assert insert_request["tool"] == "lark-doc-update"
    assert fill_request["tool"] == "lark-doc-whiteboard-update"
    assert fill_request["dry_run_first"] is True


def test_lark_vendor_builds_openapi_exploration_contract(tmp_path):
    spec = {
        "brand": "feishu",
        "requirement": "把用户加入飞书群聊",
        "keywords": ["群成员", "加人进群"],
        "service_candidates": ["im"],
        "write_operation": True,
        "required_scopes": ["im:chat:write"],
        "api_candidates": [
            {
                "name": "Add chat members",
                "method": "POST",
                "path": "/open-apis/im/v1/chats/oc_demo/members",
                "data": {"id_list": ["ou_demo"]},
                "params": {"member_id_type": "open_id"},
                "required_scopes": ["im:chat:write"],
            }
        ],
    }
    spec_path = tmp_path / "openapi.json"
    spec_path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    out_dir = tmp_path / "openapi-out"

    proc = run(ROOT / "scripts" / "lark_vendor" / "explore_openapi_contract.py", spec_path, out_dir)
    assert proc.returncode == 0, proc.stderr

    contract = json.loads((out_dir / "openapi-exploration-contract.json").read_text(encoding="utf-8"))
    call_plan = json.loads((out_dir / "openapi-call-plan.json").read_text(encoding="utf-8"))
    assert contract["brand_host"] == "open.feishu.cn"
    assert contract["safety_gates"]["confirm_before_write"] is True
    assert contract["discovery_steps"][0]["commands"][0] == ["lark-cli", "im", "--help"]
    assert contract["api_candidates"][0]["command"][0:3] == ["lark-cli", "api", "POST"]
    assert call_plan["recommended_first_call"]["path"] == "/open-apis/im/v1/chats/oc_demo/members"


def test_lark_vendor_builds_lark_skill_spec_and_scaffold(tmp_path):
    spec = {
        "name": "lark-chat-member-helper",
        "title": "Lark Chat Member Helper",
        "summary": "封装群成员管理",
        "trigger_scenarios": ["把人拉进群", "批量管理群成员"],
        "shortcut_commands": [
            {
                "title": "查看 IM 能力",
                "command": ["lark-cli", "im", "--help"],
                "rationale": "先确认是否已有 shortcut 或已注册 API",
            }
        ],
        "openapi_calls": [
            {
                "title": "添加群成员",
                "method": "POST",
                "path": "/open-apis/im/v1/chats/oc_demo/members",
                "params": {"member_id_type": "open_id"},
                "data": {"id_list": ["ou_demo"]},
            }
        ],
        "scopes": [{"operation": "添加群成员", "scope": "im:chat:write"}],
        "safety_rules": ["写入前确认用户意图", "禁止猜测 chat_id"],
        "orchestration": ["先查群信息，再写入成员", "失败时返回 chat_id 与错误码"],
    }
    spec_path = tmp_path / "skill-spec.json"
    spec_path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    out_dir = tmp_path / "skill-out"

    proc = run(ROOT / "scripts" / "lark_vendor" / "build_lark_skill_spec.py", spec_path, out_dir)
    assert proc.returncode == 0, proc.stderr

    normalized = json.loads((out_dir / "lark-skill-spec.normalized.json").read_text(encoding="utf-8"))
    command_plan = json.loads((out_dir / "lark-command-plan.json").read_text(encoding="utf-8"))
    skill_md = (out_dir / "SKILL.md").read_text(encoding="utf-8")
    assert normalized["name"] == "lark-chat-member-helper"
    assert len(command_plan["commands"]) == 2
    assert "name: lark-chat-member-helper" in skill_md
    assert "lark-cli api POST /open-apis/im/v1/chats/oc_demo/members" in skill_md
    assert "`im:chat:write`" in skill_md


def test_chart_pipeline_outputs_all_stage_artifacts_and_quality_gate_report(tmp_path):
    spec = {
        "title": "demo flowchart",
        "keywords": ["flowchart"],
        "nodes": [{"id": "start", "label": "开始"}],
        "edges": [["start", "start"]],
    }
    spec_path = tmp_path / "chart.json"
    spec_path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    out_dir = tmp_path / "pipeline-out"

    proc = run(ROOT / "scripts" / "chart_pipeline" / "run_chart_pipeline.py", spec_path, out_dir)
    assert proc.returncode == 0, proc.stderr
    for name in [
        "normalized.json",
        "selection.json",
        "plan.json",
        "layout.json",
        "render-manifest.json",
        "static-check.json",
        "vqa.json",
        "delivery.json",
    ]:
        assert (out_dir / name).exists(), name

    proc2 = run(ROOT / "scripts" / "chart_pipeline" / "build_quality_gate_report.py", out_dir)
    assert proc2.returncode == 0, proc2.stderr
    report = json.loads((out_dir / "quality-gate-report.json").read_text(encoding="utf-8"))
    assert report["gate_a"]["status"] == "needs-runtime-verification"
    assert report["gate_b"]["requires_real_feishu_export"] is True


def test_verify_vendored_skills_reports_all_required_skill_docs_present():
    proc = run(ROOT / "scripts" / "verify_vendored_skills.py")
    assert proc.returncode == 0, proc.stderr
    report = json.loads((ROOT / "reports" / "vendored-skills-verification.json").read_text(encoding="utf-8"))
    assert all(report.values())
    assert report["references/brainstorming/SKILL.md"] is True
    assert report["references/design-lark-chart/SKILL.md"] is True
    assert report["references/lark-doc/SKILL.md"] is True
    assert report["references/system-skill-creator/SKILL.md"] is True
    assert report["references/superpowers/writing-plans/SKILL.md"] is True
    assert report["references/superpowers/requesting-code-review/code-reviewer.md"] is True
    assert report["references/superpowers/using-superpowers/SKILL.md"] is True


def test_package_agent_install_refreshes_staging_manifest_and_install_zip(tmp_path):
    skill_copy = tmp_path / "skill-copy"
    shutil.copytree(ROOT, skill_copy)
    dist = skill_copy / "dist"

    proc = run(skill_copy / "scripts" / "package_agent_install.py", skill_copy, dist)
    assert proc.returncode == 0, proc.stderr

    install_zip = dist / "skill-creator-pro-agent-install.zip"
    manifest = json.loads((dist / "agent-install-manifest.json").read_text(encoding="utf-8"))
    staging_skill = dist / "_agent_install_staging" / "skill-creator-pro"
    assert install_zip.exists()
    assert staging_skill.exists()
    assert manifest["zip"].endswith("skill-creator-pro-agent-install.zip")
    assert "references" in manifest["included_roots"]
    assert "scripts/" in manifest["copied"]
    with zipfile.ZipFile(install_zip) as z:
        names = set(z.namelist())
    assert "skill-creator-pro/scripts/package_agent_install.py" in names
    assert "skill-creator-pro/references/brainstorming/SKILL.md" in names


def test_verify_bundle_records_package_check(tmp_path):
    skill_copy = tmp_path / "skill-copy"
    shutil.copytree(ROOT, skill_copy)

    proc = run(skill_copy / "scripts" / "verify_bundle.py", skill_copy)
    assert proc.returncode == 0, proc.stderr

    verification_path = skill_copy / "reports" / "verification.json"
    assert verification_path.exists()
    verification = json.loads(verification_path.read_text(encoding="utf-8"))
    commands = [" ".join(check["cmd"]) for check in verification["checks"]]
    assert any("quick_validate.py" in cmd for cmd in commands)
    assert any("generate_openai_yaml.py" in cmd for cmd in commands)
    assert any("package_skill.py" in cmd for cmd in commands)
