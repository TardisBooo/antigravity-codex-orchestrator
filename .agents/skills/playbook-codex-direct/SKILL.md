---
name: playbook-codex-direct
description: >-
  Codex Direct Relay Playbook: ultra-lean workflow where Antigravity directly dispatches tasks
  to Codex CLI and translates the technical outcome into clear, jargon-free plain human language ("翻译成人话").
  Codex model is selectable in chat (defaults to gpt-6.2-sol with reasoning effort max).
  Activate when user asks to run codex direct relay, codex direct playbook, or /playbook-codex-direct.
---

# Codex 直通转发与人话转译 Playbook (Codex Direct Relay Playbook)

这是一个**极简、轻量、直通**的协同作业剧本。
在此工作流中，本地 Antigravity 默认模型**不做复杂的重型思考或代码生成**，仅承担两项轻量核心职责：
1. **任务直通转发 (Direct Relay)**：把用户的自然语言诉求组装为结构化 Prompt，直接下发给本地 Codex CLI 执行。
2. **结果人话转译 (Human-friendly Translation)**：Codex 执行完毕返回复杂的代码 diff、编译日志和技术堆栈后，Antigravity 负责将其**翻译成通俗、直白、不堆砌术语的“人话”**（清楚说明改动了什么、解决什么痛点、如何快速验证），并整理输出整洁交付文档。

---

## 0. 模型自主选择矩阵 (Model Selection Matrix)

用户可以在对话中随时指定 Codex 运行模型（通过自然语言输入，例如：“*用 6.2 astra low*” 或 “*用 gpt-5.6-sol*”）。如果用户未指定，则默认采用 **`gpt-6.2-sol`（推理强度: `max`）**。

| 用户指令示例 | 对应 Codex 参数 | 适用场景 |
|---|---|---|
| *(默认缺省)* | `-m gpt-6.2-sol -c model_reasoning_effort="max"` | 复杂架构重构、深层算法设计、难缠 Bug 攻坚 |
| “用 6.2 sol max” | `-m gpt-6.2-sol -c model_reasoning_effort="max"` | 满血推理，最强代码与数学逻辑 |
| “用 6.2 astra low” | `-m gpt-6.2-astra -c model_reasoning_effort="low"` | 快速编写脚本、数据轻量提取、快速修补 |
| “用 6 astra low” | `-m gpt-6-astra -c model_reasoning_effort="low"` | 快速探索、高吞吐快速迭代 |
| “用 5.6 sol” | `-m gpt-5.6-sol` | 经典稳定编码任务 |

---

## 1. 核心执行流程 (Workflow Steps)

```
[用户需求输入] (自然语言)
       │
       ▼
 [阶段 1: 任务直通下发] Antigravity 组装指令，调用 Codex CLI 执行
       │ (非交互式、防终端死锁、启用 JSONL 监控)
       ▼
 [阶段 2: Codex 本地执行] 搜料、代码编写、单元测试与自检
       │
       ▼
 [阶段 3: 结果人话转译] Antigravity 将复杂 Diff 与日志翻译为通俗业务语言
       │ (讲清楚：改了哪、为什么改、效果如何、怎么验证)
       ▼
 [阶段 4: 极简文档交付] 输出清晰的 SUMMARY.md 与用户汇报
```

---

## 2. 阶段详细执行指令 (Phase Directives)

### 阶段一：任务直通下发 (Relay Phase)
- **负责角色**: 本地 Antigravity（纯转发）
- **执行逻辑**:
  1. 解析用户指令中是否有指定 Codex 模型；若无，默认 `gpt-6.2-sol` + `effort: max`。
  2. 仅在用户明确要求调用 Codex 时转发。先确认目标工作区的绝对路径，并说明 Codex 可能把任务内容和读取的项目上下文发送给已配置的模型服务。目标或授权范围不清楚时，先确认再运行。
  3. 审阅和分析使用 `read-only`。用户授权在该工作区内修改文件后，改用 `workspace-write`。只有用户明确选的是非 Git 工作目录时才传 `--skip-git-repo-check`。不要添加其他写入目录。遇到需要额外权限的操作时，停下来请用户确认，不要放宽沙箱重试。
  4. 通过标准输入传任务内容，写入后关闭输入流。使用参数数组传递模型、推理强度和路径，避免用 shell 拼接用户输入。命令结构如下：
     ```text
     codex -a on-request exec --sandbox read-only -m <CHOSEN_MODEL> -c model_reasoning_effort=<CHOSEN_EFFORT> --json -C <WORK_DIR> -
     ```
  5. 检查退出码。任务失败时，如实报告错误或待授权事项。修改成功后，在目标工作区检查 `git diff` 和测试结果。

### 阶段二：结果“人话转译”与文档总结 (Translation & Scribing Phase)
- **负责角色**: 本地 Antigravity（转译网关）
- **转译规范 (Plain Language Principles)**:
  - **拒绝 AI 官话与空洞套话**：禁止出现“全方位赋能”、“深度赋能”、“显著提升”等空洞修辞。
  - **三句话讲清本质**：
    1. **现状痛点**：之前代码哪里有问题/缺什么。
    2. **到底改了啥**：用最直白的大白话说明修改的核心逻辑（修改了哪个文件哪几个函数）。
    3. **如何验证效果**：给出最简单的一条测试命令或观察指标，让用户一眼看出效果。
  - **交付文件**:
    - 在会话中交付简明总结。用户要求写报告时，在已授权的工作区生成 `SUMMARY.md`。

---

## 3. 调用话术示例 (Usage Examples)

1. **默认满血模型（6.2 sol max）执行**:
   > “按直通 playbook（playbook-codex-direct）帮我把现有的订单导出脚本优化成异步流式导出，完成后用人话给我总结。”

2. **自选快速模型（6.2 astra low）执行**:
   > “按 codex direct playbook，用 6.2 astra low 快速把这个目录下的测试数据清洗一下，结果翻译成人话告诉我。”

3. **指定特定稳定模型（5.6 sol）执行**:
   > “使用 codex 直通工作流，指定用 5.6 sol，修复这个登录 token 校验的 bug，并输出人话文档。”
