# Codex Public Skills

Reusable Codex skills for project governance, release validation, quality gates, and backend engineering.

These skills are intentionally generic. They contain workflows, templates, and safety checks, but no project-specific business context, credentials, deployment targets, or private notes.

## Skills

- `project-governance`: initialize project collaboration files, reduce long-chat context dependence, and maintain handoff notes.
- `release-validation`: define acceptance criteria, run relevant validation, and report tested/untested items before saying done.
- `quality-gates`: select focused checks for risky changes such as permissions, forms, dates, notifications, migrations, integrations, deployments, and production data.
- `backend-engineering`: backend-focused guardrails for APIs, schemas, persistence, permissions, notifications, integrations, and deployments.

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

## License

MIT
