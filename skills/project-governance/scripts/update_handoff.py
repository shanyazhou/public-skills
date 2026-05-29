#!/usr/bin/env python3
"""Write structured handoff files for a project.

This script intentionally knows nothing about any specific project. Callers pass
task facts as arguments; the script only formats them into stable markdown.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


ACTIVE_TEMPLATE = """# ACTIVE_TASK.md - Active Task / 当前任务

短期任务草稿。任务完成后清空、归档，或把长期信息合并到 `SESSION_SUMMARY.md` / `CODING_NOTES.md`。

## Last Updated

{updated_at}

## 目标 Goal

{goal}

## 验收 Acceptance

{acceptance}

## 相关文件 Relevant Files

{files}

## 已运行命令 Commands Run

{commands}

## 当前结论 Decisions / Findings

{findings}

## 阻塞 Blockers

{blockers}

## 下一步 Next Steps

{next_steps}
"""


SUMMARY_TEMPLATE = """# SESSION_SUMMARY.md - Current Handoff / 当前交接

替换式摘要，不要追加完整聊天历史。

## Last Updated

{updated_at}

## 当前状态 Current State

{current_state}

## 近期变更 Recent Changes

{recent_changes}

## 决策 Decisions

{decisions}

## 未决事项 Open Items

{open_items}

## 下次会话检查 Next Session Checklist

{next_steps}
"""


def bullet_list(values: list[str]) -> str:
    cleaned = [v.strip() for v in values if v.strip()]
    if not cleaned:
        return "-"
    return "\n".join(f"- {v}" for v in cleaned)


def numbered_list(values: list[str]) -> str:
    cleaned = [v.strip() for v in values if v.strip()]
    if not cleaned:
        return "1."
    return "\n".join(f"{i}. {v}" for i, v in enumerate(cleaned, start=1))


def require_project_root(root: Path) -> Path:
    resolved = root.resolve()
    if not resolved.exists() or not resolved.is_dir():
        raise SystemExit(f"Project root is not a directory: {resolved}")
    return resolved


def write_active(args: argparse.Namespace) -> Path:
    root = require_project_root(Path(args.root))
    out = root / "ACTIVE_TASK.md"
    content = ACTIVE_TEMPLATE.format(
        updated_at=args.updated_at,
        goal=bullet_list(args.goal),
        acceptance=bullet_list(args.acceptance),
        files=bullet_list(args.file),
        commands=bullet_list(args.command),
        findings=bullet_list(args.finding),
        blockers=bullet_list(args.blocker),
        next_steps=numbered_list(args.next_step),
    )
    out.write_text(content, encoding="utf-8")
    return out


def write_summary(args: argparse.Namespace) -> Path:
    root = require_project_root(Path(args.root))
    out = root / "SESSION_SUMMARY.md"
    content = SUMMARY_TEMPLATE.format(
        updated_at=args.updated_at,
        current_state=bullet_list(args.current_state),
        recent_changes=bullet_list(args.recent_change),
        decisions=bullet_list(args.decision),
        open_items=bullet_list(args.open_item),
        next_steps=numbered_list(args.next_step),
    )
    out.write_text(content, encoding="utf-8")
    return out


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("root", nargs="?", default=".", help="Project root directory")
    parser.add_argument(
        "--updated-at",
        default=datetime.now().astimezone().isoformat(timespec="seconds"),
        help="Timestamp to write into the handoff file",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Update project handoff files.")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    active = subparsers.add_parser("active", help="Write ACTIVE_TASK.md")
    add_common_args(active)
    active.add_argument("--goal", action="append", default=[], help="Task goal")
    active.add_argument("--acceptance", action="append", default=[], help="Acceptance criterion")
    active.add_argument("--file", action="append", default=[], help="Relevant file path")
    active.add_argument("--command", action="append", default=[], help="Command already run")
    active.add_argument("--finding", action="append", default=[], help="Decision or finding")
    active.add_argument("--blocker", action="append", default=[], help="Current blocker")
    active.add_argument("--next-step", action="append", default=[], help="Next step")
    active.set_defaults(func=write_active)

    summary = subparsers.add_parser("summary", help="Write SESSION_SUMMARY.md")
    add_common_args(summary)
    summary.add_argument("--current-state", action="append", default=[], help="Current state")
    summary.add_argument("--recent-change", action="append", default=[], help="Recent change")
    summary.add_argument("--decision", action="append", default=[], help="Decision")
    summary.add_argument("--open-item", action="append", default=[], help="Open item")
    summary.add_argument("--next-step", action="append", default=[], help="Next session checklist item")
    summary.set_defaults(func=write_summary)

    args = parser.parse_args()
    out = args.func(args)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
