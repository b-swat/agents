---
name: task-new
description: Start a new development task — study project memory and code, then write the brief for ChatGPT (workflow steps 2–4). Use when the lead defines a new task. Arguments - project name, short task name in English, task statement.
---

# task-new — workflow steps 2–4

Rules: AGENTS.md section 3. Output documents: English Markdown, working directory only.

## Inputs

`<project>` (directory name in `../`), `<task-name>` (short English, kebab-case), the lead's task statement.
If something is missing — ask the lead.

## Steps

1. **Date and names.** `DATE=$(date +%Y-%m-%d)` (works on macOS and Ubuntu).
   Spec file: `docs/tasks/$DATE-<task-name>.md`; brief: `work/<project>/$DATE-<task-name>-brief.md`.
   Propose a short uppercase `<TAG>` for requirement IDs.
2. **Study memory.** Read `memory/<project>/MEMORY.md` (create it from `docs/templates/MEMORY_TEMPLATE.md` if missing)
   and `memory/MEMORY_REL.md` if it exists. Find earlier task specs in `docs/tasks/` related to the task.
3. **Study code** in `../<project>/`: modules, interfaces, existing tests and build files relevant to the task.
   First task in this repository → detect conventions (AGENTS.md section 1) and record them as `D-NNN`.
   Use the Explore agent for large repositories.
4. **Datasheets.** List the documents in `docs/sources/` relevant to the task. Missing ones → ask the lead
   (no internet search).
5. **Write the brief** `work/<project>/$DATE-<task-name>-brief.md`:

   ```markdown
   # Brief: <Task Title>

   | Field | Value |
   |---|---|
   | Date | YYYY-MM-DD |
   | Project | <project> |
   | Spec file to create | docs/tasks/YYYY-MM-DD-<task-name>.md |
   | Proposed type | Lite / Full — reason |
   | Proposed tag | <TAG> |

   ## Task (as stated by the lead)
   ## Code context (modules, files with path:line, current behavior, existing tests)
   ## Memory context (relevant C-/D- entries, earlier task specs)
   ## Relevant datasheets (docs/sources/..., sections)
   ## Constraints and risks known to the developer
   ## Questions for the lead
   ```

   Diagrams — Mermaid only.
6. **Report to the lead** (Russian): brief path, proposed type and tag, the spec file name ChatGPT must create,
   the template to use, questions, missing datasheets.
