#!/usr/bin/env python3
"""SessionStart hook: reminds Claude about missing or oversized project memory files.

A project is any git repository next to the workspace (../<project>); its memory lives in
memory/<project>/MEMORY.md. Rules: AGENTS.md, section 6. Works on macOS and Ubuntu (stdlib only).
"""
import json
import os
import sys
from pathlib import Path

MAX_LINES = 300
MAX_BYTES = 30 * 1024

root = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())).resolve()
memory = root / "memory"

projects = sorted(
    d.name for d in root.parent.iterdir()
    if d.is_dir() and d != root and (d / ".git").exists()
)
missing = [p for p in projects if not (memory / p / "MEMORY.md").is_file()]

oversized = []
for f in sorted(memory.glob("*/MEMORY.md")) + [memory / "MEMORY_REL.md"]:
    if f.is_file():
        data = f.read_bytes()
        if len(data) > MAX_BYTES or data.count(b"\n") > MAX_LINES:
            oversized.append(str(f.relative_to(root)))

notes = []
if missing:
    notes.append(
        f"Projects without memory/<project>/MEMORY.md: {', '.join(missing)}. Per AGENTS.md section 6 (Triggers), "
        "create them from docs/templates/MEMORY_TEMPLATE.md before other work and report this to the lead. "
        "Do not create memory files inside the repositories."
    )
if len(projects) >= 2 and not (memory / "MEMORY_REL.md").is_file():
    notes.append(
        f"The workspace has {len(projects)} projects and no memory/MEMORY_REL.md. Check whether the projects are "
        "related; if so, create it from docs/templates/MEMORY_REL_TEMPLATE.md."
    )
if oversized:
    notes.append(
        f"Memory files over the size limit ({MAX_LINES} lines / {MAX_BYTES // 1024} KB): {', '.join(oversized)}. "
        "Archive them per AGENTS.md section 6 (Size control) before other work."
    )

if notes:
    json.dump({
        "systemMessage": f"MEMORY check: {len(missing)} missing, {len(oversized)} oversized",
        "hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": " ".join(notes)},
    }, sys.stdout)
