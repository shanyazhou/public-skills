---
name: project-governance
description: Use when setting up reusable project rules / 项目治理规则, initializing a codebase for Codex collaboration, reducing long-chat context dependence, creating or refreshing project handoff files, defining engineering guardrails, starting work in a new or ungoverned repository, or turning lessons from one project into general rules.
---

# Project Governance / 项目治理

用这个 skill 建立项目级协作规则和上下文文件，同时避免把某个项目的业务细节、服务器、账号或事故直接带进公共规则。

## 核心思路 Core Idea

公共规则保持通用，项目事实留在项目里：

- Public skill / 公共 skill：方法、流程、模板、质量要求。
- Project files / 项目文件：真实产品上下文、命令、环境、服务器、未决问题、事故记录。
- Local secret files / 本地秘密文件：账号、token、私有部署说明。

不要把具体项目的服务器、密码、业务名称、人员、日期或事故写进公共/全局规则，除非已经匿名化并且只是示例。

## 初始化项目时

在项目根目录创建或更新这些文件：

- `AGENTS.md`：assistant 入口文件，说明新会话先读什么、怎么在本仓库工作。
- `PROJECT_CONTEXT.md`：稳定项目事实，如产品目标、技术栈、目录结构、运行/部署命令、环境。
- `SESSION_SUMMARY.md`：替换式当前交接摘要，不是聊天记录。
- `ACTIVE_TASK.md`：短期任务状态，用于长任务、跨文件任务和上下文变重时的轻量交接。
- `CODING_NOTES.md`：事故和回归经验，记录原因、漏检点和后续检查。
- `SECRETS.local.md`：本地敏感信息，必须加入 `.gitignore`。

如果项目需要，可以额外创建：

- `DEVELOPMENT_RULES.md`：仓库文档尚未覆盖的代码规范。
- `RELEASE_CHECKLIST.md`：项目特定 release checklist。
- `SECURITY_CHECKLIST.md`：项目特定安全风险和检查项。

生成这些文件前先读 `references/project-files-template.md`。

新项目优先运行内置初始化脚本：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/project-governance/scripts/init_project_governance.py" /path/to/project
```

初始化脚本会创建缺失的治理文件并更新 `.gitignore`；除非传入 `--force`，否则不会覆盖已有文件。

维护 handoff 优先使用内置更新脚本：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/project-governance/scripts/update_handoff.py" active /path/to/project \
  --goal "..." --acceptance "..." --file "..." --command "..." --finding "..." --next-step "..."

python3 "${CODEX_HOME:-$HOME/.codex}/skills/project-governance/scripts/update_handoff.py" summary /path/to/project \
  --current-state "..." --recent-change "..." --decision "..." --open-item "..." --next-step "..."
```

脚本只格式化调用者提供的事实，不推断项目业务，不读取 secrets。

## 快捷命令 Short Commands

当用户输入以下短命令时，按本 skill 执行：

- `Init_skill` / `Init_project`：在当前仓库运行初始化检查。创建缺失的 `AGENTS.md`、`PROJECT_CONTEXT.md`、`SESSION_SUMMARY.md`、`ACTIVE_TASK.md`、`CODING_NOTES.md`、`SECRETS.local.md`，更新 `.gitignore`，不覆盖已有文件，不写具体业务事实或 secrets。
- `Handoff` / `总结交接`：优先用 `update_handoff.py` 维护项目交接文件。当前任务仍在推进时更新 `ACTIVE_TASK.md`；阶段完成或准备开新会话时更新 `SESSION_SUMMARY.md`；真实事故/回归经验写入 `CODING_NOTES.md`。

## 维护规则 Maintenance

- `PROJECT_CONTEXT.md` 保持稳定，只在项目事实变化时更新。
- `SESSION_SUMMARY.md` 保持简短和当前状态；过期内容要删除、合并或迁移。
- `ACTIVE_TASK.md` 只保存当前任务的工作草稿；任务结束后清空、归档或把长期信息合并到 `SESSION_SUMMARY.md` / `CODING_NOTES.md`。
- `CODING_NOTES.md` 只记录真实经验，按 symptom / root cause / missed check / prevention 结构追加。
- secrets 不进入提交文件；放进本地 ignored 文件或已有 secret manager。
- 如果某条经验适用于多个项目，把通用规则沉淀到公共 skill 或模板；项目里的具体证据留在 `CODING_NOTES.md`。

主动更新 handoff 的触发条件：

- 当前任务超过 30 分钟、跨多个文件或跨多个系统边界。
- 上下文里出现大段日志、HTML、diff、截图分析或长工具输出。
- 完成一个阶段，下一步依赖当前结论、命令结果或未提交修改。
- 用户说“卡了”“开新会话”“总结一下”“handoff”“接着做”。
- 即将执行高风险变更、部署、迁移、批量数据操作或外部副作用。

新会话启动策略：

- 如果仓库已有 `AGENTS.md`，先读它列出的项目文件。
- 如果仓库没有治理文件，且用户要长期协作、改代码、部署或减少长上下文依赖，建议或直接初始化治理文件。
- 只在公共 skill 中保留通用方法；真实项目事实写入项目文件。

## 上下文卫生 Context Hygiene

- 优先用 `rg` 定位，再用小范围 `sed -n` / 文件片段读取。
- 避免把完整大文件、完整日志、完整 diff 粘进上下文或最终回答。
- 大文件优先让用户给路径，由工具按需读取。
- 长输出先用 `--stat`、`head`、`tail`、失败过滤或关键词搜索收窄。
- 每次只读和当前任务相关的文件；读到无关分支时停止扩散。
- 长任务中先维护 `ACTIVE_TASK.md`，阶段完成后再整理到 `SESSION_SUMMARY.md`。

## 工程护栏 Engineering Guardrails

生成项目规则时，包含这些通用原则：

- 写完不等于完成；验证是任务的一部分。Implementation is not completion; validation is part of the task.
- 串起完整业务流：UI、API、backend、database、async jobs、external integrations、deployment。
- 用 source search 查重复规则、阈值、文案、env vars、statuses、API names。
- 前端检查改善体验；后端检查才是最终约束。
- 权限、可见性、数据隔离必须在 server-side enforcement。
- 日期/时间逻辑必须写清 timezone、精确 cutoff、before/at/after 行为。
- 通知逻辑必须定义 trigger、recipient、aggregation、deduplication、failure logging。
- 生产变更必须说明 deploy target、migration safety、restart、logs、health checks。

## 输出风格 Output Style

当用户要求创建可复用规则集时：

1. 说明哪些内容属于 public/global rules，哪些属于 per-project files。
2. 生成简洁模板，不写长篇教条。
3. 避免项目特定名称和 secrets。
4. 为敏感文件添加项目本地 ignore rules。
5. 说明这些文件后续如何维护。
