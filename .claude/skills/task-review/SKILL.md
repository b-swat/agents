---
name: task-review
description: Review a task spec written by ChatGPT — check it against local datasheets and check requirements for testability, then write the development plan and test plan and export the PDF (workflow step 6). Use when a new or updated task spec appears in docs/tasks/.
---

# task-review — workflow step 6

Rules: AGENTS.md section 3. Edit **only Claude's sections** of the spec (owners are stated in the template).

## Steps

1. **Read** the spec `docs/tasks/YYYY-MM-DD-<task-name>.md`, the brief in `work/<project>/`, and `memory/<project>/MEMORY.md`.
   Check that the file name, type (Lite/Full), tag and all template sections are present.
2. **Datasheet check** (Developer Review). For every requirement and numeric parameter:
   - find it in the **local** datasheets `docs/sources/` (section, page, table);
   - result: `confirmed` / `mismatch: <what the datasheet says>` / `no data — requested from lead`;
   - never search the internet; missing documents go to "Missing materials requested from the lead".
3. **Testability check.** For every requirement: can the acceptance criterion be turned into a GoogleTest test?
   Level `host` or `target`; if not testable — say why and what would make it testable.
4. **Findings in ChatGPT's sections** (wrong/missing/untestable requirements) are listed in the review, not fixed.
   If they block the plan → set status `In review` and report to the lead.
5. **Development Plan**: ordered steps with files/modules, what changes and why; risks.
6. **Test Plan**: one or more tests per requirement, named `Suite.REQ_<TAG>_<NN>_<Behavior>`; level; existing tests affected.
   100% requirements coverage (docs/agent/testing.md).
7. **Revision History**: add a row (version, date, Claude, "Developer review, plan, tests").
8. **PDF**: `python3 .claude/skills/export-pdf/md2pdf.py docs/tasks/<file>.md` (skill `export-pdf`).
9. **Memory**: `C-NNN` "Task spec reviewed", `D-NNN` for design decisions in the plan.
10. **Report to the lead** (Russian): spec and PDF paths, findings, missing materials, short plan and test summary,
    request: approve the plan and confirm the tests (in the "Approvals" table or in chat).
