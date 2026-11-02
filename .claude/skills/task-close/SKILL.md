---
name: task-close
description: Close a task — merge the task branch into development, fill the completion report, re-export the PDF and update project memory (workflow step 13). Use after task-implement finished with all tests passing.
---

# task-close — workflow step 13

Rules: AGENTS.md section 3, docs/agent/git.md ("Merge into development").

## Steps

1. **Check** on the task branch: clean working tree, full test suite and build pass.
2. **Merge** into local `development` using the repository's convention (default `git merge --no-ff`), message per
   commit rules (English, no additional signatures). No fetch/pull/push unless the lead asked.
3. **Re-run** the full test suite and build on `development`.
   Merge conflict or failure → `git merge --abort` if still merging, stop, report to the lead.
4. **Test Procedure**: update Environment (Branch `development`, merge commit) and Test Results/Summary from the
   run on `development`; validate with `python3 .claude/skills/task-implement/check_test_procedure.py <spec>` → `OK`.
5. **Completion Report** in the spec (Claude's section): branch → merge commit, commits, REQ → test → result →
   verification level, deviations, follow-ups, MEMORY entries. Status `Done`. Revision History row.
6. **PDF**: `python3 .claude/skills/export-pdf/md2pdf.py docs/tasks/<file>.md`.
7. **Memory** `memory/<project>/MEMORY.md`: `C-NNN` per commit/merge (with hashes and spec reference),
   `D-NNN` for decisions taken during implementation, refresh "Current State"; `MEMORY_REL.md` if cross-project.
   Check the size limit (AGENTS.md section 6, "Size control").
8. **Report to the lead** (mention that ChatGPT can re-test by the Test Procedure) (Russian): merge commit, results, open follow-ups. Push only if requested.
