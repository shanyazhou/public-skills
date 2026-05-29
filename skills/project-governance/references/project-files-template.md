# Project Files Template / 项目文件模板

初始化项目治理文件时使用这些模板。根据真实代码调整名称和章节；不要编造 secrets。

## AGENTS.md

```markdown
# AGENTS.md - Assistant Handoff / 助手交接入口

这是 assistant 在本仓库工作的项目级指南。

新会话开始时，先读：

1. `PROJECT_CONTEXT.md`：稳定项目事实。
2. `SESSION_SUMMARY.md`：当前交接状态。
3. `ACTIVE_TASK.md`：如果存在未完成任务，先读当前任务状态。
4. `CODING_NOTES.md`：修改涉及历史事故/回归的逻辑前先读。
5. 现有仓库规则文件，如 `CLAUDE.md`、`CONTRIBUTING.md` 或架构文档。

上下文策略 Context strategy:

- 不依赖完整聊天历史。
- 稳定事实放进 `PROJECT_CONTEXT.md`。
- 当前交接状态放进 `SESSION_SUMMARY.md`。
- 当前任务草稿放进 `ACTIVE_TASK.md`。
- 事故和回归经验放进 `CODING_NOTES.md`。
- secrets 放进本地 ignored 文件或 secret manager。
- 代码变更或 release 前，先定义 acceptance criteria 并运行相关 validation。

`SESSION_SUMMARY.md` 维护方式：

- 它是替换式摘要，不是 append-only 聊天记录。
- 保留当前状态、近期决策、open items 和 next steps。
- 过期细节要删除、合并或迁移。
- 稳定事实移到 `PROJECT_CONTEXT.md`。
- 可复用经验移到 `CODING_NOTES.md`。

主动更新 handoff 的触发条件：

- 当前任务超过 30 分钟、跨多个文件或跨多个系统边界。
- 上下文里出现大段日志、HTML、diff、截图分析或长工具输出。
- 完成一个阶段，下一步依赖当前结论、命令结果或未提交修改。
- 用户说“卡了”“开新会话”“总结一下”“handoff”“接着做”。
- 即将执行高风险变更、部署、迁移、批量数据操作或外部副作用。

上下文卫生：

- 优先用 `rg` 定位，再读取小范围文件片段。
- 避免把完整大文件、完整日志、完整 diff 粘进聊天或最终回答。
- 大文件优先通过路径按需读取。
- 长输出先用 `--stat`、`head`、`tail`、失败过滤或关键词搜索收窄。
```

## PROJECT_CONTEXT.md

```markdown
# PROJECT_CONTEXT.md - Project Context / 项目上下文

这里存放协作本项目所需的稳定信息。

## 概览 Overview

- Product / 产品：
- Goal / 目标：
- Main users / 主要用户：
- Tech stack / 技术栈：
- Repository / 仓库：
- Environments / 环境：

## 结构 Structure

- `path/`: purpose
- `path/`: purpose

## 本地运行 Local Run

```bash
# commands
```

## 测试与验证 Test And Validation

```bash
# commands
```

## 部署 Deploy

- Target / 目标：
- Deploy path / 部署路径：
- Process manager / 进程管理：
- Release command or CI/CD / 发布命令：
- Health check / 健康检查：

## 敏感信息 Sensitive Information

- secrets 存在本地 ignored 文件或 secret manager。
- 不提交 passwords、tokens、private keys 或 production credentials。

## 高风险区域 High-Risk Areas

- Dates/time/cutoffs / 日期时间与截止点：
- Permissions/visibility / 权限与可见性：
- External integrations / 外部集成：
- Async jobs / 异步任务：
- Data migrations / 数据迁移：
```

## SESSION_SUMMARY.md

```markdown
# SESSION_SUMMARY.md - Current Handoff / 当前交接

替换式摘要，不要追加完整聊天历史。

## Last Updated

-

## 当前状态 Current State

-

## 近期变更 Recent Changes

-

## 决策 Decisions

-

## 未决事项 Open Items

-

## 下次会话检查 Next Session Checklist

1.
2.
3.
```

## ACTIVE_TASK.md

```markdown
# ACTIVE_TASK.md - Active Task / 当前任务

短期任务草稿。任务完成后清空、归档，或把长期信息合并到 `SESSION_SUMMARY.md` / `CODING_NOTES.md`。

## Last Updated

-

## 目标 Goal

-

## 验收 Acceptance

-

## 相关文件 Relevant Files

-

## 已运行命令 Commands Run

-

## 当前结论 Decisions / Findings

-

## 阻塞 Blockers

-

## 下一步 Next Steps

1.
2.
3.
```

## CODING_NOTES.md

```markdown
# CODING_NOTES.md - Incident And Regression Notes / 事故与回归记录

记录真实问题和可复用经验。修改相关逻辑前先读这里。

## YYYY-MM-DD: Short Title / 简短标题

### Symptom / 现象

发生了什么，表现是什么。

### Root Cause / 根因

为什么会发生。

### Missed Check / 漏检

什么检查本可以发现它。

### Prevention / 预防

- 后续检查。
- 需要搜索的关键词或代码路径。
- 需要运行的 test cases。
```

## SECRETS.local.md

```markdown
# SECRETS.local.md - Local Sensitive Notes / 本地敏感信息

这个文件只保存在本地，必须被 git ignore。

## 环境 Environments

- Production:
- Staging:
- Local:

## 访问 Access

- Server:
- Database:
- Third-party services:
```

## .gitignore additions / 忽略规则

```gitignore
SECRETS.local.md
SESSION_SUMMARY.local.md
*.local.md
```
