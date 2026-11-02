---
name: task-implement
description: Implement an approved task with TDD — task branch from development, confirmed tests first (RED), implementation (GREEN, REFACTOR), full test run, commit (workflow steps 9–12). Use only after the lead approved the plan and confirmed the tests.
---

# task-implement — workflow steps 9–12

Rules: AGENTS.md section 3, docs/agent/testing.md, docs/agent/git.md.

## Gate check (stop if not met)

In the spec's "Approvals" table: plan `Approved` **and** tests `Confirmed`. If the lead approved in chat,
record it there first ("via chat"). Otherwise — stop and ask.

## Steps

1. **Branch.** In `../<project>/`: working tree clean; `git switch development`;
   `git switch -c task/YYYY-MM-DD-<task-name>` (or the repository's naming convention from `MEMORY.md`).
   No `development` branch → ask the lead. Write the branch name into the spec header.
2. **Tests (RED).** Add exactly the confirmed tests. Start the "Test Procedure" section as soon as the commands are known. Build and run; each new test must fail for the expected reason.
   Build/test commands: the repository's conventions from `MEMORY.md` or the project skill; default:
   `cmake -S . -B build-host -DBUILD_TESTING=ON && cmake --build build-host && ctest --test-dir build-host --output-on-failure`.
3. **Implement (GREEN → REFACTOR).** Minimal code per the approved plan; then refactor with all tests green.
   No documents in the repository (hook-enforced). Code comments reference `REQ-<TAG>-<NN>` where useful.
4. **Plan or tests must change?** Stop, update the plan/test sections (version + Revision History), re-export PDF,
   ask for re-approval.
5. **Full run.** Full test suite and build pass; no new warnings.
6. **Test Procedure.** Fill the spec's "Test Procedure" section in the strict format (docs/agent/testing.md,
   "Test Procedure Format"): Environment with real tool versions (`c++ --version`, `cmake --version`, GoogleTest
   version from the build files), Prerequisites for Ubuntu and macOS, exact `STEP-NN` commands with working directory,
   expected output and pass criterion, Test Results from the real run, Summary. Then validate:
   `python3 .claude/skills/task-implement/check_test_procedure.py docs/tasks/<file>.md` → must print `OK`.
7. **Commit** on the task branch: English, repository format (inspect `git log`), no additional signatures/trailers.
8. **Skill.** If build/test/flash commands for this repository were established for the first time, create
   `.claude/skills/<project>-build-test/SKILL.md` (macOS + Ubuntu) per AGENTS.md section 0.3.
9. **Report to the lead** (Russian): commits, test results, ready for `/task-close`.
