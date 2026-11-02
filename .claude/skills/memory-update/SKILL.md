---
name: memory-update
description: Full update of local project memory — create missing MEMORY.md files, record unrecorded changes and decisions, refresh current state, update MEMORY_REL.md, enforce the size limit. Use on /memory-update or when the lead says «обнови локальную память».
---

# memory-update

Rules: AGENTS.md section 6. Memory lives in `memory/`, outside the repositories. English Markdown.

## Steps

1. **Projects**: git repositories next to the workspace —
   `python3 -c "from pathlib import Path; print([d.name for d in Path('..').iterdir() if (d/'.git').exists() and d.resolve()!=Path('.').resolve()])"`.
2. **Missing files**: create `memory/<project>/MEMORY.md` from `docs/templates/MEMORY_TEMPLATE.md`
   (Project Summary, Current State, `C-001`).
3. **Unrecorded changes**: compare the last `C-NNN` (date/commit) with `git -C ../<project> log` and with
   `docs/tasks/` specs and `docs/handoff/Q-*` answers. Append missing `C-NNN` / `D-NNN` marked `[RECONSTRUCTED]`.
   Never edit existing entries.
4. **Current State**: rewrite briefly (status, done, in progress, blocked).
5. **Relations**: shared code, protocols, hardware, interfaces between projects → create/update `memory/MEMORY_REL.md`
   from `docs/templates/MEMORY_REL_TEMPLATE.md` (`R-NNN`, `XC-NNN`, `XD-NNN`).
6. **Size control**: for each memory file over 300 lines or 30 KB — move the oldest entries verbatim to
   `memory/<project>/archive/MEMORY-YYYY.md` (`memory/archive/MEMORY_REL-YYYY.md`): keep the latest 50 changes and
   all `Accepted` decisions; add the moved ID range to the "Archive" table.
7. **Report to the lead** (Russian): files created, entries added, files archived, what could not be determined.
