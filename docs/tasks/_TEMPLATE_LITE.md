# <Task Title>

<!-- Lite task spec: bug fixes and small changes.
     File: docs/tasks/YYYY-MM-DD-<task-name>.md ; PDF export copy next to it: YYYY-MM-DD-<task-name>.pdf
     Section owners: ChatGPT — 1–3; Claude — 4–6, 8, 10; Lead — 7; anyone re-testing — 9. -->

| Field | Value |
|---|---|
| Date | YYYY-MM-DD |
| Type | Lite |
| Tag | `<TAG>` |
| Project | `<project>` (`../<project>/`) |
| Branch | `task/YYYY-MM-DD-<task-name>` (or per repository convention) |
| Spec author | ChatGPT |
| Version | 0.1 |
| Status | Draft / In review / Plan approved / Tests approved / In progress / Done |

## 1. Task

What is wrong / what must change, and the expected behavior.

## 2. Context

Where in the code (from Claude's brief), related memory entries.

## 3. Requirements

| ID | Requirement | Source | Acceptance Criterion |
|---|---|---|---|
| REQ-<TAG>-01 | ... | ... | input → expected result |

## 4. Developer Review (Claude)

Datasheet check (if relevant), testability, missing materials requested from the lead.

## 5. Plan (Claude)

1. ...

## 6. Tests (Claude)

| Test (GoogleTest) | Covers | Checks |
|---|---|---|
| `Suite.REQ_<TAG>_01_<Behavior>` | REQ-<TAG>-01 | ... |

## 7. Approvals (Lead)

| Gate | Decision | Date |
|---|---|---|
| Plan (section 5) | Approved / Rejected | |
| Tests (section 6) | Confirmed / Rejected | |

## 8. Test Procedure (Claude)

_Filled and kept up to date during testing (steps 9–11). Strict format — checked by
`python3 .claude/skills/task-implement/check_test_procedure.py <spec.md>`. Anyone (Claude, ChatGPT, the lead) must be able
to repeat the tests from this section alone. Format rules: docs/agent/testing.md, "Test Procedure format"._

### 8.1 Environment

| Item | Value |
|---|---|
| OS | `<e.g. Ubuntu 24.04>` |
| Repository | `../<project>` |
| Branch | `task/YYYY-MM-DD-<task-name>` |
| Commit | `<hash>` |
| Compiler | `<name version>` |
| CMake | `<version>` |
| GoogleTest | `<version or source>` |
| Other tools | `<name version>` / `none` |

### 8.2 Prerequisites

| # | Ubuntu | macOS |
|---|---|---|
| 1 | `<install command>` | `<install command>` |

### 8.3 Steps

#### STEP-01: Configure

- Working directory: `../<project>`
- Command:

```sh
cmake -S . -B build-host -DBUILD_TESTING=ON
```

- Expected: `<exact expected output fragment or "exit code 0">`
- Pass criterion: `<exit code 0 and ...>`

#### STEP-02: Build

- Working directory: `../<project>`
- Command:

```sh
cmake --build build-host
```

- Expected: `exit code 0, no new warnings`
- Pass criterion: `exit code 0`

#### STEP-03: Run tests

- Working directory: `../<project>`
- Command:

```sh
ctest --test-dir build-host --output-on-failure
```

- Expected: `100% tests passed`
- Pass criterion: `exit code 0 and all tests from 8.4 reported as Passed`

### 8.4 Test Results

| Test | REQ | Result | Date | Run by |
|---|---|---|---|---|
| `Suite.REQ_<TAG>_01_<Behavior>` | REQ-<TAG>-01 | pass | YYYY-MM-DD | Claude |

### 8.5 Summary

| Total | Passed | Failed | Skipped | Full suite | Date | Run by |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | pass | YYYY-MM-DD | Claude |

## 9. Re-test Log

_Every repeated run of section 8 (by ChatGPT, the lead or Claude) adds one row. Steps are executed exactly as written;
any deviation is recorded. Row format: `R-NN | YYYY-MM-DD | <who> | <OS + version> | <commit> | STEP-01..STEP-NN | pass/fail | none or details`.
The `—` row means "no re-test yet" and is replaced by the first run._

| Run | Date | Run by | OS | Commit | Steps | Result | Deviations / failures |
|---|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — | — |

## 10. Completion Report (Claude)

- Branch → merged into `development` at `<merge commit>`; commits: ...
- REQ → test → result: ...
- MEMORY entries added: ...

## 11. Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 0.1 | YYYY-MM-DD | ChatGPT | Initial version |
