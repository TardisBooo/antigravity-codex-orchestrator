# 任务执行台本 (Task Script & Execution Plan)
> **编写者**: Argon Medium (Gemini 4 Argon)  
> **执行引擎**: Codex CLI  
> **审计标准**: 严格工程学边界与零缺陷安全原则  

---

## 1. 目标概述与核心诉求 (Mission & Goals)
- **任务代号**: `{{TASK_ID}}`
- **业务背景**: {{GOAL_DESCRIPTION}}
- **交付目标**:
  1. [ ] 搜集并整理技术前置依赖与设计参考方案
  2. [ ] 编写核心实现代码与辅助配置文件
  3. [ ] 运行内部回归测试与自检评审 (`codex review`)

---

## 2. 约束边界与技术规范 (Constraints & Conventions)
- **目标目录**: `{{WORKING_DIR}}`
- **语言与版本栈**: {{TECH_STACK}}
- **防御性边界 (Invariants)**:
  - 严禁擅自修改已冻结的基础类库与公共接口签名
  - 外部依赖必须锁定语义化版本号
  - 任何新增逻辑必须提供配套的单元测试与断言验证

---

## 3. 分阶段执行指令序列 (Step-by-Step Directives for Codex)

### 阶段一：资料检索与方案提报 (Research & Proposal)
- **Codex 触发命令**:
  ```bash
  codex exec --search -s read-only -o proposal.md "<检索指令>"
  ```
- **输出物**: `proposal.md`
- **Argon 审计闸门**: 必须由 Argon Medium 审核通过后方可激活阶段二。

### 阶段二：代码落地与自检 (Implementation & Self-Review)
- **Codex 触发命令**:
  ```bash
  codex exec -s workspace-write --dangerously-bypass-approvals-and-sandbox -o execution_summary.md "<实施指令>"
  codex review --uncommitted
  ```
- **输出物**: 变更代码、构建测试日志、`review_notes.md`

### 阶段三：台账交割与技术文档 (Handover & Scribing)
- **Flash 3.8 介入**:
  - 提取 Codex 执行的 JSONL 事件流与 Git Diff。
  - 生成 `ledger.json` 与 `CHANGELOG.md`。

---

## 4. 多媒体配套台词与分镜 (Multimedia Script - If Applicable)
> 本节由 Argon Medium 创作台词，交由 Gemini 3.8 Flash 导演并由 Gemini TTS 渲染为音频。

- **解说/角色配音表**:
  - `Narrator` (解说员): `Kore`
  - `Architect` (架构师): `Puck`

### 分镜与台词对照:
| 镜头号 | 画面意象 / 视觉提示 (Visual Prompt) | 角色 | 台词内容 (Spoken Text) | 预估时长 |
|---|---|---|---|---|
| SCENE-01 | 系统架构概览图，微服务网格动态流动 | Narrator | 欢迎来到本次版本交付演示，本次我们将介绍 Antigravity 与 Codex 的无缝协同。 | 5.2s |
| SCENE-02 | 终端内高频输出 JSONL 流与代码高亮对比 | Architect | Codex 已经完成了底层接口的重构与单元测试验证。 | 4.8s |
| SCENE-03 | 最终台账审计与验收大屏，绿标高亮 | Narrator | 审计完成，台账已归档，准备上线！ | 3.5s |
