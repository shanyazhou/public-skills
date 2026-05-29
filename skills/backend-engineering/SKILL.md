---
name: backend-engineering
description: Use for backend code changes, reviews, incident fixes, API/server/database work, Prisma or SQL schema changes, migrations, permissions, notifications, scheduled jobs, external integrations, deployments, and any task where Codex must act like a senior backend engineer with strict data-contract, type, safety, and validation discipline.
---

# Backend Engineering

## Operating Posture

Treat backend work as a contract, not just code. Before saying done, prove the data model, API boundary, persistence, side effects, and deployment behavior agree.

Use this skill together with release-validation for changes, and quality-gates for high-risk areas such as permissions, notifications, integrations, migrations, or production data.

If multiple skills apply, avoid duplicating their checklists in the final answer. Use this skill for backend-specific inspection, release-validation for completion evidence, and quality-gates only for the relevant risk categories.

## First Pass

1. Read the project rules and environment docs before editing.
2. Check `git status --short`; preserve unrelated user changes.
3. Trace the full path: route/controller, service, database schema, migrations, clients, jobs, logs, and deployment target.
4. Define acceptance criteria before coding:
   - trigger/request
   - actor and authorization
   - input payload and response contract
   - database rows touched
   - external side effects
   - failure behavior and logs
5. Search for duplicate logic before changing one copy:
   - field names, status strings, env vars, role checks, date parsing, notification scene names, relation keys.

## Schema And Type Discipline

Never guess a field type from memory. Verify every field against all layers:

- database schema or Prisma model
- migration SQL
- generated/client types
- route params and request body parsing
- service function signatures
- frontend/API consumer types
- existing rows if production/test data already exists

When a value crosses a boundary, normalize once and keep the contract explicit.

Common hard rules:

- IDs must have one canonical type. Do not use `String` in one table and `Int` in another unless the external source truly differs and the conversion point is named.
- `clinicId`, `userId`, `recordId`, and similar identifiers need a documented canonical type per system.
- Date/time fields must define timezone, storage format, display format, and range-boundary behavior.
- Money, score, count, and enum/status fields must be validated server-side.
- Nullable fields must be intentional. Check old rows, defaults, and response omission behavior.
- JSON fields need shape validation at write time and safe parsing at read time.
- Do not let frontend-only TypeScript hide backend contract drift.

Before changing schema:

- inspect current model and migrations
- inspect actual data shape where possible
- plan nullable/default/backfill/index behavior
- ensure migration is safe to run repeatedly or has a recovery path
- regenerate clients if needed
- run build/type checks after generation

## API Contract Rules

For every route or endpoint change:

- Validate and coerce request input at the server boundary.
- Return stable response fields; do not silently change type, name, or omission behavior.
- Keep error messages useful and localized to the app style when user-facing.
- Ensure auth middleware and server-side authorization enforce the rule; UI checks are only ergonomics.
- Check all consumers before removing or changing fields.
- Include idempotency for retry-prone writes, especially mobile submit flows.
- Make partial failure behavior explicit: all-or-nothing, best-effort, retry, or logged skip.

When proxying legacy systems, separate external shape from internal shape. Name adapters clearly and keep conversion in one place.

## Persistence And Queries

Review queries for both correctness and blast radius:

- tenant/clinic/user scoping
- role and ownership checks
- deleted/archived/status filters
- ordering and pagination
- duplicate creation under retry/concurrency
- indexes for new filters or joins
- N+1 queries on list endpoints
- exact date windows with before/at/after behavior

When writing notifications or audit-like records, define deduplication and read semantics. Avoid “generated in memory” and “persisted row” ambiguity.

## Notifications And Integrations

For notifications, always document and verify:

- event trigger
- business candidate recipients
- channel-specific filtering
- test/development safety gates
- dedupe/aggregation
- success, failure, and skip logs
- missing mapping behavior
- environment prefixing for non-production messages

For external services:

- keep credentials in env or secret manager only
- never commit secrets
- avoid broad test sends
- use dry-run or lookup-only checks before real sends
- log enough context without logging secrets
- distinguish business recipient rules from transport routing rules

Example: external organization or workspace routing should be a transport detail. Test recipient whitelists should be one explicit notification safety gate, not mixed with role/permission whitelists.

## Deployment And Validation

Before final:

1. Run the cheapest relevant local checks:
   - server build/typecheck
   - focused tests
   - migration generation/validation if schema changed
2. If deploying:
   - sync only intended files
   - update env vars deliberately
   - run build on target
   - restart the intended process
   - health check the actual URL
   - inspect logs for the changed path
3. Report:
   - what changed
   - what checks passed
   - what was not tested and why
   - remaining operational risk

Do not claim a backend change is done merely because TypeScript compiled.

## Review Checklist

Use this checklist when reviewing backend code or before finalizing a backend patch:

- Are identifier types consistent across schema, code, and API?
- Are enums/statuses centralized or at least searched globally?
- Are request inputs validated server-side?
- Are permissions enforced server-side?
- Are database writes scoped to the correct tenant/clinic/user?
- Are old rows and nulls handled?
- Are retries/idempotency handled for mobile writes?
- Are external side effects gated in test/dev?
- Are logs sufficient to reconstruct recipient/candidate/success/failure?
- Are secrets excluded from committed files and final answers?
- Did validation run on the same environment the user will use?
