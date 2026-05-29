# Codex Public Skills

[中文说明](README.zh-CN.md)

Reusable Codex skills for project governance, handoff, release validation, quality gates, backend engineering, and incident learning.

These skills are intentionally generic. They contain workflows, templates, and safety checks, but no project-specific business context, credentials, deployment targets, or private notes.

## Skills

- `project-governance`: initialize project collaboration files, reduce long-chat context dependence, and maintain handoff notes.
- `release-validation`: define acceptance criteria, run relevant validation, and report tested/untested items before saying done.
- `quality-gates`: select focused checks for risky changes such as permissions, forms, dates, notifications, migrations, integrations, deployments, and production data.
- `backend-engineering`: backend-focused guardrails for APIs, schemas, persistence, permissions, notifications, integrations, and deployments.

## What This System Covers

This is a small operating system for Codex collaboration, not a single prompt.

- Project memory: keep stable facts in `PROJECT_CONTEXT.md`, not in chat history.
- Active task state: keep long-running work in `ACTIVE_TASK.md`.
- Session handoff: keep resumable state in `SESSION_SUMMARY.md`.
- Incident learning: record real failures and regressions in `CODING_NOTES.md`.
- Release discipline: define acceptance criteria and validation evidence before saying done.
- Risk gates: add focused checks for high-risk areas.
- Backend contracts: inspect API, schema, persistence, permissions, logs, and side effects together.

`CODING_NOTES.md` is especially important. It turns problems into future checks:

- Symptom: what happened.
- Root Cause: why it happened.
- Missed Check: what should have caught it.
- Prevention: what to search, test, or verify next time.

## Install

Copy the skills into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/* "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Restart Codex or start a new session so the skills are discovered.

## Recommended Workflow

For a new repository, ask Codex:

```text
Init_project
```

This uses `project-governance` to create missing project files such as:

- `AGENTS.md`
- `PROJECT_CONTEXT.md`
- `SESSION_SUMMARY.md`
- `ACTIVE_TASK.md`
- `CODING_NOTES.md`
- `SECRETS.local.md`

Existing files are kept unless you explicitly force an overwrite. Sensitive files are added to `.gitignore`.

For long-running work, ask:

```text
Handoff
```

This updates `ACTIVE_TASK.md` or `SESSION_SUMMARY.md` so a new session can resume without relying on full chat history.

When a regression or validation miss happens, record the reusable lesson in `CODING_NOTES.md` so related future work starts by reading the known failure pattern.

## Included Scripts

`project-governance` includes deterministic helper scripts:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/project-governance/scripts/init_project_governance.py" /path/to/project
```

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/project-governance/scripts/update_handoff.py" active /path/to/project \
  --goal "..." \
  --acceptance "..." \
  --file "..." \
  --command "..." \
  --finding "..." \
  --next-step "..."
```

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/project-governance/scripts/update_handoff.py" summary /path/to/project \
  --current-state "..." \
  --recent-change "..." \
  --decision "..." \
  --open-item "..." \
  --next-step "..."
```

## Privacy Boundary

Keep reusable methods in public skills. Keep real project facts in project files.

Do not commit:

- credentials, API keys, tokens, passwords, private keys
- production server details
- customer or patient data
- private incident evidence
- local-only deployment notes

## Connect

If you are also exploring Codex skills, AI coding workflows, or project governance for AI agents, feel free to add me on WeChat.

<img src="wechat.jpg" alt="WeChat QR code" width="260">

## License

MIT
