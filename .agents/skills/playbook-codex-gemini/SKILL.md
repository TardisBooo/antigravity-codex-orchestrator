---
name: playbook-codex-gemini
description: >-
  Modular, opt-in engineering playbook orchestrating Codex CLI (search, code, self-review),
  Gemini 4 Hydrogen API (task scripting, audit, ledger and storyboarding), and Gemini TTS.
  Local Antigravity acts strictly as a lightweight orchestrator/dispatcher, offloading all generation and review to Codex and APIs.
  Features Swarm-like visual pipeline dashboards and strict pre-flight harness verification gates.
  Codex defaults to gpt-6.2-sol with reasoning effort max.
  Activate when the user asks to execute, follow, customize, or trigger the Codex collaborative playbook or multi-agent workflow.
---

# Codex 与 Gemini 4 Hydrogen 协同分发 Playbook (Codex & Hydrogen Multi-Agent Playbook)

这是一个**模块化、全外包分发、零本地重型开销、全流程可视化**的工程与多媒体协同剧本（Playbook）。

此剧本需单独启用。使用前由用户设置 `GEMINI_API_KEY`，或用 `PLAYBOOK_KEY_FILE` 明确指定工作区之外的凭据文件。每次首次调用外部服务前，让用户核对将发送的任务、源代码片段、差异或日志。只提交本阶段所需的内容，先移除凭据和无关记录。

### 核心分工与设计原则：
1. **本地 Antigravity 仅作调度中枢 (Pure Orchestrator & Dispatcher)**:
   本地默认模型**不承担实质性的复杂方案构思、代码编写或审计推演**，纯粹负责维护任务流水线状态机、执行起飞前校验卡（Pre-Flight Inspection）、安全派发外部子进程与 API 调用、以及展示全局态势看板。
2. **所有重型工作全部外部化分发**:
   - **OpenAI Codex CLI** (`gpt-6.2-sol max`): 承担全网检索、方案初稿编制、代码落地与本地内部代码自审 (`codex review`)。
   - **Gemini 4 Hydrogen API**: 承担阶段一（台本编制与架构契约）、阶段三（方案深度审核闸门）、阶段五（台账记账与交付文档）、阶段六（多媒体视觉分镜与导演时序切片）。
   - **Gemini TTS** (`gemini-3.8-flash-tts`): 承担拟真语音合成。

---

## 0. 剧本配置字典与防错开关 (Playbook Config Matrix)

```yaml
playbook_config:
  # Codex 模型与推理配置 (默认 6.2 sol max，可随时在对话中自选)
  codex_model: "gpt-6.2-sol"       # 默认模型: gpt-6.2-sol
  codex_reasoning_effort: "max"    # 默认推理强度: max

  # 外部 API 引擎配置
  api_engine: "gemini-4-hydrogen"

  # 可视化与防错闸门
  enable_visual_dashboard: true   # 是否渲染类似 Swarm 的态势感知看板大屏
  step_by_step_gate: false        # 是否开启单步确认 (每步调用 Harness 前亮出校验卡等用户放行)

  # 阶段开关 (全流程可自由裁切)
  enable_codex_search: true       # 阶段二: 是否让 Codex 执行外部/项目材料检索
  enable_hydrogen_audit: true     # 阶段三: 是否启用 Hydrogen 深度方案审核闸门
  enable_codex_review: true       # 阶段四: 是否让 Codex 执行自身 review
  enable_ledger_docs: true        # 阶段五: 是否由 Hydrogen 生成任务台账与技术文档
  enable_multimedia: false        # 阶段六: 是否激活多媒体视听制作 (默认关闭，按需开启)

  # 运行参数
  max_audit_retries: 2            # 方案审核未通过时的最大修改轮次
  sandbox_mode: "workspace-write" # Codex 运行沙箱模式
  tts_primary_voice: "Kore"       # 默认配音员 (Kore / Puck / Fenrir / Aoede)
```

---

## 🛡️ 防错机制：起飞前 Harness 校验卡 (Pre-Flight Inspection Card)

在执行任何关键节点（调起 Codex CLI、调用外部 Hydrogen API、或运行写权限命令）前，Antigravity 必须先输出校验卡，确保调用的 Harness、路径与参数 100% 正确：

```text
┌─────────────────────────── [Harness Pre-Flight Verification] ───────────────────────────┐
│ 阶段编号: 阶段四 (代码实现)                                                               │
│ 目标 Harness: OpenAI Codex CLI (v0.156.0)                                               │
│ 模型绑定:     gpt-6.2-sol (Reasoning Effort: max)                                        │
│ 沙箱隔离模式: workspace-write (写入范围严格限制在: <TARGET_DIR>)                           │
│ 标准输入控制: Closed (stdin=DEVNULL 避免 Windows 终端死锁挂起)                            │
│ 触发完整指令: "" | codex exec -m gpt-6.2-sol -c model_reasoning_effort="max" ...         │
│ 输入产物依赖: task_script.md, proposal.md (Hydrogen Audit: APPROVED)                     │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

若 `step_by_step_gate: true`，Antigravity 将在此处暂停等待用户确认（`Proceed [Y/n]`），用户可直接纠偏。
写入前核对用户已经授权目标工作区和写入范围。需要额外权限时暂停，让用户确认。

---

## 阶段一：台本编制与架构契约 (Scripting Phase - Hydrogen API)
- **负责角色**: 外部 API (`gemini-4-hydrogen`)
- **执行逻辑**: 本地 Antigravity 仅将用户诉求打包为输入文件，直接派发给 Hydrogen API：
  ```powershell
  python scripts/hydrogen_call.py --prompt-file "user_goal.md" --out "task_script.md" --system "你是顶尖架构师，负责分析需求并制定工程边界契约与Codex执行指令"
  ```
- **输出**: `task_script.md`（定义架构边界、Codex 执行指令、测试验收指标）。

---

## 阶段二：材料搜集与方案提报 (Research & Proposal Phase - Codex CLI)
- **负责角色**: 本地 Codex CLI (`gpt-6.2-sol`, reasoning effort: `max`)
- **执行命令**:
  ```powershell
  "根据 task_script.md 检索技术选型与实现思路" | codex -a on-request --search exec -m gpt-6.2-sol -c model_reasoning_effort="max" -s read-only -o proposal.md -
  ```
- **输出**: `proposal.md`。

---

## 阶段三：方案深度审核闸门 (Proposal Audit Phase - Hydrogen API)
- **负责角色**: 外部 API (`gemini-4-hydrogen`)
- **执行逻辑**: 本地 Antigravity 将 `task_script.md` 与 Codex 的 `proposal.md` 发送给 Hydrogen API 执行零缺陷边界审查：
  ```powershell
  python scripts/hydrogen_call.py --prompt-file "audit_input.md" --out "audit_report.md" --system "你是极其严格的架构审查专家，严格检查封装性、安全隐患与复杂度，给出判定结论 APPROVED 或 REVISE_REQUIRED"
  ```
- **决策分支**: `APPROVED` 准入下一阶段；`REVISE_REQUIRED` 打回修订（最多 2 次）。

---

## 阶段四：代码实现与内部评审 (Implementation Phase - Codex CLI)
- **负责角色**: 本地 Codex CLI (`gpt-6.2-sol`, reasoning effort: `max`)
- **执行命令**:
  ```powershell
  "编写代码并运行测试" | codex -a on-request exec -m gpt-6.2-sol -c model_reasoning_effort="max" -s workspace-write --json -C "<WORK_DIR>" -
  "" | codex review --uncommitted
  ```
- **输出**: 源代码、Git Diff、自查意见、JSONL 事件流。

---

## 阶段五：台账记账与文档撰写 (Ledger & Scribing Phase - Hydrogen API)
- **负责角色**: 外部 API (`gemini-4-hydrogen`)
- **执行前必做**: 运行自检，验证 API 可用性：
  ```powershell
  python scripts/hydrogen_call.py --selftest
  ```
- **执行逻辑**: 本地 Antigravity 收集 Codex JSONL 日志与 Git Diff 整理为输入，派发给 Hydrogen API 生成规范文件：
  ```powershell
  python scripts/hydrogen_call.py --prompt-file ledger_input.md --out ledger.json --system "只输出符合 ledger_schema.json 规范的 JSON"
  python scripts/hydrogen_call.py --prompt-file summary_input.md --out SUMMARY.md
  ```
- **输出**: `ledger.json` (结构化数据) 与 `SUMMARY.md` (交付总结)。

---

## 阶段六 (可选)：多媒体视听制作 (Multimedia Phase - Hydrogen API + TTS)
- **负责角色**:
  - **视觉导演与分镜切片**: 外部 API (`gemini-4-hydrogen`)
    ```powershell
    python scripts/hydrogen_call.py --prompt-file storyboard_input.md --out timeline.json --system "规划演示分镜时长、视效提示词与时间轴切片"
    ```
  - **语音合成**: 本地 `gemini-api tts` (24kHz WAV)
    ```powershell
    gemini-api tts -f dialogue.txt --multi-speaker "Alice=Kore,Bob=Puck" --out ./voiceover.wav
    ```

---

## 7. 调用与互动示例

1. **标准全分发执行**:
   > “按 codex 协同 playbook 执行此任务。”
2. **极度防错（开启单步人工确认闸门）**:
   > “按 codex playbook 执行此任务，**开启单步确认闸门 (step_by_step_gate)**，每一步调用外部 harness 前先展示校验卡，等我放行后再跑。”
3. **自选 Codex 运行模型**:
   > “按 codex 协同 playbook 执行任务，Codex 指定使用 6.2 astra low。”
