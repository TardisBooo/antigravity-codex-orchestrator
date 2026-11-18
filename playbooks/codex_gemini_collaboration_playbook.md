# Codex 与多模型协同作业 Playbook (独立执行手册)
> **版本**: 1.2.0 (默认锁定 Codex 6.2 sol max)  
> **定位**: 模块化、声明式、完全可视化的跨模型协作剧本  
> **适用环境**: Google Antigravity + OpenAI Codex CLI + Gemini 4 / 3.8 / TTS  

---

## 🎯 核心设计哲学
1. **零入侵性 (Zero Intrusion)**: 不修改 Antigravity 底层任何一行核心引擎代码，不写死固定的黑盒脚本，纯粹依托 Antigravity 的原生能力（提示词、任务流、子智能体与 CLI 终端调度）。
2. **顶配推理驱动**: 默认锁定 Codex 使用 **`gpt-6.2-sol`** 并开启 **`reasoning_effort: max`**，兼顾高维编程推理与代码自审能力。
3. **全流程可视化 (Full Process Visualization)**: 像 Swarm 一样提供全局态势看板，节点状态（已完成/进行中/打回/待触发）、调用耗时与 Token 开销一目了然。
4. **严格防错与 Harness 校验 (Anti-Drift Harness Gate)**: 在调用每一个底层工具/模型（Harness）前，强制输出《起飞前预检卡 (Pre-flight Inspection Card)》，包含具体命令行、权限沙箱与绑定模型，杜绝调错工具或误改文件。
5. **支持单步确认模式 (Interactive Step-by-Step)**: 用户可随时开启单步放行，每一步执行前由你确认后再动，零脱缰风险。

---

## ⚙️ 剧本运行开关 (Workflow Feature Flags)

在触发此 Playbook 时，你可以根据任务需要开启或关闭任意模块：

| 开关参数 | 默认值 | 作用说明 |
|---|---|---|
| `codex_model` | **`"gpt-6.2-sol"`** | **Codex 默认执行模型** |
| `codex_reasoning_effort` | **`"max"`** | **Codex 深度推理强度** |
| `enable_visual_dashboard` | `true` | 是否实时渲染类似 Swarm 的可视化流程看板大屏 |
| `step_by_step_gate` | `false` | 是否开启单步人工确认闸门 (每步前亮出 Harness 校验卡等用户放行) |
| `enable_codex_search` | `true` | 是否调用 Codex 进行全网/项目代码资料搜集 |
| `enable_argon_audit` | `true` | 是否让 Argon Medium 对 Codex 方案进行严格边界与安全性深度审核 |
| `enable_codex_review` | `true` | 是否在代码编写后触发 Codex 内部自审 (`codex review --uncommitted`) |
| `enable_flash_ledger` | `true` | 是否由 Flash 3.8 Medium 生成机器可读台账 (`ledger.json`) 与总结 |
| `enable_multimedia` | `false` | 是否激活多媒体视听制作（分镜导演 + Gemini TTS 语音生成） |
| `max_audit_retries` | `2` | 审核不通过时的最大修改重试轮次 |

---

## 🛡️ 防错机制：起飞前 Harness 校验卡 (Pre-Flight Inspection Card)

为了防止“调用错 Harness”、“在错误目录下写入”或“参数配置漂移”，在执行任何涉及文件写入或外部模型调用的关键节点前，Antigravity 必须先在会话中亮出如下格式的校验卡：

```text
┌─────────────────────────── [Harness Pre-Flight Verification] ───────────────────────────┐
│ 阶段编号: 阶段四 (代码实现)                                                               │
│ 目标 Harness: OpenAI Codex CLI (v0.156.0)                                               │
│ 模型绑定:     gpt-6.2-sol (Reasoning Effort: max)                                        │
│ 沙箱隔离模式: workspace-write (写入范围严格限制在: D:/my_project)                         │
│ 标准输入控制: Closed (stdin=DEVNULL 避免 Windows 终端死锁挂起)                            │
│ 触发完整指令: "" | codex exec -m gpt-6.2-sol -c model_reasoning_effort="max" ...         │
│ 输入产物依赖: task_script.md, proposal.md (Argon Audit: APPROVED)                        │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

> **若开启了 `step_by_step_gate: true`**：Antigravity 会在亮出此卡后暂停，输出：  
> `“以上 Harness 与命令校验无误，是否继续执行？[Y/n]”`，等待你下达指令后再触发。

---

## 📋 分阶段执行手册 (Phase-by-Phase Directives)

### 阶段一：台本编制 (Scripting Phase)
- **负责角色**: **Argon Medium** (Gemini 4 Argon / 首席架构师)
- **Harness 校验**: 采用只读上下文分析，禁止修改任何本地源码。
- **任务目标**: 将用户的高层目标转化为严密契约《执行台本》。
- **产出物**: `task_script.md`

---

### 阶段二：资料搜集与方案提报 (Research & Proposal Phase)
- **负责角色**: **Codex CLI** (`gpt-6.2-sol`, `effort: max`)
- **Harness 校验**: 
  - 沙箱参数: `-s read-only`（严禁在此阶段写入工程代码）
  - 网络参数: `--search`（允许实时网页搜索）
- **执行命令**:
  ```powershell
  "" | codex exec -m gpt-6.2-sol -c model_reasoning_effort="max" --search --skip-git-repo-check -s read-only -o proposal.md "根据 task_script.md 检索相关实现并输出技术方案"
  ```
- **产出物**: `proposal.md`

---

### 阶段三：方案深度审核闸门 (Audit Gate Phase)
- **负责角色**: **Argon Medium** (Gemini 4 Argon / 审查专家)
- **任务目标**: 阻止设计缺陷与安全隐患流入编码环节。
- **决策分支**:
  - `APPROVED` $\rightarrow$ 准许进入阶段四。
  - `REVISE_REQUIRED` $\rightarrow$ 提炼修改意见反馈给 Codex 修订，重试计数 $+1$（最多 2 次）。

---

### 阶段四：代码实现与内部自审 (Coding & Review Phase)
- **负责角色**: **Codex CLI** (`gpt-6.2-sol`, `effort: max`)
- **执行命令**:
  ```powershell
  # 1. 编写与修改代码
  "" | codex exec -m gpt-6.2-sol -c model_reasoning_effort="max" --skip-git-repo-check --dangerously-bypass-approvals-and-sandbox --json -C "<WORK_DIR>" "根据审核通过的方案编写代码并运行测试"
  
  # 2. 内部自审查
  "" | codex review --uncommitted
  ```
- **产出物**: 源码文件、Git Diff、自查意见、JSONL 事件流。

---

### 阶段五：台账记账与技术文档 (Ledger & Scribing Phase)
- **负责角色**: **Flash 3.8 Medium** (Gemini 3.8 Flash / 文书与管家)
- **任务目标**: 统计工程开销并编写交付总结。
- **产出物**: `ledger.json` 与 `SUMMARY.md`。

---

### 阶段六 (可选)：多媒体视听制作 (Multimedia Phase)
- **负责角色**: **Gemini 3.8 Flash** (导演剪辑) + **Gemini TTS** (配音合成)
- **执行命令**:
  ```powershell
  gemini-api tts -f dialogue.txt --multi-speaker "Alice=Kore,Bob=Puck" --out ./voiceover.wav
  ```
