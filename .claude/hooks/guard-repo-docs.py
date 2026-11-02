#!/usr/bin/env python3
"""PreToolUse hook (Write|Edit|MultiEdit|NotebookEdit): documents inside repositories only on the lead's request.

A write of a document file (.md, .rst, .adoc, .pdf, .doc[x], .odt, .rtf) inside a git repository outside the
workspace is not allowed silently: the lead is asked to confirm. Rules: AGENTS.md, section 0.2.
Works on macOS and Ubuntu (stdlib only).
"""
import json
import os
import sys
from pathlib import Path

DOC_SUFFIXES = {".md", ".markdown", ".rst", ".adoc", ".pdf", ".doc", ".docx", ".odt", ".rtf"}

event = json.load(sys.stdin)
tool_input = event.get("tool_input", {})
path_str = tool_input.get("file_path") or tool_input.get("notebook_path")
if not path_str:
    sys.exit(0)

root = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())).resolve()
path = Path(path_str).resolve()
if path.suffix.lower() not in DOC_SUFFIXES or path == root or root in path.parents:
    sys.exit(0)

repo = next((p for p in path.parents if (p / ".git").exists()), None)
if repo is None:
    sys.exit(0)

json.dump({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": (
            f"Document inside repository {repo.name}: {path.name}. "
            "Documents in repositories are allowed only on the lead's explicit request (AGENTS.md, section 0.2)."
        ),
    }
}, sys.stdout)
