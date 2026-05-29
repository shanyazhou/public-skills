---
name: quality-gates
description: Use before or during code changes that affect permissions, forms, dates/times, calculations, reports, notifications, scheduled jobs, migrations, external integrations, deployments, or production data. Provides high-risk checklists that complement release validation.
---

# Quality Gates

Use this skill to identify high-risk checks before coding, while testing, and before release.

## Core Rule

Every risky change needs a gate: a short list of conditions that must be true before the work is considered complete.

Prefer focused evidence over broad claims. If a check cannot be run safely, explain the reason and the substitute evidence.

## Scope Boundary

This skill selects extra checks for risky categories. It does not replace release-validation's end-to-end acceptance and final evidence contract.

When both skills apply, pick only the relevant risk sections below and fold the result into the final validation summary. Avoid copying the full checklist into the answer.

## Universal Gates

Apply these to most changes:

- Acceptance: define trigger, actor, expected result, failure behavior, and visible user outcome.
- Full path: inspect UI state, API payload, backend validation, database effects, async work, external calls, and final display.
- Duplicate rules: search for repeated thresholds, statuses, messages, field names, env vars, and helper functions.
- Authority: frontend may warn, backend must enforce.
- Regression: run the exact reported scenario or the closest safe fixture.

## Risk-Specific Gates

### Permissions And Visibility

- Check requester, owner, assignee, reviewer, admin, inactive users, and cross-team or cross-tenant access.
- Ensure server-side filtering matches the intended visibility rule.
- Verify legacy response fields cannot bypass new restrictions.

### Forms And Hidden State

- Ensure visible UI fields match submitted payload.
- Check default values, hidden fields, edit mode, copy/clone flows, draft reloads, and rejected/resubmitted records.
- Backend validation must use the same business meaning as frontend prechecks.

### Dates, Times, And Cutoffs

- Define timezone explicitly.
- Test before, at, and after cutoff.
- Check midnight, end of day, weekends, month boundaries, future dates, and past edits.
- Never infer local business dates from UTC serialization unless that is the actual requirement.

### Calculations, Reports, And Metrics

- Verify inclusion/exclusion rules, stale data, future data, overrides, and deleted/archived records.
- Check that snapshots or cached data are valid for the current cutoff.
- Compare at least one known input to a manually expected result.

### Notifications

- Define event, recipient, channel, aggregation, deduplication, and failure behavior.
- Check missing user mappings, disabled users, external permission errors, and dry-run/test-recipient paths.
- Avoid sending multiple messages when one aggregated message is required.

### Scheduled Jobs And Async Work

- Check first run, repeated run, no-op run, retry behavior, and persisted last-run markers.
- Ensure manual execution cannot create invalid future-effective data.
- Verify logs include enough context for production diagnosis.

### Migrations And Data Changes

- Make migrations idempotent when possible.
- Check existing data, nullable/default behavior, indexes, foreign keys, rollback or recovery path.
- Verify production and local schema assumptions before deploying.

### External Integrations

- Check credentials, scopes/permissions, rate limits, timeout behavior, retries, and error logging.
- Use sandbox, dry-run, or test recipients for side effects.
- Record operational steps when configuration outside the repo changes.

### Deployment

- Confirm target environment, intended files, env vars, migrations, restart command, logs, and health check.
- After deploy, verify the specific changed behavior on the real target.

## Final Evidence

When this skill applies, final responses should include:

- Gates selected.
- Checks run.
- Pass/fail result.
- Checks not run and why.
- Residual risk or follow-up.

Keep this evidence focused. Name the gate categories, not every checklist bullet, unless a missed edge case is the main issue.
