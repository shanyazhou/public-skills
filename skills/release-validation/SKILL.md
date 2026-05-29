---
name: release-validation
description: Use in any project when making code changes, bug fixes, deployments, production changes, scheduled jobs, integrations, notifications, calculations, metrics, or any task the user expects to work end-to-end. Requires defining acceptance criteria, running relevant validation before saying done, and reporting tested/untested items.
---

# Release Validation

## Core Rule

Do not treat implementation as completion. For any code change or deployment, finish only after:

1. Acceptance criteria are explicit.
2. The relevant business flow has been tested.
3. Edge cases and failure paths have been considered.
4. The final answer says what was tested, what was not tested, and any remaining risk.

If a test would send real user notifications, mutate production data, or create external side effects, use dry-run, test recipients, a safe fixture, or explain exactly what was not run.

## Scope Boundary

This skill owns the end-to-end completion contract: acceptance criteria, validation evidence, tested/untested items, and residual risk.

When quality-gates also applies, use it to choose risk-specific checks, but merge the final evidence into one concise validation section instead of repeating two reports.

When a domain skill such as backend-engineering also applies, let the domain skill guide what to inspect; this skill decides whether the work is complete enough to say done.

## Workflow

### 1. Before Coding

Write or infer a short acceptance checklist. Keep it concrete:

- Trigger/event.
- Expected actor and recipient.
- Data conditions.
- Time/date boundary if relevant.
- Frontend visible state and backend payload if relevant.
- Failure behavior.

For ambiguous requirements, ask only if a wrong assumption would be risky. Otherwise state the assumption and proceed.

### 2. During Development

Trace the full path, not only the file being edited:

- Frontend validation/state.
- API payload.
- Backend validation.
- Database reads/writes.
- Async jobs, timers, queues, or external APIs.
- UI refresh or user-visible result.

Search for duplicate rule copies. Use `rg` for thresholds, messages, function names, statuses, dates, env vars, and API names.

### 3. Required Test Layers

Always run the cheapest applicable checks:

- Syntax/type checks for changed code.
- Unit or focused tests if present.
- Direct API or service invocation for backend behavior.
- UI or payload verification for frontend changes.
- Database migration verification for schema changes.
- Logs after restart/deploy.

For production deployments:

- Deploy/sync only intended files.
- Run migrations idempotently.
- Restart with updated environment if env changed.
- Health check the real service.
- Verify the specific changed behavior on the deployed target.

### 4. Edge Case Checklist

Use the relevant subset:

- Date/time: local timezone, UTC, exact cutoff times, before/at/after cutoff, midnight, end of day, cross-day, weekends, holidays, month boundaries.
- Scheduled jobs: before trigger, at trigger, after trigger, no duplicate run, persisted last-run marker.
- Notifications: correct recipient, no extra recipients, aggregation/deduplication, missing user mapping, external permission errors, dry-run path.
- Scoring/metrics: future dates excluded, cutoff already reached, cutoff not reached, stale/early data ignored, adjustment/override behavior.
- Forms: visible UI state equals submitted payload, hidden fields cannot become stale, frontend precheck matches backend final check.
- Roles/permissions: requester, assignee, reviewer, approver, admin, owner, inactive or disabled users.
- Data state: draft, submitted, approved, rejected, assigned, deleted, archived, or otherwise terminal records.
- Migrations: existing data, repeat execution, nullable defaults, index/foreign-key safety.

### 5. Final Response Contract

Before final, include high-signal verification:

- What changed.
- What exact checks ran.
- What passed.
- What was not tested and why.
- Any operational notes such as env vars, migrations, restart, or production health.

Never say only "done" for a code or production change.

Keep the final evidence compact. If multiple skills were used, do not list each skill separately unless that helps the user understand residual risk.

## Failure Protocol

If a user reports a regression after release:

1. Acknowledge it as a validation miss.
2. Inspect logs/data before guessing.
3. Fix the issue.
4. Add or update a note/checklist item in the project notes when the failure reveals a reusable lesson.
5. Re-run the relevant acceptance case on the actual target.
