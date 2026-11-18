---
name: playbook-codex-gemini
description: >-
  Modular, opt-in engineering playbook orchestrating Codex CLI (search, code, self-review),
  Argon Medium (scripting, audit), Gemini 4 Hydrogen via key-file API (ledger, docs), and optional Gemini 3.8 Flash + TTS (multimedia).
  Features Swarm-like visual pipeline dashboards and strict pre-flight harness verification gates.
  Codex defaults to gpt-6.2-sol with reasoning effort max.
  Activate when the user asks to execute, follow, customize, or trigger the Codex collaborative playbook or multi-agent workflow.
---

# Codex 与多模型协同作业 Playbook (Playbook: Codex & Gemini Collaboration)

这是一个**模块化、零侵入、全流程可视化、具备严格 Harness 防错机制**的工程与多媒体协作剧本（Playbook）。
本剧本不修改 Antigravity 任何底层机制，完全依托 Antigravity 原生的命令调度（`run_command`）、子智能体（`invoke_subagent`）与上下文管理驱动。

---

## 0. 剧本配置字典与防错开关 (Playbook Config Matrix)

```yaml
playbook_config:
  # Codex 模型与推理配置 (默认 6.2 sol max)
  codex_model: "gpt-6.2-sol"       # 默认模型: gpt-6.2-sol
  codex_reasoning_effort: "max"    # 默认推理强度: max

  # 可视化与防错闸门
  enable_visual_dashboard: true   # 是否渲染类似 Swarm 的态势感知看板大屏
  step_by_step_gate: false        # 是否开启单步确认 (每步调用 Harness 前亮出校验卡等用户放行)

  # 阶段开关
  enable_codex_search: true       # 是否让 Codex 执行外部/项目材料检索
  enable_argon_audit: true        # 是否启用 Argon Medium 深度审核闸门
  enable_codex_review: true       # 是否让 Codex 执行自身 review
  enable_flash_ledger: true       # 是否生成任务台账与技术文档
  enable_multimedia: false        # 是否激活多媒体视听制作 (默认关闭，按需开启)

  # 阶段五 台账/文档 引擎 (替换原 Flash 3.8 Medium)
  ledger_engine: "hydrogen-api"                   # 通过 key 文件调用 Hydrogen API
  hydrogen_model: "gemini-4-hydrogen"
  hydrogen_key_file: "E:\\Workspaces\\key.txt"     # 可用环境变量 PLAYBOOK_KEY_FILE 覆盖
  hydrogen_key_label: "Gemini 4 Hydrogen"         # key.txt 中该 key 上方的标题行

  # 运行参数
  max_audit_retries: 2            # 方案审核未通过时的最大修改轮次
  sandbox_mode: "workspace-write" # Codex 运行沙箱模式
  tts_primary_voice: "Kore"       # 默认配音员 (Kore / Puck / Fenrir / Aoede)
```

---

## 🛡️ 防错机制：起飞前 Harness 校验卡 (Pre-Flight Inspection Card)

在执行任何关键节点（尤其是调起外部进程、使用写权限或执行代码自审）前，Antigravity 必须先输出校验卡，确保调用的 Harness、路径与参数 100% 正确：

```text
┌─────────────────────────── [Harness Pre-Flight Verification] ───────────────────────────┐
│ 阶段编号: 阶段四 (代码实现)                                                               │
│ 目标 Harness: OpenAI Codex CLI (v0.156.0)                                               │
│ 模型绑定:     gpt-6.2-sol (Reasoning Effort: max)                                        │
│ 沙箱隔离模式: workspace-write (写入范围严格限制在: <TARGET_DIR>)                           │
│ 标准输入控制: Closed (stdin=DEVNULL 避免 Windows 终端死锁挂起)                            │
│ 触发完整指令: "" | codex exec -m gpt-6.2-sol -c model_reasoning_effort="max" ...         │
│ 输入产物依赖: task_script.md, proposal.md (Argon Audit: APPROVED)                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

若 `step_by_step_gate: true`，Antigravity 将在此处暂停等待用户确认（`Proceed [Y/n]`），用户可直接纠偏（例如修正目录、调整模型、修改提示词）。

---

## 阶段一：台本编制 (Scripting Phase - Argon Medium)
- **负责角色**: 首席架构师 (Chief Architect / Gemini 4 Argon)
- **输入**: 原始需求描述。
- **输出**: `task_script.md`（定义架构边界、Codex 执行指令、测试验收指标）。

---

## 阶段二：材料搜集与方案提报 (Research & Proposal Phase - Codex CLI)
- **负责角色**: Codex CLI (`gpt-6.2-sol`, reasoning effort: `max`)
- **执行命令**:
  ```powershell
  "" | codex exec -m gpt-6.2-sol -c model_reasoning_effort="max" --search --skip-git-repo-check -s read-only -o proposal.md "检索技术选型与实现思路"
  ```
- **输出**: `proposal.md`。

---

## 阶段三：方案深度审核闸门 (Proposal Audit Phase - Argon Medium)
- **负责角色**: 审查专家 (Auditor / Gemini 4 Argon)
- **审查检查清单**: 边界保护、时间空间复杂度、测试可行性、无未授权外部依赖。
- **决策分支**: `APPROVED` 进入下一阶段；`REVISE_REQUIRED` 打回修订（最多 2 次）。

---

## 阶段四：代码实现与内部评审 (Implementation Phase - Codex CLI)
- **负责角色**: Codex CLI (`gpt-6.2-sol`, reasoning effort: `max`)
- **执行命令**:
  ```powershell
  "" | codex exec -m gpt-6.2-sol -c model_reasoning_effort="max" --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox --json -C "<WORK_DIR>" "编写代码并运行测试"
  "" | codex review --uncommitted
  ```
- **输出**: 源代码、Git Diff、自查意见、JSONL 事件流。

---

## 阶段五：台账记账与文档撰写 (Ledger & Scribing Phase - Gemini 4 Hydrogen API)
- **负责角色**: 文书与管家 (Scribe)，由 **`gemini-4-hydrogen`** 通过 key 文件里的 API 真实调用，不再由主会话模型代演。
- **执行前必做（Hydrogen 可用性自检）**: 每次进入本阶段先跑一次自检，失败则停下并报告，不得改由主会话代写。
  ```powershell
  python "<PLAYBOOK_DIR>/scripts/hydrogen_call.py" --selftest
  ```
  自检输出 `{"ok": true, ...}` 才继续。`503 high demand` 属于瞬时错误，脚本内置退避重试，不算失败。
- **执行逻辑**: 主会话先把 Codex 的 JSONL 用量、`git diff --stat`、审核结论整理成输入文件，再交给 Hydrogen：
  ```powershell
  python "<PLAYBOOK_DIR>/scripts/hydrogen_call.py" --prompt-file ledger_input.md --out ledger.json --system "只输出符合 ledger_schema.json 的 JSON"
  python "<PLAYBOOK_DIR>/scripts/hydrogen_call.py" --prompt-file summary_input.md --out SUMMARY.md
  ```
  - `ledger.json` (结构化数据)
  - `SUMMARY.md` (交付总结)
- **Key 处理**: key 只在调用时从 `hydrogen_key_file` 读取，经子进程环境变量传给 `gemini-api`。禁止回显、写入日志、写入仓库或粘贴进命令行。

---

## 阶段六 (可选)：多媒体视听制作 (Multimedia Production Phase)
- **负责角色**: Gemini 3.8 Flash (分镜导演) + Gemini TTS (配音合成)
- **执行逻辑**:
  ```powershell
  gemini-api tts -f script.txt --multi-speaker "Alice=Kore,Bob=Puck" --out ./voiceover.wav
  ```

---

## 7. 调用与互动示例

1. **标准执行（默认启用 6.2 sol max）**:
   > “按 codex 协同 playbook 执行此任务。”
2. **极度防错（开启单步人工确认闸门）**:
   > “按 codex playbook 执行此任务，**开启单步确认闸门 (step_by_step_gate)**，每一步调用 harness 前先向我展示校验卡，等我放行后再动。”
