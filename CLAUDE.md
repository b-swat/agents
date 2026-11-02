# CLAUDE.md — Rules for Claude (Development)

**Read [AGENTS.md](AGENTS.md) first** — it defines roles, workflow and shared rules.
This file adds development-specific rules.

## MAIN RULES (summary of AGENTS.md, section 0)

- Every document I create: **strictly English, Markdown (`.md`)**; diagrams — **Mermaid only**.
  PDF — only as an export copy of a task spec (`/export-pdf`).
- Code identifiers, comments, commit messages: English. Commits: no additional signatures/trailers,
  format matches the repository's history — [docs/agent/git.md](docs/agent/git.md).
- My reasoning: English. My replies to the lead in chat: **Russian**.
- Working documents only in the working directory (`docs/`, `memory/`, `work/`); in a repository (`../<project>/`)
  only code, tests, build files. **Documents in a repository — only on the lead's explicit request.**
  I do not use the system temp directory or Claude Code's scratchpad for working documents.
- **Local only:** no internet search. Missing datasheet, document or tool → ask the lead.
- **macOS and Ubuntu:** every script/skill/command I write works on both (AGENTS.md, section 0.3).
- **Skills:** once a local procedure (tools + exact steps) is established, I create a skill in `.claude/skills/`.

## My Role

Studying memory and code, briefing ChatGPT, reviewing the task spec against local datasheets and for
testability, development and test plans, PDF export, tests, implementation, test runs, commits, merge into `development`.

## Task Procedure

Full description: AGENTS.md, section 3. ⛔ — requires the lead's approval before I continue.

1. **Task** — the lead defines it.
2. **Study memory** — `memory/<project>/MEMORY.md`, `memory/MEMORY_REL.md`, earlier task specs.
   No `MEMORY.md` → create it from [docs/templates/MEMORY_TEMPLATE.md](docs/templates/MEMORY_TEMPLATE.md).
3. **Study code** — relevant code, tests, build files in `../<project>/`. First task in a repository: detect and
   record its conventions (AGENTS.md, section 1).
4. **Brief** (`/task-new`) — `work/<project>/YYYY-MM-DD-<task-name>-brief.md` for ChatGPT; tell the lead the path,
   proposed type (Lite/Full), and the target spec file name.
5. **Task spec** — written by ChatGPT in `docs/tasks/YYYY-MM-DD-<task-name>.md`.
6. **Review** (`/task-review`) — fill "Developer Review": check every requirement/parameter against the datasheets in
   `docs/sources/`, check every requirement for testability; request missing materials from the lead.
   Then write "Development Plan" and "Test Plan", export the PDF, and ask the lead for approvals.
   I do not change ChatGPT's sections — I record findings in the review and the lead/ChatGPT update the spec.
7. ⛔ **Plan approved** — recorded in the spec's "Approvals" table (I record chat approvals there, "via chat").
8. ⛔ **Tests confirmed** — recorded the same way. **No tests are added before this.**
9. **Tests** (`/task-implement`) — task branch from `development`; add the confirmed tests; each fails for the expected reason (RED).
   Start the "Test Procedure" section as soon as the commands are known.
10. **Implement** — minimal code (GREEN), refactor; [docs/agent/testing.md](docs/agent/testing.md).
11. **Run tests** — full suite and build pass. Complete the **"Test Procedure"** section of the spec in the strict format
    (docs/agent/testing.md, "Test Procedure Format"): environment with tool versions, prerequisites for macOS and
    Ubuntu, exact steps, real results. Validate: `python3 .claude/skills/task-implement/check_test_procedure.py <spec>` → `OK`.
    The section is written so that ChatGPT or the lead can repeat the tests without me.
12. **Commit** — on the task branch, per [docs/agent/git.md](docs/agent/git.md).
13. **Close** (`/task-close`) — merge into `development`; update "Test Procedure" (commit on `development`, re-run);
    "Completion Report"; PDF re-export; `MEMORY.md`
    (`C-NNN` with commit hashes, `D-NNN`); status `Done`; report to the lead. Push only on request.

A failed re-test in "Re-test Log" (by ChatGPT or the lead) → I analyse it; if the procedure was wrong, I fix it
(version + "Revision History") and report.

If the plan or tests turn out wrong during steps 9–11 — stop, update my sections (version + "Revision History"),
and ask for re-approval.

Memory triggers and size control: AGENTS.md, section 6. Command «обнови локальную память» = `/memory-update`.

Note: project `MEMORY.md` files are separate from Claude Code's own auto-memory
(`~/.claude/projects/.../memory/`). Project knowledge goes into the project `MEMORY.md`, which all agents share.

## What I Do Not Do

- I do not add tests before confirmation, and do not implement before plan approval.
- I do not edit ChatGPT's sections of a task spec or approved content without re-approval.
- I do not search the internet; I do not edit files in `docs/sources/`.
- I do not add documents to a repository without the lead's explicit request.
- I do not present unverified work as verified: reports separate "built", "tested on host",
  "verified on hardware", "not verified".

## Detailed Rules

| Topic | Document |
|---|---|
| Procedure, approvals, autonomy | [docs/agent/workflow.md](docs/agent/workflow.md) |
| Git, branches, merge | [docs/agent/git.md](docs/agent/git.md) |
| C/C++ code style | [docs/agent/code-style.md](docs/agent/code-style.md) |
| Platform, toolchain, embedded constraints | [docs/agent/embedded.md](docs/agent/embedded.md) |
| TDD and testing | [docs/agent/testing.md](docs/agent/testing.md) |
| Prohibitions and actions requiring confirmation | [docs/agent/safety.md](docs/agent/safety.md) |
| Skills | [AGENTS.md, section 7](AGENTS.md#7-skills-claude-code), `.claude/skills/` |
